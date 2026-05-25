"""Normalize ollama-python native tool calls for IA-Carmine broker execution."""

from __future__ import annotations

import json
import re
from typing import Any

_QWEN_TOOL_CALL_BLOCK_RE = re.compile(r"<tool_call>\s*(.*?)\s*</tool_call>", re.DOTALL)


def normalize_ollama_tool_calls(
    chat_response: Any,
    *,
    allow_content_json_adapter: bool = False,
    allow_template_adapter: bool = True,
) -> list[dict[str, Any]]:
    data = _plain(chat_response)
    message = data.get("message") if isinstance(data, dict) else {}
    if not isinstance(message, dict):
        return []
    calls = message.get("tool_calls")
    if not isinstance(calls, list) or not calls:
        content = str(message.get("content") or "")
        if allow_template_adapter:
            template_calls = _normalize_qwen_template_tool_calls(content)
            if template_calls:
                return template_calls
        if allow_content_json_adapter:
            return _normalize_qwen_content_json_tool_call(content)
        return []
    normalized: list[dict[str, Any]] = []
    for index, call in enumerate(calls, start=1):
        item = _plain(call)
        name, args = _tool_name_args(item)
        if not name:
            continue
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


def _normalize_qwen_template_tool_calls(content: str) -> list[dict[str, Any]]:
    """Accept only the model-template native <tool_call> envelope, not naked JSON/prose."""
    stripped = (content or "").strip()
    if not stripped.startswith("<tool_call>"):
        return []
    matches = list(_QWEN_TOOL_CALL_BLOCK_RE.finditer(stripped))
    if not matches:
        return []
    residue = _QWEN_TOOL_CALL_BLOCK_RE.sub("", stripped).strip()
    if residue:
        return []
    normalized: list[dict[str, Any]] = []
    for block_index, match in enumerate(matches, start=1):
        for item_index, item in enumerate(_json_objects(match.group(1)), start=1):
            name, args = _tool_name_args(item)
            if not name:
                continue
            index = len(normalized) + 1
            normalized.append(
                {
                    "id": f"qwen_template_tool_call_{index:03d}",
                    "tool": name,
                    "requirement": "",
                    "reason": "ollama_qwen_template_native_tool_call",
                    "args": args,
                    "native_provider": "ollama",
                    "native_shape": "ollama-qwen-template.content.<tool_call>",
                    "adapter_native": True,
                    "template_block_index": block_index,
                    "template_item_index": item_index,
                }
            )
    return normalized


def _normalize_qwen_content_json_tool_call(content: str) -> list[dict[str, Any]]:
    """Adapter fallback for qwen2.5-coder on Ollama when chat(tools=...) emits raw JSON."""
    stripped, fenced = _single_json_payload(_strip_qwen_template_tokens(content))
    if not (stripped.startswith("{") and stripped.endswith("}")):
        return []
    try:
        item = json.loads(stripped)
    except json.JSONDecodeError:
        return []
    if not isinstance(item, dict):
        return []
    name, args = _tool_name_args(item)
    if not name:
        return []
    return [
        {
            "id": "qwen_content_json_tool_call_001",
            "tool": name,
            "requirement": "",
            "reason": (
                "ollama_qwen_content_json_fence_tool_call_adapter"
                if fenced
                else "ollama_qwen_content_json_tool_call_adapter"
            ),
            "args": args,
            "native_provider": "ollama",
            "native_shape": (
                "ollama-qwen2.5-coder.chat_tools.content_json_fence_adapter"
                if fenced
                else "ollama-qwen2.5-coder.chat_tools.content_json_adapter"
            ),
            "adapter_native": True,
            "adapter_strict_json": True,
            "adapter_single_fenced_json": fenced,
        }
    ]


def _single_json_payload(content: str) -> tuple[str, bool]:
    stripped = (content or "").strip()
    if not stripped.startswith("```"):
        return stripped, False
    lines = stripped.splitlines()
    if len(lines) < 3 or not lines[0].strip().startswith("```") or lines[-1].strip() != "```":
        return stripped, False
    body = "\n".join(lines[1:-1]).strip()
    return body, True


def _strip_qwen_template_tokens(content: str) -> str:
    stripped = (content or "").strip()
    for token in ("<|im_start|>", "<|im_end|>", "<|endoftext|>"):
        stripped = stripped.replace(token, "")
    return stripped.strip()


def _json_objects(text: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    index = 0
    values: list[dict[str, Any]] = []
    source = (text or "").strip()
    while index < len(source):
        while index < len(source) and source[index].isspace():
            index += 1
        if index >= len(source):
            break
        try:
            value, end = decoder.raw_decode(source, index)
        except json.JSONDecodeError:
            return []
        if not isinstance(value, dict):
            return []
        values.append(value)
        index = end
    return values


def _tool_name_args(item: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    function = item.get("function") if isinstance(item.get("function"), dict) else {}
    name = str(function.get("name") or item.get("name") or "").strip()
    args = item.get("arguments") if "arguments" in item else function.get("arguments")
    return name, _arguments(args)


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
