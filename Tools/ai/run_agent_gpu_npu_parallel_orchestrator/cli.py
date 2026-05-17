#!/usr/bin/env python3
"""Compatibility entrypoint for the GPU/NPU parallel orchestrator."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[3]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from tools.ai.gpu_npu_parallel_orchestrator.cli import main
from tools.ai.gpu_npu_parallel_orchestrator.runner import run_orchestrator
from tools.ai.gpu_npu_parallel_orchestrator.common import runtime_state_gate

__all__ = ["main", "run_orchestrator", "runtime_state_gate"]

if __name__ == "__main__":
    raise SystemExit(main())
