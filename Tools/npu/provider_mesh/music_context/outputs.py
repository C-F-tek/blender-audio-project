"""Output renderers for music context artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from .common import OUT_MD, round_float

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
