"""Models and direct CLI value maps for operator product launcher."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_RUN_LABEL = "spark_direct"

CLI_VALUE_KEYS = {
    "budget_minutes": "--budget-minutes",
    "max_iterations": "--max-iterations",
    "min_runtime_rounds": "--min-runtime-rounds",
    "min_proposal_iterations": "--min-proposal-iterations",
    "max_rounds": "--max-rounds",
    "files_per_round": "--files-per-round",
    "max_provider_revisions": "--max-provider-revisions",
    "timeout_seconds": "--timeout-seconds",
    "preflight_timeout_seconds": "--preflight-timeout-seconds",
    "provider_model": "--provider-model",
    "gpu1_base_url": "--gpu1-base-url",
    "gpu0_model": "--gpu0-model",
    "gpu0_base_url": "--gpu0-base-url",
    "gpu0_vulkan_visible_devices": "--gpu0-vulkan-visible-devices",
    "ollama_num_ctx": "--ollama-num-ctx",
    "ollama_gpu_layers": "--ollama-gpu-layers",
    "ollama_num_thread": "--ollama-num-thread",
    "ollama_context_candidates": "--ollama-context-candidates",
    "gpu0_model_dir": "--gpu0-model-dir",
    "npu_model_dir": "--npu-model-dir",
    "operator_gpu_observation": "--operator-gpu-observation",
    "max_new_tokens": "--max-new-tokens",
    "gpu0_max_new_tokens": "--gpu0-max-new-tokens",
    "keep_alive": "--keep-alive",
    "gpu0_iterations": "--gpu0-iterations",
    "gpu0_min_seconds": "--gpu0-min-seconds",
    "npu_micro_timeout_seconds": "--npu-micro-timeout-seconds",
    "npu_max_context_chars": "--npu-max-context-chars",
    "npu_max_prompt_chars": "--npu-max-prompt-chars",
    "npu_max_new_tokens": "--npu-max-new-tokens",
    "npu_device_workload_seconds": "--npu-device-workload-seconds",
    "npu_device_workload_iterations": "--npu-device-workload-iterations",
    "startup_max_memory_chars": "--startup-max-memory-chars",
    "startup_max_context_files": "--startup-max-context-files",
    "startup_scan_context_files": "--startup-scan-context-files",
    "startup_max_chars_per_file": "--startup-max-chars-per-file",
    "rag_db": "--rag-db",
    "rag_index_policy": "--rag-index-policy",
    "rag_embedding_endpoint": "--rag-embedding-endpoint",
    "rag_embedding_model": "--rag-embedding-model",
    "rag_ingest_batch_size": "--rag-ingest-batch-size",
    "rag_embed_smoke_batch_size": "--rag-embed-smoke-batch-size",
    "rag_chunk_min_chars": "--rag-chunk-min-chars",
    "rag_chunk_max_chars": "--rag-chunk-max-chars",
    "rag_chunk_overlap_chars": "--rag-chunk-overlap-chars",
    "rag_max_file_size": "--rag-max-file-size",
    "rag_top_k": "--rag-top-k",
    "rag_char_budget": "--rag-char-budget",
    "context_document_count": "--context-document-count",
    "context_document_preview_chars": "--context-document-preview-chars",
    "semantic_code_chunk_limit": "--semantic-code-chunk-limit",
    "semantic_code_chunk_preview_chars": "--semantic-code-chunk-preview-chars",
    "semantic_evidence_chunk_limit": "--semantic-evidence-chunk-limit",
    "memory_search_limit": "--memory-search-limit",
    "tool_catalog_limit": "--tool-catalog-limit",
    "revision_context_max_tasks": "--revision-context-max-tasks",
    "startup_provider_input_workers": "--startup-provider-input-workers",
    "startup_required_context_profile": "--startup-required-context-profile",
    "startup_operational_memory_query": "--startup-operational-memory-query",
    "startup_operational_memory_limit": "--startup-operational-memory-limit",
    "tool_inventory_roots": "--tool-inventory-roots",
    "semantic_path_boosts": "--semantic-path-boosts",
    "ai_context_pack_profile": "--ai-context-pack-profile",
    "code_interpreter_inputs": "--code-interpreter-inputs",
    "duplication_audit_roots": "--duplication-audit-roots",
    "provider_prompt_tool_catalog_cap": "--provider-prompt-tool-catalog-cap",
}

CLI_FLAG_KEYS = {
    "allow_provider_generation": "--allow-provider-generation",
    "require_ollama_gpu_residency": "--require-ollama-gpu-residency",
    "strict_provider_model": "--strict-provider-model",
    "allow_npu_device_workload": "--allow-npu-device-workload",
    "skip_startup_reload": "--skip-startup-reload",
    "strict_startup_reload": "--strict-startup-reload",
    "rag_allow_missing_embeddings": "--rag-allow-missing-embeddings",
    "no_documents": "--no-documents",
}


@dataclass
class LauncherConfig:
    repo_root: Path
    request_file: Path
    intermediate_root: Path
    final_root: Path
    run_label: str = DEFAULT_RUN_LABEL
    python_exe: str = ""
    stamp: str = ""
    revision_context: str | None = None
    budget_minutes: int | None = None
    max_iterations: int | None = None
    min_runtime_rounds: int | None = None
    min_proposal_iterations: int | None = None
    max_rounds: int | None = None
    files_per_round: int | None = None
    max_provider_revisions: int | None = None
    timeout_seconds: int | None = None
    preflight_timeout_seconds: int | None = None
    provider_model: str | None = None
    gpu1_base_url: str | None = None
    gpu0_model: str | None = None
    gpu0_base_url: str | None = None
    gpu0_vulkan_visible_devices: str | None = None
    ollama_num_ctx: int | None = None
    ollama_gpu_layers: str | None = None
    ollama_num_thread: int | None = None
    ollama_context_candidates: str | None = None
    strict_provider_model: bool | None = None
    gpu0_model_dir: str | None = None
    npu_model_dir: str | None = None
    operator_gpu_observation: str | None = None
    max_new_tokens: int | None = None
    gpu0_max_new_tokens: int | None = None
    keep_alive: str | None = None
    gpu0_iterations: int | None = None
    gpu0_min_seconds: float | None = None
    npu_micro_timeout_seconds: int | None = None
    npu_max_context_chars: int | None = None
    npu_max_prompt_chars: int | None = None
    npu_max_new_tokens: int | None = None
    npu_device_workload_seconds: float | None = None
    npu_device_workload_iterations: int | None = None
    startup_max_memory_chars: int | None = None
    startup_max_context_files: int | None = None
    startup_scan_context_files: int | None = None
    startup_max_chars_per_file: int | None = None
    rag_db: str | None = None
    rag_index_policy: str | None = None
    rag_embedding_endpoint: str | None = None
    rag_embedding_model: str | None = None
    rag_ingest_batch_size: int | None = None
    rag_embed_smoke_batch_size: int | None = None
    rag_chunk_min_chars: int | None = None
    rag_chunk_max_chars: int | None = None
    rag_chunk_overlap_chars: int | None = None
    rag_max_file_size: int | None = None
    rag_top_k: int | None = None
    rag_char_budget: int | None = None
    rag_allow_missing_embeddings: bool | None = None
    context_document_count: int | None = None
    context_document_preview_chars: int | None = None
    semantic_code_chunk_limit: int | None = None
    semantic_code_chunk_preview_chars: int | None = None
    semantic_evidence_chunk_limit: int | None = None
    memory_search_limit: int | None = None
    tool_catalog_limit: int | None = None
    revision_context_max_tasks: int | None = None
    startup_provider_input_workers: int | None = None
    startup_required_context_profile: str | None = None
    startup_operational_memory_query: str | None = None
    startup_operational_memory_limit: int | None = None
    tool_inventory_roots: str | None = None
    semantic_path_boosts: str | None = None
    ai_context_pack_profile: str | None = None
    code_interpreter_inputs: str | None = None
    duplication_audit_roots: str | None = None
    provider_prompt_tool_catalog_cap: int | None = None
    allow_provider_generation: bool | None = None
    require_ollama_gpu_residency: bool | None = None
    allow_npu_device_workload: bool | None = None
    skip_startup_reload: bool | None = None
    strict_startup_reload: bool | None = None
    no_documents: bool | None = None
    effective_universe_config: dict[str, Any] | None = None
    field_sources: dict[str, str] | None = None
