#!/usr/bin/env python3
"""Compatibility wrapper for agnostic AI tools smoke matrix."""

from __future__ import annotations

try:
    from agnostic_ai_tools_smoke_matrix.cli import main
except ImportError:
    from Tools.validation.agnostic_ai_tools_smoke_matrix.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
