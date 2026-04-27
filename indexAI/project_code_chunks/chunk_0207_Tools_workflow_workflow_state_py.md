# Project Code Chunk 207/212

- File: `Tools/workflow/workflow_state.py`
- Part: `2`
- Lines: `266-573`

## Symbol Map
- Imports: `from __future__ import annotations`, `from dataclasses import dataclass, asdict`, `from datetime import datetime`, `from pathlib import Path`, `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `time`
- Classes: `OperationResult` line 45; `WorkflowSession` line 125 methods: default, save
- Functions: `now_iso()` line 40; `write_json(path, payload)` line 59; `append_event(operation, event, payload)` line 64; `save_operation_result(result)` line 76; `slugify(value)` line 82; `track_stem_from_wav(wav_path)` line 89; `build_artifacts(wav_path)` line 93; `load_session(create)` line 159; `set_current_wav(wav_path)` line 191; `reset_to_default_wav()` line 218; `set_debug_enabled(enabled)` line 239; `available_ollama_models()` line 248; `set_ai_models()` line 266; `python_executable()` line 297; `audio_python_executable()` line 313; `run_command(command, operation, check, echo, debug, print_output, metadata, log)` line 346; `finish_session_operation(session, operation)` line 425; `path_within(path, parent)` line 431; `is_safe_intermediate_target(path)` line 439; `cleanup_intermediate_targets(session, include_all_tracks, include_logs)` line 450; `cleanup_render_frame_targets(session)` line 565; `delete_target_set(operation, targets, session)` line 582; `human_bytes(size)` line 632; `scan_path_stats(path)` line 641; `collect_matching_files(root, patterns)` line 683; `file_set_stats(name, paths)` line 692; `build_project_storage_stats(session)` line 714; `format_project_storage_stats(stats)` line 795; `cleanup_intermediates(session, include_all_tracks, include_logs)` line 841; `cleanup_render_frames(session)` line 854; `operation_status(session)` line 859; `run_analyze_wav(session, fps, skip_music_context)` line 877; `run_track_summary(session)` line 894; `run_music_context(session, include_ollama, ollama_model)` line 912; `run_code_context(session)` line 934; `run_project_ai_index(session, force)` line 941; `run_asset_inventory(session)` line 950; `run_scene_director_brief(session)` line 968; `run_manual_index(session, limit_files)` line 1001; `ensure_manual_library(session)` line 1011; `artifact_missing(session, key)` line 1017; `ensure_ai_prerequisites(session, phase, include_manual)` line 1022; `run_dual_ai(session, phase, include_manual, skip_npu, skip_ollama, creative_model, technical_model, max_new_tokens)` line 1053; `run_full_audio_prepare(session)` line 1123
- Assignments: `ROOT`, `PROJECT_DIR`, `AUDIO_DIR`, `RENDERS_DIR`, `OUTPUT_DIR`, `TOOLS_DIR`, `NPU_DIR`, `INDEX_AI_DIR`, `SESSION_PATH`, `LOG_DIR`, `EVENT_LOG_PATH`, `LAST_RESULT_PATH`, `DEFAULT_WAV`, `DEFAULT_TRACK_STEM`, `DEFAULT_RENDER_STEM`, `DEFAULT_FRAME_PREFIX`, `NPU_PYTHON`, `AUDIO_PYTHON`, `DEFAULT_CREATIVE_MODEL`, `DEFAULT_TECHNICAL_MODEL`, `DEFAULT_CHAT_MODEL`, `DEFAULT_SCRIPT_TOKENS`

## Content
```py
00266: def set_ai_models(
00267:     *,
00268:     creative_model: str | None = None,
00269:     technical_model: str | None = None,
00270:     chat_model: str | None = None,
00271:     script_max_tokens: int | None = None,
00272: ) -> WorkflowSession:
00273:     session = load_session()
00274:     if creative_model:
00275:         session.creative_model = creative_model
00276:     if technical_model:
00277:         session.technical_model = technical_model
00278:     if chat_model:
00279:         session.chat_model = chat_model
00280:     if script_max_tokens:
00281:         session.script_max_tokens = max(1200, int(script_max_tokens))
00282:     session.last_operation = "set_ai_models"
00283:     session.save()
00284:     append_event(
00285:         "set_ai_models",
00286:         "updated",
00287:         {
00288:             "creative_model": session.creative_model,
00289:             "technical_model": session.technical_model,
00290:             "chat_model": session.chat_model,
00291:             "script_max_tokens": session.script_max_tokens,
00292:         },
00293:     )
00294:     return session
00295: 
00296: 
00297: def python_executable() -> Path:
00298:     if NPU_PYTHON.exists():
00299:         result = run_command(
00300:             [str(NPU_PYTHON), "-c", "print('ok')"],
00301:             operation="probe_python",
00302:             check=False,
00303:             echo=False,
00304:             debug=False,
00305:             print_output=False,
00306:             log=False,
00307:         )
00308:         if result.ok:
00309:             return NPU_PYTHON
00310:     return Path(sys.executable)
00311: 
00312: 
00313: def audio_python_executable() -> Path:
00314:     if AUDIO_PYTHON.exists():
00315:         result = run_command(
00316:             [str(AUDIO_PYTHON), "-c", "import librosa, numpy, matplotlib; print('audio ok')"],
00317:             operation="probe_audio_python",
00318:             check=False,
00319:             echo=False,
00320:             debug=False,
00321:             print_output=False,
00322:             log=False,
00323:         )
00324:         if result.ok:
00325:             return AUDIO_PYTHON
00326: 
00327:     fallback = Path(sys.executable)
00328:     result = run_command(
00329:         [str(fallback), "-c", "import librosa, numpy, matplotlib; print('audio ok')"],
00330:         operation="probe_audio_python_fallback",
00331:         check=False,
00332:         echo=False,
00333:         debug=False,
00334:         print_output=False,
00335:         log=False,
00336:     )
00337:     if result.ok:
00338:         return fallback
00339: 
00340:     raise RuntimeError(
00341:         "Runtime audio non disponibile: serve un Python con librosa, numpy e matplotlib. "
00342:         f"Atteso: {AUDIO_PYTHON}"
00343:     )
00344: 
00345: 
00346: def run_command(
00347:     command: list[str],
00348:     operation: str = "command",
00349:     check: bool = True,
00350:     echo: bool = True,
00351:     debug: bool | None = None,
00352:     print_output: bool = True,
00353:     metadata: dict | None = None,
00354:     log: bool = True,
00355: ) -> OperationResult:
00356:     session_debug = load_session(create=False).debug_enabled if debug is None else debug
00357:     started_at = now_iso()
00358:     start = time.perf_counter()
00359:     cwd = str(PROJECT_DIR)
00360:     metadata = metadata or {}
00361: 
00362:     if log:
00363:         append_event(
00364:             operation,
00365:             "start",
00366:             {
00367:                 "command": command,
00368:                 "cwd": cwd,
00369:                 "metadata": metadata,
00370:                 "debug": session_debug,
00371:             },
00372:         )
00373: 
00374:     if echo:
00375:         print("\n$ " + " ".join(f'"{part}"' if " " in part else part for part in command))
00376:     if session_debug:
00377:         print(f"[DEBUG] operation={operation}")
00378:         print(f"[DEBUG] cwd={cwd}")
00379:         print(f"[DEBUG] metadata={json.dumps(metadata, ensure_ascii=False)}")
00380: 
00381:     result = subprocess.run(
00382:         command,
00383:         cwd=cwd,
00384:         text=True,
00385:         stdout=subprocess.PIPE,
00386:         stderr=subprocess.STDOUT,
00387:         check=False,
00388:     )
00389:     output = result.stdout or ""
00390:     if output and print_output:
00391:         print(output.rstrip())
00392: 
00393:     ended_at = now_iso()
00394:     op_result = OperationResult(
00395:         operation=operation,
00396:         ok=result.returncode == 0,
00397:         started_at=started_at,
00398:         ended_at=ended_at,
00399:         elapsed_sec=round(time.perf_counter() - start, 4),
00400:         command=command,
00401:         cwd=cwd,
00402:         returncode=result.returncode,
00403:         stdout_tail=output[-8000:],
00404:         metadata=metadata,
00405:     )
00406: 
00407:     if log:
00408:         save_operation_result(op_result)
00409: 
00410:     if session_debug:
00411:         print(f"[DEBUG] returncode={result.returncode}")
00412:         print(f"[DEBUG] elapsed_sec={op_result.elapsed_sec}")
00413:         print(f"[DEBUG] last_result={LAST_RESULT_PATH}")
00414:         print(f"[DEBUG] event_log={EVENT_LOG_PATH}")
00415: 
00416:     if check and result.returncode != 0:
00417:         op_result.error = f"Comando fallito con exit code {result.returncode}"
00418:         if log:
00419:             save_operation_result(op_result)
00420:         raise RuntimeError(op_result.error)
00421: 
00422:     return op_result
00423: 
00424: 
00425: def finish_session_operation(session: WorkflowSession, operation: str) -> None:
00426:     session.last_operation = operation
00427:     session.last_result_path = str(LAST_RESULT_PATH)
00428:     session.save()
00429: 
00430: 
00431: def path_within(path: Path, parent: Path) -> bool:
00432:     try:
00433:         path.resolve(strict=False).relative_to(parent.resolve(strict=False))
00434:         return True
00435:     except ValueError:
00436:         return False
00437: 
00438: 
00439: def is_safe_intermediate_target(path: Path) -> bool:
00440:     allowed = path_within(path, OUTPUT_DIR) or path_within(path, NPU_DIR) or path_within(path, INDEX_AI_DIR)
00441:     forbidden = (
00442:         path_within(path, AUDIO_DIR)
00443:         or path_within(path, RENDERS_DIR)
00444:         or path == PROJECT_DIR
00445:         or path == ROOT
00446:     )
00447:     return allowed and not forbidden
00448: 
00449: 
00450: def cleanup_intermediate_targets(session: WorkflowSession, include_all_tracks: bool = True, include_logs: bool = True) -> dict:
00451:     file_targets: set[Path] = set()
00452:     dir_targets: set[Path] = set()
00453: 
00454:     artifact_keys = [
00455:         "analysis_json",
00456:         "analysis_plot_png",
00457:         "blender_keyframes_json",
00458:         "track_summary_json",
00459:         "music_context_json",
00460:         "analysis_ai_context_json",
00461:         "dual_ai_plan_json",
00462:         "ollama_music_insights_json",
00463:         "ai_implementation_draft_json",
00464:         "gpu_task_packet_json",
00465:         "scene_brief_json",
00466:         "asset_inventory_json",
00467:         "generated_scene_script",
00468:     ]
00469:     for key in artifact_keys:
00470:         value = session.artifacts.get(key)
00471:         if value:
00472:             file_targets.add(Path(value))
00473: 
00474:     if include_all_tracks and OUTPUT_DIR.exists():
00475:         patterns = [
00476:             "*_analysis.json",
00477:             "*_analysis.png",
00478:             "*_analysis_blender_keyframes.json",
00479:             "*_track_summary.json",
00480:             "*_music_context.json",
00481:             "*_analysis_ai_context.json",
00482:             "*_dual_ai_scene_plan.json",
00483:             "*_ollama_music_insights.json",
00484:             "*_ai_implementation_draft.json",
00485:             "*_gpu_task_packet.json",
00486:             "*_scene_brief.json",
00487:         ]
00488:         for pattern in patterns:
00489:             file_targets.update(path for path in OUTPUT_DIR.glob(pattern) if path.is_file())
00490: 
00491:     npu_files = [
00492:         "npu_code_context.md",
00493:         "npu_code_index.md",
00494:         "npu_code_manifest.json",
00495:         "npu_context_for_aider.md",
00496:         "npu_chunk_notes.md",
00497:         "npu_music_context.md",
00498:         "npu_music_manifest.json",
00499:         "npu_music_context_for_aider.md",
00500:         "npu_music_chunk_notes.md",
00501:         "npu_dual_ai_technical_notes.md",
00502:         "npu_dual_ai_implementation_notes.md",
00503:         "npu_dual_ai_chunk_notes.md",
00504:         "dual_ai_blender_agent_brief.md",
00505:         "ollama_music_insights.md",
00506:         "npu_preflight_report.json",
00507:         "npu_smoke_chunk_notes.md",
00508:         "npu_smoke_context_for_aider.md",
00509:         "generated_blender_script_candidate.py",
00510:         "generated_implementation_notes.md",
00511:     ]
00512:     file_targets.update(NPU_DIR / name for name in npu_files)
00513: 
00514:     slug = slugify(session.track_stem)
00515:     generated_ai_files = [
00516:         INDEX_AI_DIR / "scene_scripts" / f"{slug}_scene_builder_candidate.py",
00517:         INDEX_AI_DIR / "patch_library" / f"{slug}_npu_service_capsule.json",
00518:         INDEX_AI_DIR / "patch_library" / f"{slug}_npu_service_capsule.md",
00519:         INDEX_AI_DIR / "patch_library" / f"{slug}_gpu_task_packet.json",
00520:     ]
00521:     file_targets.update(generated_ai_files)
00522:     if include_all_tracks:
00523:         for pattern in [
00524:             "*_scene_builder_candidate.py",
00525:             "*_npu_service_capsule.json",
00526:             "*_npu_service_capsule.md",
00527:             "*_gpu_task_packet.json",
00528:         ]:
00529:             file_targets.update(path for path in INDEX_AI_DIR.glob(f"**/{pattern}") if path.is_file())
00530: 
00531:     npu_dirs = [
00532:         "npu_code_chunks",
00533:         "npu_music_chunks",
00534:     ]
00535:     dir_targets.update(NPU_DIR / name for name in npu_dirs)
00536: 
00537:     if include_logs:
00538:         dir_targets.add(LOG_DIR)
00539: 
00540:     existing_files = sorted(
00541:         {
00542:             path.resolve(strict=False)
00543:             for path in file_targets
00544:             if path.exists() and path.is_file() and is_safe_intermediate_target(path)
00545:         },
00546:         key=lambda item: str(item).lower(),
00547:     )
00548:     existing_dirs = sorted(
00549:         {
00550:             path.resolve(strict=False)
00551:             for path in dir_targets
00552:             if path.exists() and path.is_dir() and is_safe_intermediate_target(path)
00553:         },
00554:         key=lambda item: len(str(item)),
00555:         reverse=True,
00556:     )
00557: 
00558:     return {
00559:         "files": [str(path) for path in existing_files],
00560:         "dirs": [str(path) for path in existing_dirs],
00561:         "protected_roots": [str(AUDIO_DIR), str(RENDERS_DIR)],
00562:     }
00563: 
00564: 
00565: def cleanup_render_frame_targets(session: WorkflowSession) -> dict:
00566:     frame_dir = Path(session.artifacts.get("render_frames_dir", ""))
00567:     targets = []
00568:     if frame_dir.exists() and frame_dir.is_dir() and path_within(frame_dir, RENDERS_DIR):
00569:         targets.append(str(frame_dir.resolve(strict=False)))
00570: 
00571:     return {
00572:         "files": [],
00573:         "dirs": targets,
```
