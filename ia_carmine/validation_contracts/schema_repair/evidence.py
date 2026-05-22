"""Runtime-tool evidence extraction for schema repair."""

from __future__ import annotations

from typing import Any

from .common import _compact_tool_result

def collect_recent_runtime_tool_evidence(
    context_reports: list[dict[str, Any]],
    *,
    max_reports: int = 8,
    max_results_per_report: int = 6,
) -> list[dict[str, Any]]:
    """Return compact runtime-tool evidence from broker/feedback contexts."""

    evidence: list[dict[str, Any]] = []
    for item in reversed(context_reports):
        if not isinstance(item, dict):
            continue
        kind = item.get("kind")
        if kind not in {"runtime_tool_feedback_context", "agent_runtime_tool_broker"}:
            continue
        tool_results = item.get("tool_results", [])
        if not isinstance(tool_results, list):
            tool_results = []
        summary = item.get("summary", {}) if isinstance(item.get("summary"), dict) else {}
        evidence.append(
            {
                "kind": kind,
                "path": item.get("path"),
                "source": item.get("source") or summary.get("source"),
                "round": item.get("round") or summary.get("round"),
                "passed": item.get("passed"),
                "summary": {
                    "tool_request_count": summary.get("tool_request_count"),
                    "requested_tool_count": summary.get("requested_tool_count"),
                    "tool_execution_count": summary.get("tool_execution_count"),
                    "blocked_tool_count": summary.get("blocked_tool_count"),
                    "failed_tool_count": summary.get("failed_tool_count"),
                    "deterministic_fallback": summary.get("deterministic_fallback"),
                },
                "tool_results": [
                    _compact_tool_result(result)
                    for result in tool_results[:max_results_per_report]
                    if isinstance(result, dict)
                ],
            }
        )
        if len(evidence) >= max_reports:
            break
    return list(reversed(evidence))

def summarize_round_schema_failures(
    rounds: list[dict[str, Any]], *, max_rounds: int = 10
) -> dict[str, Any]:
    """Summarize provider contract failures from previous rounds."""

    recent = rounds[-max_rounds:]
    reason_counts: dict[str, int] = {}
    schema_error_examples: list[str] = []
    for item in recent:
        if not isinstance(item, dict):
            continue
        reason = str(item.get("empty_recommendations_reason") or "")
        if reason:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
        schema_errors = item.get("schema_errors", [])
        if isinstance(schema_errors, list):
            for error in schema_errors:
                text = str(error)
                if text and text not in schema_error_examples:
                    schema_error_examples.append(text)
                if len(schema_error_examples) >= 8:
                    break
    return {
        "round_count_seen": len(rounds),
        "recent_round_count": len(recent),
        "json_parse_error_count": sum(
            1 for item in recent if isinstance(item, dict) and not item.get("json_ok", True)
        ),
        "schema_mismatch_count": sum(
            1
            for item in recent
            if isinstance(item, dict) and item.get("model_output_schema_mismatch")
        ),
        "context_echo_count": sum(
            1 for item in recent if isinstance(item, dict) and item.get("context_echo_detected")
        ),
        "reason_counts": reason_counts,
        "schema_error_examples": schema_error_examples,
    }
