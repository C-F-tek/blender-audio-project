"""Explicit CLI-only Universo IA run config resolver."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any

OPTIONAL_FIELDS = {
    "strict_provider_model",
    "ollama_num_thread",
    "gpu0_model_dir",
    "operator_gpu_observation",
    "rag_allow_missing_embeddings",
    "skip_startup_reload",
    "strict_startup_reload",
    "no_documents",
}


@dataclass
class UniverseRunConfig:
    budget_minutes: int | None = None
    max_iterations: int | None = None
    min_runtime_rounds: int | None = None
    min_proposal_iterations: int | None = None
    max_rounds: int | None = None
    files_per_round: int | None = None
    max_provider_revisions: int | None = None
    timeout_seconds: int | None = None
    preflight_timeout_seconds: int | None = None
    revision_context: str | None = None
    revision_context_max_tasks: int | None = None
    provider_model: str | None = None
    strict_provider_model: bool | None = None
    gpu1_base_url: str | None = None
    gpu0_model: str | None = None
    gpu0_base_url: str | None = None
    gpu0_vulkan_visible_devices: str | None = None
    ollama_num_ctx: int | None = None
    gpu0_ollama_num_ctx: int | None = None
    ollama_gpu_layers: str | None = None
    ollama_num_thread: int | None = None
    ollama_context_candidates: str | None = None
    gpu0_model_dir: str | None = None
    npu_model_dir: str | None = None
    operator_gpu_observation: str | None = None
    max_new_tokens: int | None = None
    gpu0_max_new_tokens: int | None = None
    keep_alive: str | None = None
    gpu0_iterations: int | None = None
    gpu0_min_seconds: float | None = None
    npu_micro_start_mode: str | None = None
    npu_micro_timeout_seconds: int | None = None
    npu_final_wait_seconds: int | None = None
    npu_max_context_chars: int | None = None
    npu_max_prompt_chars: int | None = None
    npu_max_new_tokens: int | None = None
    max_degraded_lanes: int | None = None
    npu_device_workload_seconds: float | None = None
    npu_device_workload_iterations: int | None = None
    startup_max_memory_chars: int | None = None
    startup_max_context_files: int | None = None
    startup_scan_context_files: int | None = None
    startup_max_chars_per_file: int | None = None
    startup_provider_input_workers: int | None = None
    startup_required_context_profile: str | None = None
    startup_operational_memory_query: str | None = None
    startup_operational_memory_limit: int | None = None
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


INT_FIELDS = {
    "budget_minutes",
    "max_iterations",
    "min_runtime_rounds",
    "min_proposal_iterations",
    "max_rounds",
    "files_per_round",
    "max_provider_revisions",
    "timeout_seconds",
    "preflight_timeout_seconds",
    "revision_context_max_tasks",
    "ollama_num_ctx",
    "gpu0_ollama_num_ctx",
    "ollama_num_thread",
    "max_new_tokens",
    "gpu0_max_new_tokens",
    "gpu0_iterations",
    "npu_final_wait_seconds",
    "npu_micro_timeout_seconds",
    "npu_max_context_chars",
    "npu_max_prompt_chars",
    "npu_max_new_tokens",
    "max_degraded_lanes",
    "npu_device_workload_iterations",
    "startup_max_memory_chars",
    "startup_max_context_files",
    "startup_scan_context_files",
    "startup_max_chars_per_file",
    "startup_provider_input_workers",
    "startup_operational_memory_limit",
    "rag_ingest_batch_size",
    "rag_embed_smoke_batch_size",
    "rag_chunk_min_chars",
    "rag_chunk_max_chars",
    "rag_chunk_overlap_chars",
    "rag_max_file_size",
    "rag_top_k",
    "rag_char_budget",
    "context_document_count",
    "context_document_preview_chars",
    "semantic_code_chunk_limit",
    "semantic_code_chunk_preview_chars",
    "semantic_evidence_chunk_limit",
    "memory_search_limit",
    "tool_catalog_limit",
    "provider_prompt_tool_catalog_cap",
}
FLOAT_FIELDS = {"gpu0_min_seconds", "npu_device_workload_seconds"}
BOOL_FIELDS = {
    "strict_provider_model",
    "rag_allow_missing_embeddings",
    "allow_provider_generation",
    "require_ollama_gpu_residency",
    "allow_npu_device_workload",
    "skip_startup_reload",
    "strict_startup_reload",
    "no_documents",
}


@dataclass
class ResolvedUniverseRunConfig:
    config: UniverseRunConfig
    field_sources: dict[str, str]

    def as_payload(self) -> dict[str, Any]:
        return {
            "effective_universe_config": asdict(self.config),
            "field_sources": dict(self.field_sources),
        }


def config_field_names() -> set[str]:
    return {field.name for field in fields(UniverseRunConfig)}


def _coerce_bool(value: Any, *, field_name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "y", "on"}:
            return True
        if lowered in {"0", "false", "no", "n", "off"}:
            return False
    raise SystemExit(f"invalid boolean for {field_name}: {value!r}")


def _coerce_value(field_name: str, current_value: Any, value: Any) -> Any:
    if value is None:
        return None
    if field_name in BOOL_FIELDS:
        return _coerce_bool(value, field_name=field_name)
    if field_name in INT_FIELDS:
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise SystemExit(f"invalid integer for {field_name}: {value!r}") from exc
    if field_name in FLOAT_FIELDS:
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise SystemExit(f"invalid float for {field_name}: {value!r}") from exc
    return str(value)


def resolve_universe_config(
    *,
    repo_root: Path,
    args: Any,
    provided_dests: set[str],
) -> ResolvedUniverseRunConfig:
    _ = repo_root
    config = UniverseRunConfig()
    sources = {field: "unresolved_missing" for field in config_field_names()}
    profile_sources = getattr(args, "_profile_applied_fields", {}) or {}
    if not isinstance(profile_sources, dict):
        profile_sources = {}

    configured_dests = (provided_dests | set(str(key) for key in profile_sources)) & config_field_names()
    for dest in sorted(configured_dests):
        value = getattr(args, dest)
        current = getattr(config, dest)
        setattr(config, dest, _coerce_value(dest, current, value))
        sources[dest] = "cli_arg" if dest in provided_dests else str(profile_sources.get(dest) or "profile")

    missing = sorted(
        field
        for field, source in sources.items()
        if source == "unresolved_missing" and field not in OPTIONAL_FIELDS
    )
    if missing:
        raise SystemExit(
            "missing explicit Universo IA run parameter(s); provide CLI flags: "
            f"{', '.join(missing)}"
        )
    for field in OPTIONAL_FIELDS:
        if sources.get(field) == "unresolved_missing":
            sources[field] = "optional_unset"

    return ResolvedUniverseRunConfig(
        config=config,
        field_sources=sources,
    )


def apply_resolved_config_to_args(args: Any, resolved: ResolvedUniverseRunConfig) -> None:
    for key, value in asdict(resolved.config).items():
        setattr(args, key, value)


def launcher_config_metadata(resolved: ResolvedUniverseRunConfig) -> dict[str, Any]:
    return {
        "effective_universe_config": asdict(resolved.config),
        "field_sources": dict(resolved.field_sources),
    }
