#!/usr/bin/env python3
"""RuntimeState model for the provider runtime heap."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

LANES = (
    "gpu1",
    "gpu0",
    "npu",
    "broker",
    "context_memory",
    "deterministic",
    "telemetry",
    "orchestrator",
)
DEGRADED_STATUSES = {"degraded", "failed"}
KNOWN_STATUSES = {
    "ready",
    "running",
    "degraded",
    "failed",
    "disabled",
    "skipped",
    "unknown",
}


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def normalize_status(value: Any) -> str:
    status = str(value or "").strip().lower()
    return status if status in KNOWN_STATUSES else ""


def degraded_lanes(lane_status: dict[str, str]) -> list[str]:
    return sorted(lane for lane, status in lane_status.items() if status in DEGRADED_STATUSES)


@dataclass
class RuntimeState:
    """Unified state derived from append-only runtime heap events."""

    lane_status: dict[str, str] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    patch_plans: list[dict[str, Any]] = field(default_factory=list)
    validations: list[dict[str, Any]] = field(default_factory=list)
    updated_at: str = ""

    def apply_event(self, event: dict[str, Any]) -> None:
        payload = safe_dict(event.get("payload"))
        event_type = str(event.get("event_type") or "")
        source_lane = str(event.get("source") or "")
        payload_lane = str(payload.get("lane") or "").strip().lower()
        lane = payload_lane if payload_lane in LANES else source_lane
        status = normalize_status(payload.get("status"))
        if lane in LANES and status:
            self.lane_status[lane] = status
            self.updated_at = str(event.get("created_at") or "")
        if event_type in {"lane_evidence", "evidence_response"}:
            self.evidence.append(
                {
                    "created_at": event.get("created_at"),
                    "lane": lane,
                    "status": status or self.lane_status.get(lane, "unknown"),
                    "payload": payload,
                }
            )
        elif event_type == "recommendation":
            self.recommendations.append(payload)
        elif event_type == "patch_plan":
            self.patch_plans.append(payload)
        elif event_type == "validation":
            self.validations.append(payload)

    @classmethod
    def from_events(cls, events: list[dict[str, Any]]) -> RuntimeState:
        state = cls()
        for event in events:
            if event.get("kind") == "provider_runtime_event":
                state.apply_event(event)
        return state

    def as_dict(self) -> dict[str, Any]:
        return {
            "lane_status": dict(sorted(self.lane_status.items())),
            "degraded_lanes": degraded_lanes(self.lane_status),
            "degraded_lane_count": len(degraded_lanes(self.lane_status)),
            "evidence_count": len(self.evidence),
            "recommendation_count": len(self.recommendations),
            "patch_plan_count": len(self.patch_plans),
            "validation_count": len(self.validations),
            "latest_recommendation": self.recommendations[-1] if self.recommendations else {},
            "latest_patch_plan": self.patch_plans[-1] if self.patch_plans else {},
            "latest_validation": self.validations[-1] if self.validations else {},
            "updated_at": self.updated_at,
        }
