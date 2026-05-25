"""Canonical product-state classification for heap context closure."""

from __future__ import annotations

from typing import Any


def build_product_state(
    *,
    code_product_contract: dict[str, Any],
    external_contract: dict[str, Any],
    final_result: dict[str, Any],
    final_payload: dict[str, Any],
    launcher_contract_errors: list[str],
) -> dict[str, Any]:
    real_code_product_ready = bool(code_product_contract.get("real_code_product_ready"))
    final_product_delta_applied_count = _safe_int(
        code_product_contract.get("final_product_delta_applied_count")
        or final_payload.get("final_product_delta_applied_count")
        or 0
    )
    text_product_ready = bool(
        (
            code_product_contract.get("text_product_ready")
            or final_payload.get("text_product_ready")
        )
        and final_product_delta_applied_count > 0
    )
    final_product_surface_ready = bool(real_code_product_ready or text_product_ready)
    plan_product_kind = str(
        final_payload.get("plan_product_kind")
        or code_product_contract.get("plan_product_kind")
        or ""
    ).strip()
    product_kind = str(final_payload.get("product_kind") or "").strip()
    if product_kind == "code_or_text_product_candidate":
        product_kind = ""
    if not product_kind:
        if real_code_product_ready and text_product_ready:
            product_kind = "text_and_code_product"
        elif real_code_product_ready:
            product_kind = "code_patch_product"
        elif text_product_ready:
            product_kind = "text_product"
        elif external_contract.get("resume_from_block_id") and external_contract.get(
            "provider_execution_performed"
        ):
            product_kind = "blocked_continuation_product"
        else:
            product_kind = "diagnostic_decision_product"
    provider_runtime_blocked = bool(
        not external_contract.get("provider_execution_performed")
        and (
            external_contract.get("provider_rejection_reasons")
            or external_contract.get("missing_roles")
        )
    )
    if provider_runtime_blocked:
        product_kind = "provider_runtime_blocked_product"

    approved = bool(
        product_kind
        in {"code_patch_product", "text_product", "text_and_code_product", "technical_plan_product"}
        and final_result.get("passed")
        and final_product_surface_ready
        and not launcher_contract_errors
    )
    continuation_required = bool(
        final_payload.get("continuation_required")
        or product_kind == "blocked_continuation_product"
    )
    if continuation_required and product_kind == "provider_runtime_blocked_product":
        product_kind = "blocked_continuation_product"
    product_status = (
        "approved_product"
        if approved
        else "blocked_continuation_product"
        if continuation_required
        else "blocked_with_reason"
    )
    blocked_reason = _blocked_reason(
        approved=approved,
        continuation_required=continuation_required,
        launcher_contract_errors=launcher_contract_errors,
        final_payload=final_payload,
        external_contract=external_contract,
    )
    soft_close_reason = _soft_close_reason(
        approved=approved,
        continuation_required=continuation_required,
        blocked_reason=blocked_reason,
        final_payload=final_payload,
    )
    return {
        "canonical_product_path": (
            code_product_contract.get("path", "")
            if real_code_product_ready
            else code_product_contract.get("plan_product_path", "")
        ),
        "product_kind": product_kind,
        "product_status": product_status,
        "product_approval_status": (
            "approved" if approved else "continuation_required" if continuation_required else "blocked"
        ),
        "product_approval_evidence": {
            "final_readable_product_passed": bool(final_result.get("passed")),
            "real_code_product_ready": real_code_product_ready,
            "text_product_ready": text_product_ready,
            "final_product_surface_ready": final_product_surface_ready,
            "plan_product_kind": plan_product_kind,
            "final_product_delta_applied_count": final_product_delta_applied_count,
            "provider_execution_performed": bool(
                external_contract.get("provider_execution_performed")
            ),
            "missing_roles": external_contract.get("missing_roles") or [],
            "provider_rejection_reasons": external_contract.get("provider_rejection_reasons") or [],
            "pointer_block_count": external_contract.get("pointer_block_count"),
            "resume_from_block_id": external_contract.get("resume_from_block_id"),
        },
        "product_blocked_reason": blocked_reason,
        "resume_from_block_id": external_contract.get("resume_from_block_id", ""),
        "latest_block_id": external_contract.get("latest_block_id", ""),
        "continuation_required": continuation_required,
        "soft_close_reason": soft_close_reason,
        "runtime_governor_semantics": (
            "budget_iterations_rounds_and_provider_revisions_are_soft_governors"
        ),
    }


def _blocked_reason(
    *,
    approved: bool,
    continuation_required: bool,
    launcher_contract_errors: list[str],
    final_payload: dict[str, Any],
    external_contract: dict[str, Any],
) -> str:
    if approved:
        return ""
    final_reason = _final_payload_reason(final_payload)
    if final_reason and final_reason != "runtime_soft_governor_left_resume_pointer":
        return final_reason
    provider_reasons = [
        str(item)
        for item in (external_contract.get("provider_rejection_reasons") or [])
        if str(item).strip()
    ]
    if provider_reasons:
        return ",".join(provider_reasons)
    missing_roles = [
        str(item) for item in (external_contract.get("missing_roles") or []) if str(item).strip()
    ]
    if missing_roles and not external_contract.get("provider_execution_performed"):
        return "provider_runtime_missing_verified_roles:" + ",".join(missing_roles)
    if continuation_required:
        return final_reason or "runtime_soft_governor_left_resume_pointer"
    blocking = final_payload.get("blocking_reasons")
    if isinstance(blocking, list) and blocking:
        return str(blocking[0])
    if launcher_contract_errors:
        return launcher_contract_errors[0]
    return "runtime_product_not_approved"


def _soft_close_reason(
    *,
    approved: bool,
    continuation_required: bool,
    blocked_reason: str,
    final_payload: dict[str, Any],
) -> str:
    if approved:
        return ""
    final_reason = _final_payload_reason(final_payload)
    if final_reason and final_reason != "runtime_soft_governor_left_resume_pointer":
        return final_reason
    if continuation_required:
        return blocked_reason or final_reason or "runtime_soft_governor_left_resume_pointer"
    return ""


def _final_payload_reason(final_payload: dict[str, Any]) -> str:
    for key in ("product_blocked_reason", "soft_close_reason"):
        value = str(final_payload.get(key) or "").strip()
        if value:
            return value
    return ""


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
