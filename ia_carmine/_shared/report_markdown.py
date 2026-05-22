"""Small Markdown rendering helpers for JSON report summaries."""

from __future__ import annotations

from typing import Any, Iterable


def report_header(title: str, fields: Iterable[tuple[str, Any]]) -> list[str]:
    lines = [f"# {title}", ""]
    lines.extend(f"- {label}: `{value}`" for label, value in fields)
    return lines


def append_errors_and_warnings(lines: list[str], report: dict[str, Any]) -> None:
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
