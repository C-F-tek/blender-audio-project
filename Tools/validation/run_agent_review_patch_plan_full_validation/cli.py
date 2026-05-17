#!/usr/bin/env python3
"""Compatibility wrapper for agent review patch-plan full validation."""

from __future__ import annotations

try:
    from agent_review_patch_plan_full_validation.cli import main
except ImportError:
    from Tools.validation.agent_review_patch_plan_full_validation.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
