from __future__ import annotations

from typing import Any

from ia_carmine.product.operator_product_core import LauncherConfig, OperatorProductController
from ia_carmine.product.operator_product_core.direct_command import resolve_config, run_dir_for
from ia_carmine.product.operator_product_core.public_documents import default_public_documents_root
from ia_carmine._shared.ollama_provider_selection import provider_model_policy_fields
from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import context_hierarchy_payload
from ia_carmine.runtime.run.dry_run_policy import dry_run_contract_policy


def _parameters_source(field_sources: dict[str, Any]) -> str:
    values = {
        str(value)
        for value in field_sources.values()
        if str(value or "").strip() and str(value or "").strip() != "optional_unset"
    }
    has_cli = "cli_arg" in values
    has_profile = any(value.startswith("profile:") for value in values)
    if has_cli and has_profile:
        return "profile_plus_explicit_cli_surface_with_visible_effective_config"
    if has_profile:
        return "profile_surface_with_visible_effective_config"
    if has_cli:
        return "explicit_cli_surface_with_visible_effective_config"
    return "unresolved_config_surface"


def dry_run_report(config: LauncherConfig) -> dict[str, Any]:
    cfg = resolve_config(config)
    model_policy = provider_model_policy_fields(str(cfg.provider_model or "auto"))
    command = OperatorProductController(config).build_command()
    effective_universe_config = cfg.effective_universe_config or {}
    field_sources = cfg.field_sources or {}
    effective_config = context_hierarchy_payload(
        cfg,
        gpu1_ctx=cfg.ollama_num_ctx,
        field_sources=field_sources,
    ).get("operator_effective_config", {})
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
        "provider_model_explicit": str(cfg.provider_model or "auto").lower() != "auto",
        "provider_model": str(cfg.provider_model or "auto"),
        "model_switch_allowed": bool(model_policy["model_switch_allowed"]),
        "model_switch_performed": False,
        "model_selection_policy": model_policy["model_selection_policy"],
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
        "parameters_source": _parameters_source(field_sources),
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
        "direct_parameters": dict(effective_universe_config),
        **dry_run_contract_policy(
            gpu1_base_url=cfg.gpu1_base_url,
            gpu0_base_url=cfg.gpu0_base_url,
            keep_alive=cfg.keep_alive,
            field_sources=field_sources,
        ),
    }
