"""Reusable Ollama model manager backed by the canonical SDK session."""

from __future__ import annotations

from ia_carmine.providers.ollama.config import DEFAULT_BASE_URL, normalize_base_url
from ia_carmine.providers.ollama.session import OllamaSession


class OllamaModelManager:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        keep_alive: str = "120s",
        shutdown_server: bool = True,
        startup_timeout: float = 20.0,
        num_thread: int | None = None,
    ) -> None:
        self.base_url = normalize_base_url(base_url)
        self.keep_alive = keep_alive
        self.shutdown_server = shutdown_server
        self.startup_timeout = startup_timeout
        self.num_thread = num_thread if num_thread and num_thread > 0 else None
        self.session: OllamaSession | None = None
        self.current_model: str | None = None

    def generate(
        self,
        model: str,
        prompt: str,
        max_new_tokens: int = 900,
        temperature: float = 0.15,
        num_thread: int | None = None,
        response_format: str | None = None,
    ) -> tuple[str, str]:
        if self.session and self.current_model != model:
            self.session.close()
            self.session = None
            self.current_model = None
        effective_num_thread = num_thread if num_thread and num_thread > 0 else self.num_thread
        if not self.session:
            self.session = OllamaSession(
                model=model,
                base_url=self.base_url,
                keep_alive=self.keep_alive,
                shutdown_server=False,
                unload_model=True,
                startup_timeout=self.startup_timeout,
                num_thread=effective_num_thread,
            ).start()
            self.current_model = self.session.model
        text = self.session.generate(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            num_thread=effective_num_thread,
            response_format=response_format,
        )
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
