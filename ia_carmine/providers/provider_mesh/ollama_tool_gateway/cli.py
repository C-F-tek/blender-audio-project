"""CLI for the Ollama tool gateway."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .common import (
    DEFAULT_MODEL,
    DEFAULT_OLLAMA_URL,
    DEFAULT_OUTPUT_DIR,
    MAX_FILE_CHARS,
    MAX_SEARCH_RESULTS,
    GatewayConfig,
    resolve_repo_path,
)
from .loop import run_loop, write_outputs

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a safe Ollama tool loop over IA-Carmine memory and files."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--model", default=os.environ.get("OLLAMA_TOOL_GATEWAY_MODEL", DEFAULT_MODEL)
    )
    parser.add_argument(
        "--ollama-url", default=os.environ.get("OLLAMA_HOST_URL", DEFAULT_OLLAMA_URL)
    )
    parser.add_argument("--task", required=True)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-rounds", type=int, default=6)
    parser.add_argument("--max-file-chars", type=int, default=MAX_FILE_CHARS)
    parser.add_argument("--max-search-results", type=int, default=MAX_SEARCH_RESULTS)
    parser.add_argument("--allow-output-read", action="store_true")
    args = parser.parse_args()
    if not str(args.model or "").strip():
        raise SystemExit("ollama_tool_gateway_model_explicit_required: pass --model")
    if not str(args.ollama_url or "").strip():
        raise SystemExit("ollama_tool_gateway_url_explicit_required: pass --ollama-url")

    repo_root = Path(args.repo_root).resolve()
    config = GatewayConfig(
        repo_root=repo_root,
        model=args.model,
        ollama_url=args.ollama_url,
        output_dir=resolve_repo_path(repo_root, args.output_dir),
        max_rounds=max(1, args.max_rounds),
        max_file_chars=max(1000, args.max_file_chars),
        max_search_results=max(1, args.max_search_results),
        allow_output_read=args.allow_output_read,
    )
    report = run_loop(config, args.task)
    outputs = write_outputs(config, report)
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "model": config.model,
                "outputs": outputs,
                "final_answer": report["final_answer"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2
