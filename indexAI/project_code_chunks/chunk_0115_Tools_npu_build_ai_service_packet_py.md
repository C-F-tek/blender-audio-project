# Project Code Chunk 115/212

- File: `Tools/npu/build_ai_service_packet.py`
- Part: `2`
- Lines: `236-355`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `argparse`, `hashlib`, `json`, `re`, `from typing import Any`
- Functions: `slugify(value, max_len)` line 20; `read_json(path)` line 25; `sha256_file(path)` line 33; `safe_float(value, default)` line 43; `top_project_files(manifest)` line 50; `role_for_file(file_name)` line 83; `compact_segments(music_context, limit)` line 102; `build_ai_service_packet(track_stem, analysis_path, track_summary_path, music_context_path, analysis_ai_context_path, blender_keyframes_path, dual_plan_path, npu_notes, npu_status, scene_brief, asset_inventory)` line 138; `format_capsule_md(capsule)` line 305; `main()` line 325
- Assignments: `ROOT`, `OUTPUT_DIR`, `INDEX_AI_DIR`, `PATCH_LIBRARY_DIR`, `SCENE_SCRIPTS_DIR`, `PROJECT_MANIFEST_JSON`

## Content
```py
00236:             "do_not_modify_project_source": True,
00237:             "propose_new_files_only": [
00238:                 "indexAI/scene_scripts/",
00239:                 "indexAI/patch_library/",
00240:             ],
00241:             "match_existing_style": True,
00242:             "preserve_current_scene_logic": True,
00243:             "all_existing_files_are_reference_only": True,
00244:         },
00245:         "task_contract": {
00246:             "gpu_director": "create scene plan using capsule, manual, and project style",
00247:             "gpu_code_interpreter": "write review-only standalone Blender Python scene builder in allowed output path",
00248:             "validator": "reject empty scripts, markdown answers, existing-source modifications, missing reference files",
00249:             "chunk_protocol": [
00250:                 "Treat capsule refs as authoritative file handles.",
00251:                 "Ask for or load exact source chunks only when needed.",
00252:                 "Never replace full keyframes with compact segments; compact segments are only semantic guidance.",
00253:                 "Return structured JSON for machine use, not prose, during plan/script phases.",
00254:             ],
00255:         },
00256:         "npu_service": {
00257:             "status": npu_status,
00258:             "notes_digest": npu_notes[:2400],
00259:         },
00260:         "plan_digest": {
00261:             "has_plan": bool(dual_plan),
00262:             "summary": (dual_plan.get("final_plan") or dual_plan).get("recommended_scene_plan", {}),
00263:         },
00264:     }
00265: 
00266:     gpu_packet = {
00267:         "format": "SPAZIOTEMPO_GPU_TASK_PACKET_V1",
00268:         "generated_at": capsule["generated_at"],
00269:         "track_stem": track_stem,
00270:         "capsule": capsule,
00271:         "required_output_schema": {
00272:             "implementation_kind": "new_blender_scene_script_from_json",
00273:             "reference_files": [{"file": "existing project file", "reason": "style/source reference only"}],
00274:             "proposed_files": [{"file": f"indexAI/scene_scripts/{slug}_scene_builder_candidate.py", "kind": "standalone_blender_scene_builder"}],
00275:             "scene_script": "non-empty Python code",
00276:             "notes": ["short implementation notes"],
00277:         },
00278:     }
00279: 
00280:     capsule_json = PATCH_LIBRARY_DIR / f"{slug}_npu_service_capsule.json"
00281:     packet_json = PATCH_LIBRARY_DIR / f"{slug}_gpu_task_packet.json"
00282:     output_packet_json = OUTPUT_DIR / f"{track_stem}_gpu_task_packet.json"
00283:     capsule_md = PATCH_LIBRARY_DIR / f"{slug}_npu_service_capsule.md"
00284: 
00285:     SCENE_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
00286:     (SCENE_SCRIPTS_DIR / "README.md").write_text(
00287:         "# AI Scene Scripts\n\nStandalone Blender scene-builder drafts generated from intermediate JSON files.\n",
00288:         encoding="utf-8",
00289:     )
00290:     capsule_json.write_text(json.dumps(capsule, indent=2, ensure_ascii=False), encoding="utf-8")
00291:     packet_json.write_text(json.dumps(gpu_packet, indent=2, ensure_ascii=False), encoding="utf-8")
00292:     output_packet_json.write_text(json.dumps(gpu_packet, indent=2, ensure_ascii=False), encoding="utf-8")
00293:     capsule_md.write_text(format_capsule_md(capsule), encoding="utf-8")
00294: 
00295:     return {
00296:         "capsule": capsule,
00297:         "gpu_packet": gpu_packet,
00298:         "capsule_json": str(capsule_json),
00299:         "gpu_packet_json": str(packet_json),
00300:         "output_gpu_packet_json": str(output_packet_json),
00301:         "capsule_md": str(capsule_md),
00302:     }
00303: 
00304: 
00305: def format_capsule_md(capsule: dict[str, Any]) -> str:
00306:     lines = [
00307:         "# Spaziotempo NPU Service Capsule\n\n",
00308:         f"Generated: `{capsule['generated_at']}`\n\n",
00309:         "## Routing\n",
00310:         json.dumps(capsule["routing_policy"], indent=2, ensure_ascii=False),
00311:         "\n\n## Track\n",
00312:         json.dumps(capsule["track"], indent=2, ensure_ascii=False),
00313:         "\n\n## Project Files\n",
00314:     ]
00315:     for item in capsule["project_language"]["files"]:
00316:         lines.append(f"- `{item['id']}` `{item['file']}`: {item['role']}\n")
00317:     lines.append("\n## Audio Segments\n")
00318:     for segment in capsule["audio_language"]["segments"]:
00319:         lines.append(
00320:             f"- `{segment['id']}` t={segment['t']} b={segment['b']} i={segment['i']} ctl={segment['ctl']}\n"
00321:         )
00322:     return "".join(lines)
00323: 
00324: 
00325: def main() -> None:
00326:     parser = argparse.ArgumentParser(description="Build compact NPU service capsule and GPU task packet.")
00327:     parser.add_argument("--track-stem", required=True)
00328:     parser.add_argument("--analysis", required=True)
00329:     parser.add_argument("--track-summary", required=True)
00330:     parser.add_argument("--music-context", required=True)
00331:     parser.add_argument("--analysis-ai-context", required=True)
00332:     parser.add_argument("--blender-keyframes-json", required=True)
00333:     parser.add_argument("--dual-plan", default="")
00334:     parser.add_argument("--npu-notes", default="")
00335:     parser.add_argument("--npu-status", default="service_packet")
00336:     args = parser.parse_args()
00337: 
00338:     result = build_ai_service_packet(
00339:         track_stem=args.track_stem,
00340:         analysis_path=Path(args.analysis),
00341:         track_summary_path=Path(args.track_summary),
00342:         music_context_path=Path(args.music_context),
00343:         analysis_ai_context_path=Path(args.analysis_ai_context),
00344:         blender_keyframes_path=Path(args.blender_keyframes_json),
00345:         dual_plan_path=Path(args.dual_plan) if args.dual_plan else None,
00346:         npu_notes=Path(args.npu_notes).read_text(encoding="utf-8", errors="replace") if args.npu_notes else "",
00347:         npu_status=args.npu_status,
00348:     )
00349:     print(f"[OK] Wrote: {result['capsule_json']}")
00350:     print(f"[OK] Wrote: {result['gpu_packet_json']}")
00351:     print(f"[OK] Wrote: {result['output_gpu_packet_json']}")
00352: 
00353: 
00354: if __name__ == "__main__":
00355:     main()
```
