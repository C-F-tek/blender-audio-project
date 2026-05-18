"""Report assembly for refactor duplication audits."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

from .candidates import (
    build_exact_name_candidates,
    build_manual_review_patch_plan_candidates,
    build_rule_candidates,
    dedupe_candidates,
)
from .common import DEFAULT_ROOTS, now_stamp, split_values
from .reports import (
    collect_report_status,
    merge_existing_audit_candidates,
    summarize_existing_audit_reports,
    verify_layering,
)
from .scanner import collect_functions, iter_python_files

def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or now_stamp()
    roots = split_values(args.root) or list(DEFAULT_ROOTS)
    reports_raw = split_values(args.report)
    reports_raw.extend(split_values(args.line_count_report))
    reports_raw.extend(split_values(args.code_interpreter_report))
    reports_raw.extend(split_values(args.python_syntax_report))
    reports_raw.extend(split_values(args.bundle_smoke_report))
    reports_raw.extend(split_values(args.memory_routing_report))
    report_paths = []
    for value in reports_raw:
        if value not in report_paths:
            report_paths.append(value)
    input_audit_paths = split_values(args.input_audit_report)
    existing_audit_summary = summarize_existing_audit_reports(repo_root, input_audit_paths)

    files = iter_python_files(repo_root, roots)
    functions, parse_warnings = collect_functions(repo_root, files)
    candidates = dedupe_candidates(
        build_rule_candidates(functions)
        + build_exact_name_candidates(functions)
        + merge_existing_audit_candidates(repo_root, input_audit_paths)
    )
    candidates = candidates[: max(1, args.max_candidates)]
    refactor_verification = verify_layering(repo_root)
    report_status, report_warnings = collect_report_status(repo_root, report_paths)

    advisory = [
        "Do not apply refactors automatically from this report; generate a focused manual-review patch plan first.",
        "Keep provider/orchestrator request-packet refactors advisory-only until schema stability is proven by broker/orchestrator smoke tests.",
    ]
    if any(item.get("candidate_id") == "dup_markdown_renderers" for item in candidates):
        advisory.append(
            "Markdown rendering duplication is mostly presentation-layer and should remain local unless a stable shared status-section helper emerges."
        )

    source_failed = [item for item in report_status if item.get("passed") is False]
    errors = [f"source report failed: {item.get('path')}" for item in source_failed]
    warnings = parse_warnings + report_warnings
    if not candidates:
        warnings.append(
            "No duplication candidates detected; verify roots and patterns before treating this as complete."
        )

    generated_patch_plan_candidates = build_manual_review_patch_plan_candidates(candidates)
    imported_patch_plan_candidates = list(
        existing_audit_summary.get("manual_review_patch_plan_candidates") or []
    )
    manual_review_patch_plan_candidates = (
        generated_patch_plan_candidates + imported_patch_plan_candidates
    )
    helper_reuse_recommendations = [
        "Reuse Tools.ai._shared.github_evidence_bundle_io for evidence-bundle path/text/JSON helpers when semantics match.",
        "Reuse Tools.ai._shared.github_evidence_bundle_artifacts for artifact discovery and chunk pointer metadata.",
        "Reuse Tools.validation._shared.report_utils for validation output path resolution and JSON report writing.",
        "Prefer promoting existing local functions into existing helper modules over creating new generic helper modules.",
    ]
    for item in existing_audit_summary.get("helper_reuse_recommendations") or []:
        if item not in helper_reuse_recommendations:
            helper_reuse_recommendations.append(item)
    advisory_only_findings = list(advisory)
    for item in existing_audit_summary.get("advisory_only_findings") or []:
        if item not in advisory_only_findings:
            advisory_only_findings.append(item)

    report = {
        "schema_version": 1,
        "kind": "refactor_duplication_audit",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stamp": stamp,
        "repo_root": str(repo_root),
        "roots": roots,
        "passed": not errors and bool(refactor_verification.get("passed")),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "blender_runtime_execution_performed": False,
        "python_file_count": len(files),
        "function_count": len(functions),
        "duplication_candidate_count": len(candidates),
        "refactor_verification": refactor_verification,
        "duplication_candidates": candidates,
        "helper_reuse_recommendations": helper_reuse_recommendations,
        "manual_review_patch_plan_candidates": manual_review_patch_plan_candidates,
        "advisory_only_findings": advisory_only_findings,
        "input_audit_reports": existing_audit_summary.get("reports", []),
        "source_reports": report_status,
        "validation_commands": [
            "python -m py_compile tools/ai/refactor_duplication_audit/cli.py -m Tools.validation run_refactor_duplication_audit_smoke",
            "python -m Tools.ai refactor_duplication_audit --help",
            "python -m Tools.validation run_refactor_duplication_audit_smoke --repo-root .",
            "python -m Tools.validation.check_python_syntax --repo-root .",
            "python -m Tools.validation run_agent_runtime_tool_broker_smoke --repo-root .",
        ],
        "stop_conditions": [
            "Stop if python syntax validation fails.",
            "Stop if patch_application_performed=True.",
            "Stop if sqlite_write_performed=True or persistent_memory_write_performed=True.",
            "Stop if a ready refactor would break CLI/report schema without a migration plan.",
        ],
        "errors": errors,
        "warnings": warnings,
        "guardrails": {
            "report_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "manual_review_required": True,
        },
    }
    return report
