#!/usr/bin/env python3
"""Unified entrypoint for validators, smokes, and local gates."""

from __future__ import annotations

try:
    from validation_gate.cli import main
except ImportError:
    from Tools.validation.validation_gate.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
