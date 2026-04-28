from __future__ import annotations

import json
import os
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Any

from components.st_theme import STTheme, apply_spaziotempo_theme


@dataclass(frozen=True)
class PathStats:
    name: str
    path: Path
    exists: bool
    bytes: int
    files: int
    dirs: int
    sample: tuple[Path, ...]


def human_bytes(size: int | float) -> str:
    value = float(size or 0)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024.0 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024.0
    return f"{value:.1f} TB"


def scan_tree(path: Path, *, sample_limit: int = 24) -> PathStats:
    path = Path(path).expanduser()
    if not path.exists():
        return PathStats(path.name or str(path), path, False, 0, 0, 0, tuple())

    total_bytes = 0
    files = 0
    dirs = 0
    sample: list[Path] = []

    if path.is_file():
        return PathStats(path.name, path, True, path.stat().st_size, 1, 0, (path,))

    stack = [path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    try:
                        entry_path = Path(entry.path)
                        if entry.is_dir(follow_symlinks=False):
                            dirs += 1
                            if len(sample) < sample_limit:
                                sample.append(entry_path)
                            stack.append(entry_path)
                        elif entry.is_file(follow_symlinks=False):
                            files += 1
                            stat = entry.stat(follow_symlinks=False)
                            total_bytes += stat.st_size
                            if len(sample) < sample_limit:
                                sample.append(entry_path)
                    except OSError:
                        continue
        except OSError:
            continue

    return PathStats(path.name or str(path), path, True, total_bytes, files, dirs, tuple(sample))


def immediate_children_stats(path: Path) -> list[PathStats]:
    path = Path(path).expanduser()
    if not path.exists() or not path.is_dir():
        return []
    children = []
    for child in sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
        children.append(scan_tree(child))
    return children


def safe_path(value: Any) -> Path | None:
    if isinstance(value, str) and value.strip():
        return Path(value).expanduser()
    return None


class StorageDashboardWindow(tk.Toplevel):
    """Themed project/storage dashboard focused on the Blender workspace root."""

    def __init__(self, master: tk.Tk, *, session_loader, workflow_state_module) -> None:
        super().__init__(master)
        self.session_loader = session_loader
        self.wf = workflow_state_module
        self.session = self.session_loader()
        self.root_dir = Path(self.wf.ROOT).expanduser()
        self.project_dir = Path(self.wf.PROJECT_DIR).expanduser()
        self.selected_path: Path | None = None

        self.title("Spaziotempo Storage Dashboard")
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
            text="Focus: cartella blender, progetto e artefatti generati",
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

        self.tree = ttk.Treeview(left, columns=("type", "size", "files", "dirs", "path"), show="tree headings")
        self.tree.heading("#0", text="Nome")
        self.tree.heading("type", text="Tipo")
        self.tree.heading("size", text="Dimensione")
        self.tree.heading("files", text="File")
        self.tree.heading("dirs", text="Dir")
        self.tree.heading("path", text="Percorso")
        self.tree.column("#0", width=250)
        self.tree.column("type", width=90)
        self.tree.column("size", width=95, anchor="e")
        self.tree.column("files", width=70, anchor="e")
        self.tree.column("dirs", width=70, anchor="e")
        self.tree.column("path", width=460)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", lambda _event: self.preview_selected())
        self.tree.bind("<Double-1>", lambda _event: self.open_selected())

        tree_scroll = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="right", fill="y")

        toolbar = ttk.Frame(right)
        toolbar.pack(fill="x", pady=(0, 6))
        ttk.Button(toolbar, text="Open selected", command=self.open_selected).pack(side="left")
        ttk.Button(toolbar, text="Open folder", command=self.open_selected_folder).pack(side="left", padx=(8, 0))
        ttk.Button(toolbar, text="Copy path", command=self.copy_selected_path).pack(side="left", padx=(8, 0))

        self.preview = tk.Text(
            right,
            wrap="word",
            background=STTheme.panel,
            foreground=STTheme.text,
            insertbackground=STTheme.cyan,
            borderwidth=1,
            relief="solid",
        )
        self.preview.pack(fill="both", expand=True)

    def clear_metrics(self) -> None:
        for child in self.metric_frame.winfo_children():
            child.destroy()

    def add_metric(self, title: str, value: str, note: str) -> None:
        card = ttk.Frame(self.metric_frame, style="Panel.TFrame", padding=10)
        card.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ttk.Label(card, text=title, style="MetricName.TLabel").pack(anchor="w")
        ttk.Label(card, text=value, style="Metric.TLabel").pack(anchor="w", pady=(4, 0))
        ttk.Label(card, text=note, style="MetricName.TLabel", wraplength=220).pack(anchor="w", pady=(4, 0))

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
        self.add_metric("Fuori dal progetto", human_bytes(outside_bytes), f"{len(outside_stats)} cartelle/file | {outside_files} file")
        self.add_metric("Renders", human_bytes(renders_stats.bytes), str(self.wf.RENDERS_DIR))
        self.add_metric("Output dati", human_bytes(output_stats.bytes), str(self.wf.OUTPUT_DIR))

        self.tree.delete(*self.tree.get_children())
        root_id = self.insert_stat("", root_stats, "blender-root")
        project_id = self.insert_stat(root_id, project_stats, "project")

        outside_id = self.tree.insert(
            root_id,
            "end",
            text="Contenuto in blender fuori da blender-audio-project",
            values=("group", human_bytes(outside_bytes), outside_files, sum(item.dirs for item in outside_stats), str(self.root_dir)),
            open=True,
        )
        for item in outside_stats:
            self.insert_stat(outside_id, item, "external")

        generated_id = self.tree.insert(project_id, "end", text="Artefatti sessione corrente", values=("group", "", "", "", ""), open=True)
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
        self.write_preview(self.build_overview_text(root_stats, project_stats, outside_stats))

    def insert_stat(self, parent: str, stat: PathStats, kind: str) -> str:
        type_name = "folder" if stat.path.is_dir() else "file"
        if not stat.exists:
            type_name = "missing"
        iid = self.tree.insert(
            parent,
            "end",
            text=stat.name,
            values=(type_name, human_bytes(stat.bytes), stat.files, stat.dirs, str(stat.path)),
        )
        self.tree.set(iid, "type", kind if kind not in {"project", "external", "blender-root"} else type_name)
        return iid

    def build_overview_text(self, root_stats: PathStats, project_stats: PathStats, outside_stats: list[PathStats]) -> str:
        lines = [
            "SPAZIOTEMPOREC STORAGE OVERVIEW",
            "=" * 80,
            f"Blender root: {self.root_dir}",
            f"Project dir:  {self.project_dir}",
            "",
            f"Root totale:     {human_bytes(root_stats.bytes)} | files={root_stats.files} dirs={root_stats.dirs}",
            f"Project totale:  {human_bytes(project_stats.bytes)} | files={project_stats.files} dirs={project_stats.dirs}",
            "",
            "Elementi dentro blender ma fuori da blender-audio-project:",
        ]
        if not outside_stats:
            lines.append("  Nessun elemento rilevato fuori dal progetto.")
        for item in outside_stats[:60]:
            lines.append(
                f"  - {item.path.name}: {human_bytes(item.bytes)} | files={item.files} dirs={item.dirs} | {item.path}"
            )
        if len(outside_stats) > 60:
            lines.append(f"  ... altri {len(outside_stats) - 60} elementi")
        lines.extend([
            "",
            "Doppio click su una riga per aprire file/cartella.",
            "Usa Open folder per aprire la cartella che contiene il file selezionato.",
        ])
        return "\n".join(lines)

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
            children = immediate_children_stats(path)
            lines = [f"Cartella: {path}", f"Elementi diretti: {len(children)}", ""]
            for child in children[:120]:
                lines.append(f"{child.path.name:<42} {human_bytes(child.bytes):>10} files={child.files:<6} dirs={child.dirs:<6}")
            if len(children) > 120:
                lines.append(f"... altri {len(children) - 120} elementi")
            self.write_preview("\n".join(lines))
            return

        suffix = path.suffix.lower()
        if suffix in {".json", ".md", ".txt", ".py", ".log", ".jsonl", ".csv"}:
            try:
                raw = path.read_text(encoding="utf-8", errors="replace")
                if suffix == ".json":
                    try:
                        raw = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
                    except Exception:
                        pass
                self.write_preview(raw[:100000] + ("\n\n<preview troncata>" if len(raw) > 100000 else ""))
            except Exception as exc:
                self.write_preview(f"Errore lettura file:\n{path}\n\n{exc}")
        else:
            self.write_preview(f"File: {path}\nDimensione: {human_bytes(path.stat().st_size)}\n\nDoppio click/Open per aprire esternamente.")

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
