from __future__ import annotations

from typing import Any


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _bool_at(data: dict[str, Any], *path: str) -> bool:
    current: Any = data
    for key in path:
        current = safe_dict(current).get(key)
    return bool(current)


def build_telemetry_quality(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    runtime_usage = safe_dict(loaded.get("runtime_usage"))
    capability = safe_dict(loaded.get("runtime_capability"))
    run_summary = safe_dict(loaded.get("full_toolbox_telemetry"))
    provider_evidence = safe_dict(run_summary.get("provider_evidence") or runtime_usage.get("provider_evidence"))
    usage_summary = safe_dict(runtime_usage.get("summary"))
    tool_calls = safe_list(runtime_usage.get("tool_calls"))
    required = {
        "runtime_usage_seen": bool(runtime_usage),
        "runtime_capability_seen": bool(capability),
        "tool_call_entries_seen": bool(tool_calls or usage_summary.get("tool_call_entry_count")),
        "provider_execution_observed": bool(
            provider_evidence.get("provider_execution_performed")
            or runtime_usage.get("provider_execution_performed")
            or run_summary.get("provider_execution_performed")
        ),
        "gpu1_primary_observed": bool(
            provider_evidence.get("gpu_provider_execution_performed")
            or _bool_at(run_summary, "guardrails", "gpu_provider_execution_performed")
        ),
        "gpu0_companion_observed": bool(
            provider_evidence.get("gpu0_peer_support_provider_execution_performed")
            or _bool_at(run_summary, "guardrails", "gpu0_peer_provider_execution_performed")
        ),
        "npu_micro_or_tool_observed": bool(
            provider_evidence.get("npu_provider_execution_performed")
            or provider_evidence.get("npu_micro_tool_lane_performed")
            or _bool_at(run_summary, "guardrails", "npu_micro_non_blocking")
        ),
    }
    missing = [key for key, ok in required.items() if not ok]
    score = round(100.0 * (len(required) - len(missing)) / len(required), 2)
    return {
        "score": score,
        "required_signals": required,
        "missing_signals": missing,
        "tool_call_entry_count": usage_summary.get("tool_call_entry_count") or len(tool_calls),
        "executed_count": usage_summary.get("executed_count"),
        "failed_count": usage_summary.get("failed_count"),
        "blocked_count": usage_summary.get("blocked_count"),
        "provider_evidence": provider_evidence,
    }


def build_evidence_coverage(loaded: dict[str, dict[str, Any]], input_status: dict[str, str]) -> dict[str, Any]:
    expected = [
        "patch_quality",
        "decision_loop",
        "runtime_usage",
        "runtime_capability",
        "repository_consistency",
        "memory_bundle",
        "full_toolbox_telemetry",
        "github_evidence_bundle",
    ]
    coverage = {key: bool(loaded.get(key)) for key in expected}
    missing = [key for key in expected if not coverage[key]]
    score = round(100.0 * (len(expected) - len(missing)) / len(expected), 2)
    return {
        "score": score,
        "coverage": coverage,
        "missing_evidence": missing,
        "input_status": input_status,
    }
