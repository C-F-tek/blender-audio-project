#!/usr/bin/env python3
"""Compose heap proposal chunks into a final local review package.

The composer is deterministic and operator-facing. It assembles proposal
iterations, accepted/rejected quality state, GPU0 companion reviews, NPU
workload/audit pieces, provider reports, debug/runtime status and startup
preload manifest into a readable package. It also works on fallback heap reports
so Documents export is available even after preload/heap failures.
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def read_text(path: Path, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
    if limit is not None and len(text) > limit:
        return text[:limit] + "\n...[truncated]\n"
    return text


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def discover_run_dir(repo_root: Path, report_file: str, run_dir: str) -> Path:
    if run_dir:
        return resolve_path(repo_root, run_dir)
    if report_file:
        report = resolve_path(repo_root, report_file)
        if report.name == "heap_runtime_completeness_gate_report.json":
            return report.parent
    validation = repo_root / "output" / "validation"
    candidates = sorted(
        [path for path in validation.glob("*") if path.is_dir() and (path / "heap_runtime_completeness_gate_report.json").exists()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return candidates[0]
    raise SystemExit("unable to discover run dir; provide --run-dir or --report-file")


def documents_root(custom_root: str, stamp: str) -> Path:
    base = Path(custom_root).expanduser() if custom_root else Path.home() / "Documents"
    return (base / f"aicarmine_heap_final_proposals_{stamp}").resolve()


def load_startup_manifest(run_dir: Path) -> dict[str, Any]:
    return read_json(run_dir / "startup_context_memory_reload" / "heap_context_memory_reload_manifest.json")


def load_startup_reconciliation(run_dir: Path) -> dict[str, Any]:
    return read_json(run_dir / "heap_startup_context_reconciliation.json")


def append_artifact_ref(refs: list[str], value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        return
    normalized = value.replace("\\", "/")
    if normalized not in refs:
        refs.append(normalized)


def startup_artifact_refs(startup_manifest: dict[str, Any], report: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    artifacts = startup_manifest.get("artifacts") if isinstance(startup_manifest.get("artifacts"), dict) else {}
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
            if isinstance(artifact, dict):
                append_artifact_ref(refs, artifact.get("path"))
            else:
                append_artifact_ref(refs, artifact)
    output_contract = report.get("real_run_output_contract") if isinstance(report.get("real_run_output_contract"), dict) else {}
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
    output_contract = report.get("real_run_output_contract") if isinstance(report.get("real_run_output_contract"), dict) else {}
    product_status = metrics.get("product_status") or output_contract.get("product_status")
    startup_contract = startup_manifest.get("contract") if isinstance(startup_manifest.get("contract"), dict) else {}
    input_ready = bool(
        startup_manifest.get("input_ready_before_heap") is True
        or startup_contract.get("input_ready_before_heap") is True
    )
    artifact_refs = startup_artifact_refs(startup_manifest, report)
    provider_execution = bool(
        report.get("provider_execution_performed")
        or metrics.get("provider_execution_performed")
        or output_contract.get("provider_execution_performed")
        or any(item.get("provider_execution_performed") for item in provider_reports)
    )
    proposal_artifacts = report.get("proposal_iteration_artifacts") if isinstance(report.get("proposal_iteration_artifacts"), list) else []
    proposal_count = len(proposals) or len(proposal_artifacts)
    reconciliation_passed = (
        startup_reconciliation.get("passed") is True
        if startup_reconciliation
        else None
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
        impl = data.get("implementation_quality") if isinstance(data.get("implementation_quality"), dict) else {}
        progress = data.get("proposal_progress") if isinstance(data.get("proposal_progress"), dict) else {}
        quality_errors = []
        for source in (impl, progress):
            for error in source.get("errors") or []:
                quality_errors.append(str(error))
        proposals.append(
            {
                "name": json_path.name,
                "json_path": json_path,
                "markdown_path": md_path if md_path.exists() else None,
                "revision": data.get("revision"),
                "source": data.get("source"),
                "quality_passed": data.get("quality_passed"),
                "accepted": data.get("quality_passed") is True,
                "reject_reason": "; ".join(quality_errors) if quality_errors else ("quality_passed is not true" if data.get("quality_passed") is not True else ""),
                "implementation_quality": impl,
                "proposal_progress": progress,
                "gpu0_review": data.get("gpu0_review", []),
                "npu_micro_task_piece": data.get("npu_micro_task_piece", []),
                "npu_workload_audit": data.get("npu_workload_audit", {}),
                "anchored_source_candidates": data.get("anchored_source_candidates", []),
                "response_text": data.get("response_text", ""),
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
        lane = data.get("lane") or data.get("role") or data.get("report_kind") or data.get("kind") or path.stem
        reports.append(
            {
                "path": path,
                "kind": data.get("kind") or data.get("report_kind"),
                "lane": lane,
                "passed": data.get("passed"),
                "provider_execution_performed": data.get("provider_execution_performed"),
                "response_text": data.get("response_text", ""),
                "npu_device_workload": data.get("npu_device_workload"),
                "warnings": data.get("warnings", []),
                "errors": data.get("errors", []),
            }
        )
    return reports


def flatten_quality_blockers(report: dict[str, Any], proposals: list[dict[str, Any]], startup_manifest: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    output_contract = report.get("real_run_output_contract") if isinstance(report.get("real_run_output_contract"), dict) else {}
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    quality = output_contract.get("quality_output_signals") if isinstance(output_contract.get("quality_output_signals"), dict) else {}
    implementation = quality.get("implementation_quality") if isinstance(quality.get("implementation_quality"), dict) else {}

    if startup_manifest and startup_manifest.get("input_ready_before_heap") is False:
        blockers.append("startup input_ready_before_heap=False")
    if startup_manifest.get("startup_reload_degraded"):
        blockers.append("startup_reload_degraded=True")
    for item in startup_manifest.get("blocking_requirements", []) if isinstance(startup_manifest.get("blocking_requirements"), list) else []:
        blockers.append(f"startup blocking requirement: {item}")
    for item in startup_manifest.get("degraded_requirements", []) if isinstance(startup_manifest.get("degraded_requirements"), list) else []:
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
        impl = proposal.get("implementation_quality") if isinstance(proposal.get("implementation_quality"), dict) else {}
        progress = proposal.get("proposal_progress") if isinstance(proposal.get("proposal_progress"), dict) else {}
        for error in impl.get("errors") or []:
            blockers.append(f"{proposal.get('name')}: {error}")
        for error in progress.get("errors") or []:
            blockers.append(f"{proposal.get('name')}: {error}")
    return list(dict.fromkeys(blockers))


def proposal_text_for_review(proposal: dict[str, Any], max_chars: int | None) -> str:
    md_path = proposal.get("markdown_path")
    if isinstance(md_path, Path) and md_path.exists():
        return read_text(md_path, limit=max_chars)
    text = str(proposal.get("response_text") or "")
    if max_chars is not None and len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]\n"
    return text


def collect_gpu0_reviews(proposals: list[dict[str, Any]], provider_reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    for proposal in proposals:
        review = proposal.get("gpu0_review")
        if review:
            reviews.append({"source": proposal.get("name"), "review": review})
    for provider in provider_reports:
        lane = str(provider.get("lane") or "").lower()
        kind = str(provider.get("kind") or "").lower()
        if "gpu0" in lane or "gpu0" in kind:
            reviews.append(
                {
                    "source": repo_rel(Path.cwd(), provider["path"]) if isinstance(provider.get("path"), Path) else str(provider.get("path") or ""),
                    "passed": provider.get("passed"),
                    "provider_execution_performed": provider.get("provider_execution_performed"),
                    "summary": str(provider.get("response_text") or "")[:1200],
                    "warnings": provider.get("warnings") or [],
                }
            )
    return reviews


def collect_npu_audits(proposals: list[dict[str, Any]], provider_reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    for proposal in proposals:
        piece = proposal.get("npu_micro_task_piece")
        workload = proposal.get("npu_workload_audit")
        if piece or workload:
            audits.append({"source": proposal.get("name"), "micro_task_piece": piece, "workload_audit": workload})
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


def build_action_list(blockers: list[str], proposals: list[dict[str, Any]], startup_manifest: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    if startup_manifest.get("startup_reload_degraded"):
        actions.append("Inspect startup_context_memory_reload/heap_context_memory_reload_manifest.json and fix degraded preload requirements before increasing provider budget.")
    if any("ai_context_pack" in item for item in blockers):
        actions.append("Keep build_ai_context_pack advisory unless strict mode is requested; use generated artifacts as degraded context when included files exist.")
    if any("no verified source file references" in item for item in blockers):
        actions.append("Require every proposal chunk to cite exact repo-relative target files before it can be accepted.")
    if any("placeholder" in item.lower() or "bare_pass" in item for item in blockers):
        actions.append("Reject chunks containing pass/TODO/comment-only stubs; ask GPU0 to refine them into concrete edits or explicit non-action.")
    if any("similarity=" in item for item in blockers):
        actions.append("Feed previous proposal chunk and quality diagnosis back into GPU1/GPU0 before another revision to prevent repeated generic output.")
    if not proposals:
        actions.append("Run heap again after preload package export; the fallback composer is currently preserving diagnostics but no proposal chunks exist.")
    actions.append("Use the final TXT/JSON package as operator review input; do not apply patches automatically.")
    return list(dict.fromkeys(actions))


def render_startup_section(repo_root: Path, startup_manifest: dict[str, Any]) -> list[str]:
    if not startup_manifest:
        return ["## Startup preload manifest", "", "- No startup manifest found.", ""]
    artifacts = startup_manifest.get("artifacts") if isinstance(startup_manifest.get("artifacts"), dict) else {}
    lines = [
        "## Startup preload manifest",
        "",
        f"- Passed: `{startup_manifest.get('passed')}`",
        f"- Input ready before heap: `{startup_manifest.get('input_ready_before_heap')}`",
        f"- Startup reload degraded: `{startup_manifest.get('startup_reload_degraded')}`",
        f"- Required reload passed: `{startup_manifest.get('required_reload_passed')}`",
        f"- Optional reload passed: `{startup_manifest.get('optional_reload_passed')}`",
        f"- Degraded requirements: `{startup_manifest.get('degraded_requirements')}`",
        f"- Blocking requirements: `{startup_manifest.get('blocking_requirements')}`",
        "",
        "### Loaded artifacts",
        "",
    ]
    for key, value in artifacts.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    return lines


def render_markdown(
    *,
    repo_root: Path,
    run_dir: Path,
    report: dict[str, Any],
    startup_manifest: dict[str, Any],
    proposals: list[dict[str, Any]],
    provider_reports: list[dict[str, Any]],
    blockers: list[str],
    gpu0_reviews: list[dict[str, Any]],
    npu_audits: list[dict[str, Any]],
    action_list: list[str],
    product_causality: dict[str, Any],
    max_proposal_chars: int,
) -> str:
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    output_contract = report.get("real_run_output_contract") if isinstance(report.get("real_run_output_contract"), dict) else {}
    context_refs = output_contract.get("context_artifact_refs") or []
    accepted = [item for item in proposals if item.get("accepted")]
    rejected = [item for item in proposals if not item.get("accepted")]

    lines: list[str] = [
        "# IA-Carmine Heap Final Proposal Composer",
        "",
        "## Runtime status",
        "",
        f"- Run dir: `{repo_rel(repo_root, run_dir)}`",
        f"- Product status: `{metrics.get('product_status') or output_contract.get('product_status')}`",
        f"- Quality output passed: `{metrics.get('quality_output_passed')}`",
        f"- Provider revisions: `{metrics.get('provider_revision_count')}`",
        f"- Runtime debug lab required: `{output_contract.get('runtime_debug_lab_required')}`",
        f"- Runtime debug lab passed: `{output_contract.get('runtime_debug_lab_passed')}`",
        f"- Fallback heap report: `{report.get('fallback_heap_report', False)}`",
        f"- Product causality status: `{product_causality.get('product_causality_status')}`",
        f"- Product causality passed: `{product_causality.get('product_causality_passed')}`",
        f"- Startup artifact refs: `{product_causality.get('startup_artifact_ref_count')}`",
        f"- Provider execution evidence present: `{product_causality.get('provider_execution_evidence_present')}`",
        f"- Proposal artifact count: `{product_causality.get('proposal_artifact_count')}`",
        "",
        "## External heap product causality",
        "",
    ]
    reasons = product_causality.get("causality_reasons") if isinstance(product_causality.get("causality_reasons"), list) else []
    if reasons:
        lines.extend(f"- {reason}" for reason in reasons)
    else:
        lines.append("- Causalita' esterna coerente con artifact/report disponibili.")
    lines.extend([
        "",
        "## Context-limit escape protocol",
        "",
        "Il prodotto finale non dipende dalla sola finestra token di GPU1: ogni proposta viene salvata come chunk riusabile, GPU0/NPU producono review e audit separati, e questo composer assembla il risultato finale dai file persistenti.",
        "",
    ])
    lines.extend(render_startup_section(repo_root, startup_manifest))

    if blockers:
        lines.extend(["## Blocking quality issues", ""])
        lines.extend(f"- {item}" for item in blockers)
        lines.append("")
    else:
        lines.extend(["## Blocking quality issues", "", "- Nessun blocco deterministico rilevato dal composer.", ""])

    lines.extend(["## Accepted proposal chunks", ""])
    if not accepted:
        lines.append("- Nessun chunk accettato dal quality gate.")
    for proposal in accepted:
        lines.append(f"- `{proposal.get('name')}` revision=`{proposal.get('revision')}` source=`{proposal.get('source')}`")
    lines.append("")

    lines.extend(["## Rejected proposal chunks", ""])
    if not rejected:
        lines.append("- Nessun chunk rifiutato.")
    for proposal in rejected:
        lines.append(f"- `{proposal.get('name')}` revision=`{proposal.get('revision')}` reason=`{proposal.get('reject_reason')}`")
    lines.append("")

    lines.extend(["## GPU0 companion review/refine", ""])
    if not gpu0_reviews:
        lines.append("- Nessuna review GPU0 trovata nei proposal/provider report.")
    for review in gpu0_reviews:
        lines.extend(["```json", json.dumps(review, indent=2, ensure_ascii=False, default=str)[:3000], "```", ""])
    lines.append("")

    lines.extend(["## NPU workload/audit pieces", ""])
    if not npu_audits:
        lines.append("- Nessun audit/workload NPU trovato nei proposal/provider report.")
    for audit in npu_audits:
        lines.extend(["```json", json.dumps(audit, indent=2, ensure_ascii=False, default=str)[:3000], "```", ""])
    lines.append("")

    lines.extend(["## Provider reports", ""])
    for provider in provider_reports:
        rel = repo_rel(repo_root, provider["path"]) if isinstance(provider.get("path"), Path) else ""
        workload = provider.get("npu_device_workload") if isinstance(provider.get("npu_device_workload"), dict) else {}
        lines.extend(
            [
                f"### {provider.get('lane') or 'provider'}",
                "",
                f"- Report: `{rel}`",
                f"- Kind: `{provider.get('kind')}`",
                f"- Passed: `{provider.get('passed')}`",
                f"- Provider execution: `{provider.get('provider_execution_performed')}`",
            ]
        )
        if workload:
            lines.extend(
                [
                    f"- NPU workload performed: `{workload.get('performed')}`",
                    f"- NPU workload iterations: `{workload.get('iterations')}`",
                    f"- NPU workload seconds: `{workload.get('seconds')}`",
                    f"- Python: `{workload.get('python_exe')}`",
                ]
            )
        summary = str(provider.get("response_text") or "").strip()
        if summary:
            lines.extend(["", summary[:1600], ""])

    lines.extend(["## Proposal chunks", ""])
    if not proposals:
        lines.append("- Nessuna proposal iteration trovata.")
    for proposal in proposals:
        lines.extend(
            [
                f"### {proposal.get('name')}",
                "",
                f"- Revision: `{proposal.get('revision')}`",
                f"- Source: `{proposal.get('source')}`",
                f"- Quality passed: `{proposal.get('quality_passed')}`",
                f"- Accepted: `{proposal.get('accepted')}`",
                f"- Reject reason: `{proposal.get('reject_reason')}`",
                "",
            ]
        )
        anchored = proposal.get("anchored_source_candidates") or []
        if anchored:
            lines.extend(["Anchored source candidates:"])
            lines.extend(f"- `{item}`" for item in anchored[:20])
            lines.append("")
        lines.extend(["```markdown", proposal_text_for_review(proposal, max_proposal_chars), "```", ""])

    lines.extend(["## Context artifacts", ""])
    if context_refs:
        for ref in context_refs[:120]:
            lines.append(f"- `{ref}`")
    elif startup_manifest.get("artifacts"):
        for value in startup_manifest.get("artifacts", {}).values():
            if value:
                lines.append(f"- `{value}`")
    else:
        lines.append("- Nessun context artifact ref disponibile.")
    lines.append("")

    lines.extend(["## Concrete action list", ""])
    for action in action_list:
        lines.append(f"- {action}")
    lines.append("")
    return "\n".join(lines)


def write_documents_package(
    *,
    stamp: str,
    doc_dir: Path,
    markdown: str,
    json_data: dict[str, Any],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    doc_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    proposal_txt_outputs: list[str] = []
    proposal_chunk_outputs: list[str] = []
    md_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}.md"
    txt_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}.txt"
    json_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}.json"
    manifest_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}_DOWNLOADS.txt"
    md_path.write_text(markdown, encoding="utf-8")
    txt_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    written.extend([str(md_path), str(txt_path), str(json_path)])

    chunk_dir = doc_dir / "proposal_chunks"
    chunk_txt_dir = doc_dir / "proposal_chunks_txt"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    chunk_txt_dir.mkdir(parents=True, exist_ok=True)
    for proposal in proposals:
        md = proposal.get("markdown_path")
        js = proposal.get("json_path")
        if isinstance(md, Path) and md.exists():
            target = chunk_dir / md.name
            shutil.copyfile(md, target)
            written.append(str(target))
            proposal_chunk_outputs.append(str(target))
        if isinstance(js, Path) and js.exists():
            target = chunk_dir / js.name
            shutil.copyfile(js, target)
            written.append(str(target))
            proposal_chunk_outputs.append(str(target))
        txt_name = f"{Path(str(proposal.get('name') or 'proposal')).stem}.txt"
        txt_target = chunk_txt_dir / txt_name
        txt_target.write_text(proposal_text_for_review(proposal, None), encoding="utf-8")
        written.append(str(txt_target))
        proposal_txt_outputs.append(str(txt_target))

    manifest_lines = [
        "IA-Carmine heap final proposal download package",
        "",
        f"Primary TXT: {txt_path}",
        f"Primary Markdown: {md_path}",
        f"Primary JSON: {json_path}",
        "",
        "Proposal TXT chunks:",
    ]
    manifest_lines.extend(f"- {path}" for path in proposal_txt_outputs)
    manifest_lines.extend(["", "All outputs:"])
    manifest_lines.extend(f"- {path}" for path in written)
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    written.append(str(manifest_path))

    return {
        "documents_dir": str(doc_dir),
        "documents_outputs": written,
        "primary_markdown": str(md_path),
        "primary_txt": str(txt_path),
        "primary_json": str(json_path),
        "download_manifest_txt": str(manifest_path),
        "proposal_chunk_outputs": proposal_chunk_outputs,
        "proposal_txt_outputs": proposal_txt_outputs,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--report-file", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--documents-root", default="")
    parser.add_argument("--write-documents", action="store_true")
    parser.add_argument("--max-proposal-chars", type=int, default=18000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    run_dir = discover_run_dir(repo_root, args.report_file, args.run_dir)
    report_file = resolve_path(repo_root, args.report_file) if args.report_file else run_dir / "heap_runtime_completeness_gate_report.json"
    report = read_json(report_file)
    startup_manifest = load_startup_manifest(run_dir)
    startup_reconciliation = load_startup_reconciliation(run_dir)
    stamp = str(report.get("stamp") or startup_manifest.get("stamp") or (report.get("metrics") or {}).get("stamp") or now_stamp())

    proposals = list_proposals(run_dir)
    provider_reports = list_provider_reports(run_dir)
    blockers = flatten_quality_blockers(report, proposals, startup_manifest)
    gpu0_reviews = collect_gpu0_reviews(proposals, provider_reports)
    npu_audits = collect_npu_audits(proposals, provider_reports)
    action_list = build_action_list(blockers, proposals, startup_manifest)
    product_causality = compute_product_causality(
        report=report,
        startup_manifest=startup_manifest,
        startup_reconciliation=startup_reconciliation,
        proposals=proposals,
        provider_reports=provider_reports,
    )

    markdown = render_markdown(
        repo_root=repo_root,
        run_dir=run_dir,
        report=report,
        startup_manifest=startup_manifest,
        proposals=proposals,
        provider_reports=provider_reports,
        blockers=blockers,
        gpu0_reviews=gpu0_reviews,
        npu_audits=npu_audits,
        action_list=action_list,
        product_causality=product_causality,
        max_proposal_chars=max(2000, int(args.max_proposal_chars)),
    )
    accepted = [item for item in proposals if item.get("accepted")]
    rejected = [item for item in proposals if not item.get("accepted")]
    result = {
        "schema_version": 1,
        "kind": "heap_final_proposal_composer",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "run_dir": repo_rel(repo_root, run_dir),
        "report_file": repo_rel(repo_root, report_file),
        "startup_manifest": startup_manifest,
        "startup_reload_degraded": bool(startup_manifest.get("startup_reload_degraded")),
        "proposal_count": len(proposals),
        "accepted_proposal_count": len(accepted),
        "rejected_proposal_count": len(rejected),
        "provider_report_count": len(provider_reports),
        "gpu0_review_count": len(gpu0_reviews),
        "npu_audit_count": len(npu_audits),
        "blocking_issue_count": len(blockers),
        "blocking_issues": blockers,
        "action_list": action_list,
        "product_status": (report.get("metrics") or {}).get("product_status") or (report.get("real_run_output_contract") or {}).get("product_status"),
        "quality_output_passed": (report.get("metrics") or {}).get("quality_output_passed"),
        "product_causality": product_causality,
        "product_causality_status": product_causality.get("product_causality_status"),
        "product_causality_passed": product_causality.get("product_causality_passed"),
        "startup_reconciliation": startup_reconciliation,
        "proposals": [
            {
                "name": item.get("name"),
                "revision": item.get("revision"),
                "source": item.get("source"),
                "quality_passed": item.get("quality_passed"),
                "accepted": item.get("accepted"),
                "reject_reason": item.get("reject_reason"),
                "implementation_quality": item.get("implementation_quality"),
                "proposal_progress": item.get("proposal_progress"),
                "gpu0_review": item.get("gpu0_review"),
                "npu_micro_task_piece": item.get("npu_micro_task_piece"),
                "npu_workload_audit": item.get("npu_workload_audit"),
                "anchored_source_candidates": item.get("anchored_source_candidates"),
            }
            for item in proposals
        ],
        "accepted_proposals": [item.get("name") for item in accepted],
        "rejected_proposals": [{"name": item.get("name"), "reason": item.get("reject_reason")} for item in rejected],
        "gpu0_reviews": gpu0_reviews,
        "npu_audits": npu_audits,
        "provider_reports": [
            {
                "path": repo_rel(repo_root, item["path"]) if isinstance(item.get("path"), Path) else "",
                "kind": item.get("kind"),
                "lane": item.get("lane"),
                "passed": item.get("passed"),
                "provider_execution_performed": item.get("provider_execution_performed"),
                "npu_device_workload": item.get("npu_device_workload"),
                "errors": item.get("errors"),
                "warnings": item.get("warnings"),
            }
            for item in provider_reports
        ],
    }

    output = resolve_path(repo_root, args.output) if args.output else run_dir / "heap_final_proposal_composer.json"
    markdown_output = resolve_path(repo_root, args.markdown_output) if args.markdown_output else run_dir / "heap_final_proposal_composer.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    markdown_output.write_text(markdown, encoding="utf-8")
    result["output"] = repo_rel(repo_root, output)
    result["markdown_output"] = repo_rel(repo_root, markdown_output)

    if args.write_documents:
        doc_dir = documents_root(args.documents_root, stamp)
        document_package = write_documents_package(
            stamp=stamp,
            doc_dir=doc_dir,
            markdown=markdown,
            json_data=result,
            proposals=proposals,
        )
        result.update(document_package)
        result["download_hint"] = f"Apri o copia il file TXT principale: {document_package['primary_txt']}"

    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
