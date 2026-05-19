"""Reusable FFmpeg encode profile definitions.

This module is package-agnostic and intentionally does not import ``bpy``.
It can be used by Blender scripts, normal Python tools, validation utilities,
and future AI-generated packages.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EncodeProfile:
    """A reusable collection of FFmpeg arguments for final video encoding."""

    name: str
    video_args: tuple[str, ...]
    audio_args: tuple[str, ...]
    color_args: tuple[str, ...]
    container_args: tuple[str, ...]
    description: str = ""


YOUTUBE_BT709_COLOR_ARGS = (
    "-pix_fmt",
    "yuv420p",
    "-colorspace",
    "bt709",
    "-color_primaries",
    "bt709",
    "-color_trc",
    "bt709",
)

AAC_320K_AUDIO_ARGS = (
    "-c:a",
    "aac",
    "-b:a",
    "320k",
)

FASTSTART_MP4_ARGS = (
    "-movflags",
    "+faststart",
)

CPU_SVT_AV1_YOUTUBE = EncodeProfile(
    name="cpu_svt_av1_youtube",
    description="CPU SVT-AV1 profile for high-quality YouTube-oriented output.",
    video_args=(
        "-c:v",
        "libsvtav1",
        "-preset",
        "4",
        "-crf",
        "24",
    ),
    audio_args=AAC_320K_AUDIO_ARGS,
    color_args=YOUTUBE_BT709_COLOR_ARGS,
    container_args=FASTSTART_MP4_ARGS,
)

CPU_SVT_AV1_YOUTUBE_12_THREADS = EncodeProfile(
    name="cpu_svt_av1_youtube_12_threads",
    description="CPU SVT-AV1 YouTube profile constrained to 12 encoding threads.",
    video_args=(
        "-c:v",
        "libsvtav1",
        "-preset",
        "4",
        "-crf",
        "24",
        "-threads",
        "12",
    ),
    audio_args=AAC_320K_AUDIO_ARGS,
    color_args=YOUTUBE_BT709_COLOR_ARGS,
    container_args=FASTSTART_MP4_ARGS,
)

GPU_AV1_NVENC_YOUTUBE = EncodeProfile(
    name="gpu_av1_nvenc_youtube",
    description="GPU AV1 NVENC profile for fast YouTube-oriented iterations.",
    video_args=(
        "-c:v",
        "av1_nvenc",
        "-gpu",
        "0",
        "-preset",
        "p7",
        "-tune",
        "hq",
        "-rc:v",
        "vbr",
        "-cq:v",
        "18",
        "-b:v",
        "0",
    ),
    audio_args=AAC_320K_AUDIO_ARGS,
    color_args=YOUTUBE_BT709_COLOR_ARGS,
    container_args=FASTSTART_MP4_ARGS,
)

PROFILES: dict[str, EncodeProfile] = {
    CPU_SVT_AV1_YOUTUBE.name: CPU_SVT_AV1_YOUTUBE,
    CPU_SVT_AV1_YOUTUBE_12_THREADS.name: CPU_SVT_AV1_YOUTUBE_12_THREADS,
    GPU_AV1_NVENC_YOUTUBE.name: GPU_AV1_NVENC_YOUTUBE,
}


def list_profiles() -> tuple[str, ...]:
    """Return available encode profile names."""
    return tuple(sorted(PROFILES))


def get_profile(name: str) -> EncodeProfile:
    """Return an encode profile by name with a clear error for invalid names."""
    try:
        return PROFILES[name]
    except KeyError as exc:
        available = ", ".join(list_profiles())
        raise ValueError(
            f"Unknown encode profile: {name}. Available profiles: {available}"
        ) from exc


def profile_to_args(profile: EncodeProfile) -> list[str]:
    """Flatten a profile into FFmpeg arguments."""
    return [
        *profile.video_args,
        *profile.audio_args,
        *profile.color_args,
        *profile.container_args,
    ]
