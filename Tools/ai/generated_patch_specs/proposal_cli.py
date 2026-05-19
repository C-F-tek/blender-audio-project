"""CLI for proposal-derived patch specs."""

from __future__ import annotations

from .cli_specs import run_proposal_cli


def main() -> int:
    return run_proposal_cli()
