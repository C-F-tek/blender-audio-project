"""Package-agnostic path helpers for Blender audio-reactive workflows.

The helpers in this module intentionally avoid importing ``bpy``. They can be
used by normal Python tools, AI/NPU pipeline scripts, and Blender packages.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

PROJECT_MARKERS = (
    "pyproject.toml",
    "AGENTS.md",
    ".git",
)


def as_path(value: str | Path) -> Path:
    """Return ``value`` as an expanded ``Path`` without requiring it to exist."""
    return Path(value).expanduser()


def resolve_path(value: str | Path, base: str | Path | None = None) -> Path:
    """Resolve a path.

    Relative paths are resolved against ``base`` when provided, otherwise against
    the current working directory.
    """
    path = as_path(value)
    if path.is_absolute():
        return path.resolve()
    root = as_path(base) if base is not None else Path.cwd()
    return (root / path).resolve()


def find_project_root(
    start: str | Path | None = None, markers: Iterable[str] = PROJECT_MARKERS
) -> Path:
    """Find the repository root by walking upward from ``start``.

    The first parent containing at least one marker is returned.
    """
    current = resolve_path(start or Path.cwd())
    if current.is_file():
        current = current.parent

    marker_tuple = tuple(markers)
    for candidate in (current, *current.parents):
        if any((candidate / marker).exists() for marker in marker_tuple):
            return candidate

    raise FileNotFoundError(
        f"Project root not found from {current}. Expected one of: {', '.join(marker_tuple)}"
    )


def ensure_directory(path: str | Path) -> Path:
    """Create and return a directory path."""
    resolved = resolve_path(path)
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def ensure_parent_dir(path: str | Path) -> Path:
    """Create the parent directory for ``path`` and return the resolved path."""
    resolved = resolve_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def ensure_file(path: str | Path, label: str = "File") -> Path:
    """Return an existing file path or raise a descriptive error."""
    resolved = resolve_path(path)
    if not resolved.is_file():
        raise FileNotFoundError(f"{label} not found: {resolved}")
    return resolved


def ensure_existing_dir(path: str | Path, label: str = "Directory") -> Path:
    """Return an existing directory path or raise a descriptive error."""
    resolved = resolve_path(path)
    if not resolved.is_dir():
        raise NotADirectoryError(f"{label} not found: {resolved}")
    return resolved


def relative_to_root(path: str | Path, root: str | Path | None = None) -> str:
    """Return a stable POSIX-style relative path when possible."""
    resolved = resolve_path(path)
    base = resolve_path(root) if root is not None else find_project_root(resolved)
    try:
        return resolved.relative_to(base).as_posix()
    except ValueError:
        return resolved.as_posix()


def first_existing(paths: Iterable[str | Path]) -> Path | None:
    """Return the first path that exists, preserving the order of candidates."""
    for item in paths:
        path = resolve_path(item)
        if path.exists():
            return path
    return None
