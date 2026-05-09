#!/usr/bin/env python3
"""Build advisory repository change proposals.

The tool is intentionally non-mutating. It reads validation reports, local AI
resource-lane reports and current runtime peer evidence, then writes proposal
JSON/Markdown that a human or trusted agent can review.

It never applies patches, never edits source files and never runs providers.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "output/ai_pipeline"
DEFAULT_BASENAME = "repository_change_proposals"

DEFAULT_REPORTS = (
    "output/validation/python_syntax.json",
    "output/validation/npu_pipeline_modules.json",
    "output/validation/npu_pipeline_helper_tests.json",
    "output/validation/npu_pipeline_docs.json",
    "output/validation/provider_result_parsing.json",
    "output/validation/provider_result_report.json",
    "output/validation/ai_workload_report_quality.json",
    "output/validation/npu_runtime_output_manifest.json",
    "output/validation/local_ai_resource_lanes.json",
    "output/validation/local_provider_probe.json",
    "output/validation/execution_plan_status.json",
    "output/validation/validation_report_contract.json",
    "output/ai_pipeline/repository_update_suggestions.json",
)

RUNTIME_REPORT_PATTERNS = (
    "output/validation/openvino_gpu0_workload_*.json",
    "output/validation/npu_micro_peer_*.json",
    "output/validation/real_product_preflight_runtime_evidence_correlation.json",
    "output/validation/*runtime_evidence_correlation*.json",
    "output/validation/generated_patch_specs_review_pr_apply*.json",
    "output/validation/patch_suggestion_bundle_apply*.json",
    "output/local_ai_runs/*/ai_packets/heap_exchange_runtime_entry.json",
    "output/local_ai_runs/*/ai_packets/heap_peer_runtime_manifest.json",
    "output/local_ai_runs/*/ai_packets/heap_exchange_closure_audit.json",
    "output/patch_specs/*_manifest.json",
)

SUPPORTED_SUGGESTION_OUTPUT_KINDS = (
    "python_code",
    "markdown",
    "json",
    "powershell",
    "workflow_yaml",
    "path_group",
    "text_or_config",
)

CONCRETE_OPERATION_NAMES = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}

STAMP_RE = re.compile(r"\d{8}-\d{6}")


def split_path_values(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "path": str(path), "data": None, "error": "missing"}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return {"exists": True, "path": str(path), "data": data, "error": ""}
    except Exception as exc:  # noqa: BLE001 - advisory report.
        return {"exists": True, "path": str(path), "data": None, "error": f"{type(exc).__name__}: {exc}"}


def report_by_kind(reports: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_kind: dict[str, dict[str, Any]] = {}
    for report in reports:
        data = report.get("data")
        if isinstance(data, dict):
            kind = str(data.get("kind") or Path(report["path"]).stem)
            by_kind[kind] = data
    return by_kind


def reports_by_kind(reports: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_kind: dict[str, list[dict[str, Any]]] = {}
    for report in reports:
        data = report.get("data")
        if isinstance(data, dict):
            kind = str(data.get("kind") or Path(report["path"]).stem)
            by_kind.setdefault(kind, []).append(data)
    return by_kind


def report_passed(report: dict[str, Any] | None) -> bool:
    return isinstance(report, dict) and report.get("passed") is True


def infer_stamp_from_values(*values: str) -> str:
    for value in values:
        matches = STAMP_RE.findall(str(value or ""))
        if matches:
            return matches[-1]
    return ""


def report_matches_stamp(path: Path, data: Any, stamp: str) -> bool:
    if not stamp:
        return True
    if stamp in path.as_posix():
        return True
    if isinstance(data, dict):
        for key in ("Stamp", "stamp", "DataStamp", "generated_stamp"):
            if str(data.get(key) or "") == stamp:
                return True
    return False


def discover_runtime_report_paths(repo_root: Path, stamp: str, max_files: int) -> list[str]:
    candidates: list[Path] = []
    for pattern in RUNTIME_REPORT_PATTERNS:
        candidates.extend(path for path in repo_root.glob(pattern) if path.is_file())
    unique = {path.resolve(): path for path in candidates}
    ordered = sorted(unique.values(), key=lambda item: item.stat().st_mtime, reverse=True)
    selected: list[str] = []
    for path in ordered:
        if len(selected) >= max_files:
            break
        loaded = read_json_if_exists(path)
        data = loaded.get("data")
        if loaded.get("error"):
            continue
        if not report_matches_stamp(path, data, stamp):
            continue
        selected.append(repo_relative(path, repo_root))
    return selected


def classify_target_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.endswith("/") or "*" in normalized:
        return "path_group"
    suffix = Path(normalized).suffix.lower()
    if suffix == ".py":
        return "python_code"
    if suffix == ".md":
        return "markdown"
    if suffix == ".json":
        return "json"
    if suffix == ".ps1":
        return "powershell"
    if suffix in {".yml", ".yaml"}:
        return "workflow_yaml"
    return "text_or_config"


def build_suggestion_outputs(target_files: list[str]) -> list[dict[str, str]]:
    return [
        {
            "path": path,
            "artifact_kind": classify_target_path(path),
            "operation": "manual_patch_suggestion",
            "content_status": "proposal_only",
            "write_policy": "manual_review_only",
        }
        for path in target_files
    ]


def all_provider_observability_green(by_kind: dict[str, dict[str, Any]]) -> bool:
    resource_lanes = by_kind.get("local_ai_resource_lanes")
    npu_manifest = by_kind.get("npu_runtime_output_manifest")
    provider_parsing = by_kind.get("provider_result_parsing")
    provider_probe = by_kind.get("local_provider_probe")

    ready_lanes = set(resource_lanes.get("ready_lanes") or []) if isinstance(resource_lanes, dict) else set()
    return (
        report_passed(resource_lanes)
        and {"gpu", "npu", "ollama"}.issubset(ready_lanes)
        and report_passed(npu_manifest)
        and int(npu_manifest.get("blocked_count") or 0) == 0
        and report_passed(provider_parsing)
        and report_passed(provider_probe)
        and provider_probe.get("provider_execution_performed") is True
    )


def provider_report_adoption_green(by_kind: dict[str, dict[str, Any]]) -> bool:
    provider_result_report = by_kind.get("provider_result_report")
    provider_probe = by_kind.get("local_provider_probe")
    return (
        all_provider_observability_green(by_kind)
        and report_passed(provider_result_report)
        and provider_result_report.get("provider_execution_performed") is False
        and provider_result_report.get("mode") == "runtime_safe_report_only"
        and provider_probe.get("provider_execution_performed") is True
    )


def workload_quality_decision(by_kind: dict[str, dict[str, Any]]) -> dict[str, Any]:
    report = by_kind.get("ai_workload_report_quality")
    if not isinstance(report, dict):
        return {
            "quality_report_present": False,
            "usable_lanes": [],
            "unusable_lanes": [],
            "ollama_gpu_primary_advisory_allowed": False,
            "npu_excluded_from_primary_advisory": True,
        }
    decision = report.get("decision") if isinstance(report.get("decision"), dict) else {}
    return {
        "quality_report_present": True,
        "usable_lanes": report.get("usable_lanes") or [],
        "unusable_lanes": report.get("unusable_lanes") or [],
        "ollama_gpu_primary_advisory_allowed": decision.get("ollama_gpu_primary_advisory_allowed") is True,
        "npu_excluded_from_primary_advisory": decision.get("npu_excluded_from_primary_advisory") is not False,
        "routing_policy": decision.get("routing_policy") or report.get("policy"),
    }


def ai_workload_quality_has_unusable_output(by_kind: dict[str, dict[str, Any]]) -> bool:
    report = by_kind.get("ai_workload_report_quality")
    return isinstance(report, dict) and bool(report.get("unusable_lanes"))


def proposal(
    *,
    proposal_id: str,
    priority: str,
    area: str,
    title: str,
    rationale: str,
    target_files: list[str],
    change_type: str,
    sketch: list[str],
    validation: list[str],
    stop_conditions: list[str],
    suggestion_outputs: list[dict[str, str]] | None = None,
    do_not_touch: list[str] | None = None,
    evidence_summary: dict[str, Any] | None = None,
    concrete_operations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": proposal_id,
        "priority": priority,
        "area": area,
        "title": title,
        "rationale": rationale,
        "target_files": target_files,
        "change_type": change_type,
        "apply_mode": "manual_review_only",
        "patch_sketch": sketch,
        "evidence_summary": evidence_summary or {},
        "suggestion_outputs": suggestion_outputs if suggestion_outputs is not None else build_suggestion_outputs(target_files),
        "validation_commands": validation,
        "stop_conditions": stop_conditions,
        "do_not_touch": do_not_touch
        or [
            "runtime Blender files",
            "Ready To Jazz migration",
            "full analysis JSON",
            "generated indexes by hand",
            "provider execution behavior unless explicitly scoped",
        ],
    }
    if concrete_operations:
        item["concrete_operations"] = concrete_operations
    return item


def runtime_peer_evidence_summary(by_kind_multi: dict[str, list[dict[str, Any]]], reports: list[dict[str, Any]]) -> dict[str, Any]:
    kinds = {kind: len(items) for kind, items in by_kind_multi.items()}
    gpu0_reports = by_kind_multi.get("openvino_gpu0_workload", [])
    npu_reports = by_kind_multi.get("npu_micro_peer", [])
    heap_entry_reports = by_kind_multi.get("heap_exchange_runtime_entry", [])
    heap_manifest_reports = by_kind_multi.get("heap_peer_runtime_manifest", [])
    closure_reports = by_kind_multi.get("heap_exchange_closure_audit", [])
    correlation_reports = by_kind_multi.get("runtime_evidence_correlation", [])
    apply_reports = by_kind_multi.get("patch_suggestion_bundle_apply", [])

    latest_apply = apply_reports[-1] if apply_reports else {}
    manual_items = latest_apply.get("manual_review_items") if isinstance(latest_apply, dict) else []
    if not isinstance(manual_items, list):
        manual_items = []

    metadata_only_count = sum(
        1
        for item in manual_items
        if isinstance(item, dict)
        and "metadata-only" in str(item.get("reason") or "")
    )
    operation_count = int(latest_apply.get("operation_count") or 0) if isinstance(latest_apply, dict) else 0
    changed_count = int(latest_apply.get("changed_count") or 0) if isinstance(latest_apply, dict) else 0

    return {
        "report_kinds_seen": kinds,
        "runtime_report_paths": [
            repo_path
            for report in reports
            for repo_path in [str(report.get("path") or "")]
            if "output/" in repo_path.replace("\\", "/")
        ],
        "heap_entry_present": bool(heap_entry_reports),
        "heap_peer_runtime_manifest_present": bool(heap_manifest_reports),
        "heap_closure_audit_present": bool(closure_reports),
        "gpu0_workload_present": bool(gpu0_reports),
        "gpu0_observable": any(
            report.get("openvino_gpu0_observable_workload_passed") is True or report.get("passed") is True
            for report in gpu0_reports
        ),
        "npu_micro_peer_present": bool(npu_reports),
        "npu_peer_activity_requested": any(report.get("npu_peer_activity_requested") is True for report in npu_reports),
        "runtime_evidence_correlation_present": bool(correlation_reports),
        "patch_apply_report_present": bool(apply_reports),
        "patch_apply_operation_count": operation_count,
        "patch_apply_changed_count": changed_count,
        "metadata_only_manual_review_count": metadata_only_count,
        "needs_concrete_generated_product": bool(apply_reports) and operation_count == 0,
    }


def runtime_peer_evidence_ready(summary: dict[str, Any]) -> bool:
    return (
        summary.get("heap_entry_present") is True
        and summary.get("heap_peer_runtime_manifest_present") is True
        and summary.get("gpu0_workload_present") is True
        and summary.get("npu_micro_peer_present") is True
        and summary.get("runtime_evidence_correlation_present") is True
    )


def runtime_peer_evidence_proposal(summary: dict[str, Any]) -> dict[str, Any]:
    marker = "<!-- IA-CARMINE-RUNTIME-PEER-EVIDENCE-PROPOSAL -->"
    content = (
        "\n\n"
        f"{marker}\n"
        "## Runtime peer evidence proposal path\n\n"
        "The repository-change proposal builder can consume current-stamp heap/exchange, GPU0, "
        "NPU peer, runtime correlation and generated patch-spec apply reports. This keeps the "
        "GPU1/Ollama advisory lane grounded in the active heap instead of falling back to "
        "static validation-only context.\n\n"
        "When generated patch specs are metadata-only, the proposal path must expose that as "
        "a concrete product gap and prefer deterministic, reviewable operations over "
        "evidence-only success.\n"
    )
    return proposal(
        proposal_id="P-RUNTIME-PEER-EVIDENCE-FEED",
        priority="P1",
        area="heap_exchange_product",
        title="Feed current runtime peer evidence into repository proposals",
        rationale=(
            "Current heap/GPU0/NPU/runtime-correlation evidence is available, but generated patch "
            "specs can still collapse into metadata-only proposals. The proposal builder must "
            "surface current runtime evidence and emit a concrete, reviewable product lane."
        ),
        target_files=[
            "Tools/ai/build_repository_change_proposals.py",
            "Tools/ai/build_patch_specs_from_proposals.py",
            "Tools/validation/README.md",
        ],
        change_type="runtime_evidence_proposal_feed",
        evidence_summary={"runtime_peer_evidence": summary},
        sketch=[
            "Discover current-stamp heap, GPU0, NPU and runtime-correlation reports.",
            "Carry runtime peer evidence into repository_change_proposals evidence_summary.",
            "Allow reviewed proposals to provide concrete deterministic operations for patch-spec generation.",
            "Fail if runtime evidence exists but no concrete generated product can be produced.",
        ],
        concrete_operations=[
            {
                "operation": "append_once",
                "path": "Tools/validation/README.md",
                "content": content,
                "source_id": "P-RUNTIME-PEER-EVIDENCE-FEED",
                "family": "runtime_peer_evidence",
                "description": "document runtime peer evidence proposal path",
            }
        ],
        validation=[
            "python .\\Tools\\validation\\run_repository_change_proposals_runtime_evidence_smoke.py --repo-root .",
            "python .\\Tools\\validation\\run_generated_patch_specs_empty_product_smoke.py --repo-root .",
            "python -m py_compile .\\Tools\\ai\\build_repository_change_proposals.py .\\Tools\\ai\\build_patch_specs_from_proposals.py",
            "git diff --check",
        ],
        stop_conditions=[
            "Any change would execute providers from the proposal builder.",
            "Any change would fabricate source changes without runtime evidence.",
            "Any change would write under output/**, indexAI/code_chunks/** or docs/LOCAL_VALIDATION_EVIDENCE/** as final product.",
        ],
    )


def ai_workload_quality_remediation_proposal(by_kind: dict[str, dict[str, Any]]) -> dict[str, Any]:
    quality_summary = workload_quality_decision(by_kind)
    usable = ", ".join(quality_summary.get("usable_lanes") or []) or "none"
    unusable = ", ".join(quality_summary.get("unusable_lanes") or []) or "none"
    return proposal(
        proposal_id="P-AI-WORKLOAD-REPORT-QUALITY-GATE",
        priority="P1",
        area="local_ai_workloads",
        title="Gate AI workload reports before using them as advisory context",
        rationale=(
            f"AI workload report quality found usable lanes: {usable}; unusable lanes: {unusable}. "
            "Downstream packets and proposals should trust only usable workload reports and keep unusable lanes limited to probes until their decoding/configuration is fixed."
        ),
        target_files=[
            "Tools/validation/check_ai_workload_report_quality.py",
            "Tools/npu/run_npu_review.py",
            "Tools/ai/suggest_repository_updates.py",
            "Tools/ai/build_repository_change_proposals.py",
            "Tools/validation/README.md",
            "docs/JSON_SCHEMAS.md",
        ],
        change_type="workload_quality_gate",
        evidence_summary={"workload_quality_decision": quality_summary},
        sketch=[
            "Keep Ollama/GPU workload reports as primary advisory context when classified usable.",
            "Exclude or clearly mark NPU/OpenVINO generated reports as unusable when they are numeric/hex-like or non-linguistic.",
            "Do not disable NPU preflight/probe; only prevent low-quality NPU generation output from influencing suggestions.",
            "Add report metadata that distinguishes availability, execution and output usability.",
        ],
        validation=[
            "python .\\Tools\\validation\\check_ai_workload_report_quality.py --repo-root . --output .\\output\\validation\\ai_workload_report_quality.json",
            "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_ollama_real_workload_after_tests -ProposalBasename npu_ollama_real_workload_proposals -ContextFile output/ai_packets/npu_real_workload_report.md,output/ai_packets/ollama_gpu_real_workload_report.md -ReportFile output/validation/ai_workload_report_quality.json,output/validation/local_ai_resource_lanes.json,output/validation/provider_result_report.json,output/validation/local_provider_probe.json,output/validation/npu_runtime_output_manifest.json",
        ],
        stop_conditions=[
            "Any change would execute providers implicitly or by default.",
            "Any change would hide a failing/unusable AI workload report instead of reporting it.",
            "Any change would alter NPU/Ollama model configuration, prompt prose or provider orchestration.",
        ],
    )


def provider_report_adoption_proposal() -> dict[str, Any]:
    return proposal(
        proposal_id="P-RUNTIME-SAFE-PROVIDER-REPORT-ADOPTION",
        priority="P2",
        area="npu_backend",
        title="Adopt provider result reports in runtime-safe observability",
        rationale=(
            "Resource lanes, runtime-output manifest, provider-result parsing and explicit local provider probes are green. "
            "The next safe step is to let runtime-adjacent tooling consume already-produced provider results as reports, "
            "without executing providers or changing legacy runtime behavior."
        ),
        target_files=[
            "Tools/npu/run_dual_ai_pipeline.py",
            "Tools/npu/pipeline/providers.py",
            "Tools/npu/pipeline/reports.py",
            "Tools/validation/check_provider_result_parsing.py",
            "Tools/validation/check_npu_pipeline_modules.py",
            "Tools/npu/pipeline/README.md",
            "docs/JSON_SCHEMAS.md",
        ],
        change_type="runtime_safe_report_adoption",
        sketch=[
            "Add a runtime-safe helper that turns already-obtained provider payloads into provider_result_report JSON.",
            "Do not call Ollama, NPU, GPU, OpenVINO generation or provider sessions from the legacy runtime path.",
            "Write reports under output/validation or an explicitly report-only output path.",
            "Expose provider_execution_performed accurately: false for parsed legacy/simulated payloads, true only for explicit probe tools.",
            "Add smoke/unit validation that proves report adoption does not modify prompt prose, model selection, temperature or legacy outputs.",
        ],
        validation=[
            "python .\\Tools\\validation\\check_provider_result_parsing.py --repo-root . --output .\\output\\validation\\provider_result_parsing.json",
            "python .\\Tools\\npu\\build_provider_result_report.py --repo-root . --use-samples --output .\\output\\validation\\provider_result_report.json",
            "python .\\Tools\\ai\\run_local_provider_probe.py --repo-root . --run-ollama --run-npu --output .\\output\\validation\\local_provider_probe.json",
            "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1",
        ],
        stop_conditions=[
            "Any change would execute providers from the legacy runtime path.",
            "Any change would alter prompt prose, model, temperature or provider orchestration.",
            "Any change would touch Blender runtime, Ready To Jazz, full analysis JSON or generated indexes by hand.",
            "Any report cannot distinguish parsed existing payloads from explicit provider execution.",
        ],
    )


def post_validation_loop_hardening_proposal() -> dict[str, Any]:
    return proposal(
        proposal_id="P-POST-VALIDATION-LOOP-HARDENING",
        priority="P2",
        area="workflow_core",
        title="Harden the post-validation report/packet/proposal loop",
        rationale=(
            "Resource lanes, runtime-output manifest, provider parsing, explicit provider probes and runtime-safe provider report adoption are green. "
            "The next safe milestone is consolidating the internal loop so future coding/test cycles produce stable reports, packets, proposals and stop conditions without adding new runtime features."
        ),
        target_files=[
            "Tools/workflow/run_local_validation_after_refactor.ps1",
            "Tools/workflow/run_npu_pipeline_helper_validation.ps1",
            "Tools/workflow/run_post_validation_ai_packet.ps1",
            "Tools/ai/suggest_repository_updates.py",
            "Tools/ai/build_repository_change_proposals.py",
            "Tools/validation/README.md",
            "WORKFLOW.md",
            "docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md",
            "docs/JSON_SCHEMAS.md",
        ],
        change_type="post_validation_loop_hardening",
        sketch=[
            "Include provider_result_report in standard NPU packet/proposal validation commands everywhere it is relevant.",
            "Ensure local full validation summaries point to packet and proposal outputs consistently.",
            "Add a compact loop-health report that states which reports are missing, stale, passing or blocking.",
            "Keep generated outputs under output/ and keep source changes separate from local report generation.",
            "Document the canonical order: validation -> resource/probe reports -> runtime-safe provider report -> packet -> proposals -> reindex.",
        ],
        validation=[
            "python .\\Tools\\validation\\check_provider_result_parsing.py --repo-root . --output .\\output\\validation\\provider_result_parsing.json",
            "python .\\Tools\\npu\\build_provider_result_report.py --repo-root . --use-samples --output .\\output\\validation\\provider_result_report.json",
            "python .\\Tools\\ai\\check_local_resource_lanes.py --repo-root . --parallel --output .\\output\\validation\\local_ai_resource_lanes.json --markdown-output .\\output\\validation\\local_ai_resource_lanes.md",
            "python .\\Tools\\ai\\run_local_provider_probe.py --repo-root . --run-ollama --run-npu --output .\\output\\validation\\local_provider_probe.json",
            "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2",
        ],
        stop_conditions=[
            "Any change would add new provider execution to default validation without an explicit flag.",
            "Any change would auto-apply proposal patches or commit generated reports.",
            "Any change would mix local generated outputs with source files or generated indexes.",
            "Any change would broaden permissions, network access, secrets or authentication behavior.",
        ],
    )


def default_npu_observability_proposal() -> dict[str, Any]:
    return proposal(
        proposal_id="P-NEXT-NPU-OBSERVABILITY",
        priority="P2",
        area="npu_backend",
        title="Add additive NPU observability before provider execution changes",
        rationale="Current reports do not indicate blocking failures. The next safe app-agnostic step is deeper observability, not provider behavior changes.",
        target_files=[
            "Tools/npu/build_runtime_output_manifest.py",
            "Tools/ai/check_local_resource_lanes.py",
            "Tools/ai/suggest_repository_updates.py",
            "docs/JSON_SCHEMAS.md",
            "Tools/validation/README.md",
        ],
        change_type="observability_extension",
        sketch=[
            "Include runtime-output manifest and resource-lane reports in the default NPU packet profile.",
            "Add proposal generation output next to packet JSON/Markdown.",
            "Keep every output advisory and generated under output/.",
        ],
        validation=[
            "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1",
            "python .\\Tools\\ai\\check_local_resource_lanes.py --repo-root . --parallel --output .\\output\\validation\\local_ai_resource_lanes.json --markdown-output .\\output\\validation\\local_ai_resource_lanes.md",
            "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_after_tests -ReportFile output/validation/local_ai_resource_lanes.json -ReportFile output/validation/npu_runtime_output_manifest.json",
        ],
        stop_conditions=["Any change requires modifying provider execution, prompt prose, Blender runtime or generated indexes manually."],
    )


def build_proposals(reports: list[dict[str, Any]], *, profile: str) -> list[dict[str, Any]]:
    by_kind = report_by_kind(reports)
    by_kind_multi = reports_by_kind(reports)
    proposals: list[dict[str, Any]] = []
    runtime_summary = runtime_peer_evidence_summary(by_kind_multi, reports)

    if runtime_peer_evidence_ready(runtime_summary) and runtime_summary.get("needs_concrete_generated_product"):
        proposals.append(runtime_peer_evidence_proposal(runtime_summary))

    execution_plan_status = by_kind.get("execution_plan_status")
    if not proposals and execution_plan_status and execution_plan_status.get("passed") is False:
        proposals.append(
            proposal(
                proposal_id="P-EXEC-PLAN-STATUS",
                priority="P1",
                area="execution_plans",
                title="Fix execution-plan folder/status drift",
                rationale="The execution-plan validator reports terminal-status plans in the wrong folder or invalid status markers.",
                target_files=["docs/EXECUTION_PLANS/active/", "docs/EXECUTION_PLANS/completed/", "docs/EXECUTION_PLANS/abandoned/"],
                change_type="docs_move_or_status_fix",
                sketch=[
                    "Move plans with top-level `## Status` = `completed` from active/ to completed/.",
                    "Move abandoned plans to abandoned/ or change their top-level status back to active/planned if still open.",
                    "Do not treat folder README.md files as execution plans.",
                ],
                validation=[
                    "python .\\Tools\\validation\\check_execution_plan_status.py --repo-root . --output .\\output\\validation\\execution_plan_status.json",
                    "python .\\Tools\\validation\\check_docs_links.py --repo-root . --output .\\output\\validation\\docs_links.json",
                ],
                stop_conditions=["Any moved plan has unclear status or contains active unfinished work."],
            )
        )

    npu_manifest = by_kind.get("npu_runtime_output_manifest")
    if not proposals and npu_manifest and npu_manifest.get("blocked_count", 0):
        proposals.append(
            proposal(
                proposal_id="P-NPU-MANIFEST-BLOCKED-OUTPUTS",
                priority="P1",
                area="npu_observability",
                title="Review blocked NPU runtime output paths",
                rationale="The runtime-output manifest found paths outside the exact legacy output allowlist.",
                target_files=["Tools/npu/build_runtime_output_manifest.py", "Tools/npu/pipeline/artifact_paths.py", "docs/JSON_SCHEMAS.md"],
                change_type="policy_review",
                sketch=[
                    "Inspect each blocked output path in `output/validation/npu_runtime_output_manifest.json`.",
                    "If the path is a legitimate legacy runtime output, add it to the exact allowlist with a focused test.",
                    "If not legitimate, keep it blocked and document why.",
                ],
                validation=[
                    "python .\\Tools\\npu\\build_runtime_output_manifest.py --repo-root . --output .\\output\\validation\\npu_runtime_output_manifest.json",
                    "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1",
                ],
                stop_conditions=["A blocked path points to source code, full analysis JSON or an unreviewed generated destination."],
            )
        )

    resource_lanes = by_kind.get("local_ai_resource_lanes")
    if not proposals and resource_lanes:
        ready = set(resource_lanes.get("ready_lanes") or [])
        available = set(resource_lanes.get("available_lanes") or [])
        if {"npu", "gpu", "ollama"} - ready:
            proposals.append(
                proposal(
                    proposal_id="P-RESOURCE-LANE-PREFLIGHTS",
                    priority="P2",
                    area="local_ai_resources",
                    title="Stabilize local NPU/GPU/Ollama resource-lane readiness",
                    rationale="One or more local AI resource lanes are unavailable or not ready. Keeping this as observability improves future parallel pipeline work.",
                    target_files=["Tools/ai/check_local_resource_lanes.py", "Tools/workflow/run_post_validation_ai_packet.ps1", "Tools/validation/README.md"],
                    change_type="preflight_hardening",
                    sketch=[
                        f"Ready lanes currently reported: {sorted(ready)}.",
                        f"Available lanes currently reported: {sorted(available)}.",
                        "Keep missing lanes as warnings unless explicitly required with `--require-lane`.",
                        "Add narrower diagnostics for lanes that are available but not ready.",
                    ],
                    validation=[
                        "python .\\Tools\\ai\\check_local_resource_lanes.py --repo-root . --parallel --output .\\output\\validation\\local_ai_resource_lanes.json --markdown-output .\\output\\validation\\local_ai_resource_lanes.md",
                        "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_post_validation_ai_packet.ps1 -Profile npu -ReportFile output/validation/local_ai_resource_lanes.json",
                    ],
                    stop_conditions=["A lane probe would need long generation, Blender execution, GPU render or provider behavior changes."],
                )
            )

    validation_contract = by_kind.get("validation_report_contract")
    if not proposals and validation_contract and validation_contract.get("passed") is False:
        proposals.append(
            proposal(
                proposal_id="P-REPORT-CONTRACT-CONSISTENCY",
                priority="P1",
                area="validation_contracts",
                title="Normalize validation report root fields",
                rationale="The validation-report contract checker found reports missing common fields or using inconsistent types.",
                target_files=["Tools/validation/*.py", "Tools/npu/pipeline/reports.py", "docs/JSON_SCHEMAS.md"],
                change_type="contract_normalization",
                sketch=[
                    "Add missing root fields additively: schema_version, kind, repo_root, passed, errors, warnings where applicable.",
                    "Do not remove validator-specific fields.",
                    "Keep strict mode opt-in until all local reports are aligned.",
                ],
                validation=[
                    "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
                    "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2",
                ],
                stop_conditions=["A proposed normalization would change the meaning of existing report fields."],
            )
        )

    if not proposals:
        if ai_workload_quality_has_unusable_output(by_kind):
            proposals.append(ai_workload_quality_remediation_proposal(by_kind))
        elif provider_report_adoption_green(by_kind):
            proposals.append(post_validation_loop_hardening_proposal())
        elif all_provider_observability_green(by_kind):
            proposals.append(provider_report_adoption_proposal())
        else:
            proposals.append(default_npu_observability_proposal())

    return proposals


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Repository Change Proposals", ""]
    lines.append(f"- Generated at: `{report['generated_at']}`")
    lines.append(f"- Profile: `{report['profile']}`")
    lines.append(f"- Apply mode: `{report['apply_mode']}`")
    lines.append(f"- Proposal count: `{len(report['proposals'])}`")
    if report.get("runtime_report_paths"):
        lines.append(f"- Runtime reports read: `{len(report['runtime_report_paths'])}`")
    lines.append("")
    for item in report["proposals"]:
        lines.append(f"## {item['id']} — {item['title']}")
        lines.append("")
        lines.append(f"- Priority: `{item['priority']}`")
        lines.append(f"- Area: `{item['area']}`")
        lines.append(f"- Change type: `{item['change_type']}`")
        lines.append(f"- Apply mode: `{item['apply_mode']}`")
        lines.append(f"- Rationale: {item['rationale']}")
        lines.append("")
        if item.get("evidence_summary"):
            lines.append("### Evidence summary")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(item["evidence_summary"], indent=2, ensure_ascii=False))
            lines.append("```")
            lines.append("")
        lines.append("### Target files")
        for path in item["target_files"]:
            lines.append(f"- `{path}`")
        lines.append("")
        lines.append("### Patch sketch")
        for step in item["patch_sketch"]:
            lines.append(f"- {step}")
        lines.append("")
        if item.get("concrete_operations"):
            lines.append("### Concrete operations")
            for op in item["concrete_operations"]:
                lines.append(f"- `{op.get('operation')}` `{op.get('path')}`")
            lines.append("")
        if item.get("suggestion_outputs"):
            lines.append("### Suggestion outputs")
            for output in item["suggestion_outputs"]:
                lines.append(
                    f"- `{output.get('artifact_kind')}` `{output.get('path')}` "
                    f"({output.get('operation')}, {output.get('write_policy')})"
                )
            lines.append("")
        lines.append("### Validation")
        for command in item["validation_commands"]:
            lines.append(f"- `{command}`")
        lines.append("")
        lines.append("### Stop conditions")
        for condition in item["stop_conditions"]:
            lines.append(f"- {condition}")
        lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append("These are proposals only. They must not be auto-applied without explicit review.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--profile", default="core")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=DEFAULT_BASENAME)
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--runtime-report-stamp", default="")
    parser.add_argument("--runtime-report-max-files", type=int, default=40)
    parser.add_argument("--no-discover-runtime-reports", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    explicit_report_paths = split_path_values(list(args.report_file or []))
    stamp = args.runtime_report_stamp or infer_stamp_from_values(args.basename, *explicit_report_paths)
    runtime_report_paths: list[str] = []
    if not args.no_discover_runtime_reports:
        runtime_report_paths = discover_runtime_report_paths(repo_root, stamp, args.runtime_report_max_files)

    report_paths = list(DEFAULT_REPORTS) + explicit_report_paths + runtime_report_paths
    loaded_reports = [read_json_if_exists(repo_root / path) for path in dict.fromkeys(report_paths)]
    proposals = build_proposals(loaded_reports, profile=args.profile)

    output_dir = repo_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_json = output_dir / f"{args.basename}.json"
    output_md = output_dir / f"{args.basename}.md"

    report = {
        "schema_version": 1,
        "kind": "repository_change_proposals",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "profile": args.profile,
        "passed": True,
        "errors": [],
        "warnings": [],
        "apply_mode": "manual_review_only",
        "runtime_report_stamp": stamp,
        "runtime_report_paths": runtime_report_paths,
        "suggestion_contract": {
            "schema_version": 1,
            "supported_output_kinds": list(SUPPORTED_SUGGESTION_OUTPUT_KINDS),
            "default_operation": "manual_patch_suggestion",
            "default_write_policy": "manual_review_only",
            "supported_concrete_operations": sorted(CONCRETE_OPERATION_NAMES),
            "provider_execution_performed": False,
        },
        "reports_read": [item["path"] for item in loaded_reports],
        "proposals": proposals,
    }

    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": True, "json": str(output_json), "markdown": str(output_md), "proposal_count": len(proposals)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
