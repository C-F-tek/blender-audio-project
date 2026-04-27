# Project Code Chunk 205/212

- File: `Tools/workflow/workflow_shell.py`
- Part: `2`
- Lines: `270-298`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `sys`, `from workflow_state import DEFAULT_WAV, EVENT_LOG_PATH, LAST_RESULT_PATH, SESSION_PATH, build_project_storage_stats, format_project_storage_stats, load_session, available_ollama_models, mark_active_operation_interrupted, open_debug_monitor_window, operation_status, reset_to_default_wav, cleanup_intermediate_targets, cleanup_intermediates, cleanup_render_frame_targets, cleanup_render_frames, run_analyze_wav, run_advanced_debug_check, run_code_context, run_dual_ai, run_full_audio_prepare, run_manual_index, run_music_context, run_project_ai_index, run_scene_director_brief, run_startup_service_check, run_track_summary, set_current_wav, set_ai_models, set_debug_enabled`
- Functions: `print_header(session)` line 40; `ask_path(prompt)` line 71; `ask_bool(prompt, default)` line 75; `menu()` line 83; `choose_model(prompt, current)` line 110; `confirm_cleanup(title, targets)` line 127; `main()` line 156

## Content
```py
00270:                 chat = choose_model("Chat model per direttore AI", session.chat_model)
00271:                 raw_tokens = input(f"Max token script [{session.script_max_tokens}]: ").strip()
00272:                 tokens = int(raw_tokens) if raw_tokens else session.script_max_tokens
00273:                 session = set_ai_models(
00274:                     creative_model=creative,
00275:                     technical_model=technical,
00276:                     chat_model=chat,
00277:                     script_max_tokens=tokens,
00278:                 )
00279: 
00280:             elif choice == "22":
00281:                 print(run_startup_service_check())
00282: 
00283:             else:
00284:                 print("Scelta non riconosciuta.")
00285: 
00286:         except KeyboardInterrupt:
00287:             print("\nOperazione interrotta.")
00288:         except Exception as exc:
00289:             print(f"\n[ERRORE] {exc}")
00290: 
00291:         input("\nInvio per continuare...")
00292: 
00293: 
00294: if __name__ == "__main__":
00295:     try:
00296:         main()
00297:     except KeyboardInterrupt:
00298:         sys.exit(130)
```
