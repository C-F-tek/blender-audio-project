"""CLI for agent-review evidence sufficiency."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.validation.report_utils import write_json_report, write_text_report

from .evidence_common import DEFAULT_MARKDOWN, DEFAULT_OUTPUT, DEFAULT_REFINED_PROPOSALS, DEFAULT_REFINED_REVIEW, resolve_path
from .evidence_report import build_report, render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--refined-review", default=DEFAULT_REFINED_REVIEW)
    parser.add_argument("--refined-proposals", default=DEFAULT_REFINED_PROPOSALS)
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "ready_for_manual_patch_count": report["decision"]["ready_for_manual_patch_count"],
                "needs_more_context_count": report["decision"]["needs_more_context_count"],
                "sufficient_for_real_pr": report["decision"]["sufficient_for_real_pr"],
                "provider_execution_performed": False,
                "patch_application_performed": False,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report.get("passed") else 2
