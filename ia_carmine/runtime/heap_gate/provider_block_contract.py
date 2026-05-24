"""Provider block contract helpers for same-heap provider reports."""

from __future__ import annotations

from typing import Any
from ia_carmine._shared.provider_work_verification import provider_work_status
from ia_carmine.runtime.heap_gate.gpu0_secondary_decision import normalize_gpu0_decision


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
    if lane_key in {"gpu0_peer", "npu_micro_task_auditor"}:
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
    response_text = str(
        provider_report.get("response_text")
        or provider_report.get("response_text_tail")
        or ""
    ).strip()
    selected_model = str(provider_report.get("selected_model") or "").strip()
    tool_call_count = _safe_int(provider_report.get("native_tool_call_count"))
    tool_calls = provider_report.get("tool_calls") if isinstance(provider_report.get("tool_calls"), list) else []
    semantic_done = bool(provider_report.get("semantic_provider_execution_performed"))
    native_done = bool(provider_report.get("native_tool_loop_performed"))
    classification = str(
        provider_report.get("native_tool_loop_classification")
        or provider_report.get("npu_micro_provider_classification")
        or provider_report.get("semantic_provider_classification")
        or ""
    )
    if provider_report.get("provider_replight_required") is True and provider_report.get("replight_passed") is not True:
        return False, str(
            provider_report.get("replight_blocked_reason")
            or provider_report.get("product_blocked_reason")
            or f"provider_replight_failed:{lane}"
        )
    work_status = provider_work_status(lane=lane, report=provider_report)
    if not work_status["provider_work_verified"]:
        return False, str(work_status.get("provider_rejection_reason") or "provider_no_verified_workload")
    lowered_classification = classification.lower()
    npu_nonfatal_native_error = bool(
        lane == "npu_micro_task_auditor"
        and provider_report.get("npu_peer_evidence_verified")
        and not provider_report.get("npu_native_tool_loop_required")
    )
    if (
        any(marker in lowered_classification for marker in ("timeout", "failed", "error"))
        and not npu_nonfatal_native_error
    ):
        return False, f"non_operational_classification:{classification or 'unknown'}"
    incomplete_native_tool_call = "incomplete" in lowered_classification
    if "salvaged" in lowered_classification:
        return False, f"non_operational_classification:{classification or 'unknown'}"
    if any("salvaged" in str(call.get("reason") or "").lower() for call in tool_calls if isinstance(call, dict)):
        return False, "non_operational_salvaged_tool_call"
    if lane == "gpu1_planner":
        if provider_report.get("provider_execution_performed") is not True:
            return False, "gpu1_provider_execution_not_performed"
        if provider_report.get("provider_device_verified") is not True:
            return False, str(
                provider_report.get("product_blocked_reason")
                or provider_report.get("ollama_gpu_residency_status")
                or "gpu1_ollama_gpu_residency_unproven_or_cpu_bound"
            )
        if not selected_model:
            return False, "gpu1_missing_selected_model"
        if provider_report.get("response_likely_incomplete"):
            return True, "gpu1_heap_delta_proposal_incomplete_requires_refinement"
        if _contains_heap_contract_text(response_text):
            return True, "gpu1_heap_delta_proposal_present"
        if tool_call_count > 0:
            return True, "gpu1_structured_native_tool_call_present"
        return False, "gpu1_no_heap_delta_or_native_tool_call"
    if lane == "gpu0_peer":
        if str(provider_report.get("provider_backend") or "").lower() != "ollama":
            return False, "gpu0_ollama_vulkan_required"
        if provider_report.get("provider_device_verified") is not True:
            return False, str(
                provider_report.get("product_blocked_reason")
                or provider_report.get("provider_rejection_reason")
                or "gpu0_ollama_vulkan_unavailable"
            )
        if provider_report.get("device_identity_verified") is not True:
            return False, "gpu0_device_identity_unverified"
        if "gpu0-vulkan" not in str(provider_report.get("provider_compute_device") or ""):
            return False, "gpu0_ollama_vulkan_unavailable"
        if provider_report.get("gpu0_secondary_schema_valid") is not True:
            return False, "gpu0_secondary_schema_invalid"
        if normalize_gpu0_decision(provider_report.get("gpu0_decision")) not in {
            "congruent",
            "veto",
            "refine_required",
            "incongruent",
        }:
            return False, "gpu0_secondary_decision_invalid"
        if _has_peer_lane_evidence(lane, provider_report, response_text):
            if incomplete_native_tool_call:
                return False, f"{lane}_semantic_native_tool_call_incomplete"
            return True, f"{lane}_ollama_vulkan_review_or_native_tool_call"
        return False, f"{lane}_no_review_audit_or_native_tool_call"
    if lane == "npu_micro_task_auditor":
        if provider_report.get("provider_device_verified") is not True:
            return False, "npu_openvino_provider_unavailable"
        if (
            provider_report.get("npu_micro_provider_execution_performed") is not True
            and provider_report.get("npu_peer_evidence_verified") is not True
        ):
            return False, "npu_openvino_micro_provider_not_performed"
        if provider_report.get("npu_device_workload_performed") is not True:
            return False, "npu_openvino_device_workload_not_performed"
        if _has_peer_lane_evidence(lane, provider_report, response_text):
            if incomplete_native_tool_call and provider_report.get("npu_native_tool_loop_required"):
                return False, "npu_micro_task_tool_loop_incomplete"
            if provider_report.get("npu_peer_evidence_verified"):
                return True, "npu_peer_evidence_verified"
            return True, "npu_micro_task_provider_activity"
        return False, "npu_micro_task_provider_not_performed"
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


def _has_peer_lane_evidence(
    lane: str,
    provider_report: dict[str, Any],
    response_text: str,
) -> bool:
    if _contains_review_or_audit_text(response_text):
        return True
    if lane == "gpu0_peer":
        if str(provider_report.get("provider_backend") or "").lower() == "ollama":
            return bool(
                provider_report.get("provider_device_verified")
                and "gpu0-vulkan" in str(provider_report.get("provider_compute_device") or "")
                and (
                    provider_report.get("provider_execution_performed")
                    or provider_report.get("native_tool_loop_performed")
                    or provider_report.get("ollama_compute_verified")
                )
            )
        return False
    if lane == "npu_micro_task_auditor":
        if provider_report.get("npu_peer_evidence_verified"):
            return True
        return bool(
            provider_report.get("provider_device_verified")
            and (
                provider_report.get("npu_provider_execution_performed")
                or provider_report.get("npu_device_workload_performed")
            )
            and provider_report.get("npu_micro_provider_execution_performed")
        )
    return False


def _safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0
