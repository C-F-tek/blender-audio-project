from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PathStats:
    name: str
    path: Path
    exists: bool
    bytes: int
    files: int
    dirs: int
    sample: tuple[Path, ...]


def human_bytes(size: int | float) -> str:
    value = float(size or 0)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024.0 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024.0
    return f"{value:.1f} TB"


def scan_tree(path: Path, *, sample_limit: int = 24) -> PathStats:
    path = Path(path).expanduser()
    if not path.exists():
        return PathStats(path.name or str(path), path, False, 0, 0, 0, tuple())

    total_bytes = 0
    files = 0
    dirs = 0
    sample: list[Path] = []

    if path.is_file():
        return PathStats(path.name, path, True, path.stat().st_size, 1, 0, (path,))

    stack = [path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    try:
                        entry_path = Path(entry.path)
                        if entry.is_dir(follow_symlinks=False):
                            dirs += 1
                            if len(sample) < sample_limit:
                                sample.append(entry_path)
                            stack.append(entry_path)
                        elif entry.is_file(follow_symlinks=False):
                            files += 1
                            stat = entry.stat(follow_symlinks=False)
                            total_bytes += stat.st_size
                            if len(sample) < sample_limit:
                                sample.append(entry_path)
                    except OSError:
                        continue
        except OSError:
            continue

    return PathStats(path.name or str(path), path, True, total_bytes, files, dirs, tuple(sample))


def immediate_children_stats(path: Path) -> list[PathStats]:
    path = Path(path).expanduser()
    if not path.exists() or not path.is_dir():
        return []
    return [
        scan_tree(child)
        for child in sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
    ]


def safe_path(value: Any) -> Path | None:
    if isinstance(value, str) and value.strip():
        return Path(value).expanduser()
    return None
