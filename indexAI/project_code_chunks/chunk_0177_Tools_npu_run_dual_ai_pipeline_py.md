# Project Code Chunk 177/212

- File: `Tools/npu/run_dual_ai_pipeline.py`
- Part: `2`
- Lines: `246-508`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `from datetime import datetime`, `from typing import Any`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_ai_service_packet import build_ai_service_packet, slugify`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 53; `read_json(path)` line 57; `write_json(path, data)` line 63; `read_optional_json(path)` line 68; `update_track_paths(track_stem, analysis_ai_context)` line 81; `apply_default_input_paths(args)` line 93; `validate_input_files(args)` line 106; `looks_degraded_text(text)` line 126; `deterministic_technical_notes(music_context, project_manifest, reason)` line 142; `run_npu_technical_pass(args)` line 191; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 235; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 317; `build_implementation_prompt(plan, npu_notes, include_manual, gpu_packet, scene_brief, asset_inventory)` line 379; `build_implementation_retry_prompt(plan, invalid_draft, validation)` line 491; `safe_parse_json(text, fallback_key)` line 580; `extract_python_script(text)` line 588; `draft_from_raw_python_script(text, model, reason)` line 608; `get_indexed_project_files()` line 659; `validate_implementation_draft(draft)` line 664; `generated_scene_script_relpath()` line 761; `generated_scene_script_abspath()` line 765; `deterministic_scene_builder_script(track_stem, analysis_json, music_context_json, ai_context_json, blender_keyframes_json, asset_inventory_json, scene_brief)` line 769; `deterministic_support_files(track_stem, scene_brief)` line 1152; `build_fallback_implementation_draft(reason, model, args, scene_brief, asset_inventory)` line 1205; `normalize_implementation_draft(draft, model, args, scene_brief, asset_inventory)` line 1292; `generate_implementation_draft_with_retry(manager, model_name, implementation_prompt, plan, max_new_tokens, args, scene_brief, asset_inventory)` line 1313; `write_brief(plan, creative, technical, npu_notes)` line 1376; `write_implementation_draft(draft)` line 1399; `main()` line 1453
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `DEFAULT_TRACK_STEM`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`, `ALLOWED_NEW_PREFIXES`, `PREFERRED_IMPLEMENTATION_FILES`

## Content
```py
00246:         "segments": [
00247:             {
00248:                 "index": segment.get("index"),
00249:                 "start_sec": segment.get("start_sec"),
00250:                 "end_sec": segment.get("end_sec"),
00251:                 "dominant_band": segment.get("dominant_band"),
00252:                 "intensity": segment.get("intensity"),
00253:                 "intensity_score": segment.get("intensity_score"),
00254:                 "controls": segment.get("controls"),
00255:                 "top_events": segment.get("top_events", [])[:6],
00256:             }
00257:             for segment in music_context.get("segments", [])
00258:         ],
00259:         "npu_technical_notes": npu_notes[:18000],
00260:         "primary_project_index": project_index[:14000],
00261:     }
00262:     payload = json.dumps(compact, indent=2, ensure_ascii=False)
00263:     return f"""
00264: Sei il generatore creativo locale per una scena Blender audio-reactive.
00265: 
00266: Hai un contesto musicale compatto, scene JSON esistenti e note tecniche NPU.
00267: Devi proporre una scena piu ricca SENZA cambiare direttamente codice Blender.
00268: Il codice reale del progetto e' la fonte primaria: rispetta file, moduli e funzioni esistenti.
00269: Il JSON full frame per Blender deve restare completo e invariato.
00270: 
00271: Rispondi SOLO con JSON valido.
00272: 
00273: Schema richiesto:
00274: {{
00275:   "creative_intent": "...",
00276:   "visual_language": {{
00277:     "background": "...",
00278:     "hero": "...",
00279:     "fog": "...",
00280:     "materials": "...",
00281:     "lights": "...",
00282:     "physics": "..."
00283:   }},
00284:   "scene_layers": [
00285:     {{
00286:       "layer": "Hero",
00287:       "objects": ["..."],
00288:       "audio_drivers": ["low", "mid", "high", "onset", "beat"],
00289:       "implementation_hint": "..."
00290:     }}
00291:   ],
00292:   "segment_variations": [
00293:     {{
00294:       "segment": 1,
00295:       "time_range": "0.0-16.0",
00296:       "variation": "...",
00297:       "material_modulation": "...",
00298:       "fog_modulation": "...",
00299:       "light_modulation": "...",
00300:       "camera_modulation": "..."
00301:     }}
00302:   ],
00303:   "render_safety": {{
00304:     "heavy_features_to_avoid": ["..."],
00305:     "fast_preview_strategy": "...",
00306:     "final_strategy": "..."
00307:   }},
00308:   "json_outputs_to_create": ["..."],
00309:   "do_not_touch": ["full analysis frame JSON", "..."]
00310: }}
00311: 
00312: CONTESTO:
00313: {payload}
00314: """.strip()
00315: 
00316: 
00317: def build_merge_prompt(
00318:     music_context: dict[str, Any],
00319:     npu_notes: str,
00320:     creative: dict[str, Any],
00321:     technical: dict[str, Any],
00322: ) -> str:
00323:     payload = {
00324:         "music_summary": music_context.get("analysis_summary"),
00325:         "ai_operating_contract": {
00326:             "memory_first": True,
00327:             "use_director_brief": True,
00328:             "use_assets_by_role": True,
00329:             "full_keyframes_json_is_authoritative": True,
00330:         },
00331:         "npu_technical_notes": npu_notes[:14000],
00332:         "primary_project_index": read_text(PROJECT_INDEX_MD)[:12000],
00333:         "ollama_creative": creative,
00334:         "ollama_technical": technical,
00335:     }
00336:     return f"""
00337: Sei l'orchestratore finale NPU+Ollama per Blender.
00338: 
00339: Devi fondere note tecniche e proposte creative in un piano applicabile, ma NON applicare niente.
00340: Il piano deve essere prudente, modulare e compatibile con hotpatch successivi.
00341: 
00342: Rispondi SOLO con JSON valido.
00343: 
00344: Schema:
00345: {{
00346:   "pipeline_policy": {{
00347:     "use_full_blender_keyframes_json": true,
00348:     "ai_context_is_analysis_only": true,
00349:     "ollama_model_switch_policy": "unload previous model before loading next"
00350:   }},
00351:   "recommended_scene_plan": {{
00352:     "summary": "...",
00353:     "priority_changes": ["..."],
00354:     "defer_changes": ["..."]
00355:   }},
00356:   "file_plan": {{
00357:     "read_only": ["..."],
00358:     "hotpatch_candidates": ["..."],
00359:     "json_outputs": ["..."],
00360:     "must_use_existing_files": true
00361:   }},
00362:   "audio_mapping_plan": {{
00363:     "hero_mesh": "...",
00364:     "materials": "...",
00365:     "fog": "...",
00366:     "lights": "...",
00367:     "physics": "...",
00368:     "camera": "..."
00369:   }},
00370:   "safety_checks": ["..."],
00371:   "next_commands": ["..."]
00372: }}
00373: 
00374: DATI:
00375: {json.dumps(payload, indent=2, ensure_ascii=False)}
00376: """.strip()
00377: 
00378: 
00379: def build_implementation_prompt(
00380:     plan: dict[str, Any],
00381:     npu_notes: str,
00382:     include_manual: bool,
00383:     gpu_packet: dict[str, Any] | None = None,
00384:     scene_brief: dict[str, Any] | None = None,
00385:     asset_inventory: dict[str, Any] | None = None,
00386: ) -> str:
00387:     manual_index = read_text(TOOLS_DIR / "npu_blender_manual_index.md")[:12000] if include_manual else ""
00388:     project_index = read_text(PROJECT_INDEX_MD)[:14000]
00389:     project_manifest = read_text(PROJECT_MANIFEST_JSON)[:10000]
00390:     guide = read_text(ROOT / "Scripting" / "v61b" / "SCENE_TUNING_GUIDE.md")[:10000]
00391:     project_structure = read_text(ROOT / "Scripting" / "v61b" / "PROJECT_STRUCTURE.md")[:8000]
00392:     previous_scene_script = read_text(generated_scene_script_abspath())[:18000]
00393:     slug = packet_slugify(TRACK_STEM)
00394: 
00395:     payload = {
00396:         "ai_operating_contract": {
00397:             "role": "GPU code interpreter / Blender Python writer",
00398:             "memory_first": "Apply scene_director_brief and conversation_memory before older plan defaults.",
00399:             "chunk_protocol": "Use gpu_task_packet as compact router; use referenced JSON files at runtime for exact frame data.",
00400:             "full_keyframe_rule": "Generated script must load BLENDER_KEYFRAMES_JSON and iterate keyframes['frames'] without reducing it.",
00401:             "asset_rule": "Use asset_inventory roles. primary_ball_asset is the real ball asset.",
00402:             "failure_rule": "If the model cannot produce valid code, deterministic fallback will be used and marked in validation.",
00403:         },
00404:         "gpu_task_packet": gpu_packet,
00405:         "dual_ai_plan": plan,
00406:         "npu_notes": npu_notes[:14000],
00407:         "primary_project_index": project_index,
00408:         "primary_project_manifest": project_manifest,
00409:         "project_structure": project_structure,
00410:         "scene_tuning_guide": guide,
00411:         "manual_index": manual_index,
00412:         "scene_director_brief": scene_brief or {},
00413:         "asset_inventory": asset_inventory or {},
00414:         "previous_generated_scene_script": previous_scene_script,
00415:     }
00416: 
00417:     return f"""
00418: Sei un code interpreter Blender Python che lavora come GPU writer.
00419: 
00420: Devi generare una BOZZA NUOVA, separata dal progetto vivo.
00421: Non devi modificare file esistenti del progetto.
00422: I file esistenti sono SOLO reference/style/source-map.
00423: Devi mantenere stile, nomi e logica del progetto guardando primary_project_index, ma scrivere solo in `indexAI/scene_scripts/`.
00424: Il codice candidato non deve essere vuoto: deve contenere Python Blender eseguibile come script standalone per creare una nuova scena da JSON.
00425: Lo script deve leggere i JSON di contesto, creare materiali, oggetti, modifier/deformazioni, keyframe audio-reactive e camera/luci.
00426: Per l'animazione Blender usa il file full `analysis_blender_keyframes.json` e tutti gli elementi `frames`; i segmenti compatti servono solo per composizione e macro-scelte.
00427: Se l'utente chiede modifiche nel scene_director_brief, applicale come revisione dello script precedente.
00428: Se il brief nomina asset gia presenti, usa asset_inventory. `primary_ball_asset` e' la ball reale del progetto, non sostituirla con una sfera generica salvo fallback.
00429: Se lo script diventa complesso, puoi dividerlo in piu file sotto `indexAI/scene_scripts/{slug}_scene_bundle/` usando `support_files`.
00430: Non accettare placeholder, TODO, `pass`, scene minime con solo camera/luce/piano, o spiegazioni al posto del codice.
00431: Non ridurre il JSON frame-by-frame del brano.
00432: Non inventare API se nel manuale/indice non sono presenti; se non sei sicuro, scrivi note.
00433: Se scene_director_brief contiene "due oggetti centrali" o "ball", lo script deve importare/istanziare `primary_ball_asset` due volte, con animazioni in controfase e mapping audio invertito.
00434: 
00435: Rispondi SOLO con JSON valido.
00436: Il primo carattere della risposta deve essere {{ e l'ultimo deve essere }}.
00437: Non usare Markdown, non usare blocchi ```json, non scrivere documentazione.
00438: 
00439: Schema obbligatorio:
00440: {{
00441:   "implementation_kind": "new_blender_scene_script_from_json",
00442:   "safety": {{
00443:     "does_not_modify_full_analysis_json": true,
00444:     "does_not_modify_project_source_files": true,
00445:     "requires_manual_review": true,
00446:       "needs_blender_run": true
00447:   }},
00448:   "reference_files": [
00449:     {{
00450:       "file": "Scripting/v61b/materials.py",
00451:       "exists_in_project_index": true,
00452:       "reason": "style/source reference only"
00453:     }}
00454:   ],
00455:   "proposed_files": [
00456:     {{
00457:       "file": "indexAI/scene_scripts/{slug}_scene_builder_candidate.py",
00458:       "kind": "standalone_blender_scene_builder",
00459:       "why": "new scene script, not a patch to the existing project"
00460:     }}
00461:   ],
00462:   "implementation_plan": [
00463:     {{
00464:       "reference_file": "Scripting/v61b/materials.py",
00465:       "new_file": "indexAI/scene_scripts/{slug}_scene_builder_candidate.py",
00466:       "change": "...",
00467:       "why": "...",
00468:       "risk": "low|medium|high",
00469:       "manual_check": "..."
00470:     }}
00471:   ],
00472:   "new_files_allowed": ["indexAI/scene_scripts/...", "indexAI/patch_library/..."],
00473:   "scene_script": "codice Python Blender completo e non vuoto",
00474:   "support_files": [
00475:     {{
00476:       "file": "indexAI/scene_scripts/{slug}_scene_bundle/README.md",
00477:       "kind": "notes|module|manifest|brief_snapshot",
00478:       "content": "contenuto completo del file"
00479:     }}
00480:   ],
00481:   "notes": ["..."],
00482:   "files_to_review_before_applying": ["..."],
00483:   "expected_panel_or_operator": "..."
00484: }}
00485: 
00486: CONTESTO:
00487: {json.dumps(payload, indent=2, ensure_ascii=False)}
00488: """.strip()
00489: 
00490: 
00491: def build_implementation_retry_prompt(
00492:     plan: dict[str, Any],
00493:     invalid_draft: dict[str, Any],
00494:     validation: dict[str, Any],
00495: ) -> str:
00496:     del invalid_draft  # The retry only needs the validation errors, not the full invalid text.
00497: 
00498:     manifest = read_json(PROJECT_MANIFEST_JSON) if PROJECT_MANIFEST_JSON.exists() else {}
00499:     indexed_files = sorted(
00500:         item.get("file")
00501:         for item in manifest.get("files", [])
00502:         if item.get("file")
00503:     )
00504:     preferred_files = [file_name for file_name in indexed_files if file_name in PREFERRED_IMPLEMENTATION_FILES]
00505: 
00506:     payload = {
00507:         "dual_ai_plan": plan,
00508:         "preferred_existing_files": preferred_files,
```
