from __future__ import annotations

from typing import Any


def _number(value: Any, default: float | None = None) -> float | None:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _first_present(data: dict[str, Any], keys: tuple[str, ...], default: Any = None) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return default


def normalize_audio_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    """Normalize common WAV analysis fields into a stable AI-facing shape."""
    if not isinstance(analysis, dict):
        return {}

    summary = analysis.get("analysis_summary") if isinstance(analysis.get("analysis_summary"), dict) else analysis
    track = analysis.get("track_summary") if isinstance(analysis.get("track_summary"), dict) else {}

    duration = _first_present(summary, ("duration_sec", "duration_seconds", "duration"), None)
    sample_rate = _first_present(summary, ("sample_rate", "sr", "sampleRate"), None)
    bpm = _first_present(summary, ("estimated_tempo_bpm", "tempo_bpm", "bpm"), None)
    fps = _first_present(summary, ("fps", "frame_rate"), None)

    if duration is None:
        duration = _first_present(track, ("duration_sec", "duration_seconds", "duration"), None)
    if bpm is None:
        bpm = _first_present(track, ("estimated_tempo_bpm", "tempo_bpm", "bpm"), None)
    if fps is None:
        fps = _first_present(track, ("fps", "frame_rate"), None)

    return {
        "duration_sec": _number(duration),
        "sample_rate": _number(sample_rate),
        "estimated_tempo_bpm": _number(bpm),
        "fps": _number(fps),
        "source_keys": sorted(analysis.keys()),
    }


def normalize_segments(payload: dict[str, Any], *, limit: int | None = None) -> list[dict[str, Any]]:
    """Normalize segment-like objects used by AI prompts."""
    if not isinstance(payload, dict):
        return []
    raw_segments = payload.get("segments") or payload.get("music_segments") or []
    if isinstance(raw_segments, dict):
        raw_segments = raw_segments.get("segments") or []
    if not isinstance(raw_segments, list):
        return []

    normalized: list[dict[str, Any]] = []
    for index, segment in enumerate(raw_segments[:limit] if limit else raw_segments):
        if not isinstance(segment, dict):
            continue
        normalized.append({
            "index": segment.get("index", index),
            "start_sec": _number(_first_present(segment, ("start_sec", "start", "t0"), 0.0), 0.0),
            "end_sec": _number(_first_present(segment, ("end_sec", "end", "t1"), 0.0), 0.0),
            "dominant_band": _first_present(segment, ("dominant_band", "band", "dominant"), "unknown"),
            "intensity": _first_present(segment, ("intensity", "energy_label", "level"), "unknown"),
            "intensity_score": _number(_first_present(segment, ("intensity_score", "energy", "score"), None)),
            "controls": segment.get("controls") if isinstance(segment.get("controls"), dict) else {},
            "top_events": segment.get("top_events", [])[:8] if isinstance(segment.get("top_events"), list) else [],
        })
    return normalized


def build_audio_ai_summary(
    analysis: dict[str, Any],
    track_summary: dict[str, Any] | None = None,
    music_context: dict[str, Any] | None = None,
    *,
    segment_limit: int | None = 24,
) -> dict[str, Any]:
    """Build a compact AI-facing summary from WAV-derived artifacts."""
    track_summary = track_summary or {}
    music_context = music_context or {}
    merged = {**analysis}
    if track_summary:
        merged["track_summary"] = track_summary
    if music_context:
        merged.update({key: value for key, value in music_context.items() if key not in merged})

    normalized_analysis = normalize_audio_analysis(merged)
    segments = normalize_segments(merged, limit=segment_limit)
    return {
        "schema_version": 1,
        "analysis_summary": normalized_analysis,
        "segment_count": len(segments),
        "segments": segments,
        "ai_usage": {
            "purpose": "compact audio context for prompt building",
            "full_frame_data_policy": "do not replace full frame/keyframe JSON; use this only for macro reasoning",
        },
    }
