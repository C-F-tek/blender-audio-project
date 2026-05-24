"""Soft-lock closure quorum helpers for run-unica."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.gpu0_secondary_decision import (
    gpu0_secondary_reason,
    normalize_gpu0_decision,
)
from ia_carmine.runtime.heap_gate.gpu1_closure_packet import (
    GPU1_DECISION_MISSING,
    derive_gpu1_decision,
    extract_gpu1_closure_decision_packet,
    gpu1_decision_packet_valid,
    gpu1_packets_equivalent,
    normalize_gpu1_decision,
)
from ia_carmine.runtime.heap_gate.runtime_common import Any

GPU1_CLOSURE_DECISIONS = {
    "finalize_product",
    "needs_refine",
    GPU1_DECISION_MISSING,
}
GPU0_CLOSURE_AGREEMENTS = {
    "agree_close",
    "veto_with_reason",
    "refine_once",
    "not_evaluated_waiting_for_gpu1_decision",
}
QUORUM_STATUSES = {
    "waiting_for_provider_start",
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
    events = events or []
    raw_summary = raw_summary or {"open_pointer_count_final": 0}
    latest = getattr(owner, "latest_proposal_iteration_report", lambda: {})() or {}
    response_text = getattr(owner, "response_text", lambda: "")() or ""
    targeted_used = bool(getattr(owner, "soft_lock_targeted_refine_used", False))
    provider_reports = getattr(owner, "provider_reports", []) or []
    npu_advisory = npu_closure_advisory(provider_reports)
    owner.npu_closure_advisory = npu_advisory

    resume_from = _resume_from_latest(latest)
    evidence_block = str(latest.get("block_id") or latest.get("proposal_block_id") or "")
    open_count = int(raw_summary.get("open_pointer_count_final") or 0)
    if _pre_provider_waiting(owner, events, provider_reports):
        return {
            "soft_lock_closure_owner_decision": "",
            "gpu1_closure_decision_packet": {},
            "gpu1_closure_decision_packet_valid": False,
            "gpu0_closure_agreement": "",
            "gpu0_closure_reason": "",
            "npu_closure_advisory": npu_advisory,
            "cpu_closure_validation": "waiting_for_provider_start",
            "closure_quorum_status": "waiting_for_provider_start",
            "closure_quorum_reason": "",
            "soft_lock_targeted_refine_used": targeted_used,
            "resume_from_block_id": "",
            "closure_evidence_block_id": "",
        }

    packet = extract_gpu1_closure_decision_packet(latest)
    owner_decision = normalize_gpu1_decision(
        packet.get("gpu1_decision") if packet else getattr(owner, "soft_lock_closure_owner_decision", "")
    )
    if not packet and owner_decision not in GPU1_CLOSURE_DECISIONS:
        owner_decision = gpu1_closure_decision_from_text(response_text, latest)
    if not packet or not gpu1_decision_packet_valid(packet) or owner_decision not in GPU1_CLOSURE_DECISIONS or owner_decision == GPU1_DECISION_MISSING:
        owner_decision = GPU1_DECISION_MISSING
        owner.soft_lock_closure_owner_decision = owner_decision
        owner.gpu0_closure_agreement = "not_evaluated_waiting_for_gpu1_decision"
        return {
            "soft_lock_closure_owner_decision": owner_decision,
            "gpu1_closure_decision_packet": packet,
            "gpu1_closure_decision_packet_valid": False,
            "gpu0_closure_agreement": "not_evaluated_waiting_for_gpu1_decision",
            "gpu0_closure_reason": "gpu0_veto_not_allowed_without_gpu1_decision",
            "npu_closure_advisory": npu_advisory,
            "cpu_closure_validation": "blocked_provider_or_pointer",
            "closure_quorum_status": "blocked_with_reason",
            "closure_quorum_reason": "gpu0_veto_not_allowed_without_gpu1_decision",
            "soft_lock_targeted_refine_used": targeted_used,
            "resume_from_block_id": resume_from,
            "closure_evidence_block_id": evidence_block or resume_from,
        }

    owner.soft_lock_closure_owner_decision = owner_decision
    gpu0_agreement, gpu0_reason = gpu0_closure_agreement(
        provider_reports,
        latest,
        targeted_used=targeted_used,
        gpu1_packet=packet,
    )
    if gpu0_agreement in GPU0_CLOSURE_AGREEMENTS:
        owner.gpu0_closure_agreement = gpu0_agreement
    status = ""
    reason = ""
    cpu_validation = "waiting_for_gpu1_gpu0_quorum"
    if owner_decision == "needs_refine":
        status = "targeted_refine_allowed" if not targeted_used else "blocked_continuation_ready"
        reason = "GPU1 decision packet requires refinement before closure"
    elif gpu0_agreement == "refine_once" and not targeted_used:
        status = "targeted_refine_allowed"
        reason = gpu0_reason or "GPU0 requested one targeted refinement"
    elif gpu0_agreement == "veto_with_reason":
        status = "blocked_with_reason"
        reason = gpu0_reason or "GPU0 vetoed the GPU1 delta"
    elif gpu0_agreement != "agree_close":
        status = "blocked_with_reason"
        reason = gpu0_reason or "GPU0 closure agreement missing"
    elif owner_decision == "finalize_product" and open_count == 0:
        status = "ready_to_close"
        reason = "GPU1 finalized product and GPU0 agreed with no open pointers"
        cpu_validation = "product_closure_validated"
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
        "gpu1_closure_decision_packet": packet,
        "gpu1_closure_decision_packet_valid": True,
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
    return derive_gpu1_decision(
        quality_passed=latest_report.get("quality_passed") is True,
        exit_decision=str(latest_report.get("exit_decision") or ""),
        pointer_action=str(latest_report.get("pointer_action") or ""),
        reject_reasons=[str(latest_report.get("reject_reason") or "")],
        response_text=haystack,
    )


def gpu0_closure_agreement(
    provider_reports: list[dict[str, Any]],
    latest_report: dict[str, Any] | None = None,
    *,
    targeted_used: bool = False,
    gpu1_packet: dict[str, Any] | None = None,
) -> tuple[str, str]:
    latest_report = latest_report or {}
    packet = extract_gpu1_closure_decision_packet(gpu1_packet or latest_report)
    if not packet or not gpu1_decision_packet_valid(packet):
        return (
            "not_evaluated_waiting_for_gpu1_decision",
            "gpu0_veto_not_allowed_without_gpu1_decision",
        )
    gpu0 = _latest_lane_report(provider_reports, "gpu0_peer")
    if not gpu0:
        return "refine_once", _gpu0_retry_reason(packet, "gpu0_review_missing_for_current_pointer")
    if gpu0.get("provider_device_verified") is not True:
        return "refine_once", _gpu0_retry_reason(packet, "gpu0_device_evidence_not_verified")
    if not (
        gpu0.get("operational_provider_activity")
        or gpu0.get("provider_execution_performed")
        or gpu0.get("device_workload_execution_performed")
    ):
        return "refine_once", _gpu0_retry_reason(packet, "gpu0_report_not_operational_evidence")

    review = gpu0.get("gpu0_operational_review")
    review = review if isinstance(review, dict) else {}
    veto = latest_report.get("cross_lane_veto")
    veto = veto if isinstance(veto, dict) else {}
    veto_reasons = [
        str(item)
        for item in (veto.get("reasons") if isinstance(veto.get("reasons"), list) else [])
        if str(item).strip() and not str(item).strip().lower().startswith("npu ")
    ]
    if veto_reasons and not targeted_used:
        return "refine_once", "; ".join(veto_reasons[:4])
    if gpu0.get("gpu0_secondary_schema_valid") is not True:
        if "gpu0_checked_wrong_gpu1_packet" in (gpu0.get("veto_reasons") or []):
            return "refine_once", _gpu0_retry_reason(packet, "gpu0_checked_wrong_gpu1_packet")
        if not targeted_used:
            return "refine_once", _gpu0_retry_reason(
                packet,
                "gpu0_review_invalid_requires_gpu1_retry",
            )
        return "veto_with_reason", "GPU0 secondary decision schema stayed invalid after refinement"
    if str(gpu0.get("checked_block_id") or "") != str(packet.get("gpu1_block_id") or ""):
        return "refine_once", _gpu0_retry_reason(packet, "gpu0_checked_wrong_gpu1_packet")
    if str(gpu0.get("checked_gpu1_revision") or "") != str(packet.get("gpu1_revision") or ""):
        return "refine_once", _gpu0_retry_reason(packet, "gpu0_checked_wrong_gpu1_packet")
    reviewed_packet = extract_gpu1_closure_decision_packet(gpu0)
    if not reviewed_packet:
        return "refine_once", _gpu0_retry_reason(packet, "gpu0_review_missing_gpu1_packet")
    if not gpu1_packets_equivalent(reviewed_packet, packet):
        return "refine_once", _gpu0_retry_reason(
            packet,
            "gpu0_review_stale_after_gpu1_packet_rewrite",
        )
    if gpu0.get("gpu0_unanchored_reasons") and normalize_gpu0_decision(gpu0.get("gpu0_model_decision")) in {
        "veto",
        "refine_required",
        "incongruent",
    }:
        decision = normalize_gpu0_decision(gpu0.get("gpu0_effective_decision") or gpu0.get("gpu0_decision"))
        if decision == "congruent":
            return "agree_close", "gpu0_unanchored_reason_ignored"
    decision = normalize_gpu0_decision(
        gpu0.get("gpu0_effective_decision")
        or gpu0.get("gpu0_decision")
        or review.get("gpu0_decision")
        or review.get("decision")
    )
    reason = gpu0_secondary_reason({**gpu0, **review})
    if decision == "congruent":
        return "agree_close", reason or "GPU0 structured congruence check passed"
    if decision == "veto":
        return "veto_with_reason", reason or "GPU0 structured veto"
    if decision in {"refine_required", "incongruent"}:
        if not targeted_used:
            return "refine_once", reason or f"GPU0 requested {decision}"
        return "veto_with_reason", reason or f"GPU0 still reports {decision} after refinement"
    return "veto_with_reason", "GPU0 structured decision is invalid"


def _gpu0_retry_reason(packet: dict[str, Any], reason: str) -> str:
    pointer = str(packet.get("gpu1_block_id") or "")
    revision = str(packet.get("gpu1_revision") or "")
    suffix = f":pointer={pointer}" if pointer else ""
    if revision:
        suffix += f":revision={revision}"
    return f"{reason}{suffix}"


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


def _pre_provider_waiting(
    owner: Any,
    events: list[dict[str, Any]],
    provider_reports: list[dict[str, Any]],
) -> bool:
    args = getattr(owner, "args", None)
    if not bool(getattr(args, "allow_provider_generation", False)):
        return False
    if provider_reports:
        return False
    launch_started = getattr(owner, "provider_launch_started", None)
    if callable(launch_started):
        return not bool(launch_started(events))
    for event in events:
        if event.get("event_type") != "provider_state":
            continue
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if payload.get("lane") in {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}:
            return False
    return True


def _has_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)
