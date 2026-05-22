from __future__ import annotations

from typing import Any

from ia_carmine.product.operator_product_core import LauncherConfig, OperatorProductController
from ia_carmine.product.operator_product_core.direct_command import resolve_config, run_dir_for
from ia_carmine.product.operator_product_core.public_documents import default_public_documents_root
from ia_carmine.runtime.run.dry_run_policy import dry_run_contract_policy


def dry_run_report(config: LauncherConfig) -> dict[str, Any]:
    cfg = resolve_config(config)
    command = OperatorProductController(config).build_command()
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
        "provider_model_required": False,
        "provider_model_default_auto": True,
        "requested_provider_model": str(cfg.provider_model or "auto"),
        "provider_model_explicit": str(cfg.provider_model or "auto") != "auto",
        "provider_model": str(cfg.provider_model or "auto"),
        "strict_provider_model": bool(cfg.strict_provider_model),
        "ollama_gpu_layers_requested": str(cfg.ollama_gpu_layers or "all"),
        "ollama_context_candidates": cfg.ollama_context_candidates,
        "gpu0_model_dir": cfg.gpu0_model_dir,
        "npu_model_dir": cfg.npu_model_dir,
        "operator_gpu_observation": cfg.operator_gpu_observation,
        "require_ollama_gpu_residency": True,
        "full_gpu_residency_required": True,
        "run_label": cfg.run_label,
        "parameters_source": "ia_carmine.runtime.run explicit CLI defaults/flags",
        "request_file": str(cfg.request_file),
        "intermediate_run_dir": str(run_dir_for(cfg)),
        "final_root": str(cfg.final_root),
        "public_documents_root": str(default_public_documents_root(cfg.stamp)),
        "internal_runtime": "ia_carmine.product.operator_product_core.OperatorProductController",
        "heap_runtime": "ia_carmine.runtime.heap_context_closure",
        "gate_runtime": "ia_carmine.runtime.heap_runtime.completeness_gate.HeapRuntimeCompletenessGate",
        "command": command,
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
                "max_provider_revisions",
                "timeout_seconds",
                "preflight_timeout_seconds",
                "ollama_gpu_layers",
                "ollama_num_thread",
                "ollama_context_candidates",
                "startup_max_memory_chars",
                "startup_max_context_files",
                "startup_scan_context_files",
                "startup_max_chars_per_file",
                "context_document_count",
                "context_document_preview_chars",
                "semantic_code_chunk_limit",
                "semantic_code_chunk_preview_chars",
                "semantic_evidence_chunk_limit",
                "memory_search_limit",
                "tool_catalog_limit",
            ]
        },
        **dry_run_contract_policy(),
    }
