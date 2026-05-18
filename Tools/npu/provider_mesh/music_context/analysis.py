"""Audio analysis summarization for music context."""

from __future__ import annotations

import math
from pathlib import Path

from .common import (
    SAMPLE_ROWS_PER_SEGMENT,
    TOP_EVENTS_PER_SEGMENT,
    load_json,
    rel_to_root,
    round_float,
    value_stats,
)

def frame_values(frames: list[dict], key: str) -> list[float]:
    return [round_float(frame.get(key, 0.0), 8) for frame in frames]

def energy_stats(frames: list[dict]) -> dict:
    return {
        "low": value_stats(frame_values(frames, "low")),
        "mid": value_stats(frame_values(frames, "mid")),
        "high": value_stats(frame_values(frames, "high")),
        "onset": value_stats(frame_values(frames, "onset")),
        "beat": value_stats(frame_values(frames, "beat")),
    }

def dominant_band(stats: dict) -> str:
    candidates = {
        "low": stats["low"]["avg"],
        "mid": stats["mid"]["avg"],
        "high": stats["high"]["avg"],
    }
    return max(candidates, key=candidates.get)

def intensity_label(score: float) -> str:
    if score >= 0.72:
        return "peak"
    if score >= 0.52:
        return "high"
    if score >= 0.34:
        return "medium"
    if score >= 0.18:
        return "low"
    return "quiet"

def segment_score(stats: dict) -> float:
    return round_float(
        stats["low"]["avg"] * 0.30
        + stats["mid"]["avg"] * 0.25
        + stats["high"]["avg"] * 0.20
        + stats["onset"]["p90"] * 0.20
        + stats["beat"]["avg"] * 0.05
    )

def control_suggestions(stats: dict, beat_count: int) -> dict:
    band = dominant_band(stats)
    score = segment_score(stats)
    return {
        "primary_band": band,
        "intensity": intensity_label(score),
        "hero_deformation": round_float(stats["low"]["p90"] * 0.55 + stats["onset"]["p90"] * 0.20),
        "material_shimmer": round_float(stats["mid"]["p90"] * 0.45 + stats["high"]["p90"] * 0.35),
        "fog_motion": round_float(stats["low"]["avg"] * 0.35 + stats["mid"]["avg"] * 0.25),
        "accent_emission": round_float(
            stats["high"]["p90"] * 0.65 + min(1.0, beat_count / 32.0) * 0.20
        ),
        "camera_pressure": round_float(stats["onset"]["p98"] * 0.28 + stats["beat"]["avg"] * 0.12),
    }

def split_segments(frames: list[dict], segment_seconds: float, duration: float) -> list[list[dict]]:
    segment_count = max(1, int(math.ceil(duration / segment_seconds)))
    buckets: list[list[dict]] = [[] for _ in range(segment_count)]

    for frame in frames:
        time = round_float(frame.get("time", 0.0), 8)
        index = int(time // segment_seconds)
        index = max(0, min(segment_count - 1, index))
        buckets[index].append(frame)

    return buckets

def sampled_frames(frames: list[dict], max_rows: int = SAMPLE_ROWS_PER_SEGMENT) -> list[dict]:
    if not frames:
        return []
    if len(frames) <= max_rows:
        indices = list(range(len(frames)))
    else:
        indices = sorted({round(i * (len(frames) - 1) / (max_rows - 1)) for i in range(max_rows)})

    return [
        {
            "time": round_float(frames[index].get("time", 0.0), 3),
            "low": round_float(frames[index].get("low", 0.0), 3),
            "mid": round_float(frames[index].get("mid", 0.0), 3),
            "high": round_float(frames[index].get("high", 0.0), 3),
            "onset": round_float(frames[index].get("onset", 0.0), 3),
            "beat": round_float(frames[index].get("beat", 0.0), 3),
        }
        for index in indices
    ]

def top_events(frames: list[dict], limit: int = TOP_EVENTS_PER_SEGMENT) -> list[dict]:
    ranked = sorted(
        frames,
        key=lambda frame: (
            round_float(frame.get("onset", 0.0)) * 1.00
            + round_float(frame.get("beat", 0.0)) * 0.35
            + round_float(frame.get("high", 0.0)) * 0.15
        ),
        reverse=True,
    )
    events = []
    for frame in ranked[:limit]:
        events.append(
            {
                "time": round_float(frame.get("time", 0.0), 3),
                "low": round_float(frame.get("low", 0.0), 3),
                "mid": round_float(frame.get("mid", 0.0), 3),
                "high": round_float(frame.get("high", 0.0), 3),
                "onset": round_float(frame.get("onset", 0.0), 3),
                "beat": round_float(frame.get("beat", 0.0), 3),
            }
        )
    return events

def beats_in_range(beats: list[float], start: float, end: float) -> list[float]:
    return [round_float(beat, 3) for beat in beats if start <= beat < end]

def build_segments(analysis: dict, segment_seconds: float) -> list[dict]:
    meta = analysis.get("meta", {})
    frames = analysis.get("frames", [])
    beats = [round_float(beat, 8) for beat in analysis.get("beats", [])]
    duration = round_float(
        meta.get("duration_sec") or (frames[-1].get("time", 0.0) if frames else 0.0), 8
    )

    segments = []
    for index, segment_frames in enumerate(split_segments(frames, segment_seconds, duration), 1):
        start = (index - 1) * segment_seconds
        end = min(index * segment_seconds, duration)
        stats = energy_stats(segment_frames)
        beat_times = beats_in_range(beats, start, end)
        score = segment_score(stats)
        segments.append(
            {
                "index": index,
                "start_sec": round_float(start, 3),
                "end_sec": round_float(end, 3),
                "duration_sec": round_float(max(0.0, end - start), 3),
                "frame_count": len(segment_frames),
                "beat_count": len(beat_times),
                "dominant_band": dominant_band(stats),
                "intensity_score": score,
                "intensity": intensity_label(score),
                "stats": stats,
                "controls": control_suggestions(stats, len(beat_times)),
                "beat_times": beat_times,
                "top_events": top_events(segment_frames),
                "sampled_frames": sampled_frames(segment_frames),
            }
        )
    return segments

def summarize_analysis(analysis_path: Path, segment_seconds: float) -> tuple[dict, list[dict]]:
    analysis = load_json(analysis_path)
    meta = analysis.get("meta", {})
    frames = analysis.get("frames", [])
    beats = analysis.get("beats", [])
    stats = energy_stats(frames)
    segments = build_segments(analysis, segment_seconds)

    top_by_energy = sorted(segments, key=lambda item: item["intensity_score"], reverse=True)[:8]
    top_by_onset = sorted(segments, key=lambda item: item["stats"]["onset"]["p98"], reverse=True)[
        :8
    ]

    summary = {
        "source": rel_to_root(analysis_path),
        "track_name": analysis_path.stem.replace("_analysis", ""),
        "meta": meta,
        "frame_count": len(frames),
        "beat_count": len(beats),
        "segment_seconds": segment_seconds,
        "segment_count": len(segments),
        "overall_stats": stats,
        "top_energy_segments": [
            {
                "index": item["index"],
                "start_sec": item["start_sec"],
                "end_sec": item["end_sec"],
                "dominant_band": item["dominant_band"],
                "intensity_score": item["intensity_score"],
                "intensity": item["intensity"],
            }
            for item in top_by_energy
        ],
        "top_onset_segments": [
            {
                "index": item["index"],
                "start_sec": item["start_sec"],
                "end_sec": item["end_sec"],
                "onset_p98": item["stats"]["onset"]["p98"],
                "beat_count": item["beat_count"],
            }
            for item in top_by_onset
        ],
    }

    return summary, segments
