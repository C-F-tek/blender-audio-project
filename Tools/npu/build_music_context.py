from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from datetime import datetime
from pathlib import Path

from ai_memory_context import build_ai_memory_context

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "output"
OUT_DIR = ROOT / "Tools" / "npu"
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


def scene_summary_from_json(path: Path, data: dict) -> dict:
    objects = data.get("objects", [])
    materials = data.get("materials", [])
    audio_mapping = data.get("audio_mapping", [])
    node_animation = data.get("node_animation", [])

    return {
        "file": rel_to_root(path),
        "type": "json",
        "keys": sorted(data.keys()),
        "scene_name": data.get("scene_name"),
        "visual_concept": data.get("visual_concept"),
        "style_mode": data.get("style_mode"),
        "environment": data.get("environment"),
        "lighting_style": data.get("lighting_style"),
        "palette": data.get("palette"),
        "camera": data.get("camera") or data.get("camera_style"),
        "objects_count": len(objects) if isinstance(objects, list) else 0,
        "materials_count": len(materials) if isinstance(materials, list) else 0,
        "audio_mapping_count": len(audio_mapping) if isinstance(audio_mapping, list) else 0,
        "node_animation_count": len(node_animation) if isinstance(node_animation, list) else 0,
        "object_names": [
            item.get("name") for item in objects if isinstance(item, dict) and item.get("name")
        ][:30],
        "audio_targets": [
            f"{item.get('target')}:{item.get('property')}:{item.get('band')}"
            for item in audio_mapping
            if isinstance(item, dict)
        ][:40],
    }


def load_scene_records(scene_files: list[Path]) -> list[dict]:
    records = []
    for path in scene_files:
        if not path.exists():
            continue

        text = read_text(path)
        record = {
            "file": rel_to_root(path),
            "chars": len(text),
            "lines": text.count("\n") + 1 if text else 0,
            "sha256": sha256_text(text),
            "content": text,
        }

        if path.suffix.lower() == ".json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError as exc:
                record["summary"] = {"file": rel_to_root(path), "type": "json", "error": str(exc)}
            else:
                record["summary"] = scene_summary_from_json(path, data)
        else:
            record["summary"] = {
                "file": rel_to_root(path),
                "type": "text",
                "chars": len(text),
                "lines": text.count("\n") + 1 if text else 0,
            }

        records.append(record)
    return records


def markdown_table_rows(rows: list[dict], keys: list[str]) -> str:
    lines = ["|" + "|".join(keys) + "|", "|" + "|".join(["---"] * len(keys)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(key, "")) for key in keys) + "|")
    return "\n".join(lines)


def write_chunk(path: Path, title: str, body: str) -> dict:
    text = f"# {title}\n\n{body.strip()}\n"
    path.write_text(text, encoding="utf-8")
    return {
        "path": rel_to_root(path),
        "chars": len(text),
        "sha256": sha256_text(text),
    }


def write_music_chunks(context: dict, scene_records: list[dict]) -> list[dict]:
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    for old_chunk in CHUNK_DIR.glob("chunk_*.md"):
        old_chunk.unlink()

    chunks = []
    chunk_index = 1

    overview = {
        "analysis_summary": context.get("analysis_summary"),
        "track_summary": context.get("track_summary"),
        "ai_memory_context": context.get("ai_memory_context"),
        "scene_summaries": [record["summary"] for record in scene_records],
    }
    chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_music_overview.md"
    chunks.append(
        {
            "index": chunk_index,
            "kind": "overview",
            **write_chunk(
                chunk_path,
                "NPU Music Overview",
                f"```json\n{json.dumps(overview, indent=2, ensure_ascii=False)}\n```",
            ),
        }
    )
    chunk_index += 1

    for segment in context.get("segments", []):
        table = markdown_table_rows(
            segment.get("sampled_frames", []),
            ["time", "low", "mid", "high", "onset", "beat"],
        )
        payload = {key: value for key, value in segment.items() if key not in {"sampled_frames"}}
        body = [
            "## Segment Summary\n",
            f"```json\n{json.dumps(payload, indent=2, ensure_ascii=False)}\n```\n",
            "## Sampled Frame Curve\n",
            table,
        ]
        chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_audio_segment_{segment['index']:03d}.md"
        chunks.append(
            {
                "index": chunk_index,
                "kind": "audio_segment",
                "segment_index": segment["index"],
                "start_sec": segment["start_sec"],
                "end_sec": segment["end_sec"],
                **write_chunk(
                    chunk_path, f"NPU Audio Segment {segment['index']:03d}", "\n\n".join(body)
                ),
            }
        )
        chunk_index += 1

    for record in scene_records:
        body = [
            "## Scene Summary\n",
            f"```json\n{json.dumps(record['summary'], indent=2, ensure_ascii=False)}\n```\n",
            "## Source\n",
            "```text\n",
            record["content"],
            "\n```",
        ]
        safe_name = Path(record["file"]).stem.replace(" ", "_")
        chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_scene_{safe_name}.md"
        chunks.append(
            {
                "index": chunk_index,
                "kind": "scene_spec",
                "source": record["file"],
                **write_chunk(chunk_path, f"NPU Scene Spec {record['file']}", "".join(body)),
            }
        )
        chunk_index += 1

    return chunks


def write_music_context_md(context: dict, scene_records: list[dict], chunks: list[dict]) -> None:
    summary = context.get("analysis_summary", {})
    meta = summary.get("meta", {})

    lines = [
        "# NPU Music Context\n\n",
        f"Generated: `{context['created_at']}`\n\n",
        "Purpose: compact long-context map for WAV analysis and generated scene JSON.\n\n",
        "## Track\n",
        f"- Name: `{summary.get('track_name')}`\n",
        f"- Duration: `{round_float(meta.get('duration_sec'), 3)}` sec\n",
        f"- FPS: `{meta.get('fps')}`\n",
        f"- BPM: `{round_float(meta.get('estimated_tempo_bpm'), 3)}`\n",
        f"- Frames: `{summary.get('frame_count')}`\n",
        f"- Beats: `{summary.get('beat_count')}`\n",
        f"- Segments: `{summary.get('segment_count')}` x `{summary.get('segment_seconds')}` sec\n\n",
        "## Top Energy Segments\n",
    ]

    for item in summary.get("top_energy_segments", []):
        lines.append(
            f"- Segment `{item['index']}` {item['start_sec']}-{item['end_sec']} sec: "
            f"{item['intensity']} / {item['dominant_band']} / score `{item['intensity_score']}`\n"
        )

    memory = context.get("ai_memory_context") or {}
    if memory:
        lines.append("\n## AI Memory Context\n")
        lines.append(f"- Scene brief: `{memory.get('scene_brief_json')}`\n")
        lines.append(f"- Has brief: `{memory.get('has_scene_brief')}`\n")
        for item in memory.get("durable_constraints", [])[:8]:
            lines.append(f"- Constraint: {item}\n")
        for asset in (memory.get("asset_memory") or {}).get("primary_assets", [])[:8]:
            lines.append(f"- Asset `{asset.get('role')}`: `{asset.get('path')}`\n")

    lines.append("\n## Scene Specs\n")
    for record in scene_records:
        record_summary = record["summary"]
        lines.append(
            f"- `{record['file']}`: {record_summary.get('type')} "
            f"objects `{record_summary.get('objects_count', '')}` "
            f"audio mappings `{record_summary.get('audio_mapping_count', '')}`\n"
        )

    lines.append("\n## Chunks\n")
    for chunk in chunks:
        label = chunk.get("kind", "chunk")
        detail = ""
        if label == "audio_segment":
            detail = f" segment {chunk.get('segment_index')} {chunk.get('start_sec')}-{chunk.get('end_sec')} sec"
        elif label == "scene_spec":
            detail = f" {chunk.get('source')}"
        lines.append(f"- `{chunk['path']}`: {label}{detail}\n")

    OUT_MD.write_text("".join(lines), encoding="utf-8")


def build_analysis_ai_context(context: dict) -> dict:
    return {
        "created_at": context.get("created_at"),
        "purpose": "Compact AI context. Do not use this file for Blender frame-by-frame keyframes.",
        "ai_memory_context": context.get("ai_memory_context"),
        "blender_keyframe_policy": {
            "use_full_analysis_json": True,
            "do_not_reduce_frames": True,
            "notes": "The segment data is only for AI reasoning; Blender animation must read the full analysis JSON.",
        },
        "analysis_summary": context.get("analysis_summary"),
        "track_summary": context.get("track_summary"),
        "scene_summaries": context.get("scene_summaries", []),
        "segments": [
            {
                "index": segment.get("index"),
                "start_sec": segment.get("start_sec"),
                "end_sec": segment.get("end_sec"),
                "duration_sec": segment.get("duration_sec"),
                "frame_count": segment.get("frame_count"),
                "beat_count": segment.get("beat_count"),
                "dominant_band": segment.get("dominant_band"),
                "intensity_score": segment.get("intensity_score"),
                "intensity": segment.get("intensity"),
                "stats": segment.get("stats"),
                "controls": segment.get("controls"),
                "beat_times": segment.get("beat_times", [])[:40],
                "top_events": segment.get("top_events", []),
            }
            for segment in context.get("segments", [])
        ],
    }


def write_blender_keyframe_alias(analysis_path: Path, blender_keyframes_path: Path) -> None:
    blender_keyframes_path.parent.mkdir(parents=True, exist_ok=True)
    if analysis_path.resolve() == blender_keyframes_path.resolve():
        return
    blender_keyframes_path.write_text(analysis_path.read_text(encoding="utf-8"), encoding="utf-8")


def build_music_context(
    analysis_path: Path | None = None,
    track_summary_path: Path | None = None,
    scene_files: list[Path] | None = None,
    segment_seconds: float = DEFAULT_SEGMENT_SECONDS,
    compact_json_path: Path | None = None,
    analysis_ai_context_path: Path | None = None,
    blender_keyframes_path: Path | None = None,
    run_ollama: bool = False,
    ollama_model: str = "qwen2.5-coder:14b",
) -> dict:
    analysis_path = Path(analysis_path or DEFAULT_ANALYSIS).resolve()
    track_summary_path = Path(track_summary_path or DEFAULT_TRACK_SUMMARY).resolve()
    compact_json_path = Path(compact_json_path or DEFAULT_COMPACT_JSON).resolve()
    analysis_ai_context_path = Path(
        analysis_ai_context_path or DEFAULT_ANALYSIS_AI_CONTEXT
    ).resolve()
    blender_keyframes_path = Path(
        blender_keyframes_path or DEFAULT_BLENDER_KEYFRAMES_JSON
    ).resolve()
    scene_files = scene_files or DEFAULT_SCENE_FILES

    if not analysis_path.exists():
        raise FileNotFoundError(f"Analysis JSON not found: {analysis_path}")

    analysis_summary, segments = summarize_analysis(analysis_path, segment_seconds)
    track_summary = load_json(track_summary_path) if track_summary_path.exists() else None
    scene_records = load_scene_records([Path(item).resolve() for item in scene_files])

    context = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "analysis_summary": analysis_summary,
        "track_summary": track_summary,
        "ai_memory_context": build_ai_memory_context(
            track_stem=analysis_summary.get("track_name")
            or analysis_path.stem.replace("_analysis", ""),
            output_dir=compact_json_path.parent,
        ),
        "scene_summaries": [record["summary"] for record in scene_records],
        "segments": segments,
    }

    chunks = write_music_chunks(context, scene_records)
    write_music_context_md(context, scene_records, chunks)

    manifest = {
        "created_at": context["created_at"],
        "root": str(ROOT),
        "analysis_json": rel_to_root(analysis_path),
        "blender_keyframes_json": rel_to_root(blender_keyframes_path),
        "analysis_ai_context_json": rel_to_root(analysis_ai_context_path),
        "track_summary_json": rel_to_root(track_summary_path)
        if track_summary_path.exists()
        else None,
        "compact_json": rel_to_root(compact_json_path),
        "ai_memory_context": context.get("ai_memory_context"),
        "context_md": rel_to_root(OUT_MD),
        "chunk_dir": rel_to_root(CHUNK_DIR),
        "chunk_count": len(chunks),
        "segment_seconds": segment_seconds,
        "segment_count": len(segments),
        "scene_files": [
            {
                "file": record["file"],
                "chars": record["chars"],
                "lines": record["lines"],
                "sha256": record["sha256"],
                "summary": record["summary"],
            }
            for record in scene_records
        ],
        "chunks": chunks,
    }

    OUT_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    compact_json_path.parent.mkdir(parents=True, exist_ok=True)
    compact_json_path.write_text(
        json.dumps(context, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    analysis_ai_context_path.parent.mkdir(parents=True, exist_ok=True)
    analysis_ai_context_path.write_text(
        json.dumps(build_analysis_ai_context(context), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_blender_keyframe_alias(analysis_path, blender_keyframes_path)

    if run_ollama:
        try:
            from run_ollama_music_agent import run_ollama_music_agent

            ollama_result = run_ollama_music_agent(
                context_json=analysis_ai_context_path,
                model=ollama_model,
            )
        except Exception as exc:
            manifest["ollama_error"] = str(exc)
            OUT_JSON.write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            print(f"[WARN] Ollama music agent non eseguito: {exc}")
        else:
            manifest["ollama_music_insights_json"] = rel_to_root(ollama_result["out_json"])
            manifest["ollama_music_insights_md"] = rel_to_root(ollama_result["out_md"])
            OUT_JSON.write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
            )

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build long-context music data files for the local NPU agent."
    )
    parser.add_argument("--analysis", default=str(DEFAULT_ANALYSIS))
    parser.add_argument("--track-summary", default=str(DEFAULT_TRACK_SUMMARY))
    parser.add_argument("--compact-json", default=str(DEFAULT_COMPACT_JSON))
    parser.add_argument("--analysis-ai-context", default=str(DEFAULT_ANALYSIS_AI_CONTEXT))
    parser.add_argument("--blender-keyframes-json", default=str(DEFAULT_BLENDER_KEYFRAMES_JSON))
    parser.add_argument("--segment-seconds", type=float, default=DEFAULT_SEGMENT_SECONDS)
    parser.add_argument("--scene-file", action="append", default=[])
    parser.add_argument("--run-ollama", action="store_true")
    parser.add_argument("--ollama-model", default="qwen2.5-coder:14b")
    args = parser.parse_args()

    scene_files = [Path(item) for item in args.scene_file] if args.scene_file else None
    manifest = build_music_context(
        analysis_path=Path(args.analysis),
        track_summary_path=Path(args.track_summary),
        scene_files=scene_files,
        segment_seconds=args.segment_seconds,
        compact_json_path=Path(args.compact_json),
        analysis_ai_context_path=Path(args.analysis_ai_context),
        blender_keyframes_path=Path(args.blender_keyframes_json),
        run_ollama=args.run_ollama,
        ollama_model=args.ollama_model,
    )

    print(f"[OK] Wrote: {OUT_MD}")
    print(f"[OK] Wrote: {OUT_JSON}")
    print(f"[OK] Wrote: {manifest['compact_json']}")
    print(f"[OK] Wrote: {manifest['analysis_ai_context_json']}")
    print(f"[OK] Wrote: {manifest['blender_keyframes_json']}")
    print(f"[OK] Wrote chunks: {CHUNK_DIR} ({manifest['chunk_count']} files)")


if __name__ == "__main__":
    main()
