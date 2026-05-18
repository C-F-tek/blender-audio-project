"""Runner for agent review patch-plan full validation."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .artifacts import validate_expected_outputs
from .commands import build_commands
from .common import now_iso, rel, repo_path, run_command

def run_full_validation(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    commands, bundle_json, bundle_md = build_commands(args, repo_root)
    steps: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []

    for name, command, timeout_seconds in commands:
        result = run_command(command, repo_root, timeout_seconds)
        result["name"] = name
        steps.append(result)
        if not result["ok"] and name != "git_status_short":
            errors.append(
                f"{name} returned {result['returncode']}: {result.get('error') or result.get('stderr_tail') or result.get('stdout_tail')}"
            )

    artifact_errors, artifact_warnings, artifacts = validate_expected_outputs(
        repo_root=repo_root,
        patch_plan_path=repo_path(repo_root, args.patch_plan),
        smoke_path=repo_path(repo_root, args.smoke_output),
        bundle_json=bundle_json,
        bundle_md=bundle_md,
        min_patch_plans=args.min_patch_plans,
        expect_fallback=args.expect_fallback,
    )
    errors.extend(artifact_errors)
    warnings.extend(artifact_warnings)

    return {
        "schema_version": 1,
        "kind": "agent_review_patch_plan_full_validation",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "evidence_writes_performed": True,
        "apply_mode": "report_only_full_validation_and_evidence_bundle",
        "steps": steps,
        "artifacts": artifacts,
        "evidence_bundle": {
            "json": rel(bundle_json, repo_root),
            "markdown": rel(bundle_md, repo_root),
            "validation_report": args.bundle_validation_output,
        },
        "decision": {
            "standard_validation_completed": not errors,
            "bundle_generated": bundle_json.exists() and bundle_md.exists(),
            "manual_review_required": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
        },
        "guardrails": {
            "report_only": True,
            "manual_review_required": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "blender_runtime_execution_performed": False,
            "npu_primary_advisory": False,
            "openvino_gpu_primary_lane": False,
        },
    }
