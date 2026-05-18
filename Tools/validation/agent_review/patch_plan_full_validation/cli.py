"""CLI for agent review patch-plan full validation."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report

from .defaults import (
    DEFAULT_BUNDLE_BASENAME,
    DEFAULT_BUNDLE_VALIDATION,
    DEFAULT_DOCS_LINKS,
    DEFAULT_EVIDENCE,
    DEFAULT_EVIDENCE_DIR,
    DEFAULT_MARKDOWN,
    DEFAULT_ORCHESTRATOR,
    DEFAULT_OUTPUT,
    DEFAULT_PATCH_PLAN,
    DEFAULT_PATCH_PLAN_MARKDOWN,
    DEFAULT_PYTHON_SYNTAX,
    DEFAULT_REPORT_CONTRACT,
    DEFAULT_SMOKE,
    DEFAULT_SMOKE_MARKDOWN,
)
from .markdown import render_markdown
from .runner import run_full_validation

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--orchestrator", default=DEFAULT_ORCHESTRATOR)
    parser.add_argument("--evidence", default=DEFAULT_EVIDENCE)
    parser.add_argument("--patch-plan", default=DEFAULT_PATCH_PLAN)
    parser.add_argument("--patch-plan-markdown", default=DEFAULT_PATCH_PLAN_MARKDOWN)
    parser.add_argument("--smoke-output", default=DEFAULT_SMOKE)
    parser.add_argument("--smoke-markdown-output", default=DEFAULT_SMOKE_MARKDOWN)
    parser.add_argument("--docs-links-output", default=DEFAULT_DOCS_LINKS)
    parser.add_argument("--python-syntax-output", default=DEFAULT_PYTHON_SYNTAX)
    parser.add_argument("--validation-report-contract-output", default=DEFAULT_REPORT_CONTRACT)
    parser.add_argument("--bundle-basename", default=DEFAULT_BUNDLE_BASENAME)
    parser.add_argument("--evidence-output-dir", default=DEFAULT_EVIDENCE_DIR)
    parser.add_argument("--bundle-validation-output", default=DEFAULT_BUNDLE_VALIDATION)
    parser.add_argument("--min-patch-plans", type=int, default=12)
    parser.add_argument("--expect-fallback", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--git-timeout-seconds", type=int, default=60)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_full_validation(args)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
