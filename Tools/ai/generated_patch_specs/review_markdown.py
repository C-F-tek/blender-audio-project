"""Markdown rendering for reviewed patch specs."""

from __future__ import annotations

from typing import Any

def render_manifest_markdown(manifest: dict[str, Any]) -> str:
    lines = ["# Reviewed Patch Spec", ""]
    lines.append(f"- Generated at: `{manifest['generated_at']}`")
    lines.append(f"- Source draft: `{manifest['source_draft_spec']}`")
    lines.append(f"- Replacement plan: `{manifest['source_replacement_plan']}`")
    lines.append(f"- Passed: `{manifest['passed']}`")
    lines.append(f"- Provider execution performed: `{manifest['provider_execution_performed']}`")
    lines.append("")
    lines.append("## Specs")
    lines.append("")
    for item in manifest["specs"]:
        lines.append(
            f"- `{item['path']}`: dry-run `{item['dry_run_passed']}`, "
            f"{item['operation_count']} operation(s)"
        )
    lines.append("")
    if manifest["errors"]:
        lines.append("## Errors")
        lines.append("")
        for error in manifest["errors"]:
            lines.append(f"- {error}")
        lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append("This reviewed spec has been dry-run only. It is not queued and was not applied.")
    return "\n".join(lines) + "\n"
