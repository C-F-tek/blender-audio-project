from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_text(path: str | Path) -> str:
    """Read UTF-8 text if the file exists, otherwise return an empty string."""

    candidate = Path(path)
    return candidate.read_text(encoding="utf-8", errors="replace") if candidate.exists() else ""


def read_json_object(path: str | Path) -> dict[str, Any]:
    """Read a JSON file and return it only when the root value is an object."""

    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def write_json_object(path: str | Path, data: dict[str, Any]) -> None:
    """Write a JSON object with stable formatting and parent directory creation."""

    candidate = Path(path)
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def read_optional_json_object(path: str | Path | None) -> dict[str, Any]:
    """Read an optional JSON object, returning an empty object on absence or parse failure."""

    if not path:
        return {}
    candidate = Path(path)
    if not candidate.exists():
        return {}
    try:
        data = json.loads(candidate.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}
