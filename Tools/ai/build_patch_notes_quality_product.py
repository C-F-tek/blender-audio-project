#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[2]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from Tools.ai.patch_notes_quality_product.builder import build_report
from Tools.ai.patch_notes_quality_product.reporting import render_markdown
from Tools.ai.patch_plan_quality_product.io_utils import resolve, write_json, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--task-markdown", required=True)
    parser.add_argument("--patch-plan", required=True)
    parser.add_argument("--patch-quality", default="")
    parser.add_argument("--decision-loop", default="")
    parser.add_argument("--runtime-usage", default="")
    parser.add_argument("--runtime-capability", default="")
    parser.add_argument("--repository-consistency", default="")
    parser.add_argument("--memory-bundle", default="")
    parser.add_argument("--full-toolbox-telemetry", default="")
    parser.add_argument("--github-evidence-bundle", default="")
    parser.add_argument("--branch", default="")
    parser.add_argument("--commit", default="")
    parser.add_argument("--issue", default="")
    parser.add_argument("--request", default="")
    parser.add_argument("--extra-context", action="append", default=[])
    parser.add_argument("--sqlite-fts-db", required=True)
    parser.add_argument("--min-quality-score", type=float, default=72.0)
    parser.add_argument("--strict-patch-notes-quality-gate", action="store_true")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve(repo_root, args.output)
    markdown = resolve(repo_root, args.markdown_output)
    write_json(output, report)
    write_text(markdown, render_markdown(report))
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "quality_gate_passed": report["quality_gate_passed"],
                "classification": report["classification"],
                "quality_score": report["quality_score"],
                "patch_note_count": len(report["patch_notes"]),
                "fallback_path_note_count": len(report["fallback_path_notes"]),
                "success_case_count": len(report.get("success_cases", [])),
                "fallback_case_count": len(report.get("fallback_cases", [])),
                "output": str(output),
                "markdown": str(markdown),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
