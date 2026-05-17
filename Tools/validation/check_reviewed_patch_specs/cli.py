#!/usr/bin/env python3
"""Compatibility wrapper for reviewed patch-spec contract validation."""

from __future__ import annotations

try:
    from reviewed_patch_specs_check.cli import main
except ImportError:
    from Tools.validation.reviewed_patch_specs_check.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
