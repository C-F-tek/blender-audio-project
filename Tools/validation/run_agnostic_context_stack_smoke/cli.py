#!/usr/bin/env python3
"""Compatibility wrapper for agnostic context stack smoke."""

from __future__ import annotations

try:
    from agnostic_context_stack_smoke.cli import main
except ImportError:
    from Tools.validation.agnostic_context_stack_smoke.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
