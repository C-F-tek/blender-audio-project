"""Utility functions for Universo heap refactoring.

This module centralises shared helpers that were previously duplicated across
heap‑related scripts. It provides a thin, well‑named API while preserving the
original behaviour.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def now_iso() -> str:
    """Return the current timestamp in ISO‑8601 format (seconds precision)."""
    return datetime.now().isoformat(timespec="seconds")


def read_request_file(repo_root: Path, value: str) -> str:
    """Read a file relative to ``repo_root`` if ``value`` is not absolute.

    Args:
        repo_root: Path to the repository root.
        value: Path string to read; may be absolute or relative.
    """
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.read_text(encoding="utf-8-sig", errors="replace")


def repo_rel(repo_root: Path, path: Path) -> str:
    """Return ``path`` relative to ``repo_root`` if possible, otherwise ``str``."""
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    """Safely read a JSON file, returning an empty dict on error."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:  # noqa: BLE001
        return {}
    return data if isinstance(data, dict) else {}


def make_state(objective: str, request: str = "") -> dict[str, Any]:
    """Create the initial state dictionary used by the heap runtime gate."""
    return {
        "task": {"objective": objective, "status": "active"},
        "request": {
            "text": request.strip(),
            "status": "received" if request.strip() else "not_requested",
        },
        "budget_governor": {},
        "invocation_contract": {},
        "facts": [],
        # initialize collections expected by the gate runtime
        "needs": [],
        "tool_requests": [],
        "shared_evidence": [],
        "claims": [],
        "decisions": [],
        "candidate_operations": [],
        "provider_results": [],
        "product": {},
    }
