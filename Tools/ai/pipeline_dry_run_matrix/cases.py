"""Default dry-run matrix cases."""

from __future__ import annotations

from pathlib import Path

from .case_groups_basic import basic_cases
from .case_groups_full import full_surface_cases
from .case_groups_review import review_cases
from .common import MatrixCase, ensure_sample_analysis_json


def default_cases(repo_root: Path | None = None) -> tuple[MatrixCase, ...]:
    agent_state_packet = None
    sample_analysis_json = Path("output/ai_pipeline/dry_run_matrix_inputs/sample_analysis.json")
    if repo_root is not None:
        candidate = (
            repo_root
            / "output"
            / "ai_pipeline"
            / "agent_state"
            / "validate_agent_state_memory_integration_plan.json"
        )
        if candidate.exists():
            agent_state_packet = candidate
        sample_analysis_json = ensure_sample_analysis_json(repo_root)

    cases = (
        basic_cases(sample_analysis_json)
        + review_cases()
        + full_surface_cases(sample_analysis_json)
    )
    if agent_state_packet is not None:
        cases.append(
            MatrixCase(
                name="with_agent_state_packet",
                args=(
                    "--dry-run",
                    "--write-dry-run-report",
                    "--agent-state-packet",
                    str(agent_state_packet),
                ),
                purpose="Verify optional agent state packet metadata without changing planned steps.",
            )
        )
    return tuple(cases)
