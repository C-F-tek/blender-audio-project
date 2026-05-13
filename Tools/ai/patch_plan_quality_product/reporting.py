from __future__ import annotations

from typing import Any


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Patch Plan Quality Product Gate", ""]
    for key in ("passed", "quality_gate_passed", "classification", "non_blocking"):
        lines.append(f"- {key}: `{report[key]}`")
    lines.append(f"- Patch plans: `{report['quality']['patch_plan_count']}`")
    lines.append(f"- Average plan score: `{report['quality']['average_plan_score']}`")
    lines.append(f"- SQLite FTS5 enabled: `{report['quality']['sqlite_fts5_enabled']}`")
    lines.append(f"- FTS total hits: `{report['quality']['fts_total_hit_count']}`")
    lines += ["", "## Fallback path notes", ""]
    if report["fallback_path_notes"]:
        for note in report["fallback_path_notes"]:
            lines.append(
                f"- `{note.get('reason')}` — {note.get('recommended_followup', '')}"
            )
    else:
        lines.append("- None.")
    lines += ["", "## Plan scores", ""]
    for item in report["quality"]["plan_scores"]:
        lines.append(
            f"- `{item['id']}` score=`{item['score']}` targets=`{item['target_files']}`"
        )
    lines += ["", "## Concrete utility", ""]
    for effect in report["tool_utility_proof"]["concrete_effects"]:
        lines.append(f"- {effect}")
    if report["quality_findings"]:
        lines += ["", "## Quality findings"]
        for finding in report["quality_findings"]:
            lines.append(
                f"- `{finding.get('severity')}` `{finding.get('reason')}` {finding.get('plan_id', '')}"
            )
    if report["errors"]:
        lines += ["", "## Fatal errors"]
        lines.extend(f"- {err}" for err in report["errors"])
    if report["warnings"]:
        lines += ["", "## Warnings"]
        lines.extend(f"- {warn}" for warn in report["warnings"])
    return "\n".join(lines) + "\n"
