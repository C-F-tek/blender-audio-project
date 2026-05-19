"""Shared CLI output helpers for agent-review report tools."""

from __future__ import annotations

import json
import argparse
from pathlib import Path
from typing import Any, Callable

from Tools.validation._shared.report_utils import write_json_report, write_text_report

RenderMarkdown = Callable[[dict[str, Any]], str]
SummaryBuilder = Callable[[dict[str, Any], Path, Path], dict[str, Any]]
ParserConfigurer = Callable[[argparse.ArgumentParser], None]
ReportBuilder = Callable[[argparse.Namespace], dict[str, Any]]
PathResolver = Callable[[Path, str], Path]


def write_report_and_print_summary(
    *,
    report: dict[str, Any],
    output: Path,
    markdown_output: Path,
    render_markdown: RenderMarkdown,
    build_summary: SummaryBuilder,
) -> None:
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(json.dumps(build_summary(report, output, markdown_output), indent=2, ensure_ascii=False))


def run_report_cli(
    *,
    configure_parser: ParserConfigurer,
    build_report: ReportBuilder,
    render_markdown: RenderMarkdown,
    build_summary: SummaryBuilder,
    resolve_path: PathResolver,
    default_output: str,
    default_markdown: str,
    description: str,
) -> int:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--repo-root", default=".")
    configure_parser(parser)
    parser.add_argument("--output", default=default_output)
    parser.add_argument("--markdown-output", default=default_markdown)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_report_and_print_summary(
        report=report,
        output=output,
        markdown_output=markdown_output,
        render_markdown=render_markdown,
        build_summary=build_summary,
    )
    return 0 if report.get("passed") else 2
