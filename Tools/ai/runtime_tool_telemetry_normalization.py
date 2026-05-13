#!/usr/bin/env python3
"""Status and timing normalization for runtime tool telemetry."""

from __future__ import annotations

from typing import Any


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", "."))
        except ValueError:
            return default
    return default


def infer_tool_status(entry: dict[str, Any]) -> str:
    status = str(entry.get("status") or entry.get("state") or "").strip()
    if status:
        return status

    result = safe_dict(entry.get("result"))
    returncode = entry.get("returncode", result.get("returncode"))
    if entry.get("blocked") is True:
        return "blocked"
    if entry.get("failed") is True:
        return "failed"
    if entry.get("executed") is True:
        return "executed_ok" if returncode in (None, 0) else "executed_failed"
    if entry.get("executed") is False:
        return "declared_not_executed"
    if result.get("passed") is True:
        return "reported_passed"
    if result.get("passed") is False:
        return "reported_failed"
    return "unknown_unclassified"


def normalize_tool_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(entry)
    normalized["status"] = infer_tool_status(normalized)
    elapsed = safe_float(normalized.get("elapsed_seconds"))
    normalized["elapsed_seconds"] = round(max(0.0, elapsed), 3)
    result = safe_dict(normalized.get("result"))
    if "returncode" not in normalized and result.get("returncode") is not None:
        normalized["returncode"] = result.get("returncode")
    if (
        normalized.get("executed") is False
        and normalized["status"] == "declared_not_executed"
    ):
        normalized.setdefault(
            "declared_not_executed_reason",
            "planner_declared_request_without_matching_broker_result",
        )
    return normalized


def status_quality(entries: list[dict[str, Any]]) -> dict[str, Any]:
    status_missing = [
        item for item in entries if not str(item.get("status") or "").strip()
    ]
    elapsed_missing = [
        item
        for item in entries
        if item.get("executed") is True
        and safe_float(item.get("elapsed_seconds")) <= 0.0
    ]
    return {
        "status_normalized": not status_missing,
        "status_missing_count": len(status_missing),
        "executed_elapsed_missing_count": len(elapsed_missing),
        "elapsed_seconds_measurement": "broker_reported_or_timestamp_derived",
    }
