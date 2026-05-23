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
    parser.add_argument("--budget-minutes", type=int, default=None)
    parser.add_argument("--max-iterations", type=int, default=None)
    parser.add_argument("--min-runtime-rounds", type=int, default=None)
    parser.add_argument("--min-proposal-iterations", type=int, default=None)
    parser.add_argument("--max-provider-revisions", type=int, default=None)
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=None,
        help="Gate planning rounds; must be high enough to complete base evidence before provider lanes.",
    )
    parser.add_argument("--files-per-round", type=int, default=None)
    parser.add_argument("--allow-provider-generation", action="store_true")
    parser.add_argument("--operator-intent", action="store_true")
    parser.add_argument("--require-ollama-gpu-residency", action="store_true", default=False)
    parser.add_argument("--provider-model", default="")
    parser.add_argument("--gpu1-base-url", default="")
    parser.add_argument("--gpu0-model", default="")
    parser.add_argument("--gpu0-base-url", default="")
    parser.add_argument("--gpu0-vulkan-visible-devices", default="")
    parser.add_argument("--strict-provider-model", action="store_true")
    parser.add_argument("--ollama-num-ctx", type=int, default=None)
    parser.add_argument("--ollama-gpu-layers", "--ollama-num-gpu", dest="ollama_gpu_layers", default="")
    parser.add_argument("--ollama-num-thread", type=int, default=None)
    parser.add_argument("--ollama-context-candidates", default="")
    parser.add_argument("--gpu0-model-dir", default="")
    parser.add_argument("--npu-model-dir", default="")
    parser.add_argument("--operator-gpu-observation", default="")
    parser.add_argument("--max-new-tokens", type=int, default=None)
    parser.add_argument("--gpu0-max-new-tokens", type=int, default=None)
    parser.add_argument("--keep-alive", default="")
    parser.add_argument("--gpu0-iterations", type=int, default=None)
    parser.add_argument("--gpu0-min-seconds", type=float, default=None)
    parser.add_argument("--npu-micro-timeout-seconds", type=int, default=None)
    parser.add_argument("--npu-max-context-chars", type=int, default=None)
    parser.add_argument("--npu-max-prompt-chars", type=int, default=None)
    parser.add_argument("--npu-max-new-tokens", type=int, default=None)
    parser.add_argument(
        "--allow-npu-device-workload",
        action="store_true",
        default=False,
        help="Opt in to bounded NPU device workload; semantic NPU audit still runs without it.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=None)
    parser.add_argument("--npu-device-workload-seconds", type=float, default=None)
    parser.add_argument("--npu-device-workload-iterations", type=int, default=None)
    parser.add_argument("--documents-root", default="")
    parser.add_argument("--no-documents", action="store_true")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--preflight-timeout-seconds", type=int, default=None)
    parser.add_argument("--skip-startup-reload", action="store_true")
    parser.add_argument("--strict-startup-reload", action="store_true")
    parser.add_argument("--startup-max-memory-chars", type=int, default=None)
    parser.add_argument("--startup-max-context-files", type=int, default=None)
    parser.add_argument("--startup-scan-context-files", type=int, default=None)
    parser.add_argument("--startup-max-chars-per-file", type=int, default=None)
    parser.add_argument("--rag-db", default="")
    parser.add_argument("--rag-index-policy", choices=("auto", "always", "never"), default="")
    parser.add_argument("--rag-embedding-endpoint", default="")
    parser.add_argument("--rag-embedding-model", default="")
    parser.add_argument("--rag-ingest-batch-size", type=int, default=None)
    parser.add_argument("--rag-embed-smoke-batch-size", type=int, default=None)
    parser.add_argument("--rag-chunk-min-chars", type=int, default=None)
    parser.add_argument("--rag-chunk-max-chars", type=int, default=None)
    parser.add_argument("--rag-chunk-overlap-chars", type=int, default=None)
    parser.add_argument("--rag-max-file-size", type=int, default=None)
    parser.add_argument("--rag-top-k", type=int, default=None)
    parser.add_argument("--rag-char-budget", type=int, default=None)
    parser.add_argument("--rag-allow-missing-embeddings", action="store_true")
    parser.add_argument("--context-document-count", type=int, default=None)
    parser.add_argument("--context-document-preview-chars", type=int, default=None)
    parser.add_argument("--semantic-code-chunk-limit", type=int, default=None)
    parser.add_argument("--semantic-code-chunk-preview-chars", type=int, default=None)
    parser.add_argument("--semantic-evidence-chunk-limit", type=int, default=None)
    parser.add_argument("--memory-search-limit", type=int, default=None)
    parser.add_argument("--tool-catalog-limit", type=int, default=None)
    parser.add_argument("--startup-provider-input-workers", type=int, default=None)
    parser.add_argument("--startup-required-context-profile", default="")
    parser.add_argument(
        "--startup-operational-memory-query",
        default="",
    )
    parser.add_argument("--startup-operational-memory-limit", type=int, default=None)
    parser.add_argument("--tool-inventory-roots", default="")
    parser.add_argument("--semantic-path-boosts", default="")
    parser.add_argument("--ai-context-pack-profile", default="")
    parser.add_argument("--code-interpreter-inputs", default="")
    parser.add_argument("--duplication-audit-roots", default="")
    parser.add_argument("--provider-prompt-tool-catalog-cap", type=int, default=None)
    parser.add_argument(
        "--revision-context",
        default="",
        help="Revision context path, 'auto_latest' or 'off'. Default auto-loads latest complete heap run context.",
    )
    parser.add_argument("--revision-context-max-tasks", type=int, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_launcher(args)


if __name__ == "__main__":
    raise SystemExit(main())
