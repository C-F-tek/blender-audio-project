"""Shared constants and helpers for music context generation."""

from __future__ import annotations

import hashlib
import json
import math
import statistics
from pathlib import Path

from Tools.npu.provider_mesh._shared.ai_memory_context import build_ai_memory_context

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "output"
OUT_DIR = ROOT / "Tools" / "npu" / "context_artifacts"
CHUNK_DIR = OUT_DIR / "npu_music_chunks"

DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
DEFAULT_ANALYSIS = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_analysis.json"
DEFAULT_TRACK_SUMMARY = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_track_summary.json"
DEFAULT_COMPACT_JSON = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_music_context.json"
DEFAULT_ANALYSIS_AI_CONTEXT = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_analysis_ai_context.json"
DEFAULT_BLENDER_KEYFRAMES_JSON = (
    OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_analysis_blender_keyframes.json"
)
OUT_MD = OUT_DIR / "npu_music_context.md"
OUT_JSON = OUT_DIR / "npu_music_manifest.json"

DEFAULT_SCENE_FILES = [
    ROOT / "scene_spec_album_driven.json",
    ROOT / "scene_spec_album_driven_normalized.json",
    ROOT / "scene_spec_album_driven_raw.txt",
    ROOT / "scene_spec_from_npu.json",
    ROOT / "scene_spec_from_npu_raw.txt",
]

DEFAULT_SEGMENT_SECONDS = 16.0
SAMPLE_ROWS_PER_SEGMENT = 64
TOP_EVENTS_PER_SEGMENT = 12

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()

def rel_to_root(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")

def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)

def round_float(value: object, digits: int = 4) -> float:
    try:
        number = float(value)
    except Exception:
        number = 0.0
    if math.isnan(number) or math.isinf(number):
        number = 0.0
    return round(number, digits)

def quantile(values: list[float], ratio: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = max(0.0, min(1.0, ratio)) * (len(ordered) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return ordered[lo]
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)

def avg_top(values: list[float], ratio: float = 0.1) -> float:
    if not values:
        return 0.0
    count = max(1, int(len(values) * ratio))
    return statistics.mean(sorted(values, reverse=True)[:count])

def value_stats(values: list[float]) -> dict:
    if not values:
        return {
            "avg": 0.0,
            "min": 0.0,
            "max": 0.0,
            "std": 0.0,
            "p50": 0.0,
            "p90": 0.0,
            "p98": 0.0,
            "top10_avg": 0.0,
        }

    return {
        "avg": round_float(statistics.mean(values)),
        "min": round_float(min(values)),
        "max": round_float(max(values)),
        "std": round_float(statistics.pstdev(values) if len(values) > 1 else 0.0),
        "p50": round_float(quantile(values, 0.50)),
        "p90": round_float(quantile(values, 0.90)),
        "p98": round_float(quantile(values, 0.98)),
        "top10_avg": round_float(avg_top(values)),
    }
