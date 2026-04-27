from __future__ import annotations

from pathlib import Path
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request


def normalize_base_url(value: str | None) -> str:
    base_url = value or "http://127.0.0.1:11434"
    if not base_url.startswith(("http://", "https://")):
        base_url = "http://" + base_url
    return base_url.rstrip("/")


DEFAULT_BASE_URL = normalize_base_url(os.environ.get("OLLAMA_API_BASE") or os.environ.get("OLLAMA_HOST"))
DEFAULT_MODELS = ("qwen2.5-coder:14b", "gpt-oss:20b", "autumnzsd/qwen2.5-coder-tools:latest")


def ollama_home() -> Path:
    env_home = os.environ.get("OLLAMA_MODELS")
    if env_home:
        return Path(env_home).expanduser().resolve().parent
    return Path.home() / ".ollama"


def manifest_root() -> Path:
    models_dir = Path(os.environ.get("OLLAMA_MODELS", str(Path.home() / ".ollama" / "models"))).expanduser()
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
        candidates.append(Path(user_profile) / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe")

    for candidate in candidates:
        try:
            exists = candidate.exists()
        except PermissionError:
            exists = True
        if exists:
            return candidate

    return None


def _json_request(base_url: str, path: str, payload: dict | None = None, timeout: float = 10.0) -> dict:
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


def is_server_ready(base_url: str = DEFAULT_BASE_URL, timeout: float = 2.0) -> bool:
    try:
        _json_request(base_url, "/api/tags", timeout=timeout)
    except Exception:
        return False
    return True


def list_models(base_url: str = DEFAULT_BASE_URL) -> list[str]:
    data = _json_request(base_url, "/api/tags", timeout=8.0)
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
        model_parts = rel[2:-1]
        tag = rel[-1]
        model_name = "/".join(model_parts)

        if registry == "registry.ollama.ai" and namespace == "library":
            names.append(f"{model_name}:{tag}")
        elif registry == "registry.ollama.ai":
            names.append(f"{namespace}/{model_name}:{tag}")
        else:
            names.append(f"{namespace}/{model_name}:{tag}")

    return sorted(set(names))


def start_server(ollama_exe: Path, base_url: str = DEFAULT_BASE_URL, startup_timeout: float = 20.0) -> subprocess.Popen:
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


def strip_json_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    return stripped


def parse_json_response(text: str) -> dict:
    stripped = strip_json_fence(text)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start >= 0 and end > start:
            return json.loads(stripped[start : end + 1])
        raise


class OllamaModelManager:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        keep_alive: str = "5m",
        shutdown_server: bool = True,
        startup_timeout: float = 20.0,
    ) -> None:
        self.base_url = normalize_base_url(base_url)
        self.keep_alive = keep_alive
        self.shutdown_server = shutdown_server
        self.startup_timeout = startup_timeout
        self.session: OllamaSession | None = None
        self.current_model: str | None = None

    def generate(
        self,
        model: str,
        prompt: str,
        max_new_tokens: int = 900,
        temperature: float = 0.15,
    ) -> tuple[str, str]:
        if self.session and self.current_model != model:
            self.session.close()
            self.session = None
            self.current_model = None

        if not self.session:
            self.session = OllamaSession(
                model=model,
                base_url=self.base_url,
                keep_alive=self.keep_alive,
                shutdown_server=False,
                unload_model=True,
                startup_timeout=self.startup_timeout,
            ).start()
            self.current_model = self.session.model

        text = self.session.generate(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
        return text, self.session.model or model

    def close(self) -> None:
        if self.session:
            self.session.close()
            self.session = None
        self.current_model = None

    def __enter__(self) -> "OllamaModelManager":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


class OllamaSession:
    def __init__(
        self,
        model: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        keep_alive: str = "5m",
        shutdown_server: bool = True,
        unload_model: bool = True,
        startup_timeout: float = 20.0,
    ) -> None:
        self.base_url = base_url
        self.base_url = normalize_base_url(base_url)
        self.preferred_model = model
        self.keep_alive = keep_alive
        self.shutdown_server = shutdown_server
        self.unload_model_on_close = unload_model
        self.startup_timeout = startup_timeout
        self.ollama_exe = find_ollama_exe()
        self.process: subprocess.Popen | None = None
        self.started_server = False
        self.model: str | None = None

    def start(self) -> "OllamaSession":
        if not is_server_ready(self.base_url):
            if not self.ollama_exe:
                raise FileNotFoundError(
                    "Ollama server is not reachable and ollama.exe was not found. "
                    "Set OLLAMA_EXE or restart the shell after installing Ollama."
                )
            self.process = start_server(self.ollama_exe, self.base_url, self.startup_timeout)
            self.started_server = True

        available = list_models(self.base_url)
        if not available:
            available = list_models_from_disk()
        self.model = choose_model(self.preferred_model, available)
        return self

    def generate(self, prompt: str, max_new_tokens: int = 900, temperature: float = 0.15) -> str:
        if not self.model:
            self.start()

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": self.keep_alive,
            "options": {
                "temperature": temperature,
                "num_predict": max_new_tokens,
            },
        }
        data = _json_request(self.base_url, "/api/generate", payload=payload, timeout=600.0)
        return str(data.get("response", "")).strip()

    def unload_model(self) -> None:
        if not self.model:
            return

        payload = {
            "model": self.model,
            "prompt": "",
            "stream": False,
            "keep_alive": 0,
        }
        try:
            _json_request(self.base_url, "/api/generate", payload=payload, timeout=30.0)
        except Exception:
            pass

        if self.ollama_exe:
            try:
                subprocess.run(
                    [str(self.ollama_exe), "stop", self.model],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    timeout=30.0,
                    check=False,
                )
            except Exception:
                pass

    def close(self) -> None:
        if self.unload_model_on_close:
            self.unload_model()

        if self.started_server and self.shutdown_server and self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=8.0)
            except subprocess.TimeoutExpired:
                self.process.kill()

    def __enter__(self) -> "OllamaSession":
        return self.start()

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
