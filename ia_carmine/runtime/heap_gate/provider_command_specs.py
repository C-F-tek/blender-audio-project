"""Provider teamwork command spec builder."""

from __future__ import annotations

import os
from typing import Any

from ia_carmine.runtime.heap_gate.provider_time import build_provider_lane_time_contracts
from ia_carmine.runtime.heap_gate.runtime_common import Path, repo_rel


def _time_fields(lane_time: dict[str, Any]) -> dict[str, Any]:
    return {
        "time_counter_contract": lane_time,
        "budget_counter_seconds": lane_time.get("budget_counter_seconds"),
        "soft_close_after_seconds": lane_time.get("soft_close_after_seconds"),
        "watchdog_timeout_seconds": lane_time.get("watchdog_timeout_seconds", 0),
        "timeout_seconds": lane_time.get("timeout_seconds", 0),
        "native_tool_timeout_seconds": lane_time.get("native_tool_timeout_seconds", 0),
        "sidecar_join_after_primary_seconds": lane_time.get(
            "sidecar_join_after_primary_seconds", 0
        ),
        "lane_authority": lane_time.get("lane_authority", ""),
        "closure_owner": lane_time.get("closure_owner", False),
        "primary_closer": lane_time.get("primary_closer", False),
        "sidecar_lane": lane_time.get("sidecar_lane", False),
        "micro_audit_only": lane_time.get("micro_audit_only", False),
        "reviewer_refiner": lane_time.get("reviewer_refiner", False),
        "native_tool_calling_policy": lane_time.get("native_tool_calling_policy", ""),
        "delta_context_mode": lane_time.get("delta_context_mode", ""),
        "npu_micro_timeout_enforced": lane_time.get("npu_micro_timeout_enforced", False),
    }


def _npu_device_workload_args(gate: Any) -> list[str]:
    """Return controlled physical NPU workload args.

    In provider-generation mode the NPU microtask lane must perform bounded
    device work unless an explicit diagnostic profile disables it upstream.
    """
    if not bool(getattr(gate.args, "allow_npu_device_workload", False)):
        return []
    return [
        "--run-device-workload",
        "--device-workload-seconds",
        str(gate.args.npu_device_workload_seconds),
        "--device-workload-iterations",
        str(gate.args.npu_device_workload_iterations),
    ]


def _provider_keep_alive(gate: Any) -> str:
    value = str(getattr(gate.args, "keep_alive", "") or "").strip().lower()
    if value in {"", "0", "0s", "0m", "0h"} and bool(
        getattr(gate.args, "allow_provider_generation", False)
    ):
        return "120s"
    return str(getattr(gate.args, "keep_alive", "") or "120s")


def build_provider_command_specs(
    gate: Any,
    work_dir: Path,
    revision: int = 0,
    selected_lanes: set[str] | None = None,
) -> list[dict[str, Any]]:
    suffix = f"_revision{revision}" if revision else ""
    gpu1_json = work_dir / f"gpu1_ollama_provider_probe{suffix}.json"
    gpu0_json = work_dir / f"gpu0_ollama_vulkan_peer{suffix}.json"
    gpu0_md = work_dir / f"gpu0_ollama_vulkan_peer{suffix}.md"
    npu_json = work_dir / f"npu_micro_task_auditor{suffix}.json"
    npu_md = work_dir / f"npu_micro_task_auditor{suffix}.md"
    leader_packet = str(getattr(gate, "provider_leader_packet_path", "") or "")
    startup_manifest = str(getattr(gate.args, "startup_manifest", "") or "")
    task_file = str(getattr(gate.args, "task_file", "") or "")
    request_file = str(getattr(gate.args, "request_file", "") or "")
    request_args = ["--request-file", request_file] if request_file else ["--request", gate.request_text()]
    startup_args = (
        ["--startup-manifest", startup_manifest]
        if startup_manifest
        else (["--task-file", task_file] if task_file else [])
    )
    lane_times = build_provider_lane_time_contracts(gate.args)
    npu_timeout = lane_times["npu_micro_task_auditor"].get("timeout_seconds", 60)
    npu_tool_timeout = lane_times["npu_micro_task_auditor"].get(
        "native_tool_timeout_seconds", npu_timeout
    )
    gpu1_model = str(getattr(gate, "selected_provider_model", "") or gate.args.provider_model or "auto")
    gpu0_model = str(os.environ.get("IA_CARMINE_GPU0_MODEL") or "qwen3:1.7b")
    gpu0_base_url = str(
        os.environ.get("IA_CARMINE_GPU0_OLLAMA_BASE_URL") or "http://127.0.0.1:11435"
    )
    gpu0_vulkan_devices = str(os.environ.get("IA_CARMINE_GPU0_VULKAN_VISIBLE_DEVICES") or "auto")
    gpu1_base_url = str(os.environ.get("IA_CARMINE_GPU1_OLLAMA_BASE_URL") or "")
    gpu1_ctx = int(getattr(gate, "selected_ollama_num_ctx", 0) or gate.args.ollama_num_ctx)
    keep_alive = _provider_keep_alive(gate)
    specs = [
        {
            "lane": "gpu1_planner",
            "requirement": "gpu1_provider_planner",
            "role": "primary_planner_cumulative_responder",
            "output": gpu1_json,
            "provider_backend": "ollama",
            "provider_compute_device": "ollama/gpu",
            "provider_device_policy": "ollama_gpu_accelerator_residency_cpu_only_blocked",
            **_time_fields(lane_times["gpu1_planner"]),
            "command": [
                gate.child_python(),
                "-m",
                "ia_carmine",
                "run_local_provider_probe",
                "--repo-root",
                ".",
                "--run-ollama",
                "--require-ollama-gpu-residency",
                *(["--ollama-base-url", gpu1_base_url] if gpu1_base_url else []),
                "--model",
                gpu1_model,
                "--prompt",
                "__GPU1_CUMULATIVE_PROMPT__",
                "--timeout",
                "0",
                "--max-new-tokens",
                str(int(gate.args.max_new_tokens)),
                "--ollama-num-ctx",
                str(gpu1_ctx),
                "--ollama-gpu-layers",
                str(gate.args.ollama_gpu_layers or "all"),
                "--ollama-context-candidates",
                str(getattr(gate.args, "ollama_context_candidates", "") or "8192,4096"),
                "--keep-alive",
                keep_alive,
                "--output",
                repo_rel(gate.repo_root, gpu1_json),
                *(["--strict-provider-model"] if getattr(gate.args, "strict_provider_model", False) else []),
                *(["--operator-gpu-observation", str(getattr(gate.args, "operator_gpu_observation", ""))] if str(getattr(gate.args, "operator_gpu_observation", "")).strip() else []),
            ],
        },
        {
            "lane": "gpu0_peer",
            "requirement": "gpu0_provider_peer",
            "role": "gpu0_peer_reviewer_refiner",
            "output": gpu0_json,
            "provider_backend": "ollama",
            "provider_compute_device": "ollama/gpu0-vulkan",
            "provider_device_policy": "ollama_gpu0_vulkan_required_openvino_gpu0_forbidden",
            **_time_fields(lane_times["gpu0_peer"]),
            "command": [
                gate.child_python(),
                "-m",
                "ia_carmine",
                "build_ollama_gpu0_peer_report",
                "--repo-root",
                ".",
                "--base-url",
                gpu0_base_url,
                "--restart-gpu0-vulkan-server",
                "--gpu0-vulkan-visible-devices",
                gpu0_vulkan_devices,
                "--model",
                gpu0_model,
                "--max-new-tokens",
                str(int(gate.args.max_new_tokens)),
                "--ollama-num-ctx",
                str(gpu1_ctx),
                "--ollama-gpu-layers",
                str(gate.args.ollama_gpu_layers or "all"),
                "--ollama-context-candidates",
                str(getattr(gate.args, "ollama_context_candidates", "") or "8192,4096"),
                "--keep-alive",
                keep_alive,
                *startup_args,
                *(["--leader-packet", leader_packet] if leader_packet else []),
                *request_args,
                "--output",
                repo_rel(gate.repo_root, gpu0_json),
                "--markdown-output",
                repo_rel(gate.repo_root, gpu0_md),
                *(["--strict-provider-model"] if getattr(gate.args, "strict_provider_model", False) else []),
                *(["--operator-gpu-observation", str(getattr(gate.args, "operator_gpu_observation", ""))] if str(getattr(gate.args, "operator_gpu_observation", "")).strip() else []),
            ],
        },
        {
            "lane": "npu_micro_task_auditor",
            "requirement": "npu_micro_task_auditor",
            "role": "npu_micro_task_auditor",
            "output": npu_json,
            "provider_backend": "openvino",
            "provider_compute_device": "openvino/NPU",
            "provider_device_policy": "openvino_NPU_only_cpu_not_provider",
            **_time_fields(lane_times["npu_micro_task_auditor"]),
            "command": [
                gate.child_python(),
                "-m",
                "ia_carmine",
                "build_npu_micro_task_companion_report",
                "--repo-root",
                ".",
                *startup_args,
                *request_args,
                *(["--leader-packet", leader_packet] if leader_packet else []),
                "--python-exe",
                gate.child_python(),
                "--timeout-seconds",
                str(npu_timeout),
                "--max-context-chars",
                str(gate.args.npu_max_context_chars),
                "--tool-loop-timeout-seconds",
                str(npu_tool_timeout),
                "--max-prompt-chars",
                str(gate.args.npu_max_prompt_chars),
                "--tool-loop-max-new-tokens",
                str(gate.args.npu_max_new_tokens),
                *(["--npu-model-dir", str(getattr(gate.args, "npu_model_dir", ""))] if str(getattr(gate.args, "npu_model_dir", "")).strip() else []),
                *_npu_device_workload_args(gate),
                "--output",
                repo_rel(gate.repo_root, npu_json),
                "--markdown-output",
                repo_rel(gate.repo_root, npu_md),
            ],
        },
    ]
    if getattr(gate.args, "ollama_num_thread", None):
        specs[0]["command"].extend(
            ["--ollama-num-thread", str(int(gate.args.ollama_num_thread))]
        )
        specs[1]["command"].extend(
            ["--ollama-num-thread", str(int(gate.args.ollama_num_thread))]
        )
    if selected_lanes is None:
        return specs
    return [spec for spec in specs if str(spec.get("lane")) in selected_lanes]
