"""Shared artifact catalog primitives for workflow GUI and shell views."""

from __future__ import annotations

import os
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

TEXT_EXTENSIONS = {".json", ".md", ".txt", ".py", ".log", ".jsonl", ".csv"}
IMAGE_EXTENSIONS = {".png", ".gif", ".jpg", ".jpeg", ".webp", ".ppm", ".pgm"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".aac", ".m4a"}
ROOT_SCAN_PATTERNS = ("*.json", "*.md", "*.txt", "*.png", "*.mp4", "*.mov", "*.mkv", "*.wav")
RENDER_SIBLING_PATTERNS = ("*.mp4", "*.mov", "*.mkv", "*.webm")


@dataclass(frozen=True)
class ArtifactEntry:
    key: str
    path: Path
    category: str
    exists: bool
    size: int

    @property
    def suffix(self) -> str:
        return self.path.suffix.lower()


def human_bytes(size: int | float) -> str:
    value = float(size or 0)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024.0 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024.0
    return f"{value:.1f} TB"


def classify_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    if suffix in AUDIO_EXTENSIONS:
        return "audio"
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in TEXT_EXTENSIONS:
        return "text"
    if path.is_dir():
        return "folder"
    return "file"


def open_external(path: Path) -> None:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Percorso non trovato: {path}")

    system = platform.system().lower()
    if system == "windows":
        os.startfile(str(path))  # type: ignore[attr-defined]
    elif system == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


def collect_artifact_entries(
    session: Any,
    *,
    extra_roots: Iterable[Path] | None = None,
    include_existing_only: bool = False,
    include_render_siblings: bool = False,
) -> list[ArtifactEntry]:
    collector = _ArtifactCollector(include_existing_only=include_existing_only)
    artifacts = getattr(session, "artifacts", {})
    for key, value in artifacts.items():
        if isinstance(value, str):
            collector.add_item(key, value)
    for root in extra_roots or []:
        collector.add_root(Path(root).expanduser(), ROOT_SCAN_PATTERNS)
    if include_render_siblings:
        render_mp4 = Path(artifacts.get("render_mp4", "")).expanduser()
        render_dir = render_mp4.parent if str(render_mp4) else None
        if render_dir and render_dir.exists():
            collector.add_root(render_dir, RENDER_SIBLING_PATTERNS, key_prefix="render")
    return collector.sorted_items()


class _ArtifactCollector:
    def __init__(self, *, include_existing_only: bool) -> None:
        self.include_existing_only = include_existing_only
        self.items: list[ArtifactEntry] = []
        self.seen: set[str] = set()

    def add_item(self, key: str, raw_path: str | Path | None) -> None:
        if not raw_path:
            return
        path = Path(raw_path).expanduser()
        marker = str(path.resolve(strict=False)).lower()
        if marker in self.seen:
            return
        self.seen.add(marker)
        exists = path.exists()
        if self.include_existing_only and not exists:
            return
        size = path.stat().st_size if exists and path.is_file() else 0
        self.items.append(
            ArtifactEntry(
                key=key,
                path=path,
                category=classify_path(path),
                exists=exists,
                size=size,
            )
        )

    def add_root(
        self,
        root: Path,
        patterns: Iterable[str],
        *,
        key_prefix: str = "scan",
    ) -> None:
        if not root.exists():
            return
        for pattern in patterns:
            for path in root.glob(pattern):
                self.add_item(f"{key_prefix}:{path.name}", path)

    def sorted_items(self) -> list[ArtifactEntry]:
        return sorted(self.items, key=lambda item: (not item.exists, item.category, item.key.lower()))
