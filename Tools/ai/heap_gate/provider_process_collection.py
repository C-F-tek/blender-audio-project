"""Non-blocking provider process collection for the heap gate."""
from __future__ import annotations
from collections.abc import Callable
import time
from Tools.ai.heap_gate.runtime_common import (
    Any,
    Path,
    now_iso,
    provider_heap_lane,
    read_json,
    repo_rel,
    subprocess,
    terminate_process_tree,
)
from Tools.ai.heap_gate.provider_universe_abort import (
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
    while pending:
        now = time.perf_counter()
        stalled = _terminate_nonproductive_gpu1_stall(
            gate,
            prepared,
            pending,
            now,
            timeout_seconds,
            round_id,
            revision,
        )
        if stalled:
            pending.remove(stalled)
            if on_completed is not None:
                try:
                    on_completed(stalled)
                except Exception as exc:  # noqa: BLE001 - one lane must not block peer joins.
                    stalled["absorb_error"] = f"{type(exc).__name__}: {exc}"
            if _terminate_pending_when_universe_inactive(
                gate, prepared, pending, round_id, revision, timeout_seconds, on_completed
            ):
                return
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
def _terminate_nonproductive_gpu1_stall(
    gate: Any,
    prepared: list[dict[str, Any]],
    pending: list[dict[str, Any]],
    now: float,
    timeout_seconds: int,
    round_id: int,
    revision: int,
) -> dict[str, Any] | None:
    gpu1 = next(
        (
            item
            for item in pending
            if str(item.get("lane") or "") == "gpu1_planner"
            and item.get("completed") is None
            and item.get("process") is not None
        ),
        None,
    )
    if gpu1 is None:
        return None
    process = gpu1.get("process")
    if process is None or process.poll() is not None:
        return None
    elapsed = now - float(gpu1.get("started_perf") or now)
    item_timeout = float(gpu1.get("timeout_seconds") or timeout_seconds)
    threshold = max(60.0, min(120.0, item_timeout * 0.6))
    if elapsed < threshold:
        return None
    if _gpu1_output_observable(gate, gpu1):
        return None
    if _materialized_provider_or_proposal_present(gate):
        return None
    if not _peer_lanes_degraded_without_operational_blocks(prepared):
        return None
    reason = "gpu1_nonproductive_runtime_stall"
    try:
        terminate_process_tree(process)
        stdout, stderr = process.communicate(timeout=5)
    except Exception:
        stdout = ""
        stderr = "provider stall; output collection failed after termination"
    gpu1["completed"] = subprocess.CompletedProcess(
        list(gpu1.get("command") or []),
        returncode=124,
        stdout=stdout or "",
        stderr=(stderr or "") + f"\n{reason}",
    )
    gpu1["completed_at"] = now_iso()
    gpu1["elapsed_seconds"] = round(elapsed, 6)
    gpu1["failure_kind"] = reason
    _publish_lane_state(gate, gpu1, revision, round_id, "failed", timeout_seconds)
    if reason not in gate.errors:
        gate.errors.append(reason)
    payload = {
        "kind": reason,
        "round": round_id,
        "revision": revision,
        "lane": "gpu1_planner",
        "elapsed_seconds": gpu1["elapsed_seconds"],
        "timeout_seconds": item_timeout,
        "peer_lanes": _peer_lane_statuses(prepared),
        "output": repo_rel(gate.repo_root, Path(gpu1["spec"]["output"])),
    }
    gate.append_heap_exchange_event(payload)
    gate.publish(
        "orchestrator",
        "validation_signal",
        payload,
        target="deterministic",
        correlation_id=f"{gate.stamp}:gpu1-stall:{round_id}",
        round_id=round_id,
    )
    return gpu1
def _terminate_pending_when_universe_inactive(
    gate: Any,
    prepared: list[dict[str, Any]],
    pending: list[dict[str, Any]],
    round_id: int,
    revision: int,
    timeout_seconds: int,
    on_completed: Callable[[dict[str, Any]], None] | None,
) -> bool:
    reason = provider_universe_abort_reason(prepared)
    if not reason:
        return False
    block_provider_universe_run(gate, reason, round_id, revision)
    gate.append_heap_exchange_event(
        {"kind": "provider_universe_aborted", "round": round_id, "revision": revision, "reason": reason}
    )
    if not pending:
        return True
    terminate_pending_provider_processes(gate, pending, round_id, revision, reason)
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
def _gpu1_output_observable(gate: Any, item: dict[str, Any]) -> bool:
    output = Path(item["spec"]["output"])
    if not output.is_absolute():
        output = gate.repo_root / output
    if not output.is_file():
        return False
    try:
        data = read_json(output)
    except Exception:
        return output.stat().st_size > 0
    if not isinstance(data, dict):
        return output.stat().st_size > 0
    if not data:
        return output.stat().st_size > 0
    if data.get("kind") == "ollama_provider_partial":
        try:
            partial_chars = int(data.get("partial_response_chars") or 0)
        except (TypeError, ValueError):
            partial_chars = 0
        if partial_chars > 0:
            return True
    if str(data.get("response_text") or data.get("provider_heap_delta_text") or "").strip():
        return True
    try:
        native_count = int(data.get("native_tool_call_count") or 0)
    except (TypeError, ValueError):
        native_count = 0
    if native_count > 0:
        return True
    calls = data.get("tool_calls")
    return isinstance(calls, list) and bool(calls)
def _materialized_provider_or_proposal_present(gate: Any) -> bool:
    if any(
        isinstance(report, dict) and report.get("operational_provider_activity")
        for report in getattr(gate, "provider_reports", [])
    ):
        return True
    proposal_refs = getattr(gate, "proposal_iteration_artifacts", None)
    if not callable(proposal_refs):
        return False
    try:
        return bool(proposal_refs())
    except Exception:
        return False
def _peer_lanes_degraded_without_operational_blocks(prepared: list[dict[str, Any]]) -> bool:
    peers = [
        item
        for item in prepared
        if str(item.get("lane") or "") in {"gpu0_peer", "npu_micro_task_auditor"}
    ]
    if len(peers) < 2:
        return False
    for item in peers:
        completed = item.get("completed")
        if completed is None:
            return False
        report = item.get("provider_report")
        if isinstance(report, dict):
            if report.get("operational_provider_activity"):
                return False
            continue
        if getattr(completed, "returncode", 1) == 0:
            return False
    return True
def _peer_lane_statuses(prepared: list[dict[str, Any]]) -> list[dict[str, Any]]:
    statuses: list[dict[str, Any]] = []
    for item in prepared:
        lane = str(item.get("lane") or "")
        if lane not in {"gpu0_peer", "npu_micro_task_auditor"}:
            continue
        report = item.get("provider_report")
        completed = item.get("completed")
        statuses.append(
            {
                "lane": lane,
                "completed": completed is not None,
                "returncode": getattr(completed, "returncode", None),
                "operational_provider_activity": (
                    report.get("operational_provider_activity")
                    if isinstance(report, dict)
                    else None
                ),
                "provider_activity_classification": (
                    report.get("provider_activity_classification")
                    if isinstance(report, dict)
                    else ""
                ),
            }
        )
    return statuses
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
            "failure_kind": item.get("failure_kind") or "",
            "output": repo_rel(gate.repo_root, Path(item["spec"]["output"])),
            "execution_mode": "concurrent_provider_teamwork",
        },
        target="orchestrator",
        correlation_id=str(item["correlation"]),
        round_id=round_id,
    )
