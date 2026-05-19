"""Ollama runtime configuration, paths, and logging."""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def normalize_base_url(value: str | None) -> str:
    base_url = value or "http://127.0.0.1:11434"
    if not base_url.startswith(("http://", "https://")):
        base_url = "http://" + base_url
    return base_url.rstrip("/")


DEFAULT_BASE_URL = normalize_base_url(
    os.environ.get("OLLAMA_API_BASE") or os.environ.get("OLLAMA_HOST")
)
DEFAULT_MODELS = (
    "qwen3-coder:latest",
    "autumnzsd/qwen2.5-coder-tools:latest",
    "qwen2.5-coder:14b",
)
DEFAULT_OLLAMA_THREAD_FRACTION = 0.85
DEFAULT_OLLAMA_NUM_CTX = 16384


def default_ollama_num_thread() -> int:
    for env_name in ("SPAZIOTEMPO_OLLAMA_NUM_THREAD", "OLLAMA_NUM_THREAD"):
        value = os.environ.get(env_name)
        if not value:
            continue
        try:
            parsed = int(value)
        except ValueError:
            continue
        if parsed > 0:
            return parsed
    logical_cpus = os.cpu_count() or 1
    return max(1, int(logical_cpus * DEFAULT_OLLAMA_THREAD_FRACTION))


def default_ollama_num_ctx() -> int:
    for env_name in (
        "IA_CARMINE_OLLAMA_NUM_CTX",
        "SPAZIOTEMPO_OLLAMA_NUM_CTX",
        "OLLAMA_NUM_CTX",
    ):
        value = os.environ.get(env_name)
        if not value:
            continue
        try:
            parsed = int(value)
        except ValueError:
            continue
        if parsed >= 4096:
            return parsed
    return DEFAULT_OLLAMA_NUM_CTX


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def ollama_runtime_log_path() -> Path:
    return project_root() / "output" / "workflow_logs" / "ollama_runtime_events.jsonl"


def append_ollama_runtime_event(event: str, payload: dict) -> None:
    try:
        path = ollama_runtime_log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        row = {"time": now_iso(), "event": event, "payload": payload}
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception:
        pass


def ollama_home() -> Path:
    env_home = os.environ.get("OLLAMA_MODELS")
    if env_home:
        return Path(env_home).expanduser().resolve().parent
    return Path.home() / ".ollama"


def manifest_root() -> Path:
    models_dir = Path(
        os.environ.get("OLLAMA_MODELS", str(Path.home() / ".ollama" / "models"))
    ).expanduser()
    return models_dir / "manifests"


def find_ollama_exe() -> Path | None:
    env_path = os.environ.get("OLLAMA_EXE")
    candidates = []
    if env_path:
        candidates.append(Path(env_path))

    which_path = shutil.which("ollama")
    if which_path:
        candidates.append(Path(which_path))

    local_app = os.environ.get("LOCALAPPDATA")
    program_files = os.environ.get("ProgramFiles")
    user_profile = os.environ.get("USERPROFILE")

    if local_app:
        candidates.extend(
            [
                Path(local_app) / "Programs" / "Ollama" / "ollama.exe",
                Path(local_app) / "Ollama" / "ollama.exe",
                Path(local_app) / "Microsoft" / "WindowsApps" / "ollama.exe",
            ]
        )
    if program_files:
        candidates.append(Path(program_files) / "Ollama" / "ollama.exe")
    if user_profile:
        candidates.append(
            Path(user_profile) / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe"
        )

    for candidate in candidates:
        try:
            exists = candidate.exists()
        except PermissionError:
            exists = True
        if exists:
            return candidate
    return None
