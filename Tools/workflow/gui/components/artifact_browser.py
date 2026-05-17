from __future__ import annotations

import json
import os
import platform
import subprocess
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Any

from components.st_theme import text_widget_colors

TEXT_EXTENSIONS = {".json", ".md", ".txt", ".py", ".log", ".jsonl", ".csv"}
IMAGE_EXTENSIONS = {".png", ".gif", ".ppm", ".pgm"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".aac", ".m4a"}


@dataclass(frozen=True)
class ArtifactItem:
    key: str
    path: Path
    category: str
    exists: bool
    size: int

    @property
    def suffix(self) -> str:
        return self.path.suffix.lower()


def human_bytes(size: int | float) -> str:
    value = float(size or 0)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024.0 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024.0
    return f"{value:.1f} TB"


def classify_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    if suffix in AUDIO_EXTENSIONS:
        return "audio"
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in TEXT_EXTENSIONS:
        return "text"
    if path.is_dir():
        return "folder"
    return "file"


def open_external(path: Path) -> None:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Percorso non trovato: {path}")

    system = platform.system().lower()
    if system == "windows":
        os.startfile(str(path))  # type: ignore[attr-defined]
    elif system == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


def collect_session_artifacts(
    session: Any, extra_roots: list[Path] | None = None
) -> list[ArtifactItem]:
    items: list[ArtifactItem] = []
    seen: set[str] = set()

    def add_item(key: str, raw_path: str | Path | None) -> None:
        if not raw_path:
            return
        path = Path(raw_path).expanduser()
        marker = str(path.resolve(strict=False)).lower()
        if marker in seen:
            return
        seen.add(marker)
        exists = path.exists()
        size = path.stat().st_size if exists and path.is_file() else 0
        items.append(
            ArtifactItem(
                key=key,
                path=path,
                category=classify_path(path),
                exists=exists,
                size=size,
            )
        )

    for key, value in getattr(session, "artifacts", {}).items():
        if isinstance(value, str):
            add_item(key, value)

    for root in extra_roots or []:
        root = Path(root).expanduser()
        if not root.exists():
            continue
        for pattern in ("*.json", "*.md", "*.txt", "*.png", "*.mp4", "*.mov", "*.mkv", "*.wav"):
            for path in root.glob(pattern):
                add_item(f"scan:{path.name}", path)

    return sorted(items, key=lambda item: (not item.exists, item.category, item.key.lower()))


class ArtifactBrowserWindow(tk.Toplevel):
    """Browse and inspect generated workflow artifacts."""

    SORT_COLUMNS = ("status", "category", "key", "size", "path")

    def __init__(self, master: tk.Tk, *, session_loader, extra_roots_loader=None) -> None:
        super().__init__(master)
        self.session_loader = session_loader
        self.extra_roots_loader = extra_roots_loader
        self.items: list[ArtifactItem] = []
        self.filtered_items: list[ArtifactItem] = []
        self.image_ref: tk.PhotoImage | None = None
        self.filter_var = tk.StringVar(value="all")
        self.search_var = tk.StringVar(value="")
        self.sort_column = "key"
        self.sort_reverse = False

        self.title("Artifact Browser")
        self.geometry("1220x780")
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.build_layout()
        self.refresh()

    def build_layout(self) -> None:
        root = ttk.Frame(self, padding=8)
        root.pack(fill="both", expand=True)

        toolbar = ttk.Frame(root)
        toolbar.pack(fill="x", pady=(0, 6))
        ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(side="left")
        ttk.Button(toolbar, text="Open", command=self.open_selected).pack(side="left", padx=(6, 0))
        ttk.Button(toolbar, text="Open folder", command=self.open_selected_folder).pack(
            side="left", padx=(6, 0)
        )
        ttk.Button(toolbar, text="Sort reset", command=self.reset_sort).pack(
            side="left", padx=(6, 0)
        )
        ttk.Button(toolbar, text="Hide", command=self.hide).pack(side="right")

        ttk.Label(toolbar, text="Filter").pack(side="left", padx=(14, 4))
        filter_box = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=["all", "video", "audio", "image", "text", "folder", "missing"],
            width=10,
            state="readonly",
        )
        filter_box.pack(side="left")
        filter_box.bind("<<ComboboxSelected>>", lambda _event: self.apply_filter())

        ttk.Label(toolbar, text="Search").pack(side="left", padx=(14, 4))
        search = ttk.Entry(toolbar, textvariable=self.search_var, width=32)
        search.pack(side="left")
        search.bind("<KeyRelease>", lambda _event: self.apply_filter())

        panes = ttk.PanedWindow(root, orient="horizontal")
        panes.pack(fill="both", expand=True)

        left = ttk.Frame(panes)
        right = ttk.Frame(panes)
        panes.add(left, weight=1)
        panes.add(right, weight=2)

        columns = ("status", "category", "key", "size", "path")
        self.tree = ttk.Treeview(left, columns=columns, show="headings", height=28)
        for column, width in [
            ("status", 78),
            ("category", 88),
            ("key", 230),
            ("size", 96),
            ("path", 460),
        ]:
            self.tree.column(column, width=width, anchor="e" if column == "size" else "w")
        self.configure_headings()
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", lambda _event: self.preview_selected())
        self.tree.bind("<Double-1>", lambda _event: self.open_selected())

        yscroll = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side="right", fill="y")

        self.preview_title = ttk.Label(right, text="Preview", font=("TkDefaultFont", 11, "bold"))
        self.preview_title.pack(anchor="w", pady=(0, 6))

        self.preview = tk.Text(right, wrap="none", **text_widget_colors(self))
        self.preview.pack(fill="both", expand=True)

        self.preview_scroll = ttk.Scrollbar(
            self.preview, orient="vertical", command=self.preview.yview
        )
        self.preview.configure(yscrollcommand=self.preview_scroll.set)
        self.preview_scroll.pack(side="right", fill="y")

    def configure_headings(self) -> None:
        labels = {
            "status": "STATO",
            "category": "TIPO",
            "key": "CHIAVE",
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

    def sort_key(self, item: ArtifactItem):
        if self.sort_column == "status":
            return 0 if item.exists else 1
        if self.sort_column == "category":
            return item.category.lower()
        if self.sort_column == "key":
            return item.key.lower()
        if self.sort_column == "size":
            return item.size
        if self.sort_column == "path":
            return str(item.path).lower()
        return item.key.lower()

    def hide(self) -> None:
        self.withdraw()

    def show(self) -> None:
        self.deiconify()
        self.lift()
        self.refresh()

    def refresh(self) -> None:
        try:
            session = self.session_loader()
            extra_roots = self.extra_roots_loader(session) if self.extra_roots_loader else []
            self.items = collect_session_artifacts(session, extra_roots=extra_roots)
            self.apply_filter()
        except Exception as exc:
            messagebox.showerror("Artifact browser", str(exc))

    def apply_filter(self) -> None:
        category_filter = self.filter_var.get()
        query = self.search_var.get().strip().lower()
        self.filtered_items = []
        for item in self.items:
            if category_filter == "missing" and item.exists:
                continue
            if category_filter not in {"all", "missing"} and item.category != category_filter:
                continue
            haystack = f"{item.key} {item.path} {item.category}".lower()
            if query and query not in haystack:
                continue
            self.filtered_items.append(item)

        self.filtered_items.sort(key=self.sort_key, reverse=self.sort_reverse)
        self.tree.delete(*self.tree.get_children())
        for index, item in enumerate(self.filtered_items):
            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    "OK" if item.exists else "MISSING",
                    item.category,
                    item.key,
                    human_bytes(item.size),
                    str(item.path),
                ),
            )
        self.write_preview(
            f"{len(self.filtered_items)} artefatti visualizzati su {len(self.items)} totali. Clicca sulle intestazioni per ordinare."
        )

    def selected_item(self) -> ArtifactItem | None:
        selected = self.tree.selection()
        if not selected:
            return None
        index = int(selected[0])
        if 0 <= index < len(self.filtered_items):
            return self.filtered_items[index]
        return None

    def preview_selected(self) -> None:
        item = self.selected_item()
        if item is None:
            return
        self.preview_title.configure(text=f"{item.category.upper()} | {item.key}")
        if not item.exists:
            self.write_preview(f"Percorso mancante:\n{item.path}")
            return
        if item.category == "text":
            self.preview_text_file(item.path)
        elif item.category == "image":
            self.preview_image_file(item.path)
        elif item.category == "video":
            self.write_preview(
                "Video disponibile. Usa Open per aprirlo nel player di sistema.\n\n"
                f"File: {item.path}\nSize: {human_bytes(item.size)}"
            )
        elif item.category == "audio":
            self.write_preview(
                "Audio disponibile. Usa Open per aprirlo nel player/editor di sistema.\n\n"
                f"File: {item.path}\nSize: {human_bytes(item.size)}"
            )
        elif item.category == "folder":
            self.write_preview_folder(item.path)
        else:
            self.write_preview(f"File: {item.path}\nSize: {human_bytes(item.size)}")

    def write_preview(self, text: str) -> None:
        self.image_ref = None
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", text)
        self.preview.configure(state="normal")

    def preview_text_file(self, path: Path, max_chars: int = 90000) -> None:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
            if path.suffix.lower() == ".json":
                try:
                    raw = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
                except Exception:
                    pass
            if len(raw) > max_chars:
                raw = raw[:max_chars] + "\n\n<preview troncata>"
            self.write_preview(raw)
        except Exception as exc:
            self.write_preview(f"Errore lettura file:\n{path}\n\n{exc}")

    def preview_image_file(self, path: Path) -> None:
        try:
            image = tk.PhotoImage(file=str(path))
            self.image_ref = image
            self.preview.configure(state="normal")
            self.preview.delete("1.0", "end")
            self.preview.image_create("1.0", image=image)
            self.preview.insert(
                "end",
                f"\n\n{path}\n{image.width()}x{image.height()} px | {human_bytes(path.stat().st_size)}",
            )
        except Exception as exc:
            self.write_preview(
                "Preview immagine non disponibile in Tk per questo file. Usa Open per aprirlo esternamente.\n\n"
                f"{path}\n\n{exc}"
            )

    def write_preview_folder(self, path: Path, max_items: int = 120) -> None:
        try:
            entries = sorted(
                path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())
            )
            lines = [f"Cartella: {path}", f"Elementi: {len(entries)}", ""]
            for entry in entries[:max_items]:
                kind = "DIR " if entry.is_dir() else "FILE"
                size = "" if entry.is_dir() else f" {human_bytes(entry.stat().st_size)}"
                lines.append(f"{kind} {entry.name}{size}")
            if len(entries) > max_items:
                lines.append(f"... altri {len(entries) - max_items} elementi")
            self.write_preview("\n".join(lines))
        except Exception as exc:
            self.write_preview(f"Errore lettura cartella:\n{path}\n\n{exc}")

    def open_selected(self) -> None:
        item = self.selected_item()
        if item is None:
            messagebox.showinfo("Open", "Seleziona un artefatto.")
            return
        try:
            open_external(item.path)
        except Exception as exc:
            messagebox.showerror("Open", str(exc))

    def open_selected_folder(self) -> None:
        item = self.selected_item()
        if item is None:
            messagebox.showinfo("Open folder", "Seleziona un artefatto.")
            return
        target = item.path if item.path.is_dir() else item.path.parent
        try:
            open_external(target)
        except Exception as exc:
            messagebox.showerror("Open folder", str(exc))
