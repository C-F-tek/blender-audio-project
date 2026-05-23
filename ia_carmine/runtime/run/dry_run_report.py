from __future__ import annotations

from typing import Any

from ia_carmine.product.operator_product_core import LauncherConfig, OperatorProductController
from ia_carmine.product.operator_product_core.direct_command import resolve_config, run_dir_for
from ia_carmine.product.operator_product_core.public_documents import default_public_documents_root
from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import context_hierarchy_payload
from ia_carmine.runtime.run.dry_run_policy import dry_run_contract_policy


def dry_run_report(config: LauncherConfig) -> dict[str, Any]:
    cfg = resolve_config(config)
    command = OperatorProductController(config).build_command()
    effective_universe_config = cfg.effective_universe_config or {}
    field_sources = cfg.field_sources or {}
    effective_config = context_hierarchy_payload(cfg, gpu1_ctx=cfg.ollama_num_ctx).get(
        "operator_effective_config", {}
    )
    return {
        "schema_version": 1,
        "kind": "operator_universe_run_plan",
        "canonical_entrypoint": "python -m ia_carmine.cli run",
        "runtime": "heap_context_closure",
        "single_product_entry": True,
        "parallel_product_entry": False,
        "smoke_product_entry": False,
        "execution_performed": False,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "provider_generation_required": True,
        "provider_model_required": True,
        "provider_model_default_auto": False,
        "requested_provider_model": str(cfg.provider_model or "auto"),
        "provider_model_explicit": str(cfg.provider_model or "auto") != "auto",
        "provider_model": str(cfg.provider_model or "auto"),
        "effective_universe_config": effective_universe_config,
        "field_sources": field_sources,
        "expanded_heap_command": command,
        "strict_provider_model": bool(cfg.strict_provider_model),
        "gpu1_base_url": cfg.gpu1_base_url,
        "gpu0_model": cfg.gpu0_model,
        "gpu0_base_url": cfg.gpu0_base_url,
        "gpu0_vulkan_visible_devices": cfg.gpu0_vulkan_visible_devices,
        "ollama_gpu_layers_requested": str(cfg.ollama_gpu_layers or "all"),
        "ollama_context_candidates": cfg.ollama_context_candidates,
        "gpu0_model_dir": cfg.gpu0_model_dir,
        "npu_model_dir": cfg.npu_model_dir,
        "operator_gpu_observation": cfg.operator_gpu_observation,
        "require_ollama_gpu_residency": True,
        "full_gpu_residency_required": True,
        "provider_keep_alive": cfg.keep_alive,
        "run_label": cfg.run_label,
        "parameters_source": "explicit_cli_surface_with_visible_effective_config",
        "request_file": str(cfg.request_file),
        "intermediate_run_dir": str(run_dir_for(cfg)),
        "final_root": str(cfg.final_root),
        "public_documents_root": str(default_public_documents_root(cfg.stamp)),
        "internal_runtime": "ia_carmine.product.operator_product_core.OperatorProductController",
        "heap_runtime": "ia_carmine.runtime.heap_context_closure",
        "gate_runtime": "ia_carmine.runtime.heap_runtime.completeness_gate.HeapRuntimeCompletenessGate",
        "command": command,
        "operator_effective_provider_config": effective_config,
        "provider_generation_requested": "--allow-provider-generation" in command,
        "provider_replight_required": True,
        "provider_replight_failure_policy": "close_immediately_blocked_with_reason",
        "provider_role_coexistence_required": True,
        "provider_role_coexistence_policy": (
            "GPU1 Ollama, GPU0 Ollama/Vulkan and NPU OpenVINO must be alive in "
            "the same provider window before the heap pointer loop treats them "
            "as one provider universe."
        ),
        "provider_compute_policy": {
            "gpu1_planner": "ollama_100_percent_gpu_residency_required",
            "gpu0_peer": "ollama_gpu0_vulkan_model_loop_required",
            "npu_micro_task_auditor": "openvino_NPU_device_workload_and_model_loop_required",
            "cpu": "runtime_only_not_provider",
        },
        "codex_failure_counter_markdown_updates": {"performed": False, "reason": "dry_run"},
        "direct_parameters": {
            key: getattr(cfg, key)
            for key in [
                "budget_minutes",
                "max_iterations",
                "min_runtime_rounds",
                "min_proposal_iterations",
                "max_rounds",
                "files_per_round",
                "max_provider_revisions",
                "timeout_seconds",
                "preflight_timeout_seconds",
                "ollama_gpu_layers",
                "gpu1_base_url",
                "gpu0_model",
                "gpu0_base_url",
                "gpu0_vulkan_visible_devices",
                "ollama_num_ctx",
                "gpu0_ollama_num_ctx",
                "ollama_num_thread",
                "ollama_context_candidates",
                "max_new_tokens",
                "gpu0_max_new_tokens",
                "keep_alive",
                "startup_max_memory_chars",
                "startup_max_context_files",
                "startup_scan_context_files",
                "startup_max_chars_per_file",
                "rag_db",
                "rag_index_policy",
                "rag_embedding_endpoint",
                "rag_embedding_model",
                "rag_ingest_batch_size",
                "rag_embed_smoke_batch_size",
                "rag_chunk_min_chars",
                "rag_chunk_max_chars",
                "rag_chunk_overlap_chars",
                "rag_max_file_size",
                "rag_top_k",
                "rag_char_budget",
                "rag_allow_missing_embeddings",
                "context_document_count",
                "context_document_preview_chars",
                "semantic_code_chunk_limit",
                "semantic_code_chunk_preview_chars",
                "semantic_evidence_chunk_limit",
                "memory_search_limit",
                "tool_catalog_limit",
                "startup_provider_input_workers",
                "startup_required_context_profile",
                "startup_operational_memory_query",
                "startup_operational_memory_limit",
                "tool_inventory_roots",
                "semantic_path_boosts",
                "ai_context_pack_profile",
                "code_interpreter_inputs",
                "duplication_audit_roots",
                "provider_prompt_tool_catalog_cap",
            ]
        },
        **dry_run_contract_policy(
            gpu1_base_url=cfg.gpu1_base_url,
            gpu0_base_url=cfg.gpu0_base_url,
            keep_alive=cfg.keep_alive,
        ),
    }
