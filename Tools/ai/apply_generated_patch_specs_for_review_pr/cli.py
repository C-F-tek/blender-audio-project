#!/usr/bin/env python3
"""Compatibility entrypoint for generated patch-spec apply."""

from __future__ import annotations

from generated_patch_specs.apply_cli import main


if __name__ == "__main__":
    raise SystemExit(main())
