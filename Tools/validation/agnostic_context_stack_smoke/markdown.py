"""Markdown renderer for agnostic context stack smoke."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agnostic Context Stack Smoke", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Dry run: `{report['dry_run']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Step count: `{report['step_count']}`")
    lines.append("")
    for step in report["steps"]:
        lines.append(f"## {step['name']}")
        lines.append("")
        lines.append(f"- OK: `{step['ok']}`")
        lines.append(f"- Return code: `{step['returncode']}`")
        if step.get("errors"):
            lines.append("")
            lines.append("Errors:")
            for error in step["errors"]:
                lines.append(f"- {error}")
        if step.get("outputs"):
            lines.append("")
            lines.append("Outputs:")
            for item in step["outputs"]:
                lines.append(
                    f"- `{item.get('path')}` ok=`{item.get('ok')}` kind=`{item.get('kind')}` passed=`{item.get('passed')}`"
                )
        lines.append("")
    return "\n".join(lines) + "\n"
