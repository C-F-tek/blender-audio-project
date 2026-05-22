"""Runtime loop metric helpers for provider lane state."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import Any, safe_dict, safe_int


def build_provider_lane_metrics(
    owner: Any,
    provider_reports_by_lane: dict[str, dict[str, Any]],
    latest_provider_reports: list[dict[str, Any]],
) -> dict[str, Any]:
    required_lanes = (
        {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}
        if owner.args.allow_provider_generation
        else set()
    )
    lane_names = sorted(provider_reports_by_lane)
    semantic_required = {"gpu0_peer"} if owner.args.allow_provider_generation else set()
    semantic_missing = sorted(
        lane
        for lane in semantic_required
        if lane in provider_reports_by_lane
        and not provider_reports_by_lane.get(lane, {}).get(
            "semantic_provider_execution_performed"
        )
    )
    latest_proposal = owner.latest_proposal_iteration_report()
    gpu0_review = safe_dict(
        provider_reports_by_lane.get("gpu0_peer", {}).get("gpu0_operational_review")
    )
    npu_audit = safe_dict(
        provider_reports_by_lane.get("npu_micro_task_auditor", {}).get(
            "npu_operational_audit"
        )
    )
    npu_report = provider_reports_by_lane.get("npu_micro_task_auditor", {})
    npu_micro_activity_ok = bool(
        npu_report.get("npu_peer_evidence_verified")
        or npu_report.get("npu_peer_activity_performed")
        or npu_report.get("npu_provider_execution_performed")
        or npu_report.get("npu_device_execution_performed")
        or npu_report.get("operational_provider_activity")
    )
    lane_authority = {
        "gpu1_planner": "primary_open_review_close_synthesis",
        "gpu0_peer": "reviewer_refiner_not_primary_closer",
        "npu_micro_task_auditor": "microtask_tool_auditor_not_primary_closer",
    }
    replight_reports = list(getattr(owner, "provider_replight_reports", []) or [])
    replight_reports.extend(
        item for item in latest_provider_reports if item.get("replight_passed") is not None
    )
    return {
        "provider_lane_count": len({item.get("lane") for item in owner.provider_reports}),
        "provider_lane_names": lane_names,
        "required_provider_lanes": sorted(required_lanes),
        "missing_provider_lanes": sorted(required_lanes - set(lane_names)),
        "provider_execution_performed": owner.provider_execution_performed,
        "provider_native_tool_call_count": sum(
            safe_int(item.get("native_tool_call_count")) for item in latest_provider_reports
        ),
        "provider_textual_tool_call_count": sum(
            safe_int(item.get("textual_tool_call_count")) for item in latest_provider_reports
        ),
        "provider_native_tool_loop_requested_count": sum(
            1 for item in latest_provider_reports if item.get("native_tool_loop_requested")
        ),
        "provider_native_tool_loop_supported_count": sum(
            1 for item in latest_provider_reports if item.get("native_tool_loop_supported")
        ),
        "provider_native_tool_missing_lanes": [
            str(item.get("lane") or "unknown")
            for item in latest_provider_reports
            if item.get("native_tool_loop_requested")
            and safe_int(item.get("native_tool_call_count")) <= 0
        ],
        "provider_native_tool_missing_required_lanes": sorted(
            lane
            for lane in required_lanes
            if provider_reports_by_lane.get(lane, {}).get("native_tool_loop_requested")
            and _native_tool_loop_required(lane, provider_reports_by_lane.get(lane, {}))
            and safe_int(provider_reports_by_lane.get(lane, {}).get("native_tool_call_count"))
            <= 0
        ),
        "provider_native_tool_unavailable_required_lanes": sorted(
            lane
            for lane in required_lanes
            if provider_reports_by_lane.get(lane, {}).get("native_tool_loop_requested")
            and _native_tool_loop_required(lane, provider_reports_by_lane.get(lane, {}))
            and not provider_reports_by_lane.get(lane, {}).get("native_tool_loop_supported")
        ),
        "semantic_required_provider_lanes": sorted(semantic_required),
        "provider_semantic_execution_count": sum(
            1
            for item in latest_provider_reports
            if item.get("semantic_provider_execution_performed")
        ),
        "provider_semantic_missing_required_lanes": semantic_missing,
        "provider_teamwork_required": True,
        "provider_replight_required": bool(owner.args.allow_provider_generation),
        "provider_replight_passed_lanes": sorted(
            str(item.get("provider_id") or item.get("lane") or "")
            for item in replight_reports
            if item.get("replight_passed") is True
        ),
        "provider_replight_failed_lanes": sorted(
            str(item.get("provider_id") or item.get("lane") or "")
            for item in replight_reports
            if item.get("replight_passed") is not True
        ),
        "provider_replight_reports": [
            {
                "lane": str(item.get("provider_id") or item.get("lane") or ""),
                "provider_model": item.get("provider_model") or item.get("selected_model"),
                "provider_backend": item.get("provider_backend"),
                "provider_compute_device": item.get("provider_compute_device"),
                "provider_loaded": item.get("provider_loaded"),
                "generated_phrase": item.get("generated_phrase"),
                "prompt_token_count": item.get("prompt_token_count"),
                "completion_token_count": item.get("completion_token_count"),
                "tokens_per_second": item.get("tokens_per_second"),
                "available_tool_names": item.get("available_tool_names") or [],
                "functionalities": item.get("functionalities") or [],
                "replight_passed": item.get("replight_passed"),
                "replight_blocked_reason": item.get("replight_blocked_reason"),
            }
            for item in replight_reports
        ],
        "closure_owner": "gpu1_planner",
        "lane_authority": lane_authority,
        "native_tool_calling_policy": {
            "gpu1_planner": "may_drive_broker_native_tool_calls_and_own_final_synthesis",
            "gpu0_peer": "same_tool_schema_peer_only_requires_later_gpu1_consumption",
            "npu_micro_task_auditor": "micro_audit_native_tools_diagnostic_only",
        },
        "revision_lane_policy": getattr(owner, "provider_revision_lane_policy", {}),
        "npu_micro_timeout_enforced": bool(
            provider_reports_by_lane.get("npu_micro_task_auditor", {}).get(
                "npu_micro_timeout_enforced"
            )
        ),
        "npu_peer_evidence_verified": bool(npu_report.get("npu_peer_evidence_verified")),
        "npu_native_tool_loop_error": str(npu_report.get("npu_native_tool_loop_error") or ""),
        "npu_native_tool_loop_required": bool(npu_report.get("npu_native_tool_loop_required")),
        "delta_context_mode": "startup_full_once_then_pointer_delta_revisions",
        "soft_close_reached": bool(owner.runtime_soft_close_reached()),
        "soft_close_is_finalization_signal_only": bool(
            owner.time_counter_contract.get("soft_close_is_finalization_signal_only")
        ),
        "early_exit_when_product_ready_with_evidence": bool(
            owner.time_counter_contract.get("early_exit_when_product_ready_with_evidence")
        ),
        "latest_proposal_quality_passed": (
            latest_proposal.get("quality_passed") if latest_proposal else None
        ),
        "latest_proposal_reject_reason": str(latest_proposal.get("reject_reason") or ""),
        "latest_proposal_pointer_action": str(latest_proposal.get("pointer_action") or ""),
        "latest_proposal_exit_decision": str(latest_proposal.get("exit_decision") or ""),
        "latest_proposal_target_files": (
            latest_proposal.get("target_files")
            if isinstance(latest_proposal.get("target_files"), list)
            else []
        ),
        "latest_gpu0_review_decision": str(gpu0_review.get("decision") or ""),
        "latest_gpu0_missing_delta_sections": (
            gpu0_review.get("missing_delta_sections")
            if isinstance(gpu0_review.get("missing_delta_sections"), list)
            else []
        ),
        "latest_npu_audit_decision": str(npu_audit.get("decision") or ""),
        "npu_micro_activity_ok": npu_micro_activity_ok,
    }


def _native_tool_loop_required(lane: str, report: dict[str, Any]) -> bool:
    if lane == "npu_micro_task_auditor":
        return bool(report.get("npu_native_tool_loop_required"))
    return True
