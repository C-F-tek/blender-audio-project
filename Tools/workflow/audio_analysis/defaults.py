"""Shared defaults for audio analysis workflow tools."""

from __future__ import annotations

from pathlib import Path

DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
DEFAULT_WAV_NAME = f"{DEFAULT_TRACK_STEM}.wav"
DEFAULT_OLLAMA_MODEL = "qwen2.5-coder:14b"


def default_output_dir(repo_root: Path) -> Path:
    return repo_root / "output"


def default_analysis_json(repo_root: Path) -> Path:
    return default_output_dir(repo_root) / f"{DEFAULT_TRACK_STEM}_analysis.json"


def default_summary_json(repo_root: Path) -> Path:
    return default_output_dir(repo_root) / f"{DEFAULT_TRACK_STEM}_track_summary.json"
