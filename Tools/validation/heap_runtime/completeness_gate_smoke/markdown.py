"""Markdown renderer for heap runtime completeness smoke reports."""

from __future__ import annotations

from typing import Any


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Runtime Completeness Gate Smoke", "", f"- Passed: `{report.get('passed')}`"]
    for run in report.get("runs") or []:
        lines.extend(["", f"## {run.get('label')}", ""])
        lines.append(f"- Passed: `{run.get('passed')}`")
        lines.append(f"- Run dir: `{run.get('run_dir')}`")
        metrics = run.get("metrics") if isinstance(run.get("metrics"), dict) else {}
        for key in (
            "product_status",
            "completed_requirement_count",
            "required_requirement_count",
            "missing_requirements",
            "budget_exhausted",
            "tool_execution_count",
        ):
            lines.append(f"- {key}: `{metrics.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    counters = (
        report.get("codex_failure_counters")
        if isinstance(report.get("codex_failure_counters"), dict)
        else {}
    )
    if counters:
        lines.extend(["", "## Codex Failure Counter Increments", ""])
        for key in (
            "script_gaming_regression_increment",
            "operator_block_increment",
            "misleading_codex_lie_increment",
            "user_interrupted",
        ):
            lines.append(f"- {key}: `{counters.get(key)}`")
    return "\n".join(lines) + "\n"
