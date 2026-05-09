#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def exists(repo_root: Path, rel: str) -> bool:
    return (repo_root / rel).exists()


def has(text: str, token: str) -> bool:
    return token in text


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = [
        "# OpenVINO Peer Topology Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        "",
        "## Checks",
        "",
    ]
    for key in report.get("check_order") or []:
        lines.append(f"- `{key}`: `{report.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return write_text_report("\n".join(lines) + "\n", output)


def build_report(repo_root: Path) -> dict[str, Any]:
    openvino_devices = read_text(repo_root / "Tools/ai/full0to10_hardware_capability/openvino_devices.py")
    gpu0_contract = read_text(repo_root / "Tools/ai/full0to10_accelerator_control/gpu0_contract.py")
    npu_capability = read_text(repo_root / "Tools/ai/full0to10_hardware_capability/npu.py")
    workloads = read_text(repo_root / "Tools/ai/runtime_hardware_capability/workloads.py")
    gpu0_peer = read_text(repo_root / "Tools/ai/provider_mesh_runtime/gpu0_peer.py")
    npu_micro = read_text(repo_root / "Tools/ai/provider_mesh_runtime/npu_micro.py")
    runtime_heap = read_text(repo_root / "Tools/ai/provider_mesh_runtime/runtime_heap.py")
    orchestrator = read_text(repo_root / "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py")
    runtime_mesh = read_text(repo_root / "Tools/validation/check_real_product_runtime_mesh_contract.py")
    wrapper = read_text(repo_root / "Tools/workflow/run_unified_real_product_pr.ps1")

    checks: dict[str, bool] = {
        "openvino_visibility_normalizes_cpu_gpu0_gpu1_npu": all(
            token in openvino_devices
            for token in ("openvino_cpu", "openvino_gpu0", "openvino_gpu1", "openvino_npu")
        )
        and has(openvino_devices, '"GPU.0"')
        and has(openvino_devices, '"GPU.1"')
        and has(openvino_devices, '"NPU"'),

        "gpu1_reserved_from_openvino_workload": has(workloads, '"reserved_for_cuda_ollama"')
        and has(workloads, "openvino_gpu1_openvino_workload_allowed")
        and has(workloads, "False")
        and has(workloads, "no workload was executed on GPU.1"),

        "gpu0_compile_targets_gpu0_only": has(workloads, 'compile_model(model, "GPU.0")')
        and has(workloads, 'report["selected_device"] = "GPU.0"')
        and has(workloads, "openvino_gpu0_provider_execution_performed")
        and has(workloads, "openvino_gpu0_not_primary_advisory"),

        "gpu0_peer_command_is_support_lane": has(gpu0_peer, "build_openvino_gpu0_workload_report.py")
        and has(gpu0_peer, "--production-support")
        and has(gpu0_peer, "peer_support_round_")
        and has(gpu0_peer, "should_launch_gpu0_peer_support"),

        "npu_probe_is_no_model_load_no_generation": has(npu_capability, '"model_load_performed": False')
        and has(npu_capability, '"generation_performed": False')
        and has(npu_capability, "available_devices"),

        "npu_micro_uses_runtime_context_and_tool_broker": has(npu_micro, "collect_runtime_tool_context_reports")
        and has(npu_micro, "runtime_heap_snapshot")
        and has(npu_micro, "--runtime-tool-context-report")
        and has(npu_micro, "--max-npu-tool-requests")
        and has(npu_micro, "run_npu_gpu_deep_review_auditor.py"),

        "runtime_heap_records_gpu0_npu_events": has(runtime_heap, "append_runtime_heap_event")
        and has(orchestrator, "gpu0-peer-support")
        and has(orchestrator, "npu-micro-support")
        and has(orchestrator, "write_runtime_heap_snapshot"),

        "orchestrator_launches_gpu0_and_npu_as_peers": has(orchestrator, "launch_due_gpu0_peer_supports")
        and has(orchestrator, "launch_due_npu_micro_supports")
        and has(orchestrator, "active_gpu0_supports")
        and has(orchestrator, "active_npu_micro_supports")
        and has(orchestrator, "close_deadline"),

        "runtime_mesh_requires_openvino_gpu0_and_npu": has(runtime_mesh, "gpu0_openvino_tool_workload")
        and has(runtime_mesh, "npu_peer_micro_lane")
        and has(runtime_mesh, "openvino_gpu0_mentions_openvino")
        and has(runtime_mesh, "npu_companion_mentions_npu"),

        "real_product_wrapper_requests_openvino_npu_peer_lanes": has(wrapper, "-RunOpenVinoGpu0Workload")
        and has(wrapper, "-RunNpuProbe")
        and has(wrapper, "-RunNpuDecodeSmoke")
        and has(wrapper, '[string]$NpuMicroStartMode = "peer"'),
    }

    check_order = [
        "openvino_visibility_normalizes_cpu_gpu0_gpu1_npu",
        "gpu1_reserved_from_openvino_workload",
        "gpu0_compile_targets_gpu0_only",
        "gpu0_peer_command_is_support_lane",
        "npu_probe_is_no_model_load_no_generation",
        "npu_micro_uses_runtime_context_and_tool_broker",
        "runtime_heap_records_gpu0_npu_events",
        "orchestrator_launches_gpu0_and_npu_as_peers",
        "runtime_mesh_requires_openvino_gpu0_and_npu",
        "real_product_wrapper_requests_openvino_npu_peer_lanes",
    ]

    errors = [f"missing openvino peer topology contract: {name}" for name in check_order if not checks.get(name)]

    return {
        "schema_version": 1,
        "kind": "openvino_peer_topology_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "check_order": check_order,
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
