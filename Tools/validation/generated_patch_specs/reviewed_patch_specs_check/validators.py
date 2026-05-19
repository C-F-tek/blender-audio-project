"""Reviewed patch-spec manifest and spec validators."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import normalize_repo_path, read_json_object, repo_relative, resolve_repo_path
from .constants import (
    EXPECTED_APPLY_MODE,
    EXPECTED_MANIFEST_KIND,
    EXPECTED_REVIEW_STATUS,
    EXPECTED_SPEC_KIND,
    REQUIRED_MANIFEST_FIELDS,
    REQUIRED_SPEC_FIELDS,
)
from .dry_run import dry_run_spec
from .path_validation import replacement_errors, target_path_errors, validation_command_errors

def validate_operation(operation: Any, index: int, repo_root: Path) -> dict[str, Any]:
    label = f"operations[{index}]"
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(operation, dict):
        return {
            "label": label,
            "ok": False,
            "errors": [f"{label} must be an object"],
            "warnings": warnings,
        }

    path = normalize_repo_path(operation.get("path"))
    errors.extend(target_path_errors(path, repo_root))
    replacements = operation.get("replacements")
    if not isinstance(replacements, list) or not replacements:
        errors.append("replacements must be a non-empty list")
    else:
        for repl_index, replacement in enumerate(replacements):
            for error in replacement_errors(replacement):
                errors.append(f"replacements[{repl_index}]: {error}")
    if operation.get("review_status") not in {None, EXPECTED_REVIEW_STATUS}:
        errors.append(f"review_status must be {EXPECTED_REVIEW_STATUS} when present")

    return {
        "label": label,
        "path": path,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "replacement_count": len(replacements) if isinstance(replacements, list) else 0,
    }


def validate_spec(path: Path, repo_root: Path) -> dict[str, Any]:
    rel_path = repo_relative(path, repo_root)
    errors: list[str] = []
    warnings: list[str] = []
    if rel_path.startswith("patch_specs/inbox/"):
        errors.append("reviewed spec is in the GitHub Action inbox queue")

    data, parse_error = read_json_object(path)
    if parse_error or data is None:
        return {
            "path": rel_path,
            "exists": path.exists(),
            "json_ok": False,
            "ok": False,
            "errors": errors + [parse_error or "unknown JSON parse error"],
            "warnings": warnings,
            "operation_count": 0,
            "operation_checks": [],
            "dry_run": {
                "passed": False,
                "error": parse_error or "unknown JSON parse error",
                "reports": [],
            },
        }

    missing = [field for field in REQUIRED_SPEC_FIELDS if field not in data]
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if data.get("kind") != EXPECTED_SPEC_KIND:
        errors.append(f"kind must be {EXPECTED_SPEC_KIND}")
    if int(data.get("version", 0) or 0) != 1:
        errors.append("version must be 1")
    if data.get("apply_mode") != EXPECTED_APPLY_MODE:
        errors.append("apply_mode must be manual_review_only")
    if data.get("review_status") != EXPECTED_REVIEW_STATUS:
        errors.append(f"review_status must be {EXPECTED_REVIEW_STATUS}")
    if data.get("provider_execution_performed") is not False:
        errors.append("provider_execution_performed must be false")

    operations = data.get("operations")
    if not isinstance(operations, list) or not operations:
        errors.append("operations must be a non-empty list")
        operation_checks: list[dict[str, Any]] = []
    else:
        operation_checks = [
            validate_operation(operation, index, repo_root)
            for index, operation in enumerate(operations)
        ]
        for check in operation_checks:
            for error in check.get("errors", []):
                errors.append(f"{check.get('label')}: {error}")
            for warning in check.get("warnings", []):
                warnings.append(f"{check.get('label')}: {warning}")

    for command in data.get("validation_commands") or []:
        errors.extend(validation_command_errors(command))

    recorded_dry_run = data.get("dry_run")
    if not isinstance(recorded_dry_run, dict) or recorded_dry_run.get("passed") is not True:
        errors.append("recorded dry_run.passed must be true")

    dry_run_passed = False
    dry_run_reports: list[dict[str, Any]] = []
    dry_run_error = ""
    if not errors:
        dry_run_passed, dry_run_reports, dry_run_error = dry_run_spec(repo_root, data)
        if not dry_run_passed:
            errors.append(f"dry-run failed: {dry_run_error}")
        elif not any(item.get("changed") for item in dry_run_reports):
            errors.append("dry-run passed but no target would change")

    return {
        "path": rel_path,
        "exists": True,
        "json_ok": True,
        "kind": data.get("kind"),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "operation_count": len(operations) if isinstance(operations, list) else 0,
        "operation_checks": operation_checks,
        "dry_run": {
            "passed": dry_run_passed and not errors,
            "error": dry_run_error,
            "reports": dry_run_reports,
        },
    }


def validate_manifest(path: Path, repo_root: Path) -> dict[str, Any]:
    rel_path = repo_relative(path, repo_root)
    errors: list[str] = []
    warnings: list[str] = []
    data, parse_error = read_json_object(path)
    if parse_error or data is None:
        return {
            "path": rel_path,
            "exists": path.exists(),
            "json_ok": False,
            "ok": False,
            "errors": [parse_error or "unknown JSON parse error"],
            "warnings": warnings,
            "spec_paths": [],
        }

    missing = [field for field in REQUIRED_MANIFEST_FIELDS if field not in data]
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if data.get("kind") != EXPECTED_MANIFEST_KIND:
        errors.append(f"kind must be {EXPECTED_MANIFEST_KIND}")
    if data.get("provider_execution_performed") is not False:
        errors.append("provider_execution_performed must be false")
    if data.get("apply_mode") != EXPECTED_APPLY_MODE:
        errors.append("apply_mode must be manual_review_only")
    if data.get("review_status") != EXPECTED_REVIEW_STATUS:
        errors.append(f"review_status must be {EXPECTED_REVIEW_STATUS}")

    specs = data.get("specs")
    spec_paths: list[str] = []
    if not isinstance(specs, list) or not specs:
        errors.append("specs must be a non-empty list")
    else:
        for item in specs:
            if not isinstance(item, dict):
                errors.append("spec manifest entries must be objects")
                continue
            spec_path = normalize_repo_path(item.get("path"))
            if not spec_path:
                errors.append("spec manifest entry path is required")
                continue
            if spec_path.startswith("patch_specs/inbox/"):
                errors.append(f"manifest points to queued inbox spec: {spec_path}")
            spec_paths.append(spec_path)
    if isinstance(data.get("reviewed_spec_count"), int) and len(spec_paths) != data.get(
        "reviewed_spec_count"
    ):
        errors.append("reviewed_spec_count does not match specs length")

    return {
        "path": rel_path,
        "exists": True,
        "json_ok": True,
        "kind": data.get("kind"),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "spec_paths": spec_paths,
    }


def validate_reviewed_patch_specs(
    repo_root: Path, manifest_paths: list[Path], spec_paths: list[Path]
) -> dict[str, Any]:
    manifest_checks = [validate_manifest(path, repo_root) for path in manifest_paths]
    paths_from_manifests = [
        resolve_repo_path(repo_root, spec_path)
        for manifest in manifest_checks
        for spec_path in manifest.get("spec_paths", [])
    ]
    all_spec_paths = list(dict.fromkeys([*paths_from_manifests, *spec_paths]))
    spec_checks = [validate_spec(path, repo_root) for path in all_spec_paths]

    errors = [
        f"{item['path']}: {error}"
        for item in [*manifest_checks, *spec_checks]
        for error in item.get("errors", [])
    ]
    warnings = [
        f"{item['path']}: {warning}"
        for item in [*manifest_checks, *spec_checks]
        for warning in item.get("warnings", [])
    ]
    if not manifest_checks and not spec_checks:
        errors.append("no manifests or specs were provided")

    return {
        "schema_version": 1,
        "kind": "reviewed_patch_spec_contract",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "manifest_count": len(manifest_checks),
        "spec_count": len(spec_checks),
        "manifest_checks": manifest_checks,
        "spec_checks": spec_checks,
    }
