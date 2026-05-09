"""Report writers for agent_runtime_debug_lab."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from Tools.validation.report_utils import resolve_output_path, write_text_report
except ImportError:
    from report_utils import resolve_output_path, write_text_report  # type: ignore


def render_guardrails(report: dict[str, Any]) -> list[str]:
    guardrails = report.get("guardrails") or {}
    lines = ["", "## Guardrails", "", "| Guardrail | Value |", "|---|---:|"]
    for key in sorted(guardrails):
        lines.append(f"| `{key}` | `{guardrails[key]}` |")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Agent Runtime Debug Lab",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Operation count: `{report.get('operation_count')}`",
        f"- Failed count: `{report.get('failed_count')}`",
        "",
        "## Operations",
        "",
        "| ID | Type | Executed | OK | Return code | Outputs |",
        "|---|---|---:|---:|---:|---|",
    ]
    for item in report.get("operations") or []:
        outputs = ", ".join(f"`{path}`" for path in item.get("outputs", []))
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` | `{}` | {} |".format(
                item.get("id", ""),
                item.get("type", ""),
                item.get("executed", False),
                item.get("ok", False),
                item.get("returncode", ""),
                outputs,
            )
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report.get("errors", []))
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report.get("warnings", []))
    lines.extend(render_guardrails(report))
    return "\n".join(lines) + "\n"


def write_reports(repo_root: Path, output: str, markdown_output: str, report: dict[str, Any], markdown: str) -> None:
    output_path = resolve_output_path(repo_root, output)
    markdown_path = resolve_output_path(repo_root, markdown_output)
    if not output_path.resolve().relative_to(repo_root.resolve()).as_posix().startswith("output/validation/"):
        raise ValueError("JSON output must be under output/validation/")
    if not markdown_path.resolve().relative_to(repo_root.resolve()).as_posix().startswith("output/validation/"):
        raise ValueError("Markdown output must be under output/validation/")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_text_report(markdown, markdown_path)
