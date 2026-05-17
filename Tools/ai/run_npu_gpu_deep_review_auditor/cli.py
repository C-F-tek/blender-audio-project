#!/usr/bin/env python3
"""Compatibility entrypoint for the NPU/GPU deep review auditor."""

from __future__ import annotations

import sys
from pathlib import Path

repo_root_for_import = Path(__file__).resolve().parents[3]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from tools.ai.npu_gpu_deep_review_auditor import main


if __name__ == "__main__":
    raise SystemExit(main())
