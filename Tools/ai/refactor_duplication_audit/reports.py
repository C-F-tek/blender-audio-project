"""Existing-report ingestion and runtime-layer checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import read_json_report, read_text, repo_rel, resolve_path, safe_id

def collect_report_status(
    repo_root: Path, report_paths: list[str]
) -> tuple[list[dict[str, Any]], list[str]]:
    reports: list[dict[str, Any]] = []
    warnings: list[str] = []
    for raw in report_paths:
        path = resolve_path(repo_root, raw)
        data = read_json_report(path)
        item = {
            "path": repo_rel(path, repo_root),
            "exists": path.exists(),
            "kind": data.get("kind"),
            "passed": data.get("passed"),
            "provider_execution_performed": data.get("provider_execution_performed"),
            "patch_application_performed": data.get("patch_application_performed"),
            "sqlite_write_performed": data.get("sqlite_write_performed"),
            "persistent_memory_write_performed": data.get("persistent_memory_write_performed"),
            "errors": data.get("errors", []),
            "warnings": data.get("warnings", []),
        }
        if path.exists() and not data:
            warnings.append(
                f"{repo_rel(path, repo_root)} exists but is not a JSON object or could not be parsed"
            )
        reports.append(item)
    return reports, warnings

def verify_layering(repo_root: Path) -> dict[str, Any]:
    files = {
        "builder": repo_root / "Tools/ai/shared_toolbox_bundle/cli.py",
        "bundle": repo_root / "tools/ai/repository_product/github_evidence_bundle.py",
        "artifacts": repo_root / "tools/ai/github_evidence_bundle_artifacts.py",
        "validator": repo_root / "tools/validation/check_github_evidence_bundle.py",
        "smoke": repo_root / "tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py",
    }
    content = {key: read_text(path)[0] for key, path in files.items()}
    checks = {
        "layering_preserved": all(path.exists() for path in files.values()),
        "builder_delegates_to_common_bundle": "build_bundle" in content["builder"]
        and "Tools.ai.repository_product.github_evidence_bundle" in content["builder"],
        "chunking_in_common_evidence_layer": "artifact_chunk_index" in content["artifacts"]
        or "build_artifact_chunk_index" in content["artifacts"],
        "validator_reused": "validate_github_evidence_bundles" in content["builder"]
        and "check_github_evidence_bundle" in content["builder"],
        "smoke_coverage_present": all(
            token in content["smoke"]
            for token in (
                "chunked_large_files_seen",
                "bundle_validation_passed",
                "recursive_default_files_seen",
            )
        ),
        "cli_schema_preserved": "parse_args" in content["builder"]
        and "--validate-bundle" in content["builder"],
        "report_schema_preserved": "shared_toolbox_ai_to_ai_final_summary" in content["builder"]
        and "github_validation_evidence_bundle" in content["bundle"],
    }
    checks["passed"] = all(bool(value) for value in checks.values())
    return checks

def audit_list(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    raw = data.get(key)
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, dict)]

def normalize_imported_candidate(
    item: dict[str, Any], *, source: str, index: int
) -> dict[str, Any]:
    candidate = dict(item)
    fallback = (
        candidate.get("candidate_id")
        or candidate.get("id")
        or candidate.get("title")
        or candidate.get("repeated_logic")
    )
    candidate["candidate_id"] = safe_id(str(fallback or f"imported_audit_candidate_{index:03d}"))
    candidate.setdefault("source", source)
    candidate.setdefault(
        "repeated_logic",
        candidate.get("title") or "Imported local-AI/refactor audit candidate.",
    )
    candidate.setdefault("files_involved", candidate.get("target_files") or [])
    candidate.setdefault("existing_helper_available", None)
    candidate.setdefault(
        "preferred_existing_helper_or_module",
        candidate.get("preferred_helper")
        or candidate.get("preferred_existing_helper_or_module")
        or "Imported audit did not specify a helper/module.",
    )
    candidate.setdefault(
        "recommendation_type",
        candidate.get("recommendation_type") or "needs_more_context",
    )
    candidate.setdefault("risk", candidate.get("risk") or "needs_review")
    candidate.setdefault(
        "schema_or_cli_impact",
        candidate.get("schema_or_cli_impact") or "needs manual review",
    )
    candidate.setdefault(
        "validation_required",
        candidate.get("validation") or ["manual review", "check_python_syntax"],
    )
    candidate.setdefault("manual_review_required", True)
    return candidate

def merge_existing_audit_candidates(repo_root: Path, paths: list[str]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    candidate_keys = (
        "duplication_candidates",
        "refactor_candidates",
        "duplicate_code_candidates",
        "helper_reuse_candidates",
        "manual_review_patch_plan_candidates",
    )
    for raw in paths:
        path = resolve_path(repo_root, raw)
        source = repo_rel(path, repo_root)
        data = read_json_report(path)
        if not data:
            continue
        index = 0
        for key in candidate_keys:
            for item in audit_list(data, key):
                index += 1
                candidate = normalize_imported_candidate(item, source=source, index=index)
                candidate.setdefault("imported_from_key", key)
                merged.append(candidate)
    return merged

def summarize_existing_audit_reports(repo_root: Path, paths: list[str]) -> dict[str, Any]:
    summaries: list[dict[str, Any]] = []
    helper_recommendations: list[str] = []
    advisory_findings: list[str] = []
    manual_plans: list[dict[str, Any]] = []
    for raw in paths:
        path = resolve_path(repo_root, raw)
        rel = repo_rel(path, repo_root)
        data = read_json_report(path)
        summary = {
            "path": rel,
            "exists": path.exists(),
            "kind": data.get("kind") if data else None,
            "passed": data.get("passed") if data else None,
            "provider_execution_performed": (
                data.get("provider_execution_performed") if data else None
            ),
            "patch_application_performed": (
                data.get("patch_application_performed") if data else None
            ),
            "sqlite_write_performed": (data.get("sqlite_write_performed") if data else None),
            "persistent_memory_write_performed": (
                data.get("persistent_memory_write_performed") if data else None
            ),
            "duplication_candidate_count": (
                len(audit_list(data, "duplication_candidates")) if data else 0
            ),
            "manual_review_patch_plan_candidate_count": (
                len(audit_list(data, "manual_review_patch_plan_candidates")) if data else 0
            ),
        }
        summaries.append(summary)
        if not data:
            continue
        raw_helper = data.get("helper_reuse_recommendations")
        if isinstance(raw_helper, list):
            for item in raw_helper:
                text = str(item).strip()
                if text and text not in helper_recommendations:
                    helper_recommendations.append(text)
        raw_advisory = data.get("advisory_only_findings")
        if isinstance(raw_advisory, list):
            for item in raw_advisory:
                text = str(item).strip()
                if text and text not in advisory_findings:
                    advisory_findings.append(text)
        for item in audit_list(data, "manual_review_patch_plan_candidates"):
            plan = dict(item)
            plan.setdefault("source", rel)
            plan.setdefault("manual_review_required", True)
            manual_plans.append(plan)
    return {
        "reports": summaries,
        "helper_reuse_recommendations": helper_recommendations,
        "advisory_only_findings": advisory_findings,
        "manual_review_patch_plan_candidates": manual_plans,
    }
