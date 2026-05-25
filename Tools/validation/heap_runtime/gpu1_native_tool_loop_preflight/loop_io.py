from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import artifact_ref, read_text_windows_safe
from ia_carmine.runtime.heap_gate.gpu1_tool_result_messages import (
    gpu1_tool_result_payload,
    gpu1_tool_result_text,
)
from Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.readable import (
    assistant_after_tool,
)


def json_write(payload: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_operator_prompt(args: argparse.Namespace, repo_root: Path) -> str:
    prompt_file = str(getattr(args, "operator_prompt_file", "") or "").strip()
    if prompt_file:
        path = Path(prompt_file)
        if not path.is_absolute():
            path = repo_root / path
        return read_text_windows_safe(path)
    return str(getattr(args, "operator_prompt", "") or "")


def operator_prompt_ref(args: argparse.Namespace, repo_root: Path) -> dict[str, Any]:
    prompt_file = str(getattr(args, "operator_prompt_file", "") or "").strip()
    if not prompt_file:
        return {}
    path = Path(prompt_file)
    if not path.is_absolute():
        path = repo_root / path
    return artifact_ref(path, repo_root, kind="operator_prompt")


def assistant_history_message(report: dict[str, Any]) -> dict[str, Any]:
    message = report.get("assistant_message") if isinstance(report.get("assistant_message"), dict) else {}
    calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
    if message:
        out = {key: value for key, value in message.items() if key in {"role", "content", "tool_calls"}}
        if calls and not out.get("tool_calls"):
            out["tool_calls"] = calls
        if calls or out.get("tool_calls"):
            out["content"] = ""
        return out
    if calls:
        return {"role": "assistant", "content": "", "tool_calls": calls}
    return {"role": "assistant", "content": str(report.get("response_text") or "")}


def tool_result_message(repo_root: Path, result: dict[str, Any], tool_call_id: str) -> dict[str, Any]:
    payload = gpu1_tool_result_payload(repo_root, result, tool_call_id=tool_call_id)
    return {
        "role": "tool",
        "name": str(result.get("tool") or ""),
        "tool_call_id": tool_call_id,
        "tool_name": str(result.get("tool") or ""),
        "broker_request_id": str(result.get("request_id") or ""),
        "result_ref": str((result.get("outputs") or {}).get("json_report") or ""),
        "content": gpu1_tool_result_text(payload),
    }


def broker_args(
    repo_root: Path,
    request_file: Path,
    tool_output_dir: Path,
    broker_output: Path,
    stamp: str,
    timeout_seconds: int,
) -> argparse.Namespace:
    return argparse.Namespace(
        repo_root=str(repo_root),
        request_file=str(request_file),
        request_json="",
        payload_file="",
        job_id=stamp,
        tool_output_dir=str(tool_output_dir),
        stamp=stamp,
        timeout_seconds=timeout_seconds,
        dry_run=False,
        output=str(broker_output),
        markdown_output=str(broker_output.with_suffix(".md")),
    )


class ConsumptionOwner:
    def __init__(self, repo_root: Path, results: list[dict[str, Any]]) -> None:
        self.repo_root = repo_root
        self._results = results

    def broker_results(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            event.get("payload")
            for event in events
            if event.get("event_type") == "broker_result" and isinstance(event.get("payload"), dict)
        ] or self._results

    def provider_report_response_text(self, report: dict[str, Any]) -> str:
        return str(report.get("response_text") or "")


def has_history_shape(history: list[dict[str, Any]]) -> bool:
    assistant_tool = any(
        item.get("role") == "assistant" and isinstance(item.get("tool_calls"), list) and item.get("tool_calls")
        for item in history
    )
    tool_message = any(item.get("role") == "tool" for item in history)
    assistant_after_tool_seen = False
    seen_tool = False
    for item in history:
        if item.get("role") == "tool":
            seen_tool = True
        elif seen_tool and item.get("role") == "assistant":
            assistant_after_tool_seen = True
            break
    return bool(assistant_tool and tool_message and assistant_after_tool_seen)


def assistant_after_tool_message(history: list[dict[str, Any]]) -> dict[str, Any]:
    return assistant_after_tool(history)


def tool_calls(report: dict[str, Any]) -> list[dict[str, Any]]:
    calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
    return [item for item in calls if isinstance(item, dict) and str(item.get("tool") or "")]
