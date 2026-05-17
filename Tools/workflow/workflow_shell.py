from __future__ import annotations

import sys
from pathlib import Path

from artifact_consult import collect_artifacts, format_artifact_table, open_artifact
from git_auto_push import run_auto_push_generated_data
from workflow_state import (
    DEFAULT_WAV,
    EVENT_LOG_PATH,
    LAST_RESULT_PATH,
    SESSION_PATH,
    available_ollama_models,
    build_project_storage_stats,
    cleanup_intermediate_targets,
    cleanup_intermediates,
    cleanup_render_frame_targets,
    cleanup_render_frames,
    format_project_storage_stats,
    load_session,
    mark_active_operation_interrupted,
    open_debug_monitor_window,
    operation_status,
    reset_to_default_wav,
    run_advanced_debug_check,
    run_analyze_wav,
    run_code_context,
    run_dual_ai,
    run_full_audio_prepare,
    run_manual_index,
    run_music_context,
    run_project_ai_index,
    run_scene_director_brief,
    run_startup_service_check,
    run_track_summary,
    set_ai_models,
    set_current_wav,
    set_debug_enabled,
)


def print_header(session) -> None:
    status = operation_status(session)
    print("\n" + "=" * 72)
    print("SPAZIOTEMPO WORKFLOW SHELL")
    print("=" * 72)
    print(f"Sessione: {SESSION_PATH}")
    print(f"WAV:      {session.artifacts['audio_path']}")
    print(f"Track:    {session.track_stem}")
    print(f"Default:  {'no, sessione attiva' if session.use_session_track else 'si'}")
    print(f"Debug:    {'ON' if session.debug_enabled else 'OFF'}")
    print(
        f"AI:       creative={session.creative_model} | technical={session.technical_model} | chat={session.chat_model} | tokens={session.script_max_tokens}"
    )
    print(f"Ultima:   {session.last_operation or '-'}")
    print(f"Log:      {EVENT_LOG_PATH}")
    print(f"Result:   {LAST_RESULT_PATH}")
    print("\nOutput principali:")
    for key in [
        "analysis_json",
        "track_summary_json",
        "music_context_json",
        "analysis_ai_context_json",
        "blender_keyframes_json",
        "dual_ai_plan_json",
        "scene_brief_json",
        "asset_inventory_json",
        "ai_implementation_draft_json",
        "generated_scene_script",
    ]:
        mark = "OK" if status.get(key) else "--"
        print(f"  [{mark}] {key}: {session.artifacts[key]}")


def ask_path(prompt: str) -> str:
    return input(prompt).strip().strip('"')


def ask_bool(prompt: str, default: bool = False) -> bool:
    suffix = "S/n" if default else "s/N"
    value = input(f"{prompt} ({suffix}): ").strip().lower()
    if not value:
        return default
    return value in {"s", "si", "y", "yes", "true", "1"}


def menu() -> None:
    print("\nOperazioni:")
    print("  1  Scegli WAV")
    print("  2  Ripristina WAV default")
    print("  3  Analizza WAV")
    print("  4  Crea track summary")
    print("  5  Crea/aggiorna music context")
    print("  6  Crea/aggiorna code context + indexAI")
    print("  7  Prepara audio completo (3+4+5+6+manual root)")
    print("  8  Indicizza manuali locali")
    print("  9  Dual AI plan")
    print("  10 Dual AI scene script draft")
    print("  11 Push dati strutturati generati su GitHub")
    print("  12 Mostra sessione")
    print("  13 Toggle debug dettagliato")
    print("  14 Pulisci intermedi")
    print("  15 Pulisci frame render")
    print("  16 Debug advanced check")
    print("  17 Apri debug monitor finestra")
    print("  18 Registra operazione interrotta")
    print("  19 Rigenera indexAI progetto")
    print("  20 Scene director chat / modifica brief")
    print("  21 Project storage stats")
    print("  22 Consulta/apri artefatti prodotti")
    print("  23 Configura modelli AI")
    print("  24 Startup service check")
    print("  0  Esci")


def choose_model(prompt: str, current: str) -> str:
    models = available_ollama_models()
    print(f"\n{prompt}")
    if models:
        for idx, model in enumerate(models, start=1):
            mark = " *" if model == current else ""
            print(f"  {idx}. {model}{mark}")
    value = input(f"Modello [{current}]: ").strip()
    if not value:
        return current
    if value.isdigit() and models:
        idx = int(value)
        if 1 <= idx <= len(models):
            return models[idx - 1]
    return value


def confirm_cleanup(title: str, targets: dict) -> bool:
    files = targets.get("files", [])
    dirs = targets.get("dirs", [])
    print(f"\n{title}")
    print(f"File da eliminare: {len(files)}")
    for item in files[:20]:
        print(f"  FILE {item}")
    if len(files) > 20:
        print(f"  ... altri {len(files) - 20} file")

    print(f"Cartelle da eliminare: {len(dirs)}")
    for item in dirs[:20]:
        print(f"  DIR  {item}")
    if len(dirs) > 20:
        print(f"  ... altre {len(dirs) - 20} cartelle")

    protected = targets.get("protected_roots", [])
    if protected:
        print("\nProtetti:")
        for item in protected:
            print(f"  {item}")

    if not files and not dirs:
        print("\nNiente da pulire.")
        return False

    return ask_bool("\nConfermi eliminazione?", default=False)


def main() -> None:
    session = load_session(create=True)

    while True:
        print_header(session)
        menu()
        choice = input("\nScelta: ").strip().lower()

        try:
            if choice in {"0", "q", "quit", "exit"}:
                print("Ok, shell chiusa.")
                return

            if choice == "1":
                path = ask_path(f"Percorso WAV [{DEFAULT_WAV}]: ") or str(DEFAULT_WAV)
                session = set_current_wav(Path(path))

            elif choice == "2":
                session = reset_to_default_wav()

            elif choice == "3":
                skip_context = ask_bool("Saltare music context dopo analisi?", default=True)
                run_analyze_wav(session, skip_music_context=skip_context)
                session = load_session()

            elif choice == "4":
                run_track_summary(session)
                session = load_session()

            elif choice == "5":
                run_music_context(session)
                session = load_session()

            elif choice == "6":
                run_code_context(session)
                session = load_session()

            elif choice == "7":
                run_full_audio_prepare(session)
                session = load_session()

            elif choice == "8":
                limit_raw = input("Numero massimo file manuale da indicizzare [80]: ").strip()
                limit = int(limit_raw) if limit_raw else 80
                run_manual_index(session, limit_files=limit)
                session = load_session()

            elif choice == "9":
                include_manual = ask_bool("Includere manuali?", default=False)
                skip_ollama = ask_bool("Saltare Ollama?", default=False)
                skip_npu = ask_bool(
                    "Saltare NPU heavy pass? La capsule service viene comunque creata", default=True
                )
                run_dual_ai(
                    session,
                    phase="plan",
                    include_manual=include_manual,
                    skip_npu=skip_npu,
                    skip_ollama=skip_ollama,
                )
                session = load_session()

            elif choice == "10":
                include_manual = ask_bool("Includere manuali?", default=True)
                skip_npu = ask_bool(
                    "Saltare NPU heavy pass? La capsule service viene comunque creata", default=True
                )
                run_dual_ai(
                    session,
                    phase="implementation",
                    include_manual=include_manual,
                    skip_npu=skip_npu,
                )
                session = load_session()

            elif choice == "11":
                pull_first = ask_bool("Fare pull --ff-only prima del push?", default=True)
                dry_run = ask_bool("Eseguire solo dry-run senza commit/push?", default=False)
                include_docs = ask_bool("Includere anche docs?", default=False)
                run_auto_push_generated_data(
                    include_output_json=True,
                    include_docs=include_docs,
                    pull_first=pull_first,
                    dry_run=dry_run,
                )
                session = load_session()

            elif choice == "12":
                pass

            elif choice == "13":
                session = set_debug_enabled(not session.debug_enabled)
                print(f"Debug dettagliato: {'ON' if session.debug_enabled else 'OFF'}")

            elif choice == "14":
                targets = cleanup_intermediate_targets(
                    session, include_all_tracks=True, include_logs=True
                )
                if confirm_cleanup("Pulizia intermedi progetto", targets):
                    result = cleanup_intermediates(
                        session, include_all_tracks=True, include_logs=True
                    )
                    print(
                        f"Eliminati: {result.metadata.get('deleted_count', 0) if result.metadata else 0}"
                    )
                    session = load_session()

            elif choice == "15":
                targets = cleanup_render_frame_targets(session)
                if confirm_cleanup("Pulizia frame render", targets):
                    result = cleanup_render_frames(session)
                    print(
                        f"Eliminati: {result.metadata.get('deleted_count', 0) if result.metadata else 0}"
                    )
                    session = load_session()

            elif choice == "16":
                print(run_advanced_debug_check(probe_write=True))

            elif choice == "17":
                process = open_debug_monitor_window(interval=3.0, probe_write=True)
                print(f"Debug monitor aperto in una nuova finestra. PID: {process.pid}")

            elif choice == "18":
                result = mark_active_operation_interrupted("manual interrupt from workflow shell")
                print(f"Registrata interruzione: {result.operation}, elapsed={result.elapsed_sec}s")
                session = load_session()

            elif choice == "19":
                force = ask_bool("Forzare rebuild anche se cache valida?", default=False)
                run_project_ai_index(session, force=force)
                session = load_session()

            elif choice == "20":
                run_scene_director_brief(session)
                session = load_session()

            elif choice == "21":
                print(format_project_storage_stats(build_project_storage_stats(session)))

            elif choice == "22":
                records = collect_artifacts(session)
                print(format_artifact_table(records))
                raw_index = input(
                    "\nIndice da aprire, F<indice> per cartella, Invio per tornare: "
                ).strip()
                if raw_index:
                    open_folder = raw_index.lower().startswith("f")
                    number_text = raw_index[1:] if open_folder else raw_index
                    opened = open_artifact(records, int(number_text), folder=open_folder)
                    print(f"Aperto: {opened.path}")

            elif choice == "23":
                creative = choose_model("Creative model per piano/visione", session.creative_model)
                technical = choose_model(
                    "Technical model per script Python Blender", session.technical_model
                )
                chat = choose_model("Chat model per direttore AI", session.chat_model)
                raw_tokens = input(f"Max token script [{session.script_max_tokens}]: ").strip()
                tokens = int(raw_tokens) if raw_tokens else session.script_max_tokens
                session = set_ai_models(
                    creative_model=creative,
                    technical_model=technical,
                    chat_model=chat,
                    script_max_tokens=tokens,
                )

            elif choice == "24":
                print(run_startup_service_check())

            else:
                print("Scelta non riconosciuta.")

        except KeyboardInterrupt:
            print("\nOperazione interrotta.")
        except Exception as exc:
            print(f"\n[ERRORE] {exc}")

        input("\nInvio per continuare...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
