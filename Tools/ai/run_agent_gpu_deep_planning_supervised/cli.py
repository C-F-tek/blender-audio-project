#!/usr/bin/env python3
"""Compatibility entrypoint for the GPU deep planning supervised runner."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[3]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from tools.ai.gpu_deep_planning_supervised.cli import main
from tools.ai.gpu_deep_planning_supervised.runner import run_supervised

__all__ = ["main", "run_supervised"]

if __name__ == "__main__":
    raise SystemExit(main())
