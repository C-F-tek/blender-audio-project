from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    checks = [
        _check_independent_sidecar_watchdogs(repo_root),
        _check_boot_handoff(repo_root),
        _check_gpu0_command_contract(repo_root),
        _check_vulkan_identity_contract(repo_root),
        _check_provider_residency_lifecycle(repo_root),
        _check_gpu1_workload_absorption(repo_root),
        _check_external_heap_health_report_filter(repo_root),
        _check_bounded_npu_micro_tasks(repo_root),
        _check_final_cleanup(repo_root),
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


def _check_independent_sidecar_watchdogs(repo_root: Path) -> dict[str, Any]:
    from ia_carmine.runtime.heap_gate.provider_time import build_provider_lane_time_contracts

    process_collection = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_process_collection.py")
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
    errors: list[str] = []
    if "--startup-manifest" not in gpu0:
        errors.append("GPU0 CLI does not accept --startup-manifest")
    if "--server-evidence" not in gpu0:
        errors.append("GPU0 CLI does not accept boot handoff server evidence")
    if "startup_manifest_context" not in gpu0:
        errors.append("GPU0 CLI does not ingest startup manifest context")
    if "--server-evidence" not in specs:
        errors.append("runtime GPU0 command does not pass boot handoff evidence")
    if "_gpu0_max_new_tokens" not in specs:
        errors.append("runtime GPU0 command does not bound peer max_new_tokens separately")
    if "--restart-gpu0-vulkan-server" in specs:
        errors.append("runtime GPU0 command still forces Vulkan server restart")
    if '"provider_model": gpu0_model' not in specs:
        errors.append("GPU0 spec does not expose provider_model for cleanup")
    if "--defer-unload" not in specs:
        errors.append("runtime GPU0 command does not defer model unload until cleanup")
    if "args.defer_unload" not in gpu0:
        errors.append("GPU0 CLI does not support provider-cycle unload deferral")
    if 'report.get("ollama_unload_verified")' in _extract_function(gpu0, "_gpu0_workload_verified"):
        errors.append("GPU0 workload verification still requires unload as proof")
    return {"name": "gpu0_command_contract", "errors": errors}


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


def _check_gpu1_workload_absorption(repo_root: Path) -> dict[str, Any]:
    local_probe = _read(repo_root, "ia_carmine/providers/provider_mesh/local_provider_probe/cli.py")
    commands = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_commands.py")
    provider_context = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_context.py")
    provider_prompt_text = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_prompt_text.py")
    errors: list[str] = []
    if "mirror_single_provider_lane" not in local_probe or "args.run_ollama" not in local_probe:
        errors.append("GPU1 provider wrapper still mirrors only replight lanes")
    for marker in ("response_text", "target_files", "validation_commands", "provider_work_verified"):
        if marker not in local_probe:
            errors.append(f"local provider probe does not mirror {marker}")
    if "lane_report_lane in {\"ollama\", lane}" not in commands:
        errors.append("runtime summarizer does not absorb lane-specific Ollama reports")
    if "_empty_report_value" not in commands:
        errors.append("runtime summarizer cannot overwrite empty top-level wrapper fields")
    if "--defer-unload" not in _read(repo_root, "ia_carmine/runtime/heap_gate/provider_command_specs.py"):
        errors.append("GPU1 provider loop does not defer model unload until cleanup")
    if "runtime_file_refs/SOURCE_PATH_ALLOWLIST_CONTRACT" not in provider_context:
        errors.append("GPU1 prompt does not anchor target files to runtime_file_refs allowlist")
    if "basename o path ricordati ma non allowlisted" not in provider_prompt_text:
        errors.append("GPU1 pointer protocol does not forbid remembered basename targets")
    return {"name": "gpu1_workload_absorption", "errors": errors}


def _check_external_heap_health_report_filter(repo_root: Path) -> dict[str, Any]:
    graph = _read(repo_root, "ia_carmine/runtime/external_heap/block_pointer_manifest/provider_graph.py")
    errors: list[str] = []
    if "provider_role_coexistence" not in graph:
        errors.append("external heap provider graph may still count boot coexistence as provider work")
    if "provider_replight" not in graph or "replight_mode" not in graph:
        errors.append("external heap provider graph may still count replight health reports as provider work")
    return {"name": "external_heap_health_report_filter", "errors": errors}


def _check_bounded_npu_micro_tasks(repo_root: Path) -> dict[str, Any]:
    npu = (
        _read(repo_root, "ia_carmine/_shared/npu_micro_task_companion_cli.py")
        + "\n"
        + _read(repo_root, "ia_carmine/_shared/npu_micro_task_contract.py")
    )
    errors: list[str] = []
    for marker in (
        "section_presence_audit",
        "target_reference_audit",
        "validation_command_audit",
        "risk_guardrail_audit",
        "NPU_DONE",
        "NPU_REJECT",
        "NPU_NO_ACTION",
        "NPU_TIMEOUT_BOUNDARY",
        "MICRO_TASK=",
        "CHECKED=",
        "FINDINGS=",
        "DECISION=",
        "REASON=",
    ):
        if marker not in npu:
            errors.append(f"NPU micro-task contract missing {marker}")
    return {"name": "bounded_npu_micro_tasks", "errors": errors}


def _check_final_cleanup(repo_root: Path) -> dict[str, Any]:
    launcher = _read(repo_root, "ia_carmine/runtime/heap_context_closure/launcher.py")
    common = _read(repo_root, "ia_carmine/runtime/heap_context_closure/common.py")
    errors: list[str] = []
    if "heap command completed provider cleanup" not in launcher:
        errors.append("launcher does not run provider cleanup after successful heap command")
    if "provider_base_url" not in common or "_stop_gpu0_vulkan_server" not in common:
        errors.append("provider cleanup does not know GPU0 base URL/server stop")
    return {"name": "final_cleanup", "errors": errors}


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
