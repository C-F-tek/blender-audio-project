from __future__ import annotations

import json
from typing import Any


def result_to_dict(result: Any, *, include_parsed: bool = False) -> dict[str, Any]:
    """Serialize a contract result for reports."""

    data: dict[str, Any] = {
        "json_ok": result.json_ok,
        "schema_ok": result.schema_ok,
        "context_echo_detected": result.context_echo_detected,
        "parse_error": result.parse_error,
        "schema_errors": list(result.schema_errors),
        "raw_response_sha256": result.raw_response_sha256,
        "raw_response_chars": result.raw_response_chars,
        "top_level_keys": list(result.top_level_keys),
        "recommendation_count": result.recommendation_count,
        "valid_recommendation_count": result.valid_recommendation_count,
        "invalid_recommendation_count": result.invalid_recommendation_count,
        "tool_request_count": result.tool_request_count,
        "valid_tool_request_count": result.valid_tool_request_count,
        "invalid_tool_request_count": result.invalid_tool_request_count,
        "empty_recommendations_reason": result.empty_recommendations_reason,
    }
    if include_parsed:
        data["parsed"] = result.parsed
    return data


def json_dumps_report(data: dict[str, Any]) -> str:
    """Dump report JSON with repository-standard formatting."""

    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"
