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
    parser.add_argument("--revision-context", default="")
    parser.add_argument("--code-product", default="")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--run-and-review", action="store_true")
    parser.add_argument("--review-code-product", action="store_true")
    parser.add_argument("--apply-safe", action="store_true")
    parser.add_argument("--confirm", default="")
    parser.add_argument("--require-all-integrated", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=None)
    parser.add_argument("--budget-minutes", type=int, default=None)
    parser.add_argument("--max-iterations", type=int, default=None)
    parser.add_argument("--min-runtime-rounds", type=int, default=None)
    parser.add_argument("--min-proposal-iterations", type=int, default=None)
    parser.add_argument("--max-rounds", type=int, default=None)
    parser.add_argument("--files-per-round", type=int, default=None)
    parser.add_argument("--max-provider-revisions", type=int, default=None)
    parser.add_argument("--preflight-timeout-seconds", type=int, default=None)
    parser.add_argument("--provider-model", default=None)
    parser.add_argument("--gpu1-base-url", default=None)
    parser.add_argument("--gpu0-model", default=None)
    parser.add_argument("--gpu0-base-url", default=None)
    parser.add_argument("--gpu0-vulkan-visible-devices", default=None)
    parser.add_argument("--strict-provider-model", action="store_true")
    parser.add_argument("--ollama-num-ctx", type=int, default=None)
    parser.add_argument("--gpu0-ollama-num-ctx", type=int, default=None)
    parser.add_argument("--ollama-gpu-layers", "--ollama-num-gpu", dest="ollama_gpu_layers", default=None)
    parser.add_argument("--ollama-num-thread", type=int, default=None)
    parser.add_argument("--ollama-context-candidates", default=None)
    parser.add_argument("--gpu0-model-dir", default=None)
    parser.add_argument("--npu-model-dir", default=None)
    parser.add_argument("--operator-gpu-observation", default=None)
    parser.add_argument("--max-new-tokens", type=int, default=None)
    parser.add_argument("--gpu0-max-new-tokens", type=int, default=None)
    parser.add_argument("--keep-alive", default=None)
    parser.add_argument("--gpu0-iterations", type=int, default=None)
    parser.add_argument("--gpu0-min-seconds", type=float, default=None)
    parser.add_argument("--npu-micro-timeout-seconds", type=int, default=None)
    parser.add_argument("--npu-max-context-chars", type=int, default=None)
    parser.add_argument("--npu-max-prompt-chars", type=int, default=None)
    parser.add_argument("--npu-max-new-tokens", type=int, default=None)
    parser.add_argument("--npu-device-workload-seconds", type=float, default=None)
    parser.add_argument("--npu-device-workload-iterations", type=int, default=None)
    parser.add_argument("--startup-max-memory-chars", type=int, default=None)
    parser.add_argument("--startup-max-context-files", type=int, default=None)
    parser.add_argument("--startup-scan-context-files", type=int, default=None)
    parser.add_argument("--startup-max-chars-per-file", type=int, default=None)
    parser.add_argument("--rag-db", default=None)
    parser.add_argument("--rag-index-policy", choices=("auto", "always", "never"), default=None)
    parser.add_argument("--rag-embedding-endpoint", default=None)
    parser.add_argument("--rag-embedding-model", default=None)
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
    parser.add_argument("--revision-context-max-tasks", type=int, default=None)
    parser.add_argument("--startup-provider-input-workers", type=int, default=None)
    parser.add_argument("--startup-required-context-profile", default=None)
    parser.add_argument("--startup-operational-memory-query", default=None)
    parser.add_argument("--startup-operational-memory-limit", type=int, default=None)
    parser.add_argument("--tool-inventory-roots", default=None)
    parser.add_argument("--semantic-path-boosts", default=None)
    parser.add_argument("--ai-context-pack-profile", default=None)
    parser.add_argument("--code-interpreter-inputs", default=None)
    parser.add_argument("--duplication-audit-roots", default=None)
    parser.add_argument("--provider-prompt-tool-catalog-cap", type=int, default=None)
    parser.add_argument("--allow-provider-generation", action="store_true", default=False)
    parser.add_argument("--require-ollama-gpu-residency", action="store_true", default=False)
    parser.add_argument("--allow-npu-device-workload", action="store_true", default=False)
    parser.add_argument("--skip-startup-reload", action="store_true", default=False)
    parser.add_argument("--strict-startup-reload", action="store_true", default=False)
    parser.add_argument("--no-documents", action="store_true", default=False)
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
        min_runtime_rounds=args.min_runtime_rounds,
        min_proposal_iterations=args.min_proposal_iterations,
        max_rounds=args.max_rounds,
        files_per_round=args.files_per_round,
        max_provider_revisions=args.max_provider_revisions,
        timeout_seconds=args.timeout_seconds,
        preflight_timeout_seconds=args.preflight_timeout_seconds,
        provider_model=args.provider_model,
        gpu1_base_url=args.gpu1_base_url,
        gpu0_model=args.gpu0_model,
        gpu0_base_url=args.gpu0_base_url,
        gpu0_vulkan_visible_devices=args.gpu0_vulkan_visible_devices,
        strict_provider_model=args.strict_provider_model,
        ollama_num_ctx=args.ollama_num_ctx,
        gpu0_ollama_num_ctx=args.gpu0_ollama_num_ctx,
        ollama_gpu_layers=args.ollama_gpu_layers,
        ollama_num_thread=args.ollama_num_thread,
        ollama_context_candidates=args.ollama_context_candidates,
        gpu0_model_dir=args.gpu0_model_dir,
        npu_model_dir=args.npu_model_dir,
        operator_gpu_observation=args.operator_gpu_observation,
        max_new_tokens=args.max_new_tokens,
        gpu0_max_new_tokens=args.gpu0_max_new_tokens,
        keep_alive=args.keep_alive,
        gpu0_iterations=args.gpu0_iterations,
        gpu0_min_seconds=args.gpu0_min_seconds,
        npu_micro_timeout_seconds=args.npu_micro_timeout_seconds,
        npu_max_context_chars=args.npu_max_context_chars,
        npu_max_prompt_chars=args.npu_max_prompt_chars,
        npu_max_new_tokens=args.npu_max_new_tokens,
        npu_device_workload_seconds=args.npu_device_workload_seconds,
        npu_device_workload_iterations=args.npu_device_workload_iterations,
        startup_max_memory_chars=args.startup_max_memory_chars,
        startup_max_context_files=args.startup_max_context_files,
        startup_scan_context_files=args.startup_scan_context_files,
        startup_max_chars_per_file=args.startup_max_chars_per_file,
        rag_db=args.rag_db,
        rag_index_policy=args.rag_index_policy,
        rag_embedding_endpoint=args.rag_embedding_endpoint,
        rag_embedding_model=args.rag_embedding_model,
        rag_ingest_batch_size=args.rag_ingest_batch_size,
        rag_embed_smoke_batch_size=args.rag_embed_smoke_batch_size,
        rag_chunk_min_chars=args.rag_chunk_min_chars,
        rag_chunk_max_chars=args.rag_chunk_max_chars,
        rag_chunk_overlap_chars=args.rag_chunk_overlap_chars,
        rag_max_file_size=args.rag_max_file_size,
        rag_top_k=args.rag_top_k,
        rag_char_budget=args.rag_char_budget,
        rag_allow_missing_embeddings=args.rag_allow_missing_embeddings,
        context_document_count=args.context_document_count,
        context_document_preview_chars=args.context_document_preview_chars,
        semantic_code_chunk_limit=args.semantic_code_chunk_limit,
        semantic_code_chunk_preview_chars=args.semantic_code_chunk_preview_chars,
        semantic_evidence_chunk_limit=args.semantic_evidence_chunk_limit,
        memory_search_limit=args.memory_search_limit,
        tool_catalog_limit=args.tool_catalog_limit,
        revision_context_max_tasks=args.revision_context_max_tasks,
        startup_provider_input_workers=args.startup_provider_input_workers,
        startup_required_context_profile=args.startup_required_context_profile,
        startup_operational_memory_query=args.startup_operational_memory_query,
        startup_operational_memory_limit=args.startup_operational_memory_limit,
        tool_inventory_roots=args.tool_inventory_roots,
        semantic_path_boosts=args.semantic_path_boosts,
        ai_context_pack_profile=args.ai_context_pack_profile,
        code_interpreter_inputs=args.code_interpreter_inputs,
        duplication_audit_roots=args.duplication_audit_roots,
        provider_prompt_tool_catalog_cap=args.provider_prompt_tool_catalog_cap,
        allow_provider_generation=args.allow_provider_generation,
        require_ollama_gpu_residency=args.require_ollama_gpu_residency,
        allow_npu_device_workload=args.allow_npu_device_workload,
        skip_startup_reload=args.skip_startup_reload,
        strict_startup_reload=args.strict_startup_reload,
        no_documents=args.no_documents,
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
