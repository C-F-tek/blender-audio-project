#!/usr/bin/env python3
"""Validate the final unified launcher manifest schema.

This validator guards the large PowerShell wrapper while manifest construction is
still partly inline. It checks the fields that downstream AI-to-AI/tooling uses:
phase_status, phase_reports, report_files, context_files and unified-run identity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


REQUIRED_TOP_LEVEL = (
    "schema_version",
    "kind",
    "stamp",
    "mode_name",
    "phase_status",
    "phase_reports",
    "report_files",
    "context_files",
)

REQUIRED_UNIFIED_FIELDS = (
    "unified_run_operational_model",
    "unified_run_source_of_knowledge",
    "unified_run_final_product",
)

EXPECTED_UNIFIED_VALUES = {
    "unified_run_operational_model": "single_dynamic_heap_exchange_run",
    "unified_run_source_of_knowledge": "heap_exchange",
    "unified_run_final_product": "reviewable_pr_with_concrete_changes",
}


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "root is not a JSON object"
    return data, None


def is_rel_report_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or ":" in normalized[:4]:
        return False
    if normalized.startswith(".git/"):
        return False
    return True


def validate_manifest(manifest: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in manifest:
            errors.append(f"missing top-level field: {key}")

    for key in REQUIRED_UNIFIED_FIELDS:
        if key not in manifest:
            errors.append(f"missing unified-run field: {key}")
        elif manifest.get(key) != EXPECTED_UNIFIED_VALUES[key]:
            errors.append(
                f"{key} must be {EXPECTED_UNIFIED_VALUES[key]!r}, got {manifest.get(key)!r}"
            )

    phase_status = manifest.get("phase_status")
    phase_reports = manifest.get("phase_reports")
    report_files = manifest.get("report_files")
    context_files = manifest.get("context_files")

    if not isinstance(phase_status, dict):
        errors.append("phase_status must be an object")
    if not isinstance(phase_reports, dict):
        errors.append("phase_reports must be an object")
    if not isinstance(report_files, list):
        errors.append("report_files must be a list")
    if not isinstance(context_files, list):
        errors.append("context_files must be a list")

    if isinstance(phase_status, dict):
        for key, value in phase_status.items():
            if not isinstance(key, str) or not key:
                errors.append("phase_status keys must be non-empty strings")
            if not isinstance(value, bool):
                warnings.append(f"phase_status.{key} is not boolean: {type(value).__name__}")

    if isinstance(phase_reports, dict):
        for key, value in phase_reports.items():
            if not isinstance(key, str) or not key:
                errors.append("phase_reports keys must be non-empty strings")
            if isinstance(value, str):
                if value and not is_rel_report_path(value):
                    errors.append(f"phase_reports.{key} must be repo-relative path: {value}")
            elif isinstance(value, list):
                for item in value:
                    if not is_rel_report_path(item):
                        errors.append(f"phase_reports.{key} contains invalid path: {item}")
            elif value is not None:
                errors.append(
                    f"phase_reports.{key} must be string/list/null, got {type(value).__name__}"
                )

    if isinstance(report_files, list):
        seen = set()
        for item in report_files:
            if not is_rel_report_path(item):
                errors.append(f"report_files contains invalid path: {item}")
            if item in seen:
                warnings.append(f"duplicate report_files entry: {item}")
            seen.add(item)

    if isinstance(context_files, list):
        seen = set()
        for item in context_files:
            if not is_rel_report_path(item):
                errors.append(f"context_files contains invalid path: {item}")
            if item in seen:
                warnings.append(f"duplicate context_files entry: {item}")
            seen.add(item)

    runtime_correlation_requested = manifest.get("runtime_evidence_correlation_requested")
    if runtime_correlation_requested not in {True, False, None}:
        errors.append("runtime_evidence_correlation_requested must be boolean/null")

    if runtime_correlation_requested is True:
        if not isinstance(phase_reports, dict):
            errors.append("runtime evidence correlation requires phase_reports object")
        elif not phase_reports.get("runtime_evidence_correlation"):
            errors.append(
                "runtime evidence correlation requested but phase_reports.runtime_evidence_correlation is missing"
            )

        if not isinstance(report_files, list):
            errors.append("runtime evidence correlation requires report_files list")
        else:
            has_runtime_correlation_report = any(
                isinstance(item, str)
                and "runtime_evidence_correlation" in item.replace("\\", "/")
                and item.replace("\\", "/").endswith(".json")
                for item in report_files
            )
            if not has_runtime_correlation_report:
                errors.append(
                    "runtime evidence correlation requested but report_files does not include runtime_evidence_correlation JSON"
                )

        if not isinstance(context_files, list):
            errors.append("runtime evidence correlation requires context_files list")
        else:
            has_runtime_correlation_context = any(
                isinstance(item, str)
                and "runtime_evidence_correlation" in item.replace("\\", "/")
                and item.replace("\\", "/").endswith(".md")
                for item in context_files
            )
            if not has_runtime_correlation_context:
                warnings.append(
                    "runtime evidence correlation requested but context_files does not include runtime_evidence_correlation Markdown"
                )

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", default="output/validation/unified_run_manifest_schema.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo_root).resolve()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = repo / manifest_path

    manifest, load_error = load_json(manifest_path)
    errors: list[str] = []
    warnings: list[str] = []

    if load_error:
        errors.append(f"manifest load failed: {load_error}")
        manifest = {}
    else:
        validation_errors, validation_warnings = validate_manifest(manifest or {})
        errors.extend(validation_errors)
        warnings.extend(validation_warnings)

    report = {
        "schema_version": 1,
        "kind": "unified_run_manifest_schema_validation",
        "repo_root": repo.as_posix(),
        "manifest": str(manifest_path),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": warnings,
    }

    output = resolve_output_path(repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
