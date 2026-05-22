from __future__ import annotations

from typing import Any


def render_markdown(evidence: dict[str, Any]) -> str:
    """Render a compact Markdown companion for the evidence bundle."""
    matrix = evidence.get("matrix") if isinstance(evidence.get("matrix"), dict) else {}
    decision = evidence.get("decision") if isinstance(evidence.get("decision"), dict) else {}
    summary = evidence.get("case_summary") if isinstance(evidence.get("case_summary"), dict) else {}
    lines = ["# AI Pipeline Dry-Run Matrix Evidence", ""]
    lines.append(f"- Generated at: `{evidence['generated_at']}`")
    lines.append(f"- Kind: `{evidence['kind']}`")
    lines.append(f"- Passed: `{evidence['passed']}`")
    lines.append(f"- Provider execution performed: `{evidence['provider_execution_performed']}`")
    lines.append(f"- Matrix report: `{evidence['source_matrix_report']}`")
    lines.append(f"- Matrix workers: `{matrix.get('matrix_workers')}`")
    lines.append(f"- Repeat cases: `{matrix.get('repeat_cases')}`")
    lines.append(f"- Cases: `{summary.get('case_count')}`")
    lines.extend(["", "## Decision", ""])
    for key, value in decision.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Case Summary", ""])
    for key, value in summary.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Validation Reports", ""])
    for item in evidence.get("validation_reports", []):
        lines.append(
            f"- `{item.get('path')}`: passed `{item.get('passed')}`, kind `{item.get('kind')}`"
        )
    lines.extend(["", "## Failed Cases", ""])
    failed = [
        item.get("name")
        for item in evidence.get("cases", [])
        if item.get("returncode") != 0
        or item.get("report_passed") is not True
        or item.get("dry_run") is not True
    ]
    if failed:
        lines.extend(f"- `{name}`" for name in failed)
    else:
        lines.append("None.")
    lines.extend(["", "This evidence summarizes dry-run planning only. It is not provider execution proof."])
    return "\n".join(lines) + "\n"
