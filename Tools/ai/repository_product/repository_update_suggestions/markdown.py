"""Markdown renderer for repository update suggestion packets."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Post-Validation AI Work Packet", ""]
    lines.append(f"- Generated at: `{report['generated_at']}`")
    lines.append(f"- Repo: `{report['repo_root']}`")
    lines.append(f"- Profile: `{report['profile']}`")
    lines.append(f"- Ollama used: `{report['ollama']['used']}`")
    lines.append(f"- Packet manifest: `{report['packet_manifest']['path']}`")
    lines.append("")
    routing = report["context"].get("advisory_context_routing", {})
    if isinstance(routing, dict):
        lines.append("## Advisory context routing")
        lines.append("")
        lines.append(f"- Enforced: `{routing.get('enforced')}`")
        lines.append(
            f"- Provider execution performed: `{routing.get('provider_execution_performed')}`"
        )
        lines.append(
            f"- Advisory lanes: `{', '.join(routing.get('advisory_lanes') or []) or 'none'}`"
        )
        lines.append(
            f"- Excluded advisory lanes: `{', '.join(routing.get('excluded_advisory_lanes') or []) or 'none'}`"
        )
        lines.append("")
    lines.append("## Deterministic suggestions")
    lines.append("")
    for item in report["suggestions"]:
        lines.append(f"### {item['priority']} â€” {item['title']}")
        lines.append("")
        lines.append(f"- Area: `{item['area']}`")
        lines.append(f"- Details: {item['details']}")
        lines.append("")
    if report["ollama"].get("text"):
        lines.append("## Local Ollama draft")
        lines.append("")
        lines.append(report["ollama"]["text"].strip())
        lines.append("")
    lines.append("## Inputs")
    lines.append("")
    lines.append("### Trusted context files")
    for path in report["context"]["context_files"]:
        lines.append(f"- `{path}`")
    lines.append("")
    excluded = (
        report["context"].get("advisory_context_routing", {}).get("excluded_context_files", [])
    )
    if excluded:
        lines.append("### Excluded advisory context files")
        for item in excluded:
            if isinstance(item, dict):
                lines.append(
                    f"- `{item.get('path')}` â€” lane `{item.get('lane')}`, reason `{item.get('reason')}`"
                )
        lines.append("")
    lines.append("### Report files")
    for path in report["context"]["report_files"]:
        lines.append(f"- `{path}`")
    lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    lines.extend(
        [
            "- Advisory only: do not auto-apply edits from this packet.",
            "- Output/input paths are configurable; defaults are not part of the architecture boundary.",
            "- Validate locally before committing generated indexes.",
            "- Keep provider execution changes in a separate explicitly scoped milestone.",
        ]
    )
    return "\n".join(lines) + "\n"
