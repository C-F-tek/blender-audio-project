#!/usr/bin/env python3
"""Compatibility entrypoint for agent-review patch bundle builder."""

from __future__ import annotations

from agent_review.patch_bundle_cli import main


if __name__ == "__main__":
    raise SystemExit(main())
