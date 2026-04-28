from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
import tkinter as tk
from tkinter import ttk

from components.st_theme import text_widget_colors


@dataclass(frozen=True)
class LiveEvent:
    time: str
    kind: str
    message: str


def classify_line(line: str) -> str:
    text = line.strip()
    lower = text.lower()
    if not text:
        return "empty"
    if text.startswith("===") and text.endswith("==="):
        return "section"
    if text.startswith("$ "):
        return "command"
    if "[error]" in lower or "traceback" in lower or "exception" in lower or "errore" in lower:
        return "error"
    if "[ok]" in lower or lower.startswith("ok ") or "success" in lower or "done" in lower:
        return "success"
    if "[debug]" in lower or "debug" in lower:
        return "debug"
    if "warning" in lower or "warn" in lower:
        return "warning"
    if re.search(r"\[[0-9]+/[0-9]+\]", text):
        return "progress"
    return "info"


class LiveOutputPanel(ttk.Frame):
    """Graphical live-output dashboard for workflow execution output."""

    def __init__(self, master) -> None:
        super().__init__(master)
        self.events: list[LiveEvent] = []
        self.counts = {
            "section": 0,
            "command": 0,
            "success": 0,
            "error": 0,
            "warning": 0,
            "debug": 0,
            "progress": 0,
            "info": 0,
        }
        self.auto_scroll = tk.BooleanVar(value=True)
        self.show_debug = tk.BooleanVar(value=True)
        self.build_layout()

    def build_layout(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 8))
        ttk.Label(header, text="Live Output", style="Header.TLabel").pack(side="left")
        ttk.Label(header, text="Esecuzione pipeline in tempo reale", style="SubHeader.TLabel").pack(side="left", padx=(14, 0))
        ttk.Button(header, text="Clear", command=self.clear).pack(side="right")
        ttk.Checkbutton(header, text="Auto-scroll", variable=self.auto_scroll).pack(side="right", padx=(0, 10))
        ttk.Checkbutton(header, text="Debug", variable=self.show_debug, command=self.rebuild_event_tree).pack(side="right", padx=(0, 10))

        self.metric_frame = ttk.Frame(self, style="Panel.TFrame")
        self.metric_frame.pack(fill="x", pady=(0, 8))
        self.metric_labels: dict[str, ttk.Label] = {}
        for key, label in [
            ("section", "Step"),
            ("command", "Command"),
            ("success", "OK"),
            ("error", "Error"),
            ("warning", "Warning"),
            ("debug", "Debug"),
        ]:
            card = ttk.Frame(self.metric_frame, style="Panel.TFrame", padding=8)
            card.pack(side="left", fill="x", expand=True, padx=4)
            ttk.Label(card, text=label, style="MetricName.TLabel").pack(anchor="w")
            value = ttk.Label(card, text="0", style="Metric.TLabel")
            value.pack(anchor="w", pady=(2, 0))
            self.metric_labels[key] = value

        panes = ttk.PanedWindow(self, orient="vertical")
        panes.pack(fill="both", expand=True)

        events_frame = ttk.LabelFrame(panes, text="Event timeline")
        raw_frame = ttk.LabelFrame(panes, text="Raw output")
        panes.add(events_frame, weight=1)
        panes.add(raw_frame, weight=3)

        columns = ("time", "kind", "message")
        self.event_tree = ttk.Treeview(events_frame, columns=columns, show="headings", height=8)
        self.event_tree.heading("time", text="ORA")
        self.event_tree.heading("kind", text="TIPO")
        self.event_tree.heading("message", text="MESSAGGIO")
        self.event_tree.column("time", width=88)
        self.event_tree.column("kind", width=90)
        self.event_tree.column("message", width=900)
        self.event_tree.pack(fill="both", expand=True, side="left")
        event_scroll = ttk.Scrollbar(events_frame, orient="vertical", command=self.event_tree.yview)
        self.event_tree.configure(yscrollcommand=event_scroll.set)
        event_scroll.pack(side="right", fill="y")

        self.raw_text = tk.Text(raw_frame, wrap="word", borderwidth=1, relief="solid", **text_widget_colors(self))
        self.raw_text.pack(fill="both", expand=True, side="left")
        raw_scroll = ttk.Scrollbar(raw_frame, orient="vertical", command=self.raw_text.yview)
        self.raw_text.configure(yscrollcommand=raw_scroll.set)
        raw_scroll.pack(side="right", fill="y")

        self.configure_tags()
        self.write_banner()

    def configure_tags(self) -> None:
        self.raw_text.tag_configure("section", font=("Segoe UI", 10, "bold"))
        self.raw_text.tag_configure("command", font=("Consolas", 9, "bold"))
        self.raw_text.tag_configure("success", foreground="green")
        self.raw_text.tag_configure("error", foreground="red", font=("Consolas", 9, "bold"))
        self.raw_text.tag_configure("warning", foreground="#9A6500")
        self.raw_text.tag_configure("debug", foreground="SystemGrayText")
        self.raw_text.tag_configure("progress", foreground="SystemHighlight")
        self.raw_text.tag_configure("info", font=("Consolas", 9))

    def write_banner(self) -> None:
        self.raw_text.insert(
            "end",
            "Live Output pronto. Avvia una operazione dalla colonna Workflow Actions.\n",
            "info",
        )

    def clear(self) -> None:
        self.events.clear()
        for key in self.counts:
            self.counts[key] = 0
        self.raw_text.delete("1.0", "end")
        self.event_tree.delete(*self.event_tree.get_children())
        self.refresh_metrics()
        self.write_banner()

    def append_text(self, text: str) -> None:
        if not text:
            return
        lines = text.splitlines(keepends=True)
        for line in lines:
            kind = classify_line(line)
            tag = kind if kind in self.counts else "info"
            self.raw_text.insert("end", line, tag)
            if kind != "empty":
                self.add_event(kind, line.strip())
        if self.auto_scroll.get():
            self.raw_text.see("end")
            children = self.event_tree.get_children()
            if children:
                self.event_tree.see(children[-1])
        self.refresh_metrics()

    def add_event(self, kind: str, message: str) -> None:
        if kind == "debug" and not self.show_debug.get():
            self.counts[kind] = self.counts.get(kind, 0) + 1
            return
        if kind in self.counts:
            self.counts[kind] += 1
        else:
            self.counts["info"] += 1
        event = LiveEvent(datetime.now().strftime("%H:%M:%S"), kind, message[:280])
        self.events.append(event)
        self.event_tree.insert("", "end", values=(event.time, event.kind.upper(), event.message))

    def refresh_metrics(self) -> None:
        for key, label in self.metric_labels.items():
            label.configure(text=str(self.counts.get(key, 0)))

    def rebuild_event_tree(self) -> None:
        self.event_tree.delete(*self.event_tree.get_children())
        for event in self.events:
            if event.kind == "debug" and not self.show_debug.get():
                continue
            self.event_tree.insert("", "end", values=(event.time, event.kind.upper(), event.message))
