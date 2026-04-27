# Project Code Chunk 193/212

- File: `Tools/workflow/project_awareness.py`
- Part: `2`
- Lines: `250-353`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `from typing import Any`, `json`
- Functions: `now_iso()` line 15; `read_json(path)` line 19; `file_status(path)` line 29; `compact_assets(asset_inventory)` line 39; `infer_track_identity(track_stem)` line 59; `compact_track_read(music_context)` line 77; `deterministic_track_opinion(track_identity, music_context)` line 104; `build_verified_answers(awareness, music_context)` line 135; `build_preflight_answers_for_message(user_message, awareness, music_context)` line 204; `build_project_awareness()` line 237; `save_project_awareness(awareness)` line 330
- Assignments: `ROOT`, `OUTPUT_DIR`, `NPU_DIR`, `INDEX_AI_DIR`

## Content
```py
00250:         "analysis_json": output_dir / f"{track_stem}_analysis.json",
00251:         "track_summary_json": output_dir / f"{track_stem}_track_summary.json",
00252:         "music_context_json": output_dir / f"{track_stem}_music_context.json",
00253:         "analysis_ai_context_json": output_dir / f"{track_stem}_analysis_ai_context.json",
00254:         "blender_keyframes_json": output_dir / f"{track_stem}_analysis_blender_keyframes.json",
00255:         "scene_brief_json": output_dir / f"{track_stem}_scene_brief.json",
00256:         "asset_inventory_json": output_dir / "spaziotempo_asset_inventory.json",
00257:         "dual_ai_plan_json": output_dir / f"{track_stem}_dual_ai_scene_plan.json",
00258:         "gpu_task_packet_json": output_dir / f"{track_stem}_gpu_task_packet.json",
00259:         "ai_implementation_draft_json": output_dir / f"{track_stem}_ai_implementation_draft.json",
00260:         "generated_scene_script": INDEX_AI_DIR / "scene_scripts" / f"{slug}_scene_builder_candidate.py",
00261:         "project_code_index": INDEX_AI_DIR / "project_code_index.md",
00262:         "project_code_manifest": INDEX_AI_DIR / "project_code_manifest.json",
00263:         "npu_music_context_md": NPU_DIR / "npu_music_context.md",
00264:         "npu_music_manifest": NPU_DIR / "npu_music_manifest.json",
00265:         "npu_code_index": NPU_DIR / "npu_code_index.md",
00266:         "npu_manual_index": NPU_DIR / "npu_blender_manual_index.md",
00267:         "npu_preflight": NPU_DIR / "npu_preflight_report.json",
00268:     }
00269: 
00270:     statuses = {name: file_status(path) for name, path in key_paths.items()}
00271:     missing = [name for name, item in statuses.items() if not item["exists"] and name not in {"ai_implementation_draft_json", "generated_scene_script"}]
00272:     ready_inputs = all(statuses[name]["exists"] for name in ["analysis_json", "music_context_json", "analysis_ai_context_json", "blender_keyframes_json"])
00273:     can_generate_script = ready_inputs and statuses["scene_brief_json"]["exists"] and statuses["asset_inventory_json"]["exists"]
00274: 
00275:     music_context = music_context or read_json(key_paths["music_context_json"])
00276:     asset_inventory = asset_inventory or read_json(output_dir / "spaziotempo_asset_inventory.json")
00277:     npu_preflight = read_json(key_paths["npu_preflight"])
00278:     segment_count = len(music_context.get("segments") or [])
00279: 
00280:     awareness = {
00281:         "format": "SPAZIOTEMPO_PROJECT_AWARENESS_V1",
00282:         "generated_at": now_iso(),
00283:         "track_stem": track_stem,
00284:         "audio_path": audio_path,
00285:         "track_identity": infer_track_identity(track_stem),
00286:         "project_identity": {
00287:             "name": "Spaziotempo Blender audio-reactive album visual pipeline",
00288:             "root": str(ROOT),
00289:             "user_runs_blender_and_render": True,
00290:             "assistant_should_not_launch_blender_or_render": True,
00291:             "current_goal": "Generate/review standalone Blender scene scripts from WAV-derived JSON, memory, assets and project style.",
00292:         },
00293:         "pipeline_state": {
00294:             "audio_already_loaded_by_pipeline": Path(audio_path).exists(),
00295:             "wav_analysis_ready": ready_inputs,
00296:             "music_context_ready": statuses["music_context_json"]["exists"],
00297:             "project_index_ready": statuses["project_code_index"]["exists"],
00298:             "manual_index_ready": statuses["npu_manual_index"]["exists"],
00299:             "service_packet_ready": statuses["gpu_task_packet_json"]["exists"],
00300:             "scene_brief_ready": statuses["scene_brief_json"]["exists"],
00301:             "can_generate_scene_script": can_generate_script,
00302:             "segment_count": segment_count,
00303:         },
00304:         "technical_files": statuses,
00305:         "asset_awareness": {
00306:             "asset_count": asset_inventory.get("asset_count", 0),
00307:             "primary_assets": compact_assets(asset_inventory),
00308:         },
00309:         "npu_context": {
00310:             "preflight_ready": bool(npu_preflight.get("ready")) if npu_preflight else False,
00311:             "available_devices": npu_preflight.get("available_devices", []) if npu_preflight else [],
00312:             "can_delegate_uncertainty": bool(npu_preflight.get("ready")),
00313:             "fallback": "If NPU is not ready, use deterministic project awareness and existing chunks instead of pretending uncertainty.",
00314:         },
00315:         "director_rules": [
00316:             "Never suggest manually importing audio into Blender; the WAV is already represented by analysis/music/keyframe JSON.",
00317:             "Never suggest opening Blender as the next generic step; the user decides when to run Blender.",
00318:             "Do not suggest rebuilding from scratch if technical files already exist.",
00319:             "When technical files exist, refer to the pipeline action: scene brief, dual AI plan, scene script draft, hot update, or review generated script.",
00320:             "Use project asset roles. If user says ball, prefer primary_ball_asset.",
00321:             "Full analysis_blender_keyframes JSON is authoritative and must not be summarized away.",
00322:             "If unsure, say which technical file/chunk should be checked, not generic Blender advice.",
00323:         ],
00324:         "missing_or_suspicious": missing,
00325:     }
00326:     awareness["verified_answers"] = build_verified_answers(awareness, music_context)
00327:     return awareness
00328: 
00329: 
00330: def save_project_awareness(awareness: dict[str, Any]) -> dict[str, str]:
00331:     patch_dir = INDEX_AI_DIR / "patch_library"
00332:     patch_dir.mkdir(parents=True, exist_ok=True)
00333:     slug = "".join(ch.lower() if ch.isalnum() else "_" for ch in str(awareness.get("track_stem", "track"))).strip("_")
00334:     slug = "_".join(part for part in slug.split("_") if part)
00335:     json_path = patch_dir / f"{slug}_project_awareness.json"
00336:     md_path = patch_dir / f"{slug}_project_awareness.md"
00337:     json_path.write_text(json.dumps(awareness, indent=2, ensure_ascii=False), encoding="utf-8")
00338:     lines = [
00339:         "# Spaziotempo Project Awareness\n\n",
00340:         f"Generated: `{awareness.get('generated_at')}`\n\n",
00341:         f"Track: `{awareness.get('track_stem')}`\n\n",
00342:         "## Pipeline State\n",
00343:     ]
00344:     for key, value in (awareness.get("pipeline_state") or {}).items():
00345:         lines.append(f"- `{key}`: `{value}`\n")
00346:     lines.append("\n## Director Rules\n")
00347:     for rule in awareness.get("director_rules", []):
00348:         lines.append(f"- {rule}\n")
00349:     lines.append("\n## Primary Assets\n")
00350:     for asset in (awareness.get("asset_awareness") or {}).get("primary_assets", []):
00351:         lines.append(f"- `{asset.get('role')}`: `{asset.get('path')}`\n")
00352:     md_path.write_text("".join(lines), encoding="utf-8")
00353:     return {"json": str(json_path), "md": str(md_path)}
```
