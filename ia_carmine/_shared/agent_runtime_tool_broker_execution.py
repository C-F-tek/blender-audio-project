#!/usr/bin/env python3
"""Execution helper for the report-only runtime tool broker."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import perf_counter

from ia_carmine._shared.file_backed_transport import artifact_ref


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass(frozen=True)
class TimedCommandResult:
    returncode: int
    stdout_tail: str
    stderr_tail: str
    error: str
    started_at: str
    finished_at: str
    elapsed_seconds: float
    stdout_ref: dict | None = None
    stderr_ref: dict | None = None
    stdout_chars: int = 0
    stderr_chars: int = 0


def execute_command_timed(
    command: list[str],
    repo_root: Path,
    timeout_seconds: int,
    output_dir: Path | None = None,
    name: str = "command",
) -> TimedCommandResult:
    started_at = now_iso()
    start = perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        stdout_text = completed.stdout or ""
        stderr_text = completed.stderr or ""
        stdout_ref, stderr_ref = _write_io_refs(repo_root, output_dir, name, stdout_text, stderr_text)
        return TimedCommandResult(
            returncode=completed.returncode,
            stdout_tail=stdout_text[-12000:],
            stderr_tail=stderr_text[-12000:],
            error="",
            started_at=started_at,
            finished_at=now_iso(),
            elapsed_seconds=round(max(0.0, perf_counter() - start), 3),
            stdout_ref=stdout_ref,
            stderr_ref=stderr_ref,
            stdout_chars=len(stdout_text),
            stderr_chars=len(stderr_text),
        )
    except subprocess.TimeoutExpired as exc:
        stdout_text = str(exc.stdout or "")
        stderr_text = str(exc.stderr or "")
        stdout_ref, stderr_ref = _write_io_refs(repo_root, output_dir, name, stdout_text, stderr_text)
        return TimedCommandResult(
            returncode=124,
            stdout_tail=stdout_text[-12000:],
            stderr_tail=stderr_text[-12000:],
            error=f"TimeoutExpired: {timeout_seconds}s",
            started_at=started_at,
            finished_at=now_iso(),
            elapsed_seconds=round(max(0.0, perf_counter() - start), 3),
            stdout_ref=stdout_ref,
            stderr_ref=stderr_ref,
            stdout_chars=len(stdout_text),
            stderr_chars=len(stderr_text),
        )
    except Exception as exc:  # noqa: BLE001 - broker report must capture failure.
        return TimedCommandResult(
            returncode=1,
            stdout_tail="",
            stderr_tail="",
            error=f"{type(exc).__name__}: {exc}",
            started_at=started_at,
            finished_at=now_iso(),
            elapsed_seconds=round(max(0.0, perf_counter() - start), 3),
            stdout_ref={},
            stderr_ref={},
            stdout_chars=0,
            stderr_chars=0,
        )


def _write_io_refs(
    repo_root: Path,
    output_dir: Path | None,
    name: str,
    stdout_text: str,
    stderr_text: str,
) -> tuple[dict, dict]:
    if output_dir is None:
        return {}, {}
    output_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = output_dir / f"{name}_stdout.txt"
    stderr_path = output_dir / f"{name}_stderr.txt"
    stdout_path.write_text(stdout_text, encoding="utf-8")
    stderr_path.write_text(stderr_text, encoding="utf-8")
    return (
        artifact_ref(stdout_path, repo_root, kind="tool_stdout", producer="agent_runtime_tool_broker", ref_id=f"{name}_stdout"),
        artifact_ref(stderr_path, repo_root, kind="tool_stderr", producer="agent_runtime_tool_broker", ref_id=f"{name}_stderr"),
    )
