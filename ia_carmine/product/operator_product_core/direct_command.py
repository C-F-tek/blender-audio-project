"""Direct heap command construction for the operator product launcher."""

from __future__ import annotations

import sys
from pathlib import Path

from .cli_contract import build_heap_runtime_argv, provider_flags_from_selection
from .io_utils import now_stamp
from .models import CLI_FLAG_KEYS, CLI_VALUE_KEYS, LauncherConfig


def resolve_project_python(repo_root: Path, explicit: str = "") -> str:
    if explicit:
        return str(Path(explicit).resolve())
    for candidate in (
        repo_root / ".venv" / "Scripts" / "python.exe",
        repo_root / "venv" / "Scripts" / "python.exe",
        repo_root / ".venv314" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate.resolve())
    return sys.executable


def resolve_config(config: LauncherConfig) -> LauncherConfig:
    repo_root = config.repo_root.resolve()
    request_file = config.request_file
    if not request_file.is_absolute():
        request_file = repo_root / request_file
    intermediate_root = config.intermediate_root
    if not intermediate_root.is_absolute():
        intermediate_root = repo_root / intermediate_root
    final_root = config.final_root
    if not final_root.is_absolute():
        final_root = repo_root / final_root
    return LauncherConfig(
        repo_root=repo_root,
        request_file=request_file.resolve(strict=False),
        intermediate_root=intermediate_root.resolve(strict=False),
        final_root=final_root.resolve(strict=False),
        run_label=config.run_label,
        python_exe=resolve_project_python(repo_root, config.python_exe),
        stamp=config.stamp or now_stamp(),
        revision_context=config.revision_context,
        budget_minutes=config.budget_minutes,
        max_iterations=config.max_iterations,
        min_runtime_rounds=config.min_runtime_rounds,
        min_proposal_iterations=config.min_proposal_iterations,
        max_rounds=config.max_rounds,
        files_per_round=config.files_per_round,
        max_provider_revisions=config.max_provider_revisions,
        timeout_seconds=config.timeout_seconds,
        preflight_timeout_seconds=config.preflight_timeout_seconds,
        provider_model=config.provider_model,
        gpu1_base_url=config.gpu1_base_url,
        gpu0_model=config.gpu0_model,
        gpu0_base_url=config.gpu0_base_url,
        gpu0_vulkan_visible_devices=config.gpu0_vulkan_visible_devices,
        ollama_num_ctx=config.ollama_num_ctx,
        gpu0_ollama_num_ctx=config.gpu0_ollama_num_ctx,
        ollama_gpu_layers=config.ollama_gpu_layers,
        ollama_num_thread=config.ollama_num_thread,
        ollama_context_candidates=config.ollama_context_candidates,
        strict_provider_model=config.strict_provider_model,
        gpu0_model_dir=config.gpu0_model_dir,
        npu_model_dir=config.npu_model_dir,
        operator_gpu_observation=config.operator_gpu_observation,
        max_new_tokens=config.max_new_tokens,
        gpu0_max_new_tokens=config.gpu0_max_new_tokens,
        keep_alive=config.keep_alive,
        gpu0_iterations=config.gpu0_iterations,
        gpu0_min_seconds=config.gpu0_min_seconds,
        npu_micro_timeout_seconds=config.npu_micro_timeout_seconds,
        npu_max_context_chars=config.npu_max_context_chars,
        npu_max_prompt_chars=config.npu_max_prompt_chars,
        npu_max_new_tokens=config.npu_max_new_tokens,
        npu_device_workload_seconds=config.npu_device_workload_seconds,
        npu_device_workload_iterations=config.npu_device_workload_iterations,
        startup_max_memory_chars=config.startup_max_memory_chars,
        startup_max_context_files=config.startup_max_context_files,
        startup_scan_context_files=config.startup_scan_context_files,
        startup_max_chars_per_file=config.startup_max_chars_per_file,
        rag_db=config.rag_db,
        rag_index_policy=config.rag_index_policy,
        rag_embedding_endpoint=config.rag_embedding_endpoint,
        rag_embedding_model=config.rag_embedding_model,
        rag_ingest_batch_size=config.rag_ingest_batch_size,
        rag_embed_smoke_batch_size=config.rag_embed_smoke_batch_size,
        rag_chunk_min_chars=config.rag_chunk_min_chars,
        rag_chunk_max_chars=config.rag_chunk_max_chars,
        rag_chunk_overlap_chars=config.rag_chunk_overlap_chars,
        rag_max_file_size=config.rag_max_file_size,
        rag_top_k=config.rag_top_k,
        rag_char_budget=config.rag_char_budget,
        rag_allow_missing_embeddings=config.rag_allow_missing_embeddings,
        context_document_count=config.context_document_count,
        context_document_preview_chars=config.context_document_preview_chars,
        semantic_code_chunk_limit=config.semantic_code_chunk_limit,
        semantic_code_chunk_preview_chars=config.semantic_code_chunk_preview_chars,
        semantic_evidence_chunk_limit=config.semantic_evidence_chunk_limit,
        memory_search_limit=config.memory_search_limit,
        tool_catalog_limit=config.tool_catalog_limit,
        revision_context_max_tasks=config.revision_context_max_tasks,
        startup_provider_input_workers=config.startup_provider_input_workers,
        startup_required_context_profile=config.startup_required_context_profile,
        startup_operational_memory_query=config.startup_operational_memory_query,
        startup_operational_memory_limit=config.startup_operational_memory_limit,
        tool_inventory_roots=config.tool_inventory_roots,
        semantic_path_boosts=config.semantic_path_boosts,
        ai_context_pack_profile=config.ai_context_pack_profile,
        code_interpreter_inputs=config.code_interpreter_inputs,
        duplication_audit_roots=config.duplication_audit_roots,
        provider_prompt_tool_catalog_cap=config.provider_prompt_tool_catalog_cap,
        allow_provider_generation=config.allow_provider_generation,
        require_ollama_gpu_residency=config.require_ollama_gpu_residency,
        allow_npu_device_workload=config.allow_npu_device_workload,
        skip_startup_reload=config.skip_startup_reload,
        strict_startup_reload=config.strict_startup_reload,
        no_documents=config.no_documents,
        effective_universe_config=config.effective_universe_config,
        field_sources=config.field_sources,
    )


def run_dir_for(config: LauncherConfig) -> Path:
    return config.intermediate_root / f"heap_context_closure_{config.stamp}"


def build_heap_command(config: LauncherConfig) -> list[str]:
    cfg = resolve_config(config)
    command = [
        cfg.python_exe,
        "-m",
        "ia_carmine.cli",
        "heap_context_closure",
        "--repo-root",
        str(cfg.repo_root),
        "--python-exe",
        cfg.python_exe,
        "--request-file",
        str(cfg.request_file),
        "--stamp",
        cfg.stamp,
        "--output-dir",
        str(run_dir_for(cfg)),
        "--documents-root",
        str(cfg.final_root),
        "--revision-context",
        str(cfg.revision_context or ""),
    ]
    for key, flag in CLI_VALUE_KEYS.items():
        value = getattr(cfg, key)
        if value not in ("", None):
            command.extend([flag, str(value)])
    for key, flag in CLI_FLAG_KEYS.items():
        if bool(getattr(cfg, key)):
            command.append(flag)
    return build_heap_runtime_argv(
        command,
        provider_flags_from_selection(bool(cfg.allow_provider_generation)),
    )
