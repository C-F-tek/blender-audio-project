from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from build_script_inventory import (
        DEFAULT_CSV_OUTPUT,
        DEFAULT_OUTPUT,
        build_report,
        write_csv,
        write_json,
    )
except ModuleNotFoundError:
    from Tools.validation.build_script_inventory import (
        DEFAULT_CSV_OUTPUT,
        DEFAULT_OUTPUT,
        build_report,
        write_csv,
        write_json,
    )


def render_markdown(report: dict[str, Any], max_rows: int) -> str:
    lines: list[str] = []
    lines.append("# Script and Tool Inventory")
    lines.append("")
    lines.append(f"- Kind: `{report['kind']}`")
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Script count: `{report['script_count']}`")
    lines.append(f"- Syntax warning count: `{report['syntax_warning_count']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.extend(["", "## Category counts", "", "| Category | Count |", "|---|---:|"])
    for key, value in report["category_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Inventory sample", ""])
    lines.append("| Path | Language | Category | Lines | Description | Functions/classes |")
    lines.append("|---|---|---|---:|---|---|")
    for item in report["items"][:max_rows]:
        lines.append(_inventory_row(item))
    if len(report["items"]) > max_rows:
        lines.extend(
            [
                "",
                f"_Rows truncated in Markdown view: {max_rows}/{len(report['items'])}. Use CSV/JSON for full inventory._",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def _inventory_row(item: dict[str, Any]) -> str:
    callables = []
    if item["functions"]:
        callables.append("fn: " + ", ".join(item["functions"][:8]))
    if item["classes"]:
        callables.append("class: " + ", ".join(item["classes"][:6]))
    callables_text = "<br>".join(callables) if callables else "not specified"
    description = str(item["description"]).replace("|", "\\|")
    return (
        f"| `{item['path']}` | `{item['language']}` | `{item['category']}` | "
        f"{item['lines']} | {description} | {callables_text} |"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a report-only inventory of repository scripts and tools.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="JSON output path.")
    parser.add_argument("--csv-output", default=DEFAULT_CSV_OUTPUT, help="CSV output path.")
    parser.add_argument("--markdown-output", default=None, help="Optional Markdown output path.")
    parser.add_argument("--markdown-max-rows", type=int, default=120, help="Maximum Markdown rows.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    write_json(Path(args.output), report)
    write_csv(Path(args.csv_output), report)
    if args.markdown_output:
        Path(args.markdown_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.markdown_output).write_text(
            render_markdown(report, max_rows=args.markdown_max_rows),
            encoding="utf-8",
        )
    return 0
