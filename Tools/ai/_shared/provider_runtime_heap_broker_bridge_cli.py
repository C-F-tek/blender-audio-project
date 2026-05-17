from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

repo_root_for_import = Path(__file__).resolve().parents[2]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report

try:
    from provider_runtime_heap_broker_bridge import DEFAULT_MARKDOWN, DEFAULT_OUTPUT, build_report
except ModuleNotFoundError:
    from Tools.ai.provider_runtime_heap_broker_bridge import (
        DEFAULT_MARKDOWN,
        DEFAULT_OUTPUT,
        build_report,
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Provider Runtime Heap Broker Bridge", ""]
    for key in (
        "passed",
        "dry_run",
        "stamp",
        "pending_broker_request_count",
        "broker_result_event_count",
        "broker_returncode",
        "broker_passed",
        "tool_request_count",
        "tool_execution_count",
        "blocked_tool_count",
        "failed_tool_count",
        "request_packet",
        "broker_report",
        "tool_output_dir",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--heap-markdown", default="")
    parser.add_argument("--bridge-dir", default="output/ai_runtime_heap/{stamp}/broker_bridge")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--max-requests", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_output_path(repo_root, args.output.format(stamp=args.stamp))
    markdown = resolve_output_path(repo_root, args.markdown_output.format(stamp=args.stamp))
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 1
