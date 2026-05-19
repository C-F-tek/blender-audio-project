from __future__ import annotations

from typing import Any


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Review Warning Policy", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Decision recovered: `{report['decision_recovered']}`")
    lines.append(f"- Warning count: `{report['warning_count']}`")
    lines.append(f"- Input-nonfatal warning count: `{report['input_nonfatal_warning_count']}`")
    lines.append(f"- Fatal report failure count: `{report['fatal_report_failure_count']}`")
    lines.append(f"- Recommendation count: `{report.get('recommendation_count')}`")
    lines.append(f"- Patch plan count: `{report.get('patch_plan_count')}`")
    lines.append("")
    lines.append("## Warning level counts")
    lines.append("")
    for key, value in report.get("warning_level_counts", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Input-nonfatal warnings")
    lines.append("")
    if not report.get("input_nonfatal_warnings"):
        lines.append("- none")
    for item in report.get("input_nonfatal_warnings", []):
        lines.append(f"- `{item.get('level')}` `{item.get('path')}`: {item.get('reason')}")
    if report.get("fatal_report_failures"):
        lines.append("")
        lines.append("## Fatal report failures")
        lines.append("")
        for item in report.get("fatal_report_failures", []):
            lines.append(f"- `{item.get('level')}` `{item.get('path')}`: {item.get('reason')}")
    return "\n".join(lines) + "\n"
