"""Validation for core AI pipeline report sections."""

from __future__ import annotations

from typing import Any

from .common import (
    KNOWN_LANES,
    add_error,
    add_warning,
    is_int,
    is_non_empty_string,
    is_non_negative_int,
    is_non_negative_number,
)

def validate_agent_state_packet(
    packet: Any, path: str, errors: list[str], warnings: list[str]
) -> None:
    """Validate the optional agent_state_packet metadata sub-contract."""
    if not isinstance(packet, dict):
        add_error(errors, path, "must be an object when present")
        return

    enabled = packet.get("enabled")
    packet_path = packet.get("path")
    exists = packet.get("exists")
    source = packet.get("source")

    if not isinstance(enabled, bool):
        add_error(errors, f"{path}.enabled", "must be bool")
    if "exists" not in packet or not isinstance(exists, bool):
        add_error(errors, f"{path}.exists", "must be bool")
    if source not in {"disabled", "cli"}:
        add_error(errors, f"{path}.source", 'must be "disabled" or "cli"')

    if enabled is True:
        if source != "cli":
            add_error(errors, f"{path}.source", 'must be "cli" when enabled=true')
        if not is_non_empty_string(packet_path):
            add_error(errors, f"{path}.path", "must be a non-empty string when enabled=true")
        if "repo_relative_path" in packet and not is_non_empty_string(
            packet.get("repo_relative_path")
        ):
            add_error(
                errors, f"{path}.repo_relative_path", "must be a non-empty string when present"
            )
    elif enabled is False:
        if exists is not False:
            add_error(errors, f"{path}.exists", "must be false when enabled=false")
        if source != "disabled":
            add_error(errors, f"{path}.source", 'must be "disabled" when enabled=false')
        if packet_path is not None and not is_non_empty_string(packet_path):
            add_error(errors, f"{path}.path", "must be null/absent or a non-empty string")

    allowed_fields = {
        "enabled",
        "path",
        "exists",
        "source",
        "repo_relative_path",
        "size_bytes",
        "modified_time",
    }
    extra_fields = sorted(set(packet) - allowed_fields)
    if extra_fields:
        add_warning(warnings, path, f"accepted extra fields: {', '.join(extra_fields)}")


def validate_preflight(preflight: Any, path: str, errors: list[str]) -> bool | None:
    """Validate preflight report metadata and return its pass state when known."""
    if not isinstance(preflight, dict):
        add_error(errors, path, "must be an object")
        return None

    passed = preflight.get("passed")
    if not isinstance(passed, bool):
        add_error(errors, f"{path}.passed", "must be bool")
        passed = None
    for list_field in ("errors", "warnings"):
        value = preflight.get(list_field)
        if value is not None and not isinstance(value, list):
            add_error(errors, f"{path}.{list_field}", "must be list when present")
    return passed


def validate_summary(summary: Any, path: str, errors: list[str], step_count: int | None) -> None:
    """Validate schema-v6 summary semantics."""
    if not isinstance(summary, dict):
        add_error(errors, path, "must be an object")
        return

    for field in ("ok_count", "failed_count", "planned_only_count"):
        if not is_non_negative_int(summary.get(field)):
            add_error(errors, f"{path}.{field}", "must be int >= 0")
    if not is_non_negative_number(summary.get("total_duration_sec")):
        add_error(errors, f"{path}.total_duration_sec", "must be int or float >= 0")
    if not isinstance(summary.get("failed_steps"), list):
        add_error(errors, f"{path}.failed_steps", "must be a list")

    lane_counts = summary.get("lane_counts")
    if not isinstance(lane_counts, dict):
        add_error(errors, f"{path}.lane_counts", "must be an object")
    else:
        for lane, count in lane_counts.items():
            if not is_non_empty_string(lane):
                add_error(errors, f"{path}.lane_counts", "lane key must be a non-empty string")
            if not is_non_negative_int(count):
                add_error(errors, f"{path}.lane_counts.{lane}", "must be int >= 0")
        if step_count is not None and sum(lane_counts.values()) != step_count:
            add_error(errors, f"{path}.lane_counts", f"must sum to step_count {step_count}")

    ok_count = summary.get("ok_count")
    failed_count = summary.get("failed_count")
    planned_only_count = summary.get("planned_only_count")
    if (
        step_count is not None
        and is_non_negative_int(ok_count)
        and is_non_negative_int(failed_count)
    ):
        if ok_count + failed_count != step_count:
            add_error(errors, path, f"ok_count + failed_count must equal step_count {step_count}")
    if (
        step_count is not None
        and is_non_negative_int(planned_only_count)
        and planned_only_count > step_count
    ):
        add_error(errors, f"{path}.planned_only_count", "must be <= step_count")


def validate_schedule(schedule: Any, path: str, errors: list[str], step_names: list[str]) -> None:
    """Validate schema-v6 schedule semantics."""
    if not isinstance(schedule, dict):
        add_error(errors, path, "must be an object")
        return

    for field in ("serial_count", "parallel_count", "total_count"):
        if not is_non_negative_int(schedule.get(field)):
            add_error(errors, f"{path}.{field}", "must be int >= 0")
    for field in ("serial", "parallel"):
        value = schedule.get(field)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            add_error(errors, f"{path}.{field}", "must be a list of strings")
    if "parallel_lanes" in schedule and not (
        isinstance(schedule.get("parallel_lanes"), list)
        and all(isinstance(item, str) for item in schedule["parallel_lanes"])
    ):
        add_error(errors, f"{path}.parallel_lanes", "must be a list of strings when present")

    serial = schedule.get("serial") if isinstance(schedule.get("serial"), list) else []
    parallel = schedule.get("parallel") if isinstance(schedule.get("parallel"), list) else []
    serial_count = schedule.get("serial_count")
    parallel_count = schedule.get("parallel_count")
    total_count = schedule.get("total_count")
    if is_non_negative_int(serial_count) and len(serial) != serial_count:
        add_error(errors, f"{path}.serial_count", "must equal len(serial)")
    if is_non_negative_int(parallel_count) and len(parallel) != parallel_count:
        add_error(errors, f"{path}.parallel_count", "must equal len(parallel)")
    if is_non_negative_int(total_count):
        if (
            is_non_negative_int(serial_count)
            and is_non_negative_int(parallel_count)
            and total_count != serial_count + parallel_count
        ):
            add_error(errors, f"{path}.total_count", "must equal serial_count + parallel_count")
        if total_count != len(step_names):
            add_error(errors, f"{path}.total_count", "must equal step_count")
    scheduled_names = [*serial, *parallel]
    if sorted(scheduled_names) != sorted(step_names):
        add_error(errors, path, "serial + parallel step names must match report steps")


def validate_lanes(
    lanes: Any, path: str, errors: list[str], warnings: list[str], step_names: list[str]
) -> None:
    """Validate lane grouping semantics."""
    if not isinstance(lanes, dict):
        add_error(errors, path, "must be an object")
        return

    for required_lane in ("CPU", "NPU", "GPU"):
        if required_lane not in lanes:
            add_error(errors, path, f"missing required lane key: {required_lane}")
    grouped_names: list[str] = []
    for lane, names in lanes.items():
        if not is_non_empty_string(lane):
            add_error(errors, path, "lane key must be a non-empty string")
        elif lane not in KNOWN_LANES:
            add_warning(warnings, f"{path}.{lane}", "accepted unknown lane")
        if not isinstance(names, list) or not all(isinstance(item, str) for item in names):
            add_error(errors, f"{path}.{lane}", "must be a list of strings")
            continue
        grouped_names.extend(names)
    if sorted(grouped_names) != sorted(step_names):
        add_error(errors, path, "lane step names must match report steps")


def validate_step(
    step: Any, index: int, errors: list[str], warnings: list[str], require_dry_run: bool
) -> str | None:
    """Validate one schema-v6 step payload."""
    path = f"steps[{index}]"
    if not isinstance(step, dict):
        add_error(errors, path, "must be an object")
        return None

    name = step.get("name")
    if not is_non_empty_string(name):
        add_error(errors, f"{path}.name", "must be a non-empty string")

    lane = step.get("lane")
    if not is_non_empty_string(lane):
        add_error(errors, f"{path}.lane", "must be a non-empty string")
    elif lane not in KNOWN_LANES:
        add_warning(warnings, f"{path}.lane", f"accepted unknown lane {lane!r}")

    if "purpose" in step and not isinstance(step.get("purpose"), str):
        add_error(errors, f"{path}.purpose", "must be string when present")
    command = step.get("command")
    if (
        not isinstance(command, list)
        or not command
        or not all(isinstance(item, str) for item in command)
    ):
        add_error(errors, f"{path}.command", "must be a non-empty list of strings")

    expected_outputs = step.get("expected_outputs")
    if expected_outputs is not None and not (
        isinstance(expected_outputs, list)
        and all(isinstance(item, str) for item in expected_outputs)
    ):
        add_error(errors, f"{path}.expected_outputs", "must be a list of strings when present")

    if not isinstance(step.get("dry_run"), bool):
        add_error(errors, f"{path}.dry_run", "must be bool")
    elif require_dry_run and step.get("dry_run") is not True:
        add_error(errors, f"{path}.dry_run", "must be true for dry-run report validation")

    if not isinstance(step.get("planned_only"), bool):
        add_error(errors, f"{path}.planned_only", "must be bool")
    elif require_dry_run and step.get("planned_only") is not True:
        add_error(errors, f"{path}.planned_only", "must be true for dry-run report validation")

    if not is_int(step.get("returncode")):
        add_error(errors, f"{path}.returncode", "must be int")
    if not is_non_negative_number(step.get("duration_sec")):
        add_error(errors, f"{path}.duration_sec", "must be int or float >= 0")
    if "pass_index" in step and not is_non_negative_int(step.get("pass_index")):
        add_error(errors, f"{path}.pass_index", "must be int >= 0")
    if "allow_failure" in step and not isinstance(step.get("allow_failure"), bool):
        add_error(errors, f"{path}.allow_failure", "must be bool when present")
    if "metadata" in step and not isinstance(step.get("metadata"), dict):
        add_error(errors, f"{path}.metadata", "must be object when present")
    if "ok" in step and not isinstance(step.get("ok"), bool):
        add_error(errors, f"{path}.ok", "must be bool when present")
    if "error" in step and step.get("error") is not None and not isinstance(step.get("error"), str):
        add_error(errors, f"{path}.error", "must be string or null when present")

    for stream_field in ("stdout", "stderr"):
        if stream_field in step and not isinstance(step.get(stream_field), str):
            add_error(errors, f"{path}.{stream_field}", "must be string")

    return str(name) if is_non_empty_string(name) else None
