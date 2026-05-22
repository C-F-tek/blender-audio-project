"""Canonical Ollama runtime configuration for IA-Carmine."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

DEFAULT_MODELS = (
    "qwen3-coder:latest",
    "autumnzsd/qwen2.5-coder-tools:latest",
    "qwen2.5-coder:14b",
)
DEFAULT_OLLAMA_THREAD_FRACTION = 0.85
DEFAULT_OLLAMA_NUM_CTX = 16384
DEFAULT_OLLAMA_INACTIVITY_UNLOAD = "120s"


def normalize_base_url(value: str | None) -> str:
    base_url = value or "http://127.0.0.1:11434"
    if not base_url.startswith(("http://", "https://")):
        base_url = "http://" + base_url
    return base_url.rstrip("/")


DEFAULT_BASE_URL = normalize_base_url(
    os.environ.get("OLLAMA_API_BASE") or os.environ.get("OLLAMA_HOST")
)


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


def bounded_keep_alive(
    value: str | int | float | None,
    *,
    default: str = DEFAULT_OLLAMA_INACTIVITY_UNLOAD,
    max_seconds: int = 120,
) -> str:
    text = str(value if value is not None else "").strip().lower()
    if text in {"", "default", "auto"}:
        return default
    if text in {"0", "0s"}:
        return "0s"
    seconds = _keep_alive_seconds(text)
    if seconds is None:
        return default
    return f"{min(seconds, max_seconds)}s"


def _keep_alive_seconds(text: str) -> int | None:
    units = {"s": 1, "m": 60, "h": 3600}
    suffix = text[-1:] if text else ""
    number = text[:-1] if suffix in units else text
    try:
        value = float(number)
    except ValueError:
        return None
    factor = units.get(suffix, 1)
    return max(0, int(value * factor))


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in (current, *current.parents):
        if (parent / ".git").exists():
            return parent
    return current.parents[3]


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


def start_server(
    ollama_exe: Path,
    base_url: str = DEFAULT_BASE_URL,
    startup_timeout: float = 20.0,
) -> subprocess.Popen:
    from ia_carmine.providers.ollama.sdk_client import OllamaSdkClient
    from ia_carmine._shared.ollama_server_process import ollama_host_env

    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    env = os.environ.copy()
    env["OLLAMA_HOST"] = ollama_host_env(base_url)
    process = subprocess.Popen(
        [str(ollama_exe), "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
        env=env,
    )
    deadline = time.time() + startup_timeout
    client = OllamaSdkClient(base_url)
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Ollama server stopped during startup.")
        if client.is_ready():
            return process
        time.sleep(0.5)
    raise TimeoutError("Ollama server did not become ready in time.")


def list_models_from_disk() -> list[str]:
    root = manifest_root()
    if not root.exists():
        return []
    names = []
    for manifest in root.rglob("*"):
        if not manifest.is_file():
            continue
        rel = manifest.relative_to(root).parts
        if len(rel) < 4:
            continue
        registry = rel[0]
        namespace = rel[1]
        model_name = "/".join(rel[2:-1])
        tag = rel[-1]
        if registry == "registry.ollama.ai" and namespace == "library":
            names.append(f"{model_name}:{tag}")
        elif registry == "registry.ollama.ai":
            names.append(f"{namespace}/{model_name}:{tag}")
        else:
            names.append(f"{namespace}/{model_name}:{tag}")
    return sorted(set(names))


def choose_model(preferred_model: str | None, available_models: list[str]) -> str:
    if preferred_model and preferred_model in available_models:
        return preferred_model
    for model in DEFAULT_MODELS:
        if model in available_models:
            return model
    if available_models:
        return available_models[0]
    wanted = preferred_model or " or ".join(DEFAULT_MODELS)
    raise RuntimeError(f"No Ollama models are available. Install or pull: {wanted}")
