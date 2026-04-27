# Project Code Chunk 119/212

- File: `Tools/npu/build_music_context.py`
- Part: `2`
- Lines: `286-547`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `hashlib`, `json`, `math`, `statistics`, `from datetime import datetime`, `from ai_memory_context import build_ai_memory_context`
- Functions: `sha256_text(text)` line 41; `rel_to_root(path)` line 45; `read_text(path)` line 52; `load_json(path)` line 56; `round_float(value, digits)` line 61; `quantile(values, ratio)` line 71; `avg_top(values, ratio)` line 85; `value_stats(values)` line 92; `frame_values(frames, key)` line 117; `energy_stats(frames)` line 121; `dominant_band(stats)` line 131; `intensity_label(score)` line 140; `segment_score(stats)` line 152; `control_suggestions(stats, beat_count)` line 162; `split_segments(frames, segment_seconds, duration)` line 176; `sampled_frames(frames, max_rows)` line 189; `top_events(frames, limit)` line 210; `beats_in_range(beats, start, end)` line 235; `build_segments(analysis, segment_seconds)` line 239; `summarize_analysis(analysis_path, segment_seconds)` line 273; `scene_summary_from_json(path, data)` line 319; `load_scene_records(scene_files)` line 353; `markdown_table_rows(rows, keys)` line 387; `write_chunk(path, title, body)` line 394; `write_music_chunks(context, scene_records)` line 404; `write_music_context_md(context, scene_records, chunks)` line 481; `build_analysis_ai_context(context)` line 538; `write_blender_keyframe_alias(analysis_path, blender_keyframes_path)` line 572; `build_music_context(analysis_path, track_summary_path, scene_files, segment_seconds, compact_json_path, analysis_ai_context_path, blender_keyframes_path, run_ollama, ollama_model)` line 579; `main()` line 676
- Assignments: `ROOT`, `OUTPUT_DIR`, `OUT_DIR`, `CHUNK_DIR`, `DEFAULT_TRACK_STEM`, `DEFAULT_ANALYSIS`, `DEFAULT_TRACK_SUMMARY`, `DEFAULT_COMPACT_JSON`, `DEFAULT_ANALYSIS_AI_CONTEXT`, `DEFAULT_BLENDER_KEYFRAMES_JSON`, `OUT_MD`, `OUT_JSON`, `DEFAULT_SCENE_FILES`, `DEFAULT_SEGMENT_SECONDS`, `SAMPLE_ROWS_PER_SEGMENT`, `TOP_EVENTS_PER_SEGMENT`

## Content
```py
00286:         "track_name": analysis_path.stem.replace("_analysis", ""),
00287:         "meta": meta,
00288:         "frame_count": len(frames),
00289:         "beat_count": len(beats),
00290:         "segment_seconds": segment_seconds,
00291:         "segment_count": len(segments),
00292:         "overall_stats": stats,
00293:         "top_energy_segments": [
00294:             {
00295:                 "index": item["index"],
00296:                 "start_sec": item["start_sec"],
00297:                 "end_sec": item["end_sec"],
00298:                 "dominant_band": item["dominant_band"],
00299:                 "intensity_score": item["intensity_score"],
00300:                 "intensity": item["intensity"],
00301:             }
00302:             for item in top_by_energy
00303:         ],
00304:         "top_onset_segments": [
00305:             {
00306:                 "index": item["index"],
00307:                 "start_sec": item["start_sec"],
00308:                 "end_sec": item["end_sec"],
00309:                 "onset_p98": item["stats"]["onset"]["p98"],
00310:                 "beat_count": item["beat_count"],
00311:             }
00312:             for item in top_by_onset
00313:         ],
00314:     }
00315: 
00316:     return summary, segments
00317: 
00318: 
00319: def scene_summary_from_json(path: Path, data: dict) -> dict:
00320:     objects = data.get("objects", [])
00321:     materials = data.get("materials", [])
00322:     audio_mapping = data.get("audio_mapping", [])
00323:     node_animation = data.get("node_animation", [])
00324: 
00325:     return {
00326:         "file": rel_to_root(path),
00327:         "type": "json",
00328:         "keys": sorted(data.keys()),
00329:         "scene_name": data.get("scene_name"),
00330:         "visual_concept": data.get("visual_concept"),
00331:         "style_mode": data.get("style_mode"),
00332:         "environment": data.get("environment"),
00333:         "lighting_style": data.get("lighting_style"),
00334:         "palette": data.get("palette"),
00335:         "camera": data.get("camera") or data.get("camera_style"),
00336:         "objects_count": len(objects) if isinstance(objects, list) else 0,
00337:         "materials_count": len(materials) if isinstance(materials, list) else 0,
00338:         "audio_mapping_count": len(audio_mapping) if isinstance(audio_mapping, list) else 0,
00339:         "node_animation_count": len(node_animation) if isinstance(node_animation, list) else 0,
00340:         "object_names": [
00341:             item.get("name")
00342:             for item in objects
00343:             if isinstance(item, dict) and item.get("name")
00344:         ][:30],
00345:         "audio_targets": [
00346:             f"{item.get('target')}:{item.get('property')}:{item.get('band')}"
00347:             for item in audio_mapping
00348:             if isinstance(item, dict)
00349:         ][:40],
00350:     }
00351: 
00352: 
00353: def load_scene_records(scene_files: list[Path]) -> list[dict]:
00354:     records = []
00355:     for path in scene_files:
00356:         if not path.exists():
00357:             continue
00358: 
00359:         text = read_text(path)
00360:         record = {
00361:             "file": rel_to_root(path),
00362:             "chars": len(text),
00363:             "lines": text.count("\n") + 1 if text else 0,
00364:             "sha256": sha256_text(text),
00365:             "content": text,
00366:         }
00367: 
00368:         if path.suffix.lower() == ".json":
00369:             try:
00370:                 data = json.loads(text)
00371:             except json.JSONDecodeError as exc:
00372:                 record["summary"] = {"file": rel_to_root(path), "type": "json", "error": str(exc)}
00373:             else:
00374:                 record["summary"] = scene_summary_from_json(path, data)
00375:         else:
00376:             record["summary"] = {
00377:                 "file": rel_to_root(path),
00378:                 "type": "text",
00379:                 "chars": len(text),
00380:                 "lines": text.count("\n") + 1 if text else 0,
00381:             }
00382: 
00383:         records.append(record)
00384:     return records
00385: 
00386: 
00387: def markdown_table_rows(rows: list[dict], keys: list[str]) -> str:
00388:     lines = ["|" + "|".join(keys) + "|", "|" + "|".join(["---"] * len(keys)) + "|"]
00389:     for row in rows:
00390:         lines.append("|" + "|".join(str(row.get(key, "")) for key in keys) + "|")
00391:     return "\n".join(lines)
00392: 
00393: 
00394: def write_chunk(path: Path, title: str, body: str) -> dict:
00395:     text = f"# {title}\n\n{body.strip()}\n"
00396:     path.write_text(text, encoding="utf-8")
00397:     return {
00398:         "path": rel_to_root(path),
00399:         "chars": len(text),
00400:         "sha256": sha256_text(text),
00401:     }
00402: 
00403: 
00404: def write_music_chunks(context: dict, scene_records: list[dict]) -> list[dict]:
00405:     CHUNK_DIR.mkdir(parents=True, exist_ok=True)
00406:     for old_chunk in CHUNK_DIR.glob("chunk_*.md"):
00407:         old_chunk.unlink()
00408: 
00409:     chunks = []
00410:     chunk_index = 1
00411: 
00412:     overview = {
00413:         "analysis_summary": context.get("analysis_summary"),
00414:         "track_summary": context.get("track_summary"),
00415:         "ai_memory_context": context.get("ai_memory_context"),
00416:         "scene_summaries": [record["summary"] for record in scene_records],
00417:     }
00418:     chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_music_overview.md"
00419:     chunks.append(
00420:         {
00421:             "index": chunk_index,
00422:             "kind": "overview",
00423:             **write_chunk(chunk_path, "NPU Music Overview", f"```json\n{json.dumps(overview, indent=2, ensure_ascii=False)}\n```"),
00424:         }
00425:     )
00426:     chunk_index += 1
00427: 
00428:     for segment in context.get("segments", []):
00429:         table = markdown_table_rows(
00430:             segment.get("sampled_frames", []),
00431:             ["time", "low", "mid", "high", "onset", "beat"],
00432:         )
00433:         payload = {
00434:             key: value
00435:             for key, value in segment.items()
00436:             if key not in {"sampled_frames"}
00437:         }
00438:         body = [
00439:             "## Segment Summary\n",
00440:             f"```json\n{json.dumps(payload, indent=2, ensure_ascii=False)}\n```\n",
00441:             "## Sampled Frame Curve\n",
00442:             table,
00443:         ]
00444:         chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_audio_segment_{segment['index']:03d}.md"
00445:         chunks.append(
00446:             {
00447:                 "index": chunk_index,
00448:                 "kind": "audio_segment",
00449:                 "segment_index": segment["index"],
00450:                 "start_sec": segment["start_sec"],
00451:                 "end_sec": segment["end_sec"],
00452:                 **write_chunk(chunk_path, f"NPU Audio Segment {segment['index']:03d}", "\n\n".join(body)),
00453:             }
00454:         )
00455:         chunk_index += 1
00456: 
00457:     for record in scene_records:
00458:         body = [
00459:             "## Scene Summary\n",
00460:             f"```json\n{json.dumps(record['summary'], indent=2, ensure_ascii=False)}\n```\n",
00461:             "## Source\n",
00462:             "```text\n",
00463:             record["content"],
00464:             "\n```",
00465:         ]
00466:         safe_name = Path(record["file"]).stem.replace(" ", "_")
00467:         chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_scene_{safe_name}.md"
00468:         chunks.append(
00469:             {
00470:                 "index": chunk_index,
00471:                 "kind": "scene_spec",
00472:                 "source": record["file"],
00473:                 **write_chunk(chunk_path, f"NPU Scene Spec {record['file']}", "".join(body)),
00474:             }
00475:         )
00476:         chunk_index += 1
00477: 
00478:     return chunks
00479: 
00480: 
00481: def write_music_context_md(context: dict, scene_records: list[dict], chunks: list[dict]) -> None:
00482:     summary = context.get("analysis_summary", {})
00483:     meta = summary.get("meta", {})
00484: 
00485:     lines = [
00486:         "# NPU Music Context\n\n",
00487:         f"Generated: `{context['created_at']}`\n\n",
00488:         "Purpose: compact long-context map for WAV analysis and generated scene JSON.\n\n",
00489:         "## Track\n",
00490:         f"- Name: `{summary.get('track_name')}`\n",
00491:         f"- Duration: `{round_float(meta.get('duration_sec'), 3)}` sec\n",
00492:         f"- FPS: `{meta.get('fps')}`\n",
00493:         f"- BPM: `{round_float(meta.get('estimated_tempo_bpm'), 3)}`\n",
00494:         f"- Frames: `{summary.get('frame_count')}`\n",
00495:         f"- Beats: `{summary.get('beat_count')}`\n",
00496:         f"- Segments: `{summary.get('segment_count')}` x `{summary.get('segment_seconds')}` sec\n\n",
00497:         "## Top Energy Segments\n",
00498:     ]
00499: 
00500:     for item in summary.get("top_energy_segments", []):
00501:         lines.append(
00502:             f"- Segment `{item['index']}` {item['start_sec']}-{item['end_sec']} sec: "
00503:             f"{item['intensity']} / {item['dominant_band']} / score `{item['intensity_score']}`\n"
00504:         )
00505: 
00506:     memory = context.get("ai_memory_context") or {}
00507:     if memory:
00508:         lines.append("\n## AI Memory Context\n")
00509:         lines.append(f"- Scene brief: `{memory.get('scene_brief_json')}`\n")
00510:         lines.append(f"- Has brief: `{memory.get('has_scene_brief')}`\n")
00511:         for item in memory.get("durable_constraints", [])[:8]:
00512:             lines.append(f"- Constraint: {item}\n")
00513:         for asset in (memory.get("asset_memory") or {}).get("primary_assets", [])[:8]:
00514:             lines.append(f"- Asset `{asset.get('role')}`: `{asset.get('path')}`\n")
00515: 
00516:     lines.append("\n## Scene Specs\n")
00517:     for record in scene_records:
00518:         record_summary = record["summary"]
00519:         lines.append(
00520:             f"- `{record['file']}`: {record_summary.get('type')} "
00521:             f"objects `{record_summary.get('objects_count', '')}` "
00522:             f"audio mappings `{record_summary.get('audio_mapping_count', '')}`\n"
00523:         )
00524: 
00525:     lines.append("\n## Chunks\n")
00526:     for chunk in chunks:
00527:         label = chunk.get("kind", "chunk")
00528:         detail = ""
00529:         if label == "audio_segment":
00530:             detail = f" segment {chunk.get('segment_index')} {chunk.get('start_sec')}-{chunk.get('end_sec')} sec"
00531:         elif label == "scene_spec":
00532:             detail = f" {chunk.get('source')}"
00533:         lines.append(f"- `{chunk['path']}`: {label}{detail}\n")
00534: 
00535:     OUT_MD.write_text("".join(lines), encoding="utf-8")
00536: 
00537: 
00538: def build_analysis_ai_context(context: dict) -> dict:
00539:     return {
00540:         "created_at": context.get("created_at"),
00541:         "purpose": "Compact AI context. Do not use this file for Blender frame-by-frame keyframes.",
00542:         "ai_memory_context": context.get("ai_memory_context"),
00543:         "blender_keyframe_policy": {
00544:             "use_full_analysis_json": True,
00545:             "do_not_reduce_frames": True,
00546:             "notes": "The segment data is only for AI reasoning; Blender animation must read the full analysis JSON.",
00547:         },
```
