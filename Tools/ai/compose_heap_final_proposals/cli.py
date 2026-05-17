#!/usr/bin/env python3
"""Compatibility entrypoint for the heap final proposal composer."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORT))

from Tools.ai.heap_final_proposals.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
