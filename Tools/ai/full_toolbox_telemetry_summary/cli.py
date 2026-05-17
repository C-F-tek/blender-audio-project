"""CLI entrypoint for full-toolbox telemetry summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from .common import DEFAULT_MARKDOWN, DEFAULT_OUTPUT, resolve_output_path, write_json_report, write_text_report
from .markdown import render_markdown
from .summary import build_summary

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--decision-loop", required=True)
    parser.add_argument("--recommendations", required=True)
    parser.add_argument("--patch-plan", required=True)
    parser.add_argument("--repository-consistency", default="")
    parser.add_argument("--repository-consistency-smoke", default="")
    parser.add_argument("--gpu-npu-sync", default="")
    parser.add_argument("--orchestrator", default="")
    parser.add_argument("--gpu-report", default="")
    parser.add_argument("--peer-exchange", default="")
    parser.add_argument("--peer-contract", default="")
    parser.add_argument("--provider-runtime-heap-telemetry", default="")
    parser.add_argument("--provider-runtime-heap-snapshot", default="")
    parser.add_argument("--provider-runtime-heap-live-signal", action="append", default=[])
    parser.add_argument("--line-count-csv", default="")
    parser.add_argument("--evidence-to-commit", action="append", default=[])
    parser.add_argument("--bundle-validation-passed", action="store_true")
    parser.add_argument("--budget-minutes", type=int, default=0)
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--files-per-round", type=int, default=0)
    parser.add_argument("--max-context-files", type=int, default=0)
    parser.add_argument("--max-chars-per-file", type=int, default=0)
    parser.add_argument("--max-new-tokens", type=int, default=0)
    parser.add_argument("--npu-auditor-every-rounds", type=int, default=0)
    parser.add_argument("--repository-consistency-map-workers", type=int, default=0)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_summary(args)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report) + "\n", markdown_output)
    return 0 if report["passed"] else 2
