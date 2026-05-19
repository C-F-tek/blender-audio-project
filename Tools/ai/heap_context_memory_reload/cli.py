"""CLI for heap startup context and memory reload."""

from __future__ import annotations

import argparse
from pathlib import Path

from Tools.ai.heap_context_memory_reload.common import (
    now_stamp,
    read_request_file,
    resolve_project_python,
)
from Tools.ai.heap_context_memory_reload.runner import run_reload
from Tools.ai.heap_context_memory_reload.runner_state import ReloadRun


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request", default="")
    parser.add_argument(
        "--request-file",
        default="",
        help="Read startup request text from file to avoid long Windows command lines.",
    )
    parser.add_argument("--stamp", default="")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-memory-chars", type=int, default=64000)
    parser.add_argument("--max-context-files", type=int, default=80)
    parser.add_argument("--startup-scan-context-files", type=int, default=10000)
    parser.add_argument("--max-chars-per-file", type=int, default=12000)
    parser.add_argument(
        "--strict-ai-context-pack",
        action="store_true",
        help="Treat build_ai_context_pack failures as startup-blocking.",
    )
    parser.add_argument(
        "--strict-startup-reload",
        action="store_true",
        help="Return failure when any startup reload tool is degraded, even if artifacts are useful.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    request_text = (
        read_request_file(repo_root, args.request_file)
        if args.request_file
        else (args.request or "")
    )
    state = ReloadRun(
        args=args,
        repo_root=repo_root,
        stamp=args.stamp or now_stamp(),
        project_python=resolve_project_python(repo_root, args.python_exe),
        output_dir=Path(args.output_dir).resolve(),
        request_text=request_text,
    )
    return run_reload(state)
