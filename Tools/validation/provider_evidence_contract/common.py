"""Shared helpers for provider evidence contract validation."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def read_optional_json(
    repo_root: Path, value: str, *, required: bool
) -> tuple[dict[str, Any], list[str], str]:
    if not value:
        return {}, ["required input argument missing"] if required else [], ""
    path = resolve_path(repo_root, value)
    rel = repo_rel(repo_root, path)
    if not path.exists():
        return (
            {},
            [f"required input missing: {rel}"] if required else [f"optional input missing: {rel}"],
            rel,
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - report validation must capture details.
        return {}, [f"{rel}: {type(exc).__name__}: {exc}"], rel
    if not isinstance(data, dict):
        return {}, [f"{rel}: JSON root is not an object"], rel
    return data, [], rel

def safe_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        if value in (None, ""):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default

def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []

def first_text(*values: Any) -> str:
    for value in values:
        if value not in (None, ""):
            return str(value)
    return ""

def is_fallback_artifact(report: dict[str, Any]) -> bool:
    return str(report.get("classification") or "") == "required_provider_artifact_missing"
