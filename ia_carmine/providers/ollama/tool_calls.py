"""Normalize ollama-python native tool calls for IA-Carmine broker execution."""

from __future__ import annotations

import json
from typing import Any


def normalize_ollama_tool_calls(chat_response: Any) -> list[dict[str, Any]]:
    data = _plain(chat_response)
    message = data.get("message") if isinstance(data, dict) else {}
    if not isinstance(message, dict):
        return []
    calls = message.get("tool_calls")
    if not isinstance(calls, list):
        return []
    normalized: list[dict[str, Any]] = []
    for index, call in enumerate(calls, start=1):
        item = _plain(call)
        function = item.get("function") if isinstance(item.get("function"), dict) else {}
        name = str(function.get("name") or "").strip()
        if not name:
            continue
        args = _arguments(function.get("arguments"))
        normalized.append(
            {
                "id": str(item.get("id") or f"ollama_tool_call_{index:03d}"),
                "tool": name,
                "requirement": str(item.get("requirement") or ""),
                "reason": str(item.get("reason") or "ollama_python_native_tool_call"),
                "args": args,
                "native_provider": "ollama",
                "native_shape": "ollama-python.message.tool_calls[].function",
            }
        )
    return normalized


def _arguments(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except Exception:
            return {"raw_arguments": value}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _plain(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_plain(item) for item in value]
    if hasattr(value, "model_dump"):
        return _plain(value.model_dump())
    if hasattr(value, "dict"):
        return _plain(value.dict())
    return value
