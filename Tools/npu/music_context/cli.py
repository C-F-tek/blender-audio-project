"""CLI entrypoint for music context generation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .builder import build_music_context
from .common import (
    CHUNK_DIR,
    DEFAULT_ANALYSIS,
    DEFAULT_ANALYSIS_AI_CONTEXT,
    DEFAULT_BLENDER_KEYFRAMES_JSON,
    DEFAULT_COMPACT_JSON,
    DEFAULT_SEGMENT_SECONDS,
    DEFAULT_TRACK_SUMMARY,
    OUT_JSON,
    OUT_MD,
)

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
