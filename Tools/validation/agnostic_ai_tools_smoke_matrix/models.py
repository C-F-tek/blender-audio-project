"""Data model for agnostic AI tools smoke matrix."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

COMMON_JSON_FIELDS = ("schema_version", "kind", "passed")

@dataclass(frozen=True)
class SmokeStep:
    """One sequential smoke test step."""

    name: str
    command: list[str]
    expected_outputs: list[str]
    required_fields: tuple[str, ...] = COMMON_JSON_FIELDS
    expected_values: dict[str, Any] = field(default_factory=dict)
    expected_values_by_output: dict[str, dict[str, Any]] = field(default_factory=dict)
    required_fields_by_output: dict[str, tuple[str, ...]] = field(default_factory=dict)
    allow_nonzero: bool = False
    heavy: bool = False
    provider_live: bool = False
    workflow: bool = False
