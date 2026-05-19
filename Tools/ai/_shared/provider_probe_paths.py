#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def ensure_repo_imports(repo_root: Path) -> None:
    for path in (repo_root, repo_root / "Tools" / "npu"):
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)
