"""Reusable FFmpeg command builder for image-sequence based workflows.

This module is package-agnostic and intentionally does not import ``bpy``.
It builds commands and optionally executes them, but it does not know anything
about Blender scenes or artistic package behavior.
"""
from __future__ import annotations

import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

try:
    from .render_profiles import EncodeProfile, profile_to_args
except ImportError:  # Allows direct script-style execution during diagnostics.
    from render_profiles import EncodeProfile, profile_to_args  # type: ignore


@dataclass(frozen=True)
class EncodeJob:
    """A complete FFmpeg encode job from image sequence plus audio."""

    input_pattern: str
    audio_path: Path
    output_path: Path
    fps: float
    first_frame: int
    profile: EncodeProfile
    ffmpeg_path: Path | None = None
    overwrite: bool = True
    shortest: bool = False


def find_ffmpeg(explicit_path: str | Path | None = None) -> Path:
    """Resolve the FFmpeg executable from an explicit path or from PATH."""
    if explicit_path:
        path = Path(explicit_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"FFmpeg not found: {path}")
        return path

    found = shutil.which("ffmpeg")
    if not found:
        raise FileNotFoundError("FFmpeg not found in PATH")
    return Path(found).resolve()


def validate_encode_job(job: EncodeJob) -> None:
    """Validate an encode job without executing FFmpeg."""
    if job.fps <= 0:
        raise ValueError(f"FPS must be > 0, got {job.fps}")
    if job.first_frame < 0:
        raise ValueError(f"first_frame must be >= 0, got {job.first_frame}")
    if not job.input_pattern:
        raise ValueError("input_pattern is required")
    if "%" not in job.input_pattern:
        raise ValueError(f"input_pattern should contain an FFmpeg frame pattern: {job.input_pattern}")
    if not job.audio_path.expanduser().is_file():
        raise FileNotFoundError(f"Audio file not found: {job.audio_path}")
    job.output_path.expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


def build_ffmpeg_command(job: EncodeJob) -> list[str]:
    """Build an FFmpeg command for an image sequence plus audio encode job."""
    validate_encode_job(job)

    ffmpeg = job.ffmpeg_path or find_ffmpeg()
    command: list[str] = [str(ffmpeg)]

    command.append("-y" if job.overwrite else "-n")
    command.extend(
        [
            "-framerate",
            str(job.fps),
            "-start_number",
            str(job.first_frame),
            "-i",
            job.input_pattern,
            "-i",
            str(job.audio_path),
        ]
    )

    command.extend(profile_to_args(job.profile))
    if job.shortest:
        command.append("-shortest")
    command.append(str(job.output_path))

    return command


def format_command(command: Sequence[str], *, shell: str = "powershell") -> str:
    """Return a copy-pasteable command string.

    ``shell="powershell"`` quotes values with double quotes when needed.
    ``shell="posix"`` uses ``shlex.join``.
    """
    if shell == "posix":
        return shlex.join(command)

    parts: list[str] = []
    for part in command:
        if not part:
            parts.append('""')
        elif any(char.isspace() for char in part) or any(char in part for char in ('&', '(', ')')):
            parts.append('"' + part.replace('"', '`"') + '"')
        else:
            parts.append(part)
    return " ".join(parts)


def run_ffmpeg_command(
    command: Sequence[str],
    *,
    dry_run: bool = True,
    check: bool = True,
) -> subprocess.CompletedProcess[str] | None:
    """Run or preview an FFmpeg command.

    Dry-run is the default to avoid accidentally starting long encodes.
    """
    if dry_run:
        print(format_command(command))
        return None

    return subprocess.run(
        list(command),
        check=check,
        text=True,
        capture_output=False,
    )
