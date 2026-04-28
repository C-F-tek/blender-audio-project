from __future__ import annotations

from tkinter import ttk


class STTheme:
    """SpazioTempoRec-inspired dark/cyan/gold palette for Tkinter widgets."""

    bg = "#050816"
    panel = "#0A1024"
    panel_alt = "#101936"
    text = "#F3F6FF"
    muted = "#A8B3CF"
    cyan = "#00D5FF"
    cyan_soft = "#4BE4FF"
    gold = "#F4B942"
    purple = "#7C4DFF"
    danger = "#FF5C7A"
    ok = "#5CFFB1"
    border = "#1B2A55"


def apply_spaziotempo_theme(root) -> None:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    root.configure(bg=STTheme.bg)

    style.configure("TFrame", background=STTheme.bg)
    style.configure("Panel.TFrame", background=STTheme.panel)
    style.configure("AltPanel.TFrame", background=STTheme.panel_alt)
    style.configure("TLabel", background=STTheme.bg, foreground=STTheme.text)
    style.configure("Muted.TLabel", background=STTheme.bg, foreground=STTheme.muted)
    style.configure("Header.TLabel", background=STTheme.bg, foreground=STTheme.cyan, font=("TkDefaultFont", 15, "bold"))
    style.configure("SubHeader.TLabel", background=STTheme.bg, foreground=STTheme.muted)
    style.configure("Metric.TLabel", background=STTheme.panel, foreground=STTheme.gold, font=("TkDefaultFont", 13, "bold"))
    style.configure("MetricName.TLabel", background=STTheme.panel, foreground=STTheme.muted)

    style.configure("TButton", padding=(9, 6), background=STTheme.panel_alt, foreground=STTheme.text)
    style.map("TButton", background=[("active", STTheme.border)], foreground=[("active", STTheme.cyan_soft)])

    style.configure("TLabelframe", background=STTheme.panel, foreground=STTheme.text, bordercolor=STTheme.border)
    style.configure("TLabelframe.Label", background=STTheme.panel, foreground=STTheme.gold, font=("TkDefaultFont", 10, "bold"))

    style.configure("TNotebook", background=STTheme.bg, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(12, 6), background=STTheme.panel_alt, foreground=STTheme.muted)
    style.map("TNotebook.Tab", background=[("selected", STTheme.border)], foreground=[("selected", STTheme.cyan)])

    style.configure(
        "Treeview",
        background=STTheme.panel,
        fieldbackground=STTheme.panel,
        foreground=STTheme.text,
        bordercolor=STTheme.border,
        rowheight=24,
    )
    style.configure("Treeview.Heading", background=STTheme.panel_alt, foreground=STTheme.gold, font=("TkDefaultFont", 9, "bold"))
    style.map("Treeview", background=[("selected", STTheme.border)], foreground=[("selected", STTheme.cyan_soft)])

    style.configure("Vertical.TScrollbar", background=STTheme.panel_alt, troughcolor=STTheme.bg)
