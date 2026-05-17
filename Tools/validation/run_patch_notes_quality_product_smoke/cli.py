#!/usr/bin/env python3
"""Compatibility wrapper for patch-notes quality product smoke."""

from __future__ import annotations

try:
    from patch_notes_quality_product_smoke.cli import main
except ImportError:
    from Tools.validation.patch_notes_quality_product_smoke.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
