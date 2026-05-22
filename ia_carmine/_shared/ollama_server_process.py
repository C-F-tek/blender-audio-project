from __future__ import annotations

import os
import subprocess
from typing import Any
from urllib.parse import urlparse


def ollama_host_env(base_url: str) -> str:
    parsed = urlparse(str(base_url or ""))
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}"
    return str(base_url or "")


def ollama_listen_pid(base_url: str) -> int | None:
    parsed = urlparse(ollama_host_env(base_url))
    if os.name != "nt" or not parsed.port:
        return None
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            f"Get-NetTCPConnection -State Listen -LocalPort {int(parsed.port)} "
            "-ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty OwningProcess"
        ),
    ]
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=5, check=False)
    except Exception:
        return None
    if completed.returncode != 0:
        return None
    try:
        pid = int((completed.stdout or "").strip().splitlines()[0])
    except (IndexError, ValueError):
        return None
    return pid if pid > 0 else None


def server_process_evidence(base_url: str) -> dict[str, Any]:
    pid = ollama_listen_pid(base_url)
    return {
        "ollama_base_url": ollama_host_env(base_url),
        "ollama_server_pid": pid,
        "ollama_server_pid_detected": bool(pid),
    }
