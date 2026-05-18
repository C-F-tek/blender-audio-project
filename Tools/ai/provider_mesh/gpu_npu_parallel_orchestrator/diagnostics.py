from __future__ import annotations

from .common import *  # noqa: F403

def gpu_direct_runtime_tool_counters(gpu_report: dict[str, Any]) -> dict[str, Any]:
    """Extract direct GPU-runner runtime-tool counters without bootstrap double counting."""

    bootstrap_request_count = safe_int(gpu_report.get("runtime_tool_bootstrap_request_count"))
    bootstrap_execution_count = safe_int(gpu_report.get("runtime_tool_bootstrap_execution_count"))
    bootstrap_failed_count = safe_int(gpu_report.get("runtime_tool_bootstrap_failed_count"))
    bootstrap_blocked_count = safe_int(gpu_report.get("runtime_tool_bootstrap_blocked_count"))
    direct_request_count = max(
        0,
        safe_int(gpu_report.get("runtime_tool_request_count")) - bootstrap_request_count,
    )
    direct_execution_count = max(
        0,
        safe_int(gpu_report.get("runtime_tool_execution_count")) - bootstrap_execution_count,
    )
    direct_failed_count = max(
        0,
        safe_int(gpu_report.get("runtime_tool_failed_count")) - bootstrap_failed_count,
    )
    direct_blocked_count = max(
        0,
        safe_int(gpu_report.get("runtime_tool_blocked_count")) - bootstrap_blocked_count,
    )
    return {
        "gpu_direct_runtime_tool_request_count": direct_request_count,
        "gpu_direct_runtime_tool_execution_count": direct_execution_count,
        "gpu_direct_runtime_tool_failed_count": direct_failed_count,
        "gpu_direct_runtime_tool_blocked_count": direct_blocked_count,
        "gpu_direct_runtime_tool_provider_request_count": safe_int(
            gpu_report.get("runtime_tool_provider_request_count")
        ),
        "gpu_direct_runtime_tool_provider_request_execution_count": safe_int(
            gpu_report.get("runtime_tool_provider_request_execution_count")
        ),
        "gpu_direct_runtime_tool_feedback_context_report_count": safe_int(
            gpu_report.get("runtime_tool_feedback_context_report_count")
        ),
        "gpu_direct_deterministic_runtime_tool_fallback_request_count": safe_int(
            gpu_report.get("deterministic_runtime_tool_fallback_request_count")
        ),
        "gpu_direct_deterministic_runtime_tool_fallback_execution_count": safe_int(
            gpu_report.get("deterministic_runtime_tool_fallback_execution_count")
        ),
    }

def npu_lane_diagnostics(
    args: argparse.Namespace, audit_records: list[dict[str, Any]]
) -> dict[str, Any]:
    """Classify the NPU audit lane without making it blocking."""

    provider_requested = bool(getattr(args, "run_npu_auditor_provider", False))
    threshold = float(getattr(args, "npu_slow_audit_threshold_seconds", 60) or 60)
    base_every = max(1, safe_int(getattr(args, "npu_auditor_every_rounds", 1), 1))
    slow_every = max(
        base_every,
        safe_int(
            getattr(args, "npu_slow_auditor_every_rounds", max(base_every, 4)),
            max(base_every, 4),
        ),
    )
    elapsed_values = [
        value
        for value in (audit_elapsed_seconds(item) for item in audit_records)
        if value is not None
    ]
    finished_count = sum(1 for item in audit_records if item.get("status") == "finished")
    running_count = sum(1 for item in audit_records if item.get("status") == "running")
    success_count = sum(
        1
        for item in audit_records
        if item.get("provider_execution_succeeded") is True
        or item.get("classification") == "usable_audit_text"
    )
    failed_count = sum(
        1
        for item in audit_records
        if item.get("status") == "finished" and item.get("returncode") not in (None, 0)
    )
    avg_elapsed = round(sum(elapsed_values) / len(elapsed_values), 3) if elapsed_values else 0.0
    max_elapsed = round(max(elapsed_values), 3) if elapsed_values else 0.0

    if not provider_requested:
        mode = "metadata_only"
    elif not audit_records:
        mode = "skipped"
    elif running_count:
        mode = "slow"
    elif max_elapsed >= threshold:
        mode = "slow"
    elif failed_count and success_count == 0:
        mode = "degraded"
    else:
        mode = "active"

    effective_every = slow_every if mode in {"slow", "degraded"} else base_every
    return {
        "mode": mode,
        "provider_requested": provider_requested,
        "audit_count": len(audit_records),
        "finished_count": finished_count,
        "running_count": running_count,
        "success_count": success_count,
        "failed_count": failed_count,
        "avg_elapsed_seconds": avg_elapsed,
        "max_elapsed_seconds": max_elapsed,
        "slow_threshold_seconds": threshold,
        "base_auditor_every_rounds": base_every,
        "slow_auditor_every_rounds": slow_every,
        "effective_auditor_every_rounds": effective_every,
        "non_blocking": True,
    }

def effective_npu_auditor_every_rounds(
    args: argparse.Namespace, audit_records: list[dict[str, Any]]
) -> int:
    return safe_int(
        npu_lane_diagnostics(args, audit_records).get("effective_auditor_every_rounds"),
        max(1, safe_int(getattr(args, "npu_auditor_every_rounds", 1), 1)),
    )

def apply_orchestrator_direct_gpu_and_lane_diagnostics(
    report: dict[str, Any],
    *,
    args: argparse.Namespace,
    gpu_report: dict[str, Any],
    audit_records: list[dict[str, Any]],
) -> None:
    """Propagate direct GPU-runner counters and adaptive lane state into the orchestrator report."""

    gpu_direct = gpu_direct_runtime_tool_counters(gpu_report)
    npu_lane = npu_lane_diagnostics(args, audit_records)
    gpu_lane = {
        "mode": "primary_fast_loop",
        "provider_execution_performed": bool(gpu_report.get("provider_execution_performed")),
        "round_count": safe_int(gpu_report.get("round_count")),
        "recommendation_count": safe_int(gpu_report.get("recommendation_count")),
        "empty_recommendations_reason": gpu_report.get("empty_recommendations_reason", ""),
        "direct_runtime_tool_execution_count": gpu_direct[
            "gpu_direct_runtime_tool_execution_count"
        ],
        "direct_provider_request_execution_count": gpu_direct[
            "gpu_direct_runtime_tool_provider_request_execution_count"
        ],
        "feedback_context_report_count": gpu_direct[
            "gpu_direct_runtime_tool_feedback_context_report_count"
        ],
    }

    report.update(gpu_direct)
    report["gpu_lane_mode"] = gpu_lane["mode"]
    report["gpu_lane"] = gpu_lane
    report["npu_lane_mode"] = npu_lane["mode"]
    report["npu_lane"] = npu_lane

    report["runtime_tool_provider_request_count"] = max(
        safe_int(report.get("runtime_tool_provider_request_count")),
        gpu_direct["gpu_direct_runtime_tool_provider_request_count"]
        + safe_int(report.get("gpu_orchestrated_runtime_tool_request_count"))
        + safe_int(report.get("npu_runtime_tool_request_count")),
    )
    report["runtime_tool_provider_request_execution_count"] = max(
        safe_int(report.get("runtime_tool_provider_request_execution_count")),
        gpu_direct["gpu_direct_runtime_tool_provider_request_execution_count"]
        + safe_int(report.get("gpu_orchestrated_runtime_tool_execution_count"))
        + safe_int(report.get("npu_runtime_tool_execution_count")),
    )
    report["deterministic_runtime_tool_fallback_execution_count"] = max(
        safe_int(report.get("deterministic_runtime_tool_fallback_execution_count")),
        gpu_direct["gpu_direct_deterministic_runtime_tool_fallback_execution_count"],
    )
    report["runtime_tool_feedback_context_report_count"] = max(
        safe_int(report.get("runtime_tool_feedback_context_report_count")),
        gpu_direct["gpu_direct_runtime_tool_feedback_context_report_count"],
    )

    gpu_summary = report.get("gpu_summary")
    if isinstance(gpu_summary, dict):
        gpu_summary.update(gpu_direct)
        gpu_summary["gpu_lane"] = gpu_lane
        gpu_summary["runtime_tool_feedback_context_report_count"] = report[
            "runtime_tool_feedback_context_report_count"
        ]

    decision = report.get("decision")
    if isinstance(decision, dict):
        decision["gpu_lane_mode"] = gpu_lane["mode"]
        decision["npu_lane_mode"] = npu_lane["mode"]
        decision["gpu_direct_runtime_tool_provider_request_execution_count"] = gpu_direct[
            "gpu_direct_runtime_tool_provider_request_execution_count"
        ]
        decision["runtime_tool_feedback_context_report_count"] = report[
            "runtime_tool_feedback_context_report_count"
        ]
        decision["npu_effective_auditor_every_rounds"] = npu_lane["effective_auditor_every_rounds"]

def build_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent GPU/NPU Parallel Orchestrator", ""]
    for key in [
        "passed",
        "provider_execution_performed",
        "patch_application_performed",
        "gpu_returncode",
        "elapsed_seconds",
        "gpu0_peer_support_count",
        "gpu0_peer_support_success_count",
        "gpu0_peer_support_overlap_count",
        "gpu0_peer_support_provider_execution_performed",
        "npu_micro_support_count",
        "npu_micro_support_success_count",
        "npu_micro_support_overlap_count",
        "npu_micro_support_provider_execution_performed",
        "npu_micro_support_tool_request_count",
        "npu_micro_runtime_tool_execution_count",
        "npu_audit_count",
        "npu_audit_success_count",
        "npu_tool_context_seen_count",
        "npu_tool_request_count",
        "npu_runtime_tool_request_count",
        "npu_runtime_tool_execution_count",
        "npu_runtime_tool_failed_count",
        "npu_runtime_tool_blocked_count",
        "npu_runtime_tool_result_count",
        "gpu_recommendation_count",
        "gpu_empty_recommendations_reason",
        "gpu_evidence_ready_for_manual_patch_count",
        "runtime_tool_broker_enabled",
        "runtime_tool_request_count",
        "runtime_tool_execution_count",
        "runtime_tool_failed_count",
        "runtime_tool_blocked_count",
        "runtime_tool_result_count",
    ]:
        lines.append(f"- `{key}`: `{report.get(key)}`")
    lines.append("")
    lines.append("## Decision")
    for key, value in report.get("decision", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## NPU Audits")
    for audit in report.get("npu_audits", []):
        lines.append(
            f"- round `{audit.get('round')}` status=`{audit.get('status')}` class=`{audit.get('classification')}` success=`{audit.get('provider_execution_succeeded')}`"
        )
    lines.append("")
    lines.append("## GPU0 Peer Support")
    for item in report.get("gpu0_peer_supports", []):
        lines.append(
            f"- round `{item.get('round')}` status=`{item.get('status')}` provider=`{item.get('provider_execution_performed')}` overlap=`{item.get('launched_while_gpu1_active')}`"
        )
    lines.append("")
    lines.append("## NPU Micro Support")
    for item in report.get("npu_micro_supports", []):
        lines.append(
            f"- round `{item.get('round')}` status=`{item.get('status')}` class=`{item.get('classification')}` provider=`{item.get('provider_execution_performed')}` overlap=`{item.get('launched_while_gpu1_active')}` tools=`{item.get('npu_tool_request_count')}`"
        )
    return "\n".join(lines) + "\n"
