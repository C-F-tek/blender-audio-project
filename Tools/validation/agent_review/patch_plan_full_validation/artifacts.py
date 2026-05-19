"""Artifact validation for agent review patch-plan full validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import load_json, rel, summarize_artifact, value_at

def validate_expected_outputs(
    *,
    repo_root: Path,
    patch_plan_path: Path,
    smoke_path: Path,
    bundle_json: Path,
    bundle_md: Path,
    min_patch_plans: int,
    expect_fallback: bool,
) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    artifacts = {
        "patch_plan": summarize_artifact(patch_plan_path, repo_root),
        "smoke": summarize_artifact(smoke_path, repo_root),
        "bundle_json": summarize_artifact(bundle_json, repo_root),
        "bundle_markdown": {
            "path": rel(bundle_md, repo_root),
            "exists": bundle_md.exists(),
            "json_ok": None,
            "error": "" if bundle_md.exists() else "missing",
        },
    }

    patch_plan, patch_error = (
        load_json(patch_plan_path) if patch_plan_path.exists() else (None, "missing")
    )
    if patch_error or patch_plan is None:
        errors.append(f"patch plan unreadable: {patch_error}")
    else:
        count = patch_plan.get("patch_plan_count")
        if not isinstance(count, int) or count < min_patch_plans:
            errors.append(
                f"patch_plan_count below minimum: expected >= {min_patch_plans}, got {count!r}"
            )
        fallback = value_at(patch_plan, "decision.fallback_used")
        if expect_fallback and fallback is not True:
            errors.append(f"expected patch plan fallback_used=true, got {fallback!r}")
        if patch_plan.get("provider_execution_performed") is not False:
            errors.append("patch plan provider_execution_performed must be false")
        if patch_plan.get("patch_application_performed") is not False:
            errors.append("patch plan patch_application_performed must be false")

    smoke, smoke_error = load_json(smoke_path) if smoke_path.exists() else (None, "missing")
    if smoke_error or smoke is None:
        errors.append(f"smoke report unreadable: {smoke_error}")
    elif smoke.get("passed") is not True:
        errors.append("agent_review_patch_plan_smoke did not pass")

    if not bundle_json.exists():
        errors.append(f"evidence bundle JSON missing: {rel(bundle_json, repo_root)}")
    if not bundle_md.exists():
        errors.append(f"evidence bundle Markdown missing: {rel(bundle_md, repo_root)}")

    bundle, bundle_error = load_json(bundle_json) if bundle_json.exists() else (None, "missing")
    if bundle_error or bundle is None:
        errors.append(f"evidence bundle unreadable: {bundle_error}")
    elif bundle.get("kind") != "github_validation_evidence_bundle":
        errors.append(f"unexpected evidence bundle kind: {bundle.get('kind')!r}")

    return errors, warnings, artifacts
