from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class STTheme:
    """System-theme compatible color aliases.

    These constants intentionally map to Tk/Windows system colors instead of a
    custom palette. The GUI follows the active operating-system theme as much as
    Tkinter can expose it.
    """

    bg = "SystemButtonFace"
    panel = "SystemWindow"
    panel_alt = "SystemButtonFace"
    text = "SystemWindowText"
    muted = "SystemGrayText"
    cyan = "SystemHighlight"
    cyan_soft = "SystemHighlight"
    gold = "SystemHotlight"
    purple = "SystemHighlight"
    danger = "red"
    ok = "green"
    border = "SystemInactiveBorder"


def system_color(root, name: str, fallback: str) -> str:
    try:
        root.winfo_rgb(name)
        return name
    except Exception:
        return fallback


def apply_system_theme(root) -> None:
    """Apply the active system look without forcing a specific ttk theme.

    Important: this function does not call theme_use('clam'), 'vista', or any
    other fixed theme. It preserves the current/default Tk theme and configures
    only safe named styles using Windows/Tk system colors.
    """

    style = ttk.Style(root)
    current_theme = style.theme_use()
    try:
        style.theme_use(current_theme)
    except tk.TclError:
        pass

    button_face = system_color(root, "SystemButtonFace", "#F0F0F0")
    window = system_color(root, "SystemWindow", "#FFFFFF")
    text = system_color(root, "SystemWindowText", "#000000")
    gray_text = system_color(root, "SystemGrayText", "#666666")
    highlight = system_color(root, "SystemHighlight", "#0078D7")
    highlight_text = system_color(root, "SystemHighlightText", "#FFFFFF")

    try:
        root.configure(bg=button_face)
    except Exception:
        pass

    # Use named styles only. Native ttk widgets still keep their platform look.
    style.configure("Panel.TFrame", background=button_face)
    style.configure("AltPanel.TFrame", background=button_face)
    style.configure("Muted.TLabel", foreground=gray_text)
    style.configure("Header.TLabel", foreground=text, font=("Segoe UI", 15, "bold"))
    style.configure("SubHeader.TLabel", foreground=gray_text)
    style.configure("Metric.TLabel", foreground=text, font=("Segoe UI", 12, "bold"))
    style.configure("MetricName.TLabel", foreground=gray_text)
    style.configure("TButton", padding=(9, 5))
    style.configure("TLabelframe.Label", font=("Segoe UI", 9, "bold"))
    style.configure("TNotebook.Tab", padding=(12, 5))
    style.configure("Treeview", background=window, fieldbackground=window, foreground=text, rowheight=24)
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
    style.map("Treeview", background=[("selected", highlight)], foreground=[("selected", highlight_text)])


def text_widget_colors(root) -> dict[str, str]:
    return {
        "background": system_color(root, "SystemWindow", "#FFFFFF"),
        "foreground": system_color(root, "SystemWindowText", "#000000"),
        "insertbackground": system_color(root, "SystemWindowText", "#000000"),
        "selectbackground": system_color(root, "SystemHighlight", "#0078D7"),
        "selectforeground": system_color(root, "SystemHighlightText", "#FFFFFF"),
    }


# Backward-compatible name used by existing GUI modules.
def apply_spaziotempo_theme(root) -> None:
    apply_system_theme(root)
