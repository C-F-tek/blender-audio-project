"""CLI entrypoint for refactor duplication audits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .common import now_stamp, resolve_output_path, write_json_report
from .markdown import render_markdown
from .report import build_report

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default=None)
    parser.add_argument("--root", action="append", default=[])
    parser.add_argument("--report", action="append", default=[])
    parser.add_argument("--line-count-report", action="append", default=[])
    parser.add_argument("--code-interpreter-report", action="append", default=[])
    parser.add_argument("--python-syntax-report", action="append", default=[])
    parser.add_argument("--bundle-smoke-report", action="append", default=[])
    parser.add_argument("--memory-routing-report", action="append", default=[])
    parser.add_argument("--input-audit-report", action="append", default=[])
    parser.add_argument("--max-candidates", type=int, default=40)
    parser.add_argument("--output", default=None)
    parser.add_argument("--markdown-output", default=None)
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or now_stamp()
    if not args.stamp:
        args.stamp = stamp
    output = resolve_output_path(
        repo_root,
        args.output or f"output/analysis/refactor_duplication_audit_{stamp}.json",
    )
    markdown = resolve_output_path(
        repo_root,
        args.markdown_output or f"output/analysis/refactor_duplication_audit_{stamp}.md",
    )
    report = build_report(args)
    write_json_report(report, output)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown),
                "python_file_count": report["python_file_count"],
                "function_count": report["function_count"],
                "duplication_candidate_count": report["duplication_candidate_count"],
                "manual_review_patch_plan_candidate_count": len(
                    report["manual_review_patch_plan_candidates"]
                ),
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
                "sqlite_write_performed": report["sqlite_write_performed"],
                "persistent_memory_write_performed": report["persistent_memory_write_performed"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report.get("passed") else 2
