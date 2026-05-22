"""CLI for agent-review evidence sufficiency."""

from __future__ import annotations

from .report_cli_specs import run_report_tool


def main() -> int:
    return run_report_tool("evidence_sufficiency")
