"""IA-Carmine resume context and forward continuation logic for pointer system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ResumeContext:
    """Context for resuming heap execution after a rewrite or back-refinement."""
    
    resume_from_block_id: str = ""
    latest_block_id: str = ""
    proposal_block_id: str = ""
    
    # Pointer closure and quorum state
    closure_evidence_block_id: str = ""
    soft_lock_state: str = ""
    
    # Continuation flags
    continuation_required: bool = False
    product_blocked_reason: str = ""
    
    def get_resume_anchor(self) -> str:
        """Return the resume anchor block ID."""
        return self.resume_from_block_id or self.latest_block_id or self.proposal_block_id or ""
    
    def can_resume_forward(self) -> bool:
        """Check if forward continuation is possible from this context."""
        if not self.resume_from_block_id and not self.latest_block_id:
            return False
        if self.continuation_required and not self.product_blocked_reason:
            return True
        return bool(self.resume_from_block_id or self.latest_block_id)


def resume_anchor(
    revision_context: dict[str, Any],
    latest_report: dict[str, Any] | None = None,
) -> str:
    """Extract the resume anchor block ID from revision context or latest report."""
    if latest_report:
        resume_from = str(latest_report.get("resume_from_block_id") or "")
        if resume_from:
            return resume_from
    
    # Fallback to revision context
    resume_from = str(revision_context.get("resume_from_block_id") or "")
    if resume_from:
        return resume_from
    
    latest_id = str(revision_context.get("latest_block_id") or "")
    proposal_id = str(revision_context.get("proposal_block_id") or "")
    
    return resume_from or latest_id or proposal_id or ""


def can_resume_forward(
    context: ResumeContext | dict[str, Any],
) -> bool:
    """Check if forward continuation is possible from the given context."""
    if isinstance(context, dict):
        resume_from = str(context.get("resume_from_block_id") or "")
        latest_id = str(context.get("latest_block_id") or "")
        continuation_required = bool(context.get("continuation_required"))
        product_blocked_reason = str(context.get("product_blocked_reason") or "")
        
        if not resume_from and not latest_id:
            return False
        if continuation_required and not product_blocked_reason:
            return True
        return bool(resume_from or latest_id)
    
    return context.can_resume_forward() if hasattr(context, 'can_resume_forward') else False


def build_resume_context(
    revision_context: dict[str, Any],
    latest_report: dict[str, Any] | None = None,
) -> ResumeContext:
    """Build a ResumeContext from revision context and latest report data."""
    resume_from_block_id = str(revision_context.get("resume_from_block_id") or "")
    if not resume_from_block_id and latest_report:
        resume_from_block_id = str(latest_report.get("resume_from_block_id") or "")
    
    latest_block_id = str(revision_context.get("latest_block_id") or "")
    if not latest_block_id and latest_report:
        latest_block_id = str(latest_report.get("latest_block_id") or "")
    
    proposal_block_id = str(revision_context.get("proposal_block_id") or "")
    
    closure_evidence_block_id = str(revision_context.get("closure_evidence_block_id") or "")
    if not closure_evidence_block_id and latest_report:
        closure_evidence_block_id = str(latest_report.get("closure_evidence_block_id") or "")
    
    soft_lock_state = str(revision_context.get("soft_lock_state") or "")
    continuation_required = bool(revision_context.get("continuation_required"))
    product_blocked_reason = str(revision_context.get("product_blocked_reason") or "")
    
    return ResumeContext(
        resume_from_block_id=resume_from_block_id,
        latest_block_id=latest_block_id,
        proposal_block_id=proposal_block_id,
        closure_evidence_block_id=closure_evidence_block_id,
        soft_lock_state=soft_lock_state,
        continuation_required=continuation_required,
        product_blocked_reason=product_blocked_reason,
    )


__all__ = [
    "ResumeContext",
    "resume_anchor",
    "can_resume_forward",
    "build_resume_context",
]