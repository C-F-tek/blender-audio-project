"""Provider lane process launch and launch manifest helpers."""
from __future__ import annotations
import time
from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    Path,
    command_env,
    now_iso,
    provider_heap_lane,
    repo_rel,
    subprocess,
    write_json_report,
)
from ia_carmine.runtime.heap_gate.provider_lane_policy import PRIMARY_LANE, lane_policy_payload


def write_provider_launch_manifest(
    gate: Any,
    path: Path,
    prepared: list[dict[str, Any]],
    round_id: int,
    revision: int,
    time_contract: dict[str, Any],
    stage: str,
) -> None:
    write_json_report(
        {
            "kind": "provider_launch_manifest",
            "execution_mode": "provider_teamwork_unified_parallel",
            "revision": revision,
            "round": round_id,
            "stage": stage,
            "created_at": now_iso(),
            "time_counter_contract": time_contract,
            "closure_owner": PRIMARY_LANE,
            "revision_opened_by_gpu1": True,
            "revision_lane_policy": getattr(gate, "provider_revision_lane_policy", {}),
            "provider_model_required": True,
            "provider_model_explicit": bool(
                str(getattr(gate.args, "provider_model", "")).strip()
                and str(getattr(gate.args, "provider_model", "")).strip() != "auto"
            ),
            "requested_provider_model": str(getattr(gate.args, "provider_model", "") or "auto"),
            "selected_provider_model": str(getattr(gate, "selected_provider_model", "") or ""),
            "selected_ollama_num_ctx": getattr(gate, "selected_ollama_num_ctx", None),
            "strict_provider_model": bool(getattr(gate.args, "strict_provider_model", False)),
            "provider_runtime_plan": getattr(gate, "provider_runtime_plan", ""),
            "provider_role_coexistence_preflight": getattr(
                gate, "provider_role_coexistence_preflight", {}
            ),
            "provider_boot_gate": getattr(gate, "provider_boot_gate", {}),
            "ollama_gpu_layers_requested": str(
                getattr(gate.args, "ollama_gpu_layers", "") or "all"
            ),
            "sidecar_start_policy": (
                "start_gpu0_npu_after_brief_gpu1_residency_preflight_not_after_gpu1_completion"
            ),
            "gpu1_residency_preflight": getattr(gate, "gpu1_residency_preflight", {}),
            "provider_replight_required": True,
            "provider_replight_reports": getattr(gate, "provider_replight_reports", []),
            "provider_replight_lanes": [
                item.get("provider_id") or item.get("lane")
                for item in getattr(gate, "provider_replight_reports", [])
                if isinstance(item, dict)
            ],
            "sidecars_start_after_gpu1_seconds": getattr(
                gate, "provider_sidecars_start_after_gpu1_seconds", None
            ),
            "soft_lock_policy": {
                "state": "closing_open_pointers",
                "new_broad_exploration_allowed": False,
                "gpu1_closure_owner": True,
                "gpu0_reviewer_refiner": True,
                "npu_micro_audit_only": True,
            },
            "lanes": [_lane_manifest_item(gate, item) for item in prepared],
        },
        path,
    )


def _lane_manifest_item(gate: Any, item: dict[str, Any]) -> dict[str, Any]:
    spec = item.get("spec", {})
    return {
        "lane": item.get("lane"),
        "requirement": item.get("requirement"),
        "role": spec.get("role"),
        "provider_model": (
            getattr(gate, "selected_provider_model", "") or gate.args.provider_model
            if item.get("lane") == PRIMARY_LANE
            else spec.get("provider_model", "")
        ),
        "pid": item.get("pid"),
        "started_at": item.get("started_at"),
        "completed_at": item.get("completed_at"),
        "elapsed_seconds": item.get("elapsed_seconds"),
        "timeout_seconds": item.get("timeout_seconds"),
        "budget_counter_seconds": item.get("budget_counter_seconds"),
        "soft_close_after_seconds": item.get("soft_close_after_seconds"),
        "watchdog_timeout_seconds": item.get("watchdog_timeout_seconds"),
        "provider_backend": spec.get("provider_backend"),
        "provider_compute_device": spec.get("provider_compute_device"),
        "provider_device_policy": spec.get("provider_device_policy"),
        **lane_policy_payload(item),
        "prepare_error": item.get("prepare_error"),
        "blocked_reason": item.get("blocked_reason", ""),
        "output": repo_rel(gate.repo_root, Path(spec["output"])),
        "leader_packet": gate.provider_leader_packet_path,
    }


def start_provider_item(gate: Any, item: dict[str, Any], round_id: int, revision: int) -> None:
    if item.get("completed") is not None:
        return
    command = list(item["command"])
    started_at = now_iso()
    started_perf = time.perf_counter()
    try:
        process = subprocess.Popen(
            command,
            cwd=gate.repo_root,
            env=command_env(gate.repo_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        item["process"] = process
        item["started_at"] = started_at
        item["started_perf"] = started_perf
        item["pid"] = process.pid
        _publish_running_state(gate, item, process.pid, started_at, round_id, revision)
    except Exception as exc:  # noqa: BLE001 - provider lane failure becomes report evidence.
        item["start_attempted_at"] = started_at
        item["started_at"] = ""
        item["completed_at"] = now_iso()
        item["elapsed_seconds"] = round(time.perf_counter() - started_perf, 6)
        item["prepare_error"] = f"start_error:{type(exc).__name__}: {exc}"
        item["completed"] = subprocess.CompletedProcess(
            command,
            returncode=127,
            stdout="",
            stderr=f"{type(exc).__name__}: {exc}",
        )


def _publish_running_state(
    gate: Any, item: dict[str, Any], pid: int, started_at: str, round_id: int, revision: int
) -> None:
    spec = item["spec"]
    gate.publish(
        provider_heap_lane(str(item["lane"])),
        "provider_state",
        {
            "id": str(item["correlation"]),
            "lane": item["lane"],
            "role": spec.get("role"),
            "requirement": item["requirement"],
            "revision": revision,
            "status": "running",
            "pid": pid,
            "started_at": started_at,
            "output": repo_rel(gate.repo_root, Path(spec["output"])),
            "execution_mode": "provider_teamwork_unified_parallel",
            "budget_counter_seconds": item.get("budget_counter_seconds"),
            "soft_close_after_seconds": item.get("soft_close_after_seconds"),
            "watchdog_timeout_seconds": item.get("watchdog_timeout_seconds"),
            "provider_backend": spec.get("provider_backend"),
            "provider_compute_device": spec.get("provider_compute_device"),
            "provider_device_policy": spec.get("provider_device_policy"),
            **lane_policy_payload(item),
        },
        target="orchestrator",
        correlation_id=str(item["correlation"]),
        round_id=round_id,
    )
