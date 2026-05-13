from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return (repo_root / path).resolve() if not path.is_absolute() else path.resolve()


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return (
            path.resolve(strict=False)
            .relative_to(repo_root.resolve(strict=False))
            .as_posix()
        )
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> tuple[dict[str, Any], str]:
    if not path or str(path) == ".":
        return {}, "not_provided"
    if not path.exists():
        return {}, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return {}, f"invalid_json: {exc}"
    if not isinstance(data, dict):
        return {}, "json_root_not_object"
    return data, ""


def read_text(path: Path, max_chars: int = 250_000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")[:max_chars]
    except Exception:
        return ""


def flatten_json(value: Any, limit: int = 250_000) -> str:
    try:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    except Exception:
        text = str(value)
    return text[:limit]


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
