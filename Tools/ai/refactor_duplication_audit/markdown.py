"""Markdown rendering for refactor duplication audits."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Refactor Duplication Audit", ""]
    for key in (
        "stamp",
        "passed",
        "provider_execution_performed",
        "patch_application_performed",
        "sqlite_write_performed",
        "persistent_memory_write_performed",
        "python_file_count",
        "function_count",
        "duplication_candidate_count",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    lines.append("")
    lines.append("## Refactor verification")
    lines.append("")
    for key, value in report.get("refactor_verification", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Duplication candidates")
    lines.append("")
    for item in report.get("duplication_candidates", []):
        lines.append(f"### `{item.get('candidate_id')}`")
        lines.append("")
        lines.append(f"- repeated_logic: {item.get('repeated_logic')}")
        lines.append(f"- recommendation_type: `{item.get('recommendation_type')}`")
        lines.append(f"- risk: `{item.get('risk')}`")
        lines.append(
            f"- preferred helper/module: {item.get('preferred_existing_helper_or_module')}"
        )
        lines.append(f"- occurrence_count: `{item.get('occurrence_count')}`")
        lines.append("- files:")
        for value in item.get("files_involved", [])[:10]:
            lines.append(f"  - `{value}`")
        lines.append("")
    lines.append("## Manual-review patch-plan candidates")
    lines.append("")
    if report.get("manual_review_patch_plan_candidates"):
        for item in report.get("manual_review_patch_plan_candidates", []):
            lines.append(
                f"- `{item.get('candidate_id')}`: {item.get('title')} ({item.get('recommendation_type')})"
            )
    else:
        lines.append("- No ready manual-review patch-plan candidate was selected.")
    lines.append("")
    lines.append("## Advisory-only findings")
    lines.append("")
    for value in report.get("advisory_only_findings", []):
        lines.append(f"- {value}")
    lines.append("")
    if report.get("warnings"):
        lines.append("## Warnings")
        lines.append("")
        for value in report.get("warnings", []):
            lines.append(f"- {value}")
    if report.get("errors"):
        lines.append("")
        lines.append("## Errors")
        lines.append("")
        for value in report.get("errors", []):
            lines.append(f"- {value}")
    return "\n".join(lines) + "\n"
