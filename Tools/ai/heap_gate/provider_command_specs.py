"""Provider teamwork command spec builder."""

from __future__ import annotations

from typing import Any

from Tools.ai.heap_gate.provider_time import build_provider_lane_time_contracts
from Tools.ai.heap_gate.runtime_common import Path, repo_rel


def _time_fields(lane_time: dict[str, Any]) -> dict[str, Any]:
    return {
        "time_counter_contract": lane_time,
        "budget_counter_seconds": lane_time.get("budget_counter_seconds"),
        "soft_close_after_seconds": lane_time.get("soft_close_after_seconds"),
        "watchdog_timeout_seconds": 0,
        "timeout_seconds": 0,
    }


def _npu_device_workload_args(gate: Any) -> list[str]:
    """Return controlled physical NPU workload args.

    The NPU microtask provider lane is mandatory in provider-generation mode,
    but the physical OpenVINO/NPU device workload remains an explicit opt-in
    controlled by the selected runtime profile/operator flag.
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


def build_provider_command_specs(gate: Any, work_dir: Path, revision: int = 0) -> list[dict[str, Any]]:
    suffix = f"_revision{revision}" if revision else ""
    gpu1_json = work_dir / f"gpu1_ollama_provider_probe{suffix}.json"
    gpu0_json = work_dir / f"gpu0_openvino_peer_workload{suffix}.json"
    gpu0_md = work_dir / f"gpu0_openvino_peer_workload{suffix}.md"
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
    return [
        {
            "lane": "gpu1_planner",
            "requirement": "gpu1_provider_planner",
            "role": "primary_planner_cumulative_responder",
            "output": gpu1_json,
            **_time_fields(lane_times["gpu1_planner"]),
            "command": [
                gate.child_python(),
                "-m",
                "Tools.ai",
                "run_local_provider_probe",
                "--repo-root",
                ".",
                "--run-ollama",
                "--model",
                gate.args.provider_model,
                "--prompt",
                "__GPU1_CUMULATIVE_PROMPT__",
                "--timeout",
                "0",
                "--max-new-tokens",
                str(int(gate.args.max_new_tokens)),
                "--ollama-num-ctx",
                str(int(gate.args.ollama_num_ctx)),
                "--keep-alive",
                str(gate.args.keep_alive),
                "--output",
                repo_rel(gate.repo_root, gpu1_json),
            ],
        },
        {
            "lane": "gpu0_peer",
            "requirement": "gpu0_provider_peer",
            "role": "gpu0_peer_reviewer_refiner",
            "output": gpu0_json,
            **_time_fields(lane_times["gpu0_peer"]),
            "command": [
                gate.child_python(),
                "-m",
                "Tools.ai",
                "build_openvino_gpu0_workload_report",
                "--repo-root",
                ".",
                "--iterations",
                str(gate.args.gpu0_iterations),
                "--min-seconds",
                str(gate.args.gpu0_min_seconds),
                "--tool-loop-timeout-seconds",
                "0",
                "--require-semantic-provider",
                "--role",
                "heap_runtime_peer_reviewer_refiner",
                *startup_args,
                *(["--leader-packet", leader_packet] if leader_packet else []),
                *request_args,
                "--output",
                repo_rel(gate.repo_root, gpu0_json),
                "--markdown-output",
                repo_rel(gate.repo_root, gpu0_md),
            ],
        },
        {
            "lane": "npu_micro_task_auditor",
            "requirement": "npu_micro_task_auditor",
            "role": "npu_micro_task_auditor",
            "output": npu_json,
            **_time_fields(lane_times["npu_micro_task_auditor"]),
            "command": [
                gate.child_python(),
                "-m",
                "Tools.ai",
                "build_npu_micro_task_companion_report",
                "--repo-root",
                ".",
                *startup_args,
                *request_args,
                *(["--leader-packet", leader_packet] if leader_packet else []),
                "--python-exe",
                gate.child_python(),
                "--timeout-seconds",
                "0",
                "--max-context-chars",
                str(gate.args.npu_max_context_chars),
                "--tool-loop-timeout-seconds",
                "0",
                "--max-prompt-chars",
                str(gate.args.npu_max_prompt_chars),
                "--tool-loop-max-new-tokens",
                str(gate.args.npu_max_new_tokens),
                *_npu_device_workload_args(gate),
                "--output",
                repo_rel(gate.repo_root, npu_json),
                "--markdown-output",
                repo_rel(gate.repo_root, npu_md),
            ],
        },
    ]