"""CLI for agent-review code patch plans."""

from __future__ import annotations

import argparse
from pathlib import Path

from .code_patch_plan_builder import build_code_patch_plan
from .code_patch_plan_deps import (
    DEFAULT_CODE_DRIFT_REPORT,
    DEFAULT_LINE_COUNT_CSV,
    DEFAULT_MARKDOWN,
    DEFAULT_OUTPUT,
    resolve_output_path,
    write_json_and_markdown,
)
from .code_patch_plan_render import render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--code-contract-drift-report", default=DEFAULT_CODE_DRIFT_REPORT)
    parser.add_argument("--line-count-csv", default=DEFAULT_LINE_COUNT_CSV)
    parser.add_argument(
        "--code-interpreter-report",
        help="Optional code_interpreter_report JSON to turn static recommendations into patch-plan candidates.",
    )
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    code_drift_path = resolve_output_path(repo_root, args.code_contract_drift_report)
    line_count_csv = resolve_output_path(repo_root, args.line_count_csv)
    code_interpreter_path = (
        resolve_output_path(repo_root, args.code_interpreter_report)
        if args.code_interpreter_report
        else None
    )
    report = build_code_patch_plan(
        repo_root, code_drift_path, line_count_csv, code_interpreter_path
    )
    print(
        write_json_and_markdown(
            repo_root,
            report,
            args.output,
            args.markdown_output,
            render_markdown(report),
        ),
        end="",
    )
    return 0 if report["passed"] else 2
