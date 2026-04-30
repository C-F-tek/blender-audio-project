from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderRequest:
    """Provider-agnostic request descriptor for future NPU/Ollama adapters."""

    provider: str
    model: str
    prompt: str
    max_tokens: int
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "prompt_chars": len(self.prompt),
            "max_tokens": self.max_tokens,
            "metadata": self.metadata or {},
        }


@dataclass(frozen=True)
class ProviderResult:
    """Provider-agnostic result envelope for future runtime adapters."""

    provider: str
    ok: bool
    text: str
    error: str | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "ok": self.ok,
            "text_chars": len(self.text),
            "error": self.error,
            "metadata": self.metadata or {},
        }


def validate_provider_request(request: ProviderRequest) -> dict[str, object]:
    """Validate a provider request without executing it."""

    issues: list[str] = []
    if not request.provider.strip():
        issues.append("provider is required")
    if not request.model.strip():
        issues.append("model is required")
    if not request.prompt.strip():
        issues.append("prompt is required")
    if request.max_tokens <= 0:
        issues.append("max_tokens must be positive")
    return {
        "ok": not issues,
        "provider": request.provider,
        "model": request.model,
        "issues": issues,
    }


def planned_provider_result(request: ProviderRequest, *, reason: str = "planned-only") -> ProviderResult:
    """Return a deterministic non-executed provider result envelope."""

    validation = validate_provider_request(request)
    if not validation["ok"]:
        return ProviderResult(
            provider=request.provider,
            ok=False,
            text="",
            error="; ".join(str(issue) for issue in validation["issues"]),
            metadata={"mode": reason, "executed": False},
        )
    return ProviderResult(
        provider=request.provider,
        ok=True,
        text="",
        error=None,
        metadata={"mode": reason, "executed": False, "model": request.model},
    )
