"""Generic runtime tool-cycle normalization.

This module intentionally uses tool_* wording. Legacy lab_* fields can keep
existing compatibility meanings, but every runtime tool can be summarized here.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


TERMINAL_FAILURE_STATUSES = {
    "parsed_invalid",
    "executed_failed",
    "executed_no_result",
    "result_written_unusable",
    "blocked_by_policy",
    "blocked_by_missing_args",
    "blocked_by_unknown_tool",
    "blocked_by_path_policy",
    "blocked_by_runtime_error",
}


def normalize_tool_cycle_status(record: dict[str, Any]) -> dict[str, Any]:
    """Return a generic tool_* lifecycle view for a broker/provider record."""
    record = record if isinstance(record, dict) else {}
    outputs = record.get("outputs") if isinstance(record.get("outputs"), dict) else {}
    errors = _strings(record.get("errors"))
    returncode = _safe_int(record.get("returncode"), default=None)
    tool_name = str(record.get("tool") or record.get("tool_name") or "").strip()
    requested = _truthy(record.get("tool_requested")) or bool(
        tool_name
        or record.get("request_id")
        or record.get("broker_request_id")
        or record.get("provider_native_tool_call")
    )
    parsed = (
        _truthy(record.get("tool_call_parsed"))
        or _truthy(record.get("provider_native_tool_call"))
        or bool(record.get("tool_call_id") or record.get("assistant_tool_call_id"))
    )
    validated = (
        _truthy(record.get("tool_call_validated"))
        or _truthy(record.get("validated"))
        or _truthy(record.get("schema_valid"))
        or bool(tool_name and not errors and record.get("blocked_by_unknown_tool") is not True)
    )
    attempted = (
        _truthy(record.get("tool_execution_attempted"))
        or returncode is not None
        or bool(record.get("executed") is not None)
    )
    performed = (
        _truthy(record.get("tool_execution_performed"))
        or _truthy(record.get("executed"))
        or returncode == 0
    )
    result_ref = record.get("tool_result_ref")
    if not isinstance(result_ref, dict):
        result_ref = tool_cycle_ref_from_outputs(outputs) or _result_ref_from_record(record)
    written = _truthy(record.get("tool_result_written")) or bool(result_ref)
    usable = _truthy(record.get("tool_result_usable")) or bool(
        written
        and performed
        and (record.get("passed") is True or record.get("summary", {}).get("passed") is True)
    )
    consumed = _truthy(record.get("tool_result_consumed_by_provider")) or _truthy(
        record.get("consumed_by_delta")
    )
    failure = _failure_reason(record, errors, returncode)
    status = _status(
        requested=requested,
        parsed=parsed,
        validated=validated,
        attempted=attempted,
        performed=performed,
        written=written,
        usable=usable,
        consumed=consumed,
        failure=failure,
    )
    return {
        "tool_requested": requested,
        "tool_call_parsed": parsed,
        "tool_call_validated": validated,
        "tool_execution_attempted": attempted,
        "tool_execution_performed": performed,
        "tool_result_written": written,
        "tool_result_ref": result_ref,
        "tool_result_usable": usable,
        "tool_result_consumed_by_provider": consumed,
        "tool_status": status,
        "tool_failure_reason": failure,
    }


def tool_cycle_ref_from_outputs(
    outputs: dict[str, Any],
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Return a stable artifact ref from common broker output fields."""
    outputs = outputs if isinstance(outputs, dict) else {}
    for key in (
        "json_report",
        "markdown_report",
        "evidence_json",
        "evidence_markdown",
        "debug_lab_report",
        "matrix_report",
        "stdout_path",
        "stderr_path",
    ):
        value = str(outputs.get(key) or "").strip()
        if value:
            return _artifact_ref(value, key, repo_root)
    return {}


def _status(
    *,
    requested: bool,
    parsed: bool,
    validated: bool,
    attempted: bool,
    performed: bool,
    written: bool,
    usable: bool,
    consumed: bool,
    failure: str,
) -> str:
    if not requested:
        return "not_requested"
    if not parsed:
        return "requested_unparsed"
    if not validated:
        return failure if failure.startswith("blocked_by_") else "parsed_invalid"
    if failure.startswith("blocked_by_"):
        return failure
    if not attempted:
        return "validated_not_executed"
    if attempted and not performed:
        return "executed_failed"
    if performed and not written:
        return "executed_no_result"
    if written and not usable:
        return "result_written_unusable"
    if written and usable and consumed:
        return "result_consumed"
    if written and usable:
        return "result_pending_provider_resume"
    return "blocked_by_runtime_error" if failure else "executed_failed"


def _failure_reason(
    record: dict[str, Any],
    errors: list[str],
    returncode: int | None,
) -> str:
    explicit = str(record.get("tool_failure_reason") or record.get("failure_reason") or "").strip()
    if explicit:
        return explicit
    if record.get("blocked_by_unknown_tool") is True:
        return "blocked_by_unknown_tool"
    if record.get("blocked_by_missing_args") is True:
        return "blocked_by_missing_args"
    if record.get("blocked_by_path_policy") is True:
        return "blocked_by_path_policy"
    joined = " ".join(errors).lower()
    if "unknown tool" in joined:
        return "blocked_by_unknown_tool"
    if "missing" in joined and "arg" in joined:
        return "blocked_by_missing_args"
    if "path" in joined and ("policy" in joined or "startup" in joined):
        return "blocked_by_path_policy"
    if returncode not in (None, 0):
        return "blocked_by_runtime_error"
    return errors[0] if errors else ""


def _result_ref_from_record(record: dict[str, Any]) -> dict[str, Any]:
    value = str(record.get("result_ref") or "").strip()
    return _artifact_ref(value, "result_ref", None) if value else {}


def _artifact_ref(value: str, kind: str, repo_root: str | Path | None) -> dict[str, Any]:
    path = Path(value)
    absolute = path
    if not absolute.is_absolute() and repo_root:
        absolute = Path(repo_root) / path
    ref = {"path": value.replace("\\", "/"), "kind": kind}
    if absolute.exists() and absolute.is_file():
        data = absolute.read_bytes()
        ref.update({"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return ref


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def _strings(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    text = str(value or "").strip()
    return [text] if text else []


def _safe_int(value: Any, default: int | None = 0) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
