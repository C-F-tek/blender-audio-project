"""Top-level AI pipeline report payload and file validators."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import (
    BASE_PIPELINE_REPORT_FIELDS,
    EXTENDED_PIPELINE_REPORT_FIELDS,
    PIPELINE_SCHEMA_VERSION,
    add_error,
    is_non_empty_string,
    is_non_negative_int,
    load_json_object,
)
from .refs import (
    validate_enabled_path_ref,
    validate_expected_outputs,
    validate_guardrail_loop,
)
from .sections import (
    validate_agent_state_packet,
    validate_lanes,
    validate_preflight,
    validate_schedule,
    validate_step,
    validate_summary,
)

def validate_ai_pipeline_report_payload(
    payload: dict[str, Any],
    *,
    require_dry_run: bool = False,
    path: str = "report",
) -> dict[str, Any]:
    """Validate one AI pipeline schema-v6 report payload."""
    errors: list[str] = []
    warnings: list[str] = []

    missing_base = sorted(BASE_PIPELINE_REPORT_FIELDS - set(payload))
    for field in missing_base:
        add_error(errors, f"{path}.{field}", "is missing")

    schema_version = payload.get("schema_version")
    if schema_version != PIPELINE_SCHEMA_VERSION:
        add_error(errors, f"{path}.schema_version", f"must be {PIPELINE_SCHEMA_VERSION}")
    if not is_non_empty_string(payload.get("generated_at")):
        add_error(errors, f"{path}.generated_at", "must be a non-empty string")
    if not is_non_empty_string(payload.get("repo_root")):
        add_error(errors, f"{path}.repo_root", "must be a non-empty string")
    if not is_non_empty_string(payload.get("output_dir")):
        add_error(errors, f"{path}.output_dir", "must be a non-empty string")
    if not isinstance(payload.get("dry_run"), bool):
        add_error(errors, f"{path}.dry_run", "must be bool")
    elif require_dry_run and payload.get("dry_run") is not True:
        add_error(errors, f"{path}.dry_run", "must be true")
    if not isinstance(payload.get("passed"), bool):
        add_error(errors, f"{path}.passed", "must be bool")

    preflight_passed = (
        validate_preflight(payload.get("preflight"), f"{path}.preflight", errors)
        if "preflight" in payload
        else None
    )
    is_preflight_failed_report = (
        preflight_passed is False
        and payload.get("passed") is False
        and payload.get("step_count") == 0
    )
    missing_extended = sorted(EXTENDED_PIPELINE_REPORT_FIELDS - set(payload))
    for field in missing_extended:
        if is_preflight_failed_report:
            add_warning(warnings, f"{path}.{field}", "missing in preflight-failed report")
        else:
            add_error(errors, f"{path}.{field}", "is missing")

    step_count = payload.get("step_count")
    if not is_non_negative_int(step_count):
        add_error(errors, f"{path}.step_count", "must be int >= 0")
        step_count_int: int | None = None
    else:
        step_count_int = step_count

    steps = payload.get("steps")
    step_names: list[str] = []
    if not isinstance(steps, list):
        add_error(errors, f"{path}.steps", "must be a list")
    else:
        if step_count_int is not None and len(steps) != step_count_int:
            add_error(errors, f"{path}.step_count", "must equal len(steps)")
        for index, step in enumerate(steps):
            name = validate_step(step, index, errors, warnings, require_dry_run)
            if name is not None:
                step_names.append(name)
        duplicates = sorted({name for name in step_names if step_names.count(name) > 1})
        if duplicates:
            add_error(errors, f"{path}.steps", f"duplicate step names: {', '.join(duplicates)}")

    if "summary" in payload:
        validate_summary(payload.get("summary"), f"{path}.summary", errors, step_count_int)
    if "schedule" in payload:
        if not (is_preflight_failed_report and payload.get("schedule") == {}):
            validate_schedule(payload.get("schedule"), f"{path}.schedule", errors, step_names)
    if "lanes" in payload:
        validate_lanes(payload.get("lanes"), f"{path}.lanes", errors, warnings, step_names)
    if "wave_entrypoint_review" in payload:
        validate_enabled_path_ref(
            payload.get("wave_entrypoint_review"),
            f"{path}.wave_entrypoint_review",
            errors,
            "report",
        )
    if "smart_context" in payload:
        smart_context = payload.get("smart_context")
        validate_enabled_path_ref(smart_context, f"{path}.smart_context", errors, "packet")
        smart_task = smart_context.get("task") if isinstance(smart_context, dict) else None
        smart_enabled = smart_context.get("enabled") if isinstance(smart_context, dict) else None
        if smart_enabled is True and not is_non_empty_string(smart_task):
            add_error(
                errors, f"{path}.smart_context.task", "must be a non-empty string when enabled=true"
            )
    if "agent_state_packet" in payload:
        validate_agent_state_packet(
            payload.get("agent_state_packet"), f"{path}.agent_state_packet", errors, warnings
        )
    if "guardrail_remediation_loop" in payload:
        validate_guardrail_loop(
            payload.get("guardrail_remediation_loop"), f"{path}.guardrail_remediation_loop", errors
        )
    if "post_run_expected_outputs" in payload:
        validate_expected_outputs(
            payload.get("post_run_expected_outputs"), f"{path}.post_run_expected_outputs", errors
        )

    if payload.get("passed") is True and isinstance(steps, list):
        failed_steps = [
            item.get("name") or f"steps[{index}]"
            for index, item in enumerate(steps)
            if isinstance(item, dict)
            and item.get("returncode") != 0
            and item.get("allow_failure") is not True
        ]
        if failed_steps:
            add_error(
                errors,
                f"{path}.passed",
                f"true but failed steps exist: {', '.join(str(item) for item in failed_steps)}",
            )

    return {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "schema_version": schema_version,
            "dry_run": payload.get("dry_run"),
            "report_passed": payload.get("passed"),
            "step_count": step_count if is_non_negative_int(step_count) else None,
            "validated_step_count": len(step_names),
            "preflight_passed": preflight_passed,
            "missing_base_fields": missing_base,
            "missing_extended_fields": missing_extended,
        },
    }


def validate_ai_pipeline_report_file(
    path: Path, *, require_dry_run: bool = False
) -> dict[str, Any]:
    """Load and validate one AI pipeline schema-v6 report file."""
    payload, load_error = load_json_object(path)
    if load_error:
        return {
            "passed": False,
            "errors": [load_error],
            "warnings": [],
            "checks": {
                "schema_version": None,
                "dry_run": None,
                "report_passed": None,
                "step_count": None,
                "validated_step_count": 0,
                "preflight_passed": None,
                "missing_base_fields": [],
                "missing_extended_fields": [],
            },
        }
    assert payload is not None
    return validate_ai_pipeline_report_payload(payload, require_dry_run=require_dry_run)
