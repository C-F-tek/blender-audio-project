from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import workflow_state as wf
from components.action_panel import ActionGroup, ActionSpec, GroupedActionPanel
from components.st_theme import STTheme, apply_spaziotempo_theme
from components.storage_dashboard import StorageDashboardWindow
from workflow_gui import WorkflowGui as LegacyWorkflowGui


class ModernWorkflowGui(LegacyWorkflowGui):
    """Adaptive workflow GUI with grouped, scrollable operations.

    This class keeps all operational methods from the legacy GUI and replaces
    only the layout layer. New GUI actions should be added by extending
    build_action_groups(), not by manually packing buttons in multiple places.
    """

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
        ttk.Checkbutton(toggles, text="Include manual", variable=self.include_manual).pack(anchor="w", pady=(0, 2))
        ttk.Checkbutton(toggles, text="Skip NPU heavy pass", variable=self.skip_npu).pack(anchor="w", pady=(0, 2))
        ttk.Checkbutton(toggles, text="Skip Ollama", variable=self.skip_ollama).pack(anchor="w", pady=(0, 6))

        model_grid = ttk.Frame(options)
        model_grid.pack(fill="x")
        ttk.Label(model_grid, text="Creative").grid(row=0, column=0, sticky="w", pady=(0, 4))
        ttk.Combobox(model_grid, textvariable=self.creative_model, values=self.available_models, width=31).grid(
            row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 4)
        )
        ttk.Label(model_grid, text="Technical").grid(row=1, column=0, sticky="w", pady=(0, 4))
        ttk.Combobox(model_grid, textvariable=self.technical_model, values=self.available_models, width=31).grid(
            row=1, column=1, sticky="ew", padx=(8, 0), pady=(0, 4)
        )
        ttk.Label(model_grid, text="Chat").grid(row=2, column=0, sticky="w", pady=(0, 4))
        ttk.Combobox(model_grid, textvariable=self.chat_model, values=self.available_models, width=31).grid(
            row=2, column=1, sticky="ew", padx=(8, 0), pady=(0, 4)
        )
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

        status_tab = ttk.Frame(notebook, padding=8)
        output_tab = ttk.Frame(notebook, padding=8)
        help_tab = ttk.Frame(notebook, padding=8)
        notebook.add(status_tab, text="Session / Outputs")
        notebook.add(output_tab, text="Live Output")
        notebook.add(help_tab, text="Workflow Guide")

        self.session_box = tk.Text(
            status_tab,
            height=16,
            wrap="word",
            borderwidth=1,
            relief="solid",
            background=STTheme.panel,
            foreground=STTheme.text,
            insertbackground=STTheme.cyan,
        )
        self.session_box.pack(fill="both", expand=True)
        self.session_box.configure(state="disabled")

        self.output = tk.Text(
            output_tab,
            wrap="word",
            borderwidth=1,
            relief="solid",
            background=STTheme.panel,
            foreground=STTheme.text,
            insertbackground=STTheme.cyan,
        )
        self.output.pack(fill="both", expand=True)

        help_text = tk.Text(
            help_tab,
            wrap="word",
            borderwidth=0,
            background=STTheme.panel,
            foreground=STTheme.text,
            insertbackground=STTheme.cyan,
        )
        help_text.pack(fill="both", expand=True)
        help_text.insert(
            "1.0",
            "Ordine operativo consigliato:\n\n"
            "1. Analyze WAV / Full audio prepare per generare i dati tecnici.\n"
            "2. Dual AI plan per produrre il piano strutturato.\n"
            "3. Scene director chat per affinare brief e vincoli.\n"
            "4. Dual AI scene script per generare lo script Blender.\n"
            "5. Artifact browser per controllare JSON, immagini, output audio/video e script prodotti.\n"
            "6. Push generated data solo dopo avere completato e verificato i dati strutturati.\n\n"
            "Statistiche:\n"
            "- Project stats apre una dashboard dedicata alla cartella blender.\n"
            "- La dashboard distingue blender-audio-project dal resto dei contenuti nella root blender.\n"
            "- Doppio click su cartelle/file per aprirli nel sistema.\n\n"
            "Estensione GUI:\n"
            "- aggiungi una nuova ActionSpec dentro build_action_groups();\n"
            "- scegli il gruppo corretto o creane uno nuovo;\n"
            "- la GUI gestisce automaticamente scroll, spacing e abilitazione pulsanti.\n",
        )
        help_text.configure(state="disabled")

    def open_project_stats_window(self) -> None:
        if self.project_stats_window is None or not self.project_stats_window.winfo_exists():
            self.project_stats_window = StorageDashboardWindow(
                self,
                session_loader=lambda: wf.load_session(create=True),
                workflow_state_module=wf,
            )
        self.project_stats_window.show()

    def build_action_groups(self) -> tuple[ActionGroup, ...]:
        return (
            ActionGroup(
                "Track setup",
                (
                    ActionSpec("Choose WAV", self.choose_wav, description="Seleziona un nuovo file audio WAV."),
                    ActionSpec("Reset default WAV", self.reset_wav, description="Torna alla traccia predefinita."),
                ),
            ),
            ActionGroup(
                "Data preparation",
                (
                    ActionSpec(
                        "Analyze WAV",
                        lambda: self.run_task("Analyze WAV", lambda: wf.run_analyze_wav(self.session, skip_music_context=True)),
                        description="Genera analisi tecnica audio base.",
                    ),
                    ActionSpec(
                        "Track summary",
                        lambda: self.run_task("Track summary", lambda: wf.run_track_summary(self.session)),
                        description="Crea riassunto compatto della traccia.",
                    ),
                    ActionSpec(
                        "Music context",
                        lambda: self.run_task("Music context", lambda: wf.run_music_context(self.session)),
                        description="Produce contesto musicale strutturato.",
                    ),
                    ActionSpec(
                        "Full audio prepare",
                        lambda: self.run_task("Full audio prepare", lambda: wf.run_full_audio_prepare(self.session)),
                        description="Esegue la preparazione audio completa.",
                    ),
                ),
            ),
            ActionGroup(
                "Project intelligence",
                (
                    ActionSpec(
                        "Code context + indexAI",
                        lambda: self.run_task("Code context + indexAI", lambda: wf.run_code_context(self.session)),
                        description="Aggiorna contesto codice e indici AI.",
                    ),
                    ActionSpec(
                        "Rebuild indexAI",
                        lambda: self.run_task("Rebuild indexAI", lambda: wf.run_project_ai_index(self.session, force=True)),
                        description="Rigenera forzatamente l'indice progetto.",
                    ),
                    ActionSpec("Index manuals", self.index_manuals, description="Indicizza manuali locali Blender/progetto."),
                ),
            ),
            ActionGroup(
                "Creative AI pipeline",
                (
                    ActionSpec("Dual AI plan", self.dual_ai_plan, description="Genera piano scena strutturato."),
                    ActionSpec("Scene director chat", self.scene_director_chat, description="Affina il brief con chat locale."),
                    ActionSpec("Dual AI scene script", self.dual_ai_draft, description="Genera bozza script Blender finale."),
                ),
            ),
            ActionGroup(
                "Review and diagnostics",
                (
                    ActionSpec("Open log panel", self.open_log_window, always_enabled=True, description="Consulta log workflow."),
                    ActionSpec("Advanced debug check", self.open_advanced_debug_window, always_enabled=True, description="Diagnostica avanzata."),
                    ActionSpec("Startup service check", self.startup_service_check, always_enabled=True, description="Verifica servizi locali."),
                    ActionSpec("Project stats", self.open_project_stats_window, always_enabled=True, description="Dashboard spazio occupato e contenuto cartella blender."),
                    ActionSpec("Debug monitor shell", self.open_debug_monitor_shell, always_enabled=True, description="Monitor debug in shell separata."),
                ),
            ),
            ActionGroup(
                "Maintenance",
                (
                    ActionSpec("Cleanup intermedi", self.cleanup_intermediates, description="Rimuove intermedi generati."),
                    ActionSpec("Cleanup render frames", self.cleanup_render_frames, description="Pulisce sequenze frame render."),
                    ActionSpec("Toggle debug", self.toggle_debug, always_enabled=True, description="Abilita/disabilita log dettagliato."),
                    ActionSpec("Mark interrupted", self.mark_interrupted, always_enabled=True, description="Marca manualmente operazione interrotta."),
                    ActionSpec("Refresh", self.refresh_session, always_enabled=True, description="Aggiorna stato sessione."),
                ),
            ),
        )


WorkflowGui = ModernWorkflowGui


def main() -> None:
    app = ModernWorkflowGui()
    app.mainloop()


if __name__ == "__main__":
    main()
