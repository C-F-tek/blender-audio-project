"""FINAL_PRODUCT_DELTA parsing and code grounding helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ia_carmine._shared.provider_tool_schemas import (
    broker_tool_api_definitions,
    validate_broker_tool_api_definitions,
)
from ia_carmine.runtime.heap_gate.runtime_common import read_json, safe_dict, safe_int


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
    pattern = rf"(?im)^\s*(?:[-*]\s*)?(?:#+\s*)?{re.escape(field_name)}\s*(?:=|:)\s*`?([A-Za-z_]+)`?"
    match = re.search(pattern, response_text or "")
    return match.group(1).strip().lower() if match else ""


def section_body(response_text: str, section_name: str) -> str:
    section_names = (
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
        rf"(?ims)^\s*(?:#+\s*)?{re.escape(section_name)}\s*(?:=|:)?\s*"
        rf"(.*?)(?=^\s*(?:#+\s*)?(?:{stop_names})\b|\Z)"
    )
    match = re.search(pattern, response_text or "")
    return match.group(1).strip() if match else ""


def final_product_protocol(response_text: str) -> dict[str, Any]:
    allowed_kinds = {"text", "code", "text_and_code"}
    allowed_actions = {"append", "replace", "supersede", "refine"}
    kind = scalar_field(response_text, "FINAL_PRODUCT_KIND")
    action = scalar_field(response_text, "FINAL_PRODUCT_ACTION")
    delta = section_body(response_text, "FINAL_PRODUCT_DELTA")
    current_pointer_present = bool(
        re.search(r"(?im)^\s*(?:#+\s*)?CURRENT_POINTER\b", response_text or "")
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
        "current_pointer_present": current_pointer_present,
        "pointer_fields_present": pointer_fields_present,
        "pointer_protocol_operational": pointer_operational,
        "consumed_evidence_present": bool(consumed_evidence),
        "next_runtime_intent_present": bool(next_runtime_intent),
        "errors": errors,
    }


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
        report = {}
        json_report = str(outputs.get("json_report") or "").strip()
        if json_report:
            report_path = Path(json_report)
            if not report_path.is_absolute():
                report_path = owner.repo_root / report_path
            report = read_json(report_path)
        report_passed = report.get("passed") if report else summary.get("passed")
        if payload.get("provider_native_tool_call") is not True:
            continue
        if payload.get("blocked"):
            continue
        if safe_int(payload.get("returncode"), default=1) != 0:
            continue
        errors = payload.get("errors") if isinstance(payload.get("errors"), list) else []
        if errors:
            continue
        if report_passed is not True:
            continue
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
