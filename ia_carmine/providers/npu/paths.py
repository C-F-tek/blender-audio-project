"""Path helpers for IA-Carmine NPU provider modules."""

from __future__ import annotations

from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    current = Path(start or __file__).resolve()
    search_from = current if current.is_dir() else current.parent
    for candidate in (search_from, *search_from.parents):
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").exists():
            return candidate
    return Path.cwd().resolve()
