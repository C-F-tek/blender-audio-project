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
from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import context_hierarchy_payload


def write_provider_launch_manifest(
    gate: Any,
    path: Path,
    prepared: list[dict[str, Any]],
    round_id: int,
    revision: int,
    time_contract: dict[str, Any],
    stage: str,
) -> None:
    metrics = _parallel_window_metrics(prepared)
    write_json_report(
        {
            "kind": "provider_launch_manifest",
            "execution_mode": "provider_teamwork_unified_parallel",
            "revision": revision,
            "provider_cycle_id": revision,
            "revision_owner_lane": PRIMARY_LANE,
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
            "provider_lane_hierarchy": context_hierarchy_payload(
                gate.args, gpu1_ctx=getattr(gate, "selected_ollama_num_ctx", None)
            ),
            "provider_role_coexistence_preflight": getattr(
                gate, "provider_role_coexistence_preflight", {}
            ),
            "provider_boot_gate": getattr(gate, "provider_boot_gate", {}),
            "ollama_gpu_layers_requested": str(
                getattr(gate.args, "ollama_gpu_layers", "") or "all"
            ),
            "sidecar_start_policy": str(
                getattr(gate, "sidecars_start_policy", "")
                or "after_gpu1_residency_handshake"
            ),
            "gpu1_boot_leader_ready": bool(
                getattr(gate, "gpu1_boot_leader_ready", False)
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
            "parallel_provider_overlap_seconds": getattr(
                gate, "parallel_provider_overlap_seconds", None
            ),
            "production_provider_window": metrics,
            "all_selected_lanes_joined": metrics.get("all_selected_lanes_joined"),
            "sidecar_alone_after_gpu1_seconds": metrics.get(
                "sidecar_alone_after_gpu1_seconds"
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
    lane = str(item.get("lane") or "")
    return {
        "lane": item.get("lane"),
        "provider_cycle_id": spec.get("revision") or item.get("revision"),
        "revision_owner_lane": PRIMARY_LANE,
        "gpu1_revision_owner": lane == PRIMARY_LANE,
        "review_for_gpu1_cycle": item.get("review_for_gpu1_cycle"),
        "audit_for_gpu1_cycle": item.get("audit_for_gpu1_cycle"),
        "cannot_open_revision": lane != PRIMARY_LANE,
        "requirement": item.get("requirement"),
        "role": spec.get("role"),
        "provider_model": spec.get("provider_model", ""),
        "pid": item.get("pid"),
        "started_at": item.get("started_at"),
        "completed_at": item.get("completed_at"),
        "elapsed_seconds": item.get("elapsed_seconds"),
        "timeout_seconds": item.get("timeout_seconds"),
        "budget_counter_seconds": item.get("budget_counter_seconds"),
        "soft_close_after_seconds": item.get("soft_close_after_seconds"),
        "watchdog_timeout_seconds": item.get("watchdog_timeout_seconds"),
        "provider_backend": spec.get("provider_backend"),
        "provider_base_url": spec.get("provider_base_url"),
        "provider_compute_device": spec.get("provider_compute_device"),
        "provider_device_policy": spec.get("provider_device_policy"),
        "logical_lane": spec.get("logical_lane") or item.get("lane"),
        "provider_backend_device_id": spec.get("provider_backend_device_id"),
        "windows_task_manager_device_hint": spec.get("windows_task_manager_device_hint"),
        "vulkan_visible_device": spec.get("vulkan_visible_device"),
        "vulkan_device_name": spec.get("vulkan_device_name"),
        "vulkan_vendor_id": spec.get("vulkan_vendor_id"),
        "device_identity_verified": spec.get("device_identity_verified"),
        "lane_tier": spec.get("lane_tier"),
        "authority": spec.get("authority"),
        "context_budget": spec.get("context_budget"),
        **lane_policy_payload(item),
        "prepare_error": item.get("prepare_error"),
        "blocked_reason": item.get("blocked_reason", ""),
        "output": repo_rel(gate.repo_root, Path(spec["output"])),
        "leader_packet": gate.provider_leader_packet_path,
    }


def _parallel_window_metrics(prepared: list[dict[str, Any]]) -> dict[str, Any]:
    primary = next((item for item in prepared if item.get("lane") == PRIMARY_LANE), {})
    primary_start = primary.get("started_perf")
    primary_end = primary.get("completed_perf")
    sidecars = [item for item in prepared if item.get("lane") != PRIMARY_LANE]
    start_skews: dict[str, float] = {}
    sidecar_alone = 0.0
    for item in sidecars:
        lane = str(item.get("lane") or "")
        side_start = item.get("started_perf")
        side_end = item.get("completed_perf")
        if primary_start is not None and side_start is not None:
            start_skews[lane] = round(float(side_start) - float(primary_start), 6)
        if primary_end is not None and side_end is not None:
            sidecar_alone = max(
                sidecar_alone,
                max(0.0, float(side_end) - float(primary_end)),
            )
    return {
        "primary_lane": PRIMARY_LANE,
        "selected_lane_count": len(prepared),
        "started_lane_count": sum(1 for item in prepared if item.get("started_at")),
        "completed_lane_count": sum(1 for item in prepared if item.get("completed_at")),
        "all_selected_lanes_joined": bool(
            prepared and all(item.get("completed") is not None for item in prepared)
        ),
        "start_skew_seconds": start_skews,
        "sidecar_alone_after_gpu1_seconds": round(sidecar_alone, 6),
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
            "provider_cycle_id": revision,
            "revision_owner_lane": PRIMARY_LANE,
            "gpu1_revision_owner": item.get("lane") == PRIMARY_LANE,
            "review_for_gpu1_cycle": revision if item.get("lane") == "gpu0_peer" else None,
            "audit_for_gpu1_cycle": revision
            if item.get("lane") == "npu_micro_task_auditor"
            else None,
            "cannot_open_revision": item.get("lane") != PRIMARY_LANE,
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
            "logical_lane": spec.get("logical_lane") or item.get("lane"),
            "provider_backend_device_id": spec.get("provider_backend_device_id"),
            "windows_task_manager_device_hint": spec.get("windows_task_manager_device_hint"),
            "vulkan_visible_device": spec.get("vulkan_visible_device"),
            "vulkan_device_name": spec.get("vulkan_device_name"),
            "vulkan_vendor_id": spec.get("vulkan_vendor_id"),
            "device_identity_verified": spec.get("device_identity_verified"),
            **lane_policy_payload(item),
        },
        target="orchestrator",
        correlation_id=str(item["correlation"]),
        round_id=round_id,
    )
