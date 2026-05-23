"""Non-blocking provider process collection for the heap gate."""
from __future__ import annotations
from collections.abc import Callable
import time
from math import inf
from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    Path,
    now_iso,
    provider_heap_lane,
    repo_rel,
    subprocess,
    terminate_process_tree,
)
from ia_carmine.runtime.heap_gate.provider_universe_abort import (
    block_provider_universe_run,
    provider_universe_abort_reason,
)
def collect_provider_processes(
    gate: Any,
    prepared: list[dict[str, Any]],
    timeout_seconds: int,
    round_id: int,
    revision: int,
    on_completed: Callable[[dict[str, Any]], None] | None = None,
) -> None:
    pending = [
        item
        for item in prepared
        if item.get("completed") is None and item.get("process") is not None
    ]
    last_heartbeat = 0.0
    if _terminate_pending_when_universe_inactive(
        gate, prepared, pending, round_id, revision, timeout_seconds, on_completed
    ):
        return
    while pending:
        now = time.perf_counter()
        for item in list(pending):
            process = item.get("process")
            if process is None:
                pending.remove(item)
                continue
            elapsed = now - float(item.get("started_perf") or now)
            watchdog = _item_watchdog_seconds(item, timeout_seconds)
            if process.poll() is None and elapsed <= watchdog:
                continue
            command = list(item["command"])
            if process.poll() is None:
                terminate_process_tree(process)
                try:
                    stdout, stderr = process.communicate(timeout=5)
                except Exception:
                    stdout, stderr = "", "provider watchdog cleanup output collection failed"
                reason = "provider watchdog timeout"
                item["completed"] = subprocess.CompletedProcess(
                    command,
                    returncode=124,
                    stdout=stdout or "",
                    stderr=(stderr or "") + f"\n{reason}",
                )
                status = "watchdog_timeout"
            else:
                stdout, stderr = process.communicate()
                item["completed"] = subprocess.CompletedProcess(
                    command,
                    returncode=process.returncode,
                    stdout=stdout or "",
                    stderr=stderr or "",
                )
                status = "finished"
            item["completed_at"] = now_iso()
            item["completed_perf"] = now
            item["elapsed_seconds"] = round(elapsed, 6)
            pending.remove(item)
            _publish_lane_state(gate, item, revision, round_id, status, timeout_seconds)
            if on_completed is not None:
                try:
                    on_completed(item)
                except Exception as exc:  # noqa: BLE001 - one lane must not block peer joins.
                    item["absorb_error"] = f"{type(exc).__name__}: {exc}"
            if _terminate_pending_when_universe_inactive(
                gate, prepared, pending, round_id, revision, timeout_seconds, on_completed
            ):
                return

        if pending and now - last_heartbeat >= 10.0:
            last_heartbeat = now
            lanes = [
                {
                    "lane": str(item.get("lane")),
                    "pid": item.get("pid"),
                    "elapsed_seconds": round(now - float(item.get("started_perf") or now), 3),
                    "timeout_seconds": item.get("timeout_seconds") or timeout_seconds,
                    "budget_counter_seconds": item.get("budget_counter_seconds"),
                    "soft_close_after_seconds": item.get("soft_close_after_seconds"),
                    "watchdog_timeout_seconds": item.get("watchdog_timeout_seconds"),
                    "closure_owner": item.get("closure_owner"),
                    "sidecar_lane": item.get("sidecar_lane"),
                    "sidecar_join_after_primary_seconds": item.get(
                        "sidecar_join_after_primary_seconds"
                    ),
                    "output": repo_rel(gate.repo_root, Path(item["spec"]["output"])),
                }
                for item in pending
            ]
            gate.append_heap_exchange_event(
                {
                    "kind": "provider_lane_heartbeat",
                    "round": round_id,
                    "revision": revision,
                    "pending_lanes": lanes,
                }
            )
            gate.publish(
                "orchestrator",
                "provider_state",
                {
                    "id": f"{gate.stamp}:provider:heartbeat:{revision}:{round_id}",
                    "revision": revision,
                    "round": round_id,
                    "status": "running",
                    "pending_lanes": lanes,
                    "execution_mode": "provider_teamwork_unified_parallel",
                },
                target="orchestrator",
                correlation_id=f"{gate.stamp}:provider:heartbeat",
                round_id=round_id,
            )
        if pending:
            time.sleep(0.2)


def _item_watchdog_seconds(item: dict[str, Any], fallback_seconds: int) -> float:
    value = float(
        item.get("watchdog_timeout_seconds")
        or item.get("timeout_seconds")
        or fallback_seconds
    )
    return inf if value <= 0 else value


def _terminate_pending_when_universe_inactive(
    gate: Any,
    prepared: list[dict[str, Any]],
    pending: list[dict[str, Any]],
    round_id: int,
    revision: int,
    timeout_seconds: int,
    on_completed: Callable[[dict[str, Any]], None] | None,
) -> bool:
    start_abort_reason = _provider_lane_start_abort_reason(prepared)
    if start_abort_reason:
        block_provider_universe_run(gate, start_abort_reason, round_id, revision)
        terminate_pending_provider_processes(gate, pending, round_id, revision, start_abort_reason)
        for item in list(pending):
            if item.get("completed") is None:
                continue
            pending.remove(item)
            if on_completed is not None:
                try:
                    on_completed(item)
                except Exception as exc:  # noqa: BLE001 - preserve lane termination evidence.
                    item["absorb_error"] = f"{type(exc).__name__}: {exc}"
        return True
    reason = provider_universe_abort_reason(prepared)
    if not reason:
        return False
    block_provider_universe_run(gate, reason, round_id, revision)
    gate.append_heap_exchange_event(
        {"kind": "provider_universe_aborted", "round": round_id, "revision": revision, "reason": reason}
    )
    if pending:
        gate.append_heap_exchange_event(
            {
                "kind": "provider_universe_blocked_waiting_for_active_lanes",
                "round": round_id,
                "revision": revision,
                "reason": reason,
                "pending_lanes": [str(item.get("lane") or "") for item in pending],
            }
        )
        return False
    return True


def _provider_lane_start_abort_reason(prepared: list[dict[str, Any]]) -> str:
    for item in prepared:
        if str(item.get("prepare_error") or ""):
            return f"provider_universe_lane_not_started:{item.get('lane')}:prepare_error"
        if item.get("completed") is not None and not item.get("started_at"):
            return f"provider_universe_lane_not_started:{item.get('lane')}:not_started"
    return ""
def terminate_pending_provider_processes(
    gate: Any,
    prepared: list[dict[str, Any]],
    round_id: int,
    revision: int,
    reason: str,
) -> None:
    for item in prepared:
        process = item.get("process")
        if process is None or item.get("completed") is not None:
            continue
        if process.poll() is not None:
            continue
        try:
            terminate_process_tree(process)
            stdout, stderr = process.communicate(timeout=5)
        except BaseException as exc:  # noqa: BLE001 - cleanup must not mask the original failure.
            stdout = ""
            stderr = f"{type(exc).__name__}: {exc}"
        item["completed"] = subprocess.CompletedProcess(
            list(item.get("command") or []),
            returncode=130,
            stdout=stdout or "",
            stderr=(stderr or "") + f"\nprovider terminated during cleanup: {reason}",
        )
        item["completed_at"] = now_iso()
        item["completed_perf"] = time.perf_counter()
        item["elapsed_seconds"] = 0.0
        try:
            watchdog = _item_watchdog_seconds(item, 0)
            published_timeout = 0 if watchdog == inf else int(watchdog)
            _publish_lane_state(gate, item, revision, round_id, "terminated", published_timeout)
        except BaseException:
            pass
def _publish_lane_state(
    gate: Any,
    item: dict[str, Any],
    revision: int,
    round_id: int,
    status: str,
    timeout_seconds: int,
) -> None:
    gate.publish(
        provider_heap_lane(str(item["lane"])),
        "provider_state",
        {
            "id": str(item["correlation"]),
            "lane": item["lane"],
            "role": item["spec"].get("role"),
            "requirement": item["requirement"],
            "revision": revision,
            "provider_cycle_id": revision,
            "revision_owner_lane": "gpu1_planner",
            "gpu1_revision_owner": item.get("lane") == "gpu1_planner",
            "review_for_gpu1_cycle": revision if item.get("lane") == "gpu0_peer" else None,
            "audit_for_gpu1_cycle": revision
            if item.get("lane") == "npu_micro_task_auditor"
            else None,
            "cannot_open_revision": item.get("lane") != "gpu1_planner",
            "status": status,
            "pid": item.get("pid"),
            "elapsed_seconds": item.get("elapsed_seconds"),
            "timeout_seconds": item.get("timeout_seconds") or timeout_seconds,
            "budget_counter_seconds": item.get("budget_counter_seconds"),
            "soft_close_after_seconds": item.get("soft_close_after_seconds"),
            "watchdog_timeout_seconds": item.get("watchdog_timeout_seconds"),
            "closure_owner": item.get("closure_owner"),
            "sidecar_lane": item.get("sidecar_lane"),
            "sidecar_join_after_primary_seconds": item.get(
                "sidecar_join_after_primary_seconds"
            ),
            "failure_kind": item.get("failure_kind") or "",
            "output": repo_rel(gate.repo_root, Path(item["spec"]["output"])),
            "execution_mode": "provider_teamwork_unified_parallel",
            "provider_backend": item["spec"].get("provider_backend"),
            "provider_compute_device": item["spec"].get("provider_compute_device"),
            "provider_device_policy": item["spec"].get("provider_device_policy"),
            "logical_lane": item["spec"].get("logical_lane") or item.get("lane"),
            "provider_backend_device_id": item["spec"].get("provider_backend_device_id"),
            "windows_task_manager_device_hint": item["spec"].get(
                "windows_task_manager_device_hint"
            ),
            "vulkan_visible_device": item["spec"].get("vulkan_visible_device"),
            "vulkan_device_name": item["spec"].get("vulkan_device_name"),
            "vulkan_vendor_id": item["spec"].get("vulkan_vendor_id"),
            "device_identity_verified": item["spec"].get("device_identity_verified"),
        },
        target="orchestrator",
        correlation_id=str(item["correlation"]),
        round_id=round_id,
    )
