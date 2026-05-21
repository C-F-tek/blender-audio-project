"""Data models for the contractor universe runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ContractorRole(str, Enum):
    STRATEGIST = "gpu1_planner"
    REVIEWER = "gpu0_reviewer_refiner"
    AUDITOR = "npu_auditor"


@dataclass(order=True, frozen=True)
class HeapItem:
    due_tick: int
    priority: int
    sequence: int
    role: ContractorRole = field(compare=False)
    kind: str = field(compare=False)
    payload: dict[str, Any] = field(default_factory=dict, compare=False)
    previous_block_id: str = field(default="", compare=False)
    refines_block_id: str = field(default="", compare=False)
    resume_from_block_id: str = field(default="", compare=False)


@dataclass(frozen=True)
class TurnResult:
    block_id: str
    status: str
    next_items: tuple[HeapItem, ...] = ()
    blocked_reason: str = ""
