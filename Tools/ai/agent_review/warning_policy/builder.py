from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from .common import (
    FINAL_KINDS,
    LEVELS,
    extract_next_layer,
    extract_reason,
    final_decision_recovered,
    infer_level,
    is_final_authoritative,
    load_report,
    now_iso,
    repo_rel,
    resolve_path,
)


def extract_existing_warnings(
    path: str, report: dict[str, Any], level: str
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    raw_warnings = report.get("warnings")
    if isinstance(raw_warnings, list):
        for index, item in enumerate(raw_warnings):
            result.append(
                {
                    "path": path,
                    "kind": report.get("kind"),
                    "level": level,
                    "severity": "warning",
                    "classification": "reported_warning",
                    "recoverable": True,
                    "message": str(item),
                    "index": index,
                }
            )
    elif isinstance(raw_warnings, dict) and raw_warnings:
        result.append(
            {
                "path": path,
                "kind": report.get("kind"),
                "level": level,
                "severity": "warning",
                "classification": "reported_warning",
                "recoverable": True,
                "message": str(raw_warnings)[:500],
                "index": 0,
            }
        )
    return result


def build_policy_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    ledger: list[dict[str, Any]] = []
    input_nonfatal: list[dict[str, Any]] = []
    fatal_failures: list[dict[str, Any]] = []

    decision_path, decision_report, decision_errors = load_report(
        repo_root, args.decision_report, missing_is_error=True
    )
    errors.extend(decision_errors)
    final_paths = {repo_rel(decision_path, repo_root)}
    for value in args.final_report:
        final_paths.add(repo_rel(resolve_path(repo_root, value), repo_root))

    recovered = final_decision_recovered(
        decision_report,
        min_recommendations=args.min_recommendations,
        min_patch_plans=args.min_patch_plans,
    )
    if not recovered:
        errors.append(
            "decision report did not recover workflow: expected passed=true, "
            "recommendation_count >= minimum, patch_plan_count >= minimum and guardrails false"
        )

    report_values = _report_values(args)
    seen_paths: set[str] = set()
    for value in report_values:
        _process_report_value(
            repo_root=repo_root,
            value=value,
            decision_path=decision_path,
            final_paths=final_paths,
            recovered=recovered,
            seen_paths=seen_paths,
            ledger=ledger,
            input_nonfatal=input_nonfatal,
            fatal_failures=fatal_failures,
        )

    if input_nonfatal:
        warnings.append(
            f"input_nonfatal_warnings present: {len(input_nonfatal)} diagnostic report(s) "
            "had passed=false but were recovered by the final decision layer"
        )
    if fatal_failures:
        errors.extend(
            f"{item['path']}: {item['classification']}: {item.get('reason', '')}"
            for item in fatal_failures
        )
    return _final_report(
        repo_root,
        decision_path,
        decision_report,
        recovered,
        errors,
        warnings,
        ledger,
        input_nonfatal,
        fatal_failures,
    )


def _report_values(args: argparse.Namespace) -> list[str]:
    report_values = list(args.report_file)
    for value in args.final_report:
        if value not in report_values:
            report_values.append(value)
    if args.decision_report not in report_values:
        report_values.append(args.decision_report)
    return report_values


def _process_report_value(
    *,
    repo_root: Path,
    value: str,
    decision_path: Path,
    final_paths: set[str],
    recovered: bool,
    seen_paths: set[str],
    ledger: list[dict[str, Any]],
    input_nonfatal: list[dict[str, Any]],
    fatal_failures: list[dict[str, Any]],
) -> None:
    path, report, load_errors = load_report(repo_root, value, missing_is_error=False)
    rel_path = repo_rel(path, repo_root)
    if rel_path in seen_paths:
        return
    seen_paths.add(rel_path)
    if load_errors:
        fatal_failures.extend(_load_error_entries(rel_path, load_errors))
        return
    if not report:
        return
    level = infer_level(rel_path, report)
    ledger.extend(extract_existing_warnings(rel_path, report, level))
    if report.get("passed") is False:
        entry = _failed_report_entry(repo_root, rel_path, report, level, final_paths, recovered, decision_path)
        if entry["classification"] == "input_nonfatal":
            input_nonfatal.append(entry)
        else:
            fatal_failures.append(entry)
        ledger.append(entry)


def _load_error_entries(rel_path: str, load_errors: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "path": rel_path,
            "kind": None,
            "level": "tool",
            "severity": "error",
            "classification": "missing_or_invalid_report",
            "recoverable": False,
            "reason": error,
        }
        for error in load_errors
    ]


def _failed_report_entry(
    repo_root: Path,
    rel_path: str,
    report: dict[str, Any],
    level: str,
    final_paths: set[str],
    recovered: bool,
    decision_path: Path,
) -> dict[str, Any]:
    recoverable = recovered and not is_final_authoritative(rel_path, report, final_paths)
    return {
        "path": rel_path,
        "kind": report.get("kind"),
        "level": level,
        "severity": "warning" if recoverable else "error",
        "classification": "input_nonfatal" if recoverable else "fatal_report_failure",
        "recoverable": recoverable,
        "reason": extract_reason(report),
        "recommended_next_layer": extract_next_layer(report),
        "recovered_by": repo_rel(decision_path, repo_root) if recovered else "",
    }


def _final_report(
    repo_root: Path,
    decision_path: Path,
    decision_report: dict[str, Any],
    recovered: bool,
    errors: list[str],
    warnings: list[str],
    ledger: list[dict[str, Any]],
    input_nonfatal: list[dict[str, Any]],
    fatal_failures: list[dict[str, Any]],
) -> dict[str, Any]:
    level_counts = Counter(str(item.get("level")) for item in ledger)
    classification_counts = Counter(str(item.get("classification")) for item in ledger)
    return {
        "schema_version": 1,
        "kind": "agent_review_warning_policy",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "decision_recovered": recovered,
        "decision_report": repo_rel(decision_path, repo_root),
        "recommendation_count": decision_report.get("recommendation_count"),
        "patch_plan_count": decision_report.get("patch_plan_count"),
        "warning_count": len(ledger),
        "input_nonfatal_warning_count": len(input_nonfatal),
        "fatal_report_failure_count": len(fatal_failures),
        "warning_level_counts": dict(sorted(level_counts.items())),
        "warning_classification_counts": dict(sorted(classification_counts.items())),
        "input_nonfatal_warnings": input_nonfatal,
        "fatal_report_failures": fatal_failures,
        "warning_ledger": ledger,
        "policy": {
            "scope": sorted(LEVELS),
            "final_authoritative_kinds": sorted(FINAL_KINDS),
            "input_nonfatal_condition": "final decision layer recovered into valid recommendations and patch plans under guardrails",
            "fatal_condition": "final authoritative report failed, required report is invalid, or guardrail was violated",
        },
        "guardrails": {
            "report_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
        },
    }
