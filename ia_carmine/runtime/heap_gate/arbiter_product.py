"""Arbiter product payload assembly for the heap gate loop."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import Any, append_unique, repo_rel
from ia_carmine.runtime.heap_gate.generic_write_followup import generic_write_document_product
from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import context_hierarchy_payload


def build_arbiter_product(
    owner: Any,
    events: list[dict[str, Any]],
    *,
    ready: bool,
    product_kind: str,
    status: str,
    missing: list[str],
    budget_exhausted: bool,
    bridge_refs: list[str],
    effective_tool_execution_count: int,
    soft_lock_state: dict[str, Any],
) -> dict[str, Any]:
    final_response_text = owner.build_final_response_text(events)
    request_input_evidence = owner.request_input_ref_or_tail()
    final_response_evidence = owner.response_text_ref_or_tail(
        final_response_text,
        name="arbiter_response_text",
        kind="arbiter_response_text",
        producer="heap_arbiter",
    )
    provider_response_evidence = owner.provider_response_refs_or_tails()
    gpu0_audit_evidence = provider_response_evidence.get("gpu0_peer") or {}
    npu_audit_evidence = provider_response_evidence.get("npu_micro_task_auditor") or {}
    generic_product = generic_write_document_product(owner, events)
    peer_reasons = []
    if int(generic_product.get("gpu0_peer_followup_pending_count") or 0) > 0:
        peer_reasons.append("gpu0_peer_followup_pending")
    if int(generic_product.get("npu_peer_followup_pending_count") or 0) > 0:
        peer_reasons.append("npu_peer_followup_pending")
    if int(generic_product.get("generic_write_capture_failed_count") or 0) > 0:
        peer_reasons.append("generic_write_capture_failed")
    if bool(getattr(owner.args, "allow_provider_generation", False)):
        if context_hierarchy_payload(
            owner.args, gpu1_ctx=getattr(owner, "selected_ollama_num_ctx", None)
        ).get("context_hierarchy_valid") is not True:
            peer_reasons.append("context_hierarchy_invalid")
        if getattr(owner, "gpu1_primary_workload_valid", None) is False:
            peer_reasons.append("gpu1_primary_workload_missing")
        if getattr(owner, "gpu1_primary_evidence_valid", None) is False:
            peer_reasons.append("gpu1_primary_evidence_missing")
        if getattr(owner, "gpu1_leader_valid", None) is False:
            peer_reasons.append("gpu1_leader_missing")
        if (
            getattr(owner, "gpu1_boot_leader_ready", False) is True
            and str(getattr(owner, "sidecars_start_policy", "") or "")
            == "after_gpu1_residency_handshake"
            and float(getattr(owner, "parallel_provider_overlap_seconds", 0.0) or 0.0)
            <= 0.0
        ):
            peer_reasons.append("parallelism_lost_by_serial_leader_gate")
    blocked_reason = (
        ",".join(peer_reasons)
        or soft_lock_state.get("closure_quorum_reason")
        or owner.budget_governor.get("decision")
        or "heap loop stopped by budget/failed requirement before readiness"
    )
    return {
        "required": True,
        "product_kind": product_kind,
        "status": status,
        "product_status": status,
        **owner.prefixed_text_evidence_fields("request_input", request_input_evidence),
        **owner.prefixed_text_evidence_fields("response_text", final_response_evidence),
        "response_source": owner.response_source(),
        "heap_event_refs": [repo_rel(owner.repo_root, owner.heap.paths.events)],
        "provider_refs": owner.provider_refs(),
        "provider_response_refs_or_tails": provider_response_evidence,
        "context_artifact_refs": owner.broker_output_refs(events),
        "generic_write_refined_request": generic_product,
        "compat_legacy_generic_write_document_product": generic_product,
        "compat_legacy_generic_write_refined_product": generic_product,
        "bridge_reports": bridge_refs,
        "quality_output_signals": owner.quality_output_signals(final_response_text, events),
        "quality_output_passed": owner.quality_output_passed(final_response_text, events),
        "historical_tool_context_refs": owner.historical_tool_context_files(),
        "response_file_reference_quality": owner.response_file_reference_quality(
            owner.response_text()
        ),
        "provider_role_decisions": owner.provider_role_decisions(),
        "toolused": effective_tool_execution_count > 0,
        "shared_memory_written_and_used": "shared_memory" in owner.completed_requirements(events),
        "gpu0_audit_ref_or_tail": gpu0_audit_evidence,
        "npu_audit_ref_or_tail": npu_audit_evidence,
        "reason": (
            "heap loop consumed tool catalog, memory, current source chunks and provider product evidence"
            if ready
            else blocked_reason
        ),
        "product_blocked_reason": "" if ready else blocked_reason,
        "product_approval_status": "approved" if ready else "blocked",
        "product_approval_evidence": soft_lock_state,
        "continuation_required": product_kind == "blocked_continuation_product",
        "soft_close_reason": "" if ready else blocked_reason,
        "completed_requirements": sorted(owner.completed_requirements(events)),
        "missing_requirements": missing,
        "budget_exhausted": budget_exhausted,
        "budget_governor": owner.budget_governor.get("decision"),
        **soft_lock_state,
    }


def publish_candidate_operation(
    owner: Any,
    *,
    ready: bool,
    missing: list[str],
    round_id: int,
) -> None:
    candidate = {
        "id": "candidate_heap_runtime_product_flow",
        "kind": "design_operation",
        "path": "tools/workflow/run_unified_real_product_pr.ps1",
        "status": "ready_for_manual_review" if ready else "blocked",
        "rationale": (
            "gate proves heap/tool/memory/context/validation convergence before product readiness"
            if ready
            else "gate blocked because heap completeness requirements were not all satisfied within budget"
        ),
        "missing_requirements": missing,
    }
    append_unique(owner.state["candidate_operations"], candidate)
    owner.candidate_operation_count += 1
    owner.publish(
        "deterministic",
        "candidate_operation",
        candidate,
        target="orchestrator",
        correlation_id=f"{owner.stamp}:candidate",
        round_id=round_id,
    )
