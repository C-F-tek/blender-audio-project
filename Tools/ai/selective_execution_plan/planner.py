"""Selective execution plan assembly."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

from .common import PLAN_KIND, SCHEMA_VERSION, resolve_repo_path
from .recommendations import build_recommendations, command_sets
from .summaries import (
    summarize_context_evidence,
    summarize_dry_run_evidence,
    summarize_execution_plans,
    summarize_provider_evidence,
    summarize_tech_debt,
    summarize_validation_contract,
)

def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    """Build the selective execution plan."""
    repo_root = Path(args.repo_root).resolve()
    context_json = resolve_repo_path(repo_root, args.context_pack_evidence)
    context_md = resolve_repo_path(repo_root, args.context_pack_evidence_md)
    dry_run_path = resolve_repo_path(repo_root, args.dry_run_evidence)
    provider_path = resolve_repo_path(repo_root, args.provider_evidence)
    validation_path = resolve_repo_path(repo_root, args.validation_report_contract)
    plan_dir = resolve_repo_path(repo_root, args.execution_plan_dir)
    tech_debt_path = resolve_repo_path(repo_root, args.tech_debt)

    context = summarize_context_evidence(context_json, context_md, repo_root)
    dry_run = summarize_dry_run_evidence(dry_run_path, repo_root)
    provider = summarize_provider_evidence(provider_path, repo_root)
    validation = summarize_validation_contract(validation_path, repo_root)
    plans = summarize_execution_plans(plan_dir, repo_root)
    tech_debt = summarize_tech_debt(tech_debt_path, repo_root)

    validators, patch_specs, blocked, local_only, github_only, risks = build_recommendations(
        context=context,
        dry_run=dry_run,
        provider=provider,
        validation=validation,
        plans=plans,
        tech_debt=tech_debt,
    )

    warnings: list[str] = []
    for section in (context, dry_run, provider, validation, tech_debt):
        raw_warnings = section.get("warnings")
        if isinstance(raw_warnings, list):
            warnings.extend(str(item) for item in raw_warnings)
    errors: list[str] = []

    passed = (
        context.get("passed") is True
        and dry_run.get("passed") is True
        and dry_run.get("all_steps_planned_only") is True
        and provider.get("provider_execution_seen") is True
        and provider.get("ollama_gpu_primary_advisory") is True
        and provider.get("npu_excluded_when_unusable") is True
        and not errors
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "kind": PLAN_KIND,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "apply_mode": "report_only",
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "inputs": {
            "context_pack_evidence": context,
            "dry_run_matrix_evidence": dry_run,
            "latest_gpu_npu_evidence": provider,
            "validation_report_contract": validation,
            "execution_plan_status": plans,
            "tech_debt_tracker": tech_debt,
        },
        "provider_evidence_summary": provider,
        "dry_run_summary": dry_run,
        "validation_health": validation,
        "recommended_validators": validators,
        "recommended_patch_specs": patch_specs,
        "blocked_actions": blocked,
        "local_only_actions_for_carmine": local_only,
        "github_only_actions_for_ai": github_only,
        "risks": risks,
        "next_command_set": command_sets(),
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
    }
