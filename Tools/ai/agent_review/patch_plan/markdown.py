"""Markdown renderer for agent review patch plans."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Review Patch Plan", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Apply mode: `{report['apply_mode']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Patch plan count: `{report['decision']['patch_plan_count']}`")
    lines.append(f"- Fallback used: `{report['decision']['fallback_used']}`")
    lines.append(f"- Manual review required: `{report['decision']['manual_review_required']}`")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    for key, value in report.get("inputs", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Patch plans")
    lines.append("")
    if not report.get("patch_plans"):
        lines.append("- none")
    for plan in report.get("patch_plans", []):
        lines.append(f"### {plan.get('id')} — {plan.get('area')}")
        lines.append(f"- Source: `{plan.get('source')}`")
        lines.append(f"- Risk: `{plan.get('risk')}`")
        lines.append(f"- Target files: `{plan.get('target_files')}`")
        lines.append(f"- Rationale: {plan.get('rationale')}")
        lines.append(f"- Strategy: {plan.get('edit_strategy')}")
        lines.append("")
    if report.get("skipped_candidates"):
        lines.append("## Skipped candidates")
        lines.append("")
        for item in report["skipped_candidates"]:
            lines.append(f"- `{item.get('id')}`: {item.get('reason')}")
        lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append(
        "This artifact is a plan only. It contains no replacements and must not be treated as an apply queue."
    )
    return "\n".join(lines) + "\n"
