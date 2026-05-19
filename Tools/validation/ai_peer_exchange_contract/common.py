"""Shared helpers for AI peer exchange contract validation."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def read_json(path: Path) -> tuple[dict[str, Any], str]:
    if not path.exists():
        return {}, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return {}, f"{type(exc).__name__}: {exc}"
    return (data, "") if isinstance(data, dict) else ({}, "json_not_object")

def safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0

def add(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)
