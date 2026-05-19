"""Provider block contract helpers for same-heap provider reports."""

from __future__ import annotations

from typing import Any


def proposal_block_id_for_revision(stamp: str, revision: int) -> str:
    return f"{stamp}:proposal:{int(revision):03d}"


def provider_block_contract(
    stamp: str,
    lane: str,
    revision: int,
    provider_report: dict[str, Any],
) -> dict[str, Any]:
    proposal_block_id = proposal_block_id_for_revision(stamp, revision)
    lane_key = str(lane or "provider").strip() or "provider"
    provider_block_id = f"{stamp}:{lane_key}:{int(revision):03d}"
    if lane_key == "gpu0_peer":
        role = "gpu0_reviewer_refiner"
        block_type = "review_refinement_block"
        pointer_action = "REFINE"
        refines = proposal_block_id
        resume = proposal_block_id
    elif lane_key == "npu_micro_task_auditor":
        role = "npu_auditor"
        block_type = "audit_block"
        pointer_action = "AUDIT"
        refines = proposal_block_id
        resume = proposal_block_id
    elif lane_key == "gpu1_planner":
        role = "gpu1_planner"
        block_type = "provider_proposal_block"
        pointer_action = "PROPOSE"
        refines = ""
        resume = proposal_block_id
    else:
        role = str(provider_report.get("role") or lane_key)
        block_type = "provider_evidence_block"
        pointer_action = "EVIDENCE"
        refines = ""
        resume = proposal_block_id
    target_files = provider_report.get("target_files")
    if not isinstance(target_files, list):
        target_files = []
    operational, classification = operational_provider_activity(lane_key, provider_report)
    return {
        "heap_block": operational,
        "operational_provider_activity": operational,
        "provider_activity_classification": classification,
        "block_id": provider_block_id,
        "provider_block_id": provider_block_id,
        "proposal_block_id": proposal_block_id,
        "revision": int(revision),
        "role": role,
        "block_type": block_type,
        "previous_block_id": "",
        "next_block_id": "",
        "refines_block_id": refines,
        "resume_from_block_id": resume,
        "pointer_action": pointer_action,
        "target_files": [str(item) for item in target_files if str(item).strip()],
        "decision": "accept" if operational and provider_report.get("passed") else "blocked",
        "exit_decision": (
            "PATCHABLE_TARGET"
            if target_files and operational and provider_report.get("passed")
            else "BLOCKED"
        ),
    }


def operational_provider_activity(
    lane: str,
    provider_report: dict[str, Any],
) -> tuple[bool, str]:
    response_text = str(provider_report.get("response_text") or "").strip()
    selected_model = str(provider_report.get("selected_model") or "").strip()
    tool_call_count = _safe_int(provider_report.get("native_tool_call_count"))
    tool_calls = provider_report.get("tool_calls") if isinstance(provider_report.get("tool_calls"), list) else []
    semantic_done = bool(provider_report.get("semantic_provider_execution_performed"))
    native_done = bool(provider_report.get("native_tool_loop_performed"))
    classification = str(
        provider_report.get("native_tool_loop_classification")
        or provider_report.get("semantic_provider_classification")
        or ""
    )
    lowered_classification = classification.lower()
    if any(marker in lowered_classification for marker in ("salvaged", "incomplete", "timeout", "failed", "error")):
        return False, f"non_operational_classification:{classification or 'unknown'}"
    if any("salvaged" in str(call.get("reason") or "").lower() for call in tool_calls if isinstance(call, dict)):
        return False, "non_operational_salvaged_tool_call"
    if lane == "gpu1_planner":
        if not selected_model:
            return False, "gpu1_missing_selected_model"
        if _contains_heap_contract_text(response_text):
            return True, "gpu1_heap_delta_proposal_present"
        if tool_call_count > 0:
            return False, "gpu1_tool_call_without_heap_delta_proposal"
        return False, "gpu1_no_heap_delta_or_native_tool_call"
    if lane in {"gpu0_peer", "npu_micro_task_auditor"}:
        if not semantic_done or not native_done:
            return False, f"{lane}_semantic_tool_loop_not_performed"
        if tool_call_count > 0 or _contains_review_or_audit_text(response_text):
            return True, f"{lane}_semantic_review_or_native_tool_call"
        return False, f"{lane}_no_review_audit_or_native_tool_call"
    return bool(response_text or tool_call_count > 0), "generic_provider_activity"


def _contains_heap_contract_text(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in ("# heap_delta_proposal", "exit_decision", "target_files", "implementation_changes", "patch_sketch"))


def _contains_review_or_audit_text(text: str) -> bool:
    lowered = text.lower()
    if any(marker in lowered for marker in ("review", "audit", "refine", "reject", "accept", "veto", "tool call", "tool_call")):
        return True
    if any(marker in lowered for marker in ("micro-task eseguita", "workload", "device", "available_devices")):
        return False
    return len(text) >= 120 and any(marker in lowered for marker in ("evidence", "target", "guardrail", "validation"))


def _safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0
