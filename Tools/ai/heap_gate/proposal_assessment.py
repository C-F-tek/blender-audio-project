"""Proposal parallel-cycle assessment helpers."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import Any


def build_heap_parallel_cycle_assessment(
    *,
    owner: Any,
    revision: int,
    source: str,
    deterministic_reviews: dict[str, Any],
    npu_audit: dict[str, Any],
) -> dict[str, Any]:
    gpu0_review = deterministic_reviews.get("gpu0_review")
    npu_piece = deterministic_reviews.get("npu_micro_task_piece")
    provider_report_lanes: list[str] = []
    for report in owner.provider_reports:
        lane = str(report.get("lane") or report.get("role") or report.get("kind") or "")
        if lane and lane not in provider_report_lanes:
            provider_report_lanes.append(lane)
    gpu1_present = str(source or "").lower().startswith("gpu1")
    gpu0_present = bool(gpu0_review) or any(
        "gpu0" in lane.lower() for lane in provider_report_lanes
    )
    npu_present = (
        bool(npu_piece)
        or bool(npu_audit)
        or any("npu" in lane.lower() for lane in provider_report_lanes)
    )
    npu_workload_ok = not npu_audit or bool(
        npu_audit.get("passed") and npu_audit.get("performed")
    )
    missing: list[str] = []
    if not gpu1_present:
        missing.append("gpu1_provider_planner")
    if not gpu0_present:
        missing.append("gpu0_companion_review")
    if not npu_present:
        missing.append("npu_micro_task_audit")
    if npu_present and not npu_workload_ok:
        missing.append("npu_workload_passed")
    return {
        "schema_version": 1,
        "kind": "heap_parallel_cycle_assessment",
        "stamp": owner.stamp,
        "revision": revision,
        "passed": not missing,
        "policy": "Proposal acceptance requires same-heap GPU1 proposal, GPU0 review/refine and NPU audit.",
        "gpu1_present": gpu1_present,
        "gpu0_present": gpu0_present,
        "npu_present": npu_present,
        "npu_workload_ok": npu_workload_ok,
        "provider_report_lanes": provider_report_lanes,
        "missing_lanes": missing,
        "provider_execution_performed": bool(owner.provider_execution_performed),
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
