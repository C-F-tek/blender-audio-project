"""Ollama session object."""

from __future__ import annotations

import subprocess
import time

from .config import (
    DEFAULT_BASE_URL,
    append_ollama_runtime_event,
    default_ollama_num_ctx,
    default_ollama_num_thread,
    find_ollama_exe,
    normalize_base_url,
)
from .http_client import choose_model, is_server_ready, json_request, list_models, list_models_from_disk, start_server


class OllamaSession:
    def __init__(
        self,
        model: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        keep_alive: str = "5m",
        shutdown_server: bool = True,
        unload_model: bool = True,
        startup_timeout: float = 20.0,
        num_thread: int | None = None,
        num_ctx: int | None = None,
    ) -> None:
        self.base_url = normalize_base_url(base_url)
        self.preferred_model = model
        self.keep_alive = keep_alive
        self.shutdown_server = shutdown_server
        self.unload_model_on_close = unload_model
        self.startup_timeout = startup_timeout
        self.num_thread = (
            num_thread if num_thread and num_thread > 0 else default_ollama_num_thread()
        )
        self.num_ctx = num_ctx if num_ctx and num_ctx >= 4096 else default_ollama_num_ctx()
        self.ollama_exe = find_ollama_exe()
        self.process: subprocess.Popen | None = None
        self.started_server = False
        self.model: str | None = None

    def start(self) -> "OllamaSession":
        start = time.perf_counter()
        if not is_server_ready(self.base_url):
            if not self.ollama_exe:
                append_ollama_runtime_event(
                    "server_not_ready",
                    {"base_url": self.base_url, "preferred_model": self.preferred_model},
                )
                raise FileNotFoundError(
                    "Ollama server is not reachable and ollama.exe was not found. "
                    "Set OLLAMA_EXE or restart the shell after installing Ollama."
                )
            self.process = start_server(self.ollama_exe, self.base_url, self.startup_timeout)
            self.started_server = True

        available = list_models(self.base_url) or list_models_from_disk()
        self.model = choose_model(self.preferred_model, available)
        append_ollama_runtime_event(
            "session_start",
            {
                "preferred_model": self.preferred_model,
                "selected_model": self.model,
                "available_model_count": len(available),
                "started_server": self.started_server,
                "num_thread": self.num_thread,
                "num_ctx": self.num_ctx,
                "elapsed_sec": round(time.perf_counter() - start, 4),
            },
        )
        return self

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 900,
        temperature: float = 0.15,
        num_thread: int | None = None,
        response_format: str | None = None,
    ) -> str:
        if not self.model:
            self.start()
        effective_num_thread = num_thread if num_thread and num_thread > 0 else self.num_thread
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": self.keep_alive,
            "options": {
                "temperature": temperature,
                "num_predict": max_new_tokens,
                "num_thread": effective_num_thread,
                "num_ctx": self.num_ctx,
            },
        }
        if response_format:
            payload["format"] = response_format
        start = time.perf_counter()
        try:
            data = json_request(self.base_url, "/api/generate", payload=payload, timeout=600.0)
        except Exception as exc:
            append_ollama_runtime_event(
                "generate_error",
                {
                    "model": self.model,
                    "prompt_chars": len(prompt),
                    "max_new_tokens": max_new_tokens,
                    "temperature": temperature,
                    "num_thread": effective_num_thread,
                    "response_format": response_format,
                    "elapsed_sec": round(time.perf_counter() - start, 4),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
            raise
        response = str(data.get("response", "")).strip()
        append_ollama_runtime_event(
            "generate_result",
            {
                "model": self.model,
                "prompt_chars": len(prompt),
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "num_thread": effective_num_thread,
                "response_format": response_format,
                "elapsed_sec": round(time.perf_counter() - start, 4),
                "response_chars": len(response),
                "empty_response": not bool(response),
                "done": data.get("done"),
                "done_reason": data.get("done_reason"),
                "prompt_eval_count": data.get("prompt_eval_count"),
                "eval_count": data.get("eval_count"),
                "response_preview": response[:300],
            },
        )
        return response

    def chat(
        self,
        messages: list[dict],
        *,
        tools: list[dict] | None = None,
        max_new_tokens: int = 900,
        temperature: float = 0.15,
        num_thread: int | None = None,
    ) -> dict:
        if not self.model:
            self.start()
        effective_num_thread = num_thread if num_thread and num_thread > 0 else self.num_thread
        payload: dict = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "keep_alive": self.keep_alive,
            "options": {
                "temperature": temperature,
                "num_predict": max_new_tokens,
                "num_thread": effective_num_thread,
                "num_ctx": self.num_ctx,
            },
        }
        if tools:
            payload["tools"] = tools
        start = time.perf_counter()
        try:
            data = json_request(self.base_url, "/api/chat", payload=payload, timeout=600.0)
        except Exception as exc:
            append_ollama_runtime_event(
                "chat_error",
                {
                    "model": self.model,
                    "message_count": len(messages),
                    "tool_count": len(tools or []),
                    "elapsed_sec": round(time.perf_counter() - start, 4),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
            raise
        message = data.get("message") if isinstance(data.get("message"), dict) else {}
        append_ollama_runtime_event(
            "chat_result",
            {
                "model": self.model,
                "message_count": len(messages),
                "tool_count": len(tools or []),
                "elapsed_sec": round(time.perf_counter() - start, 4),
                "content_chars": len(str(message.get("content") or "")),
                "tool_call_count": len(message.get("tool_calls") or []),
                "done": data.get("done"),
                "done_reason": data.get("done_reason"),
            },
        )
        return data

    def unload_model(self) -> None:
        if not self.model:
            return
        payload = {"model": self.model, "prompt": "", "stream": False, "keep_alive": 0}
        try:
            json_request(self.base_url, "/api/generate", payload=payload, timeout=30.0)
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
        append_ollama_runtime_event(
            "session_close",
            {
                "model": self.model,
                "started_server": self.started_server,
                "unload_model": self.unload_model_on_close,
                "num_thread": self.num_thread,
            },
        )

    def __enter__(self) -> "OllamaSession":
        return self.start()

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
