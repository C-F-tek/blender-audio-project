from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from Tools.ai.patch_plan_quality_product.io_utils import (
    flatten_json,
    now_iso,
    read_json,
    repo_rel,
    resolve,
)
from Tools.ai.patch_plan_quality_product.scoring import classify, list_plans, score_plan
from Tools.ai.patch_plan_quality_product.token_search import (
    build_search_index,
    safe_tokens,
    search_docs,
)


def input_paths_from_args(args: Any, repo_root: Path) -> dict[str, Path]:
    paths = {
        "patch_plan": resolve(repo_root, args.patch_plan),
        "decision_loop": resolve(repo_root, args.decision_loop),
        "recommendations": resolve(repo_root, args.recommendations),
        "runtime_usage": resolve(repo_root, args.runtime_usage),
        "runtime_capability": resolve(repo_root, args.runtime_capability),
        "repository_consistency": resolve(repo_root, args.repository_consistency),
    }
    if args.memory_bundle:
        paths["memory_bundle"] = resolve(repo_root, args.memory_bundle)
    return paths


def load_inputs(
    input_paths: dict[str, Path],
) -> tuple[dict[str, dict[str, Any]], dict[str, str], list[str], list[str]]:
    loaded, status, fatal, warnings = {}, {}, [], []
    required = {
        "patch_plan",
        "decision_loop",
        "recommendations",
        "runtime_usage",
        "runtime_capability",
        "repository_consistency",
    }
    for key, path in input_paths.items():
        data, error = read_json(path)
        loaded[key], status[key] = data, error or "ok"
        if key in required and error:
            fatal.append(f"{key}: {error} ({path})")
        elif error and error != "not_provided":
            warnings.append(f"{key}: {error} ({path})")
    return loaded, status, fatal, warnings


def build_quality_notes(
    plan_scores: list[dict[str, Any]],
    avg_score: float,
    total_hits: int,
    args: Any,
    input_status: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    findings, fallback = [], []
    if not plan_scores:
        findings.append({"severity": "high", "reason": "patch_plan_contains_no_plan_items"})
    for item in plan_scores:
        if item["score"] < args.min_plan_score:
            findings.append(
                {
                    "severity": "medium",
                    "reason": "plan_below_item_threshold",
                    "plan_id": item["id"],
                    "score": item["score"],
                    "notes": item["notes"],
                }
            )
    if avg_score < args.min_average_score:
        fallback.append(
            {
                "reason": "average_patch_plan_score_below_threshold",
                "average_plan_score": avg_score,
                "min_average_score": args.min_average_score,
                "recommended_followup": "strengthen rationale, edit strategy, source evidence, validation commands and stop conditions",
            }
        )
    if total_hits <= 0:
        fallback.append(
            {
                "reason": "sqlite_fts_search_found_no_relevant_evidence_hits",
                "recommended_followup": "verify task/evidence/telemetry/memory terms are indexed and specific enough",
            }
        )
    missing = [
        key
        for key in ("runtime_usage", "runtime_capability", "repository_consistency")
        if input_status.get(key) != "ok"
    ]
    if missing:
        fallback.append(
            {
                "reason": "required_tool_evidence_missing_or_unreadable",
                "affected_inputs": missing,
                "recommended_followup": "rerun with runtime telemetry, capability manifest and repository consistency reports enabled",
            }
        )
    return findings, fallback


def build_report(args: Any) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    db_path = resolve(repo_root, args.sqlite_fts_db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    input_paths = input_paths_from_args(args, repo_root)
    loaded, status, fatal_errors, warnings = load_inputs(input_paths)
    plans = list_plans(loaded.get("patch_plan", {}))
    plan_scores = [score_plan(plan, repo_root, i) for i, plan in enumerate(plans, 1)]
    avg_score = (
        round(sum(item["score"] for item in plan_scores) / len(plan_scores), 2)
        if plan_scores
        else 0.0
    )
    with sqlite3.connect(db_path) as conn:
        fts_enabled, indexed = build_search_index(
            conn, repo_root, input_paths, loaded, args.request, args.extra_context
        )
        query_results = []
        for term in safe_tokens(
            args.request + " " + flatten_json(plans, limit=120_000), max_terms=16
        )[:8]:
            hits = search_docs(conn, fts_enabled, term, args.search_limit)
            query_results.append({"query": term, "hit_count": len(hits), "hits": hits[:3]})
    total_hits = sum(item["hit_count"] for item in query_results)
    findings, fallback = build_quality_notes(plan_scores, avg_score, total_hits, args, status)
    quality_gate_passed = (
        bool(plan_scores) and avg_score >= args.min_average_score and total_hits > 0
    )
    if args.strict_quality_gate and not quality_gate_passed:
        fatal_errors.append("strict quality gate failed")
    return {
        "schema_version": 1,
        "kind": "patch_plan_quality_product_gate",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not fatal_errors,
        "quality_gate_passed": quality_gate_passed,
        "classification": classify(fatal_errors, quality_gate_passed, avg_score, total_hits),
        "non_blocking": not args.strict_quality_gate,
        "errors": fatal_errors,
        "warnings": warnings,
        "quality_findings": findings,
        "fallback_path_notes": fallback,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "operational_sqlite_fts_write_performed": True,
        "manual_review_required": True,
        "inputs": {
            "paths": {k: repo_rel(v, repo_root) for k, v in input_paths.items()},
            "status": status,
            "sqlite_fts_db": repo_rel(db_path, repo_root),
        },
        "quality": {
            "patch_plan_count": len(plan_scores),
            "average_plan_score": avg_score,
            "min_average_score": args.min_average_score,
            "min_plan_score": args.min_plan_score,
            "plan_scores": plan_scores,
            "sqlite_fts5_enabled": fts_enabled,
            "indexed_document_count": indexed,
            "fts_query_count": len(query_results),
            "fts_total_hit_count": total_hits,
            "query_results": query_results,
        },
        "tool_utility_proof": {
            "runtime_tool_telemetry_used": bool(loaded.get("runtime_usage", {})),
            "runtime_capability_manifest_used": bool(loaded.get("runtime_capability", {})),
            "repository_consistency_used": bool(loaded.get("repository_consistency", {})),
            "memory_bundle_used": bool(loaded.get("memory_bundle", {})),
            "sqlite_fts_or_fallback_used": True,
            "concrete_effects": [
                "scores patch plans for target concreteness, rationale, strategy, validation and stop conditions",
                "indexes request/evidence/telemetry/memory into operational SQLite FTS under output/**",
                "records query hit counts proving which evidence was reachable",
                "preserves run completion by writing fallback_path_notes instead of failing on weak patch-note quality",
            ],
        },
        "guardrails": {
            "report_only": True,
            "manual_review_required": True,
            "operational_sqlite_under_output": repo_rel(db_path, repo_root).startswith("output/"),
            "persistent_memory_write_performed": False,
            "patch_application_performed": False,
            "generated_output_commit_allowed": False,
            "strict_quality_gate": args.strict_quality_gate,
        },
    }
