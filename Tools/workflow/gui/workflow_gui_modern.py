from __future__ import annotations

import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

try:
    import workflow_core as wf
except ImportError:
    from Tools.workflow import workflow_core as wf
from components.action_panel import GroupedActionPanel
from components.live_output_panel import LiveOutputPanel
from components.session_overview import SessionOverviewFrame
from components.st_theme import apply_spaziotempo_theme, text_widget_colors
from components.storage_dashboard import StorageDashboardWindow
from workflow_gui import WorkflowGui as LegacyWorkflowGui
from workflow_gui_action_groups import build_modern_action_groups


class ModernWorkflowGui(LegacyWorkflowGui):
    """Adaptive workflow GUI with grouped actions and graphical live output."""

    def configure_style(self) -> None:
        apply_spaziotempo_theme(self)

    def build_layout(self) -> None:
        self.configure_style()
        self.geometry("1360x840")
        self.minsize(1040, 680)

        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root)
        header.pack(fill="x", pady=(0, 10))
        ttk.Label(header, text="Spaziotempo Workflow Control", style="Header.TLabel").pack(
            side="left"
        )
        ttk.Label(
            header,
            text="Pipeline audio, AI, script Blender, artefatti e pubblicazione GitHub",
            style="SubHeader.TLabel",
        ).pack(side="left", padx=(14, 0))

        body = ttk.PanedWindow(root, orient="horizontal")
        body.pack(fill="both", expand=True)

        left = ttk.Frame(body, padding=(0, 0, 8, 0))
        right = ttk.Frame(body)
        body.add(left, weight=0)
        body.add(right, weight=1)

        self.build_left_panel(left)
        self.build_right_panel(right)

    def build_left_panel(self, parent: ttk.Frame) -> None:
        options = ttk.LabelFrame(parent, text="AI Runtime")
        options.pack(fill="x", pady=(0, 10))

        toggles = ttk.Frame(options)
        toggles.pack(fill="x")
        ttk.Checkbutton(toggles, text="Include manual", variable=self.include_manual).pack(
            anchor="w", pady=(0, 2)
        )
        ttk.Checkbutton(toggles, text="Skip NPU heavy pass", variable=self.skip_npu).pack(
            anchor="w", pady=(0, 2)
        )
        ttk.Checkbutton(toggles, text="Skip Ollama", variable=self.skip_ollama).pack(
            anchor="w", pady=(0, 6)
        )

        model_grid = ttk.Frame(options)
        model_grid.pack(fill="x")
        ttk.Label(model_grid, text="Creative").grid(row=0, column=0, sticky="w", pady=(0, 4))
        ttk.Combobox(
            model_grid, textvariable=self.creative_model, values=self.available_models, width=31
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 4))
        ttk.Label(model_grid, text="Technical").grid(row=1, column=0, sticky="w", pady=(0, 4))
        ttk.Combobox(
            model_grid, textvariable=self.technical_model, values=self.available_models, width=31
        ).grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(0, 4))
        ttk.Label(model_grid, text="Chat").grid(row=2, column=0, sticky="w", pady=(0, 4))
        ttk.Combobox(
            model_grid, textvariable=self.chat_model, values=self.available_models, width=31
        ).grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=(0, 4))
        model_grid.columnconfigure(1, weight=1)

        lower = ttk.Frame(options)
        lower.pack(fill="x", pady=(4, 0))
        ttk.Label(lower, text="Script tokens").pack(side="left")
        ttk.Entry(lower, textvariable=self.script_tokens, width=8).pack(side="left", padx=(8, 0))
        ttk.Label(lower, text="Manual limit").pack(side="left", padx=(14, 0))
        ttk.Entry(lower, textvariable=self.manual_limit, width=8).pack(side="left", padx=(8, 0))
        ttk.Button(options, text="Save AI models", command=self.save_ai_models).pack(
            fill="x", pady=(8, 0)
        )

        action_panel = GroupedActionPanel(parent, title="Workflow Actions", min_width=370)
        action_panel.pack(fill="both", expand=True)
        self.buttons, self.always_enabled_buttons = action_panel.build(self.build_action_groups())

    def build_right_panel(self, parent: ttk.Frame) -> None:
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)
        self.main_notebook = notebook

        live_tab = ttk.Frame(notebook, padding=8)
        status_tab = ttk.Frame(notebook, padding=8)
        help_tab = ttk.Frame(notebook, padding=8)
        notebook.add(live_tab, text="Live Output")
        notebook.add(status_tab, text="Session / Outputs")
        notebook.add(help_tab, text="Workflow Guide")

        self.live_output_panel = LiveOutputPanel(live_tab)
        self.live_output_panel.pack(fill="both", expand=True)
        self.output = self.live_output_panel.raw_text

        self.session_overview = SessionOverviewFrame(
            status_tab,
            open_path_callback=self.open_system_path,
            copy_callback=self.copy_text_to_clipboard,
        )
        self.session_box = self.session_overview.detail

        help_text = tk.Text(help_tab, wrap="word", borderwidth=0, **text_widget_colors(self))
        help_text.pack(fill="both", expand=True)
        help_text.insert(
            "1.0",
            "Ordine operativo consigliato:\n\n"
            "1. Apri la GUI: il primo piano e' Live Output.\n"
            "2. Avvia Analyze WAV / Full audio prepare per generare i dati tecnici.\n"
            "3. Usa AI pipeline dry-run per verificare preflight, contesto macchina e output attesi.\n"
            "4. Usa AI artifact pipeline per generare chunk semantici e intermedi IA consapevoli.\n"
            "5. Usa Code context + indexAI / Rebuild indexAI quando hai modificato codice o documentazione.\n"
            "6. Usa Dual AI plan / Scene director chat / Dual AI scene script per la fase creativa.\n"
            "7. Push generated data solo dopo avere completato e verificato i dati strutturati.\n\n"
            "GUI:\n"
            "- Live Output e' la vista principale e tratta graficamente stdout/stderr.\n"
            "- Fermando il mouse su un pulsante compare una descrizione rapida della funzione.\n"
            "- Skip NPU heavy pass controlla il vecchio passaggio NPU pesante, non la nuova review IA leggera.\n"
            "- AI pipeline usa CPU per preflight/validazione e NPU solo per review/scoring leggero.\n"
            "- Le tabelle seguono l'ordinamento stile Esplora file: clic su intestazione, secondo clic inverte.\n"
            "- Session / Outputs mostra riepilogo e output in tabella, non piu' testo grezzo.\n"
            "- Project stats controlla la cartella blender e distingue blender-audio-project dal resto.\n\n"
            "Estensione GUI:\n"
            "- aggiungi una nuova ActionSpec dentro build_action_groups();\n"
            "- scegli il gruppo corretto o creane uno nuovo;\n"
            "- la GUI gestisce automaticamente scroll, spacing, tooltip e abilitazione pulsanti.\n",
        )
        help_text.configure(state="disabled")
        notebook.select(live_tab)

    def append_output(self, text: str) -> None:
        if hasattr(self, "live_output_panel"):
            self.live_output_panel.append_text(text)
        else:
            super().append_output(text)

    def open_system_path(self, path: Path) -> None:
        try:
            if not path.exists():
                raise FileNotFoundError(f"Percorso non trovato: {path}")
            os.startfile(str(path))  # type: ignore[attr-defined]
        except Exception as exc:
            messagebox.showerror("Open", str(exc))

    def copy_text_to_clipboard(self, text: str) -> None:
        self.clipboard_clear()
        self.clipboard_append(text)

    def refresh_session(self) -> None:
        self.session = wf.load_session(create=True)
        self.creative_model.set(self.session.creative_model)
        self.technical_model.set(self.session.technical_model)
        self.chat_model.set(self.session.chat_model)
        self.script_tokens.set(str(self.session.script_max_tokens))
        status = wf.operation_status(self.session)
        if hasattr(self, "session_overview"):
            self.session_overview.update_session(self.session, status)
        if self.session.debug_enabled and self.log_window is None:
            self.open_log_window()

    def open_project_stats_window(self) -> None:
        if self.project_stats_window is None or not self.project_stats_window.winfo_exists():
            self.project_stats_window = StorageDashboardWindow(
                self,
                session_loader=lambda: wf.load_session(create=True),
                workflow_state_module=wf,
            )
        self.project_stats_window.show()

    def ai_artifact_pipeline_command(self, dry_run: bool) -> list[str]:
        command = [
            str(wf.python_executable()),
            str(wf.PROJECT_DIR / "Tools" / "ai" / "run_parallel_artifact_pipeline.py"),
            "--repo-root",
            str(wf.PROJECT_DIR),
            "--analysis-json",
            str(self.session.artifacts["analysis_json"]),
            "--build-chunks",
            "--build-music-summary",
            "--use-npu",
            "--validate",
        ]
        if dry_run:
            command.extend(["--dry-run", "--write-dry-run-report"])
        return command

    def run_ai_artifact_pipeline(self, dry_run: bool) -> None:
        label = "AI pipeline dry-run" if dry_run else "AI artifact pipeline"

        def task():
            return wf.run_command(
                self.ai_artifact_pipeline_command(dry_run),
                operation="ai_artifact_pipeline_dry_run" if dry_run else "ai_artifact_pipeline",
                metadata={
                    "analysis_json": self.session.artifacts.get("analysis_json"),
                    "track_stem": self.session.track_stem,
                    "dry_run": dry_run,
                    "skip_npu_heavy_pass": self.skip_npu.get(),
                    "note": "Independent from legacy heavy NPU pass; uses the lightweight AI artifact pipeline.",
                },
            )

        self.run_task(label, task)

    def build_action_groups(self) -> tuple[ActionGroup, ...]:
        self.wf = wf
        return build_modern_action_groups(self)


WorkflowGui = ModernWorkflowGui


def main() -> None:
    app = ModernWorkflowGui()
    app.mainloop()


if __name__ == "__main__":
    main()
