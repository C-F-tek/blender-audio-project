"""Artifact discovery and quality aggregation for heap final proposals."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ia_carmine.product.heap_final_proposals.common import (
    provider_report_execution_performed,
    read_json,
    read_text,
    repo_rel,
)
from ia_carmine._shared.file_backed_transport import text_from_ref_or_tail
from ia_carmine.runtime.heap_gate.gpu1_one_turn_gate import (
    ONE_TURN_SUMMARY_FIELDS,
    strict_one_turn_gate_passed,
)

PROVIDER_REPORT_LANES = {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}
PROVIDER_REPORT_SKIP_KINDS = {
    "provider_launch_manifest",
    "provider_role_coexistence",
    "provider_runtime_plan",
    "provider_teamwork_leader_packet",
}


def append_artifact_ref(refs: list[str], value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        return
    normalized = value.replace("\\", "/")
    if normalized not in refs:
        refs.append(normalized)


def startup_artifact_refs(startup_manifest: dict[str, Any], report: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    artifacts = (
        startup_manifest.get("artifacts")
        if isinstance(startup_manifest.get("artifacts"), dict)
        else {}
    )
    for value in artifacts.values():
        append_artifact_ref(refs, value)
    for execution in startup_manifest.get("tool_executions") or []:
        if not isinstance(execution, dict):
            continue
        for key in ("useful_artifact_paths", "existing_artifact_paths", "artifact_paths"):
            for value in execution.get(key) or []:
                append_artifact_ref(refs, value)
        for summary in execution.get("artifact_summaries") or []:
            if isinstance(summary, dict):
                append_artifact_ref(refs, summary.get("path"))
        for artifact in execution.get("artifacts") or []:
            append_artifact_ref(refs, artifact.get("path") if isinstance(artifact, dict) else artifact)
    output_contract = (
        report.get("real_run_output_contract")
        if isinstance(report.get("real_run_output_contract"), dict)
        else {}
    )
    for value in output_contract.get("context_artifact_refs") or []:
        append_artifact_ref(refs, value)
    for value in report.get("context_artifact_refs") or []:
        append_artifact_ref(refs, value)
    return refs


def compute_product_causality(
    *,
    report: dict[str, Any],
    startup_manifest: dict[str, Any],
    startup_reconciliation: dict[str, Any],
    proposals: list[dict[str, Any]],
    provider_reports: list[dict[str, Any]],
) -> dict[str, Any]:
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    output_contract = (
        report.get("real_run_output_contract")
        if isinstance(report.get("real_run_output_contract"), dict)
        else {}
    )
    product_status = metrics.get("product_status") or output_contract.get("product_status")
    startup_contract = (
        startup_manifest.get("contract")
        if isinstance(startup_manifest.get("contract"), dict)
        else {}
    )
    input_ready = bool(
        startup_manifest.get("input_ready_before_heap") is True
        or startup_contract.get("input_ready_before_heap") is True
    )
    artifact_refs = startup_artifact_refs(startup_manifest, report)
    provider_execution = bool(
        report.get("provider_work_verified")
        or metrics.get("provider_work_verified")
        or output_contract.get("provider_work_verified")
        or any(item.get("provider_work_verified") for item in provider_reports)
    )
    proposal_artifacts = (
        report.get("proposal_iteration_artifacts")
        if isinstance(report.get("proposal_iteration_artifacts"), list)
        else []
    )
    proposal_count = len(proposals) or len(proposal_artifacts)
    reconciliation_passed = (
        startup_reconciliation.get("passed") is True if startup_reconciliation else None
    )
    failed_reasons: list[str] = []
    unknown_reasons: list[str] = []
    if report.get("fallback_heap_report"):
        failed_reasons.append("fallback heap report used")
    if startup_manifest and not input_ready:
        failed_reasons.append("startup manifest is not input_ready_before_heap")
    if startup_manifest and not artifact_refs:
        failed_reasons.append("startup/context artifact refs are empty")
    if product_status == "ready" and not provider_execution:
        failed_reasons.append("product_status=ready without provider execution evidence")
    if product_status == "ready" and proposal_count == 0:
        failed_reasons.append("product_status=ready without proposal iteration artifacts")
    if provider_execution and not any(
        item.get("accepted") and strict_one_turn_gate_passed(item)
        for item in proposals
    ):
        failed_reasons.append("provider execution without accepted gpu1 one-turn runtime gate")
    if not startup_manifest:
        unknown_reasons.append("startup manifest missing")
    if not report:
        unknown_reasons.append("heap report missing")
    if reconciliation_passed is False:
        unknown_reasons.append("startup reconciliation failed or was not usable")
    if product_status != "ready" and proposal_count == 0:
        unknown_reasons.append("no proposal chunks available for causal inspection")
    if failed_reasons:
        status = "failed"
        passed: bool | None = False
        reasons = failed_reasons
    elif unknown_reasons:
        status = "unknown"
        passed = None
        reasons = unknown_reasons
    else:
        status = "passed"
        passed = True
        reasons = []
    return {
        "schema_version": 1,
        "kind": "external_heap_product_causality",
        "product_causality_status": status,
        "product_causality_passed": passed,
        "product_status": product_status,
        "startup_input_ready_before_heap": input_ready,
        "startup_artifact_ref_count": len(artifact_refs),
        "provider_execution_evidence_present": provider_execution,
        "proposal_artifact_count": proposal_count,
        "startup_reconciliation_passed": reconciliation_passed,
        "composer_packaging_performed": True,
        "causality_reasons": reasons,
    }


def list_proposals(run_dir: Path) -> list[dict[str, Any]]:
    proposal_dir = run_dir / "team_context" / "proposal_iterations"
    proposals: list[dict[str, Any]] = []
    if not proposal_dir.exists():
        return proposals
    for json_path in sorted(proposal_dir.glob("heap_proposal_revision_*.json")):
        data = read_json(json_path)
        md_path = json_path.with_suffix(".md")
        impl = (
            data.get("implementation_quality")
            if isinstance(data.get("implementation_quality"), dict)
            else {}
        )
        progress = (
            data.get("proposal_progress") if isinstance(data.get("proposal_progress"), dict) else {}
        )
        quality_errors: list[str] = []
        for source in (impl, progress):
            for error in source.get("errors") or []:
                quality_errors.append(str(error))
        proposals.append(
            {
                "name": json_path.name,
                "json_path": json_path,
                "markdown_path": md_path if md_path.exists() else None,
                "block_id": data.get("block_id"),
                "revision": data.get("revision"),
                "source": data.get("source"),
                "quality_passed": data.get("quality_passed"),
                "accepted": data.get("quality_passed") is True,
                "reject_reason": (
                    "; ".join(quality_errors)
                    if quality_errors
                    else (
                        "quality_passed is not true"
                        if data.get("quality_passed") is not True
                        else ""
                    )
                ),
                "implementation_quality": impl,
                "proposal_progress": progress,
                "response_file_reference_quality": data.get("response_file_reference_quality", {}),
                "target_files": data.get("target_files", []),
                "declared_target_files": data.get("declared_target_files", []),
                "verified_declared_target_files": data.get("verified_declared_target_files", []),
                "allowlist_candidate_files": data.get("allowlist_candidate_files", []),
                "rejected_unverified_refs": data.get("rejected_unverified_refs", []),
                "validation_commands": data.get("validation_commands", []),
                "rejected_validation_refs": data.get("rejected_validation_refs", []),
                "provider_execution_performed": data.get("provider_execution_performed", False),
                "gpu0_review": data.get("gpu0_review", []),
                "npu_micro_task_piece": data.get("npu_micro_task_piece", []),
                "npu_workload_audit": data.get("npu_workload_audit", {}),
                "anchored_source_candidates": data.get("anchored_source_candidates", []),
                "response_text_ref": data.get("response_text_ref", {}),
                "response_text_chars": data.get("response_text_chars", 0),
                "response_text_sha256": data.get("response_text_sha256", ""),
                "response_text_tail": data.get("response_text_tail", ""),
                **{
                    key: data.get(key)
                    for key in ONE_TURN_SUMMARY_FIELDS
                    if key in data
                },
            }
        )
    return proposals


def list_provider_reports(run_dir: Path) -> list[dict[str, Any]]:
    provider_dir = run_dir / "provider_teamwork"
    reports: list[dict[str, Any]] = []
    if not provider_dir.exists():
        return reports
    for path in sorted(provider_dir.glob("*.json")):
        data = read_json(path)
        if _skip_provider_report(path, data):
            continue
        lane = (
            data.get("lane")
            or data.get("role")
            or data.get("report_kind")
            or data.get("kind")
            or path.stem
        )
        reports.append(
            {
                "path": path,
                "kind": data.get("kind") or data.get("report_kind"),
                "lane": lane,
                "passed": data.get("passed"),
                "provider_execution_performed": provider_report_execution_performed(data),
                "provider_work_verified": provider_report_execution_performed(data),
                "response_text_ref": data.get("response_text_ref", {}),
                "response_text_chars": data.get("response_text_chars", 0),
                "response_text_sha256": data.get("response_text_sha256", ""),
                "response_text_tail": data.get("response_text_tail", ""),
                "npu_device_workload": data.get("npu_device_workload"),
                "warnings": data.get("warnings", []),
                "errors": data.get("errors", []),
                **{
                    key: data.get(key)
                    for key in ONE_TURN_SUMMARY_FIELDS
                    if key in data
                },
            }
        )
    return reports


def _skip_provider_report(path: Path, data: dict[str, Any]) -> bool:
    name = path.name
    kind = str(data.get("kind") or data.get("report_kind") or "").strip()
    if kind in PROVIDER_REPORT_SKIP_KINDS:
        return True
    if name.startswith(("provider_launch_manifest", "provider_runtime_plan")):
        return True
    if name.startswith("provider_teamwork_leader_packet"):
        return True
    if "provider_replight" in name or data.get("replight_mode") is True:
        return True
    lane = str(
        data.get("provider_id")
        or data.get("lane")
        or data.get("requirement")
        or data.get("role")
        or ""
    ).strip()
    if lane in PROVIDER_REPORT_LANES:
        return False
    stem_lane = _lane_from_provider_report_name(path.name)
    return stem_lane not in PROVIDER_REPORT_LANES


def _lane_from_provider_report_name(name: str) -> str:
    if name.startswith("gpu1_"):
        return "gpu1_planner"
    if name.startswith("gpu0_"):
        return "gpu0_peer"
    if name.startswith("npu_"):
        return "npu_micro_task_auditor"
    return ""


def flatten_quality_blockers(
    report: dict[str, Any],
    proposals: list[dict[str, Any]],
    startup_manifest: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    output_contract = (
        report.get("real_run_output_contract")
        if isinstance(report.get("real_run_output_contract"), dict)
        else {}
    )
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    quality = (
        output_contract.get("quality_output_signals")
        if isinstance(output_contract.get("quality_output_signals"), dict)
        else {}
    )
    implementation = (
        quality.get("implementation_quality")
        if isinstance(quality.get("implementation_quality"), dict)
        else {}
    )
    if startup_manifest and startup_manifest.get("input_ready_before_heap") is False:
        blockers.append("startup input_ready_before_heap=False")
    if startup_manifest.get("startup_reload_degraded"):
        blockers.append("startup_reload_degraded=True")
    blocking_requirements = (
        startup_manifest.get("blocking_requirements", [])
        if isinstance(startup_manifest.get("blocking_requirements"), list)
        else []
    )
    degraded_requirements = (
        startup_manifest.get("degraded_requirements", [])
        if isinstance(startup_manifest.get("degraded_requirements"), list)
        else []
    )
    for item in blocking_requirements:
        blockers.append(f"startup blocking requirement: {item}")
    for item in degraded_requirements:
        blockers.append(f"startup degraded requirement: {item}")
    if report.get("fallback_heap_report"):
        blockers.append("fallback heap report used")
    for error in report.get("errors") or []:
        blockers.append(str(error))
    if metrics.get("product_status") == "blocked_with_reason":
        blockers.append("heap product_status=blocked_with_reason")
    if metrics.get("quality_output_passed") is False:
        blockers.append("quality_output_passed=False")
    for error in implementation.get("errors") or []:
        blockers.append(str(error))
    for proposal in proposals:
        if proposal.get("provider_execution_performed") and not strict_one_turn_gate_passed(
            proposal
        ):
            blockers.append(
                "gpu1_one_turn_runtime_gate_failed:"
                + str(
                    proposal.get("gpu1_one_turn_blocker")
                    or "gpu1_one_turn_runtime_gate_missing"
                )
            )
        impl = (
            proposal.get("implementation_quality")
            if isinstance(proposal.get("implementation_quality"), dict)
            else {}
        )
        progress = (
            proposal.get("proposal_progress")
            if isinstance(proposal.get("proposal_progress"), dict)
            else {}
        )
        for error in impl.get("errors") or []:
            blockers.append(f"{proposal.get('name')}: {error}")
        for error in progress.get("errors") or []:
            blockers.append(f"{proposal.get('name')}: {error}")
    return list(dict.fromkeys(blockers))


def proposal_text_for_review(
    proposal: dict[str, Any],
    max_chars: int | None,
    repo_root: Path | None = None,
) -> str:
    md_path = proposal.get("markdown_path")
    if isinstance(md_path, Path) and md_path.exists():
        return read_text(md_path, limit=max_chars)
    text = (
        text_from_ref_or_tail(repo_root, proposal, "response_text")
        if repo_root is not None
        else str(proposal.get("response_text_tail") or "")
    )
    if max_chars is not None and len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]\n"
    return text


def collect_gpu0_reviews(
    proposals: list[dict[str, Any]],
    provider_reports: list[dict[str, Any]],
    repo_root: Path | None = None,
) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    for proposal in proposals:
        review = proposal.get("gpu0_review")
        if review:
            reviews.append({"source": proposal.get("name"), "review": review})
    for provider in provider_reports:
        lane = str(provider.get("lane") or "").lower()
        kind = str(provider.get("kind") or "").lower()
        if "gpu0" in lane or "gpu0" in kind:
            source = (
                repo_rel(Path.cwd(), provider["path"])
                if isinstance(provider.get("path"), Path)
                else str(provider.get("path") or "")
            )
            reviews.append(
                {
                    "source": source,
                    "passed": provider.get("passed"),
                    "provider_execution_performed": provider.get("provider_execution_performed"),
                    "summary": (
                        text_from_ref_or_tail(repo_root, provider, "response_text")
                        if repo_root is not None
                        else str(provider.get("response_text_tail") or "")
                    )[:1200],
                    "warnings": provider.get("warnings") or [],
                }
            )
    return reviews


def collect_npu_audits(
    proposals: list[dict[str, Any]], provider_reports: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    for proposal in proposals:
        piece = proposal.get("npu_micro_task_piece")
        workload = proposal.get("npu_workload_audit")
        if piece or workload:
            audits.append(
                {
                    "source": proposal.get("name"),
                    "micro_task_piece": piece,
                    "workload_audit": workload,
                }
            )
    for provider in provider_reports:
        lane = str(provider.get("lane") or "").lower()
        kind = str(provider.get("kind") or "").lower()
        if "npu" in lane or "npu" in kind or provider.get("npu_device_workload"):
            audits.append(
                {
                    "source": str(provider.get("path") or ""),
                    "passed": provider.get("passed"),
                    "provider_execution_performed": provider.get("provider_execution_performed"),
                    "npu_device_workload": provider.get("npu_device_workload"),
                    "warnings": provider.get("warnings") or [],
                }
            )
    return audits


def build_action_list(
    blockers: list[str],
    proposals: list[dict[str, Any]],
    startup_manifest: dict[str, Any],
) -> list[str]:
    actions: list[str] = []
    if startup_manifest.get("startup_reload_degraded"):
        actions.append(
            "Inspect startup_context_memory_reload/heap_context_memory_reload_manifest.json and fix degraded preload requirements before increasing provider budget."
        )
    if any("ai_context_pack" in item for item in blockers):
        actions.append(
            "Keep build_ai_context_pack advisory unless strict mode is requested; use generated artifacts as degraded context when included files exist."
        )
    if any("no verified source file references" in item for item in blockers):
        actions.append(
            "Require every proposal chunk to cite exact repo-relative target files before it can be accepted."
        )
    if any("placeholder" in item.lower() or "bare_pass" in item for item in blockers):
        actions.append(
            "Reject chunks containing pass/TODO/comment-only stubs; ask GPU0 to refine them into concrete edits or explicit non-action."
        )
    if any("similarity=" in item for item in blockers):
        actions.append(
            "Feed previous proposal chunk and quality diagnosis back into GPU1/GPU0 before another revision to prevent repeated generic output."
        )
    if not proposals:
        actions.append(
            "Run heap again after preload package export; the fallback composer is currently preserving diagnostics but no proposal chunks exist."
        )
    actions.append("Use the final TXT/JSON package as operator review input; do not apply patches automatically.")
    return list(dict.fromkeys(actions))
