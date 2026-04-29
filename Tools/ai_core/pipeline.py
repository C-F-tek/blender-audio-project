from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol

from .artifact import ArtifactStore


@dataclass
class PipelineContext:
    job: dict[str, Any]
    data: dict[str, Any] = field(default_factory=dict)
    artifacts: ArtifactStore | None = None
    logs: list[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        self.logs.append(message)


@dataclass
class PipelineResult:
    passed: bool
    context: PipelineContext
    started_at: str
    finished_at: str
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "errors": self.errors,
            "logs": self.context.logs,
            "data_keys": sorted(self.context.data.keys()),
            "artifact_manifest": self.context.artifacts.manifest() if self.context.artifacts else None,
        }


class PipelineStage(Protocol):
    name: str

    def run(self, context: PipelineContext) -> PipelineContext:
        ...


class SequentialPipeline:
    """Minimal reusable pipeline runner.

    Stages mutate and return PipelineContext. This keeps the core generic enough
    for Blender, monitoring, code-review, report generation, and future adapters.
    """

    def __init__(self, stages: list[PipelineStage], *, stop_on_error: bool = True) -> None:
        self.stages = stages
        self.stop_on_error = stop_on_error

    def run(self, context: PipelineContext) -> PipelineResult:
        started_at = datetime.now(timezone.utc).isoformat()
        errors: list[str] = []
        for stage in self.stages:
            try:
                context.log(f"stage:start:{stage.name}")
                context = stage.run(context)
                context.log(f"stage:done:{stage.name}")
            except Exception as exc:  # noqa: BLE001 - stage failures must be captured in reports.
                message = f"{stage.name}: {type(exc).__name__}: {exc}"
                errors.append(message)
                context.log(f"stage:error:{message}")
                if self.stop_on_error:
                    break
        finished_at = datetime.now(timezone.utc).isoformat()
        if context.artifacts:
            context.artifacts.write_json("pipeline_result.json", {
                "passed": not errors,
                "started_at": started_at,
                "finished_at": finished_at,
                "errors": errors,
                "logs": context.logs,
                "data_keys": sorted(context.data.keys()),
            })
            context.artifacts.write_manifest()
        return PipelineResult(passed=not errors, context=context, started_at=started_at, finished_at=finished_at, errors=errors)
