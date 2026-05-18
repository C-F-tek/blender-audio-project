"""Recommendation construction for selective execution plans."""

from __future__ import annotations

from typing import Any

def validator_item(name: str, reason: str, command: str, required: bool = True) -> dict[str, Any]:
    """Build a validator recommendation item."""
    return {
        "name": name,
        "reason": reason,
        "command": command,
        "required": required,
        "execution_scope": "github_or_local",
        "provider_execution_performed": False,
    }

def patch_spec_item(
    identifier: str,
    title: str,
    rationale: str,
    target_files: list[str],
    blocked: bool = False,
) -> dict[str, Any]:
    """Build a report-only patch-spec recommendation."""
    return {
        "id": identifier,
        "title": title,
        "rationale": rationale,
        "target_files": target_files,
        "apply_mode": "manual_review_only",
        "status": "candidate_spec_only",
        "blocked": blocked,
        "provider_execution_performed": False,
        "patch_application_performed": False,
    }

def build_recommendations(
    *,
    context: dict[str, Any],
    dry_run: dict[str, Any],
    provider: dict[str, Any],
    validation: dict[str, Any],
    plans: dict[str, Any],
    tech_debt: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[str],
    list[str],
    list[str],
    list[str],
]:
    """Build validator, patch-spec and action recommendations."""
    validators: list[dict[str, Any]] = []
    patch_specs: list[dict[str, Any]] = []
    blocked: list[str] = []
    local_only: list[str] = []
    github_only: list[str] = []
    risks: list[str] = []

    validators.append(
        validator_item(
            "python_syntax",
            "New planner and validator are Python scripts and must compile without imports.",
            r"python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax.json",
        )
    )
    validators.append(
        validator_item(
            "ai_context_pack_contract",
            "The selective planner depends on context-pack evidence as its first input.",
            r"python -m Tools.validation check_ai_context_pack_contract --repo-root . --pack .\output\ai_context_packs\project_self_improvement.json --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\project_self_improvement_context_pack_evidence.json --output .\output\validation\ai_context_pack_contract.json",
        )
    )
    validators.append(
        validator_item(
            "dry_run_matrix_evidence_bundle",
            "Dry-run evidence must remain planned-only and must not imply provider execution.",
            r"python -m Tools.validation check_dry_run_matrix_evidence_bundle --repo-root . --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\ai_pipeline_dry_run_matrix_evidence.json --output .\output\validation\dry_run_matrix_evidence_bundle.json",
        )
    )
    validators.append(
        validator_item(
            "github_evidence_bundle",
            "Provider evidence must keep Ollama/GPU and OpenVINO/NPU roles explicit.",
            r"python -m Tools.validation check_github_evidence_bundle --repo-root . --output .\output\validation\github_evidence_bundle.json",
        )
    )
    validators.append(
        validator_item(
            "selective_execution_plan",
            "Validate the report-only planner output contract before using it for next-step selection.",
            r"python -m Tools.validation check_selective_execution_plan --repo-root . --plan .\output\ai_pipeline\selective_execution_plan.json --output .\output\validation\selective_execution_plan.json",
        )
    )
    validators.append(
        validator_item(
            "validation_report_contract",
            "Keep the new validator aligned with common validation report fields.",
            r"python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json",
        )
    )

    if context.get("passed") is not True:
        blocked.append(
            "context pack evidence is missing or not passing; do not generate patch specs from incomplete context"
        )
        risks.append(
            "Planner may fall back to Markdown context evidence when JSON evidence is unavailable."
        )
    if dry_run.get("passed") is not True or dry_run.get("all_steps_planned_only") is not True:
        blocked.append(
            "dry-run matrix evidence is not clean; do not recommend provider promotion or patch-spec generation"
        )
    if provider.get("provider_execution_seen") is not True:
        blocked.append("real provider evidence is missing; do not promote advisory provider state")
        local_only.append(
            "Generate new real GPU/NPU evidence with the explicit PowerShell command set."
        )
    if provider.get("ollama_gpu_primary_advisory") is not True:
        blocked.append("Ollama/GPU is not quality-gated as primary advisory in current evidence")
    if provider.get("npu_excluded_when_unusable") is not True:
        risks.append(
            "NPU advisory exclusion decision is absent or false; keep NPU limited to probe/guardrail/decode diagnostic."
        )
    if validation.get("passed") is not True:
        risks.append(
            "validation_report_contract output is absent or not passing in this checkout; rerun locally after planner generation."
        )

    patch_specs.append(
        patch_spec_item(
            "selective-planner-v2-validator-ranking",
            "Selective planner v2: score and rank validators",
            "Current prototype emits deterministic validator recommendations; next patch spec should add scoring without executing validators.",
            [
                "Tools/ai/selective_execution_plan/cli.py",
                "docs/AI_SELECTIVE_PLANNER.md",
            ],
            blocked=False,
        )
    )
    patch_specs.append(
        patch_spec_item(
            "provider-evidence-quality-gates",
            "Formal provider evidence quality gate spec",
            "Real GPU/NPU evidence exists but promotion criteria should be made explicit before changing provider behavior.",
            [
                "docs/LOCAL_AI_WORKFLOW.md",
                "docs/JSON_SCHEMAS.md",
                "Tools/validation/check_github_evidence_bundle/cli.py",
            ],
            blocked=provider.get("provider_execution_seen") is not True,
        )
    )
    patch_specs.append(
        patch_spec_item(
            "patch-spec-generator-integration",
            "Patch spec generator integration from selective plan",
            "After this report-only planner is validated, a future tool can convert recommended_patch_specs into draft patch specs.",
            [
                "Tools/ai/generated_patch_specs/proposal_cli.py",
                "Tools/validation/check_patch_spec_drafts/cli.py",
            ],
            blocked=context.get("passed") is not True or dry_run.get("passed") is not True,
        )
    )

    github_only.extend(
        [
            "Review committed context-pack, dry-run and provider evidence summaries.",
            "Update docs and validators only; do not modify Blender runtime or generated indexes manually.",
            "Open small PRs that add report-only tooling and explicit local command sets.",
        ]
    )
    local_only.extend(
        [
            "Run explicit GPU/NPU provider workflow only when new evidence is needed.",
            "Commit compact evidence bundles under docs/LOCAL_VALIDATION_EVIDENCE/ after local execution.",
        ]
    )

    if plans.get("related_plan_count", 0) == 0:
        risks.append("No active execution plan currently appears tied to selective planner work.")
    if not any(tech_debt.get("keywords", {}).values()):
        risks.append("Tech debt tracker does not yet expose strong selective-planner markers.")

    return validators, patch_specs, blocked, local_only, github_only, risks

def command_sets() -> dict[str, list[str]]:
    """Return copy-pasteable command sets."""
    return {
        "build_and_validate_selective_plan": [
            r"python -m Tools.ai ai_context_pack --repo-root . --profile project_self_improvement",
            r"python -m Tools.ai selective_execution_plan --repo-root . --output .\output\ai_pipeline\selective_execution_plan.json --markdown-output .\output\ai_pipeline\selective_execution_plan.md",
            r"python -m Tools.validation check_selective_execution_plan --repo-root . --plan .\output\ai_pipeline\selective_execution_plan.json --output .\output\validation\selective_execution_plan.json",
        ],
        "real_gpu_npu_evidence_for_carmine": [
            r"python -m Tools.workflow run_parallel_ai_provider_multistep `",
            r"  -Profile npu `",
            r"  -RunOllamaProbe `",
            r"  -RunNpuProbe `",
            r"  -RunNpuDecodeSmoke `",
            r"  -UsePrimaryAdvisoryProvider `",
            r"  -Basename parallel_gpu_npu_selective_planner_real `",
            r"  -ProposalBasename parallel_gpu_npu_selective_planner_real_proposals `",
            r"  -EvidenceBasename parallel_gpu_npu_selective_planner_real_evidence",
            r"python -m Tools.ai build_github_evidence_bundle --repo-root . --basename parallel_gpu_npu_selective_planner_real_evidence",
            r"python -m Tools.validation check_github_evidence_bundle --repo-root . --output .\output\validation\github_evidence_bundle.json",
            r"python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json",
        ],
        "minimum_pr_validation": [
            r"python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax.json",
            r"python -m Tools.validation check_json_artifacts --repo-root . --output .\output\validation\json_artifacts.json",
            r"python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links.json",
            r"python -m Tools.validation check_execution_plan_status --repo-root . --output .\output\validation\execution_plan_status.json",
            r"python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json",
            "git diff --check",
        ],
    }
