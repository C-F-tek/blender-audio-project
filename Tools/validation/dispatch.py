"""Central dispatcher for validators, smokes, and validation gates.

Use ``python -m Tools.validation <tool> ...`` instead of launching validation
scripts by file path. Packaged validations resolve to their package CLIs;
remaining maintained tools fall back to ``Tools.validation.<tool>:main``.
"""

from pathlib import Path

from Tools.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {
    "check_ai_context_pack_contract": "Tools.validation._shared.ai_context_pack_contract_cli:main",
    "check_ai_peer_exchange_contract": "Tools.validation.ai_peer_exchange_contract.cli:main",
    "check_github_evidence_bundle": "Tools.validation._shared.github_evidence_bundle_cli:main",
    "check_local_ai_adapter_manifest": "Tools.validation._shared.local_ai_adapter_manifest_cli:main",
    "check_npu_pipeline_modules": "Tools.validation.npu_pipeline_modules_check.cli:main",
    "check_patch_spec_drafts": "Tools.validation._shared.patch_spec_drafts_cli:main",
    "check_provider_evidence_contract": "Tools.validation.provider_evidence_contract.cli:main",
    "check_reviewed_patch_specs": "Tools.validation.reviewed_patch_specs_check.cli:main",
    "check_unified_chain_contract": "Tools.validation.unified_chain_contract.cli:main",
    "run_agent_review_patch_plan_full_validation": (
        "Tools.validation.agent_review_patch_plan_full_validation.cli:main"
    ),
    "run_agnostic_ai_tools_smoke_matrix": (
        "Tools.validation.agnostic_ai_tools_smoke_matrix.cli:main"
    ),
    "run_agnostic_context_stack_smoke": (
        "Tools.validation.agnostic_context_stack_smoke.cli:main"
    ),
    "run_patch_notes_quality_product_smoke": (
        "Tools.validation.patch_notes_quality_product_smoke.cli:main"
    ),
    "run_validation_gate": "Tools.validation.validation_gate.cli:main",
}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.validation",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="validation",
    ).main(argv)
