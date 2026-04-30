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


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    return [str(value)]


def normalize_provider_preflight_report(
    raw_report: dict[str, Any],
    *,
    provider: str,
    model: str | None = None,
    executable: str | None = None,
    model_dir: str | None = None,
) -> dict[str, Any]:
    """Normalize a provider preflight report without executing the provider."""

    report = raw_report if isinstance(raw_report, dict) else {}
    ready = bool(report.get("ready"))
    mode = str(report.get("mode") or ("provider_ready" if ready else "provider_unavailable"))
    errors = _string_list(report.get("errors"))
    warnings = _string_list(report.get("warnings"))
    devices = report.get("openvino_available_devices")
    if not isinstance(devices, list):
        devices = []

    return {
        "schema_version": 1,
        "kind": "provider_preflight",
        "provider": provider,
        "model": model,
        "executable": executable,
        "model_dir": model_dir,
        "ready": ready,
        "mode": mode,
        "provider_execution_allowed": ready,
        "provider_execution_performed": False,
        "errors": errors,
        "warnings": warnings,
        "runtime": {
            "python_starts": bool(report.get("python_starts")),
            "python_version": report.get("python_version"),
            "openvino_import": bool(report.get("openvino_import")),
            "openvino_genai_import": bool(report.get("openvino_genai_import")),
            "openvino_available_devices": devices,
            "npu_device_available": bool(report.get("npu_device_available")),
            "recommended_workers": int(report.get("recommended_workers") or 1),
        },
        "source": {
            "schema_version": report.get("schema_version"),
            "mode": report.get("mode"),
            "ready": bool(report.get("ready")),
            "python_exe": report.get("python_exe"),
            "model_dir": report.get("model_dir"),
            "python_exists": bool(report.get("python_exists")),
            "model_dir_exists": bool(report.get("model_dir_exists")),
        },
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
