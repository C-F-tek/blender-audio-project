"""Ollama client helpers for the tool gateway."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from .common import GatewayConfig

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
    payload = {
        "model": config.model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.2},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        config.ollama_url.rstrip("/") + "/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=240) as response:  # noqa: S310 - local/operator configured endpoint.
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc
    parsed = json.loads(raw)
    return str((parsed.get("message") or {}).get("content") or parsed.get("response") or "")

def system_prompt() -> str:
    return """You are IA-Carmine local tool gateway planner.
Use tools when project memory or files are needed. Answer ONLY valid JSON.

Allowed tool request:
{"type":"tool_request","tool":"file_search","arguments":{"query":"...","roots":["Tools/ai","docs"]}}
{"type":"tool_request","tool":"file_read","arguments":{"path":"Tools/ai/example.py"}}
{"type":"tool_request","tool":"memory_search","arguments":{"query":"...","scope":"operational","limit":10}}
{"type":"tool_request","tool":"memory_remember_operational","arguments":{"summary":"...","content":"...","tags":["..."]}}
{"type":"tool_request","tool":"build_context_pack","arguments":{"profile":"core_ai_backend"}}

Final answer:
{"type":"final","answer":"..."}

Never invent file content. Ask file_search/file_read when needed. Do not request writes, git, shell, delete, patch apply, Blender or secrets."""
