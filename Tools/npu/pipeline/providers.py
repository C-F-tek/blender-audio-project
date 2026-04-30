from __future__ import annotations

import json
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


@dataclass(frozen=True)
class ProviderParsedResult:
    """Parsed provider result summary without executing the provider."""

    provider: str
    ok: bool
    text: str
    parsed_json: Any | None = None
    json_ok: bool = False
    error: str | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "ok": self.ok,
            "text_chars": len(self.text),
            "json_ok": self.json_ok,
            "parsed_json_type": type(self.parsed_json).__name__ if self.parsed_json is not None else None,
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
        return [str(value) for value in value]
    return [str(value)]


def _first_text_value(raw: Any) -> str:
    if raw is None:
        return ""
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict):
        for key in ("text", "response", "content", "output"):
            value = raw.get(key)
            if isinstance(value, str):
                return value
        message = raw.get("message")
        if isinstance(message, dict) and isinstance(message.get("content"), str):
            return message["content"]
        choices = raw.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                message = first.get("message")
                if isinstance(message, dict) and isinstance(message.get("content"), str):
                    return message["content"]
                if isinstance(first.get("text"), str):
                    return first["text"]
    return str(raw)


def _extract_usage(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    usage = raw.get("usage")
    if isinstance(usage, dict):
        return dict(usage)
    out: dict[str, Any] = {}
    for key in ("prompt_eval_count", "eval_count", "total_duration", "load_duration", "prompt_tokens", "completion_tokens", "total_tokens"):
        if key in raw:
            out[key] = raw[key]
    return out


def _strip_markdown_json_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return stripped


def _parse_json_candidate(text: str) -> tuple[Any | None, bool, str | None]:
    candidate = _strip_markdown_json_fence(text)
    try:
        return json.loads(candidate), True, None
    except Exception as exc:  # noqa: BLE001 - parse report only.
        return None, False, f"json_parse_failed: {type(exc).__name__}: {exc}"


def parse_provider_result(
    raw_result: Any,
    *,
    provider: str,
    model: str | None = None,
    executed: bool = False,
    allow_json: bool = True,
) -> ProviderParsedResult:
    """Parse an already-obtained or simulated provider result.

    This helper does not execute providers. It only normalizes an existing
    payload into text/JSON/metadata fields. Markdown JSON fences are tolerated
    because some local models return fenced JSON even when asked not to.
    """

    text = _first_text_value(raw_result)
    errors: list[str] = []
    parsed_json: Any | None = None
    json_ok = False
    if allow_json and text.strip():
        parsed_json, json_ok, parse_error = _parse_json_candidate(text)
        if parse_error:
            errors.append(parse_error)
    raw_error = raw_result.get("error") if isinstance(raw_result, dict) else None
    if raw_error:
        errors.append(str(raw_error))
    metadata = {
        "model": model,
        "executed": executed,
        "usage": _extract_usage(raw_result),
        "raw_type": type(raw_result).__name__,
    }
    return ProviderParsedResult(
        provider=provider,
        ok=not raw_error and bool(text.strip()),
        text=text,
        parsed_json=parsed_json,
        json_ok=json_ok,
        error="; ".join(errors) if errors else None,
        metadata=metadata,
    )


def build_provider_result_report(
    *,
    provider: str,
    model: str | None,
    results: list[ProviderParsedResult],
    provider_execution_performed: bool = False,
) -> dict[str, Any]:
    """Build a deterministic report for parsed provider results."""

    errors = [result.error for result in results if result.error]
    return {
        "schema_version": 1,
        "kind": "provider_result_report",
        "provider": provider,
        "model": model,
        "provider_execution_performed": provider_execution_performed,
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "result_count": len(results),
        "json_ok_count": sum(1 for result in results if result.json_ok),
        "results": [result.to_dict() for result in results],
    }


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
