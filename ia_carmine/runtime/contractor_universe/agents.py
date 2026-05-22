"""Deterministic contractor agents for the initial runtime."""

from __future__ import annotations

from dataclasses import dataclass

from .clock import LogicalClock
from .heap import UniverseHeap
from .models import ContractorRole, HeapItem, TurnResult


@dataclass(frozen=True)
class DeterministicBackend:
    """Local backend used until real provider adapters leave evidence."""

    def proposal(self, request_text: str) -> dict[str, object]:
        concrete = any(token in request_text for token in ("Tools/", ".py", ".md"))
        return {
            "summary": "deterministic proposal placeholder pending real provider adapter",
            "concrete_target_detected": concrete,
            "target_files": [],
            "provider_execution_performed": False,
        }


class StrategistAgent:
    role = ContractorRole.STRATEGIST

    def __init__(self, backend: DeterministicBackend):
        self.backend = backend

    def run_turn(
        self, item: HeapItem, heap: UniverseHeap, clock: LogicalClock
    ) -> TurnResult:
        proposal = self.backend.proposal(str(item.payload.get("request") or ""))
        block_id = f"gpu1_{item.sequence}"
        heap.record_block(block_id=block_id, item=item, status="proposal_evidence", payload=proposal)
        heap.blackboard.add_event(
            "provider_evidence",
            lane="gpu1",
            payload={
                "block_id": block_id,
                "role": self.role.value,
                "provider_execution_performed": False,
                "evidence_class": "deterministic_local_proposal",
            },
        )
        next_items = (
            HeapItem(
                due_tick=clock.tick + 1,
                priority=10,
                sequence=item.sequence + 1000,
                role=ContractorRole.REVIEWER,
                kind="review",
                payload={"proposal_block_id": block_id},
                previous_block_id=block_id,
                refines_block_id=block_id,
                resume_from_block_id=block_id,
            ),
            HeapItem(
                due_tick=clock.tick + 1,
                priority=20,
                sequence=item.sequence + 2000,
                role=ContractorRole.AUDITOR,
                kind="audit",
                payload={"proposal_block_id": block_id},
                previous_block_id=block_id,
                refines_block_id=block_id,
                resume_from_block_id=block_id,
            ),
        )
        return TurnResult(block_id=block_id, status="proposal_evidence", next_items=next_items)


class ReviewerAgent:
    role = ContractorRole.REVIEWER

    def __init__(self, backend: DeterministicBackend):
        self.backend = backend

    def run_turn(
        self, item: HeapItem, heap: UniverseHeap, clock: LogicalClock
    ) -> TurnResult:
        block_id = f"gpu0_{item.sequence}"
        payload = {
            "proposal_block_id": item.payload.get("proposal_block_id", ""),
            "decision": "requires_real_provider_adapter_before_product",
            "provider_execution_performed": False,
        }
        heap.record_block(block_id=block_id, item=item, status="review_evidence", payload=payload)
        heap.blackboard.add_event("lane_evidence", lane="gpu0", payload=payload)
        return TurnResult(block_id=block_id, status="review_evidence")


class AuditorAgent:
    role = ContractorRole.AUDITOR

    def __init__(self, backend: DeterministicBackend):
        self.backend = backend

    def run_turn(
        self, item: HeapItem, heap: UniverseHeap, clock: LogicalClock
    ) -> TurnResult:
        block_id = f"npu_{item.sequence}"
        payload = {
            "proposal_block_id": item.payload.get("proposal_block_id", ""),
            "telemetry_enabled": False,
            "validation_enabled": False,
            "soft_close_due": clock.soft_close_due,
            "decision": "blocked_until_real_provider_or_reviewable_product",
        }
        heap.record_block(block_id=block_id, item=item, status="audit_evidence", payload=payload)
        heap.blackboard.add_event("lane_evidence", lane="npu", payload=payload)
        return TurnResult(
            block_id=block_id,
            status="audit_evidence",
            blocked_reason="real provider adapter and reviewable product are not wired",
        )
