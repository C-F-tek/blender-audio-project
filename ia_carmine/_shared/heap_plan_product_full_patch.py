"""Render the final heap text/prose product surface."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import read_text_evidence
from ia_carmine._shared.heap_final_readable_synthesis import (
    as_dict,
    gpu1_raw_evidence_summary,
    matrix_has_applicable_code_product,
    pointer_graph_chain_summary,
    pointer_summary,
    render_pointer_closure_markdown_lines,
    soft_lock_state_from_reports,
)


def _repo_root_from_run_dir(run_dir: Path) -> Path:
    for candidate in [run_dir, *run_dir.parents]:
        if (candidate / "ia_carmine").is_dir() and (candidate / "Tools").is_dir():
            return candidate
    return run_dir


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _proposal_reports(run_dir: Path) -> list[dict[str, Any]]:
    proposal_dir = run_dir / "team_context" / "proposal_iterations"
    reports: list[dict[str, Any]] = []
    for path in sorted(proposal_dir.glob("heap_proposal_revision_*.json")):
        report = _read_json(path)
        if not report:
            continue
        report["_source_path"] = str(path)
        reports.append(report)
    return reports


def _strict_text(repo_root: Path, report: dict[str, Any], prefix: str) -> dict[str, Any]:
    return read_text_evidence(repo_root, report, prefix, require_full=True)


def _preview_text(repo_root: Path, report: dict[str, Any], prefix: str) -> dict[str, Any]:
    return read_text_evidence(repo_root, report, prefix, require_full=False)


def _proposal_id(report: dict[str, Any]) -> str:
    return str(report.get("block_id") or f"revision:{report.get('revision')}")


def _protocol_errors(report: dict[str, Any], evidence: dict[str, Any]) -> list[str]:
    protocol = report.get("final_product_protocol")
    protocol = protocol if isinstance(protocol, dict) else {}
    errors = [str(item) for item in protocol.get("errors") or [] if str(item).strip()]
    errors.extend(str(item) for item in evidence.get("errors") or [] if str(item).strip())
    return list(dict.fromkeys(errors))


def _proposal_entry(repo_root: Path, report: dict[str, Any]) -> dict[str, Any]:
    evidence = _strict_text(repo_root, report, "final_product_delta")
    text = str(evidence.get("text") or "")
    valid = bool(
        report.get("quality_passed")
        and report.get("final_product_delta_valid")
        and text
        and evidence.get("full_verified")
    )
    protocol = report.get("final_product_protocol")
    protocol = protocol if isinstance(protocol, dict) else {}
    return {
        "block_id": _proposal_id(report),
        "revision": report.get("revision"),
        "kind": str(report.get("final_product_kind") or ""),
        "action": str(report.get("final_product_action") or ""),
        "text": text,
        "valid": valid,
        "errors": _protocol_errors(report, evidence),
        "source_path": str(report.get("_source_path") or ""),
        "previous_block_id": str(report.get("previous_block_id") or ""),
        "refines_block_id": str(report.get("refines_block_id") or ""),
        "resume_from_block_id": str(report.get("resume_from_block_id") or ""),
        "consumed_gpu0_block_ids": report.get("consumed_gpu0_block_ids")
        if isinstance(report.get("consumed_gpu0_block_ids"), list)
        else [],
        "consumed_npu_block_ids": report.get("consumed_npu_block_ids")
        if isinstance(report.get("consumed_npu_block_ids"), list)
        else [],
        "evidence_ref": evidence.get("ref_path") or "",
        "evidence_errors": evidence.get("errors") or [],
        "protocol": protocol,
    }


def _apply_delta(composed: list[dict[str, Any]], entry: dict[str, Any]) -> str:
    action = str(entry.get("action") or "").lower()
    if action == "append":
        if composed:
            previous = str(entry.get("previous_block_id") or "").strip()
            accepted_ids = {
                str(item.get("block_id") or "").strip()
                for item in composed
                if str(item.get("block_id") or "").strip()
            }
            if not previous or previous not in accepted_ids:
                return "final_product_delta_append_previous_mismatch_rejected"
        composed.append(entry)
        return "appended"
    target = str(entry.get("refines_block_id") or entry.get("previous_block_id") or "")
    if action in {"replace", "supersede", "refine"} and target:
        for index, existing in enumerate(composed):
            if str(existing.get("block_id") or "") == target:
                composed[index] = entry
                return f"{action}_applied_to:{target}"
    return f"{action or 'unknown'}_target_missing_rejected"


def _compose_final_product(
    repo_root: Path,
    reports: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    composed: list[dict[str, Any]] = []
    ledger: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for report in reports:
        entry = _proposal_entry(repo_root, report)
        if entry["valid"]:
            status = _apply_delta(composed, entry)
            if status.endswith("_rejected"):
                raw_errors = [
                    *entry.get("errors", []),
                    status,
                ]
                if "target_missing" in status:
                    raw_errors.insert(-1, "final_product_delta_target_missing")
                rejected.append(
                    {
                        **entry,
                        "raw_text": entry.get("text") or "",
                        "raw_source": "final_product_delta_ref",
                        "raw_errors": raw_errors,
                    }
                )
                continue
            ledger.append({**entry, "applied_status": status})
        else:
            raw = _strict_text(repo_root, report, "gpu1_free_text_evidence")
            raw_text = str(raw.get("text") or "")
            raw_source = "gpu1_free_text_evidence_ref"
            if not raw_text:
                raw = _strict_text(repo_root, report, "response_text")
                raw_text = str(raw.get("text") or "")
                raw_source = "response_text_ref"
            if not raw_text:
                raw = _preview_text(repo_root, report, "gpu1_free_text_evidence")
                raw_text = str(raw.get("text") or "")
                raw_source = "gpu1_free_text_evidence_preview"
            rejected.append(
                {
                    **entry,
                    "raw_text": raw_text,
                    "raw_source": raw_source,
                    "raw_errors": raw.get("errors") or [],
                }
            )
    return composed, ledger, rejected


def _fenced(text: str, info: str = "markdown") -> list[str]:
    return [f"````{info}", text.rstrip(), "````"]


def _delta_table(ledger: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| block_id | action | kind | applied_status | refines | previous |",
        "|---|---|---|---|---|---|",
    ]
    for item in ledger:
        lines.append(
            "| {block_id} | {action} | {kind} | {status} | {refines} | {previous} |".format(
                block_id=item.get("block_id") or "",
                action=item.get("action") or "",
                kind=item.get("kind") or "",
                status=item.get("applied_status") or "",
                refines=item.get("refines_block_id") or "",
                previous=item.get("previous_block_id") or "",
            )
        )
    return lines


def render_plan_product_full_patch(
    *,
    run_dir: Path,
    gate: dict[str, Any],
    revision: dict[str, Any],
    pointer: dict[str, Any],
    matrix: dict[str, Any],
    matrix_path: str,
) -> str:
    repo_root = _repo_root_from_run_dir(run_dir)
    metrics = as_dict(gate.get("metrics"))
    soft_lock_state = soft_lock_state_from_reports(gate, pointer, revision)
    has_applicable_code_product = matrix_has_applicable_code_product(matrix)
    reports = _proposal_reports(run_dir)
    composed, ledger, rejected = _compose_final_product(repo_root, reports)
    text_surface_status = (
        "FINAL_PRODUCT_TEXT_SURFACE_AVAILABLE"
        if composed
        else "FINAL_PRODUCT_TEXT_SURFACE_BLOCKED"
    )
    code_surface_status = (
        "CODE_PRODUCT_SURFACE_AVAILABLE"
        if has_applicable_code_product
        else "NO_APPLICABLE_CODE_PRODUCT"
    )
    lines = [
        "# PLAN_PRODUCT_FULL_PATCH",
        "",
        "Text/prose/decision surface of the single FINAL_PRODUCT.",
        "`CODE_PRODUCT_FULL_PATCH.md` is the code/diff surface of the same FINAL_PRODUCT when verified code exists.",
        "This artifact is produced by deterministic delta composition; it does not call GPU/provider for a final synthesis.",
        "",
        "## FINAL_PRODUCT Contract",
        "",
        "- FINAL_PRODUCT is single: text, code, or text+code.",
        "- PLAN_PRODUCT_FULL_PATCH.md and CODE_PRODUCT_FULL_PATCH.md are packaging/evidence surfaces, not competing products.",
        "- GPU1 turns contribute only through valid FINAL_PRODUCT_DELTA records.",
        "- GPU1 is not allowed to emit blocked; blocked_with_reason is a runtime/gate decision.",
        "- The composer applies append/replace/supersede/refine deltas and does not collage raw proposal bodies.",
        "",
        "## Status",
        "",
        f"- Text surface status: `{text_surface_status}`.",
        f"- Code surface status: `{code_surface_status}`.",
        "- Code product sibling: `CODE_PRODUCT_FULL_PATCH.md`.",
        f"- Matrix target count: `{matrix.get('target_count')}`.",
        f"- Verified target count: `{matrix.get('verified_target_count')}`.",
        f"- Matrix report: `{matrix_path}`.",
        f"- Resume from block: `{revision.get('resume_from_block_id') or ''}`.",
        f"- Latest block id: `{revision.get('latest_block_id') or ''}`.",
        f"- GPU1 block count: `{revision.get('gpu1_block_count') or 0}`.",
        f"- Proposal block count: `{revision.get('proposal_block_count') or 0}`.",
        f"- Applied final-product delta count: `{len(ledger)}`.",
        f"- Rejected/raw GPU1 turn count: `{len(rejected)}`.",
        "",
        "## FINAL_PRODUCT Text Surface",
        "",
    ]
    if composed:
        for index, item in enumerate(composed, start=1):
            lines.extend(
                [
                    f"### Applied Delta {index}: `{item.get('block_id')}`",
                    "",
                    f"- FINAL_PRODUCT_KIND: `{item.get('kind')}`.",
                    f"- FINAL_PRODUCT_ACTION: `{item.get('action')}`.",
                    f"- Source: `{item.get('source_path')}`.",
                    f"- Evidence ref: `{item.get('evidence_ref')}`.",
                    f"- Previous/refines/resume: `{item.get('previous_block_id')}` / `{item.get('refines_block_id')}` / `{item.get('resume_from_block_id')}`.",
                    "",
                    *_fenced(str(item.get("text") or "")),
                    "",
                ]
            )
    else:
        lines.extend(
            [
                "`blocked_with_reason`: no valid FINAL_PRODUCT_DELTA entered the text surface.",
                "",
                "Blockers:",
                "- gpu1_final_product_delta_missing",
                "- gpu1_pointer_protocol_not_operational",
                "- final_product_composer_only_collaged_blocks",
                "",
            ]
        )
    lines.extend(
        [
            "## Applied FINAL_PRODUCT_DELTA Ledger",
            "",
            *(_delta_table(ledger) if ledger else ["No valid deltas were applied."]),
            "",
            "## Rejected / Raw GPU1 Turns",
            "",
        ]
    )
    if rejected:
        for item in rejected:
            reasons = ", ".join(str(reason) for reason in item.get("errors") or []) or "unclassified"
            lines.extend(
                [
                    f"### Raw Turn `{item.get('block_id')}`",
                    "",
                    f"- Source: `{item.get('source_path')}`.",
                    f"- Raw source: `{item.get('raw_source')}`.",
                    f"- Rejection reasons: `{reasons}`.",
                    "",
                    *_fenced(str(item.get("raw_text") or "")),
                    "",
                ]
            )
    else:
        lines.extend(["No rejected GPU1 turns.", ""])
    lines.extend(
        [
            "## Technical Attachments",
            "",
            "### GPU1 Chain Evidence",
            "",
            *[f"- {line}" for line in gpu1_raw_evidence_summary(run_dir)],
            "",
            "### Pointer Graph",
            "",
            *[f"- {line}" for line in pointer_summary(run_dir, revision)],
            "",
            *render_pointer_closure_markdown_lines(soft_lock_state),
            "",
            "### Quorum And Recovery",
            "",
            *[f"- {line}" for line in pointer_graph_chain_summary(metrics, pointer, soft_lock_state)],
            "",
            "## Operational Use",
            "",
            "- Use this file as the text/prose/decision surface of the single FINAL_PRODUCT.",
            "- Apply code only from verified sections in `CODE_PRODUCT_FULL_PATCH.md`.",
            "- Treat `external_heap_primary_long_response` as a diagnostic transcript unless it applies this delta protocol.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
