from __future__ import annotations

import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from components.st_theme import apply_spaziotempo_theme, text_widget_colors
from components.storage_dashboard_preview import (
    build_directory_preview,
    build_file_preview,
    build_overview_text,
)
from components.storage_dashboard_model import (
    PathStats,
    human_bytes,
    immediate_children_stats,
    safe_path,
    scan_tree,
)


class StorageDashboardWindow(tk.Toplevel):
    """Native-themed storage dashboard focused on the Blender workspace root."""

    SORT_COLUMNS = ("name", "type", "size", "files", "dirs", "path")

    def __init__(self, master: tk.Tk, *, session_loader, workflow_state_module) -> None:
        super().__init__(master)
        self.session_loader = session_loader
        self.wf = workflow_state_module
        self.session = self.session_loader()
        self.root_dir = Path(self.wf.ROOT).expanduser()
        self.project_dir = Path(self.wf.PROJECT_DIR).expanduser()
        self.selected_path: Path | None = None
        self.item_stats: dict[str, PathStats | None] = {}
        self.sort_column = "name"
        self.sort_reverse = False

        self.title("Storage Dashboard")
        self.geometry("1280x820")
        self.minsize(980, 640)
        self.protocol("WM_DELETE_WINDOW", self.hide)
        apply_spaziotempo_theme(self)
        self.build_layout()
        self.refresh()

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()
        self.lift()
        self.refresh()

    def build_layout(self) -> None:
        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root)
        header.pack(fill="x", pady=(0, 10))
        ttk.Label(header, text="Storage Dashboard", style="Header.TLabel").pack(side="left")
        ttk.Label(
            header,
            text="Cartella blender, progetto e artefatti generati",
            style="SubHeader.TLabel",
        ).pack(side="left", padx=(14, 0))
        ttk.Button(header, text="Refresh", command=self.refresh).pack(side="right")
        ttk.Button(header, text="Hide", command=self.hide).pack(side="right", padx=(0, 8))

        self.metric_frame = ttk.Frame(root, style="Panel.TFrame")
        self.metric_frame.pack(fill="x", pady=(0, 10))

        body = ttk.PanedWindow(root, orient="horizontal")
        body.pack(fill="both", expand=True)

        left = ttk.Frame(body, padding=(0, 0, 8, 0))
        right = ttk.Frame(body)
        body.add(left, weight=2)
        body.add(right, weight=3)

        self.tree = ttk.Treeview(
            left, columns=("type", "size", "files", "dirs", "path"), show="tree headings"
        )
        self.configure_tree_headings()
        self.tree.column("#0", width=250)
        self.tree.column("type", width=95)
        self.tree.column("size", width=110, anchor="e")
        self.tree.column("files", width=80, anchor="e")
        self.tree.column("dirs", width=80, anchor="e")
        self.tree.column("path", width=520)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", lambda _event: self.preview_selected())
        self.tree.bind("<Double-1>", lambda _event: self.open_selected())

        tree_scroll = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="right", fill="y")

        toolbar = ttk.Frame(right)
        toolbar.pack(fill="x", pady=(0, 6))
        ttk.Button(toolbar, text="Open selected", command=self.open_selected).pack(side="left")
        ttk.Button(toolbar, text="Open folder", command=self.open_selected_folder).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(toolbar, text="Copy path", command=self.copy_selected_path).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(toolbar, text="Sort reset", command=self.reset_sort).pack(
            side="left", padx=(8, 0)
        )

        self.preview = tk.Text(
            right, wrap="word", borderwidth=1, relief="solid", **text_widget_colors(self)
        )
        self.preview.pack(fill="both", expand=True)

    def configure_tree_headings(self) -> None:
        labels = {
            "name": "Nome",
            "type": "Tipo",
            "size": "Dimensione",
            "files": "File",
            "dirs": "Dir",
            "path": "Percorso",
        }
        arrow = " v" if self.sort_reverse else " ^"
        self.tree.heading(
            "#0",
            text=labels["name"] + (arrow if self.sort_column == "name" else ""),
            command=lambda: self.sort_by("name"),
        )
        for column in ("type", "size", "files", "dirs", "path"):
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
        self.configure_tree_headings()
        self.sort_all_tree_levels()

    def reset_sort(self) -> None:
        self.sort_column = "name"
        self.sort_reverse = False
        self.configure_tree_headings()
        self.sort_all_tree_levels()

    def sort_key(self, iid: str):
        stat = self.item_stats.get(iid)
        text = self.tree.item(iid, "text") or ""
        values = self.tree.item(iid, "values") or ("", "", 0, 0, "")

        if self.sort_column == "name":
            return str(text).lower()
        if self.sort_column == "type":
            return str(values[0]).lower()
        if self.sort_column == "size":
            return stat.bytes if stat is not None else -1
        if self.sort_column == "files":
            return stat.files if stat is not None else -1
        if self.sort_column == "dirs":
            return stat.dirs if stat is not None else -1
        if self.sort_column == "path":
            return str(values[4]).lower() if len(values) > 4 else ""
        return str(text).lower()

    def sort_children(self, parent: str) -> None:
        children = list(self.tree.get_children(parent))
        children.sort(key=self.sort_key, reverse=self.sort_reverse)
        for index, iid in enumerate(children):
            self.tree.move(iid, parent, index)
            self.sort_children(iid)

    def sort_all_tree_levels(self) -> None:
        self.sort_children("")

    def clear_metrics(self) -> None:
        for child in self.metric_frame.winfo_children():
            child.destroy()

    def add_metric(self, title: str, value: str, note: str) -> None:
        card = ttk.Frame(self.metric_frame, style="Panel.TFrame", padding=10)
        card.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ttk.Label(card, text=title, style="MetricName.TLabel").pack(anchor="w")
        ttk.Label(card, text=value, style="Metric.TLabel").pack(anchor="w", pady=(4, 0))
        ttk.Label(card, text=note, style="MetricName.TLabel", wraplength=220).pack(
            anchor="w", pady=(4, 0)
        )

    def refresh(self) -> None:
        self.session = self.session_loader()
        root_stats = scan_tree(self.root_dir)
        project_stats = scan_tree(self.project_dir)
        renders_stats = scan_tree(Path(self.wf.RENDERS_DIR))
        output_stats = scan_tree(Path(self.wf.OUTPUT_DIR))

        outside_stats = []
        for child in immediate_children_stats(self.root_dir):
            try:
                if child.path.resolve(strict=False) == self.project_dir.resolve(strict=False):
                    continue
            except Exception:
                pass
            outside_stats.append(child)

        outside_bytes = sum(item.bytes for item in outside_stats)
        outside_files = sum(item.files for item in outside_stats)

        self.clear_metrics()
        self.add_metric("Blender root", human_bytes(root_stats.bytes), str(self.root_dir))
        self.add_metric("Project", human_bytes(project_stats.bytes), str(self.project_dir.name))
        self.add_metric(
            "Fuori dal progetto",
            human_bytes(outside_bytes),
            f"{len(outside_stats)} cartelle/file | {outside_files} file",
        )
        self.add_metric("Renders", human_bytes(renders_stats.bytes), str(self.wf.RENDERS_DIR))
        self.add_metric("Output dati", human_bytes(output_stats.bytes), str(self.wf.OUTPUT_DIR))

        self.item_stats.clear()
        self.tree.delete(*self.tree.get_children())
        root_id = self.insert_stat("", root_stats, "blender-root")
        project_id = self.insert_stat(root_id, project_stats, "project")

        outside_id = self.insert_group(
            root_id,
            "Contenuto in blender fuori da blender-audio-project",
            human_bytes(outside_bytes),
            outside_files,
            sum(item.dirs for item in outside_stats),
            self.root_dir,
        )
        for item in outside_stats:
            self.insert_stat(outside_id, item, "external")

        generated_id = self.insert_group(
            project_id, "Artefatti sessione corrente", "", "", "", None
        )
        for key, value in self.session.artifacts.items():
            path = safe_path(value)
            if path is None:
                continue
            if path.exists():
                stat = scan_tree(path)
            else:
                stat = PathStats(key, path, False, 0, 0, 0, tuple())
            self.insert_stat(generated_id, stat, key)

        self.tree.item(root_id, open=True)
        self.tree.item(project_id, open=True)
        self.tree.item(outside_id, open=True)
        self.tree.item(generated_id, open=True)
        self.sort_all_tree_levels()
        self.write_preview(
            build_overview_text(
                self.root_dir,
                self.project_dir,
                root_stats,
                project_stats,
                outside_stats,
            )
        )

    def insert_group(
        self, parent: str, label: str, size: str, files, dirs, path: Path | None
    ) -> str:
        iid = self.tree.insert(
            parent,
            "end",
            text=label,
            values=("group", size, files, dirs, str(path or "")),
            open=True,
        )
        self.item_stats[iid] = None
        return iid

    def insert_stat(self, parent: str, stat: PathStats, kind: str) -> str:
        type_name = "folder" if stat.path.is_dir() else "file"
        if not stat.exists:
            type_name = "missing"
        displayed_type = kind if kind not in {"project", "external", "blender-root"} else type_name
        iid = self.tree.insert(
            parent,
            "end",
            text=stat.name,
            values=(displayed_type, human_bytes(stat.bytes), stat.files, stat.dirs, str(stat.path)),
        )
        self.item_stats[iid] = stat
        return iid

    def preview_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        path_text = self.tree.set(selected[0], "path")
        if not path_text:
            return
        path = Path(path_text)
        self.selected_path = path
        if not path.exists():
            self.write_preview(f"Percorso mancante:\n{path}")
            return
        if path.is_dir():
            self.preview_directory(path)
            return
        self.preview_file(path)

    def preview_directory(self, path: Path) -> None:
        self.write_preview(build_directory_preview(path))

    def preview_file(self, path: Path) -> None:
        self.write_preview(build_file_preview(path))

    def write_preview(self, text: str) -> None:
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", text)
        self.preview.configure(state="normal")

    def open_path(self, path: Path) -> None:
        try:
            if not path.exists():
                raise FileNotFoundError(f"Percorso non trovato: {path}")
            os.startfile(str(path))  # type: ignore[attr-defined]
        except Exception as exc:
            messagebox.showerror("Open", str(exc))

    def open_selected(self) -> None:
        if self.selected_path is None:
            self.preview_selected()
        if self.selected_path is not None:
            self.open_path(self.selected_path)

    def open_selected_folder(self) -> None:
        if self.selected_path is None:
            self.preview_selected()
        if self.selected_path is None:
            return
        target = self.selected_path if self.selected_path.is_dir() else self.selected_path.parent
        self.open_path(target)

    def copy_selected_path(self) -> None:
        if self.selected_path is None:
            self.preview_selected()
        if self.selected_path is None:
            return
        self.clipboard_clear()
        self.clipboard_append(str(self.selected_path))
        self.write_preview(f"Percorso copiato negli appunti:\n{self.selected_path}")
