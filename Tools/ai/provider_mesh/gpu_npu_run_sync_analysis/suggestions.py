"""Operational opinions and suggestions for GPU/NPU sync analysis."""

from __future__ import annotations

from typing import Any

from .common import GPU_ELAPSED_FALLBACK_SOURCE, GPU_ROUND_ELAPSED_SOURCE, nested_dict, safe_float, safe_int

def build_suggestions(report: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    avg_gpu = metrics["avg_gpu_round_seconds"]
    avg_npu = metrics["avg_npu_audit_seconds"]
    suggested_every = max(2, min(8, round(avg_npu / avg_gpu))) if avg_gpu > 0 and avg_npu > 0 else 4
    reasoning: list[str] = []

    if metrics["npu_audit_count"] == 0:
        reasoning.append(
            "No NPU audits were observed; first verify provider availability before tuning cadence."
        )
    if metrics["npu_audit_round_coverage"] < 0.35 and metrics["gpu_round_count"] >= 12:
        reasoning.append(
            "NPU audit coverage is low compared with GPU round count; keep checkpoint auditing sampled, not per-round."
        )
    if metrics["gpu_metrics_source"] == GPU_ELAPSED_FALLBACK_SOURCE:
        reasoning.append(
            "GPU per-round elapsed_seconds was unavailable; using total GPU elapsed divided by round count as estimate."
        )
    if metrics["npu_to_gpu_avg_duration_ratio"] > 2.0:
        reasoning.append(
            "Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds."
        )
    if (
        metrics["npu_audit_success_count"] == metrics["npu_audit_count"]
        and metrics["npu_audit_count"] > 0
    ):
        reasoning.append("NPU audits are usable; tune cadence rather than disabling the lane.")
    if (
        report.get("gpu_empty_recommendations_reason") == "repair_attempt_failed"
        or report.get("empty_recommendations_reason") == "repair_attempt_failed"
    ):
        reasoning.append(
            "GPU JSON contract hardening should be tested before increasing GPU token budget further."
        )

    return {
        "recommended_profile": "gpu_npu_balanced_advisory",
        "reasoning": reasoning,
        "parameters": {
            "npu_auditor_every_rounds": suggested_every,
            "max_concurrent_npu_audits": 1,
            "npu_auditor_timeout_seconds": 420,
            "npu_max_context_chars": 8000,
            "npu_max_prompt_chars": 1200,
            "npu_max_new_tokens": 384,
            "npu_final_wait_seconds": 180,
            "gpu_max_new_tokens": 3600,
            "gpu_files_per_round": 8,
            "gpu_max_chars_per_file": 6000,
        },
        "guardrails": {
            "do_not_change_provider_model_settings_first": True,
            "keep_npu_auditor_non_blocking": True,
            "keep_max_concurrent_npu_audits": 1,
            "do_not_promote_npu_advisory": True,
            "do_not_make_openvino_gpu_primary": True,
        },
    }

def has_real_gpu_round_timing(metrics: dict[str, Any]) -> bool:
    return metrics.get("gpu_metrics_source") == GPU_ROUND_ELAPSED_SOURCE

def build_operational_opinions(metrics: dict[str, Any], performance: dict[str, Any]) -> list[str]:
    opinions: list[str] = []
    ratio = safe_float(metrics.get("npu_to_gpu_avg_duration_ratio"))
    coverage = safe_float(metrics.get("npu_audit_round_coverage"))
    runtime = nested_dict(nested_dict(performance, "gpu"), "runtime_tool_counters")
    runtime_failed = safe_int(runtime.get("runtime_tool_failed_count"))
    runtime_blocked = safe_int(runtime.get("runtime_tool_blocked_count"))

    if ratio > 2.0:
        opinions.append(
            "NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round."
        )
    elif ratio > 0:
        opinions.append(
            "GPU/NPU cadence is measurable; tune audit frequency from timing evidence rather than intuition."
        )
    if coverage < 0.5:
        opinions.append(
            "Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed."
        )
    if not has_real_gpu_round_timing(metrics):
        opinions.append(
            "GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present."
        )
    if runtime_failed or runtime_blocked:
        opinions.append(
            "Runtime tool execution had failed or blocked requests; recommendations should reference broker evidence before proposing patches."
        )
    if not opinions:
        opinions.append(
            "GPU/NPU timing is healthy enough for the current advisory workflow; keep the lane report-only."
        )
    return opinions

def build_refactoring_suggestions(
    metrics: dict[str, Any], performance: dict[str, Any]
) -> list[dict[str, Any]]:
    suggestions: list[dict[str, Any]] = []
    runtime = nested_dict(nested_dict(performance, "gpu"), "runtime_tool_counters")
    runtime_failed = safe_int(runtime.get("runtime_tool_failed_count"))
    runtime_blocked = safe_int(runtime.get("runtime_tool_blocked_count"))

    if not has_real_gpu_round_timing(metrics):
        suggestions.append(
            {
                "priority": "high",
                "area": "gpu_runner_timing",
                "recommendation": "Use rounds[*].elapsed_seconds as the primary GPU round timing source.",
                "evidence": f"gpu_metrics_source={metrics.get('gpu_metrics_source')}",
                "guardrail": "report_only_no_provider_setting_change",
            }
        )
    if (
        safe_int(nested_dict(performance, "npu").get("duration_sample_count")) == 0
        and safe_int(metrics.get("npu_audit_count")) > 0
    ):
        suggestions.append(
            {
                "priority": "high",
                "area": "npu_auditor_timing",
                "recommendation": "Persist elapsed_seconds on every NPU audit record instead of relying only on timestamps.",
                "evidence": "NPU audits exist but no duration samples were extracted.",
                "guardrail": "do_not_promote_npu_advisory",
            }
        )
    if safe_float(metrics.get("npu_to_gpu_avg_duration_ratio")) > 2.0:
        suggestions.append(
            {
                "priority": "medium",
                "area": "npu_cadence",
                "recommendation": "Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget.",
                "evidence": f"npu_to_gpu_avg_duration_ratio={metrics.get('npu_to_gpu_avg_duration_ratio')}",
                "guardrail": "keep_max_concurrent_npu_audits_1",
            }
        )
    if runtime_failed or runtime_blocked:
        suggestions.append(
            {
                "priority": "medium",
                "area": "runtime_tool_broker",
                "recommendation": "Surface failed/blocked runtime tool IDs in the next decision-loop patch plan input.",
                "evidence": f"failed={runtime_failed}, blocked={runtime_blocked}",
                "guardrail": "broker_report_only",
            }
        )
    if not suggestions:
        suggestions.append(
            {
                "priority": "low",
                "area": "observability",
                "recommendation": "Keep collecting GPU/NPU performance summaries and compare them across full-toolbox runs.",
                "evidence": "No immediate timing defect detected from available report fields.",
                "guardrail": "no_source_changes_without_evidence",
            }
        )
    return suggestions
