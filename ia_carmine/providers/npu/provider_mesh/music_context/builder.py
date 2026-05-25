"""Music context assembly."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .analysis import summarize_analysis
from .chunks import write_music_chunks
from .common import (
    CHUNK_DIR,
    DEFAULT_ANALYSIS,
    DEFAULT_ANALYSIS_AI_CONTEXT,
    DEFAULT_BLENDER_KEYFRAMES_JSON,
    DEFAULT_COMPACT_JSON,
    DEFAULT_SCENE_FILES,
    DEFAULT_SEGMENT_SECONDS,
    DEFAULT_TRACK_SUMMARY,
    OUT_JSON,
    OUT_MD,
    ROOT,
    build_ai_memory_context,
    load_json,
    rel_to_root,
)
from .outputs import build_analysis_ai_context, write_blender_keyframe_alias, write_music_context_md
from .scene import load_scene_records

def build_music_context(
    analysis_path: Path | None = None,
    track_summary_path: Path | None = None,
    scene_files: list[Path] | None = None,
    segment_seconds: float = DEFAULT_SEGMENT_SECONDS,
    compact_json_path: Path | None = None,
    analysis_ai_context_path: Path | None = None,
    blender_keyframes_path: Path | None = None,
    run_ollama: bool = False,
    ollama_model: str = "",
) -> dict:
    if run_ollama and not str(ollama_model or "").strip():
        raise ValueError("ollama_model_explicit_required")
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
