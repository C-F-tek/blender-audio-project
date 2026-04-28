#!/usr/bin/env python3
"""
Build compact AI-friendly music artifacts from an existing analysis JSON.

The source analysis JSON is read-only. New artifacts are written to the output
directory.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def first_number(data: Any, keys: tuple[str, ...]) -> float | None:
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, (int, float)):
                return float(value)
        for value in data.values():
            found = first_number(value, keys)
            if found is not None:
                return found
    if isinstance(data, list):
        for value in data[:40]:
            found = first_number(value, keys)
            if found is not None:
                return found
    return None


def find_series(data: Any) -> dict[str, list[float]]:
    wanted = ("energy", "intensity", "onset", "rms", "low", "mid", "high", "amplitude")
    out: dict[str, list[float]] = {}

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, f"{path}.{key}" if path else key)
        elif isinstance(value, list):
            if value and all(isinstance(x, (int, float)) for x in value[: min(200, len(value))]):
                if any(token in path.lower() for token in wanted):
                    out[path] = [float(x) for x in value if isinstance(x, (int, float))]
            elif value and isinstance(value[0], dict):
                for key in ("energy", "intensity", "value", "amplitude", "onset_strength"):
                    vals = [float(x[key]) for x in value if isinstance(x, dict) and isinstance(x.get(key), (int, float))]
                    if vals:
                        out[f"{path}.{key}"] = vals
                        break

    walk(data, "")
    return out


def normalize(values: list[float]) -> list[float]:
    if not values:
        return []
    lo, hi = min(values), max(values)
    if math.isclose(lo, hi):
        return [0.0 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]


def top_events(values: list[float], duration: float, limit: int = 16) -> list[dict[str, Any]]:
    if not values or duration <= 0:
        return []
    norm = normalize(values)
    indexed = sorted(enumerate(norm), key=lambda item: item[1], reverse=True)[:limit]
    denom = max(len(values) - 1, 1)
    return sorted(
        [{"time_sec": round(index / denom * duration, 3), "score": round(score, 4), "index": index} for index, score in indexed],
        key=lambda item: item["time_sec"],
    )


def synthetic_beats(duration: float, bpm: float | None) -> list[float]:
    if not bpm or duration <= 0:
        return []
    step = 60.0 / bpm
    beats, t = [], 0.0
    while t <= duration and len(beats) < 2000:
        beats.append(round(t, 3))
        t += step
    return beats


def segments(duration: float, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if duration <= 0:
        return []
    names = ["intro", "build", "development", "climax", "release", "outro"] if duration >= 180 else ["intro", "build", "climax", "release", "outro"]
    step = duration / len(names)
    result = []
    for i, name in enumerate(names):
        start = i * step
        end = duration if i == len(names) - 1 else (i + 1) * step
        local = [e for e in events if start <= e["time_sec"] < end]
        result.append({
            "name": name,
            "start_sec": round(start, 3),
            "end_sec": round(end, 3),
            "duration_sec": round(end - start, 3),
            "estimated_intensity": round(statistics.mean([e["score"] for e in local]), 4) if local else None,
            "event_count": len(local),
            "ai_use": "Vary camera, lighting, materials, fog, density, or motion intensity in this section."
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis-json", required=True)
    parser.add_argument("--output-dir", default="output/ai_pipeline")
    args = parser.parse_args()

    source = Path(args.analysis_json).resolve()
    out = Path(args.output_dir).resolve()
    data = load_json(source)
    duration = first_number(data, ("duration_sec", "duration_seconds", "duration", "track_duration_sec")) or 0.0
    bpm = first_number(data, ("bpm", "estimated_bpm", "tempo"))
    sample_rate = first_number(data, ("sample_rate", "sr", "samplerate"))
    series = find_series(data)
    primary_name = next(iter(series), None)
    primary = series.get(primary_name, []) if primary_name else []
    peaks = top_events(primary, duration)
    segs = segments(duration, peaks)
    beats = synthetic_beats(duration, bpm)
    now = datetime.now(timezone.utc).isoformat()

    artifacts = {
        "track_summary.json": {
            "schema_version": 1,
            "generated_at": now,
            "source_analysis": str(source),
            "duration_sec": round(duration, 3) if duration else None,
            "estimated_bpm": round(bpm, 3) if bpm else None,
            "sample_rate": int(sample_rate) if sample_rate else None,
            "series_detected": sorted(series.keys()),
            "primary_series": primary_name,
            "segment_count": len(segs),
            "beat_count": len(beats),
            "peak_event_count": len(peaks),
        },
        "music_segments.json": {"schema_version": 1, "generated_at": now, "source_analysis": str(source), "segments": segs},
        "audio_event_map.json": {
            "schema_version": 1,
            "generated_at": now,
            "source_analysis": str(source),
            "beats_sec": beats[:512],
            "peak_events": peaks,
            "series_used_for_peaks": primary_name,
        },
        "ai_scene_brief.json": {
            "schema_version": 1,
            "generated_at": now,
            "creative_intent": "audio-reactive cinematic Blender scene",
            "technical_intent": "Generate or patch a Blender package using compact audio summaries and validated scene mapping.",
            "track_facts": {"duration_sec": round(duration, 3) if duration else None, "estimated_bpm": round(bpm, 3) if bpm else None, "segment_count": len(segs)},
            "recommended_visual_progression": [{"segment": s["name"], "start_sec": s["start_sec"], "end_sec": s["end_sec"]} for s in segs],
            "constraints": ["Do not overwrite full analysis JSON files.", "Keep generated scripts configurable.", "Validate before accepting generated code."],
        },
        "ai_resource_budget.json": {
            "schema_version": 1,
            "generated_at": now,
            "target_profile": "local_workstation_32gb_ram_16gb_vram",
            "recommendations": {"max_parallel_npu_jobs": 4, "gpu_role": "main generation and merge", "npu_role": "short review and scoring", "cpu_role": "validation and orchestration"},
        },
    }

    written = {}
    for name, payload in artifacts.items():
        path = out / name
        write_json(path, payload)
        written[name] = str(path)
    print(json.dumps(written, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
