"""Python interpreter and subprocess environment helpers for provider mesh lanes.

The orchestrator must not silently choose a Python runtime. These helpers
centralize the rule that provider/broker subprocesses use an operator-provided
runtime only.
"""

from __future__ import annotations

import os
from pathlib import Path

from ia_carmine._shared.ollama_provider_selection import controlled_ollama_env_fields


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
    """Return explicitly configured provider Python candidates only."""
    _ = repo_root
    return [
        os.environ.get("IA_CARMINE_PYTHON", ""),
        os.environ.get("SPAZIOTEMPO_NPU_PYTHON", ""),
    ]


def resolve_child_python(repo_root: Path | None = None) -> str:
    """Resolve the Python executable for provider/broker subprocesses.

    Preference order:
    1. IA_CARMINE_PYTHON when it points at a real file.
    2. SPAZIOTEMPO_NPU_PYTHON when it points at a real file.
    """
    for raw in iter_python_candidates(repo_root):
        normalized = normalize_python_candidate(raw)
        if normalized and not is_windowsapps_python(normalized):
            return normalized
    raise RuntimeError("provider_python_explicit_required: set IA_CARMINE_PYTHON")


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
    for key, value in controlled_ollama_env_fields().items():
        env.setdefault(key, value)
    return env
