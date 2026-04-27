# Project Code Chunk 174/212

- File: `Tools/npu/run_dual_ai_pipeline - Copia.py`
- Part: `2`
- Lines: `265-506`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `sys`, `from datetime import datetime`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 38; `read_json(path)` line 42; `write_json(path, data)` line 47; `validate_input_files(args)` line 52; `looks_degraded_text(text)` line 72; `deterministic_technical_notes(music_context, project_manifest, reason)` line 85; `run_npu_technical_pass(args)` line 134; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 178; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 254; `build_implementation_prompt(plan, npu_notes, include_manual)` line 305; `safe_parse_json(text, fallback_key)` line 373; `write_brief(plan, creative, technical, npu_notes)` line 380; `validate_implementation_draft(draft)` line 403; `write_implementation_draft(draft)` line 450; `main()` line 478
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`

## Content
```py
00265: Devi fondere note tecniche e proposte creative in un piano applicabile, ma NON applicare niente.
00266: Il piano deve essere prudente, modulare e compatibile con hotpatch successivi.
00267: 
00268: Rispondi SOLO con JSON valido.
00269: 
00270: Schema:
00271: {{
00272:   "pipeline_policy": {{
00273:     "use_full_blender_keyframes_json": true,
00274:     "ai_context_is_analysis_only": true,
00275:     "ollama_model_switch_policy": "unload previous model before loading next"
00276:   }},
00277:   "recommended_scene_plan": {{
00278:     "summary": "...",
00279:     "priority_changes": ["..."],
00280:     "defer_changes": ["..."]
00281:   }},
00282:   "file_plan": {{
00283:     "read_only": ["..."],
00284:     "hotpatch_candidates": ["..."],
00285:     "json_outputs": ["..."],
00286:     "must_use_existing_files": true
00287:   }},
00288:   "audio_mapping_plan": {{
00289:     "hero_mesh": "...",
00290:     "materials": "...",
00291:     "fog": "...",
00292:     "lights": "...",
00293:     "physics": "...",
00294:     "camera": "..."
00295:   }},
00296:   "safety_checks": ["..."],
00297:   "next_commands": ["..."]
00298: }}
00299: 
00300: DATI:
00301: {json.dumps(payload, indent=2, ensure_ascii=False)}
00302: """.strip()
00303: 
00304: 
00305: def build_implementation_prompt(plan: dict, npu_notes: str, include_manual: bool) -> str:
00306:     manual_index = read_text(TOOLS_DIR / "npu_blender_manual_index.md")[:12000] if include_manual else ""
00307:     project_index = read_text(PROJECT_INDEX_MD)[:22000]
00308:     project_manifest = read_text(PROJECT_MANIFEST_JSON)[:18000]
00309:     legacy_code_index = read_text(TOOLS_DIR / "npu_code_index.md")[:8000]
00310:     guide = read_text(ROOT / "Scripting" / "v61b" / "SCENE_TUNING_GUIDE.md")[:10000]
00311:     project_structure = read_text(ROOT / "Scripting" / "v61b" / "PROJECT_STRUCTURE.md")[:8000]
00312: 
00313:     payload = {
00314:         "dual_ai_plan": plan,
00315:         "npu_notes": npu_notes[:14000],
00316:         "primary_project_index": project_index,
00317:         "primary_project_manifest": project_manifest,
00318:         "legacy_code_index": legacy_code_index,
00319:         "project_structure": project_structure,
00320:         "scene_tuning_guide": guide,
00321:         "manual_index": manual_index,
00322:     }
00323: 
00324:     return f"""
00325: Sei un agente implementatore Blender Python.
00326: 
00327: Devi generare una BOZZA di patch plan per il progetto esistente.
00328: Non devi riscrivere tutto in uno script monolitico.
00329: Ogni modifica deve riferirsi a un file gia presente nel primary_project_index, salvo nuovi file hotpatch o indexAI/patch_library.
00330: La bozza script candidata e' opzionale: usala solo se e' davvero un hotpatch separato e coerente.
00331: Non ridurre il JSON frame-by-frame del brano.
00332: Non inventare API se nel manuale/indice non sono presenti; se non sei sicuro, scrivi note.
00333: 
00334: Rispondi SOLO con JSON valido:
00335: {{
00336:   "implementation_kind": "existing_project_patch_plan",
00337:   "safety": {{
00338:     "does_not_modify_full_analysis_json": true,
00339:     "requires_manual_review": true,
00340:     "needs_blender_run": true
00341:   }},
00342:   "target_files": [
00343:     {{
00344:       "file": "Scripting/v61b/materials.py",
00345:       "exists_in_project_index": true,
00346:       "reason": "...",
00347:       "hot_update_possible": true,
00348:       "requires_full_reload": false
00349:     }}
00350:   ],
00351:   "patch_plan": [
00352:     {{
00353:       "file": "Scripting/v61b/materials.py",
00354:       "function_or_section": "...",
00355:       "change": "...",
00356:       "why": "...",
00357:       "risk": "low|medium|high",
00358:       "test_or_check": "..."
00359:     }}
00360:   ],
00361:   "new_files_allowed": ["Scripting/v61b/hotpatch/...", "indexAI/patch_library/..."],
00362:   "hotpatch_candidate_script": "codice python opzionale, oppure stringa vuota",
00363:   "notes": ["..."],
00364:   "files_to_review_before_applying": ["..."],
00365:   "expected_panel_or_operator": "..."
00366: }}
00367: 
00368: CONTESTO:
00369: {json.dumps(payload, indent=2, ensure_ascii=False)}
00370: """.strip()
00371: 
00372: 
00373: def safe_parse_json(text: str, fallback_key: str) -> dict:
00374:     try:
00375:         return parse_json_response(text)
00376:     except Exception:
00377:         return {fallback_key: text, "parse_error": True}
00378: 
00379: 
00380: def write_brief(plan: dict, creative: dict, technical: dict, npu_notes: str) -> None:
00381:     lines = [
00382:         "# Dual AI Blender Agent Brief\n\n",
00383:         f"Generated: `{datetime.now().isoformat(timespec='seconds')}`\n\n",
00384:         "## Policy\n",
00385:         "- Full Blender keyframe JSON remains untouched.\n",
00386:         "- AI compact context is analysis only.\n",
00387:         "- Ollama model switch unloads the previous model before loading the next.\n\n",
00388:         "## Recommended Plan\n",
00389:         json.dumps(plan.get("recommended_scene_plan", plan), indent=2, ensure_ascii=False),
00390:         "\n\n## Audio Mapping\n",
00391:         json.dumps(plan.get("audio_mapping_plan", {}), indent=2, ensure_ascii=False),
00392:         "\n\n## Creative Source\n",
00393:         json.dumps(creative, indent=2, ensure_ascii=False)[:12000],
00394:         "\n\n## Technical Source\n",
00395:         json.dumps(technical, indent=2, ensure_ascii=False)[:12000],
00396:         "\n\n## NPU Notes\n",
00397:         npu_notes[:12000],
00398:         "\n",
00399:     ]
00400:     DUAL_BRIEF_MD.write_text("".join(lines), encoding="utf-8")
00401: 
00402: 
00403: def validate_implementation_draft(draft: dict) -> dict:
00404:     allowed_new_prefixes = ("Scripting/v61b/hotpatch/", "indexAI/patch_library/")
00405:     manifest = read_json(PROJECT_MANIFEST_JSON) if PROJECT_MANIFEST_JSON.exists() else {}
00406:     indexed_files = {item.get("file") for item in manifest.get("files", []) if item.get("file")}
00407: 
00408:     issues: list[str] = []
00409:     target_files = draft.get("target_files") or []
00410:     patch_plan = draft.get("patch_plan") or []
00411: 
00412:     if draft.get("implementation_kind") != "existing_project_patch_plan":
00413:         issues.append("implementation_kind should be existing_project_patch_plan.")
00414: 
00415:     if not target_files and not patch_plan:
00416:         issues.append("No target_files or patch_plan entries were provided.")
00417: 
00418:     for item in target_files:
00419:         file_name = str(item.get("file") or "").replace("\\", "/")
00420:         if not file_name:
00421:             issues.append("A target_files entry has no file.")
00422:             continue
00423:         is_existing = file_name in indexed_files
00424:         is_allowed_new = file_name.startswith(allowed_new_prefixes)
00425:         if not is_existing and not is_allowed_new:
00426:             issues.append(f"Target file is not in project index and not an allowed new file: {file_name}")
00427: 
00428:     for item in patch_plan:
00429:         file_name = str(item.get("file") or "").replace("\\", "/")
00430:         if not file_name:
00431:             issues.append("A patch_plan entry has no file.")
00432:             continue
00433:         is_existing = file_name in indexed_files
00434:         is_allowed_new = file_name.startswith(allowed_new_prefixes)
00435:         if not is_existing and not is_allowed_new:
00436:             issues.append(f"Patch target is not in project index and not an allowed new file: {file_name}")
00437: 
00438:     script = draft.get("hotpatch_candidate_script", draft.get("script", ""))
00439:     if script and "analysis_blender_keyframes" in script and "write" in script.lower():
00440:         issues.append("Candidate script appears to write keyframe analysis data; review required.")
00441: 
00442:     return {
00443:         "ok": not issues,
00444:         "issues": issues,
00445:         "indexed_file_count": len(indexed_files),
00446:         "allowed_new_prefixes": list(allowed_new_prefixes),
00447:     }
00448: 
00449: 
00450: def write_implementation_draft(draft: dict) -> None:
00451:     draft["validation"] = validate_implementation_draft(draft)
00452:     write_json(IMPLEMENTATION_DRAFT_JSON, draft)
00453:     script = draft.get("hotpatch_candidate_script", draft.get("script", ""))
00454:     if not script:
00455:         script = (
00456:             "# AI implementation draft is a patch plan, not a runnable script.\n"
00457:             "# Review the JSON draft for target_files, patch_plan, validation and notes.\n"
00458:         )
00459:     IMPLEMENTATION_SCRIPT.write_text(script.rstrip() + "\n", encoding="utf-8")
00460:     notes = [
00461:         "# Generated Implementation Notes\n\n",
00462:         "This file is an AI draft. Review before loading in Blender.\n\n",
00463:         "## Validation\n",
00464:         json.dumps(draft.get("validation", {}), indent=2, ensure_ascii=False),
00465:         "\n\n",
00466:         "## Safety\n",
00467:         json.dumps(draft.get("safety", {}), indent=2, ensure_ascii=False),
00468:         "\n\n## Notes\n",
00469:     ]
00470:     for note in draft.get("notes", []):
00471:         notes.append(f"- {note}\n")
00472:     notes.append("\n## Files To Review\n")
00473:     for path in draft.get("files_to_review_before_applying", []):
00474:         notes.append(f"- `{path}`\n")
00475:     IMPLEMENTATION_NOTES.write_text("".join(notes), encoding="utf-8")
00476: 
00477: 
00478: def main() -> None:
00479:     global TRACK_STEM
00480:     global MUSIC_AI_CONTEXT, DUAL_PLAN_JSON, OLLAMA_INSIGHTS_JSON
00481:     global IMPLEMENTATION_DRAFT_JSON
00482: 
00483:     parser = argparse.ArgumentParser(description="Build code/music contexts, run NPU technical pass and Ollama creative passes.")
00484:     parser.add_argument("--phase", choices=["plan", "implementation", "full"], default="plan")
00485:     parser.add_argument("--track-stem", default=TRACK_STEM)
00486:     parser.add_argument("--analysis", default=str(OUTPUT_DIR / f"{TRACK_STEM}_analysis.json"))
00487:     parser.add_argument("--track-summary", default=str(OUTPUT_DIR / f"{TRACK_STEM}_track_summary.json"))
00488:     parser.add_argument("--compact-json", default=str(OUTPUT_DIR / f"{TRACK_STEM}_music_context.json"))
00489:     parser.add_argument("--analysis-ai-context", default=str(MUSIC_AI_CONTEXT))
00490:     parser.add_argument("--blender-keyframes-json", default=str(OUTPUT_DIR / f"{TRACK_STEM}_analysis_blender_keyframes.json"))
00491:     parser.add_argument("--skip-npu", action="store_true")
00492:     parser.add_argument("--skip-ollama", action="store_true")
00493:     parser.add_argument("--include-manual", action="store_true")
00494:     parser.add_argument("--creative-model", default="gpt-oss:20b")
00495:     parser.add_argument("--technical-model", default="qwen2.5-coder:14b")
00496:     parser.add_argument("--ollama-base-url", default=None)
00497:     parser.add_argument("--npu-python", default=str(DEFAULT_NPU_PYTHON))
00498:     parser.add_argument("--npu-model-dir", default=str(DEFAULT_MODEL_DIR))
00499:     parser.add_argument("--npu-chunk-tokens", type=int, default=520)
00500:     parser.add_argument("--npu-reduce-tokens", type=int, default=650)
00501:     parser.add_argument("--npu-final-tokens", type=int, default=900)
00502:     parser.add_argument("--max-new-tokens", type=int, default=1800)
00503:     parser.add_argument("--force-npu", action="store_true", help="Re-run NPU notes even when reusable notes exist.")
00504:     args = parser.parse_args()
00505: 
00506:     TRACK_STEM = args.track_stem
```
