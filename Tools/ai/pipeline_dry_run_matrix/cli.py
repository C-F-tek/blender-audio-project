"""CLI entrypoint for the pipeline dry-run matrix."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from pipeline.markdown_report import write_dry_run_matrix_markdown
except ImportError:
    from tools.ai.pipeline.markdown_report import write_dry_run_matrix_markdown  # type: ignore

from .cases import default_cases
from .common import default_matrix_workers, repeat_cases
from .runner import run_cases

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-dir", default="output/ai_pipeline/dry_run_matrix")
    parser.add_argument("--output", default="output/ai_pipeline/dry_run_matrix_report.json")
    parser.add_argument("--markdown-output", default="output/ai_pipeline/dry_run_matrix_report.md")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument(
        "--matrix-workers",
        type=int,
        default=default_matrix_workers(),
        help="Number of matrix cases to execute concurrently. Default: min(8, CPU count). Use 1 for serial execution.",
    )
    parser.add_argument(
        "--repeat-cases",
        type=int,
        default=1,
        help="Repeat the full case matrix N times with unique output directories for stress testing. Default: 1.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix_workers = max(1, args.matrix_workers)
    repeat_count = max(1, args.repeat_cases)
    base_cases = default_cases(repo_root)
    cases = repeat_cases(base_cases, repeat_count)
    results = run_cases(repo_root, output_dir, cases, matrix_workers, args.continue_on_error)

    passed = all(item["returncode"] == 0 and item.get("report_passed") is True for item in results)
    report = {
        "schema_version": 1,
        "repo_root": str(repo_root),
        "output_dir": str(output_dir),
        "case_count": len(results),
        "planned_case_count": len(cases),
        "base_case_count": len(base_cases),
        "repeat_cases": repeat_count,
        "matrix_workers": matrix_workers,
        "passed": passed,
        "results": results,
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output = write_dry_run_matrix_markdown(args.markdown_output, report)
    report["markdown_output"] = str(markdown_output)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if passed else 2
