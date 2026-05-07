"""Python interpreter and subprocess environment helpers for provider mesh lanes.

The orchestrator must not accidentally fall back to the WindowsApps Python shim
when a project virtual environment is available. These helpers centralize that
selection rule so GPU1/Ollama, GPU0/OpenVINO, NPU and broker subprocesses share
the same interpreter policy.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def is_windowsapps_python(path_value: str) -> bool:
    """Return True when *path_value* points at the Microsoft Store shim."""
    normalized = str(path_value).replace("\\", "/").lower()
    return "/windowsapps/" in normalized and "python" in Path(path_value).name.lower()


def normalize_python_candidate(path_value: str) -> str:
    """Return a resolved executable path, or an empty string if invalid."""
    if not path_value:
        return ""
    candidate = Path(path_value)
    try:
        if candidate.is_file():
            return str(candidate.resolve())
    except OSError:
        return ""
    return ""


def iter_python_candidates(repo_root: Path | None = None) -> list[str]:
    """Return candidates in strict project-preferred order."""
    root = repo_root or Path.cwd()
    return [
        os.environ.get("IA_CARMINE_PYTHON", ""),
        str(root / ".venv/Scripts/python.exe"),
        str(root / "venv/Scripts/python.exe"),
        str(root / ".venv314/Scripts/python.exe"),
        normalize_python_candidate(getattr(sys, "executable", "")),
    ]


def resolve_child_python(repo_root: Path | None = None) -> str:
    """Resolve the Python executable for provider/broker subprocesses.

    Preference order:
    1. IA_CARMINE_PYTHON when it points at a real file.
    2. Project virtual environments.
    3. Current interpreter when it is not the WindowsApps shim.
    4. Last-resort generic "python".
    """
    for raw in iter_python_candidates(repo_root):
        normalized = normalize_python_candidate(raw)
        if normalized and not is_windowsapps_python(normalized):
            return normalized
    return "python"


def command_env(repo_root: Path) -> dict[str, str]:
    """Build a subprocess environment pinned to the resolved project Python."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    existing = env.get("PYTHONPATH", "")
    repo_path = str(repo_root)
    child_python = resolve_child_python(repo_root)

    env["IA_CARMINE_PYTHON"] = child_python
    env["PYTHONPATH"] = repo_path if not existing else repo_path + os.pathsep + existing

    python_path = Path(child_python)
    if python_path.is_file():
        env["PATH"] = str(python_path.resolve().parent) + os.pathsep + env.get("PATH", "")
    return env
