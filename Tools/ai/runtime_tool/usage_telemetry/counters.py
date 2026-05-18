from __future__ import annotations

from .common import *  # noqa: F403

def provider_evidence_summary(
    orchestrator: dict[str, Any], gpu_report: dict[str, Any]
) -> dict[str, Any]:
    gpu_round_count = safe_int(gpu_report.get("round_count"))
    gpu_provider_performed = bool(
        gpu_report.get("provider_execution_performed")
        and gpu_round_count > 0
        and str(gpu_report.get("classification") or "") != "required_provider_artifact_missing"
        and not bool(gpu_report.get("provider_empty_response"))
    )
    npu_success_count = safe_int(orchestrator.get("npu_audit_success_count"))
    npu_audit_count = safe_int(orchestrator.get("npu_audit_count"))
    npu_provider_performed = npu_success_count > 0
    npu_micro_support_count = safe_int(orchestrator.get("npu_micro_support_count"))
    npu_micro_support_success_count = safe_int(orchestrator.get("npu_micro_support_success_count"))
    npu_micro_runtime_tool_execution_count = safe_int(
        orchestrator.get("npu_micro_runtime_tool_execution_count")
    )
    npu_micro_runtime_tool_live_execution_count = safe_int(
        orchestrator.get("npu_micro_runtime_tool_live_execution_count")
    )
    npu_micro_support_performed = bool(
        npu_micro_support_success_count > 0 or npu_micro_runtime_tool_execution_count > 0
    )
    gpu0_peer_support_performed = bool(
        orchestrator.get("gpu0_peer_support_provider_execution_performed")
    )
    degraded_reasons = []
    raw_reasons = orchestrator.get("provider_degraded_reasons")
    if isinstance(raw_reasons, list):
        degraded_reasons.extend(str(item) for item in raw_reasons)
    if not gpu_provider_performed and (orchestrator or gpu_report):
        degraded_reasons.append(
            "gpu_not_confirmed:"
            f"performed={gpu_report.get('provider_execution_performed')};"
            f"round_count={gpu_round_count};"
            f"classification={gpu_report.get('classification')};"
            f"passed={gpu_report.get('passed')}"
        )
    if (
        orchestrator.get("npu_lane_mode") in {"skipped", "metadata_only", "degraded"}
        and npu_success_count == 0
        and not npu_micro_support_performed
    ):
        degraded_reasons.append(
            "npu_auditor_not_confirmed:"
            f"audit_count={npu_audit_count};success_count={npu_success_count};"
            f"lane_mode={orchestrator.get('npu_lane_mode')}"
        )
    return {
        "provider_execution_performed": bool(gpu_provider_performed or npu_provider_performed),
        "gpu_provider_execution_performed": gpu_provider_performed,
        "gpu0_peer_support_provider_execution_performed": gpu0_peer_support_performed,
        "gpu0_peer_support_count": safe_int(orchestrator.get("gpu0_peer_support_count")),
        "gpu_round_count": gpu_round_count,
        "gpu_classification": gpu_report.get("classification"),
        "gpu_provider_empty_response": bool(gpu_report.get("provider_empty_response")),
        "npu_provider_execution_performed": npu_provider_performed,
        "npu_audit_count": npu_audit_count,
        "npu_audit_success_count": npu_success_count,
        "npu_micro_support_performed": npu_micro_support_performed,
        "npu_micro_tool_lane_performed": npu_micro_support_performed,
        "npu_micro_support_count": npu_micro_support_count,
        "npu_micro_support_success_count": npu_micro_support_success_count,
        "npu_micro_runtime_tool_execution_count": npu_micro_runtime_tool_execution_count,
        "npu_micro_runtime_tool_live_execution_count": npu_micro_runtime_tool_live_execution_count,
        "npu_lane_mode": orchestrator.get("npu_lane_mode"),
        "provider_degraded_reasons": degraded_reasons,
    }

def extract_declared_runtime_tool_counters(
    gpu_report: dict[str, Any], gpu_npu_sync: dict[str, Any]
) -> dict[str, int]:
    # Extract planner-declared runtime tool counters even when no broker entry exists.
    candidates: list[dict[str, Any]] = []

    performance = safe_dict(safe_dict(gpu_npu_sync.get("performance")).get("gpu"))
    counters = safe_dict(performance.get("runtime_tool_counters"))
    if counters:
        candidates.append(counters)

    sync_metrics = safe_dict(gpu_npu_sync.get("metrics")) or safe_dict(
        gpu_npu_sync.get("sync_metrics")
    )
    if sync_metrics:
        candidates.append(sync_metrics)

    candidates.append(gpu_report)

    def first_int(*names: str) -> int:
        for source in candidates:
            for name in names:
                value = safe_int(source.get(name), -1)
                if value >= 0:
                    return value
        return 0

    request_count = first_int("runtime_tool_request_count", "runtime_tool_provider_request_count")
    execution_count = first_int(
        "runtime_tool_execution_count", "runtime_tool_provider_request_execution_count"
    )
    failed_count = first_int("runtime_tool_failed_count")
    blocked_count = first_int("runtime_tool_blocked_count")
    fallback_request_count = first_int("deterministic_runtime_tool_fallback_request_count")
    fallback_execution_count = first_int("deterministic_runtime_tool_fallback_execution_count")

    return {
        "runtime_tool_request_count": request_count,
        "runtime_tool_execution_count": execution_count,
        "runtime_tool_failed_count": failed_count,
        "runtime_tool_blocked_count": blocked_count,
        "runtime_tool_provider_request_count": first_int("runtime_tool_provider_request_count"),
        "runtime_tool_provider_request_execution_count": first_int(
            "runtime_tool_provider_request_execution_count"
        ),
        "deterministic_runtime_tool_fallback_request_count": fallback_request_count,
        "deterministic_runtime_tool_fallback_execution_count": fallback_execution_count,
        "declared_not_executed_count": max(0, request_count - execution_count),
    }

def build_declared_runtime_tool_counter_entry(
    counters: dict[str, int],
) -> dict[str, Any]:
    # Create a single summary telemetry entry when only aggregate planner counters exist.
    return normalize_tool_entry(
        {
            "caller_ai": "gpu",
            "phase": "gpu_planner_declared_tool_request_counters",
            "round": None,
            "broker_source": "gpu_report_or_gpu_npu_sync_counters",
            "broker_report": "",
            "tool_request_id": "gpu_declared_runtime_tool_request_counter_summary",
            "tool": "declared_runtime_tool_request_summary",
            "reason": "GPU planner reported runtime tool request counters without broker-executed per-tool entries.",
            "requested_args": {},
            "status": "declared_counter_summary_not_broker_executed",
            "executed": False,
            "blocked": False,
            "failed": False,
            "elapsed_seconds": 0.0,
            "declared_counts": counters,
            "result": {
                "summary": "Planner declared runtime tool requests; broker execution count is reported separately.",
                **counters,
            },
        }
    )

def summarize_entries(entries: list[dict[str, Any]]) -> dict[str, Any]:
    by_caller: dict[str, dict[str, Any]] = {}
    by_tool: dict[str, dict[str, Any]] = {}
    by_phase: dict[str, dict[str, Any]] = {}
    total_elapsed = 0.0
    executed_count = 0
    failed_count = 0
    blocked_count = 0
    broker_entry_count = 0
    broker_executed_count = 0
    for entry in entries:
        caller = str(entry.get("caller_ai") or "unknown")
        phase = str(entry.get("phase") or "unknown")
        tool = str(entry.get("tool") or "unknown")
        elapsed = safe_float(entry.get("elapsed_seconds"))
        total_elapsed += elapsed
        result = safe_dict(entry.get("result"))
        executed = (
            entry.get("executed") is True
            or result.get("returncode") == 0
            or result.get("passed") is True
        )
        failed = (
            entry.get("failed") is True
            or result.get("failed") is True
            or result.get("returncode") not in (None, 0)
        )
        blocked = entry.get("blocked") is True
        broker_phase = "broker" in phase
        broker_entry_count += 1 if broker_phase else 0
        broker_executed_count += 1 if broker_phase and executed else 0
        executed_count += 1 if executed else 0
        failed_count += 1 if failed else 0
        blocked_count += 1 if blocked else 0
        for table, key in ((by_caller, caller), (by_tool, tool), (by_phase, phase)):
            item = table.setdefault(
                key,
                {
                    "count": 0,
                    "executed": 0,
                    "failed": 0,
                    "blocked": 0,
                    "elapsed_seconds": 0.0,
                },
            )
            item["count"] += 1
            item["executed"] += 1 if executed else 0
            item["failed"] += 1 if failed else 0
            item["blocked"] += 1 if blocked else 0
            item["elapsed_seconds"] = round(float(item["elapsed_seconds"]) + elapsed, 3)
    return {
        "tool_call_entry_count": len(entries),
        "executed_count": executed_count,
        "failed_count": failed_count,
        "blocked_count": blocked_count,
        "broker_entry_count": broker_entry_count,
        "broker_executed_count": broker_executed_count,
        "total_reported_tool_elapsed_seconds": round(total_elapsed, 3),
        "by_caller_ai": by_caller,
        "by_tool": by_tool,
        "by_phase": by_phase,
    }
