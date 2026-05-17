#!/usr/bin/env python3
"""Compatibility entrypoint for review PR preparation."""

from __future__ import annotations

from agent_review.review_pr_cli import main


if __name__ == "__main__":
    raise SystemExit(main())
