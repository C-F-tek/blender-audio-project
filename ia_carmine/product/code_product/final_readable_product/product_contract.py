"""Final readable code-product acceptance contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def revision_linked_count(revision: dict[str, Any], linked_key: str, fallback_key: str) -> int:
    try:
        return int(revision.get(linked_key) if linked_key in revision else revision.get(fallback_key) or 0)
    except (TypeError, ValueError):
        return 0


def code_product_markdown_metrics(markdown: str) -> dict[str, Any]:
    text = str(markdown or "")
    return {
        "bytes": len(text.encode("utf-8")),
        "line_count": len(text.splitlines()),
        "diff_git_blocks": text.count("diff --git"),
        "empty_code_product_marker": "EMPTY CODE PRODUCT" in text,
        "no_applicable_marker": "NO_APPLICABLE_CODE_PRODUCT" in text,
        "truncation_marker": "[truncated]" in text.lower(),
    }


def real_code_product_ready(
    *, final_document_status: str, concrete_code_proposal_count: int, code_product_metrics: dict[str, Any]
) -> bool:
    if final_document_status not in {"APPLY_REVIEW_READY", "BLOCKED_WITH_CODE_PRODUCT_REVIEW"}:
        return False
    if concrete_code_proposal_count <= 0:
        return False
    return bool(
        int(code_product_metrics.get("diff_git_blocks") or 0) > 0
        and not code_product_metrics.get("empty_code_product_marker")
        and not code_product_metrics.get("no_applicable_marker")
        and not code_product_metrics.get("truncation_marker")
    )


def final_product_blockers(
    *,
    markdown_output: Path,
    final_document_status: str,
    concrete_code_proposal_count: int,
    code_product_metrics: dict[str, Any],
    code_product_ready: bool,
    pointer: dict[str, Any],
    revision: dict[str, Any],
    matrix: dict[str, Any],
    gate: dict[str, Any],
    product_acceptance_passed: bool | None = None,
) -> list[str]:
    blockers: list[str] = []
    if gate and gate.get("passed") is False:
        blockers.append("heap runtime completeness gate did not pass")
    gate_errors = gate.get("errors") if isinstance(gate.get("errors"), list) else []
    if gate_errors:
        blockers.append("heap runtime completeness gate reported errors")
    if product_acceptance_passed is not True:
        blockers.append("external heap product acceptance did not pass")
    if not pointer:
        blockers.append("external heap pointer manifest is missing")
    elif not truthy(pointer.get("passed")):
        blockers.append("external heap pointer manifest did not pass")
    if int(pointer.get("edge_count") or 0) <= 0:
        blockers.append("external heap pointer manifest has no graph edges")
    roles = set(str(item) for item in (pointer.get("all_roles_present") or pointer.get("roles_present") or []))
    for role in ("gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor"):
        if pointer and role not in roles:
            blockers.append(f"external heap pointer manifest missing role {role}")
    provider_rejection_reasons = [
        str(item)
        for item in (pointer.get("provider_rejection_reasons") or revision.get("provider_rejection_reasons") or [])
        if str(item).strip()
    ]
    for reason in provider_rejection_reasons:
        blockers.append(f"provider runtime rejected: {reason}")
    if revision_linked_count(revision, "linked_gpu0_block_count", "gpu0_block_count") <= 0:
        blockers.append("revision context has no linked GPU0 review/refinement block")
    if revision_linked_count(revision, "linked_npu_block_count", "npu_block_count") <= 0:
        blockers.append("revision context has no linked NPU audit block")
    if not truthy(pointer.get("provider_execution_performed")):
        blockers.append("provider execution is not proven by verified pointer evidence")
    if matrix and matrix.get("passed") is not True:
        blockers.append("code execution matrix did not pass")
    if not markdown_output.exists():
        blockers.append("final readable markdown was not written")
    if final_document_status in {"DIAGNOSTIC_REVIEW_READY", "NO_APPLICABLE_CODE_PRODUCT"}:
        blockers.append(f"final document status is not a real code product: {final_document_status}")
    if final_document_status == "BLOCKED_PROVIDER_RUNTIME":
        blockers.append("final document status is provider runtime blocked")
    if concrete_code_proposal_count <= 0:
        blockers.append("no concrete code proposal was available")
    if int(code_product_metrics.get("diff_git_blocks") or 0) <= 0:
        blockers.append("CODE_PRODUCT_FULL_PATCH.md contains no diff --git block")
    if code_product_metrics.get("empty_code_product_marker"):
        blockers.append("CODE_PRODUCT_FULL_PATCH.md contains EMPTY CODE PRODUCT")
    if code_product_metrics.get("no_applicable_marker"):
        blockers.append("CODE_PRODUCT_FULL_PATCH.md contains NO_APPLICABLE_CODE_PRODUCT")
    if code_product_metrics.get("truncation_marker"):
        blockers.append("CODE_PRODUCT_FULL_PATCH.md contains a truncation marker")
    if not code_product_ready and not blockers:
        blockers.append("real code product contract did not pass")
    return blockers
