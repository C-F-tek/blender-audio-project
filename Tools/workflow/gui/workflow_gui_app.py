"""Classic workflow GUI application."""

from __future__ import annotations

import contextlib
import queue
import threading
import tkinter as tk
import traceback
from pathlib import Path
from tkinter import filedialog, messagebox

from components.artifact_browser import ArtifactBrowserWindow
from workflow_gui_common import QueueWriter, wf
from workflow_gui_layout import build_layout
from workflow_gui_scene_chat import SceneDirectorChatWindow
from workflow_gui_windows import AdvancedDebugWindow, LogWindow, ProjectStatsWindow


class WorkflowGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Spaziotempo Workflow Control")
        self.geometry("1180x760")
        self.minsize(980, 640)

        self.session = wf.load_session(create=True)
        self.output_queue: queue.Queue[str] = queue.Queue()
        self.worker: threading.Thread | None = None
        self.log_window: LogWindow | None = None
        self.advanced_debug_window: AdvancedDebugWindow | None = None
        self.project_stats_window: ProjectStatsWindow | None = None
        self.artifact_browser_window: ArtifactBrowserWindow | None = None
        self.scene_director_window: SceneDirectorChatWindow | None = None

        self.include_manual = tk.BooleanVar(value=True)
        self.skip_npu = tk.BooleanVar(value=True)
        self.skip_ollama = tk.BooleanVar(value=False)
        self.manual_limit = tk.StringVar(value="80")
        self.creative_model = tk.StringVar(value=self.session.creative_model)
        self.technical_model = tk.StringVar(value=self.session.technical_model)
        self.chat_model = tk.StringVar(value=self.session.chat_model)
        self.script_tokens = tk.StringVar(value=str(self.session.script_max_tokens))
        self.available_models = wf.available_ollama_models()

        self.build_layout()
        self.refresh_session()
        self.after(150, self.drain_output_queue)
        self.after(5000, self.refresh_session_loop)

        if self.session.debug_enabled:
            self.open_log_window()

    def build_layout(self) -> None:
        build_layout(self)

    def append_output(self, text: str) -> None:
        self.output.insert("end", text)
        self.output.see("end")

    def drain_output_queue(self) -> None:
        while True:
            try:
                text = self.output_queue.get_nowait()
            except queue.Empty:
                break
            self.append_output(text)
        self.after(150, self.drain_output_queue)

    def set_buttons_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for button in self.buttons:
            button.configure(state=state)
        for button in self.always_enabled_buttons:
            button.configure(state="normal")

    def run_task(self, label: str, func) -> None:
        if self.worker and self.worker.is_alive():
            messagebox.showwarning("Busy", "An operation is already running.")
            return

        def target() -> None:
            writer = QueueWriter(self.output_queue)
            self.output_queue.put(f"\n=== {label} ===\n")
            try:
                with contextlib.redirect_stdout(writer), contextlib.redirect_stderr(writer):
                    func()
                self.output_queue.put(f"\n[OK] {label}\n")
            except Exception:
                self.output_queue.put("\n[ERROR]\n")
                self.output_queue.put(traceback.format_exc())
            finally:
                self.session = wf.load_session()
                self.output_queue.put("\n--- done ---\n")
                self.after(0, self.refresh_session)
                self.after(0, lambda: self.set_buttons_enabled(True))

        self.set_buttons_enabled(False)
        self.worker = threading.Thread(target=target, daemon=True)
        self.worker.start()

    def refresh_session_loop(self) -> None:
        self.refresh_session()
        self.after(5000, self.refresh_session_loop)

    def refresh_session(self) -> None:
        self.session = wf.load_session(create=True)
        self.creative_model.set(self.session.creative_model)
        self.technical_model.set(self.session.technical_model)
        self.chat_model.set(self.session.chat_model)
        self.script_tokens.set(str(self.session.script_max_tokens))
        status = wf.operation_status(self.session)
        lines = [
            f"Session: {wf.SESSION_PATH}",
            f"WAV:     {self.session.artifacts['audio_path']}",
            f"Track:   {self.session.track_stem}",
            f"Default: {'no, session active' if self.session.use_session_track else 'yes'}",
            f"Debug:   {'ON' if self.session.debug_enabled else 'OFF'}",
            f"Creative model:  {self.session.creative_model}",
            f"Technical model: {self.session.technical_model}",
            f"Chat model:      {self.session.chat_model}",
            f"Script tokens:   {self.session.script_max_tokens}",
            f"Last:    {self.session.last_operation or '-'}",
            f"Log:     {wf.EVENT_LOG_PATH}",
            "",
            "Outputs:",
        ]
        for key in [
            "analysis_json",
            "track_summary_json",
            "music_context_json",
            "analysis_ai_context_json",
            "blender_keyframes_json",
            "dual_ai_plan_json",
            "scene_brief_json",
            "asset_inventory_json",
            "ai_implementation_draft_json",
            "generated_scene_script",
        ]:
            mark = "OK" if status.get(key) else "--"
            lines.append(f"[{mark}] {key}: {self.session.artifacts[key]}")

        self.session_box.configure(state="normal")
        self.session_box.delete("1.0", "end")
        self.session_box.insert("1.0", "\n".join(lines))
        self.session_box.configure(state="disabled")

        if self.session.debug_enabled and self.log_window is None:
            self.open_log_window()

    def choose_wav(self) -> None:
        initial = Path(self.session.artifacts["audio_path"]).parent
        path = filedialog.askopenfilename(
            title="Choose WAV",
            initialdir=str(initial if initial.exists() else wf.AUDIO_DIR),
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            self.session = wf.set_current_wav(path)
            self.refresh_session()
        except Exception as exc:
            messagebox.showerror("Choose WAV failed", str(exc))

    def reset_wav(self) -> None:
        self.session = wf.reset_to_default_wav()
        self.refresh_session()

    def index_manuals(self) -> None:
        try:
            limit = int(self.manual_limit.get() or "80")
        except ValueError:
            messagebox.showerror("Manual limit", "Manual limit must be a number.")
            return
        self.run_task("Index manuals", lambda: wf.run_manual_index(self.session, limit_files=limit))

    def save_ai_models(self) -> None:
        try:
            tokens = int(self.script_tokens.get() or str(wf.DEFAULT_SCRIPT_TOKENS))
        except ValueError:
            messagebox.showerror("Script tokens", "Script tokens must be a number.")
            return
        self.session = wf.set_ai_models(
            creative_model=self.creative_model.get().strip(),
            technical_model=self.technical_model.get().strip(),
            chat_model=self.chat_model.get().strip(),
            script_max_tokens=tokens,
        )
        self.refresh_session()

    def startup_service_check(self) -> None:
        self.run_task("Startup service check", wf.run_startup_service_check)

    def dual_ai_plan(self) -> None:
        self.run_task(
            "Dual AI plan",
            lambda: wf.run_dual_ai(
                self.session,
                phase="plan",
                include_manual=self.include_manual.get(),
                skip_npu=self.skip_npu.get(),
                skip_ollama=self.skip_ollama.get(),
                creative_model=self.creative_model.get().strip(),
                technical_model=self.technical_model.get().strip(),
                max_new_tokens=int(self.script_tokens.get() or str(wf.DEFAULT_SCRIPT_TOKENS)),
            ),
        )

    def scene_director_chat(self) -> None:
        if self.scene_director_window is None or not self.scene_director_window.winfo_exists():
            self.scene_director_window = SceneDirectorChatWindow(self)
        self.scene_director_window.show()

    def dual_ai_draft(self) -> None:
        self.run_task(
            "Dual AI scene script draft",
            lambda: wf.run_dual_ai(
                self.session,
                phase="implementation",
                include_manual=self.include_manual.get(),
                skip_npu=self.skip_npu.get(),
                skip_ollama=self.skip_ollama.get(),
                creative_model=self.creative_model.get().strip(),
                technical_model=self.technical_model.get().strip(),
                max_new_tokens=int(self.script_tokens.get() or str(wf.DEFAULT_SCRIPT_TOKENS)),
            ),
        )

    def confirm_targets(self, title: str, targets: dict) -> bool:
        files = targets.get("files", [])
        dirs = targets.get("dirs", [])
        preview = [title, "", f"Files: {len(files)}", f"Dirs: {len(dirs)}", ""]
        for item in files[:8]:
            preview.append(f"FILE {item}")
        if len(files) > 8:
            preview.append(f"... {len(files) - 8} more files")
        for item in dirs[:8]:
            preview.append(f"DIR  {item}")
        if len(dirs) > 8:
            preview.append(f"... {len(dirs) - 8} more dirs")
        if not files and not dirs:
            messagebox.showinfo(title, "Nothing to clean.")
            return False
        return messagebox.askyesno(title, "\n".join(preview))

    def cleanup_intermediates(self) -> None:
        targets = wf.cleanup_intermediate_targets(
            self.session, include_all_tracks=True, include_logs=True
        )
        if self.confirm_targets("Cleanup intermediates", targets):
            self.run_task(
                "Cleanup intermediates",
                lambda: wf.cleanup_intermediates(
                    self.session, include_all_tracks=True, include_logs=True
                ),
            )

    def cleanup_render_frames(self) -> None:
        targets = wf.cleanup_render_frame_targets(self.session)
        if self.confirm_targets("Cleanup render frames", targets):
            self.run_task("Cleanup render frames", lambda: wf.cleanup_render_frames(self.session))

    def toggle_debug(self) -> None:
        self.session = wf.set_debug_enabled(not self.session.debug_enabled)
        self.refresh_session()
        if self.session.debug_enabled:
            self.open_log_window()

    def artifact_extra_roots(self, session) -> list[Path]:
        roots: list[Path] = []
        for key in ("output_dir", "render_frames_dir"):
            value = session.artifacts.get(key)
            if value:
                roots.append(Path(value))
        for key in ("render_mp4", "render_ffmpeg_mp4"):
            value = session.artifacts.get(key)
            if value:
                roots.append(Path(value).parent)
        return roots

    def open_artifact_browser_window(self) -> None:
        if self.artifact_browser_window is None or not self.artifact_browser_window.winfo_exists():
            self.artifact_browser_window = ArtifactBrowserWindow(
                self,
                session_loader=lambda: wf.load_session(create=True),
                extra_roots_loader=self.artifact_extra_roots,
            )
        self.artifact_browser_window.show()

    def open_log_window(self) -> None:
        if self.log_window is None or not self.log_window.winfo_exists():
            self.log_window = LogWindow(self)
        self.log_window.show()

    def open_advanced_debug_window(self) -> None:
        if self.advanced_debug_window is None or not self.advanced_debug_window.winfo_exists():
            self.advanced_debug_window = AdvancedDebugWindow(self)
        self.advanced_debug_window.show()

    def open_project_stats_window(self) -> None:
        if self.project_stats_window is None or not self.project_stats_window.winfo_exists():
            self.project_stats_window = ProjectStatsWindow(self)
        self.project_stats_window.show()

    def open_debug_monitor_shell(self) -> None:
        try:
            process = wf.open_debug_monitor_window(interval=3.0, probe_write=True)
            self.append_output(f"\nDebug monitor shell opened. PID: {process.pid}\n")
        except Exception:
            self.append_output("\n" + traceback.format_exc())

    def mark_interrupted(self) -> None:
        try:
            result = wf.mark_active_operation_interrupted("manual interrupt from GUI")
            self.append_output(
                f"\nMarked interrupted: {result.operation}, elapsed={result.elapsed_sec}s\n"
            )
            self.refresh_session()
        except Exception:
            self.append_output("\n" + traceback.format_exc())
