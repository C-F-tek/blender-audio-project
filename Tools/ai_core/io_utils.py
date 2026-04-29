from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def ensure_dir(path: str | Path) -> Path:
    """Create and return a directory path."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def read_text(path: str | Path, *, encoding: str = "utf-8", errors: str = "replace", default: str | None = None) -> str:
    candidate = Path(path)
    if not candidate.exists():
        if default is not None:
            return default
        raise FileNotFoundError(candidate)
    return candidate.read_text(encoding=encoding, errors=errors)


def write_text(path: str | Path, content: str, *, encoding: str = "utf-8") -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding=encoding)
    return target


def read_json(path: str | Path, *, default: Any = None) -> Any:
    candidate = Path(path)
    if not candidate.exists():
        if default is not None:
            return default
        raise FileNotFoundError(candidate)
    with candidate.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, data: Any, *, indent: int = 2, ensure_ascii: bool = False) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=indent, ensure_ascii=ensure_ascii), encoding="utf-8")
    return target


def file_meta(path: str | Path, *, root: str | Path | None = None) -> dict[str, Any]:
    candidate = Path(path)
    rel = str(candidate)
    if root is not None:
        try:
            rel = str(candidate.resolve().relative_to(Path(root).resolve())).replace("\\", "/")
        except Exception:
            rel = str(candidate).replace("\\", "/")
    meta: dict[str, Any] = {"path": rel, "exists": candidate.exists()}
    if candidate.exists() and candidate.is_file():
        stat = candidate.stat()
        meta.update({"size_bytes": stat.st_size, "mtime": stat.st_mtime})
    return meta
