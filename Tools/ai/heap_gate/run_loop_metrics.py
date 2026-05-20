"""Runtime loop metric helpers for provider lane state."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import Any, safe_dict, safe_int


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
        npu_report.get("npu_peer_activity_performed")
        or npu_report.get("npu_provider_execution_performed")
        or npu_report.get("npu_device_execution_performed")
        or npu_report.get("operational_provider_activity")
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
            and safe_int(provider_reports_by_lane.get(lane, {}).get("native_tool_call_count"))
            <= 0
        ),
        "provider_native_tool_unavailable_required_lanes": sorted(
            lane
            for lane in required_lanes
            if provider_reports_by_lane.get(lane, {}).get("native_tool_loop_requested")
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
