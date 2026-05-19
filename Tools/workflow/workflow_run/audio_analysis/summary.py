"""Track-summary builder for WAV analysis artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any

from .context_bridge import MusicContextBridge


@dataclass(frozen=True)
class TrackSummaryOptions:
    analysis_json: Path
    out_json: Path
    repo_root: Path
    update_music_context: bool = True


class TrackSummaryBuilder:
    """Create compact energy summaries from analysis JSON files."""

    def __init__(self, context_bridge: MusicContextBridge | None = None) -> None:
        self.context_bridge = context_bridge

    def build(self, options: TrackSummaryOptions) -> dict[str, Any]:
        analysis_json = options.analysis_json.expanduser().resolve()
        out_json = options.out_json.expanduser().resolve()
        repo_root = options.repo_root.expanduser().resolve()
        bridge = self.context_bridge or MusicContextBridge(repo_root)

        data = json.loads(analysis_json.read_text(encoding="utf-8"))
        meta = data["meta"]
        frames = data["frames"]
        track_name = analysis_json.stem.replace("_analysis", "")

        summary = {
            "track_name": track_name,
            "source_analysis_json": str(analysis_json),
            "duration_sec": meta.get("duration_sec"),
            "fps": meta.get("fps"),
            "estimated_tempo_bpm": meta.get("estimated_tempo_bpm"),
            "ai_memory_context": bridge.build_ai_memory_context(track_name, out_json.parent),
            "energy_profile": self.energy_profile(frames),
        }

        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"[OK] Summary saved in: {out_json}")
        print(json.dumps(summary, indent=2, ensure_ascii=False))

        if options.update_music_context:
            bridge.build_music_context(
                analysis_path=analysis_json,
                track_summary_path=out_json,
                compact_json_path=out_json.parent / f"{track_name}_music_context.json",
            )

        return summary

    @classmethod
    def energy_profile(cls, frames: list[dict[str, Any]]) -> dict[str, float]:
        low_vals = cls._frame_values(frames, "low")
        mid_vals = cls._frame_values(frames, "mid")
        high_vals = cls._frame_values(frames, "high")
        onset_vals = cls._frame_values(frames, "onset")
        beat_vals = cls._frame_values(frames, "beat")
        return {
            "low_avg": round(cls._safe_mean(low_vals), 4),
            "mid_avg": round(cls._safe_mean(mid_vals), 4),
            "high_avg": round(cls._safe_mean(high_vals), 4),
            "low_peak_avg": round(cls._avg_top(low_vals), 4),
            "mid_peak_avg": round(cls._avg_top(mid_vals), 4),
            "high_peak_avg": round(cls._avg_top(high_vals), 4),
            "onset_avg": round(cls._safe_mean(onset_vals), 4),
            "beat_avg": round(cls._safe_mean(beat_vals), 4),
        }

    @staticmethod
    def _frame_values(frames: list[dict[str, Any]], key: str) -> list[float]:
        return [float(frame.get(key, 0.0)) for frame in frames]

    @staticmethod
    def _avg_top(values: list[float], ratio: float = 0.1) -> float:
        if not values:
            return 0.0
        count = max(1, int(len(values) * ratio))
        return mean(sorted(values, reverse=True)[:count])

    @staticmethod
    def _safe_mean(values: list[float]) -> float:
        return mean(values) if values else 0.0
