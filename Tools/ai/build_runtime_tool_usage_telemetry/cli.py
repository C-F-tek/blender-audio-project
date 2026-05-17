#!/usr/bin/env python3
"""Compatibility entrypoint for runtime tool usage telemetry."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[3]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from tools.ai.runtime_tool_usage_telemetry import *  # noqa: F403
from tools.ai.runtime_tool_usage_telemetry.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
