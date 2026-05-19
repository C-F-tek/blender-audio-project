"""HTTP and process helpers for Ollama."""

from __future__ import annotations

import json
import subprocess
import time
import urllib.request
from collections.abc import Iterator
from pathlib import Path

from .config import DEFAULT_BASE_URL, DEFAULT_MODELS, manifest_root


def json_request(
    base_url: str,
    path: str,
    payload: dict | None = None,
    timeout: float = 10.0,
) -> dict:
    url = base_url.rstrip("/") + path
    data = None
    headers = {}
    method = "GET"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
        method = "POST"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
    return json.loads(raw) if raw else {}


def stream_json_request(
    base_url: str,
    path: str,
    payload: dict,
    timeout: float = 10.0,
) -> Iterator[dict]:
    url = base_url.rstrip("/") + path
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        for raw_line in response:
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(item, dict):
                yield item


def is_server_ready(base_url: str = DEFAULT_BASE_URL, timeout: float = 2.0) -> bool:
    try:
        json_request(base_url, "/api/tags", timeout=timeout)
    except Exception:
        return False
    return True


def list_models(base_url: str = DEFAULT_BASE_URL) -> list[str]:
    data = json_request(base_url, "/api/tags", timeout=8.0)
    models = data.get("models", [])
    names = []
    for item in models:
        name = item.get("name") if isinstance(item, dict) else None
        if name:
            names.append(str(name))
    return names


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


def start_server(
    ollama_exe: Path,
    base_url: str = DEFAULT_BASE_URL,
    startup_timeout: float = 20.0,
) -> subprocess.Popen:
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    process = subprocess.Popen(
        [str(ollama_exe), "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    deadline = time.time() + startup_timeout
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Ollama server stopped during startup.")
        if is_server_ready(base_url):
            return process
        time.sleep(0.5)
    raise TimeoutError("Ollama server did not become ready in time.")


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
