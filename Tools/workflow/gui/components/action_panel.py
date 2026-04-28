from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import tkinter as tk
from tkinter import ttk


@dataclass(frozen=True)
class ActionSpec:
    """Declarative GUI action entry.

    Add new workflow actions by appending one ActionSpec to the appropriate
    ActionGroup in workflow_gui_modern.py. The panel automatically creates the
    button, tooltip-like description row, scroll support and enabled/disabled
    bookkeeping.
    """

    label: str
    command: Callable[[], None]
    always_enabled: bool = False
    description: str = ""


@dataclass(frozen=True)
class ActionGroup:
    title: str
    actions: tuple[ActionSpec, ...]


class Tooltip:
    """Small delayed tooltip for Tk/ttk widgets."""

    def __init__(self, widget: tk.Widget, text: str, *, delay_ms: int = 650, wraplength: int = 360) -> None:
        self.widget = widget
        self.text = text.strip()
        self.delay_ms = delay_ms
        self.wraplength = wraplength
        self.after_id: str | None = None
        self.window: tk.Toplevel | None = None
        if self.text:
            widget.bind("<Enter>", self.schedule, add="+")
            widget.bind("<Leave>", self.hide, add="+")
            widget.bind("<ButtonPress>", self.hide, add="+")
            widget.bind("<Motion>", self.move, add="+")

    def schedule(self, event=None) -> None:
        self.cancel()
        self.after_id = self.widget.after(self.delay_ms, lambda: self.show(event))

    def cancel(self) -> None:
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def show(self, event=None) -> None:
        self.cancel()
        if self.window or not self.text:
            return
        x = self.widget.winfo_pointerx() + 14
        y = self.widget.winfo_pointery() + 18
        self.window = tk.Toplevel(self.widget)
        self.window.wm_overrideredirect(True)
        self.window.wm_geometry(f"+{x}+{y}")
        frame = ttk.Frame(self.window, relief="solid", borderwidth=1)
        frame.pack(fill="both", expand=True)
        label = ttk.Label(
            frame,
            text=self.text,
            justify="left",
            wraplength=self.wraplength,
            padding=(8, 5),
        )
        label.pack(fill="both", expand=True)

    def move(self, event=None) -> None:
        if self.window:
            x = self.widget.winfo_pointerx() + 14
            y = self.widget.winfo_pointery() + 18
            self.window.wm_geometry(f"+{x}+{y}")

    def hide(self, event=None) -> None:
        self.cancel()
        if self.window:
            self.window.destroy()
            self.window = None


class ScrollableFrame(ttk.Frame):
    """A vertical scrollable frame implemented with a Canvas.

    Tkinter/ttk has no native scrollable Frame. This component keeps the GUI
    usable on smaller screens and with future action groups.
    """

    def __init__(self, master, *, min_width: int = 320, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = ttk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.min_width = min_width

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.content.bind("<Configure>", self._on_content_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _on_content_configure(self, _event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event) -> None:
        width = max(event.width, self.min_width)
        self.canvas.itemconfigure(self.window_id, width=width)

    def _bind_mousewheel(self, _event) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self, _event) -> None:
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event) -> None:
        delta = -1 if event.num == 4 else 1
        self.canvas.yview_scroll(delta, "units")


class GroupedActionPanel(ttk.Frame):
    """Scrollable grouped button panel for workflow operations."""

    def __init__(self, master, *, title: str = "Operations", min_width: int = 340) -> None:
        super().__init__(master)
        self.title = title
        self.tooltips: list[Tooltip] = []
        header = ttk.Frame(self)
        header.pack(fill="x", padx=2, pady=(0, 6))
        ttk.Label(header, text=title, font=("TkDefaultFont", 11, "bold")).pack(side="left")

        self.scrollable = ScrollableFrame(self, min_width=min_width)
        self.scrollable.pack(fill="both", expand=True)

    def build(self, groups: tuple[ActionGroup, ...]) -> tuple[list[ttk.Button], list[ttk.Button]]:
        runtime_buttons: list[ttk.Button] = []
        always_enabled_buttons: list[ttk.Button] = []

        for group in groups:
            group_frame = ttk.LabelFrame(self.scrollable.content, text=group.title)
            group_frame.pack(fill="x", padx=4, pady=(0, 10))

            for spec in group.actions:
                row = ttk.Frame(group_frame)
                row.pack(fill="x", padx=8, pady=(6, 3))

                button = ttk.Button(row, text=spec.label, command=spec.command)
                button.pack(fill="x")

                if spec.description:
                    self.tooltips.append(Tooltip(button, spec.description))
                    description = ttk.Label(
                        row,
                        text=spec.description,
                        wraplength=300,
                        justify="left",
                        foreground="#666666",
                    )
                    description.pack(fill="x", pady=(2, 0))

                if spec.always_enabled:
                    always_enabled_buttons.append(button)
                else:
                    runtime_buttons.append(button)

        return runtime_buttons, always_enabled_buttons
