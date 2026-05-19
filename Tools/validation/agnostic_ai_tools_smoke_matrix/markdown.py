"""Markdown renderer for agnostic AI tools smoke matrix."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agnostic AI Tools Smoke Matrix", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Dry run: `{report['dry_run']}`")
    lines.append(f"- Include Ollama live: `{report['include_ollama_live']}`")
    lines.append(f"- Include workflow: `{report['include_workflow']}`")
    lines.append(f"- Step count: `{report['step_count']}`")
    lines.append("")
    for step in report["steps"]:
        lines.append(f"## {step['name']}")
        lines.append("")
        lines.append(f"- OK: `{step['ok']}`")
        lines.append(f"- Return code: `{step['returncode']}`")
        lines.append(f"- Provider live: `{step['provider_live']}`")
        lines.append(f"- Workflow: `{step['workflow']}`")
        lines.append("")
        lines.append("Command:")
        lines.append("")
        lines.append("```text")
        lines.append(" ".join(step["command"]))
        lines.append("```")
        if step["errors"]:
            lines.append("")
            lines.append("Errors:")
            for error in step["errors"]:
                lines.append(f"- {error}")
        if step["outputs"]:
            lines.append("")
            lines.append("Outputs:")
            for output in step["outputs"]:
                lines.append(
                    f"- `{output['path']}` ok=`{output['ok']}` kind=`{output.get('kind')}` passed=`{output.get('passed')}`"
                )
        lines.append("")
    return "\n".join(lines) + "\n"
