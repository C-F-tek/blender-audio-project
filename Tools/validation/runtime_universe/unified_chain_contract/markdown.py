"""Markdown renderer for unified chain contract reports."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Unified Chain Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Stamp: `{report.get('stamp')}`",
        f"- Broken edge count: `{len(report.get('broken_edges') or [])}`",
        "",
        "## Edges",
        "",
        "| Edge | Passed | Actual | Action |",
        "|---|---:|---|---|",
    ]
    for edge in report.get("edges") or []:
        lines.append(
            f"| `{edge.get('edge')}` | `{edge.get('passed')}` | {str(edge.get('actual') or '').replace('|', '/')} | {str(edge.get('action') or '').replace('|', '/')} |"
        )
    if report.get("broken_edges"):
        lines.extend(["", "## Broken edges", ""])
        for edge in report["broken_edges"]:
            lines.extend(
                [
                    f"### {edge.get('edge')}",
                    "",
                    f"- Producer: `{edge.get('producer')}`",
                    f"- Consumer: `{edge.get('consumer')}`",
                    f"- Expected: {edge.get('expected')}",
                    f"- Actual: {edge.get('actual')}",
                    f"- Action: {edge.get('action')}",
                    "",
                ]
            )
    return "\n".join(lines) + "\n"
