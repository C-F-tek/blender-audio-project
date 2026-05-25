"""Async GPU0/NPU sidecar helpers for the heap provider loop."""

from __future__ import annotations

import time

from ia_carmine.runtime.heap_gate.gpu1_closure_packet import (
    gpu1_decision_packet_valid,
)
from ia_carmine.runtime.heap_gate.provider_lane_launch import write_provider_launch_manifest
from ia_carmine.runtime.heap_gate.provider_process_collection import poll_provider_processes
from ia_carmine.runtime.heap_gate.provider_report_absorption import (
    absorb_completed_provider_item,
)
from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    Path,
    now_iso,
    subprocess,
    write_json_report,
)


def poll_pending_provider_sidecars(owner: Any, round_id: int) -> None:
    pending_collections = list(getattr(owner, "pending_provider_sidecar_collections", []) or [])
    if not pending_collections:
        return
    still_pending: list[dict[str, Any]] = []
    for collection in pending_collections:
        sidecar_items = collection.get("sidecar_items")
        if not isinstance(sidecar_items, list):
            continue
        launch_manifest = Path(collection.get("launch_manifest"))
        work_dir = Path(collection.get("work_dir"))
        revision = int(collection.get("revision") or 0)
        timeout_seconds = int(collection.get("timeout_seconds") or owner.args.timeout_seconds)
        prepared = collection.get("prepared") if isinstance(collection.get("prepared"), list) else sidecar_items
        time_contract = (
            collection.get("time_contract")
            if isinstance(collection.get("time_contract"), dict)
            else owner.provider_time_counter_contract()
        )

        def absorb(item: dict[str, Any]) -> None:
            absorb_completed_provider_item(
                owner,
                item,
                launch_manifest=launch_manifest,
                work_dir=work_dir,
                round_id=round_id,
                revision=revision,
                timeout_seconds=timeout_seconds,
            )

        pending_count = poll_provider_processes(
            owner,
            sidecar_items,
            timeout_seconds,
            round_id,
            revision,
            on_completed=absorb,
        )
        primary_items = (
            collection.get("primary_items")
            if isinstance(collection.get("primary_items"), list)
            else []
        )
        if not pending_count:
            owner.sidecar_alone_after_gpu1_seconds = gpu1_idle_after_primary_seconds(
                primary_items,
                sidecar_items,
            )
            owner.gpu1_idle_after_primary_seconds = owner.sidecar_alone_after_gpu1_seconds
        write_provider_launch_manifest(
            owner,
            launch_manifest,
            prepared,
            round_id,
            revision,
            time_contract,
            "async_sidecars_pending" if pending_count else "async_sidecars_collected",
        )
        if pending_count:
            still_pending.append(collection)
    owner.pending_provider_sidecar_collections = still_pending


def gpu1_packet_reviewable(
    packet: dict[str, Any],
    primary_status: dict[str, Any],
) -> tuple[bool, str]:
    if (
        packet.get("gpu1_resume_after_tool_result_required") is True
        or primary_status.get("gpu1_resume_after_tool_result_required") is True
    ):
        blocker = str(
            packet.get("gpu1_tool_result_blocker")
            or primary_status.get("gpu1_tool_result_blocker")
            or "gpu1_tool_result_pending"
        )
        return False, f"gpu1_packet_not_reviewable:{blocker}"
    if not gpu1_decision_packet_valid(packet):
        errors = packet.get("packet_errors") if isinstance(packet.get("packet_errors"), list) else []
        reason = ",".join(str(item) for item in errors if str(item).strip())
        return False, f"gpu1_packet_not_reviewable:{reason or 'invalid_packet'}"
    if primary_status.get("gpu1_primary_workload_valid") is not True:
        return False, "gpu1_packet_not_reviewable:primary_workload_missing"
    if str(packet.get("gpu1_decision") or "") == "needs_refine":
        return False, "gpu1_packet_not_reviewable:gpu1_self_refine_required"
    return True, ""


def mark_sidecars_skipped(
    owner: Any,
    sidecar_items: list[dict[str, Any]],
    *,
    launch_manifest: Path,
    work_dir: Path,
    round_id: int,
    revision: int,
    timeout_seconds: int,
    reason: str,
    packet: dict[str, Any],
    absorb: Any,
) -> None:
    for item in sidecar_items:
        if item.get("absorbed"):
            continue
        spec = item["spec"]
        output = Path(spec["output"])
        lane = str(item.get("lane") or spec.get("lane") or "")
        report = {
            "schema_version": 1,
            "kind": "provider_sidecar_skipped",
            "lane": lane,
            "provider_id": lane,
            "provider_role": spec.get("provider_role") or spec.get("role"),
            "requirement": item.get("requirement") or spec.get("requirement"),
            "revision": revision,
            "passed": False,
            "status": "skipped",
            "process_status": "skipped",
            "work_status": "skipped_no_reviewable_gpu1_packet",
            "diagnostic_only": True,
            "provider_work_verified": False,
            "provider_role_counted": False,
            "provider_execution_performed": False,
            "provider_execution_attempted": False,
            "provider_execution_claim_seen": False,
            "provider_io_observed": False,
            "operational_provider_activity": False,
            "provider_replight_required": False,
            "replight_passed": True,
            "sidecar_lane": True,
            "sidecar_scope_mode": "packet_review_only",
            "sidecar_scope_contract": spec.get("sidecar_scope_contract") or "",
            "sidecar_skipped": True,
            "sidecar_skipped_reason": reason,
            "sidecar_invalid": False,
            "sidecar_incongruent": False,
            "provider_rejection_reason": reason,
            "product_blocked_reason": reason,
            "sidecar_target_pointer": packet.get("gpu1_block_id") if isinstance(packet, dict) else "",
            "gpu1_closure_decision_packet": packet if isinstance(packet, dict) else {},
            "gpu1_closure_decision_packet_valid": gpu1_decision_packet_valid(packet),
            "gpu1_closure_decision_packet_fingerprint": (
                packet.get("packet_fingerprint") if isinstance(packet, dict) else ""
            ),
        }
        write_json_report(report, output)
        now = now_iso()
        item["completed"] = subprocess.CompletedProcess(
            list(item.get("command") or []),
            returncode=0,
            stdout="",
            stderr=f"provider sidecar skipped: {reason}",
        )
        item["started_at"] = item.get("started_at") or now
        item["completed_at"] = now
        item["started_perf"] = item.get("started_perf") or time.perf_counter()
        item["completed_perf"] = time.perf_counter()
        item["elapsed_seconds"] = 0.0
        absorb_completed_provider_item(
            owner,
            item,
            launch_manifest=launch_manifest,
            work_dir=work_dir,
            round_id=round_id,
            revision=revision,
            timeout_seconds=timeout_seconds,
        )
        try:
            absorb(item)
        except Exception as exc:  # noqa: BLE001 - skip evidence must not block GPU1.
            item["absorb_error"] = f"{type(exc).__name__}: {exc}"


def gpu1_idle_after_primary_seconds(
    primary_items: list[dict[str, Any]],
    sidecar_items: list[dict[str, Any]],
) -> float:
    primary_done = max(
        (
            float(item.get("completed_perf") or 0.0)
            for item in primary_items
            if item.get("completed_perf") is not None
        ),
        default=0.0,
    )
    sidecar_done = max(
        (
            float(item.get("completed_perf") or 0.0)
            for item in sidecar_items
            if item.get("completed_perf") is not None
        ),
        default=0.0,
    )
    if not primary_done or not sidecar_done:
        return 0.0
    return round(max(0.0, sidecar_done - primary_done), 6)
