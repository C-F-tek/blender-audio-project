"""CLI entrypoint for AI peer exchange packet generation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .common import resolve_output_path, write_json_report, write_text_report
from .exchange import build_exchange
from .render import render_exchange, render_primary

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--gpu-report", required=True)
    parser.add_argument("--gpu-markdown", default="")
    parser.add_argument("--source-report", action="append", default=[])
    parser.add_argument("--response-report", default="")
    parser.add_argument("--broker-report", default="")
    parser.add_argument("--npu-report", default="")
    parser.add_argument("--npu-broker-report", default="")
    parser.add_argument("--contract-report", default="")
    parser.add_argument(
        "--primary-output",
        default="output/validation/gpu1_primary_advisory_{stamp}.json",
    )
    parser.add_argument(
        "--primary-markdown-output",
        default="output/validation/gpu1_primary_advisory_{stamp}.md",
    )
    parser.add_argument(
        "--task-output", default="output/validation/gpu0_peer_task_packet_{stamp}.json"
    )
    parser.add_argument(
        "--exchange-output", default="output/validation/ai_peer_exchange_{stamp}.json"
    )
    parser.add_argument(
        "--exchange-markdown-output",
        default="output/validation/ai_peer_exchange_{stamp}.md",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    built = build_exchange(args)
    primary_path = resolve_output_path(repo_root, args.primary_output.format(stamp=args.stamp))
    primary_md = resolve_output_path(
        repo_root, args.primary_markdown_output.format(stamp=args.stamp)
    )
    task_path = resolve_output_path(repo_root, args.task_output.format(stamp=args.stamp))
    exchange_path = resolve_output_path(repo_root, args.exchange_output.format(stamp=args.stamp))
    exchange_md = resolve_output_path(
        repo_root, args.exchange_markdown_output.format(stamp=args.stamp)
    )
    write_json_report(built["primary"], primary_path)
    write_text_report(render_primary(built["primary"]), primary_md)
    write_json_report(built["task_packet"], task_path)
    print(write_json_report(built["exchange"], exchange_path), end="")
    write_text_report(render_exchange(built["exchange"]), exchange_md)
    return 0
