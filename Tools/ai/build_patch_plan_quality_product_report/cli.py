#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.ai.patch_plan_quality_product.builder import build_report
from tools.ai.patch_plan_quality_product.io_utils import resolve, write_json, write_text
from tools.ai.patch_plan_quality_product.reporting import render_markdown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--patch-plan", required=True)
    parser.add_argument("--decision-loop", required=True)
    parser.add_argument("--recommendations", required=True)
    parser.add_argument("--runtime-usage", required=True)
    parser.add_argument("--runtime-capability", required=True)
    parser.add_argument("--repository-consistency", required=True)
    parser.add_argument("--memory-bundle", default="")
    parser.add_argument("--request", default="")
    parser.add_argument("--extra-context", action="append", default=[])
    parser.add_argument("--sqlite-fts-db", required=True)
    parser.add_argument("--min-average-score", type=float, default=72.0)
    parser.add_argument("--min-plan-score", type=float, default=60.0)
    parser.add_argument("--search-limit", type=int, default=6)
    parser.add_argument("--strict-quality-gate", action="store_true")
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
                "output": str(output),
                "markdown": str(markdown),
                "fallback_path_note_count": len(report["fallback_path_notes"]),
                "patch_plan_count": report["quality"]["patch_plan_count"],
                "average_plan_score": report["quality"]["average_plan_score"],
                "sqlite_fts5_enabled": report["quality"]["sqlite_fts5_enabled"],
                "fts_total_hit_count": report["quality"]["fts_total_hit_count"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
