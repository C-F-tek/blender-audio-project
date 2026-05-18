"""Central dispatcher for validators, smokes, and validation gates.

Use ``python -m Tools.validation <tool> ...`` instead of launching validation
scripts by file path. Packaged validations resolve to their package CLIs;
remaining maintained tools fall back to ``Tools.validation.<tool>:main``.
"""

from pathlib import Path

from Tools.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {
    "agent_review_patch_plan_full_validation": "Tools.validation.agent_review.patch_plan_full_validation.cli:main",
    "check_ai_context_pack_contract": "Tools.validation._shared.ai_context_pack_contract_cli:main",
    "check_github_evidence_bundle": "Tools.validation._shared.github_evidence_bundle_cli:main",
    "check_local_ai_adapter_manifest": "Tools.validation._shared.local_ai_adapter_manifest_cli:main",
    "check_patch_spec_drafts": "Tools.validation._shared.patch_spec_drafts_cli:main",
    "run_agent_review_code_patch_plan_smoke": "Tools.validation.agent_review.code_patch_plan_smoke.cli:main",
    "run_agent_review_decision_loop_smoke": "Tools.validation.agent_review.decision_loop_smoke.cli:main",
    "run_agent_review_evidence_sufficiency_smoke": "Tools.validation.agent_review.evidence_sufficiency_smoke.cli:main",
    "run_agent_review_full_toolbox_workflow_static_smoke": "Tools.validation.agent_review.full_toolbox_workflow_static_smoke.cli:main",
    "run_agent_review_patch_bundle_builder_smoke": "Tools.validation.agent_review.patch_bundle_builder_smoke.cli:main",
    "run_agent_review_patch_plan_smoke": "Tools.validation.agent_review.patch_plan_smoke.cli:main",
    "run_agent_review_warning_policy_smoke": "Tools.validation.agent_review.warning_policy_smoke.cli:main",
}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.validation",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="validation",
    ).main(argv)
