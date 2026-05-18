"""Validation for optional path/reference AI pipeline report sections."""

from __future__ import annotations

from typing import Any

from .common import add_error, is_non_empty_string, is_non_negative_int

def validate_enabled_path_ref(value: Any, path: str, errors: list[str], field_name: str) -> None:
    """Validate a small enabled/path-like subreport."""
    if not isinstance(value, dict):
        add_error(errors, path, "must be an object")
        return
    enabled = value.get("enabled")
    if not isinstance(enabled, bool):
        add_error(errors, f"{path}.enabled", "must be bool")
    target = value.get(field_name)
    if enabled is True and not is_non_empty_string(target):
        add_error(errors, f"{path}.{field_name}", "must be a non-empty string when enabled=true")
    if enabled is False and target is not None and not isinstance(target, str):
        add_error(errors, f"{path}.{field_name}", "must be string or null when enabled=false")


def validate_guardrail_loop(value: Any, path: str, errors: list[str]) -> None:
    """Validate guardrail remediation loop metadata."""
    if not isinstance(value, dict):
        add_error(errors, path, "must be an object")
        return
    if not isinstance(value.get("enabled"), bool):
        add_error(errors, f"{path}.enabled", "must be bool")
    if "max_passes" in value and not is_non_negative_int(value.get("max_passes")):
        add_error(errors, f"{path}.max_passes", "must be int >= 0 when present")
    passes = value.get("passes")
    if not isinstance(passes, list):
        add_error(errors, f"{path}.passes", "must be a list")
        return
    for index, item in enumerate(passes):
        item_path = f"{path}.passes[{index}]"
        if not isinstance(item, dict):
            add_error(errors, item_path, "must be an object")
            continue
        if "pass_index" in item and not is_non_negative_int(item.get("pass_index")):
            add_error(errors, f"{item_path}.pass_index", "must be int >= 0")
        if "status" in item and not is_non_empty_string(item.get("status")):
            add_error(errors, f"{item_path}.status", "must be a non-empty string when present")
        if "plan" in item and not isinstance(item.get("plan"), dict):
            add_error(errors, f"{item_path}.plan", "must be an object when present")
        if "steps" in item and not isinstance(item.get("steps"), list):
            add_error(errors, f"{item_path}.steps", "must be a list when present")


def validate_expected_outputs(value: Any, path: str, errors: list[str]) -> None:
    """Validate post-run expected output metadata."""
    if not isinstance(value, list):
        add_error(errors, path, "must be a list")
        return
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            add_error(errors, item_path, "must be an object")
            continue
        if not is_non_empty_string(item.get("path")):
            add_error(errors, f"{item_path}.path", "must be a non-empty string")
        if not isinstance(item.get("exists"), bool):
            add_error(errors, f"{item_path}.exists", "must be bool")
        if "size_bytes" in item and not is_non_negative_int(item.get("size_bytes")):
            add_error(errors, f"{item_path}.size_bytes", "must be int >= 0 when present")
        if "modified_time" in item and not is_non_empty_string(item.get("modified_time")):
            add_error(
                errors, f"{item_path}.modified_time", "must be a non-empty string when present"
            )
