from __future__ import annotations

from pathlib import Path
import sys

from git_auto_push import run_auto_push_generated_data
from workflow_state import (
    DEFAULT_WAV,
    EVENT_LOG_PATH,
    LAST_RESULT_PATH,
    SESSION_PATH,
    build_project_storage_stats,
    format_project_storage_stats,
    load_session,
    operation_status,
    run_project_ai_index,
)


def print_header(session) -> None:
    status = operation_status(session)
    print("\n" + "=" * 72)
    print("SPAZIOTEMPO INDEX / GENERATED DATA SHELL")
    print("=" * 72)
    print(f"Sessione: {SESSION_PATH}")
    print(f"WAV:      {session.artifacts['audio_path']}")
    print(f"Track:    {session.track_stem}")
    print(f"Default:  {'no, sessione attiva' if session.use_session_track else 'si'}")
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


def ask_bool(prompt: str, default: bool = False) -> bool:
    suffix = "S/n" if default else "s/N"
    value = input(f"{prompt} ({suffix}): ").strip().lower()
    if not value:
        return default
    return value in {"s", "si", "y", "yes", "true", "1"}


def menu() -> None:
    print("\nOperazioni index / generated data:")
    print("  1  Rigenera indexAI progetto")
    print("  2  Push generated data")
    print("  3  Push generated data + output JSON")
    print("  4  Dry-run push generated data")
    print("  5  Project storage stats")
    print("  0  Esci")
    print("\nNota: per tutte le altre operazioni usa workflow_shell.py o workflow_shell.ps1 originale.")


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
                force = ask_bool("Forzare rebuild anche se cache valida?", default=True)
                run_project_ai_index(session, force=force)
                session = load_session()

            elif choice == "2":
                run_auto_push_generated_data(include_output_json=False)
                session = load_session()

            elif choice == "3":
                run_auto_push_generated_data(include_output_json=True)
                session = load_session()

            elif choice == "4":
                include_output = ask_bool("Includere output JSON nel dry-run?", default=True)
                run_auto_push_generated_data(include_output_json=include_output, dry_run=True, check=False)
                session = load_session()

            elif choice == "5":
                print(format_project_storage_stats(build_project_storage_stats(session)))

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
