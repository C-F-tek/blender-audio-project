"""CLI for operator product launcher core."""

from __future__ import annotations

import argparse
from pathlib import Path

from ia_carmine._shared.report_io import print_json_report

from .io_utils import now_stamp
from .models import DEFAULT_RUN_LABEL, LauncherConfig
from .direct_command import build_heap_command, resolve_config, run_dir_for
from .runner import analyze_code_product, run_heap, run_operator_lab


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--run-label", default=DEFAULT_RUN_LABEL)
    parser.add_argument(
        "--intermediate-root", default="output/validation/operator_product_launcher"
    )
    parser.add_argument("--final-root", default="")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--revision-context", default="auto_latest")
    parser.add_argument("--code-product", default="")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--run-and-review", action="store_true")
    parser.add_argument("--review-code-product", action="store_true")
    parser.add_argument("--apply-safe", action="store_true")
    parser.add_argument("--confirm", default="")
    parser.add_argument("--require-all-integrated", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--budget-minutes", type=int, default=5)
    parser.add_argument("--max-iterations", type=int, default=2)
    parser.add_argument("--max-rounds", type=int, default=8)
    parser.add_argument("--max-provider-revisions", type=int, default=2)
    parser.add_argument("--preflight-timeout-seconds", type=int, default=90)
    parser.add_argument("--provider-model", default="auto")
    parser.add_argument("--strict-provider-model", action="store_true")
    parser.add_argument("--ollama-context-candidates", default="8192,4096")
    parser.add_argument("--gpu0-model-dir", default="")
    parser.add_argument("--npu-model-dir", default="")
    parser.add_argument("--operator-gpu-observation", default="")
    parser.add_argument("--max-new-tokens", type=int, default=900)
    parser.add_argument("--gpu0-max-new-tokens", type=int, default=0)
    parser.add_argument("--allow-provider-generation", action="store_true", default=True)
    parser.add_argument("--startup-max-memory-chars", type=int, default=0)
    parser.add_argument("--startup-max-context-files", type=int, default=0)
    parser.add_argument("--startup-scan-context-files", type=int, default=0)
    parser.add_argument("--startup-max-chars-per-file", type=int, default=0)
    parser.add_argument("--context-document-count", type=int, default=0)
    parser.add_argument("--context-document-preview-chars", type=int, default=0)
    parser.add_argument("--semantic-code-chunk-limit", type=int, default=0)
    parser.add_argument("--semantic-code-chunk-preview-chars", type=int, default=0)
    parser.add_argument("--semantic-evidence-chunk-limit", type=int, default=0)
    parser.add_argument("--memory-search-limit", type=int, default=0)
    parser.add_argument("--tool-catalog-limit", type=int, default=0)
    return parser.parse_args()


def build_config(args: argparse.Namespace, repo_root: Path, stamp: str) -> LauncherConfig:
    final_root = args.final_root or str(
        Path.home() / "Documents" / f"aicarmine_operator_launcher_{stamp}"
    )
    request_file = (
        Path(args.request_file) if args.request_file else repo_root / "docs" / "README.md"
    )
    return LauncherConfig(
        repo_root=repo_root,
        request_file=request_file,
        intermediate_root=Path(args.intermediate_root),
        final_root=Path(final_root),
        run_label=args.run_label,
        python_exe=args.python_exe,
        stamp=stamp,
        revision_context=args.revision_context,
        budget_minutes=args.budget_minutes,
        max_iterations=args.max_iterations,
        max_rounds=args.max_rounds,
        max_provider_revisions=args.max_provider_revisions,
        timeout_seconds=args.timeout_seconds,
        preflight_timeout_seconds=args.preflight_timeout_seconds,
        provider_model=args.provider_model,
        strict_provider_model=args.strict_provider_model,
        ollama_context_candidates=args.ollama_context_candidates,
        gpu0_model_dir=args.gpu0_model_dir,
        npu_model_dir=args.npu_model_dir,
        operator_gpu_observation=args.operator_gpu_observation,
        max_new_tokens=args.max_new_tokens,
        gpu0_max_new_tokens=args.gpu0_max_new_tokens,
        startup_max_memory_chars=args.startup_max_memory_chars or 32000,
        startup_max_context_files=args.startup_max_context_files or 48,
        startup_scan_context_files=args.startup_scan_context_files or 48,
        startup_max_chars_per_file=args.startup_max_chars_per_file or 8000,
        context_document_count=args.context_document_count or 24,
        context_document_preview_chars=args.context_document_preview_chars or 1200,
        semantic_code_chunk_limit=args.semantic_code_chunk_limit or 32,
        semantic_code_chunk_preview_chars=args.semantic_code_chunk_preview_chars or 1400,
        semantic_evidence_chunk_limit=args.semantic_evidence_chunk_limit or 24,
        memory_search_limit=args.memory_search_limit or 12,
        tool_catalog_limit=args.tool_catalog_limit or 80,
        allow_provider_generation=args.allow_provider_generation,
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or now_stamp()
    config = build_config(args, repo_root, stamp)
    if args.apply_safe and args.confirm != "safe_apply":
        raise SystemExit("--apply-safe requires --confirm safe_apply")
    if args.run_and_review and args.apply_safe:
        raise SystemExit("--apply-safe is a separate code-product action, not part of run-and-review")
    if args.run_and_review:
        report = run_operator_lab(config, timeout=None)
        print_json_report(report)
        return 0 if report.get("passed") else 2
    if args.run:
        report = run_heap(config, timeout=None)
        print_json_report(report)
        return 0 if report.get("passed") else 2
    code_product = Path(args.code_product)
    if not args.code_product and args.request_file:
        code_product = Path(args.request_file)
    if args.review_code_product or args.apply_safe:
        output_dir = run_dir_for(resolve_config(config))
        report = analyze_code_product(
            repo_root,
            code_product,
            output_dir,
            apply_safe=args.apply_safe,
            require_all_integrated=args.require_all_integrated,
        )
        print_json_report(report)
        return 0 if report.get("passed") else 2
    command = build_heap_command(config)
    print_json_report({"command": command, "parameters_source": "direct_cli"})
    return 0
