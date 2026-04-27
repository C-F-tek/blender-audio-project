# Project Code Chunk 190/212

- File: `Tools/workflow/gui/workflow_gui.py`
- Part: `2`
- Lines: `266-478`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `contextlib`, `json`, `queue`, `sys`, `threading`, `traceback`, `tkinter`, `from tkinter import filedialog, messagebox, ttk`, `workflow_state`, `from scene_brief import append_scene_message, clear_scene_chat_history, generate_scene_chat_reply, load_or_create_scene_brief`
- Classes: `QueueWriter` line 23 methods: __init__, write, flush; `LogWindow` line 36 methods: __init__, hide, show, read_tail, refresh, refresh_loop; `AdvancedDebugWindow` line 98 methods: __init__, hide, show, refresh, refresh_loop, open_shell_monitor; `ProjectStatsWindow` line 154 methods: __init__, hide, show, refresh, refresh_loop; `SceneDirectorChatWindow` line 202 methods: __init__, hide, show, scene_path, refresh, send_message, clear_chat, append_system_line, on_return, on_shift_return; `WorkflowGui` line 360 methods: __init__, build_layout, append_output, drain_output_queue, set_buttons_enabled, run_task, refresh_session_loop, refresh_session, choose_wav, reset_wav
- Functions: `main()` line 708
- Assignments: `THIS_DIR`, `WORKFLOW_DIR`

## Content
```py
00266:             lines.append("Scrivi qui le modifiche alla scena. Invio invia, Shift+Invio va a capo.")
00267:             lines.append("")
00268:         for item in transcript:
00269:             role = str(item.get("role") or "note").upper()
00270:             time = str(item.get("time") or "")
00271:             content = str(item.get("content") or item.get("answer") or "")
00272:             label = str(item.get("label") or "")
00273:             heading = f"{role} {time}".strip()
00274:             if label:
00275:                 heading += f" [{label}]"
00276:             lines.append(heading)
00277:             lines.append(content)
00278:             lines.append("")
00279: 
00280:         self.transcript.configure(state="normal")
00281:         self.transcript.delete("1.0", "end")
00282:         self.transcript.insert("1.0", "\n".join(lines))
00283:         self.transcript.configure(state="disabled")
00284:         self.transcript.see("end")
00285: 
00286:     def send_message(self) -> str:
00287:         if self.worker and self.worker.is_alive():
00288:             self.append_system_line("Sto ancora aspettando la risposta del modello precedente.")
00289:             return "break"
00290: 
00291:         message = self.input.get("1.0", "end-1c").strip()
00292:         if not message:
00293:             return "break"
00294:         session = wf.load_session(create=True)
00295:         brief_path = Path(session.artifacts["scene_brief_json"])
00296:         append_scene_message(
00297:             track_stem=session.track_stem,
00298:             audio_path=session.artifacts["audio_path"],
00299:             output_path=brief_path,
00300:             role="user",
00301:             content=message,
00302:         )
00303:         self.input.delete("1.0", "end")
00304:         self.refresh()
00305:         self.append_system_line("ASSISTANT: sto elaborando con Ollama...")
00306: 
00307:         def worker() -> None:
00308:             try:
00309:                 generate_scene_chat_reply(
00310:                     track_stem=session.track_stem,
00311:                     audio_path=session.artifacts["audio_path"],
00312:                     output_path=brief_path,
00313:                     user_message=message,
00314:                     model=session.chat_model,
00315:                     asset_inventory_path=Path(session.artifacts.get("asset_inventory_json", "")),
00316:                 )
00317:             except Exception:
00318:                 append_scene_message(
00319:                     track_stem=session.track_stem,
00320:                     audio_path=session.artifacts["audio_path"],
00321:                     output_path=brief_path,
00322:                     role="assistant",
00323:                     content="Errore inatteso nella chat locale:\n" + traceback.format_exc(),
00324:                 )
00325:             finally:
00326:                 self.after(0, self.refresh)
00327: 
00328:         self.worker = threading.Thread(target=worker, daemon=True)
00329:         self.worker.start()
00330:         return "break"
00331: 
00332:     def clear_chat(self) -> None:
00333:         if self.worker and self.worker.is_alive():
00334:             messagebox.showwarning("Busy", "Aspetta la risposta del modello prima di pulire la chat.")
00335:             return
00336:         if not messagebox.askyesno("Clear chat", "Pulire la cronologia chat del direttore AI? Le preferenze del brief restano salvate."):
00337:             return
00338:         session = wf.load_session(create=True)
00339:         clear_scene_chat_history(
00340:             track_stem=session.track_stem,
00341:             audio_path=session.artifacts["audio_path"],
00342:             output_path=Path(session.artifacts["scene_brief_json"]),
00343:         )
00344:         self.refresh()
00345: 
00346:     def append_system_line(self, text: str) -> None:
00347:         self.transcript.configure(state="normal")
00348:         self.transcript.insert("end", "\n" + text + "\n")
00349:         self.transcript.configure(state="disabled")
00350:         self.transcript.see("end")
00351: 
00352:     def on_return(self, _event) -> str:
00353:         return self.send_message()
00354: 
00355:     def on_shift_return(self, _event) -> None:
00356:         self.input.insert("insert", "\n")
00357:         return None
00358: 
00359: 
00360: class WorkflowGui(tk.Tk):
00361:     def __init__(self) -> None:
00362:         super().__init__()
00363:         self.title("Spaziotempo Workflow Control")
00364:         self.geometry("1180x760")
00365:         self.minsize(980, 640)
00366: 
00367:         self.session = wf.load_session(create=True)
00368:         self.output_queue: queue.Queue[str] = queue.Queue()
00369:         self.worker: threading.Thread | None = None
00370:         self.log_window: LogWindow | None = None
00371:         self.advanced_debug_window: AdvancedDebugWindow | None = None
00372:         self.project_stats_window: ProjectStatsWindow | None = None
00373:         self.scene_director_window: SceneDirectorChatWindow | None = None
00374: 
00375:         self.include_manual = tk.BooleanVar(value=True)
00376:         self.skip_npu = tk.BooleanVar(value=True)
00377:         self.skip_ollama = tk.BooleanVar(value=False)
00378:         self.manual_limit = tk.StringVar(value="80")
00379:         self.creative_model = tk.StringVar(value=self.session.creative_model)
00380:         self.technical_model = tk.StringVar(value=self.session.technical_model)
00381:         self.chat_model = tk.StringVar(value=self.session.chat_model)
00382:         self.script_tokens = tk.StringVar(value=str(self.session.script_max_tokens))
00383:         self.available_models = wf.available_ollama_models()
00384: 
00385:         self.build_layout()
00386:         self.refresh_session()
00387:         self.after(150, self.drain_output_queue)
00388:         self.after(5000, self.refresh_session_loop)
00389: 
00390:         if self.session.debug_enabled:
00391:             self.open_log_window()
00392: 
00393:     def build_layout(self) -> None:
00394:         root = ttk.Frame(self, padding=10)
00395:         root.pack(fill="both", expand=True)
00396: 
00397:         left = ttk.Frame(root)
00398:         left.pack(side="left", fill="y")
00399: 
00400:         right = ttk.Frame(root)
00401:         right.pack(side="right", fill="both", expand=True, padx=(12, 0))
00402: 
00403:         self.session_box = tk.Text(right, height=12, wrap="word")
00404:         self.session_box.pack(fill="x")
00405:         self.session_box.configure(state="disabled")
00406: 
00407:         options = ttk.LabelFrame(left, text="AI Options")
00408:         options.pack(fill="x", pady=(0, 8))
00409:         ttk.Checkbutton(options, text="Include manual", variable=self.include_manual).pack(anchor="w", padx=8, pady=(6, 0))
00410:         ttk.Checkbutton(options, text="Skip NPU heavy pass", variable=self.skip_npu).pack(anchor="w", padx=8)
00411:         ttk.Checkbutton(options, text="Skip Ollama", variable=self.skip_ollama).pack(anchor="w", padx=8)
00412:         ttk.Label(options, text="Creative model").pack(anchor="w", padx=8, pady=(6, 0))
00413:         ttk.Combobox(options, textvariable=self.creative_model, values=self.available_models, width=28).pack(fill="x", padx=8)
00414:         ttk.Label(options, text="Technical/script model").pack(anchor="w", padx=8, pady=(6, 0))
00415:         ttk.Combobox(options, textvariable=self.technical_model, values=self.available_models, width=28).pack(fill="x", padx=8)
00416:         ttk.Label(options, text="Chat model").pack(anchor="w", padx=8, pady=(6, 0))
00417:         ttk.Combobox(options, textvariable=self.chat_model, values=self.available_models, width=28).pack(fill="x", padx=8)
00418:         token_row = ttk.Frame(options)
00419:         token_row.pack(fill="x", padx=8, pady=(6, 0))
00420:         ttk.Label(token_row, text="Script tokens").pack(side="left")
00421:         ttk.Entry(token_row, textvariable=self.script_tokens, width=8).pack(side="left", padx=(6, 0))
00422:         ttk.Button(options, text="Save AI models", command=self.save_ai_models).pack(fill="x", padx=8, pady=(6, 0))
00423:         limit_row = ttk.Frame(options)
00424:         limit_row.pack(fill="x", padx=8, pady=6)
00425:         ttk.Label(limit_row, text="Manual limit").pack(side="left")
00426:         ttk.Entry(limit_row, textvariable=self.manual_limit, width=8).pack(side="left", padx=(6, 0))
00427: 
00428:         actions = ttk.LabelFrame(left, text="Operations")
00429:         actions.pack(fill="both", expand=True)
00430: 
00431:         self.buttons: list[ttk.Button] = []
00432:         self.always_enabled_buttons: list[ttk.Button] = []
00433:         specs = [
00434:             ("Choose WAV", self.choose_wav, False),
00435:             ("Reset default WAV", self.reset_wav, False),
00436:             ("Analyze WAV", lambda: self.run_task("Analyze WAV", lambda: wf.run_analyze_wav(self.session, skip_music_context=True)), False),
00437:             ("Track summary", lambda: self.run_task("Track summary", lambda: wf.run_track_summary(self.session)), False),
00438:             ("Music context", lambda: self.run_task("Music context", lambda: wf.run_music_context(self.session)), False),
00439:             ("Code context + indexAI", lambda: self.run_task("Code context + indexAI", lambda: wf.run_code_context(self.session)), False),
00440:             ("Rebuild indexAI", lambda: self.run_task("Rebuild indexAI", lambda: wf.run_project_ai_index(self.session, force=True)), False),
00441:             ("Full audio prepare", lambda: self.run_task("Full audio prepare", lambda: wf.run_full_audio_prepare(self.session)), False),
00442:             ("Index manuals", self.index_manuals, False),
00443:             ("Dual AI plan", self.dual_ai_plan, False),
00444:             ("Scene director chat", self.scene_director_chat, False),
00445:             ("Dual AI scene script", self.dual_ai_draft, False),
00446:             ("Cleanup intermedi", self.cleanup_intermediates, False),
00447:             ("Cleanup render frames", self.cleanup_render_frames, False),
00448:             ("Toggle debug", self.toggle_debug, True),
00449:             ("Open log panel", self.open_log_window, True),
00450:             ("Advanced debug check", self.open_advanced_debug_window, True),
00451:             ("Startup service check", self.startup_service_check, True),
00452:             ("Project stats", self.open_project_stats_window, True),
00453:             ("Debug monitor shell", self.open_debug_monitor_shell, True),
00454:             ("Mark interrupted", self.mark_interrupted, True),
00455:             ("Refresh", self.refresh_session, True),
00456:         ]
00457: 
00458:         for label, command, always_enabled in specs:
00459:             button = ttk.Button(actions, text=label, command=command)
00460:             button.pack(fill="x", padx=8, pady=3)
00461:             if always_enabled:
00462:                 self.always_enabled_buttons.append(button)
00463:             else:
00464:                 self.buttons.append(button)
00465: 
00466:         output_frame = ttk.LabelFrame(right, text="Live Output")
00467:         output_frame.pack(fill="both", expand=True, pady=(10, 0))
00468:         self.output = tk.Text(output_frame, wrap="word")
00469:         self.output.pack(fill="both", expand=True, padx=6, pady=6)
00470: 
00471:     def append_output(self, text: str) -> None:
00472:         self.output.insert("end", text)
00473:         self.output.see("end")
00474: 
00475:     def drain_output_queue(self) -> None:
00476:         while True:
00477:             try:
00478:                 text = self.output_queue.get_nowait()
```
