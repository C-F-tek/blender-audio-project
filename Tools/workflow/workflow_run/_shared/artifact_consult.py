from __future__ import annotations

import os
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TEXT_EXTENSIONS = {".json", ".md", ".txt", ".py", ".log", ".jsonl", ".csv"}
IMAGE_EXTENSIONS = {".png", ".gif", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".aac", ".m4a"}


@dataclass(frozen=True)
class ArtifactRecord:
    index: int
    key: str
    path: Path
    category: str
    exists: bool
    size: int


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


def collect_artifacts(session: Any, *, include_existing_only: bool = False) -> list[ArtifactRecord]:
    records: list[ArtifactRecord] = []
    seen: set[str] = set()

    def add_item(key: str, raw_path: str | Path | None) -> None:
        if not raw_path:
            return
        path = Path(raw_path).expanduser()
        marker = str(path.resolve(strict=False)).lower()
        if marker in seen:
            return
        seen.add(marker)
        exists = path.exists()
        if include_existing_only and not exists:
            return
        size = path.stat().st_size if exists and path.is_file() else 0
        records.append(
            ArtifactRecord(
                index=0,
                key=key,
                path=path,
                category=classify_path(path),
                exists=exists,
                size=size,
            )
        )

    for key, value in getattr(session, "artifacts", {}).items():
        if isinstance(value, str):
            add_item(key, value)

    render_mp4 = Path(getattr(session, "artifacts", {}).get("render_mp4", "")).expanduser()
    render_dir = render_mp4.parent if str(render_mp4) else None
    if render_dir and render_dir.exists():
        for pattern in ("*.mp4", "*.mov", "*.mkv", "*.webm"):
            for path in render_dir.glob(pattern):
                add_item(f"render:{path.name}", path)

    sorted_records = sorted(
        records, key=lambda item: (not item.exists, item.category, item.key.lower())
    )
    return [
        ArtifactRecord(
            index=index,
            key=item.key,
            path=item.path,
            category=item.category,
            exists=item.exists,
            size=item.size,
        )
        for index, item in enumerate(sorted_records, start=1)
    ]


def format_artifact_table(records: list[ArtifactRecord]) -> str:
    lines = [
        "=" * 96,
        "ARTEFATTI PRODOTTI",
        "=" * 96,
        f"Totale: {len(records)}",
        "",
        f"{'#':>3}  {'OK':<7} {'TYPE':<8} {'SIZE':>10}  {'KEY':<34} PATH",
        "-" * 96,
    ]
    for item in records:
        ok = "OK" if item.exists else "MISS"
        lines.append(
            f"{item.index:>3}  {ok:<7} {item.category:<8} {human_bytes(item.size):>10}  "
            f"{item.key[:34]:<34} {item.path}"
        )
    return "\n".join(lines)


def open_artifact(
    records: list[ArtifactRecord], index: int, *, folder: bool = False
) -> ArtifactRecord:
    for item in records:
        if item.index == index:
            target = item.path if folder or item.path.is_dir() else item.path
            if folder and not item.path.is_dir():
                target = item.path.parent
            open_external(target)
            return item
    raise ValueError(f"Indice artefatto non valido: {index}")
