# Project Code Chunk 120/212

- File: `Tools/npu/build_music_context.py`
- Part: `3`
- Lines: `548-711`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `hashlib`, `json`, `math`, `statistics`, `from datetime import datetime`, `from ai_memory_context import build_ai_memory_context`
- Functions: `sha256_text(text)` line 41; `rel_to_root(path)` line 45; `read_text(path)` line 52; `load_json(path)` line 56; `round_float(value, digits)` line 61; `quantile(values, ratio)` line 71; `avg_top(values, ratio)` line 85; `value_stats(values)` line 92; `frame_values(frames, key)` line 117; `energy_stats(frames)` line 121; `dominant_band(stats)` line 131; `intensity_label(score)` line 140; `segment_score(stats)` line 152; `control_suggestions(stats, beat_count)` line 162; `split_segments(frames, segment_seconds, duration)` line 176; `sampled_frames(frames, max_rows)` line 189; `top_events(frames, limit)` line 210; `beats_in_range(beats, start, end)` line 235; `build_segments(analysis, segment_seconds)` line 239; `summarize_analysis(analysis_path, segment_seconds)` line 273; `scene_summary_from_json(path, data)` line 319; `load_scene_records(scene_files)` line 353; `markdown_table_rows(rows, keys)` line 387; `write_chunk(path, title, body)` line 394; `write_music_chunks(context, scene_records)` line 404; `write_music_context_md(context, scene_records, chunks)` line 481; `build_analysis_ai_context(context)` line 538; `write_blender_keyframe_alias(analysis_path, blender_keyframes_path)` line 572; `build_music_context(analysis_path, track_summary_path, scene_files, segment_seconds, compact_json_path, analysis_ai_context_path, blender_keyframes_path, run_ollama, ollama_model)` line 579; `main()` line 676
- Assignments: `ROOT`, `OUTPUT_DIR`, `OUT_DIR`, `CHUNK_DIR`, `DEFAULT_TRACK_STEM`, `DEFAULT_ANALYSIS`, `DEFAULT_TRACK_SUMMARY`, `DEFAULT_COMPACT_JSON`, `DEFAULT_ANALYSIS_AI_CONTEXT`, `DEFAULT_BLENDER_KEYFRAMES_JSON`, `OUT_MD`, `OUT_JSON`, `DEFAULT_SCENE_FILES`, `DEFAULT_SEGMENT_SECONDS`, `SAMPLE_ROWS_PER_SEGMENT`, `TOP_EVENTS_PER_SEGMENT`

## Content
```py
00548:         "analysis_summary": context.get("analysis_summary"),
00549:         "track_summary": context.get("track_summary"),
00550:         "scene_summaries": context.get("scene_summaries", []),
00551:         "segments": [
00552:             {
00553:                 "index": segment.get("index"),
00554:                 "start_sec": segment.get("start_sec"),
00555:                 "end_sec": segment.get("end_sec"),
00556:                 "duration_sec": segment.get("duration_sec"),
00557:                 "frame_count": segment.get("frame_count"),
00558:                 "beat_count": segment.get("beat_count"),
00559:                 "dominant_band": segment.get("dominant_band"),
00560:                 "intensity_score": segment.get("intensity_score"),
00561:                 "intensity": segment.get("intensity"),
00562:                 "stats": segment.get("stats"),
00563:                 "controls": segment.get("controls"),
00564:                 "beat_times": segment.get("beat_times", [])[:40],
00565:                 "top_events": segment.get("top_events", []),
00566:             }
00567:             for segment in context.get("segments", [])
00568:         ],
00569:     }
00570: 
00571: 
00572: def write_blender_keyframe_alias(analysis_path: Path, blender_keyframes_path: Path) -> None:
00573:     blender_keyframes_path.parent.mkdir(parents=True, exist_ok=True)
00574:     if analysis_path.resolve() == blender_keyframes_path.resolve():
00575:         return
00576:     blender_keyframes_path.write_text(analysis_path.read_text(encoding="utf-8"), encoding="utf-8")
00577: 
00578: 
00579: def build_music_context(
00580:     analysis_path: Path | None = None,
00581:     track_summary_path: Path | None = None,
00582:     scene_files: list[Path] | None = None,
00583:     segment_seconds: float = DEFAULT_SEGMENT_SECONDS,
00584:     compact_json_path: Path | None = None,
00585:     analysis_ai_context_path: Path | None = None,
00586:     blender_keyframes_path: Path | None = None,
00587:     run_ollama: bool = False,
00588:     ollama_model: str = "qwen2.5-coder:14b",
00589: ) -> dict:
00590:     analysis_path = Path(analysis_path or DEFAULT_ANALYSIS).resolve()
00591:     track_summary_path = Path(track_summary_path or DEFAULT_TRACK_SUMMARY).resolve()
00592:     compact_json_path = Path(compact_json_path or DEFAULT_COMPACT_JSON).resolve()
00593:     analysis_ai_context_path = Path(analysis_ai_context_path or DEFAULT_ANALYSIS_AI_CONTEXT).resolve()
00594:     blender_keyframes_path = Path(blender_keyframes_path or DEFAULT_BLENDER_KEYFRAMES_JSON).resolve()
00595:     scene_files = scene_files or DEFAULT_SCENE_FILES
00596: 
00597:     if not analysis_path.exists():
00598:         raise FileNotFoundError(f"Analysis JSON not found: {analysis_path}")
00599: 
00600:     analysis_summary, segments = summarize_analysis(analysis_path, segment_seconds)
00601:     track_summary = load_json(track_summary_path) if track_summary_path.exists() else None
00602:     scene_records = load_scene_records([Path(item).resolve() for item in scene_files])
00603: 
00604:     context = {
00605:         "created_at": datetime.now().isoformat(timespec="seconds"),
00606:         "analysis_summary": analysis_summary,
00607:         "track_summary": track_summary,
00608:         "ai_memory_context": build_ai_memory_context(
00609:             track_stem=analysis_summary.get("track_name") or analysis_path.stem.replace("_analysis", ""),
00610:             output_dir=compact_json_path.parent,
00611:         ),
00612:         "scene_summaries": [record["summary"] for record in scene_records],
00613:         "segments": segments,
00614:     }
00615: 
00616:     chunks = write_music_chunks(context, scene_records)
00617:     write_music_context_md(context, scene_records, chunks)
00618: 
00619:     manifest = {
00620:         "created_at": context["created_at"],
00621:         "root": str(ROOT),
00622:         "analysis_json": rel_to_root(analysis_path),
00623:         "blender_keyframes_json": rel_to_root(blender_keyframes_path),
00624:         "analysis_ai_context_json": rel_to_root(analysis_ai_context_path),
00625:         "track_summary_json": rel_to_root(track_summary_path) if track_summary_path.exists() else None,
00626:         "compact_json": rel_to_root(compact_json_path),
00627:         "ai_memory_context": context.get("ai_memory_context"),
00628:         "context_md": rel_to_root(OUT_MD),
00629:         "chunk_dir": rel_to_root(CHUNK_DIR),
00630:         "chunk_count": len(chunks),
00631:         "segment_seconds": segment_seconds,
00632:         "segment_count": len(segments),
00633:         "scene_files": [
00634:             {
00635:                 "file": record["file"],
00636:                 "chars": record["chars"],
00637:                 "lines": record["lines"],
00638:                 "sha256": record["sha256"],
00639:                 "summary": record["summary"],
00640:             }
00641:             for record in scene_records
00642:         ],
00643:         "chunks": chunks,
00644:     }
00645: 
00646:     OUT_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
00647:     compact_json_path.parent.mkdir(parents=True, exist_ok=True)
00648:     compact_json_path.write_text(json.dumps(context, indent=2, ensure_ascii=False), encoding="utf-8")
00649:     analysis_ai_context_path.parent.mkdir(parents=True, exist_ok=True)
00650:     analysis_ai_context_path.write_text(
00651:         json.dumps(build_analysis_ai_context(context), indent=2, ensure_ascii=False),
00652:         encoding="utf-8",
00653:     )
00654:     write_blender_keyframe_alias(analysis_path, blender_keyframes_path)
00655: 
00656:     if run_ollama:
00657:         try:
00658:             from run_ollama_music_agent import run_ollama_music_agent
00659: 
00660:             ollama_result = run_ollama_music_agent(
00661:                 context_json=analysis_ai_context_path,
00662:                 model=ollama_model,
00663:             )
00664:         except Exception as exc:
00665:             manifest["ollama_error"] = str(exc)
00666:             OUT_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
00667:             print(f"[WARN] Ollama music agent non eseguito: {exc}")
00668:         else:
00669:             manifest["ollama_music_insights_json"] = rel_to_root(ollama_result["out_json"])
00670:             manifest["ollama_music_insights_md"] = rel_to_root(ollama_result["out_md"])
00671:             OUT_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
00672: 
00673:     return manifest
00674: 
00675: 
00676: def main() -> None:
00677:     parser = argparse.ArgumentParser(description="Build long-context music data files for the local NPU agent.")
00678:     parser.add_argument("--analysis", default=str(DEFAULT_ANALYSIS))
00679:     parser.add_argument("--track-summary", default=str(DEFAULT_TRACK_SUMMARY))
00680:     parser.add_argument("--compact-json", default=str(DEFAULT_COMPACT_JSON))
00681:     parser.add_argument("--analysis-ai-context", default=str(DEFAULT_ANALYSIS_AI_CONTEXT))
00682:     parser.add_argument("--blender-keyframes-json", default=str(DEFAULT_BLENDER_KEYFRAMES_JSON))
00683:     parser.add_argument("--segment-seconds", type=float, default=DEFAULT_SEGMENT_SECONDS)
00684:     parser.add_argument("--scene-file", action="append", default=[])
00685:     parser.add_argument("--run-ollama", action="store_true")
00686:     parser.add_argument("--ollama-model", default="qwen2.5-coder:14b")
00687:     args = parser.parse_args()
00688: 
00689:     scene_files = [Path(item) for item in args.scene_file] if args.scene_file else None
00690:     manifest = build_music_context(
00691:         analysis_path=Path(args.analysis),
00692:         track_summary_path=Path(args.track_summary),
00693:         scene_files=scene_files,
00694:         segment_seconds=args.segment_seconds,
00695:         compact_json_path=Path(args.compact_json),
00696:         analysis_ai_context_path=Path(args.analysis_ai_context),
00697:         blender_keyframes_path=Path(args.blender_keyframes_json),
00698:         run_ollama=args.run_ollama,
00699:         ollama_model=args.ollama_model,
00700:     )
00701: 
00702:     print(f"[OK] Wrote: {OUT_MD}")
00703:     print(f"[OK] Wrote: {OUT_JSON}")
00704:     print(f"[OK] Wrote: {manifest['compact_json']}")
00705:     print(f"[OK] Wrote: {manifest['analysis_ai_context_json']}")
00706:     print(f"[OK] Wrote: {manifest['blender_keyframes_json']}")
00707:     print(f"[OK] Wrote chunks: {CHUNK_DIR} ({manifest['chunk_count']} files)")
00708: 
00709: 
00710: if __name__ == "__main__":
00711:     main()
```
