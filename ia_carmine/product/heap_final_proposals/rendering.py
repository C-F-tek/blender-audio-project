"""Markdown rendering for heap final proposal composition."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ia_carmine.product.heap_final_proposals.artifacts import proposal_text_for_review
from ia_carmine.product.heap_final_proposals.common import repo_rel


def render_startup_section(repo_root: Path, startup_manifest: dict[str, Any]) -> list[str]:
    if not startup_manifest:
        return ["## Startup preload manifest", "", "- No startup manifest found.", ""]
    artifacts = (
        startup_manifest.get("artifacts")
        if isinstance(startup_manifest.get("artifacts"), dict)
        else {}
    )
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
    lines.extend(f"- `{key}`: `{value}`" for key, value in artifacts.items())
    lines.append("")
    return lines


def render_markdown(
    decision_block: dict[str, Any],
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
    output_contract = (
        report.get("real_run_output_contract")
        if isinstance(report.get("real_run_output_contract"), dict)
        else {}
    )
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
        "## Operator decision",
        "",
        f"- Decision: `{decision_block.get('decision')}`",
        f"- Reason: {decision_block.get('reason')}",
        f"- Accepted proposal count: `{decision_block.get('accepted_count')}`",
        f"- Rejected proposal count: `{decision_block.get('rejected_count')}`",
        f"- Source allowlist enforced: `{decision_block.get('allowlist_enforced')}`",
        f"- Source allowlist path: `{decision_block.get('allowlist_path') or 'none'}`",
        "",
        "## External heap product causality",
        "",
    ]
    _append_reason_sections(lines, decision_block, product_causality)
    lines.extend(render_startup_section(repo_root, startup_manifest))
    _append_blockers(lines, blockers)
    _append_proposal_summaries(lines, "Accepted proposal chunks", accepted, "Nessun chunk accettato dal quality gate.")
    _append_proposal_summaries(lines, "Rejected proposal chunks", rejected, "Nessun chunk rifiutato.")
    _append_json_blocks(lines, "GPU0 companion review/refine", gpu0_reviews, "Nessuna review GPU0 trovata nei proposal/provider report.")
    _append_json_blocks(lines, "NPU workload/audit pieces", npu_audits, "Nessun audit/workload NPU trovato nei proposal/provider report.")
    _append_provider_reports(lines, repo_root, provider_reports)
    _append_full_proposals(lines, proposals, max_proposal_chars)
    _append_context_refs(lines, context_refs, startup_manifest)
    lines.extend(["## Concrete action list", ""])
    lines.extend(f"- {action}" for action in action_list)
    lines.append("")
    return "\n".join(lines)


def _append_reason_sections(
    lines: list[str], decision_block: dict[str, Any], product_causality: dict[str, Any]
) -> None:
    gate_reasons = (
        decision_block.get("gate_reasons")
        if isinstance(decision_block.get("gate_reasons"), list)
        else []
    )
    if gate_reasons:
        lines.extend(["### Operator gate reasons", ""])
        lines.extend(f"- {reason}" for reason in gate_reasons[:40])
        lines.append("")
    reasons = (
        product_causality.get("causality_reasons")
        if isinstance(product_causality.get("causality_reasons"), list)
        else []
    )
    lines.extend(f"- {reason}" for reason in reasons)
    if not reasons:
        lines.append("- Causalita' esterna coerente con artifact/report disponibili.")
    lines.extend(
        [
            "",
            "## Context-limit escape protocol",
            "",
            "Il prodotto finale non dipende dalla sola finestra token di GPU1: ogni proposta viene salvata come chunk riusabile, GPU0/NPU producono review e audit separati, e questo composer assembla il risultato finale dai file persistenti.",
            "",
        ]
    )


def _append_blockers(lines: list[str], blockers: list[str]) -> None:
    lines.extend(["## Blocking quality issues", ""])
    if blockers:
        lines.extend(f"- {item}" for item in blockers)
    else:
        lines.append("- Nessun blocco deterministico rilevato dal composer.")
    lines.append("")


def _append_proposal_summaries(
    lines: list[str], heading: str, proposals: list[dict[str, Any]], empty_message: str
) -> None:
    lines.extend([f"## {heading}", ""])
    if not proposals:
        lines.append(f"- {empty_message}")
    for proposal in proposals:
        details = (
            f"- `{proposal.get('name')}` revision=`{proposal.get('revision')}` "
            f"source=`{proposal.get('source')}`"
        )
        if "Rejected" in heading:
            details += f" reason=`{proposal.get('reject_reason')}`"
        lines.append(details)
    lines.append("")


def _append_json_blocks(
    lines: list[str], heading: str, items: list[dict[str, Any]], empty_message: str
) -> None:
    lines.extend([f"## {heading}", ""])
    if not items:
        lines.append(f"- {empty_message}")
    for item in items:
        lines.extend(["```json", json.dumps(item, indent=2, ensure_ascii=False, default=str)[:3000], "```", ""])
    lines.append("")


def _append_provider_reports(
    lines: list[str], repo_root: Path, provider_reports: list[dict[str, Any]]
) -> None:
    lines.extend(["## Provider reports", ""])
    for provider in provider_reports:
        rel = repo_rel(repo_root, provider["path"]) if isinstance(provider.get("path"), Path) else ""
        workload = (
            provider.get("npu_device_workload")
            if isinstance(provider.get("npu_device_workload"), dict)
            else {}
        )
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


def _append_full_proposals(
    lines: list[str], proposals: list[dict[str, Any]], max_proposal_chars: int
) -> None:
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


def _append_context_refs(
    lines: list[str], context_refs: list[Any], startup_manifest: dict[str, Any]
) -> None:
    lines.extend(["## Context artifacts", ""])
    if context_refs:
        lines.extend(f"- `{ref}`" for ref in context_refs[:120])
    elif startup_manifest.get("artifacts"):
        for value in startup_manifest.get("artifacts", {}).values():
            if value:
                lines.append(f"- `{value}`")
    else:
        lines.append("- Nessun context artifact ref disponibile.")
    lines.append("")
