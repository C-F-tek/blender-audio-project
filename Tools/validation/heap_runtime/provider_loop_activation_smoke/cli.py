from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from Tools.validation.heap_runtime.provider_loop_hierarchy_checks import (
    run_provider_loop_hierarchy_checks,
)
from Tools.validation.heap_runtime.provider_loop_primary_evidence_checks import run_provider_loop_primary_evidence_checks
from Tools.validation.heap_runtime.provider_loop_native_tool_checks import (
    check_ollama_native_tool_lane_contract,
)
from Tools.validation.heap_runtime.provider_loop_tail_checks import (
    check_bounded_npu_micro_tasks,
    check_external_heap_health_report_filter,
    check_final_cleanup,
    check_gpu1_workload_absorption,
    check_rejected_gpu1_retry_contract,
)
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    checks = [
        _check_heap_loop_bootstrap_import_contract(repo_root),
        _check_independent_sidecar_watchdogs(repo_root),
        _check_boot_handoff(repo_root),
        _check_gpu0_command_contract(repo_root),
        check_ollama_native_tool_lane_contract(repo_root),
        _check_vulkan_identity_contract(repo_root),
        _check_provider_residency_lifecycle(repo_root),
        run_provider_loop_hierarchy_checks(repo_root),
        run_provider_loop_primary_evidence_checks(repo_root),
        check_gpu1_workload_absorption(repo_root),
        check_rejected_gpu1_retry_contract(repo_root),
        check_external_heap_health_report_filter(repo_root),
        check_bounded_npu_micro_tasks(repo_root),
        check_final_cleanup(repo_root),
        _check_gpu1_one_turn_gate_contract(repo_root),
        _check_provider_model_selection_policy(repo_root),
    ]
    errors = [error for check in checks for error in check.get("errors", [])]
    report = {
        "schema_version": 1,
        "kind": "provider_loop_activation_smoke",
        "repo_root": str(repo_root),
        "passed": not errors,
        "checks": checks,
        "errors": errors,
    }
    if args.output:
        output = _resolve(repo_root, args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2
def _check_heap_loop_bootstrap_import_contract(repo_root: Path) -> dict[str, Any]:
    loop_steps = _read(repo_root, "ia_carmine/runtime/heap_gate/loop_steps.py")
    errors: list[str] = []
    if "safe_dict(" in loop_steps and "safe_dict," not in loop_steps:
        errors.append("loop_steps.py uses safe_dict but does not import it from runtime_common")
    return {"name": "heap_loop_bootstrap_import_contract", "errors": errors}
def _check_independent_sidecar_watchdogs(repo_root: Path) -> dict[str, Any]:
    from ia_carmine.runtime.heap_gate.provider_time import build_provider_lane_time_contracts

    process_collection = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_process_collection.py")
    provider_execution = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_execution.py")
    run_loop = _read(repo_root, "ia_carmine/runtime/heap_gate/run_loop.py")
    args = SimpleNamespace(budget_minutes=5, timeout_seconds=600, npu_micro_timeout_seconds=60)
    contracts = build_provider_lane_time_contracts(args)
    errors: list[str] = []
    if "sidecar join timeout after primary closure owner completed" in process_collection:
        errors.append("provider process collection still kills sidecars after primary completion")
    if "sidecar_expired" in process_collection or "_primary_completed_perf" in process_collection:
        errors.append("provider process collection still computes primary-completion sidecar expiry")
    if contracts["gpu0_peer"].get("sidecar_join_after_primary_seconds") != 0:
        errors.append("GPU0 sidecar join after primary is not disabled")
    if contracts["npu_micro_task_auditor"].get("sidecar_join_after_primary_seconds") != 0:
        errors.append("NPU sidecar join after primary is not disabled")
    if "collect_provider_processes(\n                self,\n                prepared," in provider_execution:
        errors.append("provider loop still blocks GPU1 on full prepared sidecar join")
    if "poll_pending_provider_sidecars(round_id)" not in run_loop:
        errors.append("run loop does not poll async sidecars without blocking GPU1")
    if "pending_provider_sidecar_collections.append" not in provider_execution:
        errors.append("provider loop does not retain async sidecar process handles")
    return {"name": "independent_sidecar_watchdogs", "errors": errors}
def _check_boot_handoff(repo_root: Path) -> dict[str, Any]:
    coexistence = _read(repo_root, "ia_carmine/providers/provider_mesh/provider_role_coexistence/cli.py")
    preflight = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_coexistence_preflight.py")
    errors: list[str] = []
    for marker in ("--handoff-provider-loop", "deferred_until_provider_cleanup"):
        if marker not in coexistence:
            errors.append(f"provider role coexistence missing {marker}")
    if "--handoff-provider-loop" not in preflight:
        errors.append("runtime boot preflight does not request provider-loop handoff")
    return {"name": "boot_handoff", "errors": errors}


def _check_gpu0_command_contract(repo_root: Path) -> dict[str, Any]:
    gpu0 = _read(repo_root, "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py")
    specs = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_command_specs.py")
    metrics = _read(repo_root, "ia_carmine/runtime/heap_gate/run_loop_metrics.py")
    errors: list[str] = []
    if "--startup-manifest" not in gpu0:
        errors.append("GPU0 CLI does not accept --startup-manifest")
    if "--server-evidence" not in gpu0:
        errors.append("GPU0 CLI does not accept boot handoff server evidence")
    if "startup_manifest_context" not in gpu0:
        errors.append("GPU0 CLI does not ingest startup manifest context")
    if "--server-evidence" not in specs:
        errors.append("runtime GPU0 command does not pass boot handoff evidence")
    if "_gpu0_server_evidence_path" not in specs:
        errors.append("runtime GPU0 command does not inherit prior GPU0 server evidence")
    if "_gpu0_max_new_tokens" not in specs:
        errors.append("runtime GPU0 command does not bound peer max_new_tokens separately")
    if "--restart-gpu0-vulkan-server" in specs:
        errors.append("runtime GPU0 command still forces Vulkan server restart")
    if '"provider_model": gpu0_model' not in specs:
        errors.append("GPU0 spec does not expose provider_model for cleanup")
    if "--defer-unload" not in specs:
        errors.append("runtime GPU0 command does not defer model unload until cleanup")
    if "gpu0-sidecar-timeout-seconds" in specs or "gpu0_sidecar_timeout_seconds" in specs:
        errors.append("runtime added forbidden GPU0 sidecar timeout truncation flag")
    if "packet_review_only" not in specs or "sidecar_scope_mode" not in specs:
        errors.append("runtime sidecar command specs do not expose packet_review_only scope")
    for marker in (
        "gpu1_idle_after_primary_seconds",
        "sidecar_alone_after_gpu1_seconds",
        "gpu1_congruence_check_performed",
    ):
        if marker not in metrics:
            errors.append(f"provider lane metrics missing {marker}")
    if "args.defer_unload" not in gpu0:
        errors.append("GPU0 CLI does not support provider-cycle unload deferral")
    if "final synthesis" not in gpu0 or "complete alternate plan" not in gpu0:
        errors.append("GPU0 prompt does not forbid final synthesis / alternate full planning")
    if 'report.get("ollama_unload_verified")' in _extract_function(gpu0, "_gpu0_workload_verified"):
        errors.append("GPU0 workload verification still requires unload as proof")
    return {"name": "gpu0_command_contract", "errors": errors}




def _check_gpu1_one_turn_gate_contract(repo_root: Path) -> dict[str, Any]:
    helper = repo_root / "ia_carmine/runtime/heap_gate/gpu1_one_turn_gate.py"
    runtime_files = {
        "provider_execution": _read(repo_root, "ia_carmine/runtime/heap_gate/provider_execution.py"),
        "terminal": _read(repo_root, "ia_carmine/runtime/heap_gate/terminal_invariants.py"),
        "metrics": "\n".join(
            (
                _read(repo_root, "ia_carmine/runtime/heap_gate/run_loop_metrics.py"),
                _read(repo_root, "ia_carmine/runtime/heap_gate/run_loop_metric_helpers.py"),
            )
        ),
        "chat_loop": _read(repo_root, "ia_carmine/runtime/heap_gate/gpu1_native_tool_chat_loop.py"),
    }
    errors: list[str] = []
    if not helper.exists():
        errors.append("gpu1_one_turn_gate.py is missing")
    joined = "\n".join(runtime_files.values())
    forbidden = "Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight"
    if forbidden in joined:
        errors.append("runtime imports GPU1 preflight validator instead of production helper")
    if "gpu1_one_turn_runtime_gate" not in runtime_files["terminal"]:
        errors.append("terminal invariants do not require gpu1_one_turn_runtime_gate")
    if "gpu1_one_turn_runtime_gate_passed" not in runtime_files["metrics"]:
        errors.append("run_loop_metrics does not expose gpu1_one_turn_runtime_gate_passed")
    if "gpu1_one_turn_strict_fields_passed" not in runtime_files["metrics"]:
        errors.append("run_loop_metrics does not expose gpu1_one_turn_strict_fields_passed")
    helper_text = _read(repo_root, "ia_carmine/runtime/heap_gate/gpu1_one_turn_gate.py")
    if "gpu1_one_turn_broker_request_count" not in helper_text:
        errors.append("strict one-turn gate does not require broker request count")
    if "gpu1_one_turn_errors" not in helper_text:
        errors.append("strict one-turn gate does not reject recorded one-turn errors")
    if "build_gpu1_one_turn_runtime_gate" not in runtime_files["chat_loop"]:
        errors.append("gpu1_native_tool_chat_loop does not call production one-turn helper")
    if "skipped_gpu1_one_turn_gate_failed" not in runtime_files["provider_execution"]:
        errors.append("provider_execution does not block sidecars on one-turn gate failure")
    return {"name": "gpu1_one_turn_gate_contract", "errors": errors}


def _check_provider_model_selection_policy(repo_root: Path) -> dict[str, Any]:
    selection_source = _read(repo_root, "ia_carmine/_shared/ollama_provider_selection.py")
    command_specs = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_command_specs.py")
    coexistence = _read(repo_root, "ia_carmine/providers/provider_mesh/provider_role_coexistence/cli.py")
    ollama_config = _read(repo_root, "ia_carmine/providers/ollama/config.py")
    errors = _probe_provider_model_selection_policy()
    if "FALLBACK_ORDER" in selection_source or "fallback_order" in selection_source:
        errors.append("runtime provider selector still exposes fallback order")
    for rel, source in (
        ("ia_carmine/_shared/ollama_provider_selection.py", selection_source),
        ("ia_carmine/runtime/heap_gate/provider_command_specs.py", command_specs),
        ("ia_carmine/providers/provider_mesh/provider_role_coexistence/cli.py", coexistence),
        ("ia_carmine/providers/ollama/config.py", ollama_config),
    ):
        if "qwen2.5-coder:14b" in source:
            errors.append(f"{rel} still hardcodes qwen2.5-coder:14b")
    if "provider_model_selection_mismatch" not in command_specs:
        errors.append("provider_command_specs does not block explicit model mismatch")
    if "provider_model_explicit_required" not in coexistence:
        errors.append("provider role coexistence does not require explicit GPU1 model")
    return {"name": "provider_model_selection_policy", "errors": errors}


def _probe_provider_model_selection_policy() -> list[str]:
    from ia_carmine._shared import ollama_provider_selection as selection

    old_inventory = selection.ollama_model_inventory
    old_gpus = selection.nvidia_gpu_inventory
    inventory_payload = {
        "qwen3-coder:30b": {"size_bytes": 1},
        "qwen2.5-coder:14b": {"size_bytes": 1},
    }
    selection.ollama_model_inventory = lambda: dict(inventory_payload)
    selection.nvidia_gpu_inventory = lambda: [
        {"name": "NVIDIA", "uuid": "GPU-smoke", "memory_total_mib": 100000, "memory_free_mib": 100000}
    ]
    errors: list[str] = []
    try:
        explicit = selection.select_ollama_provider_model(
            "qwen3-coder:30b",
            ["qwen2.5-coder:14b", "qwen3-coder:30b"],
            num_ctx=8192,
            context_candidates="8192",
            strict=False,
        )
        if explicit.get("selected_provider_model") != "qwen3-coder:30b":
            errors.append(f"explicit model was not selected exactly: {explicit}")
        if explicit.get("model_switch_allowed") is not False:
            errors.append("explicit provider model still allows model switch")
        if explicit.get("model_selection_policy") != "explicit_provider_model_exact":
            errors.append("explicit provider model policy is not exact")
        inventory_payload = {"qwen2.5-coder:14b": {"size_bytes": 1}}
        missing = selection.select_ollama_provider_model(
            "qwen3-coder:30b",
            ["qwen2.5-coder:14b"],
            num_ctx=8192,
            context_candidates="8192",
            strict=False,
        )
        if missing.get("blocked_reason") != "provider_model_explicit_not_installed":
            errors.append(f"missing explicit model did not block correctly: {missing}")
        inventory_payload = {
            "qwen3-coder:30b": {"size_bytes": 1},
            "qwen2.5-coder:14b": {"size_bytes": 1},
        }
        auto = selection.select_ollama_provider_model(
            "auto",
            ["qwen2.5-coder:14b", "qwen3-coder:30b"],
            num_ctx=8192,
            context_candidates="8192",
            strict=False,
        )
        if auto.get("blocked_reason") != "provider_model_explicit_required":
            errors.append(f"auto provider model did not block as explicit-required: {auto}")
    finally:
        selection.ollama_model_inventory = old_inventory
        selection.nvidia_gpu_inventory = old_gpus
    return errors




def _check_vulkan_identity_contract(repo_root: Path) -> dict[str, Any]:
    vulkan = _read(repo_root, "ia_carmine/providers/ollama/vulkan_devices.py")
    context = _read(repo_root, "ia_carmine/providers/provider_mesh/TOOL_CONTEXT.md")
    errors: list[str] = []
    if 'vendor == "0x8086"' not in vulkan:
        errors.append("Vulkan GPU0 auto-selection is not pinned to Intel vendor identity")
    if "Windows Task Manager numbering" not in context:
        errors.append("provider mesh context does not document Windows/Vulkan index mismatch")
    if "GGML_VK_VISIBLE_DEVICES" not in context:
        errors.append("provider mesh context does not document resolved Vulkan visible device")
    return {"name": "vulkan_identity_contract", "errors": errors}


def _check_provider_residency_lifecycle(repo_root: Path) -> dict[str, Any]:
    provider_time = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_time.py")
    heap_context = _read(repo_root, "ia_carmine/runtime/heap_gate/TOOL_CONTEXT.md")
    mesh_context = _read(repo_root, "ia_carmine/providers/provider_mesh/TOOL_CONTEXT.md")
    errors: list[str] = []
    for marker in (
        "keep_gpu1_gpu0_loaded_across_provider_revisions_until_production_cycle_cleanup",
        "ollama_model_unload_only_at_provider_production_cycle_cleanup",
    ):
        if marker not in provider_time:
            errors.append(f"provider time contract missing residency marker {marker}")
    if "GPU1 must remain resident for the whole provider production cycle" not in heap_context:
        errors.append("heap gate context does not document GPU1 production-cycle residency")
    if "model unload and GPU0 `11435` shutdown are final cleanup" not in mesh_context:
        errors.append("provider mesh context does not document final cleanup residency")
    return {"name": "provider_residency_lifecycle", "errors": errors}


def _read(repo_root: Path, rel: str) -> str:
    return (repo_root / rel).read_text(encoding="utf-8", errors="replace")


def _extract_function(text: str, name: str) -> str:
    marker = f"def {name}("
    start = text.find(marker)
    if start < 0:
        return ""
    next_def = text.find("\ndef ", start + len(marker))
    return text[start:] if next_def < 0 else text[start:next_def]


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


if __name__ == "__main__":
    raise SystemExit(main())
