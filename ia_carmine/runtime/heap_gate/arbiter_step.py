"""Arbiter step helper for the heap runtime gate."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.arbiter_product import (
    build_arbiter_product,
    publish_candidate_operation,
)
from ia_carmine.runtime.heap_gate.generic_write_followup import (
    generic_write_document_product_eligible,
    generic_write_followup_pending_count,
)
from ia_carmine.runtime.heap_gate.pointer_soft_lock import runtime_soft_lock_state
from ia_carmine.runtime.heap_gate.runtime_common import Any, append_unique, safe_dict


def run_arbiter_step(owner: Any, round_id: int, events: list[dict[str, Any]]) -> None:
    if owner.state["decisions"]:
        return
    missing = owner.missing_requirements(events)
    unattempted = owner.next_unattempted_plan_item(events)
    ready = not missing
    bridge_refs = owner.bridge_report_refs(events)
    effective_tool_execution_count = owner.effective_tool_execution_count(events)
    generic_product_ready = generic_write_document_product_eligible(owner, events)
    if ready and effective_tool_execution_count <= 0:
        missing = [*missing, "broker_tool_execution"]
        ready = False
    if ready and not bridge_refs:
        missing = [*missing, "broker_bridge_reports"]
        ready = False
    if ready and owner.request_text() and not owner.response_text_complete() and not generic_product_ready:
        missing = [*missing, "gpu1_request_response_complete"]
        ready = False
    file_quality = owner.response_file_reference_quality(owner.response_text())
    if ready and not file_quality.get("passed") and not generic_product_ready:
        missing = [*missing, "verified_unambiguous_source_refs"]
        ready = False
    soft_lock_state = runtime_soft_lock_state(owner, events)
    if ready and int(soft_lock_state.get("open_pointer_count_final") or 0) > 0:
        missing = [*missing, "open_pointer_closure"]
        ready = False
    closure_quorum_status = str(soft_lock_state.get("closure_quorum_status") or "")
    closure_can_exit = closure_quorum_status in {
        "ready_to_close",
        "blocked_continuation_ready",
        "blocked_with_reason",
    }
    if (
        ready
        and owner.detailed_output_expected()
        and not owner.quality_output_passed(owner.response_text(), events)
        and not generic_product_ready
    ):
        missing = [*missing, "provider_quality_output"]
        ready = False
    generic_pending = generic_write_followup_pending_count(owner, events)
    if ready and generic_pending:
        missing = [*missing, "generic_write_followup_pending"]
        ready = False
    budget_exhausted = bool(getattr(owner, "runtime_soft_close_reached", lambda: False)())
    no_more_progress = unattempted is None and bool(missing)
    refinement_possible = (
        owner.detailed_output_expected()
        and owner.provider_reports
        and owner.proposal_cycle_requires_refinement(owner.response_text(), events)
    )
    if not ready and refinement_possible and not closure_can_exit:
        return
    if not ready and not budget_exhausted and not no_more_progress and not closure_can_exit:
        return
    if closure_quorum_status == "blocked_continuation_ready":
        missing = list(dict.fromkeys([*missing, "blocked_continuation_product"]))
    elif closure_quorum_status == "blocked_with_reason":
        reason = str(soft_lock_state.get("closure_quorum_reason") or "")
        if reason:
            missing = list(dict.fromkeys([*missing, reason]))
    if not ready and not budget_exhausted and not no_more_progress and not closure_can_exit:
        return
    status = "ready" if ready else "blocked_with_reason"
    product_kind = _product_kind(ready, generic_product_ready, closure_quorum_status)
    decision = {
        "id": "heap_completeness_gate_decision",
        "from": "arbiter",
        "decision": ("product_ready_heap_complete" if ready else "blocked_with_reason"),
        "evidence_refs": [
            "heap:task_state",
            "heap:broker_result",
            "heap:shared_evidence",
            "heap:validation_signal",
            *bridge_refs[-4:],
        ],
        "completed_requirements": sorted(owner.completed_requirements(events)),
        "missing_requirements": missing,
        "budget_exhausted": budget_exhausted,
        "budget_decision": owner.budget_governor.get("decision"),
        "invocation_gate_decision": safe_dict(owner.invocation_contract.get("real_run_gate")).get("decision"),
        "provider_generation_permit_allowed": owner.budget_governor.get("permit_allowed"),
        "product_kind": product_kind,
        **soft_lock_state,
    }
    append_unique(owner.state["decisions"], decision)
    owner.decision_count += 1
    owner.publish(
        "deterministic",
        "decision",
        decision,
        target="orchestrator",
        correlation_id=f"{owner.stamp}:decision",
        round_id=round_id,
    )
    publish_candidate_operation(owner, ready=ready, missing=missing, round_id=round_id)
    owner.state["product"] = build_arbiter_product(
        owner,
        events,
        ready=ready,
        product_kind=product_kind,
        status=status,
        missing=missing,
        budget_exhausted=budget_exhausted,
        bridge_refs=bridge_refs,
        effective_tool_execution_count=effective_tool_execution_count,
        soft_lock_state=soft_lock_state,
    )
    owner.publish(
        "orchestrator",
        "product_signal",
        owner.state["product"],
        correlation_id=f"{owner.stamp}:product",
        round_id=round_id,
    )


def _product_kind(ready: bool, generic_ready: bool, closure_quorum_status: str) -> str:
    if ready and generic_ready:
        return "generic_write_refined_product"
    if ready:
        return "final_product_approved"
    if closure_quorum_status == "blocked_continuation_ready":
        return "blocked_continuation_product"
    return "blocked_with_reason"
