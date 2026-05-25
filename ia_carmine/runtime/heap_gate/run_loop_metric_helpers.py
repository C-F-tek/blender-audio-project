"""Helper functions for provider lane runtime metrics."""

from __future__ import annotations

from ia_carmine._shared.provider_work_verification import provider_work_status
from ia_carmine.runtime.heap_gate.gpu1_one_turn_gate import (
    ONE_TURN_SUMMARY_FIELDS,
    one_turn_gate_summary,
    strict_one_turn_gate_passed,
)
from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import GPU0_LANE, GPU1_LANE, NPU_LANE
from ia_carmine.runtime.heap_gate.runtime_common import Any, safe_int


def _native_tool_loop_required(lane: str, report: dict[str, Any]) -> bool:
    if lane == "npu_micro_task_auditor":
        return bool(report.get("npu_native_tool_loop_required"))
    return True


def _latest_one_turn_summary(
    owner: Any,
    latest_gpu1_report: dict[str, Any],
    latest_proposal: dict[str, Any],
) -> dict[str, Any]:
    for source in (latest_proposal, latest_gpu1_report):
        if isinstance(source, dict) and any(key in source for key in ONE_TURN_SUMMARY_FIELDS):
            return {
                key: source.get(key)
                for key in ONE_TURN_SUMMARY_FIELDS
                if key in source
            }
    raw_gate = getattr(owner, "gpu1_one_turn_runtime_gate", {})
    if isinstance(raw_gate, dict) and raw_gate:
        return one_turn_gate_summary(raw_gate, getattr(owner, "repo_root", None))
    return {}


def _one_turn_metrics(summary: dict[str, Any]) -> dict[str, Any]:
    summary = summary if isinstance(summary, dict) else {}
    metrics = {
        "gpu1_one_turn_runtime_gate_present": bool(
            summary.get("gpu1_one_turn_runtime_gate_present")
        ),
        "gpu1_one_turn_runtime_gate_passed": summary.get(
            "gpu1_one_turn_runtime_gate_passed"
        )
        is True,
        "gpu1_one_turn_runtime_gate_path": str(
            summary.get("gpu1_one_turn_runtime_gate_path") or ""
        ),
        "gpu1_one_turn_native_tool_call_count": safe_int(
            summary.get("gpu1_one_turn_native_tool_call_count")
        ),
        "gpu1_one_turn_broker_request_count": safe_int(
            summary.get("gpu1_one_turn_broker_request_count")
        ),
        "gpu1_one_turn_broker_result_count": safe_int(
            summary.get("gpu1_one_turn_broker_result_count")
        ),
        "gpu1_one_turn_broker_result_passed_count": safe_int(
            summary.get("gpu1_one_turn_broker_result_passed_count")
        ),
        "gpu1_one_turn_role_tool_reinjected": summary.get(
            "gpu1_one_turn_role_tool_reinjected"
        )
        is True,
        "gpu1_one_turn_tool_result_consumed": summary.get(
            "gpu1_one_turn_tool_result_consumed"
        )
        is True,
        "gpu1_one_turn_final_product_protocol_valid": summary.get(
            "gpu1_one_turn_final_product_protocol_valid"
        )
        is True,
        "gpu1_one_turn_operator_delta_valid": summary.get(
            "gpu1_one_turn_operator_delta_valid"
        )
        is True,
        "gpu1_one_turn_final_product_delta_valid": summary.get(
            "gpu1_one_turn_final_product_delta_valid"
        )
        is True,
        "gpu1_one_turn_blocker": str(summary.get("gpu1_one_turn_blocker") or ""),
        "gpu1_one_turn_errors": (
            summary.get("gpu1_one_turn_errors")
            if isinstance(summary.get("gpu1_one_turn_errors"), list)
            else []
        ),
    }
    metrics["gpu1_one_turn_strict_fields_passed"] = strict_one_turn_gate_passed(metrics)
    return metrics


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
