from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ia_carmine.context.agent_context.agnostic_tool_inventory import (
    DEFAULT_MARKDOWN,
    DEFAULT_OUTPUT,
    build_inventory,
    resolve_path,
)


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Agnostic Tool Inventory", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Tool count: `{report['summary']['tool_count']}`")
    lines.append("")
    for section in (
        "category_counts",
        "owner_lane_counts",
        "consumed_lane_counts",
        "apply_mode_counts",
        "provider_execution_default_counts",
    ):
        lines.append(f"## {section}")
        lines.append("")
        for key, count in report["summary"].get(section, {}).items():
            lines.append(f"- `{key}`: {count}")
        lines.append("")
    lines.append("## Categories")
    lines.append("")
    for category, records in report.get("by_category", {}).items():
        lines.append(f"### {category}")
        lines.append("")
        for record in records[:20]:
            lines.append(
                f"- `{record['path']}` lane=`{record['owner_lane']}` "
                f"apply=`{record['apply_mode']}` provider=`{record['provider_execution_default']}`"
            )
        lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    for key, value in report.get("guardrails", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--root", action="append", default=[])
    parser.add_argument("--max-tools", type=int, default=800)
    parser.add_argument("--max-items-per-category", type=int, default=120)
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
    return 0


def _summary(report: dict[str, Any], output: Path, markdown_output: Path) -> dict[str, Any]:
    return {
        "passed": report["passed"],
        "output": str(output),
        "markdown": str(markdown_output),
        "tool_count": report["summary"]["tool_count"],
        "provider_execution_performed": False,
        "patch_application_performed": False,
    }
