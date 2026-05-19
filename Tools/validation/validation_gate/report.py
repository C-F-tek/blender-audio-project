"""Report rendering for the unified validation gate."""

from __future__ import annotations

from typing import Any


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Unified Validation Gate", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Dry run: `{report['dry_run']}`")
    lines.append(f"- Step count: `{report['step_count']}`")
    lines.append("")
    for step in report["steps"]:
        lines.append(f"## {step['name']}")
        lines.append("")
        lines.append(f"- OK: `{step['ok']}`")
        lines.append(f"- Return code: `{step['returncode']}`")
        lines.append(f"- Heavy: `{step['heavy']}`")
        lines.append(f"- Provider live: `{step['provider_live']}`")
        if step["errors"]:
            lines.append("")
            lines.append("Errors:")
            lines.extend(f"- {error}" for error in step["errors"])
        if step["outputs"]:
            lines.append("")
            lines.append("Outputs:")
            for output in step["outputs"]:
                lines.append(
                    f"- `{output['path']}` exists=`{output['exists']}` size=`{output['size_bytes']}`"
                )
        lines.append("")
    return "\n".join(lines) + "\n"
