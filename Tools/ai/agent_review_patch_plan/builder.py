"""Agent review patch plan assembly."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .common import APPLY_MODE, PLAN_KIND, load_json_object, now_iso, repo_rel, resolve_path
from .decision import build_decision
from .fallback import fallback_plans_from_evidence
from .gpu import gpu_plans_from_report
from .inputs import load_gpu_report, npu_audit_refs

def build_patch_plan(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    warnings: list[str] = []
    errors: list[str] = []

    orchestrator_path = resolve_path(repo_root, args.orchestrator)
    evidence_path = resolve_path(repo_root, args.evidence)
    orchestrator: dict[str, Any] = {}
    evidence: dict[str, Any] = {}

    if orchestrator_path.exists():
        try:
            orchestrator = load_json_object(orchestrator_path)
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Unable to read orchestrator report: {type(exc).__name__}: {exc}")
    else:
        warnings.append(f"orchestrator report missing: {repo_rel(orchestrator_path, repo_root)}")

    if evidence_path.exists():
        try:
            evidence = load_json_object(evidence_path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Unable to read evidence report: {type(exc).__name__}: {exc}")
    else:
        errors.append(f"evidence report missing: {repo_rel(evidence_path, repo_root)}")

    audit_refs = npu_audit_refs(orchestrator)
    gpu_report = load_gpu_report(repo_root, orchestrator, warnings) if orchestrator else {}
    plans, skipped = (
        gpu_plans_from_report(gpu_report=gpu_report, repo_root=repo_root, audit_refs=audit_refs)
        if gpu_report
        else ([], [])
    )

    fallback_used = False
    if not plans and evidence:
        fallback_used = True
        fallback_plans, fallback_skipped = fallback_plans_from_evidence(
            evidence=evidence,
            repo_root=repo_root,
            audit_refs=audit_refs,
        )
        plans.extend(fallback_plans)
        skipped.extend(fallback_skipped)

    if not plans and not errors:
        warnings.append(
            "no patch plans were produced from GPU recommendations or evidence fallback"
        )

    available_patch_plan_count = len(plans)
    requested_max_patch_plans = int(getattr(args, "max_patch_plans", 0) or 0)
    max_patch_plans = 0
    if requested_max_patch_plans > 0:
        warnings.append(
            "max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; "
            "patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection"
        )

    decision = build_decision(
        plans=plans,
        skipped=skipped,
        gpu_report=gpu_report,
        evidence=evidence,
        fallback_used=fallback_used,
    )
    return {
        "schema_version": 1,
        "kind": PLAN_KIND,
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": APPLY_MODE,
        "inputs": {
            "orchestrator": repo_rel(orchestrator_path, repo_root),
            "evidence": repo_rel(evidence_path, repo_root),
            "gpu_report": orchestrator.get("gpu_output"),
            "orchestrator_kind": orchestrator.get("kind"),
            "evidence_kind": evidence.get("kind"),
            "gpu_kind": gpu_report.get("kind"),
        },
        "decision": decision,
        "patch_plan_count": len(plans),
        "available_patch_plan_count": available_patch_plan_count,
        "max_patch_plans": max_patch_plans,
        "requested_max_patch_plans": requested_max_patch_plans,
        "patch_plans": plans,
        "skipped_candidate_count": len(skipped),
        "skipped_candidates": skipped,
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
