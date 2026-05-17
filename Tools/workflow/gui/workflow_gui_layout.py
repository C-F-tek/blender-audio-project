"""Layout builder for the classic workflow GUI."""

from __future__ import annotations

from tkinter import ttk

from workflow_gui_common import wf


def build_layout(self: object) -> None:
    root = ttk.Frame(self, padding=10)
    root.pack(fill="both", expand=True)

    left = ttk.Frame(root)
    left.pack(side="left", fill="y")

    right = ttk.Frame(root)
    right.pack(side="right", fill="both", expand=True, padx=(12, 0))

    self.session_box = tk.Text(right, height=12, wrap="word")
    self.session_box.pack(fill="x")
    self.session_box.configure(state="disabled")

    options = ttk.LabelFrame(left, text="AI Options")
    options.pack(fill="x", pady=(0, 8))
    ttk.Checkbutton(options, text="Include manual", variable=self.include_manual).pack(
        anchor="w", padx=8, pady=(6, 0)
    )
    ttk.Checkbutton(options, text="Skip NPU heavy pass", variable=self.skip_npu).pack(
        anchor="w", padx=8
    )
    ttk.Checkbutton(options, text="Skip Ollama", variable=self.skip_ollama).pack(
        anchor="w", padx=8
    )
    ttk.Label(options, text="Creative model").pack(anchor="w", padx=8, pady=(6, 0))
    ttk.Combobox(
        options, textvariable=self.creative_model, values=self.available_models, width=28
    ).pack(fill="x", padx=8)
    ttk.Label(options, text="Technical/script model").pack(anchor="w", padx=8, pady=(6, 0))
    ttk.Combobox(
        options, textvariable=self.technical_model, values=self.available_models, width=28
    ).pack(fill="x", padx=8)
    ttk.Label(options, text="Chat model").pack(anchor="w", padx=8, pady=(6, 0))
    ttk.Combobox(
        options, textvariable=self.chat_model, values=self.available_models, width=28
    ).pack(fill="x", padx=8)
    token_row = ttk.Frame(options)
    token_row.pack(fill="x", padx=8, pady=(6, 0))
    ttk.Label(token_row, text="Script tokens").pack(side="left")
    ttk.Entry(token_row, textvariable=self.script_tokens, width=8).pack(
        side="left", padx=(6, 0)
    )
    ttk.Button(options, text="Save AI models", command=self.save_ai_models).pack(
        fill="x", padx=8, pady=(6, 0)
    )
    limit_row = ttk.Frame(options)
    limit_row.pack(fill="x", padx=8, pady=6)
    ttk.Label(limit_row, text="Manual limit").pack(side="left")
    ttk.Entry(limit_row, textvariable=self.manual_limit, width=8).pack(side="left", padx=(6, 0))

    actions = ttk.LabelFrame(left, text="Operations")
    actions.pack(fill="both", expand=True)

    self.buttons: list[ttk.Button] = []
    self.always_enabled_buttons: list[ttk.Button] = []
    specs = [
        ("Choose WAV", self.choose_wav, False),
        ("Reset default WAV", self.reset_wav, False),
        (
            "Analyze WAV",
            lambda: self.run_task(
                "Analyze WAV", lambda: wf.run_analyze_wav(self.session, skip_music_context=True)
            ),
            False,
        ),
        (
            "Track summary",
            lambda: self.run_task("Track summary", lambda: wf.run_track_summary(self.session)),
            False,
        ),
        (
            "Music context",
            lambda: self.run_task("Music context", lambda: wf.run_music_context(self.session)),
            False,
        ),
        (
            "Code context + indexAI",
            lambda: self.run_task(
                "Code context + indexAI", lambda: wf.run_code_context(self.session)
            ),
            False,
        ),
        (
            "Rebuild indexAI",
            lambda: self.run_task(
                "Rebuild indexAI", lambda: wf.run_project_ai_index(self.session, force=True)
            ),
            False,
        ),
        (
            "Full audio prepare",
            lambda: self.run_task(
                "Full audio prepare", lambda: wf.run_full_audio_prepare(self.session)
            ),
            False,
        ),
        ("Index manuals", self.index_manuals, False),
        ("Dual AI plan", self.dual_ai_plan, False),
        ("Scene director chat", self.scene_director_chat, False),
        ("Dual AI scene script", self.dual_ai_draft, False),
        ("Cleanup intermedi", self.cleanup_intermediates, False),
        ("Cleanup render frames", self.cleanup_render_frames, False),
        ("Toggle debug", self.toggle_debug, True),
        ("Open log panel", self.open_log_window, True),
        ("Advanced debug check", self.open_advanced_debug_window, True),
        ("Startup service check", self.startup_service_check, True),
        ("Project stats", self.open_project_stats_window, True),
        ("Artifact browser", self.open_artifact_browser_window, True),
        ("Debug monitor shell", self.open_debug_monitor_shell, True),
        ("Mark interrupted", self.mark_interrupted, True),
        ("Refresh", self.refresh_session, True),
    ]

    for label, command, always_enabled in specs:
        button = ttk.Button(actions, text=label, command=command)
        button.pack(fill="x", padx=8, pady=3)
        if always_enabled:
            self.always_enabled_buttons.append(button)
        else:
            self.buttons.append(button)

    output_frame = ttk.LabelFrame(right, text="Live Output")
    output_frame.pack(fill="both", expand=True, pady=(10, 0))
    self.output = tk.Text(output_frame, wrap="word")
    self.output.pack(fill="both", expand=True, padx=6, pady=6)
