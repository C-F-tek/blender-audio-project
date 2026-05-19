"""CLI for the unified validation gate."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

from .registry import build_registered_steps, select_steps
from .report import render_markdown
from .runner import run_gate

DEFAULT_OUTPUT = "output/validation/validation_gate.json"
DEFAULT_MARKDOWN = "output/validation/validation_gate.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--suite", choices=("quick", "refactor", "smoke", "deep", "all"), default="quick")
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--include-heavy", action="store_true")
    parser.add_argument("--include-provider-live", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--heavy-timeout-seconds", type=int, default=900)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if args.list:
        report = {
            "schema_version": 1,
            "kind": "validation_gate_registry",
            "repo_root": str(repo_root),
            "suite": args.suite,
            "steps": [
                {
                    "name": step.name,
                    "suites": list(step.suites),
                    "command": step.command,
                    "heavy": step.heavy,
                    "provider_live": step.provider_live,
                    "tags": list(step.tags),
                }
                for step in build_registered_steps(args)
            ],
        }
        print(write_json_report(report, None), end="")
        return 0

    report = run_gate(repo_root, select_steps(args), dry_run=args.dry_run)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown_output)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
