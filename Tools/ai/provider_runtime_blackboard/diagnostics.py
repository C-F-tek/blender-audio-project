"""Diagnostics helpers for provider runtime blackboard."""

from __future__ import annotations

from typing import Any

from tools.ai.provider_runtime_state import normalize_status

from .common import normalize_lane, safe_dict
from .heap import ProviderRuntimeHeap

def record_lane_diagnostic(
    heap: ProviderRuntimeHeap,
    lane: str,
    status: str,
    message: str,
    details: dict[str, Any] | None = None,
    *,
    round_id: int | None = None,
    target: str | None = "orchestrator",
    correlation_id: str | None = None,
) -> dict[str, Any]:
    """Record one standardized lane diagnostic in the shared runtime heap."""
    normalized_lane = normalize_lane(lane)
    normalized_status = normalize_status(status) or "unknown"
    payload = {
        "lane": normalized_lane,
        "status": normalized_status,
        "message": str(message or ""),
        "details": safe_dict(details or {}),
    }
    return heap.add_event(
        "provider_state",
        payload,
        normalized_lane,
        round_id=round_id,
        target=target,
        correlation_id=correlation_id,
    )
