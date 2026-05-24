"""Provider sidecar recovery contract for pointer-block closure."""

from __future__ import annotations

from pathlib import Path

from ia_carmine._shared.file_backed_transport import report_text
from ia_carmine.runtime.heap_gate.provider_lane_policy import (
    GPU0_LANE,
    NPU_LANE,
    PRIMARY_LANE as GPU1_LANE,
)
from ia_carmine.runtime.heap_gate.runtime_common import Any


RECOVERY_REASON_GPU0_INVALID = "gpu0_review_invalid_requires_gpu1_retry"
RECOVERY_REASON_GPU0_WRONG_PACKET = "gpu0_checked_wrong_gpu1_packet"
RECOVERY_REASON_GPU0_VETO = "veto"
RECOVERY_REASON_GPU0_REFINE = "refine_required"
RECOVERY_REASON_NPU_PENDING = "npu_followup_pending"
RECOVERY_REASON_REJECTED_PROPOSAL = "rejected_gpu1_proposal"
RECOVERY_REASON_SIDECAR_INVALID = "sidecar_invalid"
RECOVERY_REASON_SIDECAR_INCONGRUENT = "sidecar_incongruent"
RECOVERABLE_PROVIDER_RECOVERY_REASONS = {
    RECOVERY_REASON_GPU0_INVALID,
    RECOVERY_REASON_GPU0_WRONG_PACKET,
    RECOVERY_REASON_GPU0_VETO,
    RECOVERY_REASON_GPU0_REFINE,
    RECOVERY_REASON_NPU_PENDING,
    RECOVERY_REASON_SIDECAR_INVALID,
    RECOVERY_REASON_SIDECAR_INCONGRUENT,
}
REPORT_TEXT_PREFIXES = ("gpu0_raw_response_text", "free_text_evidence", "response_text")


def provider_recovery_status(owner: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Return the live sidecar recovery state without flattening the pointer graph."""
    reports = list(getattr(owner, "provider_reports", []) or [])
    latest_gpu1 = _latest_report(reports, GPU1_LANE)
    latest_gpu0 = _latest_report(reports, GPU0_LANE)
    latest_npu = _latest_report(reports, NPU_LANE)
    latest_proposal = owner.latest_proposal_iteration_report()
    latest_sidecar_revision = max(_revision(latest_gpu0), _revision(latest_npu))
    latest_seen_revision = max(
        _revision(latest_gpu1),
        latest_sidecar_revision,
        _revision(latest_proposal),
    )
    roles_observed = _roles_observed(reports)
    roles_verified = _roles_verified(reports)
    roles_observed_invalid = _roles_observed_invalid(reports)
    reasons: list[str] = []

    gpu0_review_target = _gpu0_review_target(latest_gpu0, latest_proposal)
    if latest_gpu0 and latest_gpu0.get("gpu0_secondary_schema_valid") is not True:
        reasons.append(RECOVERY_REASON_GPU0_INVALID)
    if latest_gpu0 and latest_gpu0.get("gpu0_checked_current_packet") is False:
        reasons.append(RECOVERY_REASON_GPU0_WRONG_PACKET)
    gpu0_decision = str(
        (latest_gpu0 or {}).get("gpu0_effective_decision")
        or (latest_gpu0 or {}).get("gpu0_decision")
        or ""
    ).strip().lower()
    if gpu0_decision in {"veto", "refine_required", "incongruent"}:
        reasons.append(gpu0_decision if gpu0_decision != "incongruent" else RECOVERY_REASON_GPU0_REFINE)
    if gpu0_decision == "incongruent":
        reasons.append(RECOVERY_REASON_SIDECAR_INCONGRUENT)
    if latest_gpu0 and _sidecar_invalid(latest_gpu0):
        reasons.append(RECOVERY_REASON_SIDECAR_INVALID)

    npu_decision = str(
        ((latest_npu or {}).get("npu_operational_audit") or {}).get("decision")
        if isinstance((latest_npu or {}).get("npu_operational_audit"), dict)
        else ""
    ).strip().lower()
    npu_text = str(
        report_text(
            Path(str((latest_npu or {}).get("repo_root") or ".")).resolve(strict=False),
            latest_npu or {},
            REPORT_TEXT_PREFIXES,
        ).get("text")
        or ""
    ).lower()
    if latest_npu and (
        npu_decision.startswith("reject")
        or "reject_until" in npu_text
        or "npu_auditor_followup_pending_gpu1_consumption" in npu_text
    ):
        reasons.append(RECOVERY_REASON_NPU_PENDING)
    if latest_npu and _sidecar_invalid(latest_npu):
        reasons.append(RECOVERY_REASON_SIDECAR_INVALID)

    if owner.latest_rejected_proposal_requires_retry():
        reasons.append(RECOVERY_REASON_REJECTED_PROPOSAL)

    reasons = list(dict.fromkeys(reason for reason in reasons if reason))
    attempted_revisions = sorted(
        {
            _revision(report)
            for report in reports
            if str(report.get("lane") or "") == GPU1_LANE
            and _revision(report) > latest_sidecar_revision
        }
    )
    recovery_required = bool(reasons)
    attempted_count = int(getattr(owner, "provider_recovery_attempt_count", 0) or 0)
    recovery_attempted = bool(attempted_count or attempted_revisions)
    next_revision = max(int(getattr(owner, "provider_revision_count", 0) or 0), latest_seen_revision) + 1
    max_revisions = int(getattr(owner.args, "max_provider_revisions", 0) or 0)
    budget_exhausted = recovery_required and max_revisions >= 0 and next_revision > max_revisions
    unconsumed_peer_blocks = _unconsumed_peer_block_ids(owner, reports)
    return {
        "provider_recovery_required": recovery_required,
        "provider_recovery_reason": reasons[0] if reasons else "",
        "provider_recovery_reasons": reasons,
        "provider_recovery_attempted": recovery_attempted,
        "gpu1_recovery_attempted": recovery_attempted,
        "provider_recovery_attempt_count": attempted_count,
        "provider_revision_budget_exhausted": budget_exhausted,
        "next_gpu1_recovery_revision": next_revision if recovery_required else 0,
        "latest_sidecar_revision": latest_sidecar_revision,
        "latest_gpu0_review_target_pointer": gpu0_review_target,
        "latest_gpu0_review_status": _gpu0_status(latest_gpu0),
        "latest_npu_followup_status": _npu_status(latest_npu),
        "sidecar_scope_mode": "packet_review_only",
        "sidecar_invalid": any(reason == RECOVERY_REASON_SIDECAR_INVALID for reason in reasons),
        "sidecar_incongruent": any(reason == RECOVERY_REASON_SIDECAR_INCONGRUENT for reason in reasons),
        "sidecar_recoverable_failure": any(
            reason in RECOVERABLE_PROVIDER_RECOVERY_REASONS
            for reason in reasons
        ),
        "gpu1_congruence_check_required": recovery_required,
        "gpu1_congruence_check_performed": recovery_attempted,
        "unconsumed_peer_block_ids": unconsumed_peer_blocks,
        "roles_observed": roles_observed,
        "roles_verified": roles_verified,
        "roles_observed_invalid": roles_observed_invalid,
        "provider_recovery_chain": [
            "gpu1_initial",
            "gpu0_npu_sidecar_join",
            "gpu1_recovery_attempted" if recovery_attempted else "gpu1_recovery_missing",
        ],
    }


def maybe_run_provider_recovery(
    owner: Any,
    round_id: int,
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Run a focused GPU1 recovery revision when sidecar edges require it."""
    status = provider_recovery_status(owner, events)
    owner.provider_recovery_last_status = status
    if not status.get("provider_recovery_required"):
        return events
    universe_blocked = str(getattr(owner, "provider_universe_blocked_reason", "") or "").strip()
    if universe_blocked and not status.get("sidecar_recoverable_failure"):
        return events
    if status.get("provider_revision_budget_exhausted"):
        _publish_recovery_signal(owner, round_id, status, skipped=True)
        return events

    revision = int(status.get("next_gpu1_recovery_revision") or 0)
    if getattr(owner, "_provider_recovery_last_attempt_round", None) == round_id:
        return events
    attempted = getattr(owner, "_provider_recovery_attempted_revisions", set())
    if revision in attempted:
        return events
    attempted.add(revision)
    owner._provider_recovery_attempted_revisions = attempted
    owner._provider_recovery_last_attempt_round = round_id
    owner.provider_revision_count = revision
    owner.provider_recovery_attempt_count = int(
        getattr(owner, "provider_recovery_attempt_count", 0) or 0
    ) + 1
    owner.provider_revision_feedback = _recovery_feedback(owner, status)
    _publish_recovery_signal(owner, round_id, status, skipped=False)
    owner.run_provider_teamwork(round_id, revision=revision)
    events = owner.read_events()
    if owner.publish_provider_native_tool_calls(round_id, events):
        if owner.heap.pending_broker_requests():
            owner.run_bridge()
        events = owner.read_events()
    text = owner.response_text()
    if text:
        events = owner.persist_current_gpu1_proposal_iteration(
            revision=revision,
            events=events,
            source="gpu1_recovery_revision",
        )
    owner.publish_shared_evidence_facts(round_id, events)
    owner.provider_recovery_last_status = provider_recovery_status(owner, events)
    return owner.read_events()


def _recovery_feedback(owner: Any, status: dict[str, Any]) -> str:
    lines = [
        "PROVIDER_RECOVERY_REQUIRED:",
        "- GPU1 remains closure owner; GPU0/NPU are sidecar evidence edges.",
        "- Produce a new GPU1 pointer block that consumes the listed sidecar evidence.",
        "- If a sidecar is incoherent/invalid and the previous GPU1 block is still valid, record the consumed sidecar block id and advance to the next pointer.",
        "- If a sidecar exposes a real defect, revise the GPU1 block while preserving previous/refines/resume.",
        "- If context must propagate backward, use BACKTRACK_PROPAGATE and then RESUME_FORWARD to the resume_from_block_id.",
        f"- recovery_reasons={','.join(status.get('provider_recovery_reasons') or [])}",
        f"- review_target_pointer={status.get('latest_gpu0_review_target_pointer') or ''}",
        "- required_fields=refines_block_id,consumed_gpu0_block_id,consumed_npu_block_ids,resume_from_block_id,POINTER_ACTION,EXIT_DECISION",
    ]
    peer_blocks = [str(item) for item in status.get("unconsumed_peer_block_ids") or []]
    if peer_blocks:
        lines.append("- unconsumed_peer_block_ids=" + ",".join(peer_blocks))
    latest_gpu0 = _latest_report(list(getattr(owner, "provider_reports", []) or []), GPU0_LANE)
    latest_npu = _latest_report(list(getattr(owner, "provider_reports", []) or []), NPU_LANE)
    if latest_gpu0:
        lines.append("- raw_gpu0_evidence_excerpt=" + _excerpt(latest_gpu0))
    if latest_npu:
        lines.append("- raw_npu_evidence_excerpt=" + _excerpt(latest_npu))
    retry = owner.build_rejected_proposal_retry_feedback()
    if retry:
        lines.append(retry)
    return "\n".join(lines)


def _publish_recovery_signal(
    owner: Any,
    round_id: int,
    status: dict[str, Any],
    *,
    skipped: bool,
) -> None:
    payload = {
        "id": f"{owner.stamp}:provider_recovery:{status.get('next_gpu1_recovery_revision')}",
        **status,
        "gpu1_recovery_revision_scheduled": not skipped,
        "gpu1_recovery_revision_skipped": skipped,
    }
    owner.publish(
        "deterministic",
        "validation_signal",
        payload,
        target="gpu1",
        correlation_id=f"{owner.stamp}:provider-recovery",
        round_id=round_id,
    )
    owner.append_heap_exchange_event(
        {
            "kind": "provider_recovery_required",
            "lane": "deterministic_audit",
            "round": round_id,
            "revision": status.get("next_gpu1_recovery_revision"),
            "summary": status.get("provider_recovery_reason"),
            "skipped": skipped,
        }
    )


def _latest_report(reports: list[dict[str, Any]], lane: str) -> dict[str, Any]:
    for report in reversed(reports):
        if isinstance(report, dict) and str(report.get("lane") or "") == lane:
            return report
    return {}


def _revision(report: dict[str, Any] | None) -> int:
    if not isinstance(report, dict):
        return 0
    for key in ("revision", "provider_cycle_id", "review_for_gpu1_cycle", "audit_for_gpu1_cycle"):
        try:
            return int(report.get(key))
        except (TypeError, ValueError):
            continue
    return 0


def _roles_observed(reports: list[dict[str, Any]]) -> list[str]:
    roles: list[str] = []
    for report in reports:
        role = str(report.get("provider_role") or report.get("role") or report.get("lane") or "")
        if role and role not in roles:
            roles.append(role)
    return roles


def _roles_verified(reports: list[dict[str, Any]]) -> list[str]:
    roles: list[str] = []
    for report in reports:
        if not _report_verified(report):
            continue
        role = str(report.get("provider_role") or report.get("role") or report.get("lane") or "")
        if role and role not in roles:
            roles.append(role)
    return roles


def _roles_observed_invalid(reports: list[dict[str, Any]]) -> list[str]:
    roles: list[str] = []
    for report in reports:
        if _report_verified(report):
            continue
        if not (
            report.get("provider_execution_performed")
            or report.get("operational_provider_activity")
            or report.get("provider_loaded")
            or str(
                report_text(
                    Path(str(report.get("repo_root") or ".")).resolve(strict=False),
                    report,
                    REPORT_TEXT_PREFIXES,
                ).get("text")
                or ""
            ).strip()
        ):
            continue
        role = str(report.get("provider_role") or report.get("role") or report.get("lane") or "")
        if role and role not in roles:
            roles.append(role)
    return roles


def _sidecar_invalid(report: dict[str, Any]) -> bool:
    lane = str(report.get("lane") or "")
    if lane == GPU0_LANE:
        return bool(
            report.get("provider_rejection_reason")
            or report.get("product_blocked_reason")
            or report.get("gpu0_secondary_schema_valid") is not True
            or report.get("provider_work_verified") is False
        )
    if lane == NPU_LANE:
        audit = report.get("npu_operational_audit")
        audit = audit if isinstance(audit, dict) else {}
        decision = str(audit.get("decision") or report.get("npu_micro_decision") or "").lower()
        return bool(
            report.get("provider_rejection_reason")
            or report.get("product_blocked_reason")
            or report.get("provider_work_verified") is False
            or report.get("semantic_contract_passed") is False
            or decision.startswith("reject")
            or "reject_until" in str(
                report_text(
                    Path(str(report.get("repo_root") or ".")).resolve(strict=False),
                    report,
                    REPORT_TEXT_PREFIXES,
                ).get("text")
                or ""
            ).lower()
        )
    return False


def _report_verified(report: dict[str, Any]) -> bool:
    if str(report.get("lane") or "") == GPU0_LANE:
        return bool(report.get("provider_work_verified") and report.get("gpu0_secondary_schema_valid"))
    return bool(
        report.get("provider_work_verified")
        or report.get("gpu1_primary_workload_valid")
    )


def _gpu0_review_target(gpu0: dict[str, Any], proposal: dict[str, Any] | None) -> str:
    proposal = proposal if isinstance(proposal, dict) else {}
    return str(
        gpu0.get("review_target_pointer")
        or gpu0.get("reviewed_gpu1_block_id")
        or gpu0.get("checked_block_id")
        or gpu0.get("expected_gpu1_block_id")
        or proposal.get("block_id")
        or proposal.get("proposal_block_id")
        or ""
    )


def _gpu0_status(report: dict[str, Any]) -> str:
    if not report:
        return "not_observed"
    if report.get("gpu0_secondary_schema_valid") is True:
        return str(report.get("gpu0_effective_decision") or report.get("gpu0_decision") or "congruent")
    return "observed_invalid"


def _npu_status(report: dict[str, Any]) -> str:
    if not report:
        return "not_observed"
    audit = report.get("npu_operational_audit")
    if isinstance(audit, dict) and audit.get("decision"):
        return str(audit.get("decision"))
    if report.get("npu_peer_evidence_verified"):
        return "evidence_ready_non_closer"
    return "observed_invalid"


def _unconsumed_peer_block_ids(owner: Any, reports: list[dict[str, Any]]) -> list[str]:
    consumed: set[str] = set()
    for report in reports:
        if str(report.get("lane") or "") != GPU1_LANE:
            continue
        for key in ("consumed_peer_block_ids", "consumed_gpu0_block_ids", "consumed_npu_block_ids"):
            values = report.get(key)
            if isinstance(values, list):
                consumed.update(str(item) for item in values if str(item).strip())
    peer_blocks: list[str] = []
    for report in reports:
        if str(report.get("lane") or "") not in {GPU0_LANE, NPU_LANE}:
            continue
        block_id = str(report.get("provider_block_id") or report.get("proposal_block_id") or "")
        if block_id and block_id not in consumed:
            peer_blocks.append(block_id)
    return peer_blocks


def _excerpt(report: dict[str, Any], limit: int = 800) -> str:
    text = str(
        report_text(
            Path(str(report.get("repo_root") or ".")).resolve(strict=False),
            report,
            REPORT_TEXT_PREFIXES,
        ).get("text")
        or ""
    )
    return text.replace("\n", " | ")[:limit]
