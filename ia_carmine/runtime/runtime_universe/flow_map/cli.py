"""CLI for runtime flow-map evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ia_carmine._shared.report_io import resolve_output_path, write_json_report, write_text_report

from .builder import build_flow
from .common import DEFAULT_ENTRYPOINT, DEFAULT_OUTPUT_DIR, as_list
from .render import build_markdown, build_mermaid, write_jsonl

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--entrypoint", default=DEFAULT_ENTRYPOINT)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default="")
    parser.add_argument("--report", action="append", default=[])
    parser.add_argument("--output", default="")
    parser.add_argument("--jsonl-output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--mermaid-output", default="")
    return parser

def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).resolve()
    flow = build_flow(args)
    stamp = str(flow["stamp"])
    basename = args.basename or f"runtime_flow_{stamp}"
    output_dir = resolve_output_path(repo_root, args.output_dir)
    json_output = (
        resolve_output_path(repo_root, args.output)
        if args.output
        else output_dir / f"{basename}.json"
    )
    jsonl_output = (
        resolve_output_path(repo_root, args.jsonl_output)
        if args.jsonl_output
        else output_dir / f"{basename}.jsonl"
    )
    md_output = (
        resolve_output_path(repo_root, args.markdown_output)
        if args.markdown_output
        else output_dir / f"{basename}.md"
    )
    mmd_output = (
        resolve_output_path(repo_root, args.mermaid_output)
        if args.mermaid_output
        else output_dir / f"{basename}.mmd"
    )

    write_json_report(flow, json_output)
    write_jsonl(jsonl_output, as_list(flow.get("events")))
    write_text_report(build_markdown(flow), md_output)
    write_text_report(build_mermaid(flow), mmd_output)

    result = {
        "passed": True,
        "kind": "ia_carmine_runtime_flow_build",
        "stamp": stamp,
        "json": str(json_output),
        "jsonl": str(jsonl_output),
        "markdown": str(md_output),
        "mermaid": str(mmd_output),
        "summary": flow.get("summary"),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0
