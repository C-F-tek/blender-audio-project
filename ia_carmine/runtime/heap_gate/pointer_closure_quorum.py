"""Soft-lock closure quorum helpers for run-unica."""

from __future__ import annotations

import re

from ia_carmine.runtime.heap_gate.runtime_common import Any

GPU1_CLOSURE_DECISIONS = {
    "finalize_product",
    "blocked_continuation",
    "no_more_action",
    "needs_gpu0_refine",
}
GPU0_CLOSURE_AGREEMENTS = {"agree_close", "veto_with_reason", "refine_once"}
QUORUM_STATUSES = {
    "ready_to_close",
    "targeted_refine_allowed",
    "blocked_continuation_ready",
    "blocked_with_reason",
}


def closure_quorum_state(
    owner: Any,
    events: list[dict[str, Any]] | None = None,
    *,
    raw_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the GPU1+GPU0 soft-lock quorum state.

    NPU is deliberately advisory here: it can strengthen evidence, but it must
    not be a closer or keep the soft-lock loop alive.
    """
    del events
    raw_summary = raw_summary or {"open_pointer_count_final": 0}
    latest = getattr(owner, "latest_proposal_iteration_report", lambda: {})() or {}
    response_text = getattr(owner, "response_text", lambda: "")() or ""
    owner_decision = str(getattr(owner, "soft_lock_closure_owner_decision", "") or "")
    if owner_decision not in GPU1_CLOSURE_DECISIONS:
        owner_decision = gpu1_closure_decision_from_text(response_text, latest)
    if owner_decision in GPU1_CLOSURE_DECISIONS:
        owner.soft_lock_closure_owner_decision = owner_decision

    targeted_used = bool(getattr(owner, "soft_lock_targeted_refine_used", False))
    gpu0_agreement, gpu0_reason = gpu0_closure_agreement(
        getattr(owner, "provider_reports", []) or [],
        latest,
        targeted_used=targeted_used,
    )
    if gpu0_agreement in GPU0_CLOSURE_AGREEMENTS:
        owner.gpu0_closure_agreement = gpu0_agreement
    npu_advisory = npu_closure_advisory(getattr(owner, "provider_reports", []) or [])
    owner.npu_closure_advisory = npu_advisory

    resume_from = _resume_from_latest(latest)
    evidence_block = str(latest.get("block_id") or latest.get("proposal_block_id") or "")
    open_count = int(raw_summary.get("open_pointer_count_final") or 0)
    status = ""
    reason = ""
    cpu_validation = "waiting_for_gpu1_gpu0_quorum"
    if owner_decision == "needs_gpu0_refine":
        status = "targeted_refine_allowed" if not targeted_used else "blocked_continuation_ready"
        reason = "GPU1 requested GPU0-targeted refinement before closure"
    elif gpu0_agreement in {"veto_with_reason", "refine_once"} and not targeted_used:
        status = "targeted_refine_allowed"
        reason = gpu0_reason or "GPU0 requested one targeted refinement"
    elif not owner_decision:
        status = ""
        reason = "GPU1 closure decision not available yet"
    elif gpu0_agreement != "agree_close":
        status = "blocked_with_reason"
        reason = gpu0_reason or "GPU0 closure agreement missing"
    elif owner_decision == "finalize_product" and open_count == 0:
        status = "ready_to_close"
        reason = "GPU1 finalized product and GPU0 agreed with no open pointers"
        cpu_validation = "product_closure_validated"
    elif owner_decision in {"blocked_continuation", "no_more_action"}:
        status = "blocked_continuation_ready"
        reason = "GPU1 declared no further useful action in this run and GPU0 agreed"
        cpu_validation = "continuation_closure_validated"
    elif owner_decision == "finalize_product" and open_count > 0:
        status = "blocked_continuation_ready"
        reason = "GPU1 finalized but pointer graph still requires resume/defer closure"
        cpu_validation = "continuation_closure_validated"
    else:
        status = "blocked_with_reason"
        reason = "closure quorum state could not be classified"

    if status == "targeted_refine_allowed":
        cpu_validation = "one_targeted_refine_allowed"
    elif status == "blocked_with_reason":
        cpu_validation = "blocked_provider_or_pointer"

    return {
        "soft_lock_closure_owner_decision": owner_decision,
        "gpu0_closure_agreement": gpu0_agreement,
        "gpu0_closure_reason": gpu0_reason,
        "npu_closure_advisory": npu_advisory,
        "cpu_closure_validation": cpu_validation,
        "closure_quorum_status": status,
        "closure_quorum_reason": reason,
        "soft_lock_targeted_refine_used": targeted_used,
        "resume_from_block_id": resume_from,
        "closure_evidence_block_id": evidence_block or resume_from,
    }


def gpu1_closure_decision_from_text(
    text: str,
    latest_report: dict[str, Any] | None = None,
) -> str:
    latest_report = latest_report or {}
    haystack = "\n".join(
        [
            str(text or ""),
            str(latest_report.get("exit_decision") or ""),
            str(latest_report.get("pointer_action") or ""),
            str(latest_report.get("reject_reason") or ""),
        ]
    ).upper()
    if latest_report.get("quality_passed") is True:
        return "finalize_product"
    if _has_any(haystack, ("NEEDS_GPU0_REFINE", "GPU0_REFINE_REQUIRED")):
        return "needs_gpu0_refine"
    if _has_any(
        haystack,
        ("BLOCKED_CONTINUATION", "DEFERRED_TO_RESUME", "CONTINUATION_REQUIRED"),
    ):
        return "blocked_continuation"
    if _has_any(haystack, ("FINALIZE_RUN", "FINAL_PRODUCT_APPROVED", "FINALIZE_PRODUCT")):
        return "finalize_product"
    if _has_any(haystack, ("NO_MORE_ACTION", "NO PATCHABLE TARGET", "NO_PATCHABLE_TARGET")):
        return "no_more_action"
    return ""


def gpu0_closure_agreement(
    provider_reports: list[dict[str, Any]],
    latest_report: dict[str, Any] | None = None,
    *,
    targeted_used: bool = False,
) -> tuple[str, str]:
    latest_report = latest_report or {}
    gpu0 = _latest_lane_report(provider_reports, "gpu0_peer")
    if not gpu0:
        return "", "GPU0 closure report missing"
    if gpu0.get("provider_device_verified") is not True:
        return "veto_with_reason", "GPU0 device evidence is not verified"
    if not (
        gpu0.get("operational_provider_activity")
        or gpu0.get("provider_execution_performed")
        or gpu0.get("device_workload_execution_performed")
    ):
        return "veto_with_reason", "GPU0 report is not operational evidence"

    role_decision = str(gpu0.get("role_decision") or "")
    response = str(gpu0.get("response_text") or "")
    review = gpu0.get("gpu0_operational_review")
    review_text = str(review if not isinstance(review, dict) else review.get("decision") or review)
    veto = latest_report.get("cross_lane_veto")
    veto = veto if isinstance(veto, dict) else {}
    veto_reasons = [
        str(item)
        for item in (veto.get("reasons") if isinstance(veto.get("reasons"), list) else [])
        if str(item).strip() and not str(item).strip().lower().startswith("npu ")
    ]
    if veto_reasons and not targeted_used:
        return "refine_once", "; ".join(veto_reasons[:4])
    combined = "\n".join([role_decision, response, review_text]).lower()
    if re.search(r"\b(veto|reject|rifiut|non accett|non soddisfacente)\b", combined):
        if not targeted_used:
            return "refine_once", "GPU0 reported a concrete veto/refine signal"
        return "agree_close", "GPU0 veto already consumed by one targeted refinement"
    return "agree_close", "GPU0 has valid evidence and no active concrete veto"


def npu_closure_advisory(provider_reports: list[dict[str, Any]]) -> str:
    npu = _latest_lane_report(provider_reports, "npu_micro_task_auditor")
    if not npu:
        return "missing_or_not_selected"
    if npu.get("provider_device_verified") is True and (
        npu.get("operational_provider_activity")
        or npu.get("npu_micro_audit_performed")
        or npu.get("npu_micro_provider_execution_performed")
        or npu.get("npu_peer_activity_performed")
        or npu.get("npu_provider_execution_performed")
    ):
        return "evidence_ready_non_closer"
    if npu.get("provider_device_verified") is True:
        return "device_verified_warning_only"
    return "diagnostic_only_not_closer"


def _latest_lane_report(
    provider_reports: list[dict[str, Any]],
    lane: str,
) -> dict[str, Any]:
    for report in reversed(provider_reports):
        if str(report.get("lane") or "") == lane:
            return report
    return {}


def _resume_from_latest(latest_report: dict[str, Any]) -> str:
    return str(
        latest_report.get("resume_from_block_id")
        or latest_report.get("block_id")
        or latest_report.get("proposal_block_id")
        or ""
    )


def _has_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)
