"""CLI for GPU/NPU run sync analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ia_carmine._shared.report_io import write_json_report, write_text_report

from .analysis import analyze, render_markdown
from .common import resolve_path

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--orchestrator", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = analyze(repo_root, resolve_path(repo_root, args.orchestrator))
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report) + "\n", markdown_output)
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "npu_to_gpu_avg_duration_ratio": report["metrics"]["npu_to_gpu_avg_duration_ratio"],
                "npu_too_slow_for_per_round_lockstep": report["decision"][
                    "npu_too_slow_for_per_round_lockstep"
                ],
                "performance": report["performance"],
                "refactoring_suggestion_count": len(report["refactoring_suggestions"]),
                "patch_application_performed": report["patch_application_performed"],
                "source_writes_performed": report["source_writes_performed"],
            },
            indent=2,
        )
    )
    return 0
