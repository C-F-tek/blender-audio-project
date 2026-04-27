# Project Code Chunk 202/212

- File: `Tools/workflow/workflow_debug.py`
- Part: `2`
- Lines: `272-505`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `argparse`, `json`, `os`, `shutil`, `subprocess`, `time`, `workflow_state`
- Functions: `_iso_to_dt(value)` line 15; `_format_age(seconds)` line 24; `_format_size(size)` line 37; `_read_json(path)` line 48; `read_events(max_events)` line 57; `detect_active_operation(events)` line 75; `_tail_non_empty(path, max_lines)` line 116; `_write_probe(directory)` line 126; `path_check(label, path, required, expect)` line 145; `expected_paths_for_operation(session, operation)` line 189; `collect_processes()` line 304; `collect_write_checks(probe_write)` line 338; `active_compute_processes(processes, operation)` line 361; `build_debug_report(probe_write)` line 390; `_format_check(item)` line 467; `_format_process(item)` line 475; `format_debug_report(report)` line 485; `main()` line 578

## Content
```py
00272:         progress_files = [("NPU chunk notes", npu("npu_dual_ai_chunk_notes.md"), "file")]
00273:     elif operation == "dual_ai_implementation":
00274:         operation_inputs = [
00275:             ("Analysis JSON", artifacts["analysis_json"], "file"),
00276:             ("Track summary JSON", artifacts["track_summary_json"], "file"),
00277:             ("Music context JSON", artifacts["music_context_json"], "file"),
00278:             ("Analysis AI context JSON", artifacts["analysis_ai_context_json"], "file"),
00279:             ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
00280:             ("Dual AI scene plan JSON", artifacts["dual_ai_plan_json"], "file"),
00281:             ("run_dual_ai_pipeline.py", npu("run_dual_ai_pipeline.py"), "file"),
00282:             ("NPU Python", wf.NPU_PYTHON, "file"),
00283:         ]
00284:         operation_outputs = [
00285:             ("AI implementation draft JSON", artifacts["ai_implementation_draft_json"], "file"),
00286:             ("Generated script candidate", npu("generated_blender_script_candidate.py"), "file"),
00287:             ("Generated implementation notes", npu("generated_implementation_notes.md"), "file"),
00288:             ("NPU implementation notes", npu("npu_dual_ai_implementation_notes.md"), "file"),
00289:         ]
00290:         progress_files = [("NPU chunk notes", npu("npu_dual_ai_chunk_notes.md"), "file")]
00291:     elif operation == "cleanup_intermediates":
00292:         operation_inputs = [("Output dir", wf.OUTPUT_DIR, "dir"), ("NPU dir", wf.NPU_DIR, "dir")]
00293:     elif operation == "cleanup_render_frames":
00294:         operation_inputs = [("Render frames dir", artifacts["render_frames_dir"], "dir")]
00295: 
00296:     return {
00297:         "common_inputs": common_inputs,
00298:         "operation_inputs": operation_inputs,
00299:         "operation_outputs": operation_outputs,
00300:         "progress_files": progress_files,
00301:     }
00302: 
00303: 
00304: def collect_processes() -> list[dict]:
00305:     powershell = shutil.which("powershell") or shutil.which("pwsh")
00306:     if not powershell:
00307:         return []
00308:     script = (
00309:         "Get-Process | Where-Object { $_.ProcessName -match 'python|ollama|openvino|ffmpeg|blender' } | "
00310:         "Select-Object ProcessName,Id,CPU,WorkingSet64,@{Name='StartTime';Expression={$_.StartTime.ToString('yyyy-MM-dd HH:mm:ss')}},Path | "
00311:         "Sort-Object WorkingSet64 -Descending | ConvertTo-Json -Compress -Depth 3"
00312:     )
00313:     try:
00314:         result = subprocess.run(
00315:             [powershell, "-NoProfile", "-Command", script],
00316:             text=True,
00317:             stdout=subprocess.PIPE,
00318:             stderr=subprocess.DEVNULL,
00319:             check=False,
00320:             timeout=6,
00321:         )
00322:     except Exception:
00323:         return []
00324:     output = (result.stdout or "").strip()
00325:     if not output:
00326:         return []
00327:     try:
00328:         payload = json.loads(output)
00329:     except json.JSONDecodeError:
00330:         return []
00331:     if isinstance(payload, dict):
00332:         payload = [payload]
00333:     if not isinstance(payload, list):
00334:         return []
00335:     return [item for item in payload if isinstance(item, dict)]
00336: 
00337: 
00338: def collect_write_checks(probe_write: bool = True) -> list[dict]:
00339:     targets = [
00340:         ("Project root", wf.PROJECT_DIR),
00341:         ("Output dir", wf.OUTPUT_DIR),
00342:         ("Workflow log dir", wf.LOG_DIR),
00343:         ("NPU tools dir", wf.NPU_DIR),
00344:         ("Renders dir", wf.RENDERS_DIR),
00345:     ]
00346:     checks: list[dict] = []
00347:     for label, path in targets:
00348:         base = path_check(label, path, required=True, expect="dir")
00349:         base["write_probe"] = ""
00350:         if probe_write:
00351:             ok, message = _write_probe(Path(path))
00352:             base["writable"] = ok
00353:             base["write_probe"] = message
00354:             if not ok:
00355:                 base["status"] = "WARN" if base["status"] == "OK" else base["status"]
00356:                 base["message"] = message
00357:         checks.append(base)
00358:     return checks
00359: 
00360: 
00361: def active_compute_processes(processes: list[dict], operation: str) -> list[dict]:
00362:     heavy_ops = {
00363:         "analyze_wav",
00364:         "build_manual_context",
00365:         "dual_ai_plan",
00366:         "dual_ai_implementation",
00367:         "full_audio_prepare",
00368:     }
00369:     if operation not in heavy_ops:
00370:         return []
00371: 
00372:     active: list[dict] = []
00373:     for item in processes:
00374:         name = str(item.get("ProcessName") or "").lower()
00375:         ram = int(item.get("WorkingSet64") or 0)
00376:         path = str(item.get("Path") or "").lower()
00377:         if "ollama app" in name:
00378:             continue
00379:         if name.startswith("python") and ram > 200 * 1024 * 1024:
00380:             active.append(item)
00381:         elif name.startswith("ollama") and ram > 200 * 1024 * 1024:
00382:             active.append(item)
00383:         elif "ffmpeg" in name or "blender" in name:
00384:             active.append(item)
00385:         elif "openvino" in name or "openvino" in path:
00386:             active.append(item)
00387:     return active
00388: 
00389: 
00390: def build_debug_report(probe_write: bool = True) -> dict:
00391:     session = wf.load_session(create=True)
00392:     events = read_events()
00393:     active = detect_active_operation(events)
00394:     operation = active["operation"] or session.last_operation or "-"
00395:     expected = expected_paths_for_operation(session, operation)
00396: 
00397:     common_checks = [path_check(label, path, required=True, expect=expect) for label, path, expect in expected["common_inputs"]]
00398:     input_checks = [path_check(label, path, required=True, expect=expect) for label, path, expect in expected["operation_inputs"]]
00399:     output_checks = [path_check(label, path, required=False, expect=expect) for label, path, expect in expected["operation_outputs"]]
00400:     progress_checks = [path_check(label, path, required=False, expect=expect) for label, path, expect in expected["progress_files"]]
00401: 
00402:     start_dt = _iso_to_dt(active.get("started_at"))
00403:     watched = output_checks + progress_checks
00404:     latest_write: dict | None = None
00405:     for item in watched:
00406:         item_dt = _iso_to_dt(item.get("mtime"))
00407:         if not item_dt:
00408:             continue
00409:         if start_dt and item_dt < start_dt:
00410:             item["message"] = "old file from before active operation"
00411:         if latest_write is None or str(item.get("mtime", "")) > str(latest_write.get("mtime", "")):
00412:             latest_write = item
00413: 
00414:     warnings: list[str] = []
00415:     if active["active"] and latest_write:
00416:         latest_dt = _iso_to_dt(latest_write.get("mtime"))
00417:         if latest_dt:
00418:             idle = (datetime.now() - latest_dt).total_seconds()
00419:             if idle > 600:
00420:                 warnings.append(f"No watched output/progress file changed for {_format_age(idle)}.")
00421:     if active["active"] and not latest_write and active.get("elapsed_sec") and active["elapsed_sec"] > 300:
00422:         warnings.append("Active operation has no watched output/progress files yet after 5m.")
00423: 
00424:     if any(item["status"] in {"MISSING", "WARN"} for item in input_checks):
00425:         warnings.append("Some required input paths for the active operation are missing or suspicious.")
00426: 
00427:     progress_previews = []
00428:     for label, path, _expect in expected["progress_files"]:
00429:         progress_previews.append({"label": label, "path": str(path), "tail": _tail_non_empty(Path(path))})
00430: 
00431:     processes = collect_processes()
00432:     compute_processes = active_compute_processes(processes, operation)
00433:     active_status = "active" if active.get("active") else "none"
00434:     if active.get("active") and active.get("elapsed_sec") and active["elapsed_sec"] > 120 and not compute_processes:
00435:         active_status = "stale_or_interrupted"
00436:         warnings.append(
00437:             "Log has a start event without a result, but no heavy Python/Ollama/Blender/FFmpeg process is running."
00438:         )
00439: 
00440:     report = {
00441:         "generated_at": wf.now_iso(),
00442:         "session": {
00443:             "path": str(wf.SESSION_PATH),
00444:             "track_stem": session.track_stem,
00445:             "audio_path": session.artifacts.get("audio_path"),
00446:             "debug_enabled": session.debug_enabled,
00447:             "last_operation": session.last_operation,
00448:         },
00449:         "active_operation": active,
00450:         "active_status": active_status,
00451:         "operation_for_checks": operation,
00452:         "last_result": _read_json(wf.LAST_RESULT_PATH),
00453:         "common_checks": common_checks,
00454:         "input_checks": input_checks,
00455:         "output_checks": output_checks,
00456:         "progress_checks": progress_checks,
00457:         "write_checks": collect_write_checks(probe_write=probe_write),
00458:         "progress_previews": progress_previews,
00459:         "processes": processes,
00460:         "active_compute_processes": compute_processes,
00461:         "recent_events": events[-8:],
00462:         "warnings": warnings,
00463:     }
00464:     return report
00465: 
00466: 
00467: def _format_check(item: dict) -> str:
00468:     size = _format_size(item.get("size"))
00469:     mtime = item.get("mtime") or "-"
00470:     message = item.get("message") or item.get("write_probe") or ""
00471:     suffix = f" | {message}" if message else ""
00472:     return f"[{item.get('status', 'OK')}] {item.get('label')}: {item.get('path')} | {size} | {mtime}{suffix}"
00473: 
00474: 
00475: def _format_process(item: dict) -> str:
00476:     name = item.get("ProcessName", "-")
00477:     pid = item.get("Id", "-")
00478:     cpu = item.get("CPU", "-")
00479:     ram = _format_size(int(item.get("WorkingSet64") or 0))
00480:     start = item.get("StartTime", "-")
00481:     path = item.get("Path") or ""
00482:     return f"{name} pid={pid} cpu={cpu} ram={ram} start={start} {path}"
00483: 
00484: 
00485: def format_debug_report(report: dict) -> str:
00486:     active = report["active_operation"]
00487:     session = report["session"]
00488:     lines: list[str] = []
00489:     lines.append("=" * 78)
00490:     lines.append("SPAZIOTEMPO ADVANCED DEBUG CHECK")
00491:     lines.append("=" * 78)
00492:     lines.append(f"Generated: {report['generated_at']}")
00493:     lines.append(f"Track:     {session['track_stem']}")
00494:     lines.append(f"Audio:     {session['audio_path']}")
00495:     lines.append(f"Debug:     {'ON' if session['debug_enabled'] else 'OFF'}")
00496:     if active.get("active"):
00497:         status = report.get("active_status", "active")
00498:         if status == "stale_or_interrupted":
00499:             lines.append(
00500:                 f"Active:    stale/interrupted log for {active.get('operation')} since {active.get('started_at')} "
00501:                 f"elapsed {_format_age(active.get('elapsed_sec'))}"
00502:             )
00503:         else:
00504:             lines.append(
00505:                 f"Active:    {active.get('operation')} since {active.get('started_at')} "
```
