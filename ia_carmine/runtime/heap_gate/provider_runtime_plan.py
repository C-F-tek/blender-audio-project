from __future__ import annotations

import json
import subprocess

from ia_carmine._shared.ollama_provider_selection import (
    nvidia_gpu_inventory,
    ollama_model_inventory,
    parse_context_candidates,
)
from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import context_hierarchy_payload
from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, repo_rel, write_json_report


def write_provider_runtime_plan(
    gate: Any,
    work_dir: Path,
    *,
    selected_lanes: set[str] | None,
    stage: str,
    reports: list[dict[str, Any]] | None = None,
) -> Path:
    path = work_dir / "provider_runtime_plan.json"
    payload = {
        "kind": "provider_runtime_plan",
        "stage": stage,
        "requested_provider_model": str(getattr(gate.args, "provider_model", "") or "auto"),
        "selected_provider_model": str(getattr(gate, "selected_provider_model", "") or ""),
        "selected_ollama_num_ctx": getattr(gate, "selected_ollama_num_ctx", None),
        "provider_lane_hierarchy": context_hierarchy_payload(
            gate.args, gpu1_ctx=getattr(gate, "selected_ollama_num_ctx", None)
        ),
        "strict_provider_model": bool(getattr(gate.args, "strict_provider_model", False)),
        "ollama_context_candidates": parse_context_candidates(
            str(getattr(gate.args, "ollama_context_candidates", "") or "8192,4096"),
            int(getattr(gate.args, "ollama_num_ctx", 0) or 0),
        ),
        "operator_gpu_observation": str(getattr(gate.args, "operator_gpu_observation", "") or ""),
        "gpu0_model_dir": str(getattr(gate.args, "gpu0_model_dir", "") or ""),
        "npu_model_dir": str(getattr(gate.args, "npu_model_dir", "") or ""),
        "required_lanes": sorted(selected_lanes or []),
        "nvidia_gpus": nvidia_gpu_inventory(),
        "ollama_models": sorted(ollama_model_inventory().keys()),
        "openvino_devices": _openvino_devices(gate),
        "provider_replight_reports": _compact_reports(reports or []),
        "provider_role_coexistence_preflight": _compact_coexistence(
            getattr(gate, "provider_role_coexistence_preflight", {})
        ),
        "provider_boot_gate": _compact_coexistence(getattr(gate, "provider_boot_gate", {})),
    }
    write_json_report(payload, path)
    gate.provider_runtime_plan = repo_rel(gate.repo_root, path)
    return path


def _compact_reports(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = (
        "provider_id",
        "lane",
        "provider_model",
        "requested_provider_model",
        "selected_provider_model",
        "model_switch_reason",
        "lane_tier",
        "authority",
        "closure_owner",
        "context_budget",
        "provider_backend",
        "provider_compute_device",
        "provider_device_verified",
        "full_gpu_residency_verified",
        "device_workload_execution_performed",
        "semantic_provider_model_loaded",
        "npu_device_workload_performed",
        "npu_micro_provider_model_loaded",
        "replight_passed",
        "replight_blocked_reason",
    )
    return [{key: report.get(key) for key in keys if key in report} for report in reports]


def _compact_coexistence(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict) or not report:
        return {}
    roles = report.get("roles") if isinstance(report.get("roles"), dict) else {}
    return {
        "passed": report.get("passed"),
        "coexistence_verified": report.get("coexistence_verified"),
        "output": report.get("output"),
        "gpu1_alive": roles.get("gpu1_planner", {}).get("alive_during_coexistence")
        if isinstance(roles.get("gpu1_planner"), dict)
        else None,
        "gpu0_alive": roles.get("gpu0_peer", {}).get("alive_during_coexistence")
        if isinstance(roles.get("gpu0_peer"), dict)
        else None,
        "npu_loaded": roles.get("npu_micro_task_auditor", {}).get("model_loaded")
        if isinstance(roles.get("npu_micro_task_auditor"), dict)
        else None,
    }


def _openvino_devices(gate: Any) -> dict[str, Any]:
    command = [
        gate.child_python(),
        "-c",
        "import json, openvino as ov; print(json.dumps(ov.Core().available_devices))",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=str(gate.repo_root),
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001 - inventory is evidence, not control flow.
        return {"performed": False, "error": f"{type(exc).__name__}: {exc}"}
    try:
        devices = json.loads((completed.stdout or "").strip().splitlines()[-1])
    except Exception:
        devices = []
    return {
        "performed": True,
        "returncode": completed.returncode,
        "devices": devices if isinstance(devices, list) else [],
        "stderr_tail": (completed.stderr or "")[-1000:],
    }
