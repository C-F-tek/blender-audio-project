"""Markdown reporting for generated patch-spec application."""

from __future__ import annotations

from typing import Any

from ia_carmine._shared.report_markdown import append_errors_and_warnings, report_header

def render_markdown(report: dict[str, Any]) -> str:
    lines = report_header(
        "Generated Patch Specs Review PR Apply",
        [
            ("Passed", report.get("passed")),
            ("Apply requested", report.get("apply_requested")),
            ("Patch application performed", report.get("patch_application_performed")),
            ("Operation count", report.get("operation_count")),
            ("Changed count", report.get("changed_count")),
            ("Applied count", report.get("applied_count")),
            ("Manual review required", report.get("manual_review_required")),
        ],
    )
    lines.extend(["", "## Results", ""])
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
    append_errors_and_warnings(lines, report)
    return "\n".join(lines) + "\n"
