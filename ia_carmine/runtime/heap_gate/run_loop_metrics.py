"""Runtime loop metric helpers for provider lane state."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import (
    GPU0_LANE,
    GPU1_LANE,
    NPU_LANE,
    context_hierarchy_payload,
    lane_hierarchy,
)
from ia_carmine.runtime.heap_gate.gpu0_secondary_decision import normalize_gpu0_decision
from ia_carmine.runtime.heap_gate.gpu1_closure_packet import (
    extract_gpu1_closure_decision_packet,
    gpu1_decision_packet_valid,
    gpu1_packets_equivalent,
)
from ia_carmine.runtime.heap_gate.runtime_common import Any, safe_dict, safe_int
from ia_carmine._shared.provider_work_verification import provider_work_status


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
    semantic_required = {GPU0_LANE} if owner.args.allow_provider_generation else set()
    semantic_missing = sorted(
        lane
        for lane in semantic_required
        if lane in provider_reports_by_lane
        and not _lane_has_model_execution(owner.provider_reports, lane)
    )
    latest_proposal = owner.latest_proposal_iteration_report()
    latest_final_product_protocol = safe_dict(
        latest_proposal.get("final_product_protocol") if latest_proposal else {}
    )
    latest_gpu1_packet = extract_gpu1_closure_decision_packet(latest_proposal)
    gpu0_review = safe_dict(
        provider_reports_by_lane.get("gpu0_peer", {}).get("gpu0_operational_review")
    )
    gpu0_report = provider_reports_by_lane.get(GPU0_LANE, {})
    latest_gpu0_reviewed_packet = extract_gpu1_closure_decision_packet(gpu0_report)
    latest_gpu1_packet_valid = gpu1_decision_packet_valid(latest_gpu1_packet)
    latest_gpu1_block_id = str(latest_gpu1_packet.get("gpu1_block_id") or "")
    latest_gpu1_revision = str(latest_gpu1_packet.get("gpu1_revision") or "")
    latest_gpu1_fingerprint = str(latest_gpu1_packet.get("packet_fingerprint") or "")
    latest_gpu0_reviewed_fingerprint = str(
        gpu0_report.get("reviewed_packet_fingerprint")
        or gpu0_review.get("reviewed_packet_fingerprint")
        or gpu0_report.get("expected_packet_fingerprint")
        or gpu0_review.get("expected_packet_fingerprint")
        or latest_gpu0_reviewed_packet.get("packet_fingerprint")
        or ""
    )
    latest_gpu0_checked_block_id = str(
        gpu0_report.get("reviewed_gpu1_block_id")
        or gpu0_review.get("reviewed_gpu1_block_id")
        or gpu0_report.get("checked_block_id")
        or gpu0_review.get("checked_block_id")
        or gpu0_report.get("expected_gpu1_block_id")
        or gpu0_review.get("expected_gpu1_block_id")
        or gpu0_report.get("review_target_pointer")
        or gpu0_review.get("review_target_pointer")
        or ""
    )
    latest_gpu0_checked_revision = str(
        gpu0_report.get("reviewed_revision")
        or gpu0_review.get("reviewed_revision")
        or gpu0_report.get("checked_gpu1_revision")
        or gpu0_review.get("checked_gpu1_revision")
        or gpu0_report.get("expected_gpu1_revision")
        or gpu0_review.get("expected_gpu1_revision")
        or ""
    )
    gpu0_secondary_schema_valid = gpu0_report.get("gpu0_secondary_schema_valid") is True or (
        gpu0_review.get("gpu0_secondary_schema_valid") is True
    )
    latest_gpu0_checked_current_packet = bool(
        gpu0_report.get("gpu0_checked_current_packet")
        or gpu0_review.get("gpu0_checked_current_packet")
    )
    latest_gpu0_packet_stale = bool(
        latest_gpu1_packet
        and (
            (
                latest_gpu0_reviewed_fingerprint
                and latest_gpu0_reviewed_fingerprint != latest_gpu1_fingerprint
            )
            or (
                latest_gpu0_reviewed_packet
                and not gpu1_packets_equivalent(latest_gpu0_reviewed_packet, latest_gpu1_packet)
            )
            or (
                latest_gpu0_checked_block_id
                and latest_gpu0_checked_block_id != latest_gpu1_block_id
            )
            or (
                latest_gpu0_checked_revision
                and latest_gpu0_checked_revision != latest_gpu1_revision
            )
        )
    )
    latest_gpu1_block_reviewed_by_gpu0 = bool(
        latest_gpu1_packet_valid
        and gpu0_secondary_schema_valid
        and latest_gpu0_checked_current_packet
        and latest_gpu0_checked_block_id == latest_gpu1_block_id
        and latest_gpu0_checked_revision == latest_gpu1_revision
        and latest_gpu0_reviewed_fingerprint == latest_gpu1_fingerprint
        and not latest_gpu0_packet_stale
    )
    gpu0_decision = normalize_gpu0_decision(
        gpu0_report.get("gpu0_effective_decision")
        or gpu0_report.get("gpu0_decision")
        or gpu0_review.get("gpu0_effective_decision")
        or gpu0_review.get("gpu0_decision")
        or gpu0_review.get("decision")
    )
    npu_audit = safe_dict(
        provider_reports_by_lane.get("npu_micro_task_auditor", {}).get(
            "npu_operational_audit"
        )
    )
    npu_report = provider_reports_by_lane.get(NPU_LANE, {})
    npu_micro_activity_ok = bool(
        npu_report.get("npu_peer_evidence_verified")
        or npu_report.get("npu_peer_activity_performed")
        or npu_report.get("npu_provider_execution_performed")
        or npu_report.get("npu_device_execution_performed")
        or npu_report.get("operational_provider_activity")
    )
    hierarchy = {
        lane: lane_hierarchy(lane)
        for lane in (GPU1_LANE, GPU0_LANE, NPU_LANE)
    }
    lane_authority = {lane: data.get("authority") for lane, data in hierarchy.items()}
    context_payload = context_hierarchy_payload(
        owner.args, gpu1_ctx=getattr(owner, "selected_ollama_num_ctx", None)
    )
    consumed_peer_block_ids = _consumed_peer_block_ids(owner.provider_reports)
    latest_gpu1_report = next(
        (
            item
            for item in reversed(latest_provider_reports)
            if str(item.get("lane") or "") == GPU1_LANE
        ),
        {},
    )
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
        "gpu1_native_tool_call_count": safe_int(
            latest_gpu1_report.get("native_tool_call_count")
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
            and item.get("native_tool_loop_supported")
            and safe_int(item.get("native_tool_call_count")) <= 0
        ],
        "provider_native_tool_missing_required_lanes": sorted(
            lane
            for lane in required_lanes
            if provider_reports_by_lane.get(lane, {}).get("native_tool_loop_requested")
            and _native_tool_loop_required(lane, provider_reports_by_lane.get(lane, {}))
            and provider_reports_by_lane.get(lane, {}).get("native_tool_loop_supported")
            and not provider_reports_by_lane.get(lane, {}).get(
                "provider_native_tool_api_attempt_failed"
            )
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
        "provider_native_tool_attempt_failed_required_lanes": sorted(
            lane
            for lane in required_lanes
            if provider_reports_by_lane.get(lane, {}).get("native_tool_loop_requested")
            and _native_tool_loop_required(lane, provider_reports_by_lane.get(lane, {}))
            and provider_reports_by_lane.get(lane, {}).get(
                "provider_native_tool_api_attempt_failed"
            )
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
        "lane_tiers": {lane: data.get("lane_tier") for lane, data in hierarchy.items()},
        "lane_authority": lane_authority,
        "lane_context_budgets": {
            "gpu1_planner": context_payload.get("gpu1_context_budget"),
            "gpu0_peer": context_payload.get("gpu0_context_budget"),
            "npu_micro_task_auditor": context_payload.get("npu_context_budget"),
        },
        "gpu1_context_budget": context_payload.get("gpu1_context_budget"),
        "gpu0_context_budget": context_payload.get("gpu0_context_budget"),
        "npu_context_budget": context_payload.get("npu_context_budget"),
        "context_hierarchy_valid": context_payload.get("context_hierarchy_valid"),
        "context_hierarchy_label": context_payload.get("context_hierarchy_label"),
        "context_hierarchy_scope": context_payload.get("context_hierarchy_scope"),
        "context_hierarchy_rule": context_payload.get("context_hierarchy_rule"),
        "operator_effective_provider_config": context_payload.get("operator_effective_config"),
        "gpu1_lane_identity": context_payload.get("gpu1_lane_identity"),
        "gpu1_replight_scope": context_payload.get("gpu1_replight_scope"),
        "gpu1_replight_valid": bool(getattr(owner, "gpu1_replight_valid", False)),
        "gpu1_boot_leader_ready": bool(
            getattr(owner, "gpu1_boot_leader_ready", False)
        ),
        "gpu1_primary_workload_valid": bool(
            getattr(owner, "gpu1_primary_workload_valid", False)
        ),
        "gpu1_primary_evidence_valid": bool(
            getattr(owner, "gpu1_primary_evidence_valid", False)
        ),
        "gpu1_primary_evidence_source": str(
            getattr(owner, "gpu1_primary_evidence_source", "") or ""
        ),
        "gpu1_primary_workload_chars": safe_int(
            getattr(owner, "gpu1_primary_workload_chars", 0)
        ),
        "gpu1_primary_workload_tokens": safe_int(
            getattr(owner, "gpu1_primary_workload_tokens", 0)
        ),
        "leader_source": str(getattr(owner, "leader_source", "") or "none"),
        "sidecars_start_policy": str(
            getattr(owner, "sidecars_start_policy", "") or ""
        ),
        "sidecar_scope_mode": str(
            getattr(owner, "provider_sidecar_scope_mode", "") or "packet_review_only"
        ),
        "pending_provider_sidecar_count": _pending_provider_sidecar_count(owner),
        "sidecar_async_pending": bool(_pending_provider_sidecar_count(owner) > 0),
        "parallel_provider_overlap_seconds": getattr(
            owner, "parallel_provider_overlap_seconds", 0.0
        ),
        "gpu1_idle_after_primary_seconds": getattr(
            owner, "gpu1_idle_after_primary_seconds", 0.0
        ),
        "sidecar_alone_after_gpu1_seconds": getattr(
            owner, "sidecar_alone_after_gpu1_seconds", 0.0
        ),
        "provider_lane_workload_metrics": _lane_workload_metrics(latest_provider_reports),
        "device_identity_map": _device_identity_map(latest_provider_reports),
        "gpu1_leader_valid": bool(getattr(owner, "gpu1_leader_valid", False)),
        "gpu1_leader_block_id": str(getattr(owner, "gpu1_leader_block_id", "") or ""),
        "gpu1_consumed_generic_write_block_ids": list(
            getattr(owner, "gpu1_consumed_generic_write_block_ids", []) or []
        ),
        "consumed_peer_block_ids": consumed_peer_block_ids,
        "gpu1_consumed_gpu0_peer": bool(
            any(str(block).find(":gpu0_peer:") >= 0 for block in consumed_peer_block_ids)
        ),
        "gpu1_consumed_npu_peer": bool(
            any(str(block).find(":npu_micro_task_auditor:") >= 0 for block in consumed_peer_block_ids)
        ),
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
        "npu_peer_evidence_available": bool(npu_report.get("npu_peer_evidence_verified")),
        "npu_native_tool_loop_error": str(npu_report.get("npu_native_tool_loop_error") or ""),
        "npu_native_tool_loop_required": bool(npu_report.get("npu_native_tool_loop_required")),
        "delta_context_mode": "startup_full_once_then_pointer_delta_revisions",
        "soft_close_reached": bool(owner.runtime_soft_close_reached()),
        "terminal_validation_scope": (
            "sampled_on_soft_close"
            if bool(owner.runtime_soft_close_reached())
            else "full_required_product"
        ),
        "soft_close_is_finalization_signal_only": bool(
            owner.time_counter_contract.get("soft_close_is_finalization_signal_only")
        ),
        "early_exit_when_product_ready_with_evidence": bool(
            owner.time_counter_contract.get("early_exit_when_product_ready_with_evidence")
        ),
        "latest_proposal_quality_passed": (
            latest_proposal.get("quality_passed") if latest_proposal else None
        ),
        "gpu1_closure_decision_packet": latest_gpu1_packet,
        "gpu1_closure_decision_packet_valid": gpu1_decision_packet_valid(
            latest_gpu1_packet
        ),
        "latest_gpu1_decision": str(latest_gpu1_packet.get("gpu1_decision") or ""),
        "latest_gpu1_block_id": latest_gpu1_block_id,
        "latest_gpu1_revision": latest_gpu1_revision,
        "latest_gpu1_refine_continuity": (
            latest_proposal.get("gpu1_refine_continuity")
            if isinstance(latest_proposal.get("gpu1_refine_continuity"), dict)
            else {}
        ),
        "latest_proposal_reject_reason": str(latest_proposal.get("reject_reason") or ""),
        "latest_proposal_pointer_action": str(latest_proposal.get("pointer_action") or ""),
        "latest_proposal_exit_decision": str(latest_proposal.get("exit_decision") or ""),
        "latest_final_product_kind": str(latest_proposal.get("final_product_kind") or ""),
        "latest_final_product_action": str(latest_proposal.get("final_product_action") or ""),
        "latest_final_product_delta_valid": (
            latest_proposal.get("final_product_delta_valid") if latest_proposal else None
        ),
        "latest_final_product_pointer_protocol_operational": (
            latest_final_product_protocol.get("pointer_protocol_operational")
            if latest_final_product_protocol
            else None
        ),
        "latest_final_product_protocol_errors": (
            latest_final_product_protocol.get("errors")
            if isinstance(latest_final_product_protocol.get("errors"), list)
            else []
        ),
        "latest_proposal_target_files": (
            latest_proposal.get("target_files")
            if isinstance(latest_proposal.get("target_files"), list)
            else []
        ),
        "gpu0_secondary_schema_valid": gpu0_secondary_schema_valid,
        "latest_gpu1_block_requires_gpu0_review": bool(latest_gpu1_packet),
        "latest_gpu1_block_reviewed_by_gpu0": latest_gpu1_block_reviewed_by_gpu0,
        "gpu0_review_invalid_requires_gpu1_retry": bool(
            latest_gpu1_packet and not latest_gpu1_block_reviewed_by_gpu0
        ),
        "latest_gpu0_review_decision": gpu0_decision,
        "sidecar_incongruent": bool(
            gpu0_decision == "incongruent"
            or gpu0_report.get("sidecar_incongruent")
            or npu_report.get("sidecar_incongruent")
        ),
        "sidecar_invalid": bool(
            gpu0_report.get("sidecar_invalid")
            or npu_report.get("sidecar_invalid")
            or gpu0_report.get("provider_rejection_reason")
            or npu_report.get("provider_rejection_reason")
        ),
        "gpu1_congruence_check_performed": bool(
            getattr(owner, "provider_recovery_attempt_count", 0)
            or any(
                str(report.get("lane") or "") == GPU1_LANE
                and safe_int(report.get("revision")) > max(
                    safe_int(gpu0_report.get("revision")),
                    safe_int(npu_report.get("revision")),
                )
                for report in owner.provider_reports
            )
        ),
        "latest_gpu0_model_decision": normalize_gpu0_decision(
            gpu0_report.get("gpu0_model_decision")
            or gpu0_review.get("gpu0_model_decision")
        ),
        "latest_gpu0_effective_decision": gpu0_decision,
        "latest_gpu0_role_decision": str(
            gpu0_report.get("role_decision") or gpu0_review.get("role_decision") or ""
        ),
        "latest_gpu0_checked_current_packet": latest_gpu0_checked_current_packet,
        "latest_gpu0_packet_stale_after_gpu1_packet_rewrite": latest_gpu0_packet_stale,
        "latest_gpu0_reviewed_packet_fingerprint": str(
            latest_gpu0_reviewed_fingerprint
        ),
        "latest_gpu1_packet_fingerprint": str(
            latest_gpu1_fingerprint
        ),
        "latest_gpu0_expected_gpu1_block_id": str(
            latest_gpu0_checked_block_id
        ),
        "latest_gpu0_expected_gpu1_revision": str(
            latest_gpu0_checked_revision
        ),
        "latest_gpu0_unanchored_reasons": (
            gpu0_report.get("gpu0_unanchored_reasons")
            if isinstance(gpu0_report.get("gpu0_unanchored_reasons"), list)
            else (
                gpu0_review.get("gpu0_unanchored_reasons")
                if isinstance(gpu0_review.get("gpu0_unanchored_reasons"), list)
                else []
            )
        ),
        "latest_gpu0_decision_override_reason": str(
            gpu0_report.get("gpu0_decision_override_reason")
            or gpu0_review.get("gpu0_decision_override_reason")
            or ""
        ),
        "latest_gpu0_veto_reasons": (
            gpu0_report.get("veto_reasons")
            if isinstance(gpu0_report.get("veto_reasons"), list)
            else (
                gpu0_review.get("veto_reasons")
                if isinstance(gpu0_review.get("veto_reasons"), list)
                else []
            )
        ),
        "latest_gpu0_incongruence_reasons": (
            gpu0_report.get("incongruence_reasons")
            if isinstance(gpu0_report.get("incongruence_reasons"), list)
            else (
                gpu0_review.get("incongruence_reasons")
                if isinstance(gpu0_review.get("incongruence_reasons"), list)
                else []
            )
        ),
        "latest_gpu0_free_text_used_as_product": bool(
            gpu0_report.get("free_text_used_as_product")
            or gpu0_review.get("free_text_used_as_product")
        ),
        "latest_gpu0_free_text_used_as_decision": bool(
            gpu0_report.get("free_text_used_as_decision")
            or gpu0_review.get("free_text_used_as_decision")
        ),
        "latest_gpu0_missing_delta_sections": (
            gpu0_review.get("missing_delta_sections")
            if isinstance(gpu0_review.get("missing_delta_sections"), list)
            else []
        ),
        "latest_npu_audit_decision": str(npu_audit.get("decision") or ""),
        "npu_lane_contract": str(
            npu_report.get("npu_lane_contract") or "microtask_tool_calling_openvino"
        ),
        "npu_micro_activity_ok": npu_micro_activity_ok,
    }


def _native_tool_loop_required(lane: str, report: dict[str, Any]) -> bool:
    if lane == "npu_micro_task_auditor":
        return bool(report.get("npu_native_tool_loop_required"))
    return True


def _device_identity_map(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for report in reports:
        lane = str(report.get("lane") or "").strip()
        if lane not in {GPU1_LANE, GPU0_LANE, NPU_LANE}:
            continue
        items.append(
            {
                "logical_lane": report.get("logical_lane") or lane,
                "provider_compute_device": report.get("provider_compute_device"),
                "provider_backend_device_id": report.get("provider_backend_device_id"),
                "windows_task_manager_device_hint": report.get(
                    "windows_task_manager_device_hint"
                ),
                "vulkan_visible_device": report.get("vulkan_visible_device"),
                "vulkan_device_name": report.get("vulkan_device_name"),
                "vulkan_vendor_id": report.get("vulkan_vendor_id"),
                "device_identity_verified": report.get("device_identity_verified"),
            }
        )
    return items


def _lane_has_model_execution(reports: list[dict[str, Any]], lane: str) -> bool:
    for report in reversed(reports):
        if str(report.get("lane") or "") != lane:
            continue
        if provider_work_status(lane=lane, report=report).get("provider_work_verified"):
            return True
    return False


def _pending_provider_sidecar_count(owner: Any) -> int:
    total = 0
    for collection in getattr(owner, "pending_provider_sidecar_collections", []) or []:
        sidecar_items = (
            collection.get("sidecar_items")
            if isinstance(collection, dict)
            and isinstance(collection.get("sidecar_items"), list)
            else []
        )
        total += sum(
            1
            for item in sidecar_items
            if isinstance(item, dict)
            and item.get("completed") is None
            and item.get("process") is not None
        )
    return total


def _consumed_peer_block_ids(reports: list[dict[str, Any]]) -> list[str]:
    for report in reversed(reports):
        if str(report.get("lane") or "") != GPU1_LANE:
            continue
        consumed: list[str] = []
        for key in (
            "gpu1_consumed_peer_block_ids",
            "consumed_peer_block_ids",
            "consumed_gpu0_review_block_ids",
            "consumed_gpu0_block_ids",
            "consumed_npu_block_ids",
            "consumed_provider_block_ids",
            "consumed_block_ids",
        ):
            refs = report.get(key)
            if isinstance(refs, list):
                for item in refs:
                    value = str(item).strip()
                    if value and value not in consumed:
                        consumed.append(value)
        if consumed:
            return consumed
    return []


def _lane_workload_metrics(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics: list[dict[str, Any]] = []
    for report in reports:
        lane = str(report.get("lane") or "")
        if lane not in {GPU1_LANE, GPU0_LANE, NPU_LANE}:
            continue
        metrics.append(
            {
                "lane": lane,
                "provider_cycle_id": report.get("provider_cycle_id")
                if report.get("provider_cycle_id") is not None
                else report.get("revision"),
                "workload_elapsed_seconds": report.get("elapsed_seconds"),
                "prompt_eval_count": report.get("prompt_eval_count")
                or report.get("prompt_token_count"),
                "eval_count": report.get("eval_count")
                or report.get("completion_token_count"),
                "work_verified": bool(
                    report.get("provider_work_verified")
                    or report.get("gpu1_primary_workload_valid")
                ),
                "accepted_by_gpu1": bool(
                    lane == GPU1_LANE
                    or str(report.get("provider_block_id") or "")
                    in _consumed_peer_block_ids(reports)
                ),
            }
        )
    return metrics
