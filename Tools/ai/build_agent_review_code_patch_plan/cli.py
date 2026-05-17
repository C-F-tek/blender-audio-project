#!/usr/bin/env python3
"""Compatibility entrypoint for agent-review code patch plans."""

from __future__ import annotations

from agent_review.code_patch_plan_cli import main


if __name__ == "__main__":
    raise SystemExit(main())
