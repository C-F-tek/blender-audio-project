from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

repo_root_for_import = Path(__file__).resolve().parents[3]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from Tools.validation._shared.report_utils import write_json_report, write_text_report

from .builder import build_policy_report
from .common import DEFAULT_MARKDOWN_OUTPUT, DEFAULT_OUTPUT, resolve_path
from .markdown import render_markdown


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--decision-report", required=True)
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--final-report", action="append", default=[])
    parser.add_argument("--min-recommendations", type=int, default=1)
    parser.add_argument("--min-patch-plans", type=int, default=1)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN_OUTPUT)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_policy_report(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(json.dumps(_summary(report, output, markdown_output), indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


def _summary(report: dict, output: Path, markdown_output: Path) -> dict:
    return {
        "passed": report["passed"],
        "output": str(output),
        "markdown": str(markdown_output),
        "decision_recovered": report["decision_recovered"],
        "warning_count": report["warning_count"],
        "input_nonfatal_warning_count": report["input_nonfatal_warning_count"],
        "fatal_report_failure_count": report["fatal_report_failure_count"],
        "provider_execution_performed": report["provider_execution_performed"],
        "patch_application_performed": report["patch_application_performed"],
    }
