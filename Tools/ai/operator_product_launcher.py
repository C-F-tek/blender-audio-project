#!/usr/bin/env python3
"""Tkinter operator launcher for heap final-product review/apply workflow."""

from __future__ import annotations

import json
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

try:
    from tools.ai.operator_product_launcher_core import (
        DEFAULT_PROFILE,
        LauncherConfig,
        analyze_code_product,
        build_heap_command,
        profile_names,
        resolve_config,
        run_dir_for,
        run_heap,
        select_profile,
    )
except ImportError:  # pragma: no cover
    import sys

    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.operator_product_launcher_core import (  # type: ignore
        DEFAULT_PROFILE,
        LauncherConfig,
        analyze_code_product,
        build_heap_command,
        profile_names,
        resolve_config,
        run_dir_for,
        run_heap,
        select_profile,
    )


class OperatorLauncherApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("IA-Carmine Operator Product Launcher")
        self.messages: queue.Queue[str] = queue.Queue()
        cwd = Path.cwd()
        self.repo_root = tk.StringVar(value=str(cwd))
        self.request_file = tk.StringVar(value=str(cwd / "docs" / "README.md"))
        self.intermediate_root = tk.StringVar(
            value=str(cwd / "output" / "validation" / "operator_product_launcher")
        )
        self.final_root = tk.StringVar(value=str(Path.home() / "Documents"))
        self.python_exe = tk.StringVar(value=str(cwd / ".venv" / "Scripts" / "python.exe"))
        self.profile = tk.StringVar(value=DEFAULT_PROFILE)
        self.stamp = tk.StringVar(value="")
        self.startup_max_memory_chars = tk.StringVar(value="")
        self.startup_max_context_files = tk.StringVar(value="")
        self.startup_scan_context_files = tk.StringVar(value="")
        self.startup_max_chars_per_file = tk.StringVar(value="")
        self.code_product = tk.StringVar(value="")
        self.last_report: dict[str, Any] = {}
        self._build()
        self._load_profiles()
        self._poll_messages()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for row, (label, variable, kind) in enumerate(
            [
                ("Repo dir", self.repo_root, "dir"),
                ("Input MD", self.request_file, "file"),
                ("Intermediate dir", self.intermediate_root, "dir"),
                ("Final output dir", self.final_root, "dir"),
                ("Python exe", self.python_exe, "file"),
                ("Code product", self.code_product, "file"),
            ]
        ):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
            ttk.Entry(frame, textvariable=variable, width=88).grid(
                row=row, column=1, sticky="ew", pady=2
            )
            ttk.Button(
                frame, text="...", width=3, command=lambda v=variable, k=kind: self._browse(v, k)
            ).grid(row=row, column=2, padx=4)
        ttk.Label(frame, text="Intensity").grid(row=6, column=0, sticky="w", pady=2)
        self.profile_combo = ttk.Combobox(
            frame, textvariable=self.profile, width=40, state="readonly"
        )
        self.profile_combo.grid(row=6, column=1, sticky="w", pady=2)
        self.profile_combo.bind(
            "<<ComboboxSelected>>", lambda _event: self._sync_profile_defaults()
        )
        for row, (label, variable) in enumerate(
            [
                ("Memory chars", self.startup_max_memory_chars),
                ("Context files", self.startup_max_context_files),
                ("Scan files", self.startup_scan_context_files),
                ("Chars per file", self.startup_max_chars_per_file),
            ],
            start=7,
        ):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
            ttk.Entry(frame, textvariable=variable, width=18).grid(
                row=row, column=1, sticky="w", pady=2
            )
        ttk.Label(frame, text="Stamp").grid(row=11, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=self.stamp, width=40).grid(
            row=11, column=1, sticky="w", pady=2
        )
        buttons = ttk.Frame(frame)
        buttons.grid(row=12, column=0, columnspan=3, sticky="ew", pady=8)
        ttk.Button(buttons, text="Build Command", command=self.build_command).pack(
            side="left", padx=3
        )
        ttk.Button(buttons, text="Run Full", command=self.run_full).pack(side="left", padx=3)
        ttk.Button(buttons, text="Review Code Product", command=self.review_code_product).pack(
            side="left", padx=3
        )
        ttk.Button(buttons, text="Apply Safe", command=self.apply_safe).pack(side="left", padx=3)
        self.log = tk.Text(frame, height=24, width=110, wrap="word")
        self.log.grid(row=13, column=0, columnspan=3, sticky="nsew")
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(13, weight=1)

    def _browse(self, variable: tk.StringVar, kind: str) -> None:
        value = filedialog.askdirectory() if kind == "dir" else filedialog.askopenfilename()
        if value:
            variable.set(value)

    def _load_profiles(self) -> None:
        try:
            names = profile_names(Path(self.repo_root.get()))
            self.profile_combo["values"] = names
            if self.profile.get() not in names and names:
                self.profile.set(names[0])
            self._sync_profile_defaults()
        except Exception as exc:  # noqa: BLE001
            self._log(f"Profile load failed: {type(exc).__name__}: {exc}")

    def _sync_profile_defaults(self) -> None:
        try:
            profile = select_profile(Path(self.repo_root.get()), self.profile.get())
            values = {
                self.startup_max_memory_chars: profile.get("startup_max_memory_chars"),
                self.startup_max_context_files: profile.get("startup_max_context_files"),
                self.startup_scan_context_files: profile.get("startup_scan_context_files"),
                self.startup_max_chars_per_file: profile.get("startup_max_chars_per_file"),
            }
            for variable, value in values.items():
                variable.set("" if value in (None, "") else str(value))
        except Exception as exc:  # noqa: BLE001
            self._log(f"Profile default sync failed: {type(exc).__name__}: {exc}")

    def _int_field(self, label: str, variable: tk.StringVar) -> int | None:
        raw = variable.get().strip()
        if not raw:
            return None
        value = int(raw)
        if value <= 0:
            raise ValueError(f"{label} must be greater than zero")
        return value

    def profile_overrides(self) -> dict[str, int]:
        fields = {
            "startup_max_memory_chars": ("Memory chars", self.startup_max_memory_chars),
            "startup_max_context_files": ("Context files", self.startup_max_context_files),
            "startup_scan_context_files": ("Scan files", self.startup_scan_context_files),
            "startup_max_chars_per_file": ("Chars per file", self.startup_max_chars_per_file),
        }
        overrides: dict[str, int] = {}
        for key, (label, variable) in fields.items():
            value = self._int_field(label, variable)
            if value is not None:
                overrides[key] = value
        return overrides

    def config(self) -> LauncherConfig:
        return LauncherConfig(
            repo_root=Path(self.repo_root.get()),
            request_file=Path(self.request_file.get()),
            intermediate_root=Path(self.intermediate_root.get()),
            final_root=Path(self.final_root.get()),
            profile_name=self.profile.get(),
            python_exe=self.python_exe.get(),
            stamp=self.stamp.get(),
            profile_overrides=self.profile_overrides(),
        )

    def _log(self, text: str) -> None:
        self.log.insert("end", text.rstrip() + "\n")
        self.log.see("end")

    def _poll_messages(self) -> None:
        while not self.messages.empty():
            self._log(self.messages.get())
        self.root.after(250, self._poll_messages)

    def worker(self, label: str, func: Any) -> None:
        def run() -> None:
            self.messages.put(f"[{label}] started")
            try:
                data = func()
                self.last_report = data if isinstance(data, dict) else {}
                self.messages.put(json.dumps(data, indent=2, ensure_ascii=False)[-8000:])
                self.messages.put(f"[{label}] done")
            except Exception as exc:  # noqa: BLE001
                self.messages.put(f"[{label}] failed: {type(exc).__name__}: {exc}")

        threading.Thread(target=run, daemon=True).start()

    def build_command(self) -> None:
        try:
            command = build_heap_command(self.config())
            self._log(json.dumps({"command": command}, indent=2, ensure_ascii=False))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Build command failed", f"{type(exc).__name__}: {exc}")

    def run_full(self) -> None:
        self.worker("run-full", lambda: self._run_full())

    def _run_full(self) -> dict[str, Any]:
        report = run_heap(self.config())
        code_product = str(report.get("code_product") or "")
        if code_product:
            self.code_product.set(code_product)
        return report

    def review_code_product(self) -> None:
        self.worker("review", lambda: self._analyze(False))

    def apply_safe(self) -> None:
        if not messagebox.askyesno(
            "Apply safe sections", "Apply only sections classified safe by the intake tool?"
        ):
            return
        self.worker("apply-safe", lambda: self._analyze(True))

    def _analyze(self, apply_safe: bool) -> dict[str, Any]:
        cfg = resolve_config(self.config())
        code_product = Path(self.code_product.get())
        output_dir = run_dir_for(cfg)
        return analyze_code_product(
            cfg.repo_root,
            code_product,
            output_dir,
            apply_safe=apply_safe,
            require_all_integrated=apply_safe,
        )


def main() -> int:
    root = tk.Tk()
    OperatorLauncherApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
