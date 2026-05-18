"""Scene director chat window for the classic workflow GUI."""

from __future__ import annotations

import threading
import tkinter as tk
import traceback
from pathlib import Path
from tkinter import messagebox, ttk

from Tools.workflow.workflow_run._shared.scene_brief import (
    append_scene_message,
    clear_scene_chat_history,
    generate_scene_chat_reply,
    load_or_create_scene_brief,
)
from workflow_gui_common import wf


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
        ttk.Button(toolbar, text="Save message", command=self.send_message).pack(
            side="left", padx=(6, 0)
        )
        ttk.Button(toolbar, text="Clear chat", command=self.clear_chat).pack(
            side="left", padx=(6, 0)
        )
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
        memory = (
            brief.get("conversation_memory")
            if isinstance(brief.get("conversation_memory"), dict)
            else {}
        )
        if memory:
            lines.append(
                f"Memory: {memory.get('message_count', 0)} messaggi, aggiornata {memory.get('updated_at', '-')}"
            )
            constraints = (
                memory.get("durable_constraints")
                if isinstance(memory.get("durable_constraints"), list)
                else []
            )
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
            messagebox.showwarning(
                "Busy", "Aspetta la risposta del modello prima di pulire la chat."
            )
            return
        if not messagebox.askyesno(
            "Clear chat",
            "Pulire la cronologia chat del direttore AI? Le preferenze del brief restano salvate.",
        ):
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
