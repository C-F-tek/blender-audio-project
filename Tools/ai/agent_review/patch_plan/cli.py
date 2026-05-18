"""CLI entrypoint for agent review patch plans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from Tools.validation._shared.report_utils import write_json_report, write_text_report

from .builder import build_patch_plan
from .common import DEFAULT_EVIDENCE, DEFAULT_MARKDOWN, DEFAULT_ORCHESTRATOR, DEFAULT_OUTPUT, resolve_path
from .markdown import render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--orchestrator", default=DEFAULT_ORCHESTRATOR)
    parser.add_argument("--evidence", default=DEFAULT_EVIDENCE)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument(
        "--max-patch-plans",
        type=int,
        default=0,
        help="Compatibility/telemetry only; does not truncate valid patch plans.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_patch_plan(args)
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
                "patch_plan_count": report["patch_plan_count"],
                "available_patch_plan_count": report.get("available_patch_plan_count"),
                "max_patch_plans": report.get("max_patch_plans"),
                "requested_max_patch_plans": report.get("requested_max_patch_plans"),
                "fallback_used": report["decision"]["fallback_used"],
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
                "manual_review_required": report["decision"]["manual_review_required"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2
