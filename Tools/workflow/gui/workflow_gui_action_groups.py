from __future__ import annotations

from components.action_panel import ActionGroup, ActionSpec


def build_modern_action_groups(gui) -> tuple[ActionGroup, ...]:
    return (
        ActionGroup(
            "Track setup",
            (
                ActionSpec(
                    "Choose WAV",
                    gui.choose_wav,
                    description="Seleziona un nuovo file audio WAV.",
                ),
                ActionSpec(
                    "Reset default WAV",
                    gui.reset_wav,
                    description="Torna alla traccia predefinita.",
                ),
            ),
        ),
        ActionGroup(
            "Data preparation",
            (
                ActionSpec(
                    "Analyze WAV",
                    lambda: gui.run_task(
                        "Analyze WAV",
                        lambda: gui.wf.run_analyze_wav(gui.session, skip_music_context=True),
                    ),
                    description="Genera l'analisi tecnica del WAV e i file JSON base necessari al resto del workflow.",
                ),
                ActionSpec(
                    "Track summary",
                    lambda: gui.run_task(
                        "Track summary", lambda: gui.wf.run_track_summary(gui.session)
                    ),
                    description="Crea un riassunto tecnico compatto della traccia partendo dall'analisi audio.",
                ),
                ActionSpec(
                    "Music context",
                    lambda: gui.run_task(
                        "Music context", lambda: gui.wf.run_music_context(gui.session)
                    ),
                    description="Produce un contesto musicale strutturato per le fasi IA successive.",
                ),
                ActionSpec(
                    "Full audio prepare",
                    lambda: gui.run_task(
                        "Full audio prepare", lambda: gui.wf.run_full_audio_prepare(gui.session)
                    ),
                    description="Esegue la preparazione audio completa: analisi, summary, contesto e keyframe Blender.",
                ),
            ),
        ),
        ActionGroup(
            "AI artifact pipeline",
            (
                ActionSpec(
                    "AI pipeline dry-run",
                    lambda: gui.run_ai_artifact_pipeline(dry_run=True),
                    description="Verifica preflight, profilo macchina, input disponibili, lane CPU/NPU/GPU e output attesi senza scrivere artefatti reali.",
                ),
                ActionSpec(
                    "AI artifact pipeline",
                    lambda: gui.run_ai_artifact_pipeline(dry_run=False),
                    description="Genera chunk semantici, intermedi musicali AI-friendly, candidati di mapping, review NPU leggera e validazione artefatti.",
                ),
            ),
        ),
        ActionGroup(
            "Project intelligence",
            (
                ActionSpec(
                    "Code context + indexAI",
                    lambda: gui.run_task(
                        "Code context + indexAI", lambda: gui.wf.run_code_context(gui.session)
                    ),
                    description="Aggiorna contesto codice e indici AI tradizionali usati dalla pipeline dual-AI.",
                ),
                ActionSpec(
                    "Rebuild indexAI",
                    lambda: gui.run_task(
                        "Rebuild indexAI",
                        lambda: gui.wf.run_project_ai_index(gui.session, force=True),
                    ),
                    description="Rigenera forzatamente l'indice progetto quando hai modificato codice, documentazione o strutture IA.",
                ),
                ActionSpec(
                    "Index manuals",
                    gui.index_manuals,
                    description="Indicizza manuali locali Blender/progetto con il limite file configurato.",
                ),
            ),
        ),
        ActionGroup(
            "Creative AI pipeline",
            (
                ActionSpec(
                    "Dual AI plan",
                    gui.dual_ai_plan,
                    description="Genera il piano scena strutturato usando Ollama e, se non bypassato, il vecchio passaggio NPU pesante.",
                ),
                ActionSpec(
                    "Scene director chat",
                    gui.scene_director_chat,
                    description="Apre la chat locale per affinare il brief e salvare preferenze creative persistenti.",
                ),
                ActionSpec(
                    "Dual AI scene script",
                    gui.dual_ai_draft,
                    description="Genera la bozza dello script Blender finale a partire dal piano, dal brief e dal contesto tecnico.",
                ),
            ),
        ),
        ActionGroup(
            "Review and diagnostics",
            (
                ActionSpec(
                    "Open log panel",
                    gui.open_log_window,
                    always_enabled=True,
                    description="Consulta eventi workflow, ultimo risultato e log operativi.",
                ),
                ActionSpec(
                    "Advanced debug check",
                    gui.open_advanced_debug_window,
                    always_enabled=True,
                    description="Esegue controlli diagnostici avanzati su percorsi, scrittura file e stato progetto.",
                ),
                ActionSpec(
                    "Startup service check",
                    gui.startup_service_check,
                    always_enabled=True,
                    description="Verifica i servizi locali necessari al workflow, inclusi runtime e modelli quando disponibili.",
                ),
                ActionSpec(
                    "Project stats",
                    gui.open_project_stats_window,
                    always_enabled=True,
                    description="Apre la dashboard di spazio occupato e riepilogo delle aree del progetto.",
                ),
                ActionSpec(
                    "Debug monitor shell",
                    gui.open_debug_monitor_shell,
                    always_enabled=True,
                    description="Apre un monitor debug in una shell separata con aggiornamento periodico.",
                ),
            ),
        ),
        ActionGroup(
            "Maintenance",
            (
                ActionSpec(
                    "Cleanup intermedi",
                    gui.cleanup_intermediates,
                    description="Rimuove intermedi generati in modo controllato, preservando audio e render finali.",
                ),
                ActionSpec(
                    "Cleanup render frames",
                    gui.cleanup_render_frames,
                    description="Pulisce la directory dei frame render della traccia corrente, mantenendo gli MP4 finali.",
                ),
                ActionSpec(
                    "Toggle debug",
                    gui.toggle_debug,
                    always_enabled=True,
                    description="Abilita o disabilita il logging dettagliato del workflow.",
                ),
                ActionSpec(
                    "Mark interrupted",
                    gui.mark_interrupted,
                    always_enabled=True,
                    description="Marca manualmente l'operazione corrente come interrotta nei log di workflow.",
                ),
                ActionSpec(
                    "Refresh",
                    gui.refresh_session,
                    always_enabled=True,
                    description="Aggiorna lo stato della sessione e la lista degli output rilevati.",
                ),
            ),
        ),
    )
