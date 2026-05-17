"""NPU tool-request extraction and deterministic fallback."""

from __future__ import annotations

import json
import re
from typing import Any

from tools.ai.runtime_tool_guidance import (
    ALLOWED_RUNTIME_TOOLS,
    deterministic_fallback_tool_requests,
    validate_runtime_tool_request_object,
)

ALLOWED_RUNTIME_TOOL_NAMES = ALLOWED_RUNTIME_TOOLS
JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)

def _tool_request_error(index: int, message: str) -> str:
    return f"tool_requests[{index}]: {message}"

def _candidate_json_payloads(text: str) -> list[Any]:
    candidates: list[str] = []
    stripped = text.strip()
    if stripped:
        candidates.append(stripped)
    for match in JSON_FENCE_RE.finditer(text):
        payload = match.group(1).strip()
        if payload:
            candidates.append(payload)
    parsed: list[Any] = []
    for candidate in candidates:
        try:
            parsed.append(json.loads(candidate))
        except Exception:
            continue
    return parsed

def _raw_tool_requests_from_payload(payload: Any) -> list[Any]:
    if isinstance(payload, dict) and isinstance(payload.get("tool_requests"), list):
        return list(payload["tool_requests"])
    if isinstance(payload, list):
        return payload
    return []

def extract_npu_tool_requests_from_text(
    text: str, max_requests: int = 8
) -> tuple[list[dict[str, Any]], list[str]]:
    valid: list[dict[str, Any]] = []
    errors: list[str] = []
    raw_requests: list[Any] = []
    for payload in _candidate_json_payloads(text):
        raw_requests.extend(_raw_tool_requests_from_payload(payload))
    for index, item in enumerate(raw_requests[: max(0, max_requests)], start=1):
        if not isinstance(item, dict):
            errors.append(_tool_request_error(index, "request must be an object"))
            continue
        shared_errors = validate_runtime_tool_request_object(item, index)
        if shared_errors:
            errors.extend(shared_errors)
            continue
        tool = str(item.get("tool") or "").strip()
        args = item.get("args", {})
        valid.append(
            {
                "id": str(item.get("id") or f"npu_tool_{index:03d}"),
                "tool": tool,
                "reason": str(
                    item.get("reason")
                    or "NPU auditor requested additional report-only tool evidence."
                ),
                "args": args,
                "source": "npu_auditor",
            }
        )
    if len(raw_requests) > max_requests:
        errors.append(f"tool_requests truncated: {len(raw_requests)} requested, max {max_requests}")
    return valid, errors

def should_use_npu_deterministic_tool_fallback(
    *,
    run_npu: bool,
    metadata_only: bool,
    runtime_tool_context_reports: list[dict[str, Any]],
    tool_requests: list[dict[str, Any]],
    classification: str,
    disabled: bool,
) -> bool:
    """Return whether the NPU audit lane should emit broker-compatible fallback tools."""

    if disabled:
        return False
    if metadata_only:
        return False
    if not run_npu:
        return False
    if tool_requests:
        return False
    if not runtime_tool_context_reports:
        return False
    return classification in {
        "usable_audit_text",
        "provider_empty_response",
        "unusable_output",
        "dependency_missing_openvino_genai",
        "npu_python_missing",
    }

def build_npu_deterministic_tool_fallback_requests(
    *,
    classification: str,
    runtime_tool_context_reports: list[dict[str, Any]],
    max_requests: int,
) -> list[dict[str, Any]]:
    """Build safe NPU fallback tool requests for broker execution by the orchestrator."""

    reason = (
        "NPU auditor emitted no valid tool_requests while runtime tool context was available; "
        f"classification={classification}; runtime_tool_context_report_count={len(runtime_tool_context_reports)}"
    )
    requests = deterministic_fallback_tool_requests(reason, max_requests=max_requests)
    normalized: list[dict[str, Any]] = []
    for index, request in enumerate(requests, start=1):
        item = dict(request)
        item["id"] = f"npu_{item.get('id') or f'fallback_{index:03d}'}"
        item["source"] = "npu_deterministic_fallback"
        item["reason"] = f"NPU deterministic fallback: {item.get('reason', reason)}"
        normalized.append(item)
    return normalized
