from __future__ import annotations

import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

import workflow_state as wf
from components.action_panel import ActionGroup, ActionSpec, GroupedActionPanel
from components.live_output_panel import LiveOutputPanel
from components.session_overview import SessionOverviewFrame
from components.st_theme import apply_spaziotempo_theme, text_widget_colors
from components.storage_dashboard import StorageDashboardWindow
from workflow_gui import WorkflowGui as LegacyWorkflowGui


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
        ttk.Label(header, text="Spaziotempo Workflow Control", style="Header.TLabel").pack(side="left")
        ttk.Label(header, text="Pipeline audio, AI, script Blender, artefatti e pubblicazione GitHub", style="SubHeader.TLabel").pack(side="left", padx=(14, 0))

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
        ttk.Checkbutton(toggles, text="Include manual", variable=self.include_manual).pack(anchor="w", pady=(0, 2))
        ttk.Checkbutton(toggles, text="Skip NPU heavy pass", variable=self.skip_npu).pack(anchor="w", pady=(0, 2))
        ttk.Checkbutton(toggles, text="Skip Ollama", variable=self.skip_ollama).pack(anchor="w", pady=(0, 6))
        model_grid = ttk.Frame(options)
        model_grid.pack(fill="x")
        ttk.Label(model_grid, text="Creative").grid(row=0, column=0, sticky="w", pady=(0, 4))
        ttk.Combobox(model_grid, textvariable=self.creative_model, values=self.available_models, width=31).grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 4))
        ttk.Label(model_grid, text="Technical").grid(row=1, column=0, sticky="w", pady=(0, 4))
        ttk.Combobox(model_grid, textvariable=self.technical_model, values=self.available_models, width=31).grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(0, 4))
        ttk.Label(model_grid, text="Chat").grid(row=2, column=0, sticky="w", pady=(0, 4))
        ttk.Combobox(model_grid, textvariable=self.chat_model, values=self.available_models, width=31).grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=(0, 4))
        model_grid.columnconfigure(1, weight=1)
        lower = ttk.Frame(options)
        lower.pack(fill="x", pady=(4, 0))
        ttk.Label(lower, text="Script tokens").pack(side="left")
        ttk.Entry(lower, textvariable=self.script_tokens, width=8).pack(side="left", padx=(8, 0))
        ttk.Label(lower, text="Manual limit").pack(side="left", padx=(14, 0))
        ttk.Entry(lower, textvariable=self.manual_limit, width=8).pack(side="left", padx=(8, 0))
        ttk.Button(options, text="Save AI models", command=self.save_ai_models).pack(fill="x", pady=(8, 0))
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
        self.session_overview = SessionOverviewFrame(status_tab, open_path_callback=self.open_system_path, copy_callback=self.copy_text_to_clipboard)
        self.session_box = self.session_overview.detail
        help_text = tk.Text(help_tab, wrap="word", borderwidth=0, **text_widget_colors(self))
        help_text.pack(fill="both", expand=True)
        help_text.insert("1.0", "Ordine operativo consigliato:\n\n1. Full audio prepare.\n2. AI pipeline dry-run.\n3. AI artifact pipeline: ora genera smart context packet + guardrail NPU-light.\n4. Scene director chat / Dual AI scene script.\n5. Push generated data o Push all project changes.\n\nNote tecniche:\n- Skip NPU heavy pass controlla solo il vecchio passaggio NPU pesante.\n- La nuova NPU guardrail resta separata e leggera.\n- Smart context non taglia conoscenza: crea capsule, manifest e packet selezionati.\n- I file completi restano referenziati e leggibili tramite path/SHA.\n")
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
            self.project_stats_window = StorageDashboardWindow(self, session_loader=lambda: wf.load_session(create=True), workflow_state_module=wf)
        self.project_stats_window.show()

    def ai_artifact_pipeline_command(self, dry_run: bool) -> list[str]:
        command = [
            str(wf.python_executable()),
            str(wf.PROJECT_DIR / "Tools" / "ai" / "run_parallel_artifact_pipeline.py"),
            "--repo-root", str(wf.PROJECT_DIR),
            "--analysis-json", str(self.session.artifacts["analysis_json"]),
            "--track-stem", self.session.track_stem,
            "--build-chunks",
            "--build-music-summary",
            "--smart-context",
            "--smart-task", "Scene Director Blender Python generation audio-reactive full keyframe preservation asset-aware composition",
            "--npu-guardrail",
            "--use-npu",
            "--validate",
            "--continue-on-error",
        ]
        if dry_run:
            command.extend(["--dry-run", "--write-dry-run-report"])
        return command

    def run_ai_artifact_pipeline(self, dry_run: bool) -> None:
        label = "AI pipeline dry-run" if dry_run else "AI artifact pipeline"

        def task():
            return wf.run_command(self.ai_artifact_pipeline_command(dry_run), operation="ai_artifact_pipeline_dry_run" if dry_run else "ai_artifact_pipeline", metadata={"analysis_json": self.session.artifacts.get("analysis_json"), "track_stem": self.session.track_stem, "dry_run": dry_run, "smart_context": True, "npu_guardrail": True, "skip_npu_heavy_pass": self.skip_npu.get(), "note": "Smart context + NPU guardrail are independent from legacy heavy NPU pass."})

        self.run_task(label, task)

    def build_action_groups(self) -> tuple[ActionGroup, ...]:
        return (
            ActionGroup("Track setup", (ActionSpec("Choose WAV", self.choose_wav, description="Seleziona un nuovo file audio WAV."), ActionSpec("Reset default WAV", self.reset_wav, description="Torna alla traccia predefinita."))),
            ActionGroup("Data preparation", (
                ActionSpec("Analyze WAV", lambda: self.run_task("Analyze WAV", lambda: wf.run_analyze_wav(self.session, skip_music_context=True)), description="Genera l'analisi tecnica del WAV e i file JSON base."),
                ActionSpec("Track summary", lambda: self.run_task("Track summary", lambda: wf.run_track_summary(self.session)), description="Crea un riassunto tecnico compatto della traccia."),
                ActionSpec("Music context", lambda: self.run_task("Music context", lambda: wf.run_music_context(self.session)), description="Produce un contesto musicale strutturato."),
                ActionSpec("Full audio prepare", lambda: self.run_task("Full audio prepare", lambda: wf.run_full_audio_prepare(self.session)), description="Esegue preparazione audio completa."),
            )),
            ActionGroup("AI artifact pipeline", (
                ActionSpec("AI pipeline dry-run", lambda: self.run_ai_artifact_pipeline(dry_run=True), description="Verifica preflight e piano: include smart context e NPU guardrail."),
                ActionSpec("AI artifact pipeline", lambda: self.run_ai_artifact_pipeline(dry_run=False), description="Genera intermedi IA, smart context packet, manifest, review NPU e validazione."),
            )),
            ActionGroup("Project intelligence", (
                ActionSpec("Code context + indexAI", lambda: self.run_task("Code context + indexAI", lambda: wf.run_code_context(self.session)), description="Aggiorna contesto codice e indici AI tradizionali."),
                ActionSpec("Rebuild indexAI", lambda: self.run_task("Rebuild indexAI", lambda: wf.run_project_ai_index(self.session, force=True)), description="Rigenera forzatamente l'indice progetto."),
                ActionSpec("Index manuals", self.index_manuals, description="Indicizza manuali locali Blender/progetto."),
            )),
            ActionGroup("Creative AI pipeline", (
                ActionSpec("Dual AI plan", self.dual_ai_plan, description="Genera il piano scena strutturato."),
                ActionSpec("Scene director chat", self.scene_director_chat, description="Apre la chat locale per affinare il brief."),
                ActionSpec("Dual AI scene script", self.dual_ai_draft, description="Genera la bozza dello script Blender finale."),
            )),
            ActionGroup("Review and diagnostics", (
                ActionSpec("Open log panel", self.open_log_window, always_enabled=True, description="Consulta eventi workflow e ultimo risultato."),
                ActionSpec("Advanced debug check", self.open_advanced_debug_window, always_enabled=True, description="Controlli diagnostici avanzati."),
                ActionSpec("Startup service check", self.startup_service_check, always_enabled=True, description="Verifica servizi locali e runtime."),
                ActionSpec("Project stats", self.open_project_stats_window, always_enabled=True, description="Dashboard spazio occupato e stato progetto."),
                ActionSpec("Debug monitor shell", self.open_debug_monitor_shell, always_enabled=True, description="Monitor debug in shell separata."),
            )),
            ActionGroup("Maintenance", (
                ActionSpec("Cleanup intermedi", self.cleanup_intermediates, description="Rimuove intermedi, smart context e log workflow preservando audio/render."),
                ActionSpec("Cleanup render frames", self.cleanup_render_frames, description="Pulisce frame render della traccia corrente."),
                ActionSpec("Toggle debug", self.toggle_debug, always_enabled=True, description="Abilita/disabilita logging dettagliato."),
                ActionSpec("Mark interrupted", self.mark_interrupted, always_enabled=True, description="Marca operazione come interrotta."),
                ActionSpec("Refresh", self.refresh_session, always_enabled=True, description="Aggiorna stato sessione e output."),
            )),
        )


WorkflowGui = ModernWorkflowGui


def main() -> None:
    app = ModernWorkflowGui()
    app.mainloop()


if __name__ == "__main__":
    main()
