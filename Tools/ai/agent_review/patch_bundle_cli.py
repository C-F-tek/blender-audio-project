"""CLI for agent-review patch bundle builder."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from Tools.validation._shared.report_utils import write_json_report, write_text_report

from .patch_bundle_builder import build_bundle, render_markdown
from .patch_bundle_common import (
    DEFAULT_BASENAME,
    DEFAULT_MARKDOWN,
    DEFAULT_OUTPUT,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PATCH_PLAN,
    resolve_path,
)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--patch-plan", default=DEFAULT_PATCH_PLAN)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=DEFAULT_BASENAME)
    parser.add_argument("--stamp", default="")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument("--write-bundle", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_bundle(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "errors": report["errors"],
                "warnings": report["warnings"],
                "output": str(output),
                "markdown": str(markdown_output),
                "bundle_zip": report.get("bundle_zip"),
                "operation_count": report["operation_count"],
                "skipped_candidate_count": report["skipped_candidate_count"],
                "patch_application_performed": report["patch_application_performed"],
                "sqlite_write_performed": report["sqlite_write_performed"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2
