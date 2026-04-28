"""FFmpeg wrapper template.

For production packages, prefer shared utilities from Scripting/shared/ when available.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def find_ffmpeg(configured_path: str = "") -> str:
    """Return an ffmpeg executable path or raise FileNotFoundError."""

    if configured_path:
        candidate = Path(configured_path)
        if candidate.exists():
            return str(candidate)

    found = shutil.which("ffmpeg")
    if found:
        return found

    raise FileNotFoundError("FFmpeg not found. Configure FFMPEG_EXE_PATH or update PATH.")


def build_basic_command(cfg, fps: int | float | None = None) -> list[str]:
    """Build a conservative FFmpeg command for an image sequence plus audio."""

    fps = fps or cfg.FPS
    ffmpeg = find_ffmpeg(cfg.FFMPEG_EXE_PATH)
    image_pattern = cfg.OUTPUT_IMAGE_SEQUENCE_DIR / f"{cfg.OUTPUT_IMAGE_SEQUENCE_PREFIX}%04d.png"

    return [
        ffmpeg,
        "-y",
        "-framerate",
        str(fps),
        "-start_number",
        "1",
        "-i",
        str(image_pattern),
        "-i",
        str(cfg.AUDIO_PATH),
        "-c:v",
        "libsvtav1",
        "-preset",
        "4",
        "-crf",
        "24",
        "-pix_fmt",
        "yuv420p",
        "-colorspace",
        "bt709",
        "-color_primaries",
        "bt709",
        "-color_trc",
        "bt709",
        "-c:a",
        "aac",
        "-b:a",
        str(cfg.FFMPEG_AUDIO_BITRATE),
        "-shortest",
        "-movflags",
        "+faststart",
        str(cfg.OUTPUT_VIDEO_PATH),
    ]


def run_encode(cfg, fps: int | float | None = None) -> None:
    """Run the package encoding command."""

    command = build_basic_command(cfg, fps=fps)
    subprocess.run(command, check=True)
