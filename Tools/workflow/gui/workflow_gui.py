from __future__ import annotations

from pathlib import Path
import contextlib
import json
import queue
import sys
import threading
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


THIS_DIR = Path(__file__).resolve().parent
WORKFLOW_DIR = THIS_DIR.parent
if str(WORKFLOW_DIR) not in sys.path:
    sys.path.insert(0, str(WORKFLOW_DIR))

import workflow_state as wf  # noqa: E402
from components.artifact_browser import ArtifactBrowserWindow  # noqa: E402
from scene_brief import append_scene_message, clear_scene_chat_history, generate_scene_chat_reply, load_or_create_scene_brief  # noqa: E402


class QueueWriter:
    def __init__(self, target_queue: queue.Queue[str]) -> None:
        self.target_queue = target_queue

    def write(self, text: str) -> int:
        if text:
            self.target_queue.put(text)
        return len(text)

    def flush(self) -> None:
        return None


class LogWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.title("Spaziotempo Workflow Logs")
        self.geometry("980x620")
        self.protocol("WM_DELETE_WINDOW", self.hide)

        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=8, pady=6)
        ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(side="left")
        ttk.Button(toolbar, text="Hide", command=self.hide).pack(side="left", padx=(6, 0))

        self.text = tk.Text(self, wrap="none", height=32)
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        yscroll = ttk.Scrollbar(self.text, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side="right", fill="y")

        self.after(1000, self.refresh_loop)

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()
        self.lift()
        self.refresh()

    def read_tail(self, path: Path, max_lines: int = 160) -> str:
        if not path.exists():
            return f"{path}\n<missing>\n"
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception as exc:
            return f"{path}\n<read failed: {exc}>\n"
        return "\n".join(lines[-max_lines:]) + "\n"

    def refresh(self) -> None:
        body = []
        body.append(f"EVENT LOG: {wf.EVENT_LOG_PATH}\n")
        body.append(self.read_tail(wf.EVENT_LOG_PATH))
        body.append("\nLAST RESULT:\n")
        if wf.LAST_RESULT_PATH.exists():
            try:
                payload = json.loads(wf.LAST_RESULT_PATH.read_text(encoding="utf-8"))
                body.append(json.dumps(payload, indent=2, ensure_ascii=False))
            except Exception:
                body.append(self.read_tail(wf.LAST_RESULT_PATH, max_lines=120))
        else:
            body.append("<missing>")

        self.text.delete("1.0", "end")
        self.text.insert("1.0", "".join(body))
        self.text.see("end")

    def refresh_loop(self) -> None:
        if self.state() != "withdrawn":
            self.refresh()
        self.after(2500, self.refresh_loop)


class AdvancedDebugWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.title("Spaziotempo Advanced Debug")
        self.geometry("1120x760")
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.auto_refresh = tk.BooleanVar(value=True)

        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=8, pady=6)
        ttk.Button(toolbar, text="Check", command=self.refresh).pack(side="left")
        ttk.Checkbutton(toolbar, text="Auto refresh", variable=self.auto_refresh).pack(side="left", padx=(8, 0))
        ttk.Button(toolbar, text="Open shell monitor", command=self.open_shell_monitor).pack(side="left", padx=(8, 0))
        ttk.Button(toolbar, text="Hide", command=self.hide).pack(side="left", padx=(8, 0))

        self.text = tk.Text(self, wrap="none")
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        yscroll = ttk.Scrollbar(self.text, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side="right", fill="y")

        self.after(1000, self.refresh_loop)

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()
        self.lift()
        self.refresh()

    def refresh(self) -> None:
        try:
            report = wf.run_advanced_debug_check(probe_write=True)
        except Exception:
            report = traceback.format_exc()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", report)
        self.text.see("end")

    def refresh_loop(self) -> None:
        if self.state() != "withdrawn" and self.auto_refresh.get():
            self.refresh()
        self.after(3000, self.refresh_loop)

    def open_shell_monitor(self) -> None:
        try:
            process = wf.open_debug_monitor_window(interval=3.0, probe_write=True)
            self.text.insert("end", f"\n\nOpened shell debug monitor PID: {process.pid}\n")
            self.text.see("end")
        except Exception:
            self.text.insert("end", "\n\n" + traceback.format_exc())
            self.text.see("end")


class ProjectStatsWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.title("Spaziotempo Project Stats")
        self.geometry("1120x760")
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.auto_refresh = tk.BooleanVar(value=False)

        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=8, pady=6)
        ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(side="left")
        ttk.Checkbutton(toolbar, text="Auto refresh", variable=self.auto_refresh).pack(side="left", padx=(8, 0))
        ttk.Button(toolbar, text="Hide", command=self.hide).pack(side="left", padx=(8, 0))

        self.text = tk.Text(self, wrap="none")
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        yscroll = ttk.Scrollbar(self.text, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side="right", fill="y")

        self.after(1000, self.refresh_loop)

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()
        self.lift()
        self.refresh()

    def refresh(self) -> None:
        try:
            session = wf.load_session(create=True)
            stats = wf.build_project_storage_stats(session)
            report = wf.format_project_storage_stats(stats)
        except Exception:
            report = traceback.format_exc()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", report)
        self.text.see("1.0")

    def refresh_loop(self) -> None:
        if self.state() != "withdrawn" and self.auto_refresh.get():
            self.refresh()
        self.after(5000, self.refresh_loop)


class SceneDirectorChatWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.title("Spaziotempo Scene Director Chat")
        self.geometry("980x720")
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.worker: threading.Thread | None = None

        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=8, pady=6)
        ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(side="left")
        ttk.Button(toolbar, text="Save message", command=self.send_message).pack(side="left", padx=(6, 0))
        ttk.Button(toolbar, text="Clear chat", command=self.clear_chat).pack(side="left", padx=(6, 0))
        ttk.Button(toolbar, text="Hide", command=self.hide).pack(side="left", padx=(6, 0))

        self.transcript = tk.Text(self, wrap="word", height=26)
        self.transcript.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        self.transcript.configure(state="disabled")

        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", padx=8, pady=(0, 8))

        self.input = tk.Text(input_frame, wrap="word", height=5)
        self.input.pack(side="left", fill="both", expand=True)
        self.input.bind("<Return>", self.on_return)
        self.input.bind("<Shift-Return>", self.on_shift_return)

        send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side="right", padx=(8, 0), fill="y")

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()
        self.lift()
        self.refresh()
        self.input.focus_set()

    def scene_path(self) -> Path:
        session = wf.load_session(create=True)
        return Path(session.artifacts["scene_brief_json"])

    def refresh(self) -> None:
        session = wf.load_session(create=True)
        brief = load_or_create_scene_brief(
            track_stem=session.track_stem,
            audio_path=session.artifacts["audio_path"],
            output_path=Path(session.artifacts["scene_brief_json"]),
        )
        lines = [
            f"Track: {session.track_stem}",
            f"Brief: {session.artifacts['scene_brief_json']}",
            "",
        ]
        memory = brief.get("conversation_memory") if isinstance(brief.get("conversation_memory"), dict) else {}
        if memory:
            lines.append(f"Memory: {memory.get('message_count', 0)} messaggi, aggiornata {memory.get('updated_at', '-')}")
            constraints = memory.get("durable_constraints") if isinstance(memory.get("durable_constraints"), list) else []
            for item in constraints[-4:]:
                lines.append(f"- {item}")
            lines.append("")
        transcript = brief.get("conversation_transcript") or []
        if not transcript:
            lines.append("Scrivi qui le modifiche alla scena. Invio invia, Shift+Invio va a capo.")
            lines.append("")
        for item in transcript:
            role = str(item.get("role") or "note").upper()
            time = str(item.get("time") or "")
            content = str(item.get("content") or item.get("answer") or "")
            label = str(item.get("label") or "")
            heading = f"{role} {time}".strip()
            if label:
                heading += f" [{label}]"
            lines.append(heading)
            lines.append(content)
            lines.append("")

        self.transcript.configure(state="normal")
        self.transcript.delete("1.0", "end")
        self.transcript.insert("1.0", "\n".join(lines))
        self.transcript.configure(state="disabled")
        self.transcript.see("end")

    def send_message(self) -> str:
        if self.worker and self.worker.is_alive():
            self.append_system_line("Sto ancora aspettando la risposta del modello precedente.")
            return "break"

        message = self.input.get("1.0", "end-1c").strip()
        if not message:
            return "break"
        session = wf.load_session(create=True)
        brief_path = Path(session.artifacts["scene_brief_json"])
        append_scene_message(
            track_stem=session.track_stem,
            audio_path=session.artifacts["audio_path"],
            output_path=brief_path,
            role="user",
            content=message,
        )
        self.input.delete("1.0", "end")
        self.refresh()
        self.append_system_line("ASSISTANT: sto elaborando con Ollama...")

        def worker() -> None:
            try:
                generate_scene_chat_reply(
                    track_stem=session.track_stem,
                    audio_path=session.artifacts["audio_path"],
                    output_path=brief_path,
                    user_message=message,
                    model=session.chat_model,
                    asset_inventory_path=Path(session.artifacts.get("asset_inventory_json", "")),
                )
            except Exception:
                append_scene_message(
                    track_stem=session.track_stem,
                    audio_path=session.artifacts["audio_path"],
                    output_path=brief_path,
                    role="assistant",
                    content="Errore inatteso nella chat locale:\n" + traceback.format_exc(),
                )
            finally:
                self.after(0, self.refresh)

        self.worker = threading.Thread(target=worker, daemon=True)
        self.worker.start()
        return "break"

    def clear_chat(self) -> None:
        if self.worker and self.worker.is_alive():
            messagebox.showwarning("Busy", "Aspetta la risposta del modello prima di pulire la chat.")
            return
        if not messagebox.askyesno("Clear chat", "Pulire la cronologia chat del direttore AI? Le preferenze del brief restano salvate."):
            return
        session = wf.load_session(create=True)
        clear_scene_chat_history(
            track_stem=session.track_stem,
            audio_path=session.artifacts["audio_path"],
            output_path=Path(session.artifacts["scene_brief_json"]),
        )
        self.refresh()

    def append_system_line(self, text: str) -> None:
        self.transcript.configure(state="normal")
        self.transcript.insert("end", "\n" + text + "\n")
        self.transcript.configure(state="disabled")
        self.transcript.see("end")

    def on_return(self, _event) -> str:
        return self.send_message()

    def on_shift_return(self, _event) -> None:
        self.input.insert("insert", "\n")
        return None


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
        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)

        left = ttk.Frame(root)
        left.pack(side="left", fill="y")

        right = ttk.Frame(root)
        right.pack(side="right", fill="both", expand=True, padx=(12, 0))

        self.session_box = tk.Text(right, height=12, wrap="word")
        self.session_box.pack(fill="x")
        self.session_box.configure(state="disabled")

        options = ttk.LabelFrame(left, text="AI Options")
        options.pack(fill="x", pady=(0, 8))
        ttk.Checkbutton(options, text="Include manual", variable=self.include_manual).pack(anchor="w", padx=8, pady=(6, 0))
        ttk.Checkbutton(options, text="Skip NPU heavy pass", variable=self.skip_npu).pack(anchor="w", padx=8)
        ttk.Checkbutton(options, text="Skip Ollama", variable=self.skip_ollama).pack(anchor="w", padx=8)
        ttk.Label(options, text="Creative model").pack(anchor="w", padx=8, pady=(6, 0))
        ttk.Combobox(options, textvariable=self.creative_model, values=self.available_models, width=28).pack(fill="x", padx=8)
        ttk.Label(options, text="Technical/script model").pack(anchor="w", padx=8, pady=(6, 0))
        ttk.Combobox(options, textvariable=self.technical_model, values=self.available_models, width=28).pack(fill="x", padx=8)
        ttk.Label(options, text="Chat model").pack(anchor="w", padx=8, pady=(6, 0))
        ttk.Combobox(options, textvariable=self.chat_model, values=self.available_models, width=28).pack(fill="x", padx=8)
        token_row = ttk.Frame(options)
        token_row.pack(fill="x", padx=8, pady=(6, 0))
        ttk.Label(token_row, text="Script tokens").pack(side="left")
        ttk.Entry(token_row, textvariable=self.script_tokens, width=8).pack(side="left", padx=(6, 0))
        ttk.Button(options, text="Save AI models", command=self.save_ai_models).pack(fill="x", padx=8, pady=(6, 0))
        limit_row = ttk.Frame(options)
        limit_row.pack(fill="x", padx=8, pady=6)
        ttk.Label(limit_row, text="Manual limit").pack(side="left")
        ttk.Entry(limit_row, textvariable=self.manual_limit, width=8).pack(side="left", padx=(6, 0))

        actions = ttk.LabelFrame(left, text="Operations")
        actions.pack(fill="both", expand=True)

        self.buttons: list[ttk.Button] = []
        self.always_enabled_buttons: list[ttk.Button] = []
        specs = [
            ("Choose WAV", self.choose_wav, False),
            ("Reset default WAV", self.reset_wav, False),
            ("Analyze WAV", lambda: self.run_task("Analyze WAV", lambda: wf.run_analyze_wav(self.session, skip_music_context=True)), False),
            ("Track summary", lambda: self.run_task("Track summary", lambda: wf.run_track_summary(self.session)), False),
            ("Music context", lambda: self.run_task("Music context", lambda: wf.run_music_context(self.session)), False),
            ("Code context + indexAI", lambda: self.run_task("Code context + indexAI", lambda: wf.run_code_context(self.session)), False),
            ("Rebuild indexAI", lambda: self.run_task("Rebuild indexAI", lambda: wf.run_project_ai_index(self.session, force=True)), False),
            ("Full audio prepare", lambda: self.run_task("Full audio prepare", lambda: wf.run_full_audio_prepare(self.session)), False),
            ("Index manuals", self.index_manuals, False),
            ("Dual AI plan", self.dual_ai_plan, False),
            ("Scene director chat", self.scene_director_chat, False),
            ("Dual AI scene script", self.dual_ai_draft, False),
            ("Cleanup intermedi", self.cleanup_intermediates, False),
            ("Cleanup render frames", self.cleanup_render_frames, False),
            ("Toggle debug", self.toggle_debug, True),
            ("Open log panel", self.open_log_window, True),
            ("Advanced debug check", self.open_advanced_debug_window, True),
            ("Startup service check", self.startup_service_check, True),
            ("Project stats", self.open_project_stats_window, True),
            ("Artifact browser", self.open_artifact_browser_window, True),
            ("Debug monitor shell", self.open_debug_monitor_shell, True),
            ("Mark interrupted", self.mark_interrupted, True),
            ("Refresh", self.refresh_session, True),
        ]

        for label, command, always_enabled in specs:
            button = ttk.Button(actions, text=label, command=command)
            button.pack(fill="x", padx=8, pady=3)
            if always_enabled:
                self.always_enabled_buttons.append(button)
            else:
                self.buttons.append(button)

        output_frame = ttk.LabelFrame(right, text="Live Output")
        output_frame.pack(fill="both", expand=True, pady=(10, 0))
        self.output = tk.Text(output_frame, wrap="word")
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

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
        targets = wf.cleanup_intermediate_targets(self.session, include_all_tracks=True, include_logs=True)
        if self.confirm_targets("Cleanup intermediates", targets):
            self.run_task("Cleanup intermediates", lambda: wf.cleanup_intermediates(self.session, include_all_tracks=True, include_logs=True))

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
            self.append_output(f"\nMarked interrupted: {result.operation}, elapsed={result.elapsed_sec}s\n")
            self.refresh_session()
        except Exception:
            self.append_output("\n" + traceback.format_exc())


def main() -> None:
    app = WorkflowGui()
    app.mainloop()


if __name__ == "__main__":
    main()
