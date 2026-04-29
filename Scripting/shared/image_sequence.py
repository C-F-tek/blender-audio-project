"""Image-sequence discovery helpers for Blender/FFmpeg workflows."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from .path_utils import ensure_existing_dir, resolve_path
except ImportError:  # Allows direct script-style execution during diagnostics.
    from path_utils import ensure_existing_dir, resolve_path  # type: ignore


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".exr")


@dataclass(frozen=True)
class FrameFile:
    """A single numbered frame file."""

    path: Path
    frame_number: int | None


@dataclass(frozen=True)
class ImageSequenceInfo:
    """Detected image-sequence metadata suitable for FFmpeg command building."""

    directory: Path
    prefix: str
    extension: str
    files: tuple[FrameFile, ...]
    contiguous_files: tuple[FrameFile, ...]
    first_frame: int | None
    frame_count: int
    pattern: str | None
    has_gaps: bool


def extract_frame_number(path: str | Path, prefix: str = "") -> int | None:
    """Extract the trailing frame number from a frame path."""
    item = Path(path)
    stem = item.stem
    if prefix and stem.startswith(prefix):
        stem = stem[len(prefix):]
    match = re.search(r"(\d+)$", stem)
    return int(match.group(1)) if match else None


def sort_frame_paths(paths: Iterable[Path], prefix: str = "") -> list[FrameFile]:
    """Sort frame paths by detected frame number, then filename."""
    frames = [FrameFile(path=path, frame_number=extract_frame_number(path, prefix)) for path in paths]
    return sorted(
        frames,
        key=lambda item: (
            item.frame_number is None,
            item.frame_number if item.frame_number is not None else 0,
            item.path.name,
        ),
    )


def contiguous_initial_block(frames: Iterable[FrameFile]) -> tuple[FrameFile, ...]:
    """Return the first contiguous numbered block from a sorted sequence."""
    ordered = list(frames)
    if not ordered:
        return ()
    first = ordered[0].frame_number
    if first is None:
        return tuple(ordered)

    kept: list[FrameFile] = [ordered[0]]
    expected = first + 1
    for item in ordered[1:]:
        if item.frame_number != expected:
            break
        kept.append(item)
        expected += 1
    return tuple(kept)


def build_ffmpeg_pattern(first_file: str | Path) -> str:
    """Build an FFmpeg ``%0Nd`` pattern from the first numbered frame."""
    path = Path(first_file)
    match = re.search(r"(\d+)$", path.stem)
    if match is None:
        raise ValueError(f"Frame number not found in filename: {path.name}")

    digits = match.group(1)
    stem_prefix = path.stem[: -len(digits)]
    return str(path.with_name(f"{stem_prefix}%0{len(digits)}d{path.suffix}"))


def scan_image_sequence(
    directory: str | Path,
    *,
    prefix: str = "",
    extension: str | None = None,
    skip_empty: bool = True,
) -> ImageSequenceInfo:
    """Scan a directory and return image-sequence metadata.

    ``extension`` may be provided with or without the leading dot. When omitted,
    common image extensions are considered.
    """
    root = ensure_existing_dir(directory, "Image sequence directory")
    if extension:
        ext = extension if extension.startswith(".") else f".{extension}"
        extensions = (ext.lower(),)
    else:
        extensions = IMAGE_EXTENSIONS

    paths: list[Path] = []
    for path in root.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensions:
            continue
        if prefix and not path.stem.startswith(prefix):
            continue
        if skip_empty and path.stat().st_size <= 0:
            continue
        paths.append(path)

    files = tuple(sort_frame_paths(paths, prefix))
    contiguous = contiguous_initial_block(files)
    first_frame = contiguous[0].frame_number if contiguous else None
    frame_count = len(contiguous)
    has_gaps = len(contiguous) != len(files)
    pattern = build_ffmpeg_pattern(contiguous[0].path) if contiguous and first_frame is not None else None
    detected_ext = contiguous[0].path.suffix.lower() if contiguous else (extension if extension else "")

    return ImageSequenceInfo(
        directory=resolve_path(root),
        prefix=prefix,
        extension=detected_ext,
        files=files,
        contiguous_files=contiguous,
        first_frame=first_frame,
        frame_count=frame_count,
        pattern=pattern,
        has_gaps=has_gaps,
    )


def sequence_report(info: ImageSequenceInfo) -> dict[str, object]:
    """Return a JSON-serializable report for a detected sequence."""
    return {
        "directory": info.directory.as_posix(),
        "prefix": info.prefix,
        "extension": info.extension,
        "file_count": len(info.files),
        "contiguous_count": len(info.contiguous_files),
        "first_frame": info.first_frame,
        "frame_count": info.frame_count,
        "pattern": info.pattern,
        "has_gaps": info.has_gaps,
        "first_file": info.contiguous_files[0].path.name if info.contiguous_files else None,
        "last_file": info.contiguous_files[-1].path.name if info.contiguous_files else None,
    }
