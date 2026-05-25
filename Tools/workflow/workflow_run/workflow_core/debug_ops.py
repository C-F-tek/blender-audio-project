"""Debug and operation-list helpers for the workflow surface."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .process import finish_session_operation
from .state import (
    NPU_PYTHON,
    PROJECT_DIR,
    OperationResult,
    append_event,
    load_session,
    now_iso,
    save_operation_result,
)


def run_advanced_debug_check(probe_write: bool = True) -> str:
    from Tools.workflow.workflow_run.workflow_debug_core.formatting import format_debug_report
    from Tools.workflow.workflow_run.workflow_debug_core.report import build_debug_report

    report = build_debug_report(probe_write=probe_write)
    return format_debug_report(report)


def run_startup_service_check() -> str:
    from Tools.workflow.workflow_run.startup_check_core.report import build_report, format_report, save_report

    report = build_report(PROJECT_DIR, PROJECT_DIR.parent)
    save_report(report)
    return format_report(report)


def _powershell_quote(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def open_debug_monitor_window(
    interval: float = 3.0,
    probe_write: bool = True,
) -> subprocess.Popen:
    py = NPU_PYTHON if NPU_PYTHON.exists() else Path(sys.executable)
    args = [
        _powershell_quote(py),
        "-m",
        "Tools.workflow",
        "workflow_debug",
        "--watch",
        "--interval",
        str(max(1.0, interval)),
    ]
    if not probe_write:
        args.append("--no-write-probe")
    command = [
        "powershell",
        "-NoExit",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        "& " + " ".join(args),
    ]
    creationflags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    process = subprocess.Popen(command, cwd=str(PROJECT_DIR), creationflags=creationflags)
    append_event(
        "debug_monitor",
        "opened",
        {
            "pid": process.pid,
            "interval": interval,
            "probe_write": probe_write,
            "command": "python -m Tools.validation validator_unico --mode quick --section workflow_debug",
        },
    )
    return process


def mark_active_operation_interrupted(reason: str = "manual interrupt") -> OperationResult:
    from Tools.workflow.workflow_run.workflow_debug_core.status import detect_active_operation, read_events

    session = load_session(create=True)
    active = detect_active_operation(read_events())
    operation = active.get("operation") or session.last_operation or "unknown_operation"
    result = OperationResult(
        operation=str(operation),
        ok=False,
        started_at=str(active.get("started_at") or now_iso()),
        ended_at=now_iso(),
        elapsed_sec=round(float(active.get("elapsed_sec") or 0.0), 4),
        command=(active.get("payload") or {}).get("command"),
        cwd=str(PROJECT_DIR),
        returncode=130,
        stdout_tail="",
        error=reason,
        metadata={"marked_interrupted": True, "reason": reason},
    )
    save_operation_result(result)
    finish_session_operation(session, f"{operation}_interrupted")
    return result


def available_operations() -> list[dict]:
    return [
        {"id": "set_wav", "label": "Scegli WAV", "gui_ready": True, "heavy": False},
        {"id": "reset_wav", "label": "Ripristina WAV default", "gui_ready": True, "heavy": False},
        {"id": "analyze_wav", "label": "Analizza WAV", "gui_ready": True, "heavy": True},
        {"id": "build_track_summary", "label": "Crea track summary", "gui_ready": True, "heavy": False},
        {"id": "build_music_context", "label": "Crea/aggiorna music context", "gui_ready": True, "heavy": False},
        {"id": "build_code_context", "label": "Crea/aggiorna code context + indexAI", "gui_ready": True, "heavy": False},
        {"id": "build_project_ai_index", "label": "Rigenera indexAI progetto", "gui_ready": True, "heavy": False},
        {"id": "full_audio_prepare", "label": "Prepara audio completo", "gui_ready": True, "heavy": True},
        {"id": "build_manual_context", "label": "Indicizza manuali locali", "gui_ready": True, "heavy": True},
        {"id": "dual_ai_plan", "label": "Dual AI plan", "gui_ready": True, "heavy": True},
        {"id": "dual_ai_implementation", "label": "Dual AI scene script draft", "gui_ready": True, "heavy": True},
        {"id": "cleanup_intermediates", "label": "Pulisci intermedi", "gui_ready": True, "heavy": False},
        {"id": "cleanup_render_frames", "label": "Pulisci frame render", "gui_ready": True, "heavy": False},
        {"id": "advanced_debug_check", "label": "Debug advanced check", "gui_ready": True, "heavy": False},
        {"id": "startup_service_check", "label": "Startup service check", "gui_ready": True, "heavy": False},
        {"id": "debug_monitor_window", "label": "Apri debug monitor", "gui_ready": True, "heavy": False},
        {"id": "mark_interrupted", "label": "Registra operazione interrotta", "gui_ready": True, "heavy": False},
    ]
