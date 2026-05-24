"""Canonical Ollama session backed by ollama-python."""

from __future__ import annotations

import subprocess
import time
from collections.abc import Callable

from ia_carmine.providers.ollama.config import (
    DEFAULT_BASE_URL,
    append_ollama_runtime_event,
    bounded_keep_alive,
    choose_model,
    default_ollama_num_ctx,
    find_ollama_exe,
    list_models_from_disk,
    normalize_base_url,
    start_server,
)
from ia_carmine.providers.ollama.sdk_client import OllamaSdkClient


class OllamaSession:
    def __init__(
        self,
        model: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        keep_alive: str = "120s",
        shutdown_server: bool = True,
        unload_model: bool = True,
        startup_timeout: float = 20.0,
        gpu_layers: str | int | None = None,
        num_thread: int | None = None,
        num_ctx: int | None = None,
        client_factory=None,
    ) -> None:
        self.base_url = normalize_base_url(base_url)
        self.sdk = OllamaSdkClient(self.base_url, client_factory=client_factory)
        self.preferred_model = model
        self.keep_alive = bounded_keep_alive(keep_alive)
        self.shutdown_server = shutdown_server
        self.unload_model_on_close = unload_model
        self.startup_timeout = startup_timeout
        self.num_thread = num_thread if num_thread and num_thread > 0 else None
        self.ollama_gpu_layers_requested = _gpu_layers_label(gpu_layers)
        self.ollama_options_num_gpu = _gpu_layers_option(gpu_layers)
        self.requested_num_ctx = num_ctx if num_ctx and num_ctx > 0 else None
        self.num_ctx = self.requested_num_ctx or default_ollama_num_ctx()
        self.effective_num_ctx = self.num_ctx
        self.effective_num_ctx_source = "explicit" if self.requested_num_ctx else "default"
        self.ollama_exe = find_ollama_exe()
        self.process: subprocess.Popen | None = None
        self.started_server = False
        self.model: str | None = None
        self.last_generate_result: dict = {}
        self.last_chat_result: dict = {}

    def start(self) -> "OllamaSession":
        start = time.perf_counter()
        if not self.sdk.is_ready():
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

        available = self.sdk.list_models() or list_models_from_disk()
        self.model = choose_model(self.preferred_model, available)
        append_ollama_runtime_event(
            "session_start",
            {
                "preferred_model": self.preferred_model,
                "selected_model": self.model,
                "available_model_count": len(available),
                "started_server": self.started_server,
                "backend": "ollama-python",
                "ollama_gpu_layers_requested": self.ollama_gpu_layers_requested,
                "ollama_options_num_gpu": self.ollama_options_num_gpu,
                "num_thread": self.num_thread,
                "num_ctx": self.num_ctx,
                "requested_num_ctx": self.requested_num_ctx,
                "effective_num_ctx": self.effective_num_ctx,
                "effective_num_ctx_source": self.effective_num_ctx_source,
                "inactivity_unload_seconds": 120,
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
        partial_callback: Callable[[str, dict], None] | None = None,
    ) -> str:
        if not self.model:
            self.start()
        effective_num_thread = num_thread if num_thread and num_thread > 0 else self.num_thread
        start = time.perf_counter()
        try:
            response = self.sdk.generate(
                model=str(self.model),
                prompt=prompt,
                keep_alive=self.keep_alive,
                temperature=temperature,
                num_predict=max_new_tokens,
                num_thread=effective_num_thread,
                num_ctx=self.num_ctx,
                num_gpu=self.ollama_options_num_gpu,
                think=False,
                response_format=response_format,
                partial_callback=partial_callback,
            )
            data = self.sdk.last_generate_response
        except Exception as exc:
            append_ollama_runtime_event(
                "generate_error",
                _runtime_event_payload(self, prompt, max_new_tokens, temperature, effective_num_thread, start, exc),
            )
            raise
        append_ollama_runtime_event(
            "generate_result",
            {
                **_runtime_event_payload(self, prompt, max_new_tokens, temperature, effective_num_thread, start),
                "response_chars": len(response),
                "empty_response": not bool(response),
                "done": data.get("done"),
                "done_reason": data.get("done_reason"),
                "prompt_eval_count": data.get("prompt_eval_count"),
                "eval_count": data.get("eval_count"),
            },
        )
        self.last_generate_result = _generation_stats(data, time.perf_counter() - start)
        return response

    def chat(
        self,
        messages: list[dict],
        *,
        tools: list[dict] | None = None,
        max_new_tokens: int = 900,
        temperature: float = 0.15,
        num_thread: int | None = None,
        partial_callback: Callable[[str, dict], None] | None = None,
    ) -> dict:
        if not self.model:
            self.start()
        effective_num_thread = num_thread if num_thread and num_thread > 0 else self.num_thread
        start = time.perf_counter()
        try:
            data = self.sdk.chat(
                model=str(self.model),
                messages=messages,
                tools=tools,
                keep_alive=self.keep_alive,
                temperature=temperature,
                num_predict=max_new_tokens,
                num_thread=effective_num_thread,
                num_ctx=self.num_ctx,
                num_gpu=self.ollama_options_num_gpu,
                think=False,
                partial_callback=partial_callback,
            )
        except Exception as exc:
            append_ollama_runtime_event(
                "chat_error",
                _chat_event_payload(self, messages, tools, effective_num_thread, start, exc),
            )
            raise
        message = data.get("message") if isinstance(data.get("message"), dict) else {}
        append_ollama_runtime_event(
            "chat_result",
            {
                **_chat_event_payload(self, messages, tools, effective_num_thread, start),
                "content_chars": len(str(message.get("content") or "")),
                "tool_call_count": len(message.get("tool_calls") or []),
                "done": data.get("done"),
                "done_reason": data.get("done_reason"),
            },
        )
        self.last_chat_result = _generation_stats(data, time.perf_counter() - start)
        return data

    def unload_model(self) -> None:
        if self.model:
            self.sdk.unload(self.model)

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
                "backend": "ollama-python",
                "ollama_gpu_layers_requested": self.ollama_gpu_layers_requested,
                "ollama_options_num_gpu": self.ollama_options_num_gpu,
                "num_thread": self.num_thread,
                "num_ctx": self.num_ctx,
                "requested_num_ctx": self.requested_num_ctx,
                "effective_num_ctx": self.effective_num_ctx,
                "effective_num_ctx_source": self.effective_num_ctx_source,
            },
        )

    def __enter__(self) -> "OllamaSession":
        return self.start()

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def _runtime_event_payload(
    session: OllamaSession,
    prompt: str,
    max_new_tokens: int,
    temperature: float,
    num_thread: int | None,
    start: float,
    exc: Exception | None = None,
) -> dict:
    payload = {
        "model": session.model,
        "prompt_chars": len(prompt),
        "max_new_tokens": max_new_tokens,
        "temperature": temperature,
        "backend": "ollama-python",
        "ollama_gpu_layers_requested": session.ollama_gpu_layers_requested,
        "ollama_options_num_gpu": session.ollama_options_num_gpu,
        "num_thread": num_thread,
        "num_ctx": session.num_ctx,
        "requested_num_ctx": session.requested_num_ctx,
        "effective_num_ctx": session.effective_num_ctx,
        "effective_num_ctx_source": session.effective_num_ctx_source,
        "elapsed_sec": round(time.perf_counter() - start, 4),
    }
    if exc:
        payload.update({"error_type": type(exc).__name__, "error": str(exc)})
    return payload


def _chat_event_payload(
    session: OllamaSession,
    messages: list[dict],
    tools: list[dict] | None,
    num_thread: int | None,
    start: float,
    exc: Exception | None = None,
) -> dict:
    payload = {
        "model": session.model,
        "message_count": len(messages),
        "tool_count": len(tools or []),
        "backend": "ollama-python",
        "ollama_gpu_layers_requested": session.ollama_gpu_layers_requested,
        "ollama_options_num_gpu": session.ollama_options_num_gpu,
        "num_thread": num_thread,
        "num_ctx": session.num_ctx,
        "requested_num_ctx": session.requested_num_ctx,
        "effective_num_ctx": session.effective_num_ctx,
        "effective_num_ctx_source": session.effective_num_ctx_source,
        "elapsed_sec": round(time.perf_counter() - start, 4),
    }
    if exc:
        payload.update({"error_type": type(exc).__name__, "error": str(exc)})
    return payload


def _gpu_layers_label(value: str | int | None) -> str:
    if value is None:
        return "default"
    text = str(value).strip().lower()
    if text in {"", "default", "auto"}:
        return "default"
    if text in {"all", "-1"}:
        return "all"
    return text


def _gpu_layers_option(value: str | int | None) -> int | None:
    label = _gpu_layers_label(value)
    if label == "default":
        return None
    if label == "all":
        return -1
    try:
        return int(label)
    except ValueError as exc:
        raise ValueError("--ollama-gpu-layers must be 'all', 'default', or an integer") from exc


def _generation_stats(data: dict, elapsed_seconds: float) -> dict:
    eval_count = _positive_int(data.get("eval_count"))
    eval_duration = _positive_int(data.get("eval_duration"))
    eval_duration_seconds = (eval_duration / 1_000_000_000) if eval_duration else 0.0
    tokens_per_second = (
        round(eval_count / eval_duration_seconds, 4)
        if eval_count > 0 and eval_duration_seconds > 0
        else 0.0
    )
    return {
        "done": data.get("done"),
        "done_reason": data.get("done_reason"),
        "total_duration": data.get("total_duration"),
        "load_duration": data.get("load_duration"),
        "prompt_eval_count": data.get("prompt_eval_count"),
        "prompt_eval_duration": data.get("prompt_eval_duration"),
        "eval_count": data.get("eval_count"),
        "eval_duration": data.get("eval_duration"),
        "eval_duration_seconds": round(eval_duration_seconds, 6),
        "tokens_per_second": tokens_per_second,
        "elapsed_sec": round(elapsed_seconds, 4),
    }


def _positive_int(value: object) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0
    return parsed if parsed > 0 else 0
