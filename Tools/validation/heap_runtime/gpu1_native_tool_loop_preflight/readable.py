"""Readable GPU1 native tool-loop transcript rendering."""

from __future__ import annotations

import json
from typing import Any


def _parse_tool_result_text(content: str) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    lines = content.splitlines()
    in_window = False
    window: list[str] = []
    for line in lines:
        if line == "RUNTIME_FILE_WINDOW_TEXT_BEGIN":
            in_window = True
            continue
        if line == "RUNTIME_FILE_WINDOW_TEXT_END":
            in_window = False
            continue
        if in_window:
            window.append(line)
            continue
        key, separator, value = line.partition(":")
        if separator and key in {"request_id", "tool", "returncode", "passed", "executed"}:
            payload[key] = value.strip()
        if separator and key == "runtime_file_window_text_chars":
            payload[key] = value.strip()
    if window:
        payload["runtime_file_window_text"] = "\n".join(window)
    return payload


def assistant_after_tool(history: list[dict[str, Any]]) -> dict[str, Any]:
    seen_tool = False
    latest: dict[str, Any] = {}
    for item in history:
        if item.get("role") == "tool":
            seen_tool = True
            continue
        if seen_tool and item.get("role") == "assistant":
            latest = item
    return latest


def render_delta_readable(
    *,
    request_id: str,
    history: list[dict[str, Any]],
    protocol: dict[str, Any],
    operator_delta: dict[str, Any],
    consumption: dict[str, Any],
    delta_review: dict[str, Any],
) -> str:
    user_prompt = next(
        (str(item.get("content") or "") for item in history if item.get("role") == "user"),
        "",
    )
    assistant_tool = next(
        (
            item
            for item in reversed(history)
            if item.get("role") == "assistant"
            and isinstance(item.get("tool_calls"), list)
            and item.get("tool_calls")
        ),
        {},
    )
    tool_message = next((item for item in reversed(history) if item.get("role") == "tool"), {})
    tool_payload: dict[str, Any] = {}
    tool_content = str(tool_message.get("content") or "")
    try:
        tool_payload = json.loads(tool_content or "{}")
    except json.JSONDecodeError:
        tool_payload = _parse_tool_result_text(tool_content)
    tool_calls = (
        assistant_tool.get("tool_calls")
        if isinstance(assistant_tool.get("tool_calls"), list)
        else []
    )
    final_assistant = assistant_after_tool(history)
    delta = str(protocol.get("delta") or "")
    lines = [
        "# GPU1 Native Tool Loop Delta",
        "",
        "Transcript leggibile: prompt GPU1, tool call, tool response, resume e delta.",
        "",
        "## Stato",
        "",
        f"- Request id: `{request_id}`",
        f"- Tool result consumed by GPU1: `{consumption.get('tool_result_consumed_by_gpu1')}`",
        f"- GPU1 tool loop closed: `{not consumption.get('gpu1_waiting_for_tool_result')}`",
        f"- Final product kind/action: `{protocol.get('kind')}` / `{protocol.get('action')}`",
        f"- Final product protocol valid: `{protocol.get('passed')}`",
        f"- Operator delta valid: `{operator_delta.get('passed')}`",
        f"- Operator delta errors: `{operator_delta.get('errors') or []}`",
        f"- Deterministic delta review passed: `{delta_review.get('passed')}`",
        "",
        "## Prompt GPU1",
        "",
        "```text",
        user_prompt.strip(),
        "```",
        "",
        "## Subturn 0 - Tool Call Nativa GPU1",
        "",
        "```json",
        json.dumps(tool_calls, indent=2, ensure_ascii=False),
        "```",
        "",
        "## Broker Tool Response Reiniettata",
        "",
        f"- Tool: `{tool_payload.get('tool')}`",
        f"- Return code: `{tool_payload.get('returncode')}`",
        f"- Executed: `{tool_payload.get('executed')}`",
        f"- Request id: `{tool_payload.get('request_id')}`",
        f"- Text chars: `{tool_payload.get('runtime_file_window_text_chars')}`",
        "",
        "```text",
        str(tool_payload.get("runtime_file_window_text") or "").strip(),
        "```",
        "",
        "## RISPOSTA GPU1 DOPO AVER CONSUMATO IL TOOL_RESULT",
        "",
        "```text",
        str(final_assistant.get("content") or "").strip(),
        "```",
        "",
        "## RISPOSTA OPERATORE / FINAL_PRODUCT_DELTA ESTRATTO",
        "",
        delta.strip(),
        "",
        "## Deterministic Review Sul Delta",
        "",
        "- Tool: `deterministic_semantic_validator`",
        f"- Passed: `{delta_review.get('passed')}`",
        f"- Delta input ref: `{(delta_review.get('delta_ref') or {}).get('path')}`",
        f"- Review report ref: `{(delta_review.get('review_report_ref') or {}).get('path')}`",
        "",
    ]
    return "\n".join(lines)
