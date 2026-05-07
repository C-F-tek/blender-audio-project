from __future__ import annotations

from typing import Any


def _items(values: Any, limit: int = 12) -> list[Any]:
    return values[:limit] if isinstance(values, list) else []


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Patch Notes Quality Product", ""]
    for key in ("passed", "quality_gate_passed", "classification", "non_blocking", "quality_score"):
        lines.append(f"- {key}: `{report.get(key)}`")
    input_info = report.get("input") if isinstance(report.get("input"), dict) else {}
    lines.append(f"- Input task MD: `{input_info.get('task_markdown')}`")
    lines.append(f"- Task digest: `{input_info.get('task_digest')}`")
    lines.append(f"- Manual review required: `{report.get('manual_review_required')}`")
    telemetry = report.get("telemetry_quality") if isinstance(report.get("telemetry_quality"), dict) else {}
    coverage = report.get("evidence_coverage") if isinstance(report.get("evidence_coverage"), dict) else {}
    lines.append(f"- Telemetry quality score: `{telemetry.get('score')}`")
    lines.append(f"- Evidence coverage score: `{coverage.get('score')}`")
    lines += ["", "## Request", "", str(report.get("normalized_objective") or "")]
    lines += ["", "## Patch Plan Summary", ""]
    summary = report.get("patch_plan_summary") if isinstance(report.get("patch_plan_summary"), dict) else {}
    for key in ("patch_plan_count", "patch_quality_gate_passed", "patch_quality_classification", "average_plan_score"):
        lines.append(f"- {key}: `{summary.get(key)}`")
    lines += ["", "## Generated Patch Notes", ""]
    for note in _items(report.get("patch_notes"), 20):
        lines.append(f"- `{note.get('id')}` `{note.get('area')}` score=`{note.get('quality_score')}` targets=`{note.get('target_files')}`")
        if note.get("summary"):
            lines.append(f"  - {note.get('summary')}")
    lines += ["", "## Telemetry Quality", ""]
    for key, value in (telemetry.get("required_signals") or {}).items():
        lines.append(f"- {key}: `{value}`")
    if telemetry.get("missing_signals"):
        lines.append(f"- Missing signals: `{telemetry.get('missing_signals')}`")
    lines += ["", "## Evidence Coverage", ""]
    for key, value in (coverage.get("coverage") or {}).items():
        lines.append(f"- {key}: `{value}`")
    if report.get("fallback_path_notes"):
        lines += ["", "## Fallback Path Notes", ""]
        for note in _items(report.get("fallback_path_notes"), 20):
            lines.append(f"- `{note.get('reason')}` {note.get('recommended_followup', '')}")
    if report.get("success_cases"):
        lines += ["", "## Success Cases", ""]
        for case in _items(report.get("success_cases"), 20):
            lines.append(f"- `{case.get('case')}` score=`{case.get('score')}` gate=`{case.get('quality_gate_passed')}`")
    if report.get("fallback_cases"):
        lines += ["", "## Structured Fallback Cases", ""]
        for case in _items(report.get("fallback_cases"), 20):
            lines.append(
                f"- `{case.get('fallback_type')}` primary=`{case.get('primary_lane')}` "
                f"fallback=`{case.get('fallback_lane')}` recovered=`{case.get('recovered')}`"
            )
    if report.get("quality_findings"):
        lines += ["", "## Quality Findings", ""]
        for finding in _items(report.get("quality_findings"), 20):
            lines.append(f"- `{finding.get('severity')}` `{finding.get('reason')}`")
    lines += ["", "## Validation Commands", ""]
    for command in _items(report.get("validation_commands"), 20):
        lines.append(f"- `{command}`")
    lines += ["", "## Stop Conditions", ""]
    for condition in _items(report.get("stop_conditions"), 20):
        lines.append(f"- {condition}")
    if report.get("errors"):
        lines += ["", "## Errors", ""]
        lines.extend(f"- {item}" for item in _items(report.get("errors"), 20))
    if report.get("warnings"):
        lines += ["", "## Warnings", ""]
        lines.extend(f"- {item}" for item in _items(report.get("warnings"), 20))
    return "\n".join(lines) + "\n"
