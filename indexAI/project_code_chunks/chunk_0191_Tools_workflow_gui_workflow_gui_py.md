# Project Code Chunk 191/212

- File: `Tools/workflow/gui/workflow_gui.py`
- Part: `3`
- Lines: `479-714`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `contextlib`, `json`, `queue`, `sys`, `threading`, `traceback`, `tkinter`, `from tkinter import filedialog, messagebox, ttk`, `workflow_state`, `from scene_brief import append_scene_message, clear_scene_chat_history, generate_scene_chat_reply, load_or_create_scene_brief`
- Classes: `QueueWriter` line 23 methods: __init__, write, flush; `LogWindow` line 36 methods: __init__, hide, show, read_tail, refresh, refresh_loop; `AdvancedDebugWindow` line 98 methods: __init__, hide, show, refresh, refresh_loop, open_shell_monitor; `ProjectStatsWindow` line 154 methods: __init__, hide, show, refresh, refresh_loop; `SceneDirectorChatWindow` line 202 methods: __init__, hide, show, scene_path, refresh, send_message, clear_chat, append_system_line, on_return, on_shift_return; `WorkflowGui` line 360 methods: __init__, build_layout, append_output, drain_output_queue, set_buttons_enabled, run_task, refresh_session_loop, refresh_session, choose_wav, reset_wav
- Functions: `main()` line 708
- Assignments: `THIS_DIR`, `WORKFLOW_DIR`

## Content
```py
00479:             except queue.Empty:
00480:                 break
00481:             self.append_output(text)
00482:         self.after(150, self.drain_output_queue)
00483: 
00484:     def set_buttons_enabled(self, enabled: bool) -> None:
00485:         state = "normal" if enabled else "disabled"
00486:         for button in self.buttons:
00487:             button.configure(state=state)
00488:         for button in self.always_enabled_buttons:
00489:             button.configure(state="normal")
00490: 
00491:     def run_task(self, label: str, func) -> None:
00492:         if self.worker and self.worker.is_alive():
00493:             messagebox.showwarning("Busy", "An operation is already running.")
00494:             return
00495: 
00496:         def target() -> None:
00497:             writer = QueueWriter(self.output_queue)
00498:             self.output_queue.put(f"\n=== {label} ===\n")
00499:             try:
00500:                 with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
00501:                     func()
00502:                 self.output_queue.put(f"\n[OK] {label}\n")
00503:             except Exception:
00504:                 self.output_queue.put("\n[ERROR]\n")
00505:                 self.output_queue.put(traceback.format_exc())
00506:             finally:
00507:                 self.session = wf.load_session()
00508:                 self.output_queue.put("\n--- done ---\n")
00509:                 self.after(0, self.refresh_session)
00510:                 self.after(0, lambda: self.set_buttons_enabled(True))
00511: 
00512:         self.set_buttons_enabled(False)
00513:         self.worker = threading.Thread(target=target, daemon=True)
00514:         self.worker.start()
00515: 
00516:     def refresh_session_loop(self) -> None:
00517:         self.refresh_session()
00518:         self.after(5000, self.refresh_session_loop)
00519: 
00520:     def refresh_session(self) -> None:
00521:         self.session = wf.load_session(create=True)
00522:         self.creative_model.set(self.session.creative_model)
00523:         self.technical_model.set(self.session.technical_model)
00524:         self.chat_model.set(self.session.chat_model)
00525:         self.script_tokens.set(str(self.session.script_max_tokens))
00526:         status = wf.operation_status(self.session)
00527:         lines = [
00528:             f"Session: {wf.SESSION_PATH}",
00529:             f"WAV:     {self.session.artifacts['audio_path']}",
00530:             f"Track:   {self.session.track_stem}",
00531:             f"Default: {'no, session active' if self.session.use_session_track else 'yes'}",
00532:             f"Debug:   {'ON' if self.session.debug_enabled else 'OFF'}",
00533:             f"Creative model:  {self.session.creative_model}",
00534:             f"Technical model: {self.session.technical_model}",
00535:             f"Chat model:      {self.session.chat_model}",
00536:             f"Script tokens:   {self.session.script_max_tokens}",
00537:             f"Last:    {self.session.last_operation or '-'}",
00538:             f"Log:     {wf.EVENT_LOG_PATH}",
00539:             "",
00540:             "Outputs:",
00541:         ]
00542:         for key in [
00543:             "analysis_json",
00544:             "track_summary_json",
00545:             "music_context_json",
00546:             "analysis_ai_context_json",
00547:             "blender_keyframes_json",
00548:             "dual_ai_plan_json",
00549:             "scene_brief_json",
00550:             "asset_inventory_json",
00551:             "ai_implementation_draft_json",
00552:             "generated_scene_script",
00553:         ]:
00554:             mark = "OK" if status.get(key) else "--"
00555:             lines.append(f"[{mark}] {key}: {self.session.artifacts[key]}")
00556: 
00557:         self.session_box.configure(state="normal")
00558:         self.session_box.delete("1.0", "end")
00559:         self.session_box.insert("1.0", "\n".join(lines))
00560:         self.session_box.configure(state="disabled")
00561: 
00562:         if self.session.debug_enabled and self.log_window is None:
00563:             self.open_log_window()
00564: 
00565:     def choose_wav(self) -> None:
00566:         initial = Path(self.session.artifacts["audio_path"]).parent
00567:         path = filedialog.askopenfilename(
00568:             title="Choose WAV",
00569:             initialdir=str(initial if initial.exists() else wf.AUDIO_DIR),
00570:             filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
00571:         )
00572:         if not path:
00573:             return
00574:         try:
00575:             self.session = wf.set_current_wav(path)
00576:             self.refresh_session()
00577:         except Exception as exc:
00578:             messagebox.showerror("Choose WAV failed", str(exc))
00579: 
00580:     def reset_wav(self) -> None:
00581:         self.session = wf.reset_to_default_wav()
00582:         self.refresh_session()
00583: 
00584:     def index_manuals(self) -> None:
00585:         try:
00586:             limit = int(self.manual_limit.get() or "80")
00587:         except ValueError:
00588:             messagebox.showerror("Manual limit", "Manual limit must be a number.")
00589:             return
00590:         self.run_task("Index manuals", lambda: wf.run_manual_index(self.session, limit_files=limit))
00591: 
00592:     def save_ai_models(self) -> None:
00593:         try:
00594:             tokens = int(self.script_tokens.get() or str(wf.DEFAULT_SCRIPT_TOKENS))
00595:         except ValueError:
00596:             messagebox.showerror("Script tokens", "Script tokens must be a number.")
00597:             return
00598:         self.session = wf.set_ai_models(
00599:             creative_model=self.creative_model.get().strip(),
00600:             technical_model=self.technical_model.get().strip(),
00601:             chat_model=self.chat_model.get().strip(),
00602:             script_max_tokens=tokens,
00603:         )
00604:         self.refresh_session()
00605: 
00606:     def startup_service_check(self) -> None:
00607:         self.run_task("Startup service check", wf.run_startup_service_check)
00608: 
00609:     def dual_ai_plan(self) -> None:
00610:         self.run_task(
00611:             "Dual AI plan",
00612:             lambda: wf.run_dual_ai(
00613:                 self.session,
00614:                 phase="plan",
00615:                 include_manual=self.include_manual.get(),
00616:                 skip_npu=self.skip_npu.get(),
00617:                 skip_ollama=self.skip_ollama.get(),
00618:                 creative_model=self.creative_model.get().strip(),
00619:                 technical_model=self.technical_model.get().strip(),
00620:                 max_new_tokens=int(self.script_tokens.get() or str(wf.DEFAULT_SCRIPT_TOKENS)),
00621:             ),
00622:         )
00623: 
00624:     def scene_director_chat(self) -> None:
00625:         if self.scene_director_window is None or not self.scene_director_window.winfo_exists():
00626:             self.scene_director_window = SceneDirectorChatWindow(self)
00627:         self.scene_director_window.show()
00628: 
00629:     def dual_ai_draft(self) -> None:
00630:         self.run_task(
00631:             "Dual AI scene script draft",
00632:             lambda: wf.run_dual_ai(
00633:                 self.session,
00634:                 phase="implementation",
00635:                 include_manual=self.include_manual.get(),
00636:                 skip_npu=self.skip_npu.get(),
00637:                 skip_ollama=self.skip_ollama.get(),
00638:                 creative_model=self.creative_model.get().strip(),
00639:                 technical_model=self.technical_model.get().strip(),
00640:                 max_new_tokens=int(self.script_tokens.get() or str(wf.DEFAULT_SCRIPT_TOKENS)),
00641:             ),
00642:         )
00643: 
00644:     def confirm_targets(self, title: str, targets: dict) -> bool:
00645:         files = targets.get("files", [])
00646:         dirs = targets.get("dirs", [])
00647:         preview = [title, "", f"Files: {len(files)}", f"Dirs: {len(dirs)}", ""]
00648:         for item in files[:8]:
00649:             preview.append(f"FILE {item}")
00650:         if len(files) > 8:
00651:             preview.append(f"... {len(files) - 8} more files")
00652:         for item in dirs[:8]:
00653:             preview.append(f"DIR  {item}")
00654:         if len(dirs) > 8:
00655:             preview.append(f"... {len(dirs) - 8} more dirs")
00656:         if not files and not dirs:
00657:             messagebox.showinfo(title, "Nothing to clean.")
00658:             return False
00659:         return messagebox.askyesno(title, "\n".join(preview))
00660: 
00661:     def cleanup_intermediates(self) -> None:
00662:         targets = wf.cleanup_intermediate_targets(self.session, include_all_tracks=True, include_logs=True)
00663:         if self.confirm_targets("Cleanup intermediates", targets):
00664:             self.run_task("Cleanup intermediates", lambda: wf.cleanup_intermediates(self.session, include_all_tracks=True, include_logs=True))
00665: 
00666:     def cleanup_render_frames(self) -> None:
00667:         targets = wf.cleanup_render_frame_targets(self.session)
00668:         if self.confirm_targets("Cleanup render frames", targets):
00669:             self.run_task("Cleanup render frames", lambda: wf.cleanup_render_frames(self.session))
00670: 
00671:     def toggle_debug(self) -> None:
00672:         self.session = wf.set_debug_enabled(not self.session.debug_enabled)
00673:         self.refresh_session()
00674:         if self.session.debug_enabled:
00675:             self.open_log_window()
00676: 
00677:     def open_log_window(self) -> None:
00678:         if self.log_window is None or not self.log_window.winfo_exists():
00679:             self.log_window = LogWindow(self)
00680:         self.log_window.show()
00681: 
00682:     def open_advanced_debug_window(self) -> None:
00683:         if self.advanced_debug_window is None or not self.advanced_debug_window.winfo_exists():
00684:             self.advanced_debug_window = AdvancedDebugWindow(self)
00685:         self.advanced_debug_window.show()
00686: 
00687:     def open_project_stats_window(self) -> None:
00688:         if self.project_stats_window is None or not self.project_stats_window.winfo_exists():
00689:             self.project_stats_window = ProjectStatsWindow(self)
00690:         self.project_stats_window.show()
00691: 
00692:     def open_debug_monitor_shell(self) -> None:
00693:         try:
00694:             process = wf.open_debug_monitor_window(interval=3.0, probe_write=True)
00695:             self.append_output(f"\nDebug monitor shell opened. PID: {process.pid}\n")
00696:         except Exception:
00697:             self.append_output("\n" + traceback.format_exc())
00698: 
00699:     def mark_interrupted(self) -> None:
00700:         try:
00701:             result = wf.mark_active_operation_interrupted("manual interrupt from GUI")
00702:             self.append_output(f"\nMarked interrupted: {result.operation}, elapsed={result.elapsed_sec}s\n")
00703:             self.refresh_session()
00704:         except Exception:
00705:             self.append_output("\n" + traceback.format_exc())
00706: 
00707: 
00708: def main() -> None:
00709:     app = WorkflowGui()
00710:     app.mainloop()
00711: 
00712: 
00713: if __name__ == "__main__":
00714:     main()
```
