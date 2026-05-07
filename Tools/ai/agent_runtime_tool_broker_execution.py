#!/usr/bin/env python3
"""Execution helper for the report-only runtime tool broker."""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import perf_counter


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


def execute_command_timed(command: list[str], repo_root: Path, timeout_seconds: int) -> TimedCommandResult:
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
        return TimedCommandResult(
            returncode=completed.returncode,
            stdout_tail=completed.stdout[-12000:],
            stderr_tail=completed.stderr[-12000:],
            error="",
            started_at=started_at,
            finished_at=now_iso(),
            elapsed_seconds=round(max(0.0, perf_counter() - start), 3),
        )
    except subprocess.TimeoutExpired as exc:
        return TimedCommandResult(
            returncode=124,
            stdout_tail=exc.stdout or "",
            stderr_tail=exc.stderr or "",
            error=f"TimeoutExpired: {timeout_seconds}s",
            started_at=started_at,
            finished_at=now_iso(),
            elapsed_seconds=round(max(0.0, perf_counter() - start), 3),
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
        )
