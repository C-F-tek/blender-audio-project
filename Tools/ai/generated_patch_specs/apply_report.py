"""Markdown reporting for generated patch-spec application."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Generated Patch Specs Review PR Apply",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Apply requested: `{report.get('apply_requested')}`",
        f"- Patch application performed: `{report.get('patch_application_performed')}`",
        f"- Operation count: `{report.get('operation_count')}`",
        f"- Changed count: `{report.get('changed_count')}`",
        f"- Applied count: `{report.get('applied_count')}`",
        f"- Manual review required: `{report.get('manual_review_required')}`",
        "",
        "## Results",
        "",
    ]
    for item in report.get("results") or []:
        lines.append(
            f"- `{item.get('path')}` op=`{item.get('operation')}` changed=`{item.get('changed')}` applied=`{item.get('applied')}` ok=`{item.get('ok')}`"
        )
    if report.get("manual_review_items"):
        lines.extend(["", "## Manual review items", ""])
        for item in report["manual_review_items"][:50]:
            lines.append(
                f"- `{item.get('id')}` {item.get('reason')} targets=`{item.get('target_files')}`"
            )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"
