"""CLI for heap runtime context closure."""

from __future__ import annotations

import argparse

from ia_carmine._shared.report_io import print_json_report

from .launcher import run_launcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request", default="")
    parser.add_argument(
        "--request-file",
        default="",
        help="UTF-8 file containing the operator request. Overrides --request when set.",
    )
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--objective", default="")
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
    parser.add_argument("--canonical-run-metadata", default="")
    parser.add_argument("--canonical-run-fingerprint", default="")
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
    parser.add_argument("--gpu0-ollama-num-ctx", type=int, default=None)
    parser.add_argument("--gpu0-iterations", type=int, default=None)
    parser.add_argument("--gpu0-min-seconds", type=float, default=None)
    parser.add_argument("--npu-micro-start-mode", default="")
    parser.add_argument("--npu-micro-timeout-seconds", type=int, default=None)
    parser.add_argument("--npu-final-wait-seconds", type=int, default=None)
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
    parser.add_argument("--rag-profile", default="")
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
    parser.add_argument("--max-degraded-lanes", type=int, default=None)
    parser.add_argument(
        "--revision-context",
        default="",
        help="Revision context path or 'off'. No implicit latest-run lookup is performed.",
    )
    parser.add_argument("--revision-context-max-tasks", type=int, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not str(args.request or "").strip() and not str(args.request_file or "").strip():
        print_json_report(
            {
                "schema_version": 1,
                "kind": "heap_context_closure_entrypoint_guard",
                "passed": False,
                "error": "operator_request_required",
                "required_flags": ["--request-file"],
                "canonical_entrypoint": "python -m ia_carmine.cli run",
            }
        )
        return 2
    if not str(args.output_dir or "").strip():
        print_json_report(
            {
                "schema_version": 1,
                "kind": "heap_context_closure_entrypoint_guard",
                "passed": False,
                "error": "output_dir_required",
                "required_flags": ["--output-dir"],
                "canonical_entrypoint": "python -m ia_carmine.cli run",
            }
        )
        return 2
    if not str(args.stamp or "").strip():
        print_json_report(
            {
                "schema_version": 1,
                "kind": "heap_context_closure_entrypoint_guard",
                "passed": False,
                "error": "stamp_required",
                "required_flags": ["--stamp"],
                "canonical_entrypoint": "python -m ia_carmine.cli run",
            }
        )
        return 2
    if not str(args.objective or "").strip():
        print_json_report(
            {
                "schema_version": 1,
                "kind": "heap_context_closure_entrypoint_guard",
                "passed": False,
                "error": "objective_required",
                "required_flags": ["--objective"],
                "canonical_entrypoint": "python -m ia_carmine.cli run",
            }
        )
        return 2
    if args.allow_provider_generation and (
        not str(args.canonical_run_metadata or "").strip()
        or not str(args.canonical_run_fingerprint or "").strip()
    ):
        print_json_report(
            {
                "schema_version": 1,
                "kind": "heap_context_closure_entrypoint_guard",
                "passed": False,
                "error": "canonical_run_config_required_for_provider_generation",
                "canonical_entrypoint": "python -m ia_carmine.cli run",
                "diagnostic_without_provider_generation_allowed": True,
            }
        )
        return 2
    return run_launcher(args)


if __name__ == "__main__":
    raise SystemExit(main())
