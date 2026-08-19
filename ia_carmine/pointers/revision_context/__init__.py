"""IA-Carmine revision pointer anchoring for heap execution history."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RevisionPointer:
    """Revision pointer context with anchor information for heap blocks."""
    
    # Block identifiers
    block_id: str = ""
    proposal_block_id: str = ""
    latest_block_id: str = ""
    
    # Pointer navigation fields
    previous_block_id: str = ""
    next_block_id: str = ""
    refines_block_id: str = ""
    resume_from_block_id: str = ""
    
    # Closure and quorum state
    closure_evidence_block_id: str = ""
    soft_lock_state: str = ""
    
    # Pointer action and decisions
    pointer_action: str = ""
    exit_decision: str = ""
    quality_passed: bool = False
    
    # Continuation flags
    continuation_required: bool = False
    product_blocked_reason: str = ""
    
    def get_anchor_block_id(self) -> str:
        """Return the primary anchor block ID for this revision."""
        return self.block_id or self.proposal_block_id or ""
    
    def get_resume_anchor(self) -> str:
        """Return the resume anchor block ID for continuation after rewrite."""
        return self.resume_from_block_id or self.latest_block_id or self.proposal_block_id or ""
    
    def has_backward_pointer(self) -> bool:
        """Check if this revision has a backward pointer (previous or refines)."""
        return bool(self.previous_block_id or self.refines_block_id)
    
    def has_forward_pointer(self) -> bool:
        """Check if this revision has a forward pointer (next or resume_from)."""
        return bool(self.next_block_id or self.resume_from_block_id)
    
    def get_pointer_action_type(self) -> str:
        """Return the type of pointer action for this revision."""
        action = self.pointer_action.upper() if self.pointer_action else ""
        if action in ("PROPOSE", "EVIDENCE"):
            return "STAY_FORWARD"
        elif action in ("REFINE", "AUDIT"):
            return "BACKTRACK_PROPAGATE"
        elif action == "RESUME_FORWARD":
            return "RESUME_FORWARD"
        return action or "UNKNOWN"


def build_revision_pointer(
    revision_context: dict[str, Any],
    latest_report: dict[str, Any] | None = None,
) -> RevisionPointer:
    """Build a RevisionPointer from revision context and optional latest report."""
    block_id = str(revision_context.get("block_id") or "")
    proposal_block_id = str(revision_context.get("proposal_block_id") or "")
    latest_block_id = str(revision_context.get("latest_block_id") or "")
    
    previous_block_id = str(revision_context.get("previous_block_id") or "")
    next_block_id = str(revision_context.get("next_block_id") or "")
    refines_block_id = str(revision_context.get("refines_block_id") or "")
    resume_from_block_id = str(revision_context.get("resume_from_block_id") or "")
    
    closure_evidence_block_id = str(revision_context.get("closure_evidence_block_id") or "")
    soft_lock_state = str(revision_context.get("soft_lock_state") or "")
    
    pointer_action = str(revision_context.get("pointer_action") or "")
    exit_decision = str(revision_context.get("exit_decision") or "")
    quality_passed = bool(revision_context.get("quality_passed")) if "quality_passed" in revision_context else False
    
    continuation_required = bool(revision_context.get("continuation_required"))
    product_blocked_reason = str(revision_context.get("product_blocked_reason") or "")
    
    # Fallback to latest report if available
    if latest_report:
        if not block_id:
            block_id = str(latest_report.get("block_id") or "")
        if not proposal_block_id:
            proposal_block_id = str(latest_report.get("proposal_block_id") or "")
        if not latest_block_id:
            latest_block_id = str(latest_report.get("latest_block_id") or "")
        if not previous_block_id:
            previous_block_id = str(latest_report.get("previous_block_id") or "")
        if not next_block_id:
            next_block_id = str(latest_report.get("next_block_id") or "")
        if not refines_block_id:
            refines_block_id = str(latest_report.get("refines_block_id") or "")
        if not resume_from_block_id:
            resume_from_block_id = str(latest_report.get("resume_from_block_id") or "")
        if not closure_evidence_block_id:
            closure_evidence_block_id = str(latest_report.get("closure_evidence_block_id") or "")
        if not soft_lock_state:
            soft_lock_state = str(latest_report.get("soft_lock_state") or "")
        if not pointer_action:
            pointer_action = str(latest_report.get("pointer_action") or "")
        if not exit_decision:
            exit_decision = str(latest_report.get("exit_decision") or "")
    
    return RevisionPointer(
        block_id=block_id,
        proposal_block_id=proposal_block_id,
        latest_block_id=latest_block_id,
        previous_block_id=previous_block_id,
        next_block_id=next_block_id,
        refines_block_id=refines_block_id,
        resume_from_block_id=resume_from_block_id,
        closure_evidence_block_id=closure_evidence_block_id,
        soft_lock_state=soft_lock_state,
        pointer_action=pointer_action,
        exit_decision=exit_decision,
        quality_passed=quality_passed,
        continuation_required=continuation_required,
        product_blocked_reason=product_blocked_reason,
    )


def extract_pointer_fields(revision_context: dict[str, Any]) -> dict[str, str]:
    """Extract pointer navigation fields from a revision context dictionary."""
    return {
        "previous_block_id": str(revision_context.get("previous_block_id") or ""),
        "next_block_id": str(revision_context.get("next_block_id") or ""),
        "refines_block_id": str(revision_context.get("refines_block_id") or ""),
        "resume_from_block_id": str(revision_context.get("resume_from_block_id") or ""),
        "proposal_block_id": str(revision_context.get("proposal_block_id") or ""),
        "latest_block_id": str(revision_context.get("latest_block_id") or ""),
    }


def build_pointer_contract(
    revision_pointer: RevisionPointer | dict[str, Any],
) -> dict[str, Any]:
    """Build a pointer contract dictionary from a RevisionPointer or context."""
    if isinstance(revision_pointer, dict):
        resume_from = str(revision_pointer.get("resume_from_block_id") or "")
        latest_id = str(revision_pointer.get("latest_block_id") or "")
        proposal_id = str(revision_pointer.get("proposal_block_id") or "")
        
        return {
            "product_contract": True,
            "decision_recovery": True,
            "navigation_role": "provider_evidence_chain",
            "closure_owner": bool(resume_from or latest_id),
            "primary_closer": bool(proposal_id),
            "sidecar_evidence": False,
            "can_continue_to_next": bool(latest_id or resume_from),
            "can_backrefine": bool(revision_pointer.get("previous_block_id") or revision_pointer.get("refines_block_id")),
            "requires_review": True,
        }
    
    return {
        "product_contract": True,
        "decision_recovery": True,
        "navigation_role": "provider_evidence_chain",
        "closure_owner": bool(revision_pointer.resume_from_block_id or revision_pointer.latest_block_id),
        "primary_closer": bool(revision_pointer.proposal_block_id),
        "sidecar_evidence": False,
        "can_continue_to_next": bool(revision_pointer.latest_block_id or revision_pointer.resume_from_block_id),
        "can_backrefine": bool(revision_pointer.previous_block_id or revision_pointer.refines_block_id),
        "requires_review": True,
    }


__all__ = [
    "RevisionPointer",
    "build_revision_pointer",
    "extract_pointer_fields",
    "build_pointer_contract",
]