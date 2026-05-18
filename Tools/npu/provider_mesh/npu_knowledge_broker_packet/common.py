"""Common path helpers for NPU knowledge broker packets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .constants import FORBIDDEN_EXACT, FORBIDDEN_FRAGMENTS, FORBIDDEN_PREFIXES

def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (repo_root / path).resolve()


def normalize_path(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def path_allowed(path: str) -> bool:
    normalized = normalize_path(path)
    if not normalized or Path(normalized).is_absolute():
        return False
    if normalized in FORBIDDEN_EXACT:
        return False
    if any(normalized.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
        return False
    lower = normalized.lower()
    if any(fragment in lower for fragment in FORBIDDEN_FRAGMENTS) and lower.endswith(".json"):
        return False
    return True
