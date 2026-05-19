"""CLI for AI peer exchange contract validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report

from .report import build_report, render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument(
        "--primary-advisory", default="output/validation/gpu1_primary_advisory_{stamp}.json"
    )
    parser.add_argument(
        "--task-packet", default="output/validation/gpu0_peer_task_packet_{stamp}.json"
    )
    parser.add_argument(
        "--gpu0-response", default="output/validation/gpu0_peer_response_{stamp}.json"
    )
    parser.add_argument(
        "--gpu0-tool-requests", default="output/validation/gpu0_tool_requests_{stamp}.json"
    )
    parser.add_argument("--broker-report", default="")
    parser.add_argument("--npu-response", default="")
    parser.add_argument("--npu-broker-report", default="")
    parser.add_argument(
        "--peer-exchange", default="output/validation/ai_peer_exchange_{stamp}.json"
    )
    parser.add_argument("--require-broker-execution", action="store_true")
    parser.add_argument("--allow-degraded", action="store_true")
    parser.add_argument(
        "--output", default="output/validation/ai_peer_exchange_contract_{stamp}.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/ai_peer_exchange_contract_{stamp}.md"
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_output_path(repo_root, args.output.format(stamp=args.stamp))
    markdown = resolve_output_path(repo_root, args.markdown_output.format(stamp=args.stamp))
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] or args.allow_degraded else 2
