from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ContextSlice:
    """A bounded text slice used for deterministic prompt/context assembly."""

    label: str
    text: str
    max_chars: int

    def clipped(self) -> str:
        return self.text[: self.max_chars]

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "max_chars": self.max_chars,
            "original_chars": len(self.text),
            "clipped_chars": len(self.clipped()),
            "text": self.clipped(),
        }


def summarize_music_context(music_context: dict[str, Any]) -> dict[str, Any]:
    """Return the compact music summary fields used by NPU/Ollama prompt payloads."""

    return {
        "analysis_summary": music_context.get("analysis_summary") or {},
        "track_summary": music_context.get("track_summary") or {},
        "scene_summaries": music_context.get("scene_summaries") or [],
        "segment_count": len(music_context.get("segments") or []),
    }


def build_context_bundle(
    *,
    music_context: dict[str, Any],
    project_index: str,
    npu_notes: str,
    max_project_index_chars: int = 14000,
    max_npu_notes_chars: int = 18000,
) -> dict[str, Any]:
    """Build a deterministic app-agnostic context bundle without reading files."""

    project_slice = ContextSlice("primary_project_index", project_index, max_project_index_chars)
    npu_slice = ContextSlice("npu_technical_notes", npu_notes, max_npu_notes_chars)
    return {
        "music_summary": summarize_music_context(music_context),
        "slices": {
            project_slice.label: project_slice.to_dict(),
            npu_slice.label: npu_slice.to_dict(),
        },
    }


def context_bundle_metrics(bundle: dict[str, Any]) -> dict[str, int]:
    """Return simple metrics for a context bundle."""

    slices = bundle.get("slices") or {}
    original_chars = 0
    clipped_chars = 0
    for item in slices.values():
        if not isinstance(item, dict):
            continue
        original_chars += int(item.get("original_chars") or 0)
        clipped_chars += int(item.get("clipped_chars") or 0)
    return {
        "slice_count": len(slices),
        "original_chars": original_chars,
        "clipped_chars": clipped_chars,
    }
