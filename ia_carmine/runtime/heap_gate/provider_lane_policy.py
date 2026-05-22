"""Provider lane authority and revision selection policy."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import Any

PRIMARY_LANE = "gpu1_planner"
GPU0_LANE = "gpu0_peer"
NPU_LANE = "npu_micro_task_auditor"

LANE_POLICY_KEYS = (
    "sidecar_join_after_primary_seconds",
    "closure_owner",
    "primary_closer",
    "sidecar_lane",
    "micro_audit_only",
    "reviewer_refiner",
    "native_tool_calling_policy",
    "delta_context_mode",
    "npu_micro_timeout_enforced",
)


def lane_policy_payload(source: dict[str, Any]) -> dict[str, Any]:
    return {key: source.get(key) for key in LANE_POLICY_KEYS}


def valid_npu_micro_audit_available(provider_reports: list[dict[str, Any]]) -> bool:
    for report in reversed(provider_reports):
        if report.get("lane") != NPU_LANE:
            continue
        return bool(
            report.get("passed")
            and (
                report.get("npu_peer_activity_performed")
                or report.get("npu_micro_provider_execution_performed")
                or report.get("npu_provider_execution_performed")
                or report.get("operational_provider_activity")
            )
        )
    return False


def provider_lanes_for_revision(owner: Any, revision: int) -> set[str]:
    if revision <= 0:
        selected = {PRIMARY_LANE, GPU0_LANE, NPU_LANE}
        reason = "initial_teamwork_all_lanes"
    elif bool(getattr(owner, "skip_npu_on_soft_lock_targeted_refine", False)):
        selected = {PRIMARY_LANE, GPU0_LANE}
        reason = "soft_lock_targeted_refine_gpu1_gpu0_only_npu_advisory_inherited"
    elif not valid_npu_micro_audit_available(owner.provider_reports):
        selected = {PRIMARY_LANE, GPU0_LANE, NPU_LANE}
        reason = "revision_needs_missing_npu_micro_audit"
    else:
        selected = {PRIMARY_LANE, GPU0_LANE}
        reason = "revision_uses_inherited_npu_micro_audit"
    owner.provider_revision_lane_policy = {
        "revision": revision,
        "reason": reason,
        "selected_lanes": sorted(selected),
        "closure_owner": PRIMARY_LANE,
        "gpu0_role": "reviewer_refiner_not_primary_closer",
        "npu_role": "micro_audit_only_not_primary_closer",
    }
    return selected
