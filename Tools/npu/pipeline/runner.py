from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PipelineStagePlan:
    """A deterministic description of a future NPU pipeline stage."""

    name: str
    enabled: bool
    reason: str
    planned_outputs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "enabled": self.enabled,
            "reason": self.reason,
            "planned_outputs": list(self.planned_outputs),
        }


def build_default_stage_plan(*, include_provider_stages: bool = False) -> list[PipelineStagePlan]:
    """Build a deterministic stage plan without executing any stage."""

    stages = [
        PipelineStagePlan(
            name="config_resolution",
            enabled=True,
            reason="Resolve paths and deterministic defaults.",
        ),
        PipelineStagePlan(
            name="context_bundle",
            enabled=True,
            reason="Build bounded context payloads.",
        ),
        PipelineStagePlan(
            name="contract_validation",
            enabled=True,
            reason="Validate generated JSON contracts and artifact destinations.",
        ),
        PipelineStagePlan(
            name="artifact_write_review",
            enabled=True,
            reason="Plan generated artifact writes under allowed prefixes.",
        ),
    ]
    stages.append(
        PipelineStagePlan(
            name="provider_execution",
            enabled=include_provider_stages,
            reason="Provider calls remain disabled until runtime migration is explicitly validated.",
        )
    )
    return stages


def stage_plan_report(stages: list[PipelineStagePlan]) -> dict[str, Any]:
    """Return a compact report for a deterministic stage plan."""

    payload = [stage.to_dict() for stage in stages]
    return {
        "schema_version": 1,
        "kind": "npu_pipeline_stage_plan",
        "stage_count": len(payload),
        "enabled_stage_count": sum(1 for stage in stages if stage.enabled),
        "stages": payload,
    }
