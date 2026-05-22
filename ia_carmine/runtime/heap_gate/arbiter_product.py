"""Arbiter product payload assembly for the heap gate loop."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import Any, append_unique, repo_rel
from ia_carmine.runtime.heap_gate.generic_write_followup import generic_write_document_product


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
    generic_product = generic_write_document_product(owner, events)
    peer_reasons = []
    if int(generic_product.get("gpu0_peer_followup_pending_count") or 0) > 0:
        peer_reasons.append("gpu0_peer_followup_pending")
    if int(generic_product.get("npu_peer_followup_pending_count") or 0) > 0:
        peer_reasons.append("npu_peer_followup_pending")
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
        "request_input": owner.request_text(),
        "response_text": final_response_text,
        "response_source": owner.response_source(),
        "heap_event_refs": [repo_rel(owner.repo_root, owner.heap.paths.events)],
        "provider_refs": owner.provider_refs(),
        "provider_response_texts": owner.provider_response_texts(),
        "context_artifact_refs": owner.broker_output_refs(events),
        "generic_write_document_product": generic_product,
        "generic_write_refined_product": generic_product,
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
        "gpu0_audit": owner.provider_response_text("gpu0_peer"),
        "npu_audit": owner.provider_response_text("npu_micro_task_auditor"),
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
