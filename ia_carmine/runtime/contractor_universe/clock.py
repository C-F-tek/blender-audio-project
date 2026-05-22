"""Logical clock for bounded contractor-universe runs."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from ia_carmine.runtime.heap_gate.provider_time import build_provider_time_counter_contract


@dataclass
class LogicalClock:
    budget_seconds: int
    soft_close_after_seconds: int
    tick_seconds: float = 1.0
    tick: int = 0
    started_at: float = 0.0
    time_counter_contract: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_args(cls, args: Any) -> LogicalClock:
        contract = build_provider_time_counter_contract(args)
        return cls(
            budget_seconds=int(contract["budget_counter_seconds"]),
            soft_close_after_seconds=int(contract["soft_close_after_seconds"]),
            tick_seconds=float(contract["counter_tick_seconds"]),
            started_at=time.monotonic(),
            time_counter_contract=contract,
        )

    @property
    def elapsed_seconds(self) -> float:
        return max(0.0, time.monotonic() - self.started_at)

    @property
    def soft_close_due(self) -> bool:
        return self.elapsed_seconds >= self.soft_close_after_seconds

    def advance(self) -> None:
        self.tick += 1
