"""Process watchdog helpers for heap runtime completeness smoke."""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any

from ia_carmine._shared.process_tree import terminate_process_tree


def outer_watchdog_seconds(timeout_seconds: int) -> int:
    return max(0, int(timeout_seconds))


def derived_idle_stall_seconds(timeout_seconds: int, explicit_seconds: int) -> int:
    if explicit_seconds > 0:
        return int(explicit_seconds)
    if timeout_seconds <= 0:
        return 0
    return max(1, outer_watchdog_seconds(timeout_seconds) // 5)


def run_dir_signature(run_dir: Path, ignored_names: set[str]) -> tuple[int, int, float]:
    count = 0
    total_size = 0
    latest_mtime = 0.0
    for path in run_dir.rglob("*"):
        if not path.is_file() or path.name in ignored_names:
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        count += 1
        total_size += int(stat.st_size)
        latest_mtime = max(latest_mtime, float(stat.st_mtime))
    return count, total_size, latest_mtime


def run_with_progress_watch(
    command: list[str],
    *,
    repo_root: Path,
    env: dict[str, str],
    run_dir: Path,
    timeout_seconds: int,
    idle_stall_seconds: int,
) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
    stdout_path = run_dir / "smoke_child_stdout.txt"
    stderr_path = run_dir / "smoke_child_stderr.txt"
    ignored_names = {stdout_path.name, stderr_path.name}
    outer_seconds = outer_watchdog_seconds(timeout_seconds)
    idle_seconds = derived_idle_stall_seconds(timeout_seconds, idle_stall_seconds)
    started = time.monotonic()
    last_progress = started
    last_signature = run_dir_signature(run_dir, ignored_names)
    reason = "finished"
    with stdout_path.open("w", encoding="utf-8", errors="replace") as stdout_file:
        with stderr_path.open("w", encoding="utf-8", errors="replace") as stderr_file:
            process = subprocess.Popen(
                command,
                cwd=repo_root,
                env=env,
                stdout=stdout_file,
                stderr=stderr_file,
                text=True,
            )
            while process.poll() is None:
                now = time.monotonic()
                signature = run_dir_signature(run_dir, ignored_names)
                if signature != last_signature:
                    last_signature = signature
                    last_progress = now
                if outer_seconds > 0 and now - started >= outer_seconds:
                    reason = f"outer watchdog expired after {outer_seconds}s"
                    terminate_process_tree(process)
                    break
                if idle_seconds > 0 and now - last_progress >= idle_seconds:
                    reason = f"idle stall: no run artifact progress for {idle_seconds}s"
                    terminate_process_tree(process)
                    break
                time.sleep(0.2)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                terminate_process_tree(process)
                reason = f"{reason}; cleanup timeout"
    stdout = stdout_path.read_text(encoding="utf-8", errors="replace")
    stderr = stderr_path.read_text(encoding="utf-8", errors="replace")
    returncode = process.returncode if reason == "finished" else 124
    if reason != "finished":
        stderr = (stderr or "") + f"\nheap runtime smoke {reason}"
    meta = {
        "watchdog_reason": reason,
        "outer_watchdog_seconds": outer_seconds,
        "idle_stall_seconds": idle_seconds,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "last_progress_age_seconds": round(time.monotonic() - last_progress, 3),
        "stdout": stdout_path.as_posix(),
        "stderr": stderr_path.as_posix(),
    }
    return subprocess.CompletedProcess(command, returncode, stdout, stderr), meta
