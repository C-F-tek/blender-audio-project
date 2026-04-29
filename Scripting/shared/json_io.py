"""UTF-8 JSON helpers for scripts, packages, and AI pipeline artifacts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

try:
    from .path_utils import ensure_parent_dir, resolve_path
except ImportError:  # Allows direct script-style execution during diagnostics.
    from path_utils import ensure_parent_dir, resolve_path  # type: ignore


class JsonFileError(RuntimeError):
    """Raised when a JSON file cannot be read, parsed, or validated."""


def read_text(path: str | Path) -> str:
    """Read a UTF-8 text file."""
    resolved = resolve_path(path)
    try:
        return resolved.read_text(encoding="utf-8")
    except OSError as exc:
        raise JsonFileError(f"Unable to read text file {resolved}: {exc}") from exc


def read_json(path: str | Path) -> Any:
    """Read and parse a JSON file with a clear diagnostic on failure."""
    resolved = resolve_path(path)
    try:
        return json.loads(resolved.read_text(encoding="utf-8"))
    except OSError as exc:
        raise JsonFileError(f"Unable to read JSON file {resolved}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise JsonFileError(
            f"Invalid JSON in {resolved}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def read_json_if_exists(path: str | Path, default: Any = None) -> Any:
    """Read JSON if the file exists, otherwise return ``default``."""
    resolved = resolve_path(path)
    if not resolved.exists():
        return default
    return read_json(resolved)


def write_json(path: str | Path, data: Any, *, indent: int = 2, sort_keys: bool = False) -> Path:
    """Write JSON using UTF-8 and a final newline."""
    resolved = ensure_parent_dir(path)
    try:
        resolved.write_text(
            json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=sort_keys) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise JsonFileError(f"Unable to write JSON file {resolved}: {exc}") from exc
    return resolved


def require_mapping(data: Any, label: str = "JSON value") -> dict[str, Any]:
    """Require a JSON value to be an object/dict."""
    if not isinstance(data, dict):
        raise JsonFileError(f"{label} must be a JSON object, got {type(data).__name__}")
    return data


def require_keys(data: dict[str, Any], keys: Iterable[str], label: str = "JSON object") -> None:
    """Require a mapping to contain the provided top-level keys."""
    missing = [key for key in keys if key not in data]
    if missing:
        raise JsonFileError(f"{label} is missing required keys: {', '.join(missing)}")


def summarize_json_file(path: str | Path) -> dict[str, Any]:
    """Return a lightweight summary of a JSON file."""
    resolved = resolve_path(path)
    data = read_json(resolved)
    summary: dict[str, Any] = {
        "path": resolved.as_posix(),
        "type": type(data).__name__,
    }
    if isinstance(data, dict):
        summary["keys"] = sorted(str(key) for key in data.keys())
        summary["key_count"] = len(data)
    elif isinstance(data, list):
        summary["item_count"] = len(data)
    return summary
