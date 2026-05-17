#!/usr/bin/env python3
"""Compatibility entrypoint for reviewed patch-spec promotion."""

from __future__ import annotations

from generated_patch_specs.review_cli import main


if __name__ == "__main__":
    raise SystemExit(main())
