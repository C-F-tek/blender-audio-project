# Project Code Chunk 210/212

- File: `Tools/workflow/workflow_state.py`
- Part: `5`
- Lines: `1103-1230`

## Symbol Map
- Imports: `from __future__ import annotations`, `from dataclasses import dataclass, asdict`, `from datetime import datetime`, `from pathlib import Path`, `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `time`
- Classes: `OperationResult` line 45; `WorkflowSession` line 125 methods: default, save
- Functions: `now_iso()` line 40; `write_json(path, payload)` line 59; `append_event(operation, event, payload)` line 64; `save_operation_result(result)` line 76; `slugify(value)` line 82; `track_stem_from_wav(wav_path)` line 89; `build_artifacts(wav_path)` line 93; `load_session(create)` line 159; `set_current_wav(wav_path)` line 191; `reset_to_default_wav()` line 218; `set_debug_enabled(enabled)` line 239; `available_ollama_models()` line 248; `set_ai_models()` line 266; `python_executable()` line 297; `audio_python_executable()` line 313; `run_command(command, operation, check, echo, debug, print_output, metadata, log)` line 346; `finish_session_operation(session, operation)` line 425; `path_within(path, parent)` line 431; `is_safe_intermediate_target(path)` line 439; `cleanup_intermediate_targets(session, include_all_tracks, include_logs)` line 450; `cleanup_render_frame_targets(session)` line 565; `delete_target_set(operation, targets, session)` line 582; `human_bytes(size)` line 632; `scan_path_stats(path)` line 641; `collect_matching_files(root, patterns)` line 683; `file_set_stats(name, paths)` line 692; `build_project_storage_stats(session)` line 714; `format_project_storage_stats(stats)` line 795; `cleanup_intermediates(session, include_all_tracks, include_logs)` line 841; `cleanup_render_frames(session)` line 854; `operation_status(session)` line 859; `run_analyze_wav(session, fps, skip_music_context)` line 877; `run_track_summary(session)` line 894; `run_music_context(session, include_ollama, ollama_model)` line 912; `run_code_context(session)` line 934; `run_project_ai_index(session, force)` line 941; `run_asset_inventory(session)` line 950; `run_scene_director_brief(session)` line 968; `run_manual_index(session, limit_files)` line 1001; `ensure_manual_library(session)` line 1011; `artifact_missing(session, key)` line 1017; `ensure_ai_prerequisites(session, phase, include_manual)` line 1022; `run_dual_ai(session, phase, include_manual, skip_npu, skip_ollama, creative_model, technical_model, max_new_tokens)` line 1053; `run_full_audio_prepare(session)` line 1123
- Assignments: `ROOT`, `PROJECT_DIR`, `AUDIO_DIR`, `RENDERS_DIR`, `OUTPUT_DIR`, `TOOLS_DIR`, `NPU_DIR`, `INDEX_AI_DIR`, `SESSION_PATH`, `LOG_DIR`, `EVENT_LOG_PATH`, `LAST_RESULT_PATH`, `DEFAULT_WAV`, `DEFAULT_TRACK_STEM`, `DEFAULT_RENDER_STEM`, `DEFAULT_FRAME_PREFIX`, `NPU_PYTHON`, `AUDIO_PYTHON`, `DEFAULT_CREATIVE_MODEL`, `DEFAULT_TECHNICAL_MODEL`, `DEFAULT_CHAT_MODEL`, `DEFAULT_SCRIPT_TOKENS`

## Content
```py
01103:     asset_inventory = Path(session.artifacts.get("asset_inventory_json", ""))
01104:     if asset_inventory.exists():
01105:         args.extend(["--asset-inventory", str(asset_inventory)])
01106:     run_command(
01107:         args,
01108:         operation=f"dual_ai_{phase}",
01109:         metadata={
01110:             "track_stem": session.track_stem,
01111:             "include_manual": include_manual,
01112:             "skip_npu": skip_npu,
01113:             "skip_ollama": skip_ollama,
01114:             "creative_model": creative_model,
01115:             "technical_model": technical_model,
01116:             "max_new_tokens": max_new_tokens,
01117:             "project_index": str(INDEX_AI_DIR / "project_code_index.md"),
01118:         },
01119:     )
01120:     finish_session_operation(session, f"dual_ai_{phase}")
01121: 
01122: 
01123: def run_full_audio_prepare(session: WorkflowSession) -> None:
01124:     run_analyze_wav(session, skip_music_context=True)
01125:     run_track_summary(session)
01126:     run_music_context(session)
01127:     run_code_context(session)
01128:     ensure_manual_library(session)
01129:     finish_session_operation(session, "full_audio_prepare")
01130: 
01131: 
01132: def run_advanced_debug_check(probe_write: bool = True) -> str:
01133:     from workflow_debug import build_debug_report, format_debug_report
01134: 
01135:     report = build_debug_report(probe_write=probe_write)
01136:     return format_debug_report(report)
01137: 
01138: 
01139: def run_startup_service_check() -> str:
01140:     from startup_check import build_report, format_report, save_report
01141: 
01142:     report = build_report(PROJECT_DIR, ROOT)
01143:     save_report(report)
01144:     return format_report(report)
01145: 
01146: 
01147: def _powershell_quote(value: Path | str) -> str:
01148:     return "'" + str(value).replace("'", "''") + "'"
01149: 
01150: 
01151: def open_debug_monitor_window(interval: float = 3.0, probe_write: bool = True) -> subprocess.Popen:
01152:     py = NPU_PYTHON if NPU_PYTHON.exists() else Path(sys.executable)
01153:     script = Path(__file__).with_name("workflow_debug.py")
01154:     args = [
01155:         _powershell_quote(py),
01156:         _powershell_quote(script),
01157:         "--watch",
01158:         "--interval",
01159:         str(max(1.0, interval)),
01160:     ]
01161:     if not probe_write:
01162:         args.append("--no-write-probe")
01163:     command_text = "& " + " ".join(args)
01164:     command = [
01165:         "powershell",
01166:         "-NoExit",
01167:         "-ExecutionPolicy",
01168:         "Bypass",
01169:         "-Command",
01170:         command_text,
01171:     ]
01172:     creationflags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
01173:     process = subprocess.Popen(command, cwd=str(PROJECT_DIR), creationflags=creationflags)
01174:     append_event(
01175:         "debug_monitor",
01176:         "opened",
01177:         {
01178:             "pid": process.pid,
01179:             "interval": interval,
01180:             "probe_write": probe_write,
01181:             "script": str(script),
01182:         },
01183:     )
01184:     return process
01185: 
01186: 
01187: def mark_active_operation_interrupted(reason: str = "manual interrupt") -> OperationResult:
01188:     from workflow_debug import detect_active_operation, read_events
01189: 
01190:     session = load_session(create=True)
01191:     active = detect_active_operation(read_events())
01192:     operation = active.get("operation") or session.last_operation or "unknown_operation"
01193:     result = OperationResult(
01194:         operation=str(operation),
01195:         ok=False,
01196:         started_at=str(active.get("started_at") or now_iso()),
01197:         ended_at=now_iso(),
01198:         elapsed_sec=round(float(active.get("elapsed_sec") or 0.0), 4),
01199:         command=(active.get("payload") or {}).get("command"),
01200:         cwd=str(PROJECT_DIR),
01201:         returncode=130,
01202:         stdout_tail="",
01203:         error=reason,
01204:         metadata={"marked_interrupted": True, "reason": reason},
01205:     )
01206:     save_operation_result(result)
01207:     finish_session_operation(session, f"{operation}_interrupted")
01208:     return result
01209: 
01210: 
01211: def available_operations() -> list[dict]:
01212:     return [
01213:         {"id": "set_wav", "label": "Scegli WAV", "gui_ready": True, "heavy": False},
01214:         {"id": "reset_wav", "label": "Ripristina WAV default", "gui_ready": True, "heavy": False},
01215:         {"id": "analyze_wav", "label": "Analizza WAV", "gui_ready": True, "heavy": True},
01216:         {"id": "build_track_summary", "label": "Crea track summary", "gui_ready": True, "heavy": False},
01217:         {"id": "build_music_context", "label": "Crea/aggiorna music context", "gui_ready": True, "heavy": False},
01218:         {"id": "build_code_context", "label": "Crea/aggiorna code context + indexAI", "gui_ready": True, "heavy": False},
01219:         {"id": "build_project_ai_index", "label": "Rigenera indexAI progetto", "gui_ready": True, "heavy": False},
01220:         {"id": "full_audio_prepare", "label": "Prepara audio completo", "gui_ready": True, "heavy": True},
01221:         {"id": "build_manual_context", "label": "Indicizza manuali locali", "gui_ready": True, "heavy": True},
01222:         {"id": "dual_ai_plan", "label": "Dual AI plan", "gui_ready": True, "heavy": True},
01223:         {"id": "dual_ai_implementation", "label": "Dual AI scene script draft", "gui_ready": True, "heavy": True},
01224:         {"id": "cleanup_intermediates", "label": "Pulisci intermedi", "gui_ready": True, "heavy": False},
01225:         {"id": "cleanup_render_frames", "label": "Pulisci frame render", "gui_ready": True, "heavy": False},
01226:         {"id": "advanced_debug_check", "label": "Debug advanced check", "gui_ready": True, "heavy": False},
01227:         {"id": "startup_service_check", "label": "Startup service check", "gui_ready": True, "heavy": False},
01228:         {"id": "debug_monitor_window", "label": "Apri debug monitor", "gui_ready": True, "heavy": False},
01229:         {"id": "mark_interrupted", "label": "Registra operazione interrotta", "gui_ready": True, "heavy": False},
01230:     ]
```
