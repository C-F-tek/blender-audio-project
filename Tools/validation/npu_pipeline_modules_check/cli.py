"""CLI for NPU pipeline module smoke checker."""

from __future__ import annotations

import argparse
from pathlib import Path

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report

from .checker import npu_pipeline_modules_check

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = npu_pipeline_modules_check(repo_root)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    text = write_json_report(report, output)
    print(text, end="")
    return 0 if report["passed"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
