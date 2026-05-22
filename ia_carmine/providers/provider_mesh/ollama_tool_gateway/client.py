"""Ollama client helpers for the tool gateway."""

from __future__ import annotations

import json
from typing import Any

from .common import GatewayConfig
from ia_carmine.providers.ollama.sdk_client import OllamaSdkClient

def extract_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`").strip()
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    try:
        data = json.loads(stripped)
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        pass
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        try:
            data = json.loads(stripped[start : end + 1])
            return data if isinstance(data, dict) else None
        except json.JSONDecodeError:
            return None
    return None

def ollama_chat(config: GatewayConfig, messages: list[dict[str, str]]) -> str:
    client = OllamaSdkClient(config.ollama_url)
    parsed = client.chat(
        model=config.model,
        messages=[dict(item) for item in messages],
        keep_alive="5m",
        temperature=0.2,
        num_predict=900,
        num_thread=None,
        num_ctx=None,
    )
    return str((parsed.get("message") or {}).get("content") or parsed.get("response") or "")

def system_prompt() -> str:
    return """You are IA-Carmine local tool gateway planner.
Use tools when project memory or files are needed. Answer ONLY valid JSON.

Allowed tool request:
{"type":"tool_request","tool":"file_search","arguments":{"query":"...","roots":["ia_carmine","docs"]}}
{"type":"tool_request","tool":"file_read","arguments":{"path":"ia_carmine/example.py"}}
{"type":"tool_request","tool":"memory_search","arguments":{"query":"...","scope":"operational","limit":10}}
{"type":"tool_request","tool":"memory_remember_operational","arguments":{"summary":"...","content":"...","tags":["..."]}}
{"type":"tool_request","tool":"build_context_pack","arguments":{"profile":"core_ai_backend"}}

Final answer:
{"type":"final","answer":"..."}

Never invent file content. Ask file_search/file_read when needed. Do not request writes, git, shell, delete, patch apply, Blender or secrets."""
