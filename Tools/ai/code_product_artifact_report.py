#!/usr/bin/env python3
"""Markdown rendering for code product artifact intake reports."""

from __future__ import annotations

from typing import Any


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Code Product Artifact Intake",
        "",
        f"- Artifact: `{report.get('code_product_path')}`",
        f"- Passed: `{report.get('passed')}`",
        f"- All integrated: `{report.get('all_integrated')}`",
        f"- Target count: `{report.get('target_count')}`",
        f"- Already integrated: `{report.get('already_integrated_count')}`",
        f"- Forward applicable: `{report.get('forward_applicable_count')}`",
        f"- Needs review: `{report.get('needs_review_count')}`",
        "",
        "| Target | Status | Exists | Payload |",
        "|---|---:|---:|---:|",
    ]
    for item in report.get("sections", []):
        lines.append(
            f"| `{item.get('target_file')}` | `{item.get('status')}` | `{item.get('target_exists')}` | `{item.get('payload_kind')}` |"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"
