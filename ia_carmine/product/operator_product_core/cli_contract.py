"""Shared CLI flag contract for operator heap runtime commands."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class HeapRuntimeFlags:
    allow_provider_generation: bool = True
    operator_intent: bool = True

    def as_argv(self) -> list[str]:
        argv: list[str] = []
        if self.allow_provider_generation:
            argv.append("--allow-provider-generation")
        if self.operator_intent:
            argv.append("--operator-intent")
        return argv


def provider_flags_from_selection(provider_selected: bool) -> HeapRuntimeFlags:
    selected = bool(provider_selected)
    return HeapRuntimeFlags(
        allow_provider_generation=selected,
        operator_intent=selected,
    )


def build_heap_runtime_argv(
    base_argv: Iterable[str],
    flags: HeapRuntimeFlags,
) -> list[str]:
    argv = list(base_argv)
    for flag in flags.as_argv():
        if flag not in argv:
            argv.append(flag)
    return argv
