"""Machine-readable status for the modular AI artifact pipeline refactor."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class PipelineRefactorStatus:
    """Current state marker for AI agents and local validation tools."""

    status: str
    phase: str
    external_behavior: str
    local_validation_required: bool
    schema_version: int
    entrypoint: str
    modules: tuple[str, ...]
    validation_commands: tuple[str, ...]
    notes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


MODULAR_PIPELINE_STATUS = PipelineRefactorStatus(
    status="modular_schedule_complete_pending_local_validation",
    phase="pipeline_modularization",
    external_behavior="intended_compatible_with_schema_v6_cli_and_report",
    local_validation_required=True,
    schema_version=6,
    entrypoint="Tools/ai/pipeline/artifact_runner/cli.py",
    modules=(
        "Tools/ai/pipeline/defaults.py",
        "Tools/ai/pipeline/models.py",
        "Tools/ai/pipeline/runner.py",
        "Tools/ai/pipeline/compat.py",
        "Tools/ai/pipeline/artifact_contracts.py",
        "Tools/ai/pipeline/cli.py",
        "Tools/ai/pipeline/preflight.py",
        "Tools/ai/pipeline/steps.py",
        "Tools/ai/pipeline/scheduler.py",
        "Tools/ai/pipeline/orchestrator.py",
        "Tools/ai/pipeline/schema_report.py",
        "Tools/ai/pipeline/markdown_report.py",
        "Tools/ai/pipeline/guardrail_models.py",
        "Tools/ai/pipeline/remediation.py",
        "Tools/ai/pipeline/refactor_status.py",
        "Tools/ai/pipeline/artifact_runner/cli.py",
        "Tools/ai/pipeline/dry_run_matrix/cli.py",
        "Tools/ai/pipeline/dry_run_matrix/evidence_cli.py",
    ),
    validation_commands=(
        "python -m Tools.validation check_python_syntax --repo-root .",
        "python -m Tools.validation check_ai_pipeline_modules --repo-root . --output .\\output\\validation\\ai_pipeline_modules.json",
        "python -m Tools.validation check_refactor_status_consistency --repo-root . --output .\\output\\validation\\refactor_status_consistency.json",
        "python -m Tools.validation check_docs_links --repo-root . --output .\\output\\validation\\docs_links.json",
        "python -m Tools.ai pipeline_dry_run_matrix --repo-root . --continue-on-error",
        "python -m Tools.validation check_package_structure --repo-root .",
        "python -m Tools.validation check_json_artifacts --repo-root .",
    ),
    notes=(
        "The entrypoint is intentionally thin.",
        "Do not treat the modular split as incomplete unless local validation fails.",
        "Regenerate AI/NPU indexes after local validation.",
        "Avoid changing Blender runtime packages as part of this pipeline refactor.",
    ),
)


def get_pipeline_refactor_status() -> dict[str, Any]:
    """Return the current machine-readable pipeline refactor status."""
    return MODULAR_PIPELINE_STATUS.to_dict()
