"""CLI for heap runtime context closure."""

from __future__ import annotations

import argparse

from .common import DEFAULT_REQUEST
from .launcher import run_launcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request", default=DEFAULT_REQUEST)
    parser.add_argument(
        "--request-file",
        default="",
        help="UTF-8 file containing the operator request. Overrides --request when set.",
    )
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--budget-minutes", type=int, default=10)
    parser.add_argument("--max-iterations", type=int, default=6)
    parser.add_argument("--min-runtime-rounds", type=int, default=1)
    parser.add_argument("--min-proposal-iterations", type=int, default=0)
    parser.add_argument("--max-provider-revisions", type=int, default=6)
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=12,
        help="Gate planning rounds; must be high enough to complete base evidence before provider lanes.",
    )
    parser.add_argument("--allow-provider-generation", action="store_true")
    parser.add_argument("--provider-model", default="qwen3-coder:latest")
    parser.add_argument("--ollama-num-ctx", type=int, default=16384)
    parser.add_argument("--max-new-tokens", type=int, default=1200)
    parser.add_argument("--keep-alive", default="10m")
    parser.add_argument("--gpu0-iterations", type=int, default=16)
    parser.add_argument("--gpu0-min-seconds", type=float, default=0.1)
    parser.add_argument("--npu-micro-timeout-seconds", type=int, default=60)
    parser.add_argument("--npu-max-context-chars", type=int, default=8000)
    parser.add_argument("--npu-max-prompt-chars", type=int, default=1200)
    parser.add_argument("--npu-max-new-tokens", type=int, default=384)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--npu-device-workload-seconds", type=float, default=5.0)
    parser.add_argument("--npu-device-workload-iterations", type=int, default=5000)
    parser.add_argument("--documents-root", default="")
    parser.add_argument("--no-documents", action="store_true")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--preflight-timeout-seconds", type=int, default=120)
    parser.add_argument("--skip-startup-reload", action="store_true")
    parser.add_argument("--strict-startup-reload", action="store_true")
    parser.add_argument("--startup-max-memory-chars", type=int, default=64000)
    parser.add_argument("--startup-max-context-files", type=int, default=80)
    parser.add_argument("--startup-scan-context-files", type=int, default=10000)
    parser.add_argument("--startup-max-chars-per-file", type=int, default=12000)
    parser.add_argument(
        "--revision-context",
        default="auto_latest",
        help="Revision context path, 'auto_latest' or 'off'. Default auto-loads latest complete heap run context.",
    )
    parser.add_argument("--revision-context-max-tasks", type=int, default=12)
    return parser.parse_args()


def main() -> int:
    return run_launcher(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
