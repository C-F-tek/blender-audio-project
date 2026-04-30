#!/usr/bin/env python3
"""Validate Git-trackable GitHub evidence bundle contracts.

The check is intentionally report-only: it reads compact evidence bundles under
docs/LOCAL_VALIDATION_EVIDENCE, writes an optional validation report, and never
executes local AI providers or rewrites source evidence artifacts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:  # Allows package-style imports during external checks.
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


EXPECTED_KIND = "github_validation_evidence_bundle"
EXPECTED_SCHEMA_VERSION = 1

REQUIRED_DECISION_FIELDS = (
    "ollama_gpu_primary_advisory",
    "npu_excluded_when_unusable",
    "provider_execution_seen",
)

OPTIONAL_PROVIDER_DECISION_FIELDS = (
    "npu_decode_smoke_passed",
)

REQUIRED_REPORT_FIELDS = (
    "path",
    "exists",
    "json_ok",
    "kind",
    "passed",
    "summary",
)

OPTIONAL_SUMMARY_HINT_FIELDS_BY_KIND = {
    "ai_workload_report_quality": ("provider_execution_performed",),
    "ai_workload_quality_lane_routing": (
        "provider_execution_performed",
        "policy",
        "mode",
        "primary_advisory_provider",
        "routing",
    ),
    "npu_decode_quality_remediation": (
        "provider_execution_performed",
        "policy",
        "mode",
        "checks",
    ),
    "npu_decode_smoke_diagnostic": (
        "provider_execution_performed",
        "policy",
        "mode",
        "provider",
        "checks",
    ),
    "local_provider_probe": ("provider_execution_performed",),
    "npu_runtime_output_manifest": ("provider_execution_performed", "mode"),
    "provider_result_report": ("provider_execution_performed", "mode", "provider"),
}


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def default_bundle_paths(repo_root: Path) -> list[Path]:
    evidence_dir = repo_root / "docs" / "LOCAL_VALIDATION_EVIDENCE"
    return sorted(evidence_dir.glob("*.json"))


def split_path_values(items: list[str]) -> list[str]:
    values: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                values.append(normalized)
    return values


def read_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
    except OSError as exc:
        return None, str(exc)
    if not isinstance(data, dict):
        return None, f"expected a JSON object, got {type(data).__name__}"
    return data, None


def validate_decision(decision: Any) -> tuple[dict[str, bool], list[str], list[str]]:
    checks: dict[str, bool] = {}
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(decision, dict):
        return checks, ["decision must be an object"], warnings

    for field in REQUIRED_DECISION_FIELDS:
        checks[field] = field in decision
        if field not in decision:
            errors.append(f"decision missing required field: {field}")
        elif not isinstance(decision[field], bool):
            errors.append(f"decision.{field} must be a boolean")

    for field in OPTIONAL_PROVIDER_DECISION_FIELDS:
        checks[field] = field in decision
        if field not in decision:
            warnings.append(f"decision missing optional provider field: {field}")
        elif not isinstance(decision[field], bool):
            warnings.append(f"decision.{field} should be a boolean")

    return checks, errors, warnings


def validate_report_entry(entry: Any, index: int) -> dict[str, Any]:
    label = f"reports[{index}]"
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(entry, dict):
        return {
            "index": index,
            "path": label,
            "kind": None,
            "ok": False,
            "errors": [f"{label} must be an object"],
            "warnings": warnings,
            "summary_keys": [],
        }

    path = str(entry.get("path") or label)
    missing = [field for field in REQUIRED_REPORT_FIELDS if field not in entry]
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    summary = entry.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary must be an object")
        summary_keys: list[str] = []
    else:
        summary_keys = sorted(str(key) for key in summary.keys())
        if entry.get("kind") != summary.get("kind"):
            warnings.append("entry kind differs from summary.kind")
        if entry.get("passed") != summary.get("passed"):
            warnings.append("entry passed differs from summary.passed")
        for field in OPTIONAL_SUMMARY_HINT_FIELDS_BY_KIND.get(str(entry.get("kind")), ()):
            if field not in summary:
                warnings.append(f"provider-related summary missing optional field: {field}")

    if "exists" in entry and not isinstance(entry.get("exists"), bool):
        errors.append("exists must be a boolean")
    if "json_ok" in entry and not isinstance(entry.get("json_ok"), bool):
        errors.append("json_ok must be a boolean")
    if "passed" in entry and entry.get("passed") is not None and not isinstance(entry.get("passed"), bool):
        errors.append("passed must be a boolean or null")

    return {
        "index": index,
        "path": path,
        "kind": entry.get("kind"),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "summary_keys": summary_keys,
    }


def validate_bundle(path: Path, repo_root: Path) -> dict[str, Any]:
    rel_path = repo_relative(path, repo_root)
    errors: list[str] = []
    warnings: list[str] = []

    if not path.exists():
        return {
            "path": rel_path,
            "exists": False,
            "json_ok": False,
            "ok": False,
            "kind": None,
            "schema_version": None,
            "report_count": 0,
            "decision_checks": {},
            "report_checks": [],
            "errors": ["evidence bundle is missing"],
            "warnings": warnings,
        }

    data, parse_error = read_json_object(path)
    if parse_error or data is None:
        return {
            "path": rel_path,
            "exists": True,
            "json_ok": False,
            "ok": False,
            "kind": None,
            "schema_version": None,
            "report_count": 0,
            "decision_checks": {},
            "report_checks": [],
            "errors": [parse_error or "unknown JSON parse error"],
            "warnings": warnings,
        }

    kind = data.get("kind")
    schema_version = data.get("schema_version")
    if kind != EXPECTED_KIND:
        errors.append(f"kind must be {EXPECTED_KIND!r}")
    if schema_version != EXPECTED_SCHEMA_VERSION:
        errors.append(f"schema_version must be {EXPECTED_SCHEMA_VERSION}")

    source_reports = data.get("source_reports")
    if not isinstance(source_reports, list):
        warnings.append("source_reports should be a list")

    decision_checks, decision_errors, decision_warnings = validate_decision(data.get("decision"))
    errors.extend(decision_errors)
    warnings.extend(decision_warnings)

    raw_reports = data.get("reports")
    if not isinstance(raw_reports, list):
        errors.append("reports must be a list")
        report_checks: list[dict[str, Any]] = []
    else:
        report_checks = [validate_report_entry(entry, index) for index, entry in enumerate(raw_reports)]
        for check in report_checks:
            for error in check.get("errors", []):
                errors.append(f"{check.get('path')}: {error}")
            for warning in check.get("warnings", []):
                warnings.append(f"{check.get('path')}: {warning}")

    return {
        "path": rel_path,
        "exists": True,
        "json_ok": True,
        "ok": not errors,
        "kind": kind,
        "schema_version": schema_version,
        "report_count": len(raw_reports) if isinstance(raw_reports, list) else 0,
        "decision_checks": decision_checks,
        "report_checks": report_checks,
        "errors": errors,
        "warnings": warnings,
    }


def validate_github_evidence_bundles(repo_root: Path, paths: list[Path]) -> dict[str, Any]:
    results = [validate_bundle(path, repo_root) for path in paths]
    errors = [
        f"{item['path']}: {error}"
        for item in results
        for error in item.get("errors", [])
    ]
    warnings = [
        f"{item['path']}: {warning}"
        for item in results
        for warning in item.get("warnings", [])
    ]
    if not results:
        errors.append("no evidence bundle JSON files found")

    return {
        "schema_version": 1,
        "kind": "github_evidence_bundle_validation",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "bundle_count": len(results),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--bundle", action="append", default=[], help="Bundle JSON path. Repeatable or comma-separated.")
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    raw_bundles = split_path_values(list(args.bundle or []))
    if raw_bundles:
        paths = [
            Path(item).resolve() if Path(item).is_absolute() else (repo_root / item).resolve()
            for item in raw_bundles
        ]
    else:
        paths = default_bundle_paths(repo_root)

    report = validate_github_evidence_bundles(repo_root, paths)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    text = write_json_report(report, output)
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
