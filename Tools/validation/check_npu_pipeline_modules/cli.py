#!/usr/bin/env python3
"""Compatibility wrapper for NPU pipeline module smoke checker."""

from __future__ import annotations

try:
    from npu_pipeline_modules_check.checker import check_npu_pipeline_modules
    from npu_pipeline_modules_check.cli import main
except ImportError:
    from Tools.validation.npu_pipeline_modules_check.checker import check_npu_pipeline_modules
    from Tools.validation.npu_pipeline_modules_check.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
