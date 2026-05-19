"""Subprocess execution helpers for workflow operations."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from .state import (
    AUDIO_PYTHON,
    LAST_RESULT_PATH,
    NPU_PYTHON,
    PROJECT_DIR,
    WorkflowSession,
    append_event,
    load_session,
    now_iso,
    save_operation_result,
    OperationResult,
)


def python_executable() -> Path:
    if NPU_PYTHON.exists():
        result = run_command(
            [str(NPU_PYTHON), "-c", "print('ok')"],
            operation="probe_python",
            check=False,
            echo=False,
            debug=False,
            print_output=False,
            log=False,
        )
        if result.ok:
            return NPU_PYTHON
    return Path(sys.executable)


def audio_python_executable() -> Path:
    if AUDIO_PYTHON.exists():
        result = run_command(
            [str(AUDIO_PYTHON), "-c", "import librosa, numpy, matplotlib; print('audio ok')"],
            operation="probe_audio_python",
            check=False,
            echo=False,
            debug=False,
            print_output=False,
            log=False,
        )
        if result.ok:
            return AUDIO_PYTHON

    fallback = Path(sys.executable)
    result = run_command(
        [str(fallback), "-c", "import librosa, numpy, matplotlib; print('audio ok')"],
        operation="probe_audio_python_fallback",
        check=False,
        echo=False,
        debug=False,
        print_output=False,
        log=False,
    )
    if result.ok:
        return fallback

    raise RuntimeError(
        "Runtime audio non disponibile: serve un Python con librosa, numpy e matplotlib. "
        f"Atteso: {AUDIO_PYTHON}"
    )


def run_command(
    command: list[str],
    operation: str = "command",
    check: bool = True,
    echo: bool = True,
    debug: bool | None = None,
    print_output: bool = True,
    metadata: dict | None = None,
    log: bool = True,
) -> OperationResult:
    session_debug = load_session(create=False).debug_enabled if debug is None else debug
    started_at = now_iso()
    start = time.perf_counter()
    cwd = str(PROJECT_DIR)
    metadata = metadata or {}

    if log:
        append_event(
            operation,
            "start",
            {"command": command, "cwd": cwd, "metadata": metadata, "debug": session_debug},
        )

    if echo:
        print("\n$ " + " ".join(f'"{part}"' if " " in part else part for part in command))
    if session_debug:
        print(f"[DEBUG] operation={operation}")
        print(f"[DEBUG] cwd={cwd}")
        print(f"[DEBUG] metadata={json.dumps(metadata, ensure_ascii=False)}")

    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout or ""
    if output and print_output:
        print(output.rstrip())

    op_result = OperationResult(
        operation=operation,
        ok=result.returncode == 0,
        started_at=started_at,
        ended_at=now_iso(),
        elapsed_sec=round(time.perf_counter() - start, 4),
        command=command,
        cwd=cwd,
        returncode=result.returncode,
        stdout_tail=output[-8000:],
        metadata=metadata,
    )

    if log:
        save_operation_result(op_result)

    if session_debug:
        print(f"[DEBUG] returncode={result.returncode}")
        print(f"[DEBUG] elapsed_sec={op_result.elapsed_sec}")
        print(f"[DEBUG] last_result={LAST_RESULT_PATH}")

    if check and result.returncode != 0:
        op_result.error = f"Comando fallito con exit code {result.returncode}"
        if log:
            save_operation_result(op_result)
        raise RuntimeError(op_result.error)

    return op_result


def finish_session_operation(session: WorkflowSession, operation: str) -> None:
    session.last_operation = operation
    session.last_result_path = str(LAST_RESULT_PATH)
    session.save()
