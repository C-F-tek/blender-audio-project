"""Central dispatcher for packaged AI tools.

The dispatcher replaces legacy one-file compatibility wrappers in ``Tools/ai``.
Use ``python -m Tools.ai <tool> ...`` so each tool owns its implementation in a
dedicated package while the operator still has one predictable command surface.
"""

from pathlib import Path

from Tools.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {
    "agent_memory_routing_policy": "Tools.ai.agent_memory.routing_cli:main",
    "agent_runtime_sqlite_memory": "Tools.ai.agent_memory.sqlite_cli:main",
    "analyze_gpu_npu_run_sync": "Tools.ai.gpu_npu_run_sync_analysis.cli:main",
    "apply_patch_bundle": "Tools.ai.patchkit.apply_patch_bundle:main",
    "apply_generated_patch_specs_for_review_pr": "Tools.ai.generated_patch_specs.apply_cli:main",
    "build_agent_agnostic_tool_inventory": "Tools.ai._shared.agent_agnostic_tool_inventory_cli:main",
    "build_agent_memory_inventory": "Tools.ai._shared.agent_memory_inventory_cli:main",
    "build_agent_review_code_patch_plan": "Tools.ai.agent_review.code_patch_plan_cli:main",
    "build_agent_review_evidence_sufficiency": "Tools.ai.agent_review.evidence_cli:main",
    "build_agent_review_patch_bundle": "Tools.ai.agent_review.patch_bundle_cli:main",
    "build_agent_review_patch_plan": "Tools.ai.agent_review_patch_plan.cli:main",
    "build_ai_context_pack": "Tools.ai.ai_context_pack.cli:main",
    "build_ai_peer_exchange_packet": "Tools.ai.peer_exchange_packet.cli:main",
    "build_deterministic_recommendations": "Tools.ai.deterministic_recommendations.cli:main",
    "build_code_interpreter_report": "Tools.ai.code_interpreter_report.cli:main",
    "code_product_artifact_intake": "Tools.ai.code_product_artifact_intake.cli:main",
    "build_external_heap_revision_context": "Tools.ai.external_heap_revision_context.cli:main",
    "build_full_toolbox_run_telemetry_summary": "Tools.ai.full_toolbox_telemetry_summary.cli:main",
    "build_heap_runtime_launcher_command": "Tools.ai.heap_runtime_launcher_command.cli:main",
    "build_patch_specs_from_proposals": "Tools.ai.generated_patch_specs.proposal_cli:main",
    "build_refactor_duplication_audit": "Tools.ai.refactor_duplication_audit.cli:main",
    "build_repository_change_proposals": "Tools.ai.repository_change_proposals.cli:main",
    "build_runtime_flow_map": "Tools.ai.runtime_flow_map.cli:main",
    "build_runtime_tool_usage_telemetry": "Tools.ai.runtime_tool_usage_telemetry.cli:main",
    "build_selective_execution_plan": "Tools.ai.selective_execution_plan.cli:main",
    "build_semantic_evidence_chunks": "Tools.ai.semantic_evidence_chunks.cli:main",
    "build_shared_toolbox_ai_to_ai_bundle": "Tools.ai.shared_toolbox_bundle.cli:main",
    "compose_heap_final_proposals": "Tools.ai.heap_final_proposals.cli:main",
    "ollama_tool_gateway": "Tools.ai.ollama_tool_gateway.cli:main",
    "operator_product_gui": "Tools.ai.operator_product_view.cli:main",
    "prepare_heap_context_memory_reload": "Tools.ai.heap_context_memory_reload.cli:main",
    "prepare_review_pr": "Tools.ai.agent_review.review_pr_cli:main",
    "promote_patch_spec_draft": "Tools.ai.generated_patch_specs.review_cli:main",
    "provider_runtime_heap": "Tools.ai.provider_runtime_blackboard.cli:main",
    "refine_megalithic_review_signals": "Tools.ai.megalithic_review_refinement.cli:main",
    "run_agent_gpu_deep_planning_review": "Tools.ai.gpu_deep_planning_review.cli:main",
    "run_agent_gpu_deep_planning_supervised": "Tools.ai.gpu_deep_planning_supervised.cli:main",
    "run_agent_gpu_npu_parallel_orchestrator": "Tools.ai.gpu_npu_parallel_orchestrator.cli:main",
    "run": "Tools.ai.run.cli:main",
    "run_megalithic_repo_review": "Tools.ai.megalithic_repo_review.cli:main",
    "run_npu_gpu_deep_review_auditor": "Tools.ai.npu_gpu_deep_review_auditor.cli:main",
    "run_pipeline_dry_run_matrix": "Tools.ai.pipeline_dry_run_matrix.cli:main",
    "suggest_repository_updates": "Tools.ai.repository_update_suggestions.cli:main",
}


def _dispatcher() -> ToolDispatcher:
    return ToolDispatcher(
        package="Tools.ai",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="AI",
    )


def available_tools() -> list[str]:
    return _dispatcher().discovered_tools()


def resolve_tool(raw_name: str):
    return _dispatcher().resolve_tool(raw_name)


def main(argv: list[str] | None = None) -> int:
    return _dispatcher().main(argv)
