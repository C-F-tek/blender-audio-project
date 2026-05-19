from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = THIS_DIR.parents[1]
WORKSPACE_ROOT = PROJECT_DIR.parent
NPU_DIR = PROJECT_DIR / "Tools" / "npu"

DEFAULT_LOG_DIR = PROJECT_DIR / "output" / "workflow_logs"
DEFAULT_REPORT_JSON = DEFAULT_LOG_DIR / "startup_check.json"

if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))
if str(NPU_DIR) not in sys.path:
    sys.path.insert(0, str(NPU_DIR))


@dataclass
class Check:
    name: str
    status: str
    detail: str
    path: str | None = None


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def add(
    checks: list[Check],
    name: str,
    status: str,
    detail: str,
    path: Path | str | None = None,
) -> None:
    checks.append(Check(name=name, status=status, detail=detail, path=str(path) if path else None))


def probe_write(path: Path) -> tuple[bool, str]:
    try:
        path.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(
            prefix=".spaziotempo_probe_",
            suffix=".tmp",
            dir=str(path),
        )
        os.close(fd)
        Path(temp_name).unlink(missing_ok=True)
        return True, "temp write ok"
    except Exception as exc:
        return False, str(exc)


def run_probe(
    command: list[str],
    timeout: float = 12.0,
    cwd: Path | None = None,
) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd or PROJECT_DIR),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except Exception as exc:
        return False, str(exc)
    output = (result.stdout or "").strip()
    return result.returncode == 0, output[-1200:] if output else f"exit={result.returncode}"


def powershell_test_path(path: Path) -> bool:
    escaped = str(path).replace("'", "''")
    ok, output = run_probe(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"if (Test-Path -LiteralPath '{escaped}') {{ 'YES' }} else {{ 'NO' }}",
        ],
        timeout=6.0,
    )
    return ok and output.strip().endswith("YES")


def powershell_get_command(name: str) -> str | None:
    ok, output = run_probe(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"$cmd = Get-Command {name} -ErrorAction SilentlyContinue; if ($cmd) {{ $cmd.Source }}",
        ],
        timeout=6.0,
    )
    return output.strip() if ok and output.strip() else None


def visible_path_exists(path: Path) -> bool:
    return path.exists() or powershell_test_path(path)


def fallback_ollama_exe() -> Path | None:
    candidates: list[Path] = []
    value = os.environ.get("OLLAMA_EXE")
    if value:
        candidates.append(Path(value))

    local_app = os.environ.get("LOCALAPPDATA")
    user_profile = os.environ.get("USERPROFILE")
    program_files = os.environ.get("ProgramFiles")
    if local_app:
        candidates.extend(
            [
                Path(local_app) / "Programs" / "Ollama" / "ollama.exe",
                Path(local_app) / "Ollama" / "ollama.exe",
            ]
        )
    if user_profile:
        candidates.append(
            Path(user_profile) / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe"
        )
    if program_files:
        candidates.append(Path(program_files) / "Ollama" / "ollama.exe")

    command_path = powershell_get_command("ollama")
    if command_path:
        candidates.append(Path(command_path))

    for candidate in candidates:
        if visible_path_exists(candidate):
            return candidate
    return None


def check_python_runtime(
    checks: list[Check],
    label: str,
    python_path: Path,
    code: str,
    timeout: float = 20.0,
) -> None:
    if not python_path.exists():
        add(checks, label, "MISS", "python.exe missing", python_path)
        return
    ok, output = run_probe([str(python_path), "-c", code], timeout=timeout)
    add(checks, label, "OK" if ok else "WARN", output or "ok", python_path)


def check_ollama(checks: list[Check]) -> None:
    try:
        from Tools.npu.provider_mesh._shared.ollama_runtime import (
            DEFAULT_BASE_URL,
            find_ollama_exe,
            is_server_ready,
            list_models,
            list_models_from_disk,
            start_server,
        )

        exe = find_ollama_exe() or fallback_ollama_exe()
        if exe:
            add(checks, "Ollama executable", "OK", str(exe), exe)
        else:
            add(checks, "Ollama executable", "MISS", "ollama.exe not found; set OLLAMA_EXE")

        ready = is_server_ready(DEFAULT_BASE_URL, timeout=2.0)
        started = False
        if not ready and exe:
            try:
                start_server(exe, DEFAULT_BASE_URL, startup_timeout=10.0)
                ready = is_server_ready(DEFAULT_BASE_URL, timeout=2.0)
                started = ready
            except Exception as exc:
                add(checks, "Ollama API autostart", "WARN", str(exc), exe)

        if ready:
            try:
                models = list_models(DEFAULT_BASE_URL)
            except Exception:
                models = list_models_from_disk()
            detail = f"{DEFAULT_BASE_URL} UP"
            if started:
                detail += " (started now)"
            detail += f"; models={', '.join(models[:8]) if models else 'none'}"
            add(checks, "Ollama API", "OK", detail)
        else:
            disk_models = list_models_from_disk()
            detail = f"{DEFAULT_BASE_URL} DOWN"
            if disk_models:
                detail += f"; disk models={', '.join(disk_models[:8])}"
            add(checks, "Ollama API", "DOWN", detail)
    except Exception as exc:
        add(checks, "Ollama runtime", "WARN", str(exc))
