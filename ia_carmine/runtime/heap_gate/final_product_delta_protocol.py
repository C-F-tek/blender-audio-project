"""FINAL_PRODUCT_DELTA parsing and code grounding helpers."""

from __future__ import annotations

import json
import re
from typing import Any

from ia_carmine._shared.provider_tool_schemas import (
    broker_tool_api_definitions,
    validate_broker_tool_api_definitions,
)
from ia_carmine.runtime.heap_gate.broker_result_validation import (
    broker_result_passed,
    broker_result_report,
)
from ia_carmine.runtime.heap_gate.runtime_common import safe_dict

PROTOCOL_SECTION_NAMES = (
    "FINAL_PRODUCT_KIND",
    "FINAL_PRODUCT_ACTION",
    "CURRENT_POINTER",
    "CONSUMED_EVIDENCE",
    "NEXT_RUNTIME_INTENT",
    "FINAL_PRODUCT_DELTA",
    "TARGET_FILES",
    "PROBLEM",
    "IMPLEMENTATION_CHANGES",
    "PATCH_SKETCH_UNIFIED_DIFF",
    "VALIDATION_COMMANDS",
    "RISKS",
    "EXIT_DECISION",
)


def normalize_markdown_protocol_markers(response_text: str) -> str:
    names = "|".join(re.escape(name) for name in PROTOCOL_SECTION_NAMES)
    return re.sub(
        rf"(?im)^(\s*(?:[-*]\s*)?(?:#+\s*)?)\*\*((?:{names}))\s*([=:])\*\*",
        r"\1\2\3",
        response_text or "",
    )


def pointer_field_declared(response_text: str, field_name: str) -> bool:
    patterns = [
        rf"(?im)^\s*-?\s*{re.escape(field_name)}\s*=\s*[^\n\r]*",
        rf"(?im)^\s*{re.escape(field_name)}\s*:\s*[^\n\r]*",
    ]
    return any(re.search(pattern, response_text or "") for pattern in patterns)


def pointer_action(response_text: str, quality_passed: bool) -> str:
    match = re.search(r"POINTER_ACTION\s*=\s*([A-Z_]+)", response_text or "")
    if match:
        return match.group(1)
    if "EXIT_DECISION=NO_PATCHABLE_TARGET" in (response_text or ""):
        return "NO_PATCHABLE_TARGET"
    return "STAY_FORWARD" if quality_passed else "BACKTRACK_PROPAGATE"


def exit_decision(response_text: str, target_files: list[str]) -> str:
    match = re.search(r"EXIT_DECISION\s*=\s*([A-Z_]+)", response_text or "")
    if match:
        return match.group(1)
    if target_files:
        return "PATCHABLE_TARGET"
    return "NO_PATCHABLE_TARGET"


def pointer_field(response_text: str, field_name: str) -> str:
    pattern = rf"(?im)^\s*-?\s*{re.escape(field_name)}\s*=\s*([^\n\r]+)"
    match = re.search(pattern, response_text or "")
    if match:
        return match.group(1).strip()
    pattern = rf"(?im)^\s*{re.escape(field_name)}\s*:\s*([^\n\r]+)"
    match = re.search(pattern, response_text or "")
    return match.group(1).strip() if match else ""


def scalar_field(response_text: str, field_name: str) -> str:
    response_text = normalize_markdown_protocol_markers(response_text)
    pattern = rf"(?im)^\s*(?:[-*]\s*)?(?:#+\s*)?\*{{0,2}}{re.escape(field_name)}\*{{0,2}}\s*(?:=|:)\s*`?([A-Za-z_]+)`?"
    match = re.search(pattern, response_text or "")
    return match.group(1).strip().lower() if match else ""


def section_body(response_text: str, section_name: str) -> str:
    response_text = normalize_markdown_protocol_markers(response_text)
    section_names = PROTOCOL_SECTION_NAMES
    if section_name == "FINAL_PRODUCT_DELTA":
        section_names = (
            "FINAL_PRODUCT_KIND",
            "FINAL_PRODUCT_ACTION",
            "CURRENT_POINTER",
            "CONSUMED_EVIDENCE",
            "NEXT_RUNTIME_INTENT",
            "TARGET_FILES",
            "VALIDATION_COMMANDS",
            "RISKS",
            "EXIT_DECISION",
        )
    stop_names = "|".join(re.escape(name) for name in section_names if name != section_name)
    pattern = (
        rf"(?ims)^\s*(?:[-*]\s*)?(?:#+\s*)?\*{{0,2}}{re.escape(section_name)}\*{{0,2}}\s*(?:=|:)?\s*"
        rf"(.*?)(?=^\s*(?:[-*]\s*)?(?:#+\s*)?\*{{0,2}}(?:{stop_names})\*{{0,2}}\b|\Z)"
    )
    match = re.search(pattern, response_text or "")
    return match.group(1).strip() if match else ""


def final_product_protocol(response_text: str) -> dict[str, Any]:
    response_text = normalize_markdown_protocol_markers(response_text)
    json_protocol = _json_final_product_protocol(response_text)
    if json_protocol is not None:
        return json_protocol
    allowed_kinds = {"text", "code", "text_and_code"}
    allowed_actions = {"append", "replace", "supersede", "refine"}
    kind = scalar_field(response_text, "FINAL_PRODUCT_KIND")
    action = scalar_field(response_text, "FINAL_PRODUCT_ACTION")
    delta = section_body(response_text, "FINAL_PRODUCT_DELTA")
    current_pointer_present = bool(
        re.search(r"(?im)^\s*(?:[-*]\s*)?(?:#+\s*)?\*{0,2}CURRENT_POINTER\*{0,2}\b", response_text or "")
    )
    pointer_fields_present = {
        "previous_block_id": pointer_field_declared(response_text, "previous_block_id"),
        "refines_block_id": pointer_field_declared(response_text, "refines_block_id"),
        "resume_from_block_id": pointer_field_declared(response_text, "resume_from_block_id"),
    }
    consumed_evidence = section_body(response_text, "CONSUMED_EVIDENCE")
    next_runtime_intent = section_body(response_text, "NEXT_RUNTIME_INTENT")
    errors: list[str] = []
    if kind not in allowed_kinds:
        errors.append("gpu1_final_product_kind_invalid_or_missing")
    if action not in allowed_actions:
        errors.append("gpu1_final_product_action_invalid_or_missing")
    if kind == "blocked" or action in {"blocked", "block"}:
        errors.append("gpu1_blocked_not_allowed_as_final_product_delta")
    if not delta:
        errors.append("gpu1_final_product_delta_missing")
    missing_pointer_fields = [
        name for name, present in pointer_fields_present.items() if not present
    ]
    pointer_operational = bool(current_pointer_present and not missing_pointer_fields)
    if not pointer_operational:
        errors.append("gpu1_pointer_protocol_not_operational")
    if not consumed_evidence:
        errors.append("gpu1_consumed_evidence_section_missing")
    if not next_runtime_intent:
        errors.append("gpu1_next_runtime_intent_missing")
    return {
        "passed": not errors,
        "kind": kind,
        "action": action,
        "delta": delta,
        "delta_chars": len(delta),
        "previous_block_id": pointer_field(response_text, "previous_block_id"),
        "refines_block_id": pointer_field(response_text, "refines_block_id"),
        "resume_from_block_id": pointer_field(response_text, "resume_from_block_id"),
        "consumed_evidence_text": consumed_evidence,
        "diagnostic_tool_failures_text": section_body(response_text, "DIAGNOSTIC_TOOL_FAILURES"),
        "current_pointer_present": current_pointer_present,
        "pointer_fields_present": pointer_fields_present,
        "pointer_protocol_operational": pointer_operational,
        "consumed_evidence_present": bool(consumed_evidence),
        "next_runtime_intent_present": bool(next_runtime_intent),
        "errors": errors,
    }


def _json_final_product_protocol(response_text: str) -> dict[str, Any] | None:
    payload = _json_object(response_text)
    if not payload or not any(str(key).startswith("FINAL_PRODUCT_") for key in payload):
        return None
    allowed_kinds = {"text", "code", "text_and_code"}
    allowed_actions = {"append", "replace", "supersede", "refine"}
    kind = str(payload.get("FINAL_PRODUCT_KIND") or "").strip().lower()
    action = str(payload.get("FINAL_PRODUCT_ACTION") or "").strip().lower()
    delta = str(payload.get("FINAL_PRODUCT_DELTA") or "").strip()
    pointer = payload.get("CURRENT_POINTER")
    pointer_items = pointer if isinstance(pointer, list) else [pointer]
    pointer_dict = next((item for item in pointer_items if isinstance(item, dict)), {})
    pointer_fields_present = {
        "previous_block_id": bool(str(pointer_dict.get("previous_block_id") or "").strip()),
        "refines_block_id": "refines_block_id" in pointer_dict,
        "resume_from_block_id": bool(str(pointer_dict.get("resume_from_block_id") or "").strip()),
    }
    consumed = payload.get("CONSUMED_EVIDENCE")
    consumed_present = bool(consumed if isinstance(consumed, list) else str(consumed or "").strip())
    intent = payload.get("NEXT_RUNTIME_INTENT")
    intent_present = bool(intent if isinstance(intent, list) else str(intent or "").strip())
    errors: list[str] = []
    if kind not in allowed_kinds:
        errors.append("gpu1_final_product_kind_invalid_or_missing")
    if action not in allowed_actions:
        errors.append("gpu1_final_product_action_invalid_or_missing")
    if kind == "blocked" or action in {"blocked", "block"}:
        errors.append("gpu1_blocked_not_allowed_as_final_product_delta")
    if not delta:
        errors.append("gpu1_final_product_delta_missing")
    missing_pointer_fields = [name for name, present in pointer_fields_present.items() if not present]
    pointer_operational = bool(isinstance(pointer_dict, dict) and pointer_dict and not missing_pointer_fields)
    if not pointer_operational:
        errors.append("gpu1_pointer_protocol_not_operational")
    if not consumed_present:
        errors.append("gpu1_consumed_evidence_section_missing")
    if not intent_present:
        errors.append("gpu1_next_runtime_intent_missing")
    return {
        "passed": not errors,
        "kind": kind,
        "action": action,
        "delta": delta,
        "delta_chars": len(delta),
        "previous_block_id": str(pointer_dict.get("previous_block_id") or ""),
        "refines_block_id": str(pointer_dict.get("refines_block_id") or ""),
        "resume_from_block_id": str(pointer_dict.get("resume_from_block_id") or ""),
        "consumed_evidence_text": json.dumps(consumed, ensure_ascii=False) if not isinstance(consumed, str) else consumed,
        "diagnostic_tool_failures_text": json.dumps(payload.get("DIAGNOSTIC_TOOL_FAILURES"), ensure_ascii=False),
        "current_pointer_present": bool(pointer_dict),
        "pointer_fields_present": pointer_fields_present,
        "pointer_protocol_operational": pointer_operational,
        "consumed_evidence_present": consumed_present,
        "next_runtime_intent_present": intent_present,
        "errors": errors,
    }


def final_product_delta_runtime_classification(
    response_text: str,
    *,
    protocol: dict[str, Any] | None = None,
    consumption: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify whether a syntactically valid delta is operator product evidence."""
    protocol = protocol if isinstance(protocol, dict) else final_product_protocol(response_text)
    consumption = consumption if isinstance(consumption, dict) else {}
    delta = str(protocol.get("delta") or "").strip()
    lowered = delta.lower()
    consumed_failed_ids = [
        str(item)
        for item in (
            consumption.get("gpu1_invalid_consumed_failed_tool_result_ids")
            or consumption.get("gpu1_consumed_failed_tool_result_ids")
            or []
        )
        if str(item).strip()
    ]
    errors: list[str] = []
    classification = "operator_product_delta"
    if protocol.get("pointer_protocol_operational") is not True:
        errors.append("gpu1_pointer_protocol_not_operational")
        classification = "raw_gpu1_text_evidence"
    if consumed_failed_ids:
        errors.append("gpu1_consumed_failed_tool_result_as_evidence")
        classification = "diagnostic_non_product_delta"
    if _looks_like_tool_loop_summary(lowered):
        errors.append("gpu1_delta_tool_loop_summary_not_operator_product")
        classification = "diagnostic_non_product_delta"
    if _dominates_failed_tool_discussion(lowered):
        errors.append("gpu1_delta_failed_tool_summary_not_operator_product")
        classification = "diagnostic_non_product_delta"
    if _looks_like_correction(delta) and not str(protocol.get("refines_block_id") or "").strip():
        errors.append("gpu1_delta_correction_missing_refines_block_id")
        if classification == "operator_product_delta":
            classification = "raw_gpu1_text_evidence"
    if not delta:
        errors.append("gpu1_final_product_delta_missing")
        classification = "raw_gpu1_text_evidence"
    errors = list(dict.fromkeys(errors))
    return {
        "classification": classification,
        "operator_delta_valid": not errors,
        "final_product_delta_valid": bool(protocol.get("passed") and not errors),
        "errors": errors,
        "consumed_failed_tool_result_ids": consumed_failed_ids,
        "previous_block_id": str(protocol.get("previous_block_id") or ""),
        "refines_block_id": str(protocol.get("refines_block_id") or ""),
        "resume_from_block_id": str(protocol.get("resume_from_block_id") or ""),
    }


def _looks_like_tool_loop_summary(lowered_delta: str) -> bool:
    blocked_phrases = (
        "tool loop has reached its soft stop",
        "tool loop has reached its subturn budget",
        "following findings have been made",
        "summary of the tool loop execution",
        "this final product provides a summary of the tool loop execution",
    )
    if any(phrase in lowered_delta for phrase in blocked_phrases):
        return True
    section_markers = (
        "toolchain probe",
        "runtime file window",
        "diagnostic tool failures",
        "next steps",
        "broker result",
    )
    product_markers = (
        "target_files",
        "implementation_changes",
        "validation_commands",
        "patch_sketch",
        "operator",
        "fix",
        "correction",
    )
    return (
        sum(1 for marker in section_markers if marker in lowered_delta) >= 3
        and not any(marker in lowered_delta for marker in product_markers)
    )


def _dominates_failed_tool_discussion(lowered_delta: str) -> bool:
    failure_hits = sum(
        lowered_delta.count(marker)
        for marker in (
            "failed tool",
            "tool failed",
            "diagnostic tool failures",
            "returncode",
            "file not found",
            "runtime_file_window_path_not_in_startup_refs",
        )
    )
    product_hits = sum(
        lowered_delta.count(marker)
        for marker in ("target_files", "implementation_changes", "validation_commands", "patch", "answer")
    )
    return failure_hits >= 2 and product_hits == 0


def _looks_like_correction(delta: str) -> bool:
    lowered = delta.lower()
    return any(
        marker in lowered
        for marker in (
            "corregg",
            "correction",
            "refine",
            "rifiut",
            "rejected",
            "veto",
            "previous error",
            "errore precedente",
        )
    )


def _json_object(response_text: str) -> dict[str, Any]:
    candidate = (response_text or "").strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        candidate = "\n".join(lines).strip()
    try:
        value = json.loads(candidate)
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def response_mentions_code_diff(response_text: str) -> bool:
    return bool(
        re.search(r"(?im)^\s*(?:#+\s*)?PATCH_SKETCH_UNIFIED_DIFF\b", response_text or "")
        or re.search(r"(?im)^\s*diff --git a/", response_text or "")
        or re.search(r"(?im)^```diff\s*$", response_text or "")
    )


def broker_file_read_results(owner: Any, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for payload in owner.broker_results(events):
        if str(payload.get("tool") or "") not in {"runtime_file_window", "runtime_read_file"}:
            continue
        outputs = safe_dict(payload.get("outputs"))
        summary = safe_dict(payload.get("summary"))
        if payload.get("provider_native_tool_call") is not True:
            continue
        if not broker_result_passed(
            payload,
            repo_root=getattr(owner, "repo_root", None),
            require_report_passed=True,
        ):
            continue
        report = broker_result_report(payload, repo_root=getattr(owner, "repo_root", None))
        json_report = str(outputs.get("json_report") or "").strip()
        refs = [
            str(payload.get("request_id") or ""),
            str(payload.get("normalized_request_id") or ""),
            str(json_report or ""),
            str(outputs.get("markdown_report") or ""),
            str(outputs.get("evidence_json") or ""),
            str(outputs.get("evidence_markdown") or ""),
            str(safe_dict(report.get("source_ref")).get("path") or ""),
            str(report.get("path") or ""),
        ]
        results.append(
            {
                "tool": str(payload.get("tool") or ""),
                "request_id": str(payload.get("request_id") or ""),
                "normalized_request_id": str(payload.get("normalized_request_id") or ""),
                "provider_native_tool_call": True,
                "returncode": payload.get("returncode"),
                "outputs": outputs,
                "summary": summary,
                "report_kind": report.get("kind") or summary.get("kind"),
                "source_path": report.get("path") or safe_dict(report.get("source_ref")).get("path") or "",
                "refs": [item for item in refs if item],
            }
        )
    return results


def code_file_read_contract(
    owner: Any,
    *,
    response_text: str,
    protocol: dict[str, Any],
    target_files: list[str],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    kind = str(protocol.get("kind") or "")
    diff_present = response_mentions_code_diff(response_text)
    requires_file_read = kind in {"code", "text_and_code"} or diff_present
    consumed_evidence = section_body(response_text, "CONSUMED_EVIDENCE")
    next_runtime_intent = section_body(response_text, "NEXT_RUNTIME_INTENT")
    file_read_results = broker_file_read_results(owner, events)
    tool_api_definitions = broker_tool_api_definitions(["runtime_file_window"])
    tool_api_validation = validate_broker_tool_api_definitions(tool_api_definitions)
    consumed_text = consumed_evidence.lower()
    consumed = []
    for result in file_read_results:
        refs = [str(item) for item in result.get("refs", []) if str(item).strip()]
        if any(ref and ref.lower() in consumed_text for ref in refs):
            consumed.append(result)
    tool_request_needed = bool(
        re.search(r"runtime_(?:file_window|read_file)|file[-_ ]?read", next_runtime_intent, re.IGNORECASE)
    )
    errors: list[str] = []
    if requires_file_read:
        if not tool_api_definitions:
            errors.append("broker_tool_not_registered:runtime_file_window")
        elif not tool_api_validation.get("passed"):
            validation_errors = [
                str(item) for item in tool_api_validation.get("errors", []) if str(item).strip()
            ]
            for item in validation_errors:
                if "input_schema" in item:
                    errors.append("broker_tool_schema_missing_or_invalid:runtime_file_window")
                if "handler" in item:
                    errors.append("broker_tool_handler_unresolved:runtime_file_window")
            if not validation_errors:
                errors.append("broker_tool_schema_missing_or_invalid:runtime_file_window")
        if not target_files:
            errors.append("gpu1_code_delta_without_verified_target")
        if not file_read_results:
            errors.append("gpu1_code_delta_without_file_read")
        elif not consumed:
            errors.append("gpu1_code_delta_file_read_not_consumed")
    return {
        "required": requires_file_read,
        "verified": bool(requires_file_read and consumed and target_files),
        "diff_present": diff_present,
        "target_files": target_files,
        "available_file_read_result_count": len(file_read_results),
        "consumed_file_read_result_count": len(consumed),
        "tool_api_ready": bool(tool_api_definitions and tool_api_validation.get("passed")),
        "tool_api_definition_count": len(tool_api_definitions),
        "tool_api_errors": tool_api_validation.get("errors", []),
        "consumed_file_read_refs": [
            ref
            for result in consumed
            for ref in result.get("refs", [])
            if str(ref).strip()
        ],
        "tool_request_needed": tool_request_needed,
        "allowed_without_file_read": bool(kind == "text" and not diff_present),
        "errors": errors,
    }
