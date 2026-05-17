"""Auxiliary debug and statistics windows for the classic workflow GUI."""

from __future__ import annotations

import json
import tkinter as tk
import traceback
from pathlib import Path
from tkinter import ttk

from workflow_gui_common import wf


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
        ttk.Checkbutton(toolbar, text="Auto refresh", variable=self.auto_refresh).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(toolbar, text="Open shell monitor", command=self.open_shell_monitor).pack(
            side="left", padx=(8, 0)
        )
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
        ttk.Checkbutton(toolbar, text="Auto refresh", variable=self.auto_refresh).pack(
            side="left", padx=(8, 0)
        )
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
