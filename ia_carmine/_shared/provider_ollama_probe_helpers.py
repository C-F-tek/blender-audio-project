from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from ia_carmine._shared.provider_replight import provider_replight_fields


def positive_provider_value(name: str, value: int) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise ValueError(f"{name} must be a positive operator/heap propagated value")
    return parsed


def selection_blocked_report(
    *,
    lane: str,
    role: str,
    model: str | None,
    selected_model: str,
    reason: str,
    selection: dict[str, Any],
    elapsed_sec: float,
    base_url: str,
    server_process: dict[str, Any],
) -> dict[str, Any]:
    replight = provider_replight_fields(
        lane=lane,
        role=role,
        report={
            "provider_model": selected_model or str(model or "auto"),
            "provider_execution_performed": False,
            "provider_device_verified": False,
            "response_text": "",
        },
        default_model=selected_model or str(model or "auto"),
    )
    replight["replight_blocked_reason"] = f"provider_replight_failed:{lane}:{reason}"
    replight["replight_passed"] = False
    return {
        "lane": lane,
        "passed": False,
        "provider_execution_performed": False,
        "provider_backend": "ollama",
        "provider_compute_device": (
            "ollama/gpu0-vulkan_unavailable" if lane == "gpu0_peer" else "ollama/unavailable"
        ),
        "ollama_base_url": base_url,
        **server_process,
        "provider_device_verified": False,
        "cpu_provider_fallback_performed": False,
        "error": reason,
        "errors": [reason],
        "product_blocked_reason": reason,
        "role": role,
        **selection,
        **replight,
        "elapsed_sec": round(elapsed_sec, 4),
    }


class PartialWriter:
    def __init__(
        self,
        *,
        path: Path | None,
        markdown_path: Path | None,
        lane: str,
        selected_model: str,
        num_ctx: int | None,
        gpu_layers: str | int | None,
        num_thread: int | None,
        prompt: str | None,
        started: float,
    ) -> None:
        self.path = path
        self.markdown_path = markdown_path
        self.lane = lane
        self.selected_model = selected_model
        self.num_ctx = num_ctx
        self.gpu_layers = gpu_layers
        self.num_thread = num_thread
        self.prompt = prompt
        self.started = started
        self.last_write = 0.0

    def __call__(self, text: str, chunk: dict[str, Any]) -> None:
        if self.path is None:
            return
        now = time.perf_counter()
        if not chunk.get("done") and now - self.last_write < 1.0:
            return
        self.last_write = now
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._payload(text, chunk), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if self.markdown_path is not None:
            self.markdown_path.write_text(self._markdown(text, chunk), encoding="utf-8")

    def _payload(self, text: str, chunk: dict[str, Any]) -> dict[str, Any]:
        return {
            "kind": "ollama_provider_partial",
            "lane": self.lane,
            "status": "partial",
            "selected_model": self.selected_model,
            "num_ctx": self.num_ctx,
            "ollama_gpu_layers_requested": str(self.gpu_layers or "default"),
            "num_thread": self.num_thread,
            "prompt_chars": len(self.prompt or ""),
            "partial_response_chars": len(text),
            "last_chunk_chars": len(str(chunk.get("response") or "")),
            "done": bool(chunk.get("done")),
            "done_reason": chunk.get("done_reason"),
            "elapsed_sec": round(time.perf_counter() - self.started, 4),
            "provider_execution_performed": False,
            "provider_backend": "ollama",
            "provider_compute_device": (
                "ollama/gpu0-vulkan_pending"
                if self.lane == "gpu0_peer"
                else "ollama/pending_gpu_residency"
            ),
            "provider_device_verified": False,
            "cpu_provider_fallback_performed": False,
        }

    def _markdown(self, text: str, chunk: dict[str, Any]) -> str:
        return "\n".join(
            [
                "# Ollama Provider Partial",
                "",
                f"- Lane: `{self.lane}`",
                f"- Model: `{self.selected_model}`",
                f"- Done: `{bool(chunk.get('done'))}`",
                f"- Partial chars: `{len(text)}`",
                "",
                "## Partial Response",
                "",
                text,
                "",
            ]
        )


def parsed_contract_fields(
    *,
    parsed_json: dict[str, Any],
    text: str,
    native_tool_calls: list[dict[str, Any]],
    extract_target_refs,
    extract_validation_refs,
    extract_rejected_validation_refs=None,
) -> dict[str, Any]:
    response_text = str(
        parsed_json.get("response_text")
        or parsed_json.get("markdown")
        or parsed_json.get("proposal")
        or text
        or ""
    ).strip()
    textual_tool_calls = parsed_json.get("tool_calls") or parsed_json.get("TOOL_CALLS") or []
    if not isinstance(textual_tool_calls, list):
        textual_tool_calls = []
    if not textual_tool_calls and parsed_json.get("name"):
        textual_tool_calls = [{
            "tool": str(parsed_json.get("name")),
            "args": parsed_json.get("arguments")
            if isinstance(parsed_json.get("arguments"), dict)
            else {},
            "native_provider": "ollama",
            "native_shape": "content_json_tool_call_not_native",
        }]
    target_files = _list_or_empty(
        parsed_json.get("target_files") or parsed_json.get("TARGET_FILES")
    )
    validation_commands = _list_or_empty(
        parsed_json.get("validation_commands") or parsed_json.get("VALIDATION_COMMANDS")
    )
    parsed_validation_commands, rejected_json_validation_refs = _split_validation_commands(
        validation_commands
    )
    text_validation_commands = extract_validation_refs(response_text)
    rejected_validation_refs = list(rejected_json_validation_refs)
    if extract_rejected_validation_refs is not None:
        rejected_validation_refs.extend(extract_rejected_validation_refs(response_text))
    return {
        "response_text": response_text,
        "textual_tool_calls": textual_tool_calls,
        "target_files": target_files or extract_target_refs(response_text),
        "validation_commands": parsed_validation_commands or text_validation_commands,
        "rejected_validation_refs": _unique_ordered(rejected_validation_refs),
        "empty_output": not response_text.strip() and not native_tool_calls,
    }


def _list_or_empty(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


_VALIDATION_COMMAND_RE = re.compile(
    r"^(?:&\s*)?(?:"
    r"(?:\$[A-Za-z_][A-Za-z0-9_]*|python|py|pytest|pwsh|powershell|bash|sh|cmd|uv|ruff|mypy|npm|npx)"
    r")\b",
    re.IGNORECASE,
)
_BARE_FILE_REF_RE = re.compile(
    r"^(?:\.\/)?(?:ia_carmine|Tools|tools|docs|CHATGPT|Scripting|scripts|patch_specs|config|examples|assets|\.github|output|indexAI|renders)/"
    r"[A-Za-z0-9_./() -]+\.(?:py|ps1|md|json|txt|yml|yaml|toml|diff|patch|csv|tsv|svg|png|jpg|jpeg|webp|wav|mp3|mp4)$"
)


def _split_validation_commands(values: list[Any]) -> tuple[list[str], list[str]]:
    commands: list[str] = []
    rejected: list[str] = []
    for value in values:
        text = str(value or "").strip().strip("`'\" ")
        if not text:
            continue
        if _VALIDATION_COMMAND_RE.match(text):
            commands.append(text)
        elif _BARE_FILE_REF_RE.match(text):
            rejected.append(text)
    return _unique_ordered(commands), _unique_ordered(rejected)


def _unique_ordered(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out
