#!/usr/bin/env python3
"""Validate Ollama GPU0/Vulkan and OpenVINO NPU peer topology in runtime."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def exists(repo_root: Path, rel: str) -> bool:
    return (repo_root / rel).exists()


def has(text: str, token: str) -> bool:
    return token in text


def ordered_tokens(text: str, *tokens: str) -> bool:
    positions = [text.find(token) for token in tokens]
    return all(position >= 0 for position in positions) and positions == sorted(positions)


def ordered_lane_specs(text: str) -> bool:
    return ordered_tokens(
        text,
        '"lane": "gpu1_planner"',
        '"lane": "gpu0_peer"',
        '"lane": "npu_micro_task_auditor"',
    ) or ordered_tokens(
        text,
        '"lane": GPU1_LANE',
        '"lane": GPU0_LANE',
        '"lane": NPU_LANE',
    )


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = ["# Ollama GPU0 / OpenVINO NPU Topology Contract", "", f"- Passed: `{report.get('passed')}`", ""]
    for key in report.get("check_order") or []:
        lines.append(f"- `{key}`: `{report.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    return write_text_report("\n".join(lines) + "\n", output)


def build_report(repo_root: Path) -> dict[str, Any]:
    workloads = read_text(repo_root / "ia_carmine/providers/provider_mesh/hardware_capability/workloads.py")
    gpu0_companion = read_text(repo_root / "ia_carmine/providers/provider_mesh/gpu0_companion_task_lane/cli.py")
    gpu0_worker = read_text(repo_root / "ia_carmine/providers/provider_mesh/gpu0_peer_companion_worker/cli.py")
    npu_companion = read_text(repo_root / "ia_carmine/providers/provider_mesh/npu_micro_task_companion_report/cli.py")
    npu_companion_shared = read_text(repo_root / "ia_carmine/_shared/npu_micro_task_companion_cli.py")
    npu_shared = read_text(repo_root / "ia_carmine/providers/npu/provider_mesh/_shared/npu_runtime.py")
    provider_loop = read_text(repo_root / "ia_carmine/_shared/provider_tool_loop.py")
    provider_commands = "\n".join(
        (
            read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_commands.py"),
            read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_command_specs.py"),
            read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_time.py"),
        )
    )
    provider_execution = read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_execution.py")
    provider_absorption = read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_report_absorption.py")
    provider_collection = read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_process_collection.py")
    provider_runtime = "\n".join((provider_execution, provider_absorption, provider_collection))
    provider_teamwork_packet = read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_teamwork_packet.py")
    heap_run_loop = read_text(repo_root / "ia_carmine/runtime/heap_gate/run_loop.py")
    gpu0_workload = read_text(repo_root / "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py")
    blackboard = read_text(repo_root / "ia_carmine/runtime/provider_runtime_blackboard/cli.py")
    blackboard_common = read_text(repo_root / "ia_carmine/runtime/provider_runtime_blackboard/common.py")
    blackboard_heap = read_text(repo_root / "ia_carmine/runtime/provider_runtime_blackboard/heap.py")
    broker_bridge = read_text(repo_root / "ia_carmine/runtime/provider_runtime_blackboard/broker_bridge/cli.py")
    budget = read_text(repo_root / "ia_carmine/runtime/heap_provider/budget_governor/cli.py")
    invocation = read_text(repo_root / "ia_carmine/runtime/heap_provider/invocation_contract/cli.py")
    profiles = read_text(repo_root / "ia_carmine/runtime/run/profiles/heap_runtime_launcher_profiles.json")
    runtime_mesh = read_text(repo_root / "Tools/validation/real_product/runtime_mesh_contract/cli.py")

    checks: dict[str, bool] = {
        "ollama_gpu0_vulkan_policy_required": has(
            read_text(repo_root / "ia_carmine/providers/provider_mesh/hardware_capability/policy.py"),
            "ollama_gpu0_vulkan",
        )
        and has(provider_commands, "ollama_gpu0_vulkan_required_openvino_gpu0_forbidden"),
        "gpu1_reserved_from_openvino_workload": has(
            read_text(repo_root / "ia_carmine/providers/provider_mesh/hardware_capability/policy.py"),
            "reserved_for_cuda_ollama",
        ),
        "gpu0_peer_command_is_support_lane": exists(
            repo_root, "ia_carmine/providers/provider_mesh/gpu0_companion_task_lane/cli.py"
        )
        and has(gpu0_companion, "companion_worker")
        and has(gpu0_companion, "semantic_evidence_chunks")
        and has(gpu0_worker, "ollama_gpu0_peer_report"),
        "npu_micro_uses_runtime_context_and_tool_broker": exists(
            repo_root, "ia_carmine/providers/provider_mesh/npu_micro_task_companion_report/cli.py"
        )
        and has(npu_companion, "npu_preflight")
        and has(provider_loop, "native_tool_loop_device")
        and has(provider_loop, "tool_calls"),
        "runtime_heap_records_peer_events": exists(repo_root, "ia_carmine/runtime/provider_runtime_blackboard/cli.py")
        and has(blackboard_common, "broker_request")
        and has(blackboard_common, "product_signal")
        and has(blackboard_heap, "append_event")
        and has(broker_bridge, "provider_runtime_broker_bridge"),
        "budget_governor_defines_lanes": exists(
            repo_root, "ia_carmine/runtime/heap_provider/budget_governor/cli.py"
        )
        and has(budget, "provider_lanes")
        and has(budget, "gpu1")
        and has(budget, "gpu0")
        and has(budget, "npu"),
        "invocation_contract_defines_evidence_events": exists(
            repo_root, "ia_carmine/runtime/heap_provider/invocation_contract/cli.py"
        )
        and has(invocation, "expected_evidence_event_contract")
        and has(invocation, "broker_request")
        and has(invocation, "product_signal"),
        "orchestrator_launches_gpu0_and_npu_as_peers": exists(
            repo_root, "ia_carmine/providers/provider_mesh/gpu_npu_parallel_orchestrator/cli.py"
        )
        and exists(repo_root, "ia_carmine/providers/provider_mesh/gpu_npu_parallel_orchestrator/gpu_lanes.py")
        and exists(repo_root, "ia_carmine/providers/provider_mesh/gpu_npu_parallel_orchestrator/npu_micro.py"),
        "runtime_mesh_requires_heap_gpu0_npu": has(runtime_mesh, "gpu0_ollama_vulkan_tool_workload")
        and has(runtime_mesh, "npu_peer_micro_lane")
        and has(runtime_mesh, "heap_provider_budget_governor")
        and has(runtime_mesh, "heap_provider_invocation_contract"),
        "real_product_wrapper_requests_openvino_npu_peer_lanes": has(profiles, "gpu0_reviewer_refiner")
        and has(profiles, "npu_auditor")
        and has(npu_shared, "NPU"),
        "gpu0_provider_report_contract": exists(
            repo_root, "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py"
        )
        and has(gpu0_workload, "run_ollama_probe")
        and has(gpu0_workload, "ollama_gpu0_vulkan_required")
        and has(gpu0_workload, "openvino_gpu0_used")
        and has(gpu0_workload, "--require-ollama-gpu-residency")
        and has(gpu0_workload, "--leader-packet")
        and has(gpu0_workload, "response_text"),
        "npu_provider_report_contract": has(npu_companion_shared, "npu_provider_execution_performed")
        and has(npu_companion_shared, "npu_micro_provider_execution_performed")
        and has(npu_companion_shared, "npu_micro_provider_classification")
        and has(npu_companion_shared, "micro_task_provider_tool_loop_requested_when_lane_selected")
        and has(npu_companion_shared, "npu_micro_audit_performed")
        and has(npu_companion_shared, "npu_lane_disabled")
        and has(npu_companion_shared, "npu_peer_activity_performed")
        and has(npu_companion_shared, "native_tool_loop_provider")
        and has(npu_companion_shared, "native_tool_loop_supported")
        and has(npu_companion_shared, "native_tool_call_count")
        and has(npu_companion_shared, "leader_packet_consumed")
        and has(npu_companion_shared, "leader_packet_heap_universe_contract")
        and has(npu_companion_shared, "leader_packet_pointer_contract")
        and has(npu_companion_shared, "SOURCE_PATH_ALLOWLIST_CONTRACT")
        and has(npu_companion_shared, "--leader-packet")
        and has(npu_companion_shared, "--startup-manifest")
        and has(npu_companion_shared, "task_file_mode")
        and has(npu_companion_shared, "response_text")
        and has(npu_companion, "run_npu_device_workload"),
        "completeness_gate_executes_gpu0_npu_provider_reports": has(
            provider_commands, "build_ollama_gpu0_peer_report"
        )
        and has(provider_commands, "build_npu_micro_task_companion_report")
        and (has(provider_commands, '"lane": "gpu0_peer"') or has(provider_commands, '"lane": GPU0_LANE'))
        and (
            has(provider_commands, '"lane": "npu_micro_task_auditor"')
            or has(provider_commands, '"lane": NPU_LANE')
        )
        and has(provider_commands, "provider_execution_performed")
        and has(provider_commands, "npu_micro_provider_execution_performed")
        and has(provider_absorption, "provider_work_verified")
        and has(provider_commands, "--require-ollama-gpu-residency")
        and has(provider_commands, "--run-device-workload")
        and has(provider_commands, "--tool-loop-max-new-tokens")
        and has(provider_commands, "--leader-packet")
        and has(provider_commands, "--startup-manifest"),
        "provider_teamwork_runs_gpu0_npu_concurrently": has(
            provider_runtime, "provider_teamwork_unified_parallel"
        )
        and has(provider_execution, "provider_command_specs")
        and has(provider_execution, "collect_provider_processes")
        and has(provider_absorption, "provider_output")
        and has(provider_absorption, "provider_execution_performed")
        and has(provider_execution, "provider_launch_manifest")
        and has(provider_execution, "provider_teamwork_leader_packet")
        and has(provider_execution, "build_provider_teamwork_leader_packet")
        and has(provider_teamwork_packet, "gpu1_primary_advisory_leader")
        and has(provider_teamwork_packet, "heap_universe_contract")
        and has(provider_teamwork_packet, "same_heap_teamwork_contract")
        and has(provider_teamwork_packet, "pointer_contract")
        and has(provider_teamwork_packet, "resume_from_block_id")
        and has(provider_teamwork_packet, "gpu1_authority")
        and has(provider_teamwork_packet, "gpu0_peer_authority")
        and has(provider_teamwork_packet, "npu_peer_authority")
        and has(provider_teamwork_packet, "FINAL_PRODUCT_DELTA")
        and has(provider_teamwork_packet, "unified_parallel_execution")
        and has(provider_teamwork_packet, "re-evaluate in parallel")
        and has(provider_teamwork_packet, "requires_concrete_rewrite")
        and has(provider_teamwork_packet, "NO_PATCHABLE_TARGET")
        and has(provider_teamwork_packet, "startup_artifacts")
        and has(provider_teamwork_packet, "startup_context_plane")
        and has(provider_teamwork_packet, "artifact_reference_only_not_runtime_database")
        and has(provider_teamwork_packet, "broker_tool_evidence")
        and has(provider_teamwork_packet, "source_allowlist_contract")
        and has(provider_runtime, "started_at")
        and has(provider_absorption, "provider_process_id")
        and ordered_lane_specs(provider_commands),
        "heap_metrics_require_gpu0_npu_provider_evidence": has(
            heap_run_loop, "gpu0_provider_evidence_count"
        )
        and has(heap_run_loop, "npu_micro_task_evidence_count")
        and has(heap_run_loop, "build_provider_lane_metrics")
        and has(
            read_text(repo_root / "ia_carmine/runtime/heap_gate/run_loop_metrics.py"),
            "provider_lane_count",
        )
        and has(
            read_text(repo_root / "ia_carmine/runtime/heap_gate/run_loop_metrics.py"),
            "provider_semantic_missing_required_lanes",
        )
        and has(
            read_text(repo_root / "ia_carmine/runtime/heap_gate/run_loop_metrics.py"),
            '{"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}',
        ),
    }
    order = [
        "ollama_gpu0_vulkan_policy_required",
        "gpu1_reserved_from_openvino_workload",
        "gpu0_peer_command_is_support_lane",
        "npu_micro_uses_runtime_context_and_tool_broker",
        "runtime_heap_records_peer_events",
        "budget_governor_defines_lanes",
        "invocation_contract_defines_evidence_events",
        "orchestrator_launches_gpu0_and_npu_as_peers",
        "runtime_mesh_requires_heap_gpu0_npu",
        "real_product_wrapper_requests_openvino_npu_peer_lanes",
        "gpu0_provider_report_contract",
        "npu_provider_report_contract",
        "completeness_gate_executes_gpu0_npu_provider_reports",
        "provider_teamwork_runs_gpu0_npu_concurrently",
        "heap_metrics_require_gpu0_npu_provider_evidence",
    ]
    errors = [f"missing ollama/openvino peer topology contract: {name}" for name in order if not checks.get(name)]
    return {
        "schema_version": 1,
        "kind": "ollama_gpu0_openvino_npu_topology_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "check_order": order,
        **checks,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not errors,
        "errors": errors,
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/openvino_peer_topology_contract.json")
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    if args.markdown_output:
        write_markdown(report, resolve_output_path(repo_root, args.markdown_output))
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
