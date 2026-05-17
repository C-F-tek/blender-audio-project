"""Markdown renderer for agent review patch-plan full validation."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Review Patch Plan Full Validation", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Evidence bundle JSON: `{report['evidence_bundle']['json']}`")
    lines.append(f"- Evidence bundle Markdown: `{report['evidence_bundle']['markdown']}`")
    lines.append("")
    lines.append("## Commands")
    lines.append("")
    for step in report.get("steps", []):
        lines.append(f"### {step['name']}")
        lines.append(f"- Return code: `{step['returncode']}`")
        lines.append(f"- OK: `{step['ok']}`")
        if step.get("error"):
            lines.append(f"- Error: `{step['error']}`")
        lines.append("")
    lines.append("## Artifact summary")
    lines.append("")
    for name, artifact in report.get("artifacts", {}).items():
        lines.append(f"- `{name}`: `{artifact}`")
    lines.append("")
    if report.get("errors"):
        lines.append("## Errors")
        lines.append("")
        for error in report["errors"]:
            lines.append(f"- {error}")
        lines.append("")
    if report.get("warnings"):
        lines.append("## Warnings")
        lines.append("")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
        lines.append("")
    return "\n".join(lines) + "\n"
