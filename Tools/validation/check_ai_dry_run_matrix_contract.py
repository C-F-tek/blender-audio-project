#!/usr/bin/env python3
"""Validate the AI dry-run matrix report contract without executing the matrix.

This validator reads the report produced by:

    Tools/ai/run_pipeline_dry_run_matrix.py

It checks only the machine-readable report shape and minimal stable fields.
It does not run Blender, FFmpeg, NPU/GPU workloads or the dry-run matrix itself.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def is_non_empty_string(value: Any) -> bool:
    """Return True when value is a non-empty string after trimming whitespace."""
    return isinstance(value, str) and bool(value.strip())


def is_number(value: Any) -> bool:
    """Return True for numeric values while excluding booleans."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def add_error(errors: list[str], path: str, message: str) -> None:
    """Append a path-qualified validation error."""
    errors.append(f"{path}: {message}")


def validate_agent_state_packet(packet: Any, path: str, errors: list[str], warnings: list[str]) -> None:
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
        if "repo_relative_path" in packet and not is_non_empty_string(packet.get("repo_relative_path")):
            add_error(errors, f"{path}.repo_relative_path", "must be a non-empty string when present")
    elif enabled is False:
        if exists is not False:
            add_error(errors, f"{path}.exists", "must be false when enabled=false")
        if source != "disabled":
            add_error(errors, f"{path}.source", 'must be "disabled" when enabled=false')
        if packet_path is not None and not is_non_empty_string(packet_path):
            add_error(errors, f"{path}.path", "must be null/absent or a non-empty string")

    extra_fields = sorted(set(packet) - {"enabled", "path", "exists", "source", "repo_relative_path"})
    if extra_fields:
        warnings.append(f"{path}: accepted extra fields: {', '.join(extra_fields)}")


def validate_result(result: Any, index: int, errors: list[str], warnings: list[str]) -> str | None:
    """Validate one dry-run matrix result item."""
    path = f"results[{index}]"
    if not isinstance(result, dict):
        add_error(errors, path, "must be an object")
        return None

    name = result.get("name")
    if not is_non_empty_string(name):
        add_error(errors, f"{path}.name", "must be a non-empty string")

    if not is_non_empty_string(result.get("purpose")):
        add_error(errors, f"{path}.purpose", "must be a non-empty string")

    command = result.get("command")
    if not isinstance(command, list) or not command:
        add_error(errors, f"{path}.command", "must be a non-empty list")

    if not isinstance(result.get("returncode"), int) or isinstance(result.get("returncode"), bool):
        add_error(errors, f"{path}.returncode", "must be int")

    if not is_number(result.get("duration_sec")):
        add_error(errors, f"{path}.duration_sec", "must be int or float")

    for optional_tail in ("stdout_tail", "stderr_tail"):
        if optional_tail in result and result.get(optional_tail) is not None and not isinstance(result.get(optional_tail), str):
            add_error(errors, f"{path}.{optional_tail}", "must be string when present")

    report_exists = result.get("report_exists")
    if not isinstance(report_exists, bool):
        add_error(errors, f"{path}.report_exists", "must be bool")

    report_path = result.get("report_path")
    if report_exists is True and not is_non_empty_string(report_path):
        add_error(errors, f"{path}.report_path", "must be non-empty when report_exists=true")
    elif report_path is not None and not isinstance(report_path, str):
        add_error(errors, f"{path}.report_path", "must be string when present")

    report_passed = result.get("report_passed")
    if report_passed is not None and not isinstance(report_passed, bool):
        add_error(errors, f"{path}.report_passed", "must be bool or null")

    step_count = result.get("step_count")
    if step_count is not None:
        if not isinstance(step_count, int) or isinstance(step_count, bool) or step_count < 0:
            add_error(errors, f"{path}.step_count", "must be int >= 0 or null")

    for object_or_null in ("lanes", "summary", "schedule"):
        value = result.get(object_or_null)
        if value is not None and not isinstance(value, dict):
            add_error(errors, f"{path}.{object_or_null}", "must be object or null")

    if "agent_state_packet" in result and result.get("agent_state_packet") is not None:
        validate_agent_state_packet(result.get("agent_state_packet"), f"{path}.agent_state_packet", errors, warnings)

    return str(name) if is_non_empty_string(name) else None


def validate_matrix_report(repo_root: Path, matrix_report: Path) -> dict[str, Any]:
    """Validate the dry-run matrix report JSON file."""
    errors: list[str] = []
    warnings: list[str] = []
    names: list[str] = []
    payload: dict[str, Any] | None = None

    matrix_report_exists = matrix_report.exists()
    if not matrix_report_exists:
        errors.append(f"Matrix report not found: {matrix_report}")
    else:
        try:
            raw = json.loads(matrix_report.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                payload = raw
            else:
                errors.append("matrix report root must be an object")
        except Exception as exc:
            errors.append(f"Matrix report parse failed: {type(exc).__name__}: {exc}")

    if payload is not None:
        if "schema_version" not in payload:
            add_error(errors, "schema_version", "is missing")
        elif not isinstance(payload.get("schema_version"), int) or isinstance(payload.get("schema_version"), bool):
            add_error(errors, "schema_version", "must be int")

        if not is_non_empty_string(payload.get("repo_root")):
            add_error(errors, "repo_root", "must be a non-empty string")

        if not is_non_empty_string(payload.get("output_dir")):
            add_error(errors, "output_dir", "must be a non-empty string")

        if not isinstance(payload.get("passed"), bool):
            add_error(errors, "passed", "must be bool")

        results = payload.get("results")
        if not isinstance(results, list):
            add_error(errors, "results", "must be a list")
            result_count = 0
        else:
            result_count = len(results)
            if not results:
                add_error(errors, "results", "must not be empty")
            for index, result in enumerate(results):
                name = validate_result(result, index, errors, warnings)
                if name is not None:
                    names.append(name)

        case_count = payload.get("case_count")
        if not isinstance(case_count, int) or isinstance(case_count, bool):
            add_error(errors, "case_count", "must be int")
        elif isinstance(results, list) and case_count != len(results):
            add_error(errors, "case_count", f"must equal len(results), got {case_count} != {len(results)}")
    else:
        result_count = 0
        case_count = None

    checks = {
        "case_count": payload.get("case_count") if payload else None,
        "result_count": result_count,
        "passed": payload.get("passed") if payload else None,
        "names": names,
    }

    return {
        "schema_version": 1,
        "repo_root": str(repo_root),
        "matrix_report": str(matrix_report),
        "matrix_report_exists": matrix_report_exists,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--matrix-report",
        default="output/ai_pipeline/dry_run_matrix_report.json",
        help="Path to the dry-run matrix JSON report, relative to --repo-root unless absolute.",
    )
    parser.add_argument("--output", help="Optional JSON validation report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    matrix_report = Path(args.matrix_report)
    if not matrix_report.is_absolute():
        matrix_report = repo_root / matrix_report
    matrix_report = matrix_report.resolve()

    report = validate_matrix_report(repo_root, matrix_report)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output = output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")

    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
