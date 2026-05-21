"""Logical clock for bounded contractor-universe runs."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any


@dataclass
class LogicalClock:
    budget_seconds: int
    soft_close_after_seconds: int
    tick_seconds: float = 1.0
    tick: int = 0
    started_at: float = 0.0

    @classmethod
    def from_args(cls, args: Any) -> LogicalClock:
        budget_minutes = max(1, int(getattr(args, "budget_minutes", 10) or 10))
        budget_seconds = max(1, budget_minutes * 60)
        timeout = int(getattr(args, "timeout_seconds", 0) or 0)
        if timeout > 0:
            budget_seconds = min(budget_seconds, timeout)
        soft_close = max(1, int(budget_seconds * 0.8))
        return cls(
            budget_seconds=budget_seconds,
            soft_close_after_seconds=soft_close,
            started_at=time.monotonic(),
        )

    @property
    def elapsed_seconds(self) -> float:
        return max(0.0, time.monotonic() - self.started_at)

    @property
    def soft_close_due(self) -> bool:
        return self.elapsed_seconds >= self.soft_close_after_seconds

    def advance(self) -> None:
        self.tick += 1
