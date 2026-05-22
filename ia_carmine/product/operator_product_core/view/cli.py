"""Tkinter view for the canonical operator heap/universe run."""

from __future__ import annotations

import json
import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

from ia_carmine.product.operator_product_core import DEFAULT_RUN_LABEL, LauncherConfig
from ia_carmine.product.operator_product_core.controller import OperatorProductController
from ia_carmine.product.operator_product_core.io_utils import now_stamp
from ia_carmine.runtime.run.cli import default_final_root, default_task_md


class OperatorRunView:
    """View-only Tkinter surface for the shared operator run controller."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("IA-Carmine Run")
        self.messages: queue.Queue[str] = queue.Queue()
        cwd = Path.cwd()
        self.repo_root = tk.StringVar(value=str(cwd))
        self.request_file = tk.StringVar(value=str(default_task_md()))
        self.intermediate_root = tk.StringVar(
            value=str(cwd / "output" / "validation" / "operator_product_launcher_lab")
        )
        self.final_root = tk.StringVar(value="")
        self.python_exe = tk.StringVar(value=str(cwd / ".venv" / "Scripts" / "python.exe"))
        self.run_label = tk.StringVar(value=DEFAULT_RUN_LABEL)
        self.stamp = tk.StringVar(value="")
        self.startup_max_memory_chars = tk.StringVar(value="")
        self.startup_max_context_files = tk.StringVar(value="")
        self.startup_scan_context_files = tk.StringVar(value="")
        self.startup_max_chars_per_file = tk.StringVar(value="")
        self.context_document_count = tk.StringVar(value="")
        self.context_document_preview_chars = tk.StringVar(value="")
        self.semantic_code_chunk_limit = tk.StringVar(value="")
        self.semantic_code_chunk_preview_chars = tk.StringVar(value="")
        self.semantic_evidence_chunk_limit = tk.StringVar(value="")
        self.memory_search_limit = tk.StringVar(value="")
        self.tool_catalog_limit = tk.StringVar(value="")
        self.code_product = tk.StringVar(value="")
        self.last_report: dict[str, Any] = {}
        self._build()
        self._sync_direct_defaults()
        self._poll_messages()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        rows = [
            ("Repo dir", self.repo_root, "dir"),
            ("Input MD", self.request_file, "file"),
            ("Intermediate dir", self.intermediate_root, "dir"),
            ("Final output dir", self.final_root, "dir"),
            ("Python exe", self.python_exe, "file"),
            ("Code product", self.code_product, "file"),
        ]
        for row, (label, variable, kind) in enumerate(rows):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
            ttk.Entry(frame, textvariable=variable, width=88).grid(
                row=row, column=1, sticky="ew", pady=2
            )
            ttk.Button(
                frame,
                text="...",
                width=3,
                command=lambda v=variable, k=kind: self._browse(v, k),
            ).grid(row=row, column=2, padx=4)

        ttk.Label(frame, text="Run label").grid(row=6, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=self.run_label, width=40).grid(
            row=6, column=1, sticky="w", pady=2
        )
        direct_fields = [
            ("Memory chars", self.startup_max_memory_chars),
            ("Context files", self.startup_max_context_files),
            ("Scan files", self.startup_scan_context_files),
            ("Chars per file", self.startup_max_chars_per_file),
            ("Context docs", self.context_document_count),
            ("Context preview", self.context_document_preview_chars),
            ("Code chunks", self.semantic_code_chunk_limit),
            ("Code preview", self.semantic_code_chunk_preview_chars),
            ("Evidence chunks", self.semantic_evidence_chunk_limit),
            ("Memory search", self.memory_search_limit),
            ("Tool catalog", self.tool_catalog_limit),
        ]
        for row, (label, variable) in enumerate(direct_fields, start=7):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
            ttk.Entry(frame, textvariable=variable, width=18).grid(
                row=row, column=1, sticky="w", pady=2
            )
        ttk.Label(frame, text="Stamp").grid(row=18, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=self.stamp, width=40).grid(
            row=18, column=1, sticky="w", pady=2
        )

        buttons = ttk.Frame(frame)
        buttons.grid(row=19, column=0, columnspan=3, sticky="ew", pady=8)
        ttk.Button(buttons, text="Build Command", command=self.build_command).pack(
            side="left", padx=3
        )
        ttk.Button(buttons, text="Run", command=self.run).pack(side="left", padx=3)
        ttk.Button(buttons, text="Review Code Product", command=self.review_code_product).pack(
            side="left", padx=3
        )
        ttk.Button(buttons, text="Apply Safe", command=self.apply_safe).pack(side="left", padx=3)
        self.log = tk.Text(frame, height=24, width=110, wrap="word")
        self.log.grid(row=20, column=0, columnspan=3, sticky="nsew")
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(20, weight=1)

    def _browse(self, variable: tk.StringVar, kind: str) -> None:
        value = filedialog.askdirectory() if kind == "dir" else filedialog.askopenfilename()
        if value:
            variable.set(value)

    def _sync_direct_defaults(self) -> None:
        cfg = LauncherConfig(Path("."), Path(""), Path(""), Path(""))
        values = {
            self.startup_max_memory_chars: cfg.startup_max_memory_chars,
            self.startup_max_context_files: cfg.startup_max_context_files,
            self.startup_scan_context_files: cfg.startup_scan_context_files,
            self.startup_max_chars_per_file: cfg.startup_max_chars_per_file,
            self.context_document_count: cfg.context_document_count,
            self.context_document_preview_chars: cfg.context_document_preview_chars,
            self.semantic_code_chunk_limit: cfg.semantic_code_chunk_limit,
            self.semantic_code_chunk_preview_chars: cfg.semantic_code_chunk_preview_chars,
            self.semantic_evidence_chunk_limit: cfg.semantic_evidence_chunk_limit,
            self.memory_search_limit: cfg.memory_search_limit,
            self.tool_catalog_limit: cfg.tool_catalog_limit,
        }
        for variable, value in values.items():
            variable.set(str(value))

    def _int_field(self, label: str, variable: tk.StringVar) -> int | None:
        raw = variable.get().strip()
        if not raw:
            return None
        value = int(raw)
        if value <= 0:
            raise ValueError(f"{label} must be greater than zero")
        return value

    def direct_overrides(self) -> dict[str, int]:
        fields = {
            "startup_max_memory_chars": ("Memory chars", self.startup_max_memory_chars),
            "startup_max_context_files": ("Context files", self.startup_max_context_files),
            "startup_scan_context_files": ("Scan files", self.startup_scan_context_files),
            "startup_max_chars_per_file": ("Chars per file", self.startup_max_chars_per_file),
            "context_document_count": ("Context docs", self.context_document_count),
            "context_document_preview_chars": (
                "Context preview",
                self.context_document_preview_chars,
            ),
            "semantic_code_chunk_limit": ("Code chunks", self.semantic_code_chunk_limit),
            "semantic_code_chunk_preview_chars": (
                "Code preview",
                self.semantic_code_chunk_preview_chars,
            ),
            "semantic_evidence_chunk_limit": ("Evidence chunks", self.semantic_evidence_chunk_limit),
            "memory_search_limit": ("Memory search", self.memory_search_limit),
            "tool_catalog_limit": ("Tool catalog", self.tool_catalog_limit),
        }
        overrides: dict[str, int] = {}
        for key, (label, variable) in fields.items():
            value = self._int_field(label, variable)
            if value is not None:
                overrides[key] = value
        return overrides

    def config(self) -> LauncherConfig:
        stamp = self.stamp.get().strip()
        if not stamp:
            stamp = now_stamp()
            self.stamp.set(stamp)
        final_root = self.final_root.get().strip() or str(default_final_root(stamp))
        return LauncherConfig(
            repo_root=Path(self.repo_root.get()),
            request_file=Path(self.request_file.get()),
            intermediate_root=Path(self.intermediate_root.get()),
            final_root=Path(final_root),
            run_label=self.run_label.get(),
            python_exe=self.python_exe.get(),
            stamp=stamp,
            **self.direct_overrides(),
        )

    def controller(self) -> OperatorProductController:
        return OperatorProductController(self.config())

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
            self._log(json.dumps({"command": self.controller().build_command()}, indent=2))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Build command failed", f"{type(exc).__name__}: {exc}")

    def run(self) -> None:
        self.worker("run", lambda: self._run())

    def _run(self) -> dict[str, Any]:
        report = self.controller().run()
        code_product = str(report.get("code_product") or "")
        if code_product:
            self.code_product.set(code_product)
        return report

    def review_code_product(self) -> None:
        self.worker("review", lambda: self.controller().review_code_product(Path(self.code_product.get())))

    def apply_safe(self) -> None:
        if not messagebox.askyesno(
            "Apply safe sections", "Apply only sections classified safe by the intake tool?"
        ):
            return
        self.worker(
            "apply-safe",
            lambda: self.controller().apply_safe_code_product(Path(self.code_product.get())),
        )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--help", "-h"}:
        print("Usage: python -m ia_carmine.cli operator_product_gui")
        print("Graphical view for the same controller used by python -m ia_carmine.cli run.")
        return 0
    root = tk.Tk()
    OperatorRunView(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
