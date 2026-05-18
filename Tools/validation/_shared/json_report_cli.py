"""Reusable JSON-report CLI harness for validation tools."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report

ReportBuilder = Callable[[argparse.Namespace, Path], dict]
ParserConfigurer = Callable[[argparse.ArgumentParser], None]


def run_json_report_cli(
    *,
    configure_parser: ParserConfigurer,
    build_report: ReportBuilder,
    description: str | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--repo-root", default=".")
    configure_parser(parser)
    parser.add_argument("--output", help="Optional JSON validation report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args, repo_root)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    print(write_json_report(report, output), end="")
    return 0 if report.get("passed") else 2
