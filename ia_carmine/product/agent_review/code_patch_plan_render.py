"""Markdown rendering for agent-review code patch plans."""

from __future__ import annotations

from typing import Any

from .code_patch_plan_rules import source_kind_for

def render_markdown(report: dict[str, Any]) -> str:
    """Render the code patch-plan report as Markdown."""
    lines = ["# Agent Review Code Patch Plan", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Apply mode: `{report['apply_mode']}`")
    lines.append(f"- Manual review required: `{report['manual_review_required']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Source writes performed: `{report['source_writes_performed']}`")
    lines.append(f"- Patch plan count: `{report['patch_plan_count']}`")
    lines.append(f"- Contract-drift plan count: `{report.get('code_contract_patch_plan_count')}`")
    lines.append(f"- Static-code plan count: `{report.get('static_code_patch_plan_count')}`")
    lines.append("")
    lines.extend(render_inputs(report))
    lines.extend(render_plans(report.get("code_patch_plans", [])))
    lines.extend(render_skipped(report.get("skipped_candidates", [])))
    lines.append("## Guardrail")
    lines.append("")
    lines.append(
        "This artifact is a code patch plan only. It contains no replacements and must not be treated as an apply queue."
    )
    return "\n".join(lines) + "\n"

def render_inputs(report: dict[str, Any]) -> list[str]:
    """Render report input metadata."""
    lines = ["## Inputs", ""]
    for key, value in report.get("inputs", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    return lines

def render_plans(plans: Any) -> list[str]:
    """Render code patch plans."""
    lines = ["## Plans", ""]
    if not plans:
        return lines + ["- none", ""]
    for plan in plans:
        lines.append(f"### `{plan['id']}`")
        lines.append("")
        lines.append(f"- Area: `{plan['area']}`")
        lines.append(f"- Source kind: `{source_kind_for(plan)}`")
        lines.append(f"- Risk: `{plan['risk']}`")
        lines.append(f"- Status: `{plan['status']}`")
        lines.append(f"- Target files: `{', '.join(plan['target_files'])}`")
        lines.append(f"- Rationale: {plan['rationale']}")
        lines.append(f"- Strategy: {plan['edit_strategy']}")
        lines.append("")
    return lines

def render_skipped(skipped: Any) -> list[str]:
    """Render skipped candidate diagnostics."""
    if not skipped:
        return []
    lines = ["## Skipped candidates", ""]
    for item in skipped:
        lines.append(f"- `{item.get('id')}` `{item.get('path', '')}`: {item.get('reason')}")
    lines.append("")
    return lines
