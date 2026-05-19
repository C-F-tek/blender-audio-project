"""Models and profile key maps for operator product launcher."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROFILE_FILE = "Tools/ai/run/profiles/heap_runtime_launcher_profiles.json"
DEFAULT_PROFILE = "deep_external_heap"

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
    profile_name: str = DEFAULT_PROFILE
    python_exe: str = ""
    stamp: str = ""
    revision_context: str = ""
    profiles_file: Path | None = None
    profile_overrides: dict[str, Any] | None = None
