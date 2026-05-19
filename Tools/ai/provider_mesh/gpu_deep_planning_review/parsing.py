from __future__ import annotations

from .common import *  # noqa: F403

def parse_model_json_with_diagnostics(
    text: str,
    evidence_ready_for_manual_patch_count_value: int = 0,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Parse one model response and attach shared GPU JSON contract diagnostics."""

    contract_result = validate_model_response_contract(
        text,
        evidence_ready_for_manual_patch_count=evidence_ready_for_manual_patch_count_value,
    )
    contract = result_to_dict(contract_result, include_parsed=False)
    diagnostics: dict[str, Any] = {
        **contract,
        "contract": contract,
        "contract_empty_recommendations_reason": contract_result.empty_recommendations_reason,
        "model_output_schema_mismatch": contract_result.json_ok and not contract_result.schema_ok,
        # Legacy field retained for report consumers that still read the old name.
        "model_output_missing_required_fields": contract_result.json_ok
        and not contract_result.schema_ok,
        # The shared contract parser is strict; repair attempts are not the preferred classifier anymore.
        "repair_attempt_count": 0,
    }

    if not contract_result.json_ok:
        return (
            {
                "summary": text[:2000],
                "confidence": "low",
                "recommendations": [],
                "tool_requests": [],
                "missing_evidence": ["model_response_not_valid_json"],
                "next_best_action": "review raw model response",
            },
            diagnostics,
        )

    parsed = dict(contract_result.parsed)
    recommendations = parsed.get("recommendations")
    if not isinstance(recommendations, list):
        parsed["recommendations"] = []
    if not isinstance(parsed.get("tool_requests", []), list):
        parsed["tool_requests"] = []
    parsed.setdefault("missing_evidence", [])
    parsed.setdefault("next_best_action", "")
    return parsed, diagnostics

def parse_model_json(text: str) -> dict[str, Any]:
    parsed, _diagnostics = parse_model_json_with_diagnostics(text)
    return parsed

def _raw_recommendations(parsed: dict[str, Any]) -> list[Any]:
    recommendations = parsed.get("recommendations", [])
    return recommendations if isinstance(recommendations, list) else []

def deterministic_tool_fallback_reason_from_parsed(parsed: dict[str, Any]) -> str:
    """Return a fallback reason when provider output has no usable tool requests.

    This does not execute tools. It only decides whether the existing runtime
    broker should receive safe deterministic fallback requests. The fallback is
    explicitly marked as deterministic_fallback by runtime_tool_guidance.
    """

    if not isinstance(parsed, dict):
        return "model_output_schema_mismatch"
    raw_requests = parsed.get("tool_requests")
    if isinstance(raw_requests, list) and raw_requests:
        return ""
    recommendations = parsed.get("recommendations")
    if isinstance(recommendations, list) and recommendations:
        return ""

    keys = set(parsed)
    if keys & {
        "response",
        "files",
        "context_files",
        "repository_files",
        "file_previews",
    }:
        return (
            "context_echo_detected"
            if "files" in keys or "context_files" in keys
            else "model_output_schema_mismatch"
        )

    missing = parsed.get("missing_evidence")
    if isinstance(missing, list) and any(
        str(item) == "model_response_not_valid_json" for item in missing
    ):
        return "json_parse_failure"

    next_best_action = str(parsed.get("next_best_action") or "").strip()
    summary = str(parsed.get("summary") or "").strip()
    if next_best_action or summary or missing:
        return "evidence_ready_but_no_tool_requests"
    return ""

def extract_valid_tool_requests(
    parsed: dict[str, Any], *, max_requests: int = 8
) -> tuple[list[dict[str, Any]], list[str]]:
    """Return broker-compatible valid runtime tool requests and validation errors.

    This helper does not execute tools. It only reuses the shared GPU planner
    contract validator to keep planner, supervised runner and orchestrator
    semantics aligned.
    """

    raw_requests = parsed.get("tool_requests", [])
    if raw_requests in (None, []):
        fallback_reason = deterministic_tool_fallback_reason_from_parsed(parsed)
        if fallback_reason:
            return (
                deterministic_fallback_tool_requests(fallback_reason, max_requests=max_requests),
                [],
            )
        return [], []
    if not isinstance(raw_requests, list):
        return [], ["top-level tool_requests must be a list"]

    valid: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, item in enumerate(raw_requests):
        item_errors = validate_tool_request_object(item, index)
        if item_errors:
            errors.extend(item_errors)
            continue
        if len(valid) >= max_requests:
            errors.append(f"tool_requests[{index}] skipped: max_requests={max_requests} reached")
            continue
        valid.append(dict(item))
    return valid, errors

def classify_empty_recommendations(
    *,
    json_ok: bool,
    parse_error: str,
    repair_attempt_count: int,
    model_output_missing_required_fields: bool,
    model_output_schema_mismatch: bool,
    context_echo_detected: bool,
    raw_recommendation_candidate_count: int,
    filtered_recommendation_count: int,
    evidence_ready_for_manual_patch_count_value: int,
    valid_tool_request_count: int = 0,
) -> str:
    if filtered_recommendation_count > 0:
        return ""
    if valid_tool_request_count > 0:
        return "tool_requests_pending"
    if context_echo_detected:
        return "context_echo_detected"
    if not json_ok:
        return "json_parse_failure"
    if model_output_schema_mismatch or model_output_missing_required_fields:
        return "model_output_schema_mismatch"
    if raw_recommendation_candidate_count > 0 and filtered_recommendation_count == 0:
        return "recommendations_filtered_out"
    if evidence_ready_for_manual_patch_count_value > 0:
        return "evidence_ready_but_no_tool_requests"
    return "valid_json_empty_recommendations"

def recommendation_diagnostics_for_round(
    parsed: dict[str, Any],
    parse_diagnostics: dict[str, Any],
    evidence_ready_for_manual_patch_count_value: int,
) -> dict[str, Any]:
    raw_recommendations = _raw_recommendations(parsed)
    raw_count = len(raw_recommendations)
    tool_requests = parsed.get("tool_requests", [])
    tool_request_count = len(tool_requests) if isinstance(tool_requests, list) else 0
    filtered_count = int(parse_diagnostics.get("valid_recommendation_count") or 0)
    if "valid_recommendation_count" not in parse_diagnostics:
        filtered_count = sum(1 for rec in raw_recommendations if isinstance(rec, dict))
    reason = classify_empty_recommendations(
        json_ok=bool(parse_diagnostics.get("json_ok")),
        parse_error=str(parse_diagnostics.get("parse_error") or ""),
        repair_attempt_count=int(parse_diagnostics.get("repair_attempt_count") or 0),
        model_output_missing_required_fields=bool(
            parse_diagnostics.get("model_output_missing_required_fields")
        ),
        model_output_schema_mismatch=bool(parse_diagnostics.get("model_output_schema_mismatch")),
        context_echo_detected=bool(parse_diagnostics.get("context_echo_detected")),
        raw_recommendation_candidate_count=raw_count,
        filtered_recommendation_count=filtered_count,
        evidence_ready_for_manual_patch_count_value=evidence_ready_for_manual_patch_count_value,
        valid_tool_request_count=int(parse_diagnostics.get("valid_tool_request_count") or 0),
    )
    return {
        "json_ok": bool(parse_diagnostics.get("json_ok")),
        "parse_error": str(parse_diagnostics.get("parse_error") or ""),
        "schema_ok": bool(parse_diagnostics.get("schema_ok")),
        "schema_errors": list(parse_diagnostics.get("schema_errors") or []),
        "context_echo_detected": bool(parse_diagnostics.get("context_echo_detected")),
        "model_output_schema_mismatch": bool(parse_diagnostics.get("model_output_schema_mismatch")),
        "contract_empty_recommendations_reason": str(
            parse_diagnostics.get("contract_empty_recommendations_reason") or ""
        ),
        "contract": parse_diagnostics.get("contract", {}),
        "repair_attempt_count": int(parse_diagnostics.get("repair_attempt_count") or 0),
        "raw_recommendation_candidate_count": raw_count,
        "filtered_recommendation_count": filtered_count,
        "recommendation_count": filtered_count,
        "tool_request_count": tool_request_count,
        "valid_tool_request_count": int(parse_diagnostics.get("valid_tool_request_count") or 0),
        "invalid_tool_request_count": int(parse_diagnostics.get("invalid_tool_request_count") or 0),
        "empty_recommendations_reason": reason,
        "evidence_ready_for_manual_patch_count": evidence_ready_for_manual_patch_count_value,
        "provider_tool_request_absence_reason": (
            reason if reason == "evidence_ready_but_no_tool_requests" else ""
        ),
        "recommended_next_layer": (
            "python -m Tools.ai agent_review_patch_plan"
            if reason in {"evidence_ready_but_no_gpu_plan", "evidence_ready_but_no_tool_requests"}
            else ""
        ),
    }

def aggregate_recommendation_diagnostics(
    rounds: list[dict[str, Any]], evidence: dict[str, Any]
) -> dict[str, Any]:
    evidence_ready_count = evidence_ready_for_manual_patch_count(evidence)
    raw_count = sum(
        int(round_result.get("raw_recommendation_candidate_count") or 0) for round_result in rounds
    )
    filtered_count = len(merge_recommendations(rounds))
    repair_attempt_count = sum(
        int(round_result.get("repair_attempt_count") or 0) for round_result in rounds
    )
    json_parse_error_count = sum(
        1 for round_result in rounds if not round_result.get("json_ok", True)
    )
    context_echo_detected_count = sum(
        1 for round_result in rounds if round_result.get("context_echo_detected")
    )
    model_output_schema_mismatch_count = sum(
        1
        for round_result in rounds
        if round_result.get("model_output_schema_mismatch")
        or round_result.get("empty_recommendations_reason") == "model_output_schema_mismatch"
        or round_result.get("empty_recommendations_reason")
        == "model_output_missing_required_fields"
    )
    tool_request_count = sum(
        int(round_result.get("tool_request_count") or 0) for round_result in rounds
    )
    valid_tool_request_count = sum(
        int(round_result.get("valid_tool_request_count") or 0) for round_result in rounds
    )
    invalid_tool_request_count = sum(
        int(round_result.get("invalid_tool_request_count") or 0) for round_result in rounds
    )
    parse_errors = [
        str(round_result.get("parse_error"))
        for round_result in rounds
        if round_result.get("parse_error")
    ]

    reason = ""
    if filtered_count == 0:
        if context_echo_detected_count:
            reason = "context_echo_detected"
        elif json_parse_error_count:
            reason = "json_parse_failure"
        elif model_output_schema_mismatch_count:
            reason = "model_output_schema_mismatch"
        elif raw_count > 0:
            reason = "recommendations_filtered_out"
        elif valid_tool_request_count > 0:
            reason = "tool_requests_pending"
        elif evidence_ready_count > 0:
            reason = "evidence_ready_but_no_tool_requests"
        else:
            reason = "valid_json_empty_recommendations"

    return {
        "json_parse_error_count": json_parse_error_count,
        "context_echo_detected_count": context_echo_detected_count,
        "model_output_schema_mismatch_count": model_output_schema_mismatch_count,
        "parse_error": parse_errors[0] if parse_errors else "",
        "repair_attempt_count": repair_attempt_count,
        "raw_recommendation_candidate_count": raw_count,
        "filtered_recommendation_count": filtered_count,
        "tool_request_count": tool_request_count,
        "valid_tool_request_count": valid_tool_request_count,
        "invalid_tool_request_count": invalid_tool_request_count,
        "empty_recommendations_reason": reason,
        "evidence_ready_for_manual_patch_count": evidence_ready_count,
        "provider_tool_request_absence_reason": (
            reason if reason == "evidence_ready_but_no_tool_requests" else ""
        ),
        "recommended_next_layer": (
            "python -m Tools.ai agent_review_patch_plan"
            if evidence_ready_count > 0 or filtered_count > 0
            else "collect_more_evidence"
        ),
    }
