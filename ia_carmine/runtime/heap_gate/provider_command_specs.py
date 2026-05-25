"""Provider teamwork command spec builder."""

from __future__ import annotations

import json
from typing import Any

from ia_carmine._shared.file_backed_transport import write_text_artifact
from ia_carmine._shared.ollama_provider_selection import (
    provider_model_is_auto,
    provider_model_policy_fields,
)
from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import (
    GPU0_LANE,
    GPU1_LANE,
    NPU_LANE,
    gpu0_max_new_tokens,
    gpu0_ollama_num_ctx,
    lane_context_budget,
    lane_hierarchy,
)
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
        "lane_is_closure_owner": lane_time.get("lane_is_closure_owner", False),
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
    if not value:
        raise RuntimeError("missing explicit provider runtime parameter: keep_alive")
    return str(getattr(gate.args, "keep_alive", ""))


def _required_config_value(args: Any, name: str) -> str:
    value = str(getattr(args, name, "") or "").strip()
    if not value:
        raise RuntimeError(f"missing explicit provider runtime parameter: {name}")
    return value


def _gpu1_model_policy(gate: Any, configured_model: str) -> dict[str, Any]:
    policy = provider_model_policy_fields(configured_model)
    selected = str(getattr(gate, "selected_provider_model", "") or "").strip()
    if provider_model_is_auto(configured_model):
        raise RuntimeError("provider_model_explicit_required")
    if selected and selected != configured_model:
        raise RuntimeError(
            "provider_model_selection_mismatch:"
            f"requested={configured_model}:selected={selected}"
        )
    policy["selected_provider_model"] = configured_model
    return policy


def _canonical_provider_args(gate: Any) -> list[str]:
    fingerprint = str(getattr(gate.args, "canonical_run_fingerprint", "") or "").strip()
    if not fingerprint:
        return []
    return [
        "--canonical-run-provider-evidence",
        "--canonical-run-fingerprint",
        fingerprint,
    ]


def _gpu0_max_new_tokens(gate: Any) -> int:
    return gpu0_max_new_tokens(gate.args)


def _coexistence_evidence_path(work_dir: Path, revision: int) -> Path:
    suffix = f"_revision{revision}" if revision else ""
    return work_dir / f"provider_role_coexistence{suffix}.json"


def _gpu0_server_evidence_path(work_dir: Path, revision: int) -> Path:
    current = _coexistence_evidence_path(work_dir, revision)
    if _path_has_gpu0_server(current):
        return current
    for candidate_revision in range(int(revision) - 1, -1, -1):
        candidate = _coexistence_evidence_path(work_dir, candidate_revision)
        if _path_has_gpu0_server(candidate):
            return candidate
    candidates = sorted(
        work_dir.glob("provider_role_coexistence*.json"),
        key=lambda item: item.stat().st_mtime if item.exists() else 0,
        reverse=True,
    )
    for candidate in candidates:
        if _path_has_gpu0_server(candidate):
            return candidate
    return current


def _path_has_gpu0_server(path: Path) -> bool:
    return bool(_gpu0_server_from_path(path))


def _gpu0_server_from_path(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig", errors="replace"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    server = payload.get("gpu0_vulkan_server")
    if isinstance(server, dict):
        return server
    for key in ("provider_role_coexistence_preflight", "provider_boot_gate"):
        nested = payload.get(key)
        nested = nested if isinstance(nested, dict) else {}
        server = nested.get("gpu0_vulkan_server")
        if isinstance(server, dict):
            return server
    return {}


def _gpu0_device_identity(gate: Any, evidence_path: Path | None = None) -> dict[str, Any]:
    preflight = getattr(gate, "provider_role_coexistence_preflight", {})
    preflight = preflight if isinstance(preflight, dict) else {}
    server = preflight.get("gpu0_vulkan_server")
    server = server if isinstance(server, dict) else {}
    if not server and evidence_path is not None:
        server = _gpu0_server_from_path(evidence_path)
    selection = server.get("vulkan_device_selection")
    selection = selection if isinstance(selection, dict) else {}
    target = selection.get("target_device")
    target = target if isinstance(target, dict) else {}
    resolved = str(selection.get("resolved") or "").strip()
    vendor = str(target.get("vendorID") or "").strip().lower()
    name = str(target.get("deviceName") or "").strip()
    dtype = str(target.get("deviceType") or "").strip().lower()
    verified = bool(vendor == "0x8086" or "intel" in name.lower() or "integrated" in dtype)
    return {
        "logical_lane": GPU0_LANE,
        "provider_backend_device_id": f"vulkan:{resolved}" if resolved else "",
        "windows_task_manager_device_hint": "Windows GPU 0 / Intel(R) Graphics",
        "vulkan_visible_device": resolved,
        "vulkan_device_name": name,
        "vulkan_vendor_id": vendor,
        "device_identity_verified": verified,
    }


def _gpu1_device_identity() -> dict[str, Any]:
    return {
        "logical_lane": GPU1_LANE,
        "provider_backend_device_id": "ollama:gpu1",
        "windows_task_manager_device_hint": "Windows GPU 1 / NVIDIA GeForce RTX 5080",
        "device_identity_verified": True,
    }


def _npu_device_identity() -> dict[str, Any]:
    return {
        "logical_lane": NPU_LANE,
        "provider_backend_device_id": "openvino:NPU",
        "windows_task_manager_device_hint": "Windows NPU / Intel(R) AI Boost",
        "device_identity_verified": True,
    }


def _provider_request_args(gate: Any, work_dir: Path, revision: int) -> list[str]:
    request_file = str(getattr(gate.args, "request_file", "") or "").strip()
    if request_file:
        return ["--request-file", request_file]
    ref = write_text_artifact(
        gate.repo_root,
        work_dir / "provider_input_artifacts",
        name=f"provider_request_revision_{revision}",
        text=gate.request_text(),
        kind="provider_request",
        producer="provider_command_specs",
        suffix=".md",
    )
    return ["--request-file", str(ref.get("path") or "")]


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
    coexistence_evidence = _gpu0_server_evidence_path(work_dir, revision)
    leader_packet = str(getattr(gate, "provider_leader_packet_path", "") or "")
    startup_manifest = str(getattr(gate.args, "startup_manifest", "") or "")
    task_file = str(getattr(gate.args, "task_file", "") or "")
    request_args = _provider_request_args(gate, work_dir, revision)
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
    configured_gpu1_model = _required_config_value(gate.args, "provider_model")
    gpu1_policy = _gpu1_model_policy(gate, configured_gpu1_model)
    gpu1_model = str(gpu1_policy["selected_provider_model"])
    gpu1_strict_model = (
        bool(getattr(gate.args, "strict_provider_model", False))
        or not provider_model_is_auto(configured_gpu1_model)
    )
    gpu0_model = _required_config_value(gate.args, "gpu0_model")
    gpu0_base_url = _required_config_value(gate.args, "gpu0_base_url")
    gpu0_vulkan_devices = _required_config_value(gate.args, "gpu0_vulkan_visible_devices")
    gpu1_base_url = _required_config_value(gate.args, "gpu1_base_url")
    gpu1_ctx = int(getattr(gate, "selected_ollama_num_ctx", 0) or gate.args.ollama_num_ctx)
    gpu0_ctx = gpu0_ollama_num_ctx(gate.args)
    keep_alive = _provider_keep_alive(gate)
    gpu1_context_candidates = _required_config_value(gate.args, "ollama_context_candidates")
    gpu1_derived_config: list[dict[str, Any]] = []
    gpu0_identity = _gpu0_device_identity(gate, coexistence_evidence)
    specs = [
        {
            "lane": GPU1_LANE,
            "requirement": "gpu1_provider_planner",
            "role": "primary_planner_cumulative_responder",
            **lane_hierarchy(GPU1_LANE),
            "context_budget": lane_context_budget(
                GPU1_LANE, gpu1_ctx=gpu1_ctx, gpu0_ctx=gpu0_ctx, args=gate.args
            ),
            "output": gpu1_json,
            "provider_model": gpu1_model,
            "requested_provider_model": configured_gpu1_model,
            "selected_provider_model": gpu1_model,
            "model_switch_allowed": bool(gpu1_policy["model_switch_allowed"]),
            "model_switch_performed": bool(gpu1_policy["model_switch_performed"]),
            "model_selection_policy": gpu1_policy["model_selection_policy"],
            "provider_backend": "ollama",
            "provider_base_url": gpu1_base_url,
            "provider_compute_device": "ollama/gpu1",
            "provider_device_policy": "ollama_gpu_accelerator_residency_cpu_only_blocked",
            **_gpu1_device_identity(),
            **_time_fields(lane_times["gpu1_planner"]),
            "derived_config": gpu1_derived_config,
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
                gpu1_context_candidates,
                "--keep-alive",
                keep_alive,
                "--defer-unload",
                *_canonical_provider_args(gate),
                "--output",
                repo_rel(gate.repo_root, gpu1_json),
                *(["--strict-provider-model"] if gpu1_strict_model else []),
                *(["--operator-gpu-observation", str(getattr(gate.args, "operator_gpu_observation", ""))] if str(getattr(gate.args, "operator_gpu_observation", "")).strip() else []),
            ],
        },
        {
            "lane": GPU0_LANE,
            "requirement": "gpu0_provider_peer",
            "role": "gpu0_peer_reviewer_refiner",
            **lane_hierarchy(GPU0_LANE),
            "context_budget": lane_context_budget(
                GPU0_LANE, gpu1_ctx=gpu1_ctx, gpu0_ctx=gpu0_ctx, args=gate.args
            ),
            "output": gpu0_json,
            "provider_model": gpu0_model,
            "provider_backend": "ollama",
            "provider_base_url": gpu0_base_url,
            "provider_compute_device": "ollama/gpu0-vulkan",
            "provider_device_policy": "ollama_gpu0_vulkan_required_openvino_gpu0_forbidden",
            **gpu0_identity,
            "provider_max_new_tokens": _gpu0_max_new_tokens(gate),
            "sidecar_scope_mode": "packet_review_only",
            "sidecar_scope_contract": (
                "review_current_gpu1_packet_only_no_broad_exploration_no_final_synthesis"
            ),
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
                "--gpu0-vulkan-visible-devices",
                gpu0_vulkan_devices,
                "--server-evidence",
                repo_rel(gate.repo_root, coexistence_evidence),
                "--model",
                gpu0_model,
                "--max-new-tokens",
                str(_gpu0_max_new_tokens(gate)),
                "--ollama-num-ctx",
                str(gpu0_ctx),
                "--ollama-gpu-layers",
                str(gate.args.ollama_gpu_layers or "all"),
                "--ollama-context-candidates",
                str(gpu0_ctx),
                "--keep-alive",
                keep_alive,
                "--defer-unload",
                *_canonical_provider_args(gate),
                *startup_args,
                *(["--leader-packet", leader_packet] if leader_packet else []),
                *request_args,
                "--output",
                repo_rel(gate.repo_root, gpu0_json),
                "--markdown-output",
                repo_rel(gate.repo_root, gpu0_md),
                "--strict-provider-model",
                *(["--operator-gpu-observation", str(getattr(gate.args, "operator_gpu_observation", ""))] if str(getattr(gate.args, "operator_gpu_observation", "")).strip() else []),
            ],
        },
        {
            "lane": NPU_LANE,
            "requirement": "npu_micro_task_auditor",
            "role": "npu_micro_task_auditor",
            **lane_hierarchy(NPU_LANE),
            "context_budget": lane_context_budget(
                NPU_LANE, gpu1_ctx=gpu1_ctx, gpu0_ctx=gpu0_ctx, args=gate.args
            ),
            "output": npu_json,
            "provider_backend": "openvino",
            "provider_compute_device": "openvino/NPU",
            "provider_device_policy": "openvino_NPU_only_cpu_not_provider",
            **_npu_device_identity(),
            "sidecar_scope_mode": "packet_review_only",
            "sidecar_scope_contract": (
                "micro_audit_current_gpu1_packet_only_no_broad_exploration_no_final_synthesis"
            ),
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
                *_canonical_provider_args(gate),
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
