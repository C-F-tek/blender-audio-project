"""Defaults for the NPU review runner."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

DEFAULT_MODEL_DIR = Path.home() / "blender" / "npu-models" / "Phi-3.5-mini-instruct-int4-cw-ov"
DEFAULT_CONTEXT = ROOT / "Tools" / "npu" / "context_artifacts" / "npu_code_context.md"
DEFAULT_CHUNK_DIR = ROOT / "Tools" / "npu" / "npu_code_chunks"
DEFAULT_OUT = ROOT / "Tools" / "npu" / "npu_context_for_aider.md"
DEFAULT_NOTES_OUT = ROOT / "Tools" / "npu" / "npu_chunk_notes.md"
DEFAULT_MUSIC_CONTEXT = ROOT / "Tools" / "npu" / "context_artifacts" / "npu_music_context.md"
DEFAULT_MUSIC_CHUNK_DIR = ROOT / "Tools" / "npu" / "npu_music_chunks"
DEFAULT_MUSIC_OUT = ROOT / "Tools" / "npu" / "npu_music_context_for_aider.md"
DEFAULT_MUSIC_NOTES_OUT = ROOT / "Tools" / "npu" / "npu_music_chunk_notes.md"
