#!/usr/bin/env python3
"""Compatibility entrypoint for agent-review evidence sufficiency."""

from __future__ import annotations

from agent_review.evidence_cli import main


if __name__ == "__main__":
    raise SystemExit(main())
