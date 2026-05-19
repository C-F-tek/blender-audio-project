"""Timing summaries for GPU/NPU run sync analysis."""

from __future__ import annotations

from typing import Any

from .common import (
    audit_duration_seconds,
    compact_performance_source,
    elapsed_seconds,
    extract_gpu_round_durations,
    nested_dict,
    percentile,
    rounded_sum,
    runtime_tool_counters,
    safe_float,
    safe_int,
)

def summarize_gpu_timing(
    *,
    report: dict[str, Any],
    gpu_summary: dict[str, Any],
    rounds: list[dict[str, Any]],
    round_count: int,
) -> dict[str, Any]:
    gpu_elapsed = (
        safe_float(report.get("gpu_elapsed_seconds"))
        or safe_float(gpu_summary.get("elapsed_seconds"))
        or safe_float(report.get("elapsed_seconds"))
    )
    round_durations, source = extract_gpu_round_durations(report, rounds, round_count, gpu_elapsed)
    return {
        "elapsed_seconds": round(gpu_elapsed, 3),
        "round_count": round_count,
        "round_duration_source": source,
        "round_duration_sample_count": len(round_durations),
        "avg_round_seconds": (
            round(sum(round_durations) / len(round_durations), 3) if round_durations else 0.0
        ),
        "p50_round_seconds": round(percentile(round_durations, 50), 3),
        "p90_round_seconds": round(percentile(round_durations, 90), 3),
        "max_round_seconds": round(max(round_durations), 3) if round_durations else 0.0,
        "round_durations_total_seconds": rounded_sum(round_durations),
        "provider_empty_response_count": safe_int(report.get("provider_empty_response_count")),
        "schema_repair_retry_attempt_count": safe_int(
            report.get("schema_repair_retry_attempt_count")
        ),
        "schema_repair_retry_accept_count": safe_int(
            report.get("schema_repair_retry_accept_count")
        ),
        "runtime_tool_counters": runtime_tool_counters(report),
        "embedded_performance": compact_performance_source(gpu_summary)
        or compact_performance_source(report),
    }

def summarize_npu_timing(
    report: dict[str, Any], npu_audits: list[dict[str, Any]]
) -> dict[str, Any]:
    durations = [audit_duration_seconds(item) for item in npu_audits]
    durations = [value for value in durations if value > 0]
    status_counts: dict[str, int] = {}
    classification_counts: dict[str, int] = {}
    for item in npu_audits:
        status = str(item.get("status") or "unknown")
        classification = str(item.get("classification") or "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
        classification_counts[classification] = classification_counts.get(classification, 0) + 1

    return {
        "audit_count": len(npu_audits),
        "audit_requested_count": safe_int(report.get("npu_audit_requested_count"))
        + safe_int(report.get("npu_micro_support_count")),
        "audit_success_count": safe_int(report.get("npu_audit_success_count"))
        + safe_int(report.get("npu_micro_support_success_count")),
        "duration_sample_count": len(durations),
        "avg_audit_seconds": (round(sum(durations) / len(durations), 3) if durations else 0.0),
        "p50_audit_seconds": round(percentile(durations, 50), 3),
        "p90_audit_seconds": round(percentile(durations, 90), 3),
        "max_audit_seconds": round(max(durations), 3) if durations else 0.0,
        "audit_durations_total_seconds": rounded_sum(durations),
        "status_counts": status_counts,
        "classification_counts": classification_counts,
        "lane_diagnostics": nested_dict(report, "npu_lane_diagnostics"),
    }

def build_performance_summary(
    *,
    analyzer_started: float,
    report: dict[str, Any],
    gpu_summary: dict[str, Any],
    rounds: list[dict[str, Any]],
    npu_audits: list[dict[str, Any]],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    return {
        "analyzer_elapsed_seconds": elapsed_seconds(analyzer_started),
        "gpu": summarize_gpu_timing(
            report=report,
            gpu_summary=gpu_summary,
            rounds=rounds,
            round_count=metrics["gpu_round_count"],
        ),
        "npu": summarize_npu_timing(report, npu_audits),
        "sync": {
            "npu_to_gpu_avg_duration_ratio": metrics["npu_to_gpu_avg_duration_ratio"],
            "npu_audit_round_coverage": metrics["npu_audit_round_coverage"],
            "gpu_metrics_source": metrics["gpu_metrics_source"],
        },
        "guardrails": {
            "report_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "blender_runtime_execution_performed": False,
            "sqlite_write_performed": False,
        },
    }
