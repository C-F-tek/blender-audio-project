#!/usr/bin/env python3
"""Compatibility entrypoint for GPU/NPU run sync analysis."""

from __future__ import annotations

from gpu_npu_run_sync_analysis.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
