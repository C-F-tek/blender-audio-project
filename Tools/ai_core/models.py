from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(slots=True)
class ModelResponse:
    text: str
    model: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelClient(Protocol):
    """Small common interface for Ollama, OpenVINO, OpenAI-compatible APIs, etc."""

    def generate(self, prompt: str, **kwargs: Any) -> ModelResponse:
        ...


@dataclass(slots=True)
class StaticModelClient:
    """Deterministic test client for parser, validator and pipeline tests."""

    response_text: str
    model: str = "static"

    def generate(self, prompt: str, **kwargs: Any) -> ModelResponse:
        return ModelResponse(text=self.response_text, model=self.model, metadata={"prompt_chars": len(prompt), **kwargs})
