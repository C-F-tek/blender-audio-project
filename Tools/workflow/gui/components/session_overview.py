from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import ttk
from typing import Any

from components.st_theme import text_widget_colors


def human_bytes(size: int | float) -> str:
    value = float(size or 0)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024.0 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024.0
    return f"{value:.1f} TB"


def file_size(path_text: str) -> int:
    try:
        path = Path(path_text)
        return path.stat().st_size if path.exists() and path.is_file() else 0
    except Exception:
        return 0


class SessionOverviewFrame(ttk.Frame):
    """Readable session status panel with sortable output table."""

    OUTPUT_KEYS = (
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
        "render_mp4",
        "render_ffmpeg_mp4",
        "render_frames_dir",
    )

    SORT_COLUMNS = ("status", "key", "type", "size", "path")

    def __init__(self, master, *, open_path_callback=None, copy_callback=None) -> None:
        super().__init__(master)
        self.session = None
        self.status: dict[str, bool] = {}
        self.rows: list[dict[str, Any]] = []
        self.filtered_rows: list[dict[str, Any]] = []
        self.sort_column = "key"
        self.sort_reverse = False
        self.open_path_callback = open_path_callback
        self.copy_callback = copy_callback
        self.search_var = tk.StringVar(value="")
        self.selected_path: Path | None = None
        self.build_layout()

    def build_layout(self) -> None:
        self.pack(fill="both", expand=True)

        top = ttk.Frame(self)
        top.pack(fill="x", pady=(0, 8))

        self.track_label = ttk.Label(top, text="Track: -", style="Header.TLabel")
        self.track_label.pack(side="left")
        self.debug_label = ttk.Label(top, text="", style="SubHeader.TLabel")
        self.debug_label.pack(side="left", padx=(14, 0))

        tools = ttk.Frame(top)
        tools.pack(side="right")
        ttk.Label(tools, text="Search").pack(side="left", padx=(0, 5))
        search = ttk.Entry(tools, textvariable=self.search_var, width=28)
        search.pack(side="left")
        search.bind("<KeyRelease>", lambda _event: self.apply_filter())
        ttk.Button(tools, text="Sort reset", command=self.reset_sort).pack(side="left", padx=(8, 0))

        summary = ttk.LabelFrame(self, text="Session summary")
        summary.pack(fill="x", pady=(0, 8))
        self.summary_grid = ttk.Frame(summary)
        self.summary_grid.pack(fill="x", padx=8, pady=8)
        self.summary_values: dict[str, ttk.Label] = {}
        for index, label in enumerate(("WAV", "Last operation", "Creative", "Technical", "Chat", "Script tokens")):
            ttk.Label(self.summary_grid, text=label, style="MetricName.TLabel").grid(row=index // 2, column=(index % 2) * 2, sticky="w", padx=(0, 8), pady=3)
            value = ttk.Label(self.summary_grid, text="-", wraplength=520)
            value.grid(row=index // 2, column=(index % 2) * 2 + 1, sticky="ew", padx=(0, 18), pady=3)
            self.summary_values[label] = value
        self.summary_grid.columnconfigure(1, weight=1)
        self.summary_grid.columnconfigure(3, weight=1)

        panes = ttk.PanedWindow(self, orient="vertical")
        panes.pack(fill="both", expand=True)

        table_frame = ttk.Frame(panes)
        detail_frame = ttk.Frame(panes)
        panes.add(table_frame, weight=3)
        panes.add(detail_frame, weight=2)

        columns = ("status", "key", "type", "size", "path")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=13)
        self.tree.column("status", width=80)
        self.tree.column("key", width=250)
        self.tree.column("type", width=90)
        self.tree.column("size", width=100, anchor="e")
        self.tree.column("path", width=720)
        self.configure_headings()
        self.tree.pack(fill="both", expand=True, side="left")
        self.tree.bind("<<TreeviewSelect>>", lambda _event: self.preview_selected())
        self.tree.bind("<Double-1>", lambda _event: self.open_selected())

        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side="right", fill="y")

        detail_toolbar = ttk.Frame(detail_frame)
        detail_toolbar.pack(fill="x", pady=(8, 5))
        ttk.Button(detail_toolbar, text="Open selected", command=self.open_selected).pack(side="left")
        ttk.Button(detail_toolbar, text="Open folder", command=self.open_selected_folder).pack(side="left", padx=(8, 0))
        ttk.Button(detail_toolbar, text="Copy path", command=self.copy_selected_path).pack(side="left", padx=(8, 0))

        self.detail = tk.Text(detail_frame, wrap="word", height=8, borderwidth=1, relief="solid", **text_widget_colors(self))
        self.detail.pack(fill="both", expand=True)

    def configure_headings(self) -> None:
        labels = {
            "status": "STATO",
            "key": "OUTPUT",
            "type": "TIPO",
            "size": "DIMENSIONE",
            "path": "PERCORSO",
        }
        arrow = " ↓" if self.sort_reverse else " ↑"
        for column in self.SORT_COLUMNS:
            self.tree.heading(
                column,
                text=labels[column] + (arrow if self.sort_column == column else ""),
                command=lambda col=column: self.sort_by(col),
            )

    def sort_by(self, column: str) -> None:
        if column == self.sort_column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        self.configure_headings()
        self.apply_filter()

    def reset_sort(self) -> None:
        self.sort_column = "key"
        self.sort_reverse = False
        self.configure_headings()
        self.apply_filter()

    def sort_key(self, row: dict[str, Any]):
        if self.sort_column == "status":
            return 0 if row["exists"] else 1
        if self.sort_column == "key":
            return row["key"].lower()
        if self.sort_column == "type":
            return row["type"].lower()
        if self.sort_column == "size":
            return row["size"]
        if self.sort_column == "path":
            return row["path"].lower()
        return row["key"].lower()

    def update_session(self, session, status: dict[str, bool]) -> None:
        self.session = session
        self.status = status
        self.track_label.configure(text=f"Track: {session.track_stem}")
        self.debug_label.configure(text=f"Debug: {'ON' if session.debug_enabled else 'OFF'}")
        self.summary_values["WAV"].configure(text=session.artifacts.get("audio_path", "-"))
        self.summary_values["Last operation"].configure(text=session.last_operation or "-")
        self.summary_values["Creative"].configure(text=session.creative_model)
        self.summary_values["Technical"].configure(text=session.technical_model)
        self.summary_values["Chat"].configure(text=session.chat_model)
        self.summary_values["Script tokens"].configure(text=str(session.script_max_tokens))

        rows: list[dict[str, Any]] = []
        for key in self.OUTPUT_KEYS:
            path_text = str(session.artifacts.get(key, ""))
            path = Path(path_text) if path_text else Path()
            exists = bool(status.get(key, path.exists() if path_text else False))
            suffix = path.suffix.lower().lstrip(".") if path_text else ""
            if path_text and path.is_dir():
                type_name = "folder"
            else:
                type_name = suffix or "path"
            size = file_size(path_text) if path_text else 0
            rows.append({"key": key, "path": path_text, "exists": exists, "type": type_name, "size": size})
        self.rows = rows
        self.apply_filter()
        self.write_detail("Seleziona un output per vedere dettagli. Doppio click per aprire file/cartella.")

    def apply_filter(self) -> None:
        query = self.search_var.get().strip().lower()
        self.filtered_rows = []
        for row in self.rows:
            haystack = f"{row['key']} {row['type']} {row['path']}".lower()
            if query and query not in haystack:
                continue
            self.filtered_rows.append(row)
        self.filtered_rows.sort(key=self.sort_key, reverse=self.sort_reverse)

        self.tree.delete(*self.tree.get_children())
        for index, row in enumerate(self.filtered_rows):
            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    "OK" if row["exists"] else "MISSING",
                    row["key"],
                    row["type"],
                    human_bytes(row["size"]),
                    row["path"],
                ),
            )

    def selected_row(self) -> dict[str, Any] | None:
        selected = self.tree.selection()
        if not selected:
            return None
        index = int(selected[0])
        if 0 <= index < len(self.filtered_rows):
            return self.filtered_rows[index]
        return None

    def preview_selected(self) -> None:
        row = self.selected_row()
        if not row:
            return
        self.selected_path = Path(row["path"]) if row["path"] else None
        text = [
            f"Output: {row['key']}",
            f"Status: {'OK' if row['exists'] else 'MISSING'}",
            f"Type:   {row['type']}",
            f"Size:   {human_bytes(row['size'])}",
            f"Path:   {row['path']}",
        ]
        if self.selected_path and self.selected_path.exists() and self.selected_path.is_file():
            suffix = self.selected_path.suffix.lower()
            if suffix in {".json", ".md", ".txt", ".py", ".log", ".jsonl", ".csv"}:
                try:
                    preview = self.selected_path.read_text(encoding="utf-8", errors="replace")[:20000]
                    text.extend(["", "Preview:", preview])
                except Exception as exc:
                    text.append(f"Preview error: {exc}")
        self.write_detail("\n".join(text))

    def write_detail(self, text: str) -> None:
        self.detail.configure(state="normal")
        self.detail.delete("1.0", "end")
        self.detail.insert("1.0", text)
        self.detail.configure(state="normal")

    def open_selected(self) -> None:
        row = self.selected_row()
        if row and self.open_path_callback:
            self.open_path_callback(Path(row["path"]))

    def open_selected_folder(self) -> None:
        row = self.selected_row()
        if not row or not self.open_path_callback:
            return
        path = Path(row["path"])
        self.open_path_callback(path if path.is_dir() else path.parent)

    def copy_selected_path(self) -> None:
        row = self.selected_row()
        if row and self.copy_callback:
            self.copy_callback(row["path"])
            self.write_detail(f"Percorso copiato negli appunti:\n{row['path']}")
