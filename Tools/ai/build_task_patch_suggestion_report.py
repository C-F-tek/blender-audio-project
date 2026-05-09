#!/usr/bin/env python3
"""Convert task Markdown embedded patch suggestions into a JSON report."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Tools.ai.patch_suggestion_bundle.task_markdown import (
    build_task_patch_suggestion_report,
    write_markdown,
)
from Tools.validation.report_utils import resolve_output_path, write_json_report


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--task-file", required=True)
    parser.add_argument("--Stamp", default="")
    parser.add_argument("--output", default="output/validation/task_patch_suggestions.json")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--allow-empty", action="store_true")
    parser.add_argument("--empty-reason", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    task_file = Path(args.task_file)
    if not task_file.is_absolute():
        task_file = repo_root / task_file
    task_file = task_file.resolve()

    task_rel = task_file.relative_to(repo_root).as_posix()
    process_gate_task = task_rel.startswith("output/local_ai_task_inputs/")
    allow_empty = bool(args.allow_empty or process_gate_task)
    empty_reason = args.empty_reason
    if allow_empty and not empty_reason:
        empty_reason = "Task Markdown is an entry contract; runtime/generated patch-spec product is expected downstream."

    report = build_task_patch_suggestion_report(
        repo_root,
        task_file,
        args.Stamp,
        allow_empty=allow_empty,
        empty_reason=empty_reason,
    )
    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    if args.markdown_output:
        write_markdown(report, resolve_output_path(repo_root, args.markdown_output))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
