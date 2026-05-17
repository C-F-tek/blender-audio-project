"""Data model for the unified validation gate."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GateStep:
    """One validation, smoke, or gate command registered centrally."""

    name: str
    suites: tuple[str, ...]
    command: list[str]
    outputs: tuple[str, ...] = ()
    timeout_seconds: int = 300
    heavy: bool = False
    provider_live: bool = False
    allow_nonzero: bool = False
    tags: tuple[str, ...] = field(default_factory=tuple)
