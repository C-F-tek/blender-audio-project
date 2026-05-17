#!/usr/bin/env python3
"""Compatibility entrypoint for heap runtime launcher command generation."""

from __future__ import annotations

from heap_runtime_launcher_command.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
