from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from Tools.ai.patch_notes_quality_product.scoring import (
    build_patch_notes,
    build_product_sufficiency,
    classify,
    patch_notes_applicability,
    patch_plan_summary,
    score_product,
)
from Tools.ai.patch_notes_quality_product.task_md import (
    build_request_summary,
    load_task_markdown,
)
from Tools.ai.patch_notes_quality_product.telemetry_quality import (
    build_evidence_coverage,
    build_fallback_cases,
    build_success_cases,
    build_telemetry_quality,
)
from Tools.ai.patch_plan_quality_product.io_utils import (
    flatten_json,
    now_iso,
    read_json,
    repo_rel,
    resolve,
)
from Tools.ai.patch_plan_quality_product.token_search import (
    build_search_index,
    safe_tokens,
    search_docs,
)

OPTIONAL_INPUTS = {
    "patch_quality": "patch_quality",
    "decision_loop": "decision_loop",
    "runtime_usage": "runtime_usage",
    "runtime_capability": "runtime_capability",
    "repository_consistency": "repository_consistency",
    "memory_bundle": "memory_bundle",
    "full_toolbox_telemetry": "full_toolbox_telemetry",
    "github_evidence_bundle": "github_evidence_bundle",
}


def input_paths_from_args(args: Any, repo_root: Path) -> dict[str, Path]:
    paths = {"patch_plan": resolve(repo_root, args.patch_plan)}
    for key, attr in OPTIONAL_INPUTS.items():
        value = getattr(args, attr, "")
        if value:
            paths[key] = resolve(repo_root, value)
    return paths


def load_json_inputs(
    input_paths: dict[str, Path],
) -> tuple[dict[str, dict[str, Any]], dict[str, str], list[str], list[str]]:
    loaded: dict[str, dict[str, Any]] = {}
    status: dict[str, str] = {}
    errors: list[str] = []
    warnings: list[str] = []
    for key, path in input_paths.items():
        data, error = read_json(path)
        loaded[key] = data
        status[key] = error or "ok"
        if key == "patch_plan" and error:
            errors.append(f"{key}: {error} ({path})")
        elif error and error != "not_provided":
            warnings.append(f"{key}: {error} ({path})")
    return loaded, status, errors, warnings


def build_search_quality(
    repo_root: Path,
    db_path: Path,
    input_paths: dict[str, Path],
    loaded: dict[str, dict[str, Any]],
    request: str,
    extra_context: list[str],
) -> dict[str, Any]:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        fts_enabled, indexed = build_search_index(
            conn, repo_root, input_paths, loaded, request, extra_context
        )
        query_results = []
        terms = safe_tokens(
            request + " " + flatten_json(loaded.get("patch_plan", {}), limit=120_000),
            max_terms=14,
        )
        for term in terms[:8]:
            hits = search_docs(conn, fts_enabled, term, 6)
            query_results.append({"query": term, "hit_count": len(hits), "hits": hits[:3]})
    return {
        "sqlite_fts5_enabled": fts_enabled,
        "sqlite_fts_db": repo_rel(db_path, repo_root),
        "indexed_document_count": indexed,
        "fts_query_count": len(query_results),
        "fts_total_hit_count": sum(item["hit_count"] for item in query_results),
        "query_results": query_results,
    }


def build_report(args: Any) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    task, task_warnings = load_task_markdown(repo_root, args.task_markdown)
    input_paths = input_paths_from_args(args, repo_root)
    loaded, status, errors, warnings = load_json_inputs(input_paths)
    warnings.extend(task_warnings)
    if task_warnings:
        errors.append(task_warnings[0])
    request_summary = build_request_summary(task, args.branch, args.commit, args.issue)
    normalized_objective = str(task.get("objective_hint") or args.request or "").strip()
    patch_summary = patch_plan_summary(
        loaded.get("patch_plan", {}), loaded.get("patch_quality", {})
    )
    patch_note_limit = max(1, int(getattr(args, "max_patch_notes", 20) or 20))
    requested_min_patch_notes = max(0, int(getattr(args, "min_patch_notes", 0) or 0))
    patch_notes = build_patch_notes(
        loaded.get("patch_plan", {}),
        loaded.get("patch_quality", {}),
        limit=patch_note_limit,
    )
    validation_commands = patch_summary.get("validation_commands") or [
        "python -m py_compile tools/ai/build_patch_notes_quality_product.py",
        "python -m Tools.validation patch_notes_quality_product_smoke --repo-root .",
        "git diff --check",
    ]
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "patch_notes_quality_product",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "stamp": args.stamp,
        "passed": True,
        "quality_gate_passed": False,
        "classification": "completed_with_patch_notes_fallback",
        "non_blocking": not args.strict_patch_notes_quality_gate,
        "errors": errors,
        "warnings": warnings,
        "input": {
            "task_markdown": request_summary["input_md_path"],
            "task_digest": request_summary["task_digest"],
            "branch": args.branch,
            "commit": args.commit,
            "issue": args.issue,
            "patch_note_limit": patch_note_limit,
            "requested_min_patch_notes": requested_min_patch_notes,
        },
        "request_summary": request_summary,
        "normalized_objective": normalized_objective,
        "patch_notes": patch_notes,
        "patch_notes_applicability": patch_notes_applicability(patch_notes),
        "patch_plan_summary": patch_summary,
        "telemetry_quality": build_telemetry_quality(loaded),
        "evidence_coverage": build_evidence_coverage(loaded, status),
        "missing_evidence": [],
        "validation_commands": validation_commands,
        "stop_conditions": patch_summary.get("stop_conditions")
        or [
            "manual review rejects patch plan evidence",
            "quality_gate_passed=false under strict operator policy",
            "guardrail reports source writes or patch application",
        ],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "operational_sqlite_fts_write_performed": True,
        "manual_review_required": True,
        "inputs": {
            "paths": {key: repo_rel(path, repo_root) for key, path in input_paths.items()},
            "status": status,
        },
        "guardrails": {
            "report_only": True,
            "manual_review_required": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "persistent_memory_write_performed": False,
            "raw_output_commit_allowed": False,
            "provider_execution_performed_by_builder": False,
            "strict_patch_notes_quality_gate": args.strict_patch_notes_quality_gate,
        },
    }
    report["missing_evidence"] = report["evidence_coverage"]["missing_evidence"]
    report["product_sufficiency"] = build_product_sufficiency(
        report,
        loaded,
        task,
        patch_note_limit=patch_note_limit,
        requested_min_patch_notes=requested_min_patch_notes,
    )
    report["fts_evidence_search"] = build_search_quality(
        repo_root,
        resolve(repo_root, args.sqlite_fts_db),
        input_paths,
        loaded,
        normalized_objective,
        [args.task_markdown, *args.extra_context],
    )
    score, findings, fallback = score_product(report)
    report["quality_score"] = score
    report["quality_findings"] = findings
    report["fallback_path_notes"] = fallback
    if score < args.min_quality_score:
        report["fallback_path_notes"].append(
            {
                "reason": "patch_notes_quality_score_below_threshold",
                "quality_score": score,
                "min_quality_score": args.min_quality_score,
                "recommended_followup": "strengthen request summary, evidence coverage, telemetry signals, validation commands and concrete/applicable patch notes",
            }
        )
    if not report["patch_notes_applicability"].get("all_applicable"):
        report["fallback_path_notes"].append(
            {
                "reason": "patch_notes_not_fully_applicable",
                "invalid_note_count": report["patch_notes_applicability"].get("invalid_note_count"),
                "recommended_followup": "fix patch notes so every item has targets, summary, edit strategy, validations, stop conditions and manual review flag",
            }
        )
    if report["product_sufficiency"].get("sufficient") is False:
        report["fallback_path_notes"].append(
            {
                "reason": "patch_notes_product_insufficient",
                "insufficiency_reasons": report["product_sufficiency"].get("insufficiency_reasons"),
                "missing_available_areas": report["product_sufficiency"].get(
                    "missing_available_areas"
                ),
                "recommended_followup": "generate a broader availability-aware backlog from repository consistency findings or lower the requested task scope",
            }
        )
    if report["fts_evidence_search"]["fts_total_hit_count"] <= 0:
        report["fallback_path_notes"].append(
            {
                "reason": "patch_notes_evidence_search_found_no_hits",
                "recommended_followup": "verify task MD and evidence artifacts contain shared concrete terms",
            }
        )
    report["quality_gate_passed"] = (
        not errors
        and bool(report["patch_notes"])
        and report["patch_notes_applicability"].get("all_applicable") is True
        and report["product_sufficiency"].get("sufficient", True) is True
        and score >= args.min_quality_score
        and report["fts_evidence_search"]["fts_total_hit_count"] > 0
    )
    if args.strict_patch_notes_quality_gate and not report["quality_gate_passed"]:
        errors.append("strict patch notes quality gate failed")
    report["passed"] = not errors
    report["classification"] = classify(errors, report["quality_gate_passed"], score)
    if report["product_sufficiency"].get("sufficient") is False and not errors:
        report["classification"] = "completed_with_insufficient_all_all_patch_notes"
    report["success_cases"] = build_success_cases(report, loaded)
    report["fallback_cases"] = build_fallback_cases(report, loaded, args.min_quality_score)
    return report
