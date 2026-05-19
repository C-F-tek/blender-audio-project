from __future__ import annotations

from .common import *  # noqa: F403
from .proposal_models import proposal, proposal_concrete_operation_count, proposals_concrete_operation_count
from .proposal_templates import (
    ai_workload_quality_remediation_proposal,
    default_npu_observability_proposal,
    post_validation_loop_hardening_proposal,
    provider_report_adoption_proposal,
)
from .provider_checks import (
    ai_workload_quality_has_unusable_output,
    all_provider_observability_green,
    provider_report_adoption_green,
)
from .runtime_peer import runtime_peer_evidence_proposal, runtime_peer_evidence_ready


def build_proposals(
    reports: list[dict[str, Any]],
    *,
    profile: str,
    require_concrete: bool = False,
) -> list[dict[str, Any]]:
    by_kind = report_by_kind(reports)
    by_kind_multi = reports_by_kind(reports)
    proposals: list[dict[str, Any]] = []
    runtime_summary = runtime_peer_evidence_summary(by_kind_multi, reports)

    if runtime_peer_evidence_ready(runtime_summary) and runtime_summary.get(
        "needs_concrete_generated_product"
    ):
        proposals.append(runtime_peer_evidence_proposal(runtime_summary))

    execution_plan_status = by_kind.get("execution_plan_status")
    if not proposals and execution_plan_status and execution_plan_status.get("passed") is False:
        proposals.append(
            proposal(
                proposal_id="P-EXEC-PLAN-STATUS",
                priority="P1",
                area="execution_plans",
                title="Fix execution-plan folder/status drift",
                rationale="The execution-plan validator reports terminal-status plans in the wrong folder or invalid status markers.",
                target_files=[
                    "docs/EXECUTION_PLANS/active/",
                    "docs/EXECUTION_PLANS/completed/",
                    "docs/EXECUTION_PLANS/abandoned/",
                ],
                change_type="docs_move_or_status_fix",
                sketch=[
                    "Move plans with top-level `## Status` = `completed` from active/ to completed/.",
                    "Move abandoned plans to abandoned/ or change their top-level status back to active/planned if still open.",
                    "Do not treat folder README.md files as execution plans.",
                ],
                validation=[
                    "python -m Tools.validation check_execution_plan_status --repo-root . --output .\\output\\validation\\execution_plan_status.json",
                    "python -m Tools.validation check_docs_links --repo-root . --output .\\output\\validation\\docs_links.json",
                ],
                stop_conditions=[
                    "Any moved plan has unclear status or contains active unfinished work."
                ],
            )
        )

    npu_manifest = by_kind.get("npu_runtime_output_manifest")
    if not proposals and npu_manifest and npu_manifest.get("blocked_count", 0):
        proposals.append(
            proposal(
                proposal_id="P-NPU-MANIFEST-BLOCKED-OUTPUTS",
                priority="P1",
                area="npu_observability",
                title="Review blocked NPU runtime output paths",
                rationale="The runtime-output manifest found paths outside the exact legacy output allowlist.",
                target_files=[
                    "Tools/npu/provider_mesh/runtime_output_manifest/cli.py",
                    "Tools/npu/pipeline/artifact_paths.py",
                    "docs/JSON_SCHEMAS.md",
                ],
                change_type="policy_review",
                sketch=[
                    "Inspect each blocked output path in `output/validation/npu_runtime_output_manifest.json`.",
                    "If the path is a legitimate legacy runtime output, add it to the exact allowlist with a focused test.",
                    "If not legitimate, keep it blocked and document why.",
                ],
                validation=[
                    "python -m Tools.npu build_runtime_output_manifest --repo-root . --output .\\output\\validation\\npu_runtime_output_manifest.json",
                    "python -m Tools.workflow run_npu_pipeline_helper_validation",
                ],
                stop_conditions=[
                    "A blocked path points to source code, full analysis JSON or an unreviewed generated destination."
                ],
            )
        )

    resource_lanes = by_kind.get("local_ai_resource_lanes")
    if not proposals and resource_lanes:
        ready = set(resource_lanes.get("ready_lanes") or [])
        available = set(resource_lanes.get("available_lanes") or [])
        if {"npu", "gpu", "ollama"} - ready:
            proposals.append(
                proposal(
                    proposal_id="P-RESOURCE-LANE-PREFLIGHTS",
                    priority="P2",
                    area="local_ai_resources",
                    title="Stabilize local NPU/GPU/Ollama resource-lane readiness",
                    rationale="One or more local AI resource lanes are unavailable or not ready. Keeping this as observability improves future parallel pipeline work.",
                    target_files=[
                        "Tools/ai/provider_mesh/local_resource_lanes_check/cli.py",
                        "Tools/workflow/_powershell/run_post_validation_ai_packet.ps1",
                        "Tools/validation/README.md",
                    ],
                    change_type="preflight_hardening",
                    sketch=[
                        f"Ready lanes currently reported: {sorted(ready)}.",
                        f"Available lanes currently reported: {sorted(available)}.",
                        "Keep missing lanes as warnings unless explicitly required with `--require-lane`.",
                        "Add narrower diagnostics for lanes that are available but not ready.",
                    ],
                    validation=[
                        "python -m Tools.ai check_local_resource_lanes --repo-root . --parallel --output .\\output\\validation\\local_ai_resource_lanes.json --markdown-output .\\output\\validation\\local_ai_resource_lanes.md",
                        "python -m Tools.workflow run_post_validation_ai_packet -Profile npu -ReportFile output/validation/local_ai_resource_lanes.json",
                    ],
                    stop_conditions=[
                        "A lane probe would need long generation, Blender execution, GPU render or provider behavior changes."
                    ],
                )
            )

    validation_contract = by_kind.get("validation_report_contract")
    if not proposals and validation_contract and validation_contract.get("passed") is False:
        proposals.append(
            proposal(
                proposal_id="P-REPORT-CONTRACT-CONSISTENCY",
                priority="P1",
                area="validation_contracts",
                title="Normalize validation report root fields",
                rationale="The validation-report contract checker found reports missing common fields or using inconsistent types.",
                target_files=[
                    "Tools/validation/*.py",
                    "Tools/npu/pipeline/reports.py",
                    "docs/JSON_SCHEMAS.md",
                ],
                change_type="contract_normalization",
                sketch=[
                    "Add missing root fields additively: schema_version, kind, repo_root, passed, errors, warnings where applicable.",
                    "Do not remove validator-specific fields.",
                    "Keep strict mode opt-in until all local reports are aligned.",
                ],
                validation=[
                    "python -m Tools.validation check_validation_report_contract --repo-root . --output .\\output\\validation\\validation_report_contract.json",
                    "python -m Tools.workflow run_local_validation_after_refactor -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2",
                ],
                stop_conditions=[
                    "A proposed normalization would change the meaning of existing report fields."
                ],
            )
        )

    if not proposals and require_concrete:
        return proposals

    if not proposals:
        if ai_workload_quality_has_unusable_output(by_kind):
            proposals.append(ai_workload_quality_remediation_proposal(by_kind))
        elif provider_report_adoption_green(by_kind):
            proposals.append(post_validation_loop_hardening_proposal())
        elif all_provider_observability_green(by_kind):
            proposals.append(provider_report_adoption_proposal())
        else:
            proposals.append(default_npu_observability_proposal())

    return proposals
