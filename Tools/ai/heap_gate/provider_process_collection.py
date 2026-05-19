"""Non-blocking provider process collection for the heap gate."""

from __future__ import annotations

from collections.abc import Callable
import time

from Tools.ai.heap_gate.runtime_common import (
    Any,
    Path,
    now_iso,
    provider_heap_lane,
    repo_rel,
    subprocess,
    terminate_process_tree,
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
    while pending:
        now = time.perf_counter()
        for item in list(pending):
            process = item.get("process")
            if process is None:
                pending.remove(item)
                continue
            elapsed = now - float(item.get("started_perf") or now)
            item_timeout = float(item.get("timeout_seconds") or timeout_seconds)
            if process.poll() is None and elapsed <= item_timeout:
                continue
            command = list(item["command"])
            if process.poll() is None:
                terminate_process_tree(process)
                try:
                    stdout, stderr = process.communicate(timeout=5)
                except Exception:
                    stdout, stderr = "", "provider timeout; output collection failed after termination"
                item["completed"] = subprocess.CompletedProcess(
                    command,
                    returncode=124,
                    stdout=stdout or "",
                    stderr=(stderr or "") + "\nprovider timeout",
                )
                status = "timeout"
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
            item["elapsed_seconds"] = round(elapsed, 6)
            pending.remove(item)
            _publish_lane_state(gate, item, revision, round_id, status, timeout_seconds)
            if on_completed is not None:
                try:
                    on_completed(item)
                except Exception as exc:  # noqa: BLE001 - one lane must not block peer joins.
                    item["absorb_error"] = f"{type(exc).__name__}: {exc}"

        if pending and now - last_heartbeat >= 10.0:
            last_heartbeat = now
            lanes = [
                {
                    "lane": str(item.get("lane")),
                    "pid": item.get("pid"),
                    "elapsed_seconds": round(now - float(item.get("started_perf") or now), 3),
                    "timeout_seconds": item.get("timeout_seconds") or timeout_seconds,
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
                    "execution_mode": "concurrent_provider_teamwork",
                },
                target="orchestrator",
                correlation_id=f"{gate.stamp}:provider:heartbeat",
                round_id=round_id,
            )
        if pending:
            time.sleep(0.2)


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
        item["elapsed_seconds"] = 0.0
        try:
            _publish_lane_state(
                gate,
                item,
                revision,
                round_id,
                "terminated",
                int(item.get("timeout_seconds") or 0),
            )
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
            "status": status,
            "pid": item.get("pid"),
            "elapsed_seconds": item.get("elapsed_seconds"),
            "timeout_seconds": item.get("timeout_seconds") or timeout_seconds,
            "output": repo_rel(gate.repo_root, Path(item["spec"]["output"])),
            "execution_mode": "concurrent_provider_teamwork",
        },
        target="orchestrator",
        correlation_id=str(item["correlation"]),
        round_id=round_id,
    )
