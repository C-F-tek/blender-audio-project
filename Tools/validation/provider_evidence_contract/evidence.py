"""Provider evidence classifiers."""

from __future__ import annotations

from typing import Any

from .common import first_text, is_fallback_artifact, safe_int, safe_list

def gpu_provider_evidence(gpu_report: dict[str, Any]) -> dict[str, Any]:
    rounds = safe_list(gpu_report.get("rounds"))
    round_count = safe_int(gpu_report.get("round_count"), len(rounds))
    provider_performed = bool(gpu_report.get("provider_execution_performed"))
    provider_empty = bool(
        gpu_report.get("provider_empty_response") or gpu_report.get("provider_empty_response_count")
    )
    provider_error = first_text(
        gpu_report.get("provider_error"), "; ".join(map(str, safe_list(gpu_report.get("errors"))))
    )
    real = bool(
        gpu_report
        and not is_fallback_artifact(gpu_report)
        and provider_performed
        and round_count > 0
        and not provider_empty
    )
    return {
        "real": real,
        "passed": gpu_report.get("passed"),
        "provider_execution_performed": provider_performed,
        "round_count": round_count,
        "recommendation_count": safe_int(gpu_report.get("recommendation_count")),
        "provider_empty_response": provider_empty,
        "classification": gpu_report.get("classification"),
        "provider_error": provider_error,
    }

def npu_provider_evidence(orchestrator: dict[str, Any]) -> dict[str, Any]:
    audits = [item for item in safe_list(orchestrator.get("npu_audits")) if isinstance(item, dict)]
    success_count = sum(
        1
        for item in audits
        if item.get("provider_execution_succeeded") is True
        or item.get("provider_execution_performed") is True
        or item.get("classification") == "usable_audit_text"
    )
    load_attempt_count = sum(1 for item in audits if item.get("provider_load_attempted") is True)
    requested_count = sum(1 for item in audits if item.get("provider_execution_requested") is True)
    return {
        "real": success_count > 0,
        "audit_count": len(audits),
        "requested_count": requested_count,
        "load_attempt_count": load_attempt_count,
        "success_count": success_count,
        "lane_mode": orchestrator.get("npu_lane_mode"),
        "lane": orchestrator.get("npu_lane")
        if isinstance(orchestrator.get("npu_lane"), dict)
        else {},
    }

def npu_micro_support_evidence(orchestrator: dict[str, Any]) -> dict[str, Any]:
    supports = [
        item for item in safe_list(orchestrator.get("npu_micro_supports")) if isinstance(item, dict)
    ]
    provider_success_count = sum(
        1
        for item in supports
        if item.get("provider_execution_performed") is True
        or item.get("provider_execution_succeeded") is True
        or item.get("classification") == "usable_audit_text"
    )
    requested_count = sum(
        1 for item in supports if item.get("provider_execution_requested") is True
    )
    overlap_count = sum(1 for item in supports if item.get("launched_while_gpu1_active") is True)
    tool_request_count = sum(safe_int(item.get("npu_tool_request_count")) for item in supports)
    runtime_execution_count = sum(
        safe_int((item.get("npu_runtime_tool_broker") or {}).get("tool_execution_count"))
        for item in supports
        if isinstance(item.get("npu_runtime_tool_broker"), dict)
    )
    fallback_count = sum(
        safe_int(item.get("npu_deterministic_tool_fallback_count")) for item in supports
    )
    tool_success_count = sum(
        1
        for item in supports
        if safe_int(item.get("npu_tool_request_count")) > 0
        or safe_int(item.get("npu_deterministic_tool_fallback_count")) > 0
        or (
            isinstance(item.get("npu_runtime_tool_broker"), dict)
            and safe_int(item.get("npu_runtime_tool_broker", {}).get("tool_execution_count")) > 0
        )
    )
    lane = (
        orchestrator.get("npu_micro_lane")
        if isinstance(orchestrator.get("npu_micro_lane"), dict)
        else {}
    )
    return {
        "real": provider_success_count > 0 or tool_success_count > 0,
        "support_count": len(supports),
        "requested_count": requested_count,
        "success_count": provider_success_count + tool_success_count,
        "provider_success_count": provider_success_count,
        "tool_success_count": tool_success_count,
        "overlap_count": overlap_count,
        "tool_request_count": tool_request_count,
        "deterministic_tool_fallback_count": fallback_count,
        "runtime_tool_execution_count": runtime_execution_count,
        "tool_lane_performed": tool_success_count > 0
        or runtime_execution_count > 0
        or fallback_count > 0,
        "lane": lane,
        "non_blocking": bool(
            lane.get("non_blocking") or any(item.get("non_blocking") is True for item in supports)
        ),
    }

def probe_evidence(probe: dict[str, Any]) -> dict[str, Any]:
    lane_reports = [item for item in safe_list(probe.get("lane_reports")) if isinstance(item, dict)]
    out: dict[str, Any] = {
        "present": bool(probe),
        "passed": probe.get("passed"),
        "provider_execution_performed": bool(probe.get("provider_execution_performed")),
        "lane_count": len(lane_reports),
        "lanes": {},
    }
    lanes: dict[str, Any] = {}
    for item in lane_reports:
        lane = str(item.get("lane") or "unknown")
        parsed = item.get("parsed_result") if isinstance(item.get("parsed_result"), dict) else {}
        lanes[lane] = {
            "passed": item.get("passed"),
            "provider_execution_performed": item.get("provider_execution_performed"),
            "text_chars": parsed.get("text_chars"),
            "error": first_text(item.get("error"), parsed.get("error")),
            "selected_model": item.get("selected_model"),
        }
    out["lanes"] = lanes
    return out

def openvino_gpu0_secondary_evidence(report: dict[str, Any]) -> dict[str, Any]:
    visible = bool(report.get("openvino_gpu0_visible"))
    probe_performed = bool(report.get("openvino_gpu0_probe_performed"))
    workload_performed = bool(report.get("openvino_gpu0_workload_performed"))
    workload_passed = bool(report.get("openvino_gpu0_workload_passed"))
    provider_performed = bool(
        report.get("openvino_gpu0_provider_execution_performed")
        or report.get("provider_execution_performed")
    )
    gpu1_workload = bool(report.get("openvino_gpu1_workload_performed"))
    real = bool(
        report
        and visible
        and probe_performed
        and workload_performed
        and workload_passed
        and provider_performed
        and not gpu1_workload
    )
    return {
        "real": real,
        "present": bool(report),
        "passed": report.get("passed"),
        "openvino_gpu0_visible": visible,
        "openvino_gpu0_probe_performed": probe_performed,
        "openvino_gpu0_workload_performed": workload_performed,
        "openvino_gpu0_workload_passed": workload_passed,
        "openvino_gpu0_provider_execution_performed": provider_performed,
        "openvino_gpu0_role": report.get("openvino_gpu0_role"),
        "openvino_gpu0_not_primary_advisory": report.get("openvino_gpu0_not_primary_advisory"),
        "openvino_gpu1_reserved_visible": bool(report.get("openvino_gpu1_reserved_visible")),
        "openvino_gpu1_workload_performed": gpu1_workload,
        "selected_device": report.get("selected_device"),
        "available_devices": report.get("available_devices")
        if isinstance(report.get("available_devices"), list)
        else [],
        "errors": safe_list(report.get("errors")),
        "warnings": safe_list(report.get("warnings")),
    }

def gpu0_peer_support_evidence(orchestrator: dict[str, Any]) -> dict[str, Any]:
    supports = [
        item for item in safe_list(orchestrator.get("gpu0_peer_supports")) if isinstance(item, dict)
    ]
    success_items = [
        item
        for item in supports
        if item.get("provider_execution_performed") is True
        and item.get("openvino_gpu0_visible") is True
        and item.get("openvino_gpu0_workload_performed") is True
        and item.get("openvino_gpu0_workload_passed") is True
        and not item.get("openvino_gpu1_workload_performed")
    ]
    overlap_count = sum(1 for item in supports if item.get("launched_while_gpu1_active") is True)
    selected_devices = [
        str(item.get("selected_device"))
        for item in success_items
        if item.get("selected_device") not in (None, "")
    ]
    return {
        "real": bool(success_items),
        "support_count": len(supports),
        "success_count": len(success_items),
        "overlap_count": overlap_count,
        "provider_execution_performed": bool(success_items),
        "selected_devices": selected_devices,
        "lane": orchestrator.get("gpu0_peer_support_lane")
        if isinstance(orchestrator.get("gpu0_peer_support_lane"), dict)
        else {},
        "non_blocking": any(item.get("non_blocking") is True for item in supports),
    }
