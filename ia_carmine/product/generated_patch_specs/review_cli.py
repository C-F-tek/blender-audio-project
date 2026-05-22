"""CLI for reviewed patch-spec promotion."""

from __future__ import annotations

from .cli_specs import run_review_cli


def main() -> int:
    return run_review_cli()
