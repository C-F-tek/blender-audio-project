from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from build_agent_memory_inventory import (
        DEFAULT_MARKDOWN,
        DEFAULT_MEMORY_DB,
        DEFAULT_OUTPUT,
        build_inventory,
        resolve_path,
    )
except ModuleNotFoundError:
    from Tools.ai.build_agent_memory_inventory import (
        DEFAULT_MARKDOWN,
        DEFAULT_MEMORY_DB,
        DEFAULT_OUTPUT,
        build_inventory,
        resolve_path,
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Agent Memory Inventory",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Patch application performed: `{report.get('patch_application_performed')}`",
        f"- Memory DB: `{report.get('inputs', {}).get('memory_db')}`",
        f"- Memory DB exists: `{report.get('inputs', {}).get('memory_db_exists')}`",
        f"- Record count: `{report.get('records', {}).get('record_count')}`",
        f"- SQLite opened read-only: `{report.get('sqlite', {}).get('opened')}`",
        "",
        "## SQLite",
        "",
        f"- Schema version: `{report.get('sqlite', {}).get('schema_version')}`",
        "",
    ]
    for table in report.get("sqlite", {}).get("tables", []):
        lines.append(
            f"- `{table.get('name')}` rows=`{table.get('row_count')}` "
            f"columns=`{len(table.get('columns', []))}`"
        )
    lines.extend(["", "## Record distributions", ""])
    _append_record_distributions(lines, report)
    _append_policy_summary(lines, report)
    _append_selected_preview(lines, report)
    _append_warnings(lines, report)
    lines.extend(["", "## Guardrails", ""])
    for key, value in report.get("guardrails", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def _append_record_distributions(lines: list[str], report: dict[str, Any]) -> None:
    for name in ("kind_counts", "scope_counts", "confidence_buckets"):
        lines.append(f"### {name}")
        lines.append("")
        values = report.get("records", {}).get(name, {})
        if not values:
            lines.append("None.")
        for key, count in values.items():
            lines.append(f"- `{key}`: {count}")
        lines.append("")


def _append_policy_summary(lines: list[str], report: dict[str, Any]) -> None:
    lines.extend(["## Policy summary", ""])
    policy = report.get("policy_report", {})
    for key in ("passed", "promotion_candidate_count", "review_count", "risk_count", "duplicate_group_count"):
        lines.append(f"- `{key}`: `{policy.get(key)}`")


def _append_selected_preview(lines: list[str], report: dict[str, Any]) -> None:
    lines.extend(["", "## Selected memory preview", ""])
    preview = report.get("selected_memory_preview", [])
    if not preview:
        lines.append("None.")
    for item in preview:
        lines.extend(
            [
                f"### {item.get('record_id')} - {item.get('source')}",
                "",
                f"- Kind: `{item.get('kind')}`",
                f"- Scope: `{item.get('scope')}`",
                f"- Score: `{item.get('rank_score')}`",
                "",
                str(item.get("summary") or ""),
                "",
            ]
        )


def _append_warnings(lines: list[str], report: dict[str, Any]) -> None:
    if report.get("warnings"):
        lines.extend(["## Warnings", ""])
        for warning in report["warnings"]:
            lines.append(f"- {warning}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--objective",
        default="Inventory generic agent memory for IA-Carmine orchestration and megalithic review.",
    )
    parser.add_argument("--memory-db", default=DEFAULT_MEMORY_DB)
    parser.add_argument("--memory-jsonl", action="append", default=[])
    parser.add_argument("--memory-db-limit", type=int, default=1000)
    parser.add_argument("--max-memory-chars", type=int, default=24000)
    parser.add_argument("--max-preview-records", type=int, default=20)
    parser.add_argument("--max-policy-items", type=int, default=30)
    parser.add_argument("--max-sqlite-tables", type=int, default=40)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_inventory(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(_summary(report, output, markdown_output), indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


def _summary(report: dict[str, Any], output: Path, markdown_output: Path) -> dict[str, Any]:
    return {
        "passed": report["passed"],
        "output": str(output),
        "markdown": str(markdown_output),
        "record_count": report["records"]["record_count"],
        "memory_db_exists": report["inputs"]["memory_db_exists"],
        "provider_execution_performed": False,
        "patch_application_performed": False,
    }
