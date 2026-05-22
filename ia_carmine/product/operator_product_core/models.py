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
    "max_provider_revisions": "--max-provider-revisions",
    "timeout_seconds": "--timeout-seconds",
    "preflight_timeout_seconds": "--preflight-timeout-seconds",
    "provider_model": "--provider-model",
    "ollama_num_ctx": "--ollama-num-ctx",
    "ollama_gpu_layers": "--ollama-gpu-layers",
    "ollama_num_thread": "--ollama-num-thread",
    "ollama_context_candidates": "--ollama-context-candidates",
    "gpu0_model_dir": "--gpu0-model-dir",
    "npu_model_dir": "--npu-model-dir",
    "operator_gpu_observation": "--operator-gpu-observation",
    "max_new_tokens": "--max-new-tokens",
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
    "context_document_count": "--context-document-count",
    "context_document_preview_chars": "--context-document-preview-chars",
    "semantic_code_chunk_limit": "--semantic-code-chunk-limit",
    "semantic_code_chunk_preview_chars": "--semantic-code-chunk-preview-chars",
    "semantic_evidence_chunk_limit": "--semantic-evidence-chunk-limit",
    "memory_search_limit": "--memory-search-limit",
    "tool_catalog_limit": "--tool-catalog-limit",
    "revision_context_max_tasks": "--revision-context-max-tasks",
}

CLI_FLAG_KEYS = {
    "allow_provider_generation": "--allow-provider-generation",
    "require_ollama_gpu_residency": "--require-ollama-gpu-residency",
    "strict_provider_model": "--strict-provider-model",
    "allow_npu_device_workload": "--allow-npu-device-workload",
    "skip_startup_reload": "--skip-startup-reload",
    "strict_startup_reload": "--strict-startup-reload",
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
    revision_context: str = "auto_latest"
    budget_minutes: int = 5
    max_iterations: int = 2
    min_runtime_rounds: int = 1
    min_proposal_iterations: int = 0
    max_rounds: int = 8
    max_provider_revisions: int = 2
    timeout_seconds: int = 600
    preflight_timeout_seconds: int = 90
    provider_model: str = "auto"
    ollama_num_ctx: int = 16384
    ollama_gpu_layers: str = "all"
    ollama_num_thread: int | None = None
    ollama_context_candidates: str = "8192,4096"
    strict_provider_model: bool = False
    gpu0_model_dir: str = ""
    npu_model_dir: str = ""
    operator_gpu_observation: str = ""
    max_new_tokens: int = 900
    keep_alive: str = "120s"
    gpu0_iterations: int = 16
    gpu0_min_seconds: float = 0.1
    npu_micro_timeout_seconds: int = 60
    npu_max_context_chars: int = 8000
    npu_max_prompt_chars: int = 1200
    npu_max_new_tokens: int = 384
    npu_device_workload_seconds: float = 3.0
    npu_device_workload_iterations: int = 2500
    startup_max_memory_chars: int = 32000
    startup_max_context_files: int = 48
    startup_scan_context_files: int = 48
    startup_max_chars_per_file: int = 8000
    context_document_count: int = 24
    context_document_preview_chars: int = 1200
    semantic_code_chunk_limit: int = 32
    semantic_code_chunk_preview_chars: int = 1400
    semantic_evidence_chunk_limit: int = 24
    memory_search_limit: int = 12
    tool_catalog_limit: int = 80
    revision_context_max_tasks: int = 6
    allow_provider_generation: bool = True
    require_ollama_gpu_residency: bool = True
    allow_npu_device_workload: bool = True
    skip_startup_reload: bool = False
    strict_startup_reload: bool = False
    no_documents: bool = False
