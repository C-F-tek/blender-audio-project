"""Path and file helpers for the project AI index."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .config import (
    EXCLUDE_DIRS,
    EXCLUDE_FILE_PREFIXES,
    EXCLUDE_PARTS,
    MEDIA_SUFFIXES,
    ROOT,
    TEXT_SUFFIXES,
)

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rel_to_root(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")


def slugify(value: str, max_len: int = 80) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return slug[:max_len] or "chunk"


def should_exclude(path: Path) -> bool:
    rel_parts = path.resolve().relative_to(ROOT.resolve()).parts
    if any(part in EXCLUDE_DIRS or part in EXCLUDE_PARTS for part in rel_parts[:-1]):
        return True

    suffix = path.suffix.lower()
    if suffix in MEDIA_SUFFIXES or suffix not in TEXT_SUFFIXES:
        return True

    stem = path.stem
    if any(stem.startswith(prefix) for prefix in EXCLUDE_FILE_PREFIXES):
        return True

    if path.name.endswith(".pyc") or path.name.endswith(".pyo"):
        return True
    if path.name.startswith("."):
        return True

    return False


def collect_project_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            continue
        if should_exclude(path):
            continue
        files.append(path.resolve())
    return sorted(files, key=lambda item: rel_to_root(item).lower())
