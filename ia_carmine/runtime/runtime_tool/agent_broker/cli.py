#!/usr/bin/env python3
"""CLI wrapper for the report-only runtime tool broker."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from ia_carmine.runtime.runtime_tool.broker.common import (
        DEFAULT_MARKDOWN,
        DEFAULT_OUTPUT,
        resolve_path,
    )
    from ia_carmine.runtime.runtime_tool.broker.executor import build_report
    from ia_carmine.runtime.runtime_tool.broker.markdown import render_markdown
    from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS
    from Tools.validation._shared.report_utils import write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.runtime.runtime_tool.broker.common import (  # type: ignore
        DEFAULT_MARKDOWN,
        DEFAULT_OUTPUT,
        resolve_path,
    )
    from ia_carmine.runtime.runtime_tool.broker.executor import build_report  # type: ignore
    from ia_carmine.runtime.runtime_tool.broker.markdown import render_markdown  # type: ignore
    from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS  # type: ignore
    from Tools.validation._shared.report_utils import write_json_report  # type: ignore


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--request-json", default="")
    parser.add_argument("--tool-output-dir", default=None)
    parser.add_argument("--stamp", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    write_json_report(report, output)
    markdown.write_text(render_markdown(report), encoding="utf-8")

    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown),
                "tool_request_count": report["tool_request_count"],
                "tool_execution_count": report["tool_execution_count"],
                "blocked_tool_count": report["blocked_tool_count"],
                "failed_tool_count": report["failed_tool_count"],
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
                "sqlite_write_performed": report["sqlite_write_performed"],
                "persistent_memory_write_performed": report[
                    "persistent_memory_write_performed"
                ],
                "persistent_memory_write_count": report.get(
                    "persistent_memory_write_count", 0
                ),
                "operational_sqlite_write_performed": report[
                    "operational_sqlite_write_performed"
                ],
                "operational_sqlite_write_count": report["operational_sqlite_write_count"],
                "operational_memory_clear_count": report[
                    "operational_memory_clear_count"
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
