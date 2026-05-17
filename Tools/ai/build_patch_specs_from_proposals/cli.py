#!/usr/bin/env python3
"""Compatibility entrypoint for proposal-derived patch specs."""

from __future__ import annotations

from generated_patch_specs.proposal_cli import main


if __name__ == "__main__":
    raise SystemExit(main())
