#!/usr/bin/env python3
"""Compatibility entrypoint for the GPU deep planning review runner."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[3]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from tools.ai.gpu_deep_planning_review.cli import main
from tools.ai.gpu_deep_planning_review.common import *  # noqa: F403
from tools.ai.gpu_deep_planning_review.parsing import *  # noqa: F403
from tools.ai.gpu_deep_planning_review.prompt import build_prompt
from tools.ai.gpu_deep_planning_review.reporting import build_markdown, merge_recommendations
from tools.ai.gpu_deep_planning_review.runner import run_deep_review

if __name__ == "__main__":
    raise SystemExit(main())
