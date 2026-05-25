"""Central dispatcher for IA-Carmine Core Runtime tools.

Use ``python -m ia_carmine.cli <tool> ...`` so each tool owns its implementation
in a dedicated package while the operator still has one predictable command
surface.
"""

from pathlib import Path

from ia_carmine._shared.tool_dispatch import INTERNAL, PUBLIC, ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {
    "agent_memory_routing_policy": "ia_carmine.memory.agent_memory.routing_cli:main",
    "agent_runtime_sqlite_memory": "ia_carmine.memory.agent_memory.sqlite_cli:main",
    "runtime_sqlite_memory": "ia_carmine.memory.agent_memory.sqlite_cli:main",
    "gpu_npu_run_sync_analysis": "ia_carmine.providers.provider_mesh.gpu_npu_run_sync_analysis.cli:main",
    "apply_patch_bundle": "ia_carmine.product.patchkit.apply_patch_bundle:main",
    "generated_patch_specs_apply": "ia_carmine.product.generated_patch_specs.apply_cli:main",
    "build_dry_run_matrix_evidence_bundle": "ia_carmine.product.pipeline.dry_run_matrix.evidence_cli:main",
    "build_patch_notes_quality_product": "ia_carmine.product.patch_product.patch_notes_quality_product.cli:main",
    "build_repository_consistency_map": "ia_carmine.product.repository_product.repository_consistency_map.cli:main",
    "heap_exchange_closure_audit": "ia_carmine.runtime.heap_exchange.closure_audit.cli:main",
    "heap_exchange_runtime_entry": "ia_carmine.runtime.heap_exchange.runtime_entry.cli:main",
    "heap_exchange_runtime_exit": "ia_carmine.runtime.heap_exchange.runtime_exit.cli:main",
    "heap_exchange_peer_runtime_manifest": "ia_carmine.runtime.heap_exchange.peer_runtime_manifest.cli:main",
    "heap_exchange_task_ingress_contract": "ia_carmine.runtime.heap_exchange.task_ingress_contract.cli:main",
    "build_agent_agnostic_tool_inventory": "ia_carmine.context.agent_context.agnostic_tool_inventory.cli:main",
    "build_agent_memory_inventory": "ia_carmine.context.agent_context.memory_inventory.cli:main",
    "build_agent_state_packet": "ia_carmine.context.agent_context.state_packet.cli:main",
    "build_agent_transient_request_context": "ia_carmine.context.agent_context.transient_request_context.cli:main",
    "agent_review_code_patch_plan": "ia_carmine.product.agent_review.code_patch_plan_cli:main",
    "agent_review_evidence_sufficiency": "ia_carmine.product.agent_review.evidence_cli:main",
    "agent_review_patch_bundle": "ia_carmine.product.agent_review.patch_bundle_cli:main",
    "agent_review_patch_plan": "ia_carmine.product.agent_review.patch_plan.cli:main",
    "agent_review_warning_policy": "ia_carmine.product.agent_review.warning_policy.cli:main",
    "peer_exchange_packet": "ia_carmine.providers.provider_mesh.peer_exchange_packet.cli:main",
    "deterministic_recommendations": "ia_carmine.product.deterministic_recommendations.cli:main",
    "build_code_interpreter_report": "ia_carmine.product.code_product.interpreter_report.cli:main",
    "build_code_edit_proposal_from_plan": "ia_carmine.product.code_product.edit_proposal_from_plan.cli:main",
    "build_code_patch_artifact_pack": "ia_carmine.product.code_product.patch_artifact_pack.cli:main",
    "build_code_patch_docs_followup": "ia_carmine.product.code_product.patch_docs_followup.cli:main",
    "code_product_artifact_intake": "ia_carmine.product.code_product.artifact_intake.cli:main",
    "build_external_heap_revision_context": "ia_carmine.runtime.external_heap.revision_context.cli:main",
    "generated_patch_specs_from_proposals": "ia_carmine.product.generated_patch_specs.proposal_cli:main",
    "refactor_duplication_audit": "ia_carmine.product.repository_product.refactor_duplication_audit.cli:main",
    "repository_change_proposals": "ia_carmine.product.repository_product.repository_change_proposals.cli:main",
    "runtime_flow_map": "ia_carmine.runtime.runtime_universe.flow_map.cli:main",
    "build_unified_ai_conversation_feed": "ia_carmine.runtime.runtime_universe.unified.ai_conversation_feed.cli:main",
    "build_unified_chain_contract_args": "ia_carmine.runtime.runtime_universe.unified.chain_contract_args.cli:main",
    "build_unified_raw_debug_good_info_feed": "ia_carmine.runtime.runtime_universe.unified.raw_debug_good_info_feed.cli:main",
    "build_unified_run_observer_snapshot": "ia_carmine.runtime.runtime_universe.unified.run_observer_snapshot.cli:main",
    "selective_execution_plan": "ia_carmine.runtime.runtime_universe.selective_execution_plan.cli:main",
    "semantic_evidence_chunks": "ia_carmine.context.agent_context.semantic_evidence_chunks.cli:main",
    "shared_toolbox_bundle": "ia_carmine.context.agent_context.shared_toolbox_bundle.cli:main",
    "heap_final_proposals": "ia_carmine.product.heap_final_proposals.cli:main",
    "operator_product_gui": "ia_carmine.product.operator_product_core.view.cli:main",
    "heap_context_memory_reload": "ia_carmine.context.heap_context_memory_reload.cli:main",
    "agent_review_prepare_pr": "ia_carmine.product.agent_review.review_pr_cli:main",
    "generated_patch_specs_promote_draft": "ia_carmine.product.generated_patch_specs.review_cli:main",
    "provider_runtime_blackboard": "ia_carmine.runtime.provider_runtime_blackboard.cli:main",
    "provider_runtime_broker_bridge": "ia_carmine.runtime.provider_runtime_blackboard.broker_bridge.cli:main",
    "provider_runtime_live_signals": "ia_carmine.runtime.provider_runtime_blackboard.live_signals.cli:main",
    "provider_runtime_validation_bridge": "ia_carmine.runtime.provider_runtime_blackboard.validation_bridge.cli:main",
    "build_provider_runtime_heap_from_peer_reports": "ia_carmine.runtime.provider_runtime_blackboard.peer_reports.cli:main",
    "megalithic_review_refinement": "ia_carmine.product.repository_product.megalithic_review_refinement.cli:main",
    "run": "ia_carmine.runtime.run.cli:main",
    "run_heap_code_execution_tool": "ia_carmine.runtime.heap_runtime.code_execution_tool.cli:main",
    "run_heap_code_execution_matrix": "ia_carmine.runtime.heap_runtime.code_execution_tool.cli:main",
    "run_heap_virtual_dev_environment": "ia_carmine.runtime.heap_runtime.virtual_dev_environment.cli:main",
    "generic_write": "ia_carmine.runtime.runtime_tool.generic_write.cli:main",
    "megalithic_repo_review": "ia_carmine.product.repository_product.megalithic_repo_review.cli:main",
    "pipeline_dry_run_matrix": "ia_carmine.product.pipeline.dry_run_matrix.cli:main",
    "run_parallel_artifact_pipeline": "ia_carmine.product.pipeline.artifact_runner.cli:main",
    "agent_runtime_tool_broker": "ia_carmine.runtime.runtime_tool.agent_broker.cli:main",
    "build_analysis_input_bundle": "ia_carmine.providers.provider_mesh.analysis_input_bundle.cli:main",
    "build_external_heap_block_pointer_manifest": "ia_carmine.runtime.external_heap.block_pointer_manifest.cli:main",
    "build_github_evidence_bundle": "ia_carmine.product.repository_product.github_evidence_bundle.cli:main",
    "build_gpu0_companion_task_lane": "ia_carmine.providers.provider_mesh.gpu0_companion_task_lane.cli:main",
    "build_gpu_repair_failure_recommendation": "ia_carmine.providers.provider_mesh.gpu_repair_failure_recommendation.cli:main",
    "build_heap_runtime_product_package": "ia_carmine.runtime.heap_runtime.product_package.cli:main",
    "build_megalithic_review_pr_draft": "ia_carmine.product.repository_product.megalithic_review_pr_draft.cli:main",
    "build_npu_micro_task_companion_report": "ia_carmine.providers.provider_mesh.npu_micro_task_companion_report.cli:main",
    "build_ollama_gpu0_peer_report": "ia_carmine.providers.provider_mesh.ollama_gpu0_peer_report.cli:main",
    "ensure_ollama_role_models": "ia_carmine.providers.ollama.role_models:main",
    "ensure_openvino_npu_model": "ia_carmine.providers.provider_mesh.openvino_npu_model_probe.cli:main",
    "ensure_provider_role_coexistence": "ia_carmine.providers.provider_mesh.provider_role_coexistence.cli:main",
    "build_openvino_hardware_governance_report": "ia_carmine.providers.provider_mesh.openvino_hardware_governance_report.cli:main",
    "build_patch_plan_quality_product_report": "ia_carmine.product.patch_product.patch_plan_quality_product_report.cli:main",
    "build_review_pr_prepare_args": "ia_carmine.product.repository_product.review_pr_prepare_args.cli:main",
    "build_runtime_tool_capability_manifest": "ia_carmine.runtime.runtime_tool.capability_manifest.cli:main",
    "build_task_patch_suggestion_report": "ia_carmine.product.patch_product.task_patch_suggestion_report.cli:main",
    "check_npu_provider_environment": "ia_carmine.providers.provider_mesh.npu_provider_environment_check.cli:main",
    "code_interpreter_report": "ia_carmine.product.code_product.interpreter_report.cli:main",
    "create_task_patch_suggestion_markdown": "ia_carmine.product.patch_product.task_patch_suggestion_markdown.cli:main",
    "enrich_github_evidence_bundle_code_plan": "ia_carmine.product.repository_product.github_evidence_bundle_code_plan_enrichment.cli:main",
    "external_heap_revision_context": "ia_carmine.runtime.external_heap.revision_context.cli:main",
    "github_evidence_bundle_build_github_evidence_bundle_ready": "ia_carmine.product.repository_product.github_evidence_bundle_ready.cli:main",
    "patch_notes_quality_product": "ia_carmine.product.patch_product.patch_notes_quality_product.cli:main",
    "patch_plan_generator": "ia_carmine.product.patch_product.patch_plan_generator.cli:main",
    "patch_plan_quality_product": "ia_carmine.product.patch_product.patch_plan_quality_product.cli:main",
    "patch_suggestion_bundle": "ia_carmine.product.patch_product.patch_suggestion_bundle.cli:main",
    "patch_unified_chain_contract_wiring": "ia_carmine.runtime.runtime_universe.unified_chain_contract_wiring_patch.cli:main",
    "patch_unified_launcher_error_policy": "ia_carmine.runtime.runtime_universe.unified_launcher_error_policy_patch.cli:main",
    "provider_mesh_runtime": "ia_carmine.providers.provider_mesh.runtime.cli:main",
    "replay_gpu_planner_json_contract": "ia_carmine.providers.provider_mesh.gpu_planner_json_contract_replay.cli:main",
    "repository_consistency_map": "ia_carmine.product.repository_product.repository_consistency_map.cli:main",
    "run_external_heap_postrun_package": "ia_carmine.runtime.external_heap.postrun_package.cli:main",
    "external_heap_postrun_package": "ia_carmine.runtime.external_heap.postrun_package.cli:main",
    "run_gpu0_peer_companion_worker": "ia_carmine.providers.provider_mesh.gpu0_peer_companion_worker.cli:main",
    "run_local_provider_probe": "ia_carmine.providers.provider_mesh.local_provider_probe.cli:main",
    "runtime_tool_broker": "ia_carmine.runtime.runtime_tool.broker.cli:main",
    "analyze_code_product_artifact": "ia_carmine.product.code_product.artifact_intake.cli:main",
    "assemble_heap_final_readable_product": "ia_carmine.product.code_product.final_readable_product.cli:main",
    "build_full_context_golden_proposals": "ia_carmine.context.agent_context.full_context_golden_proposals.cli:main",
    "build_local_ai_enrichment_plan": "ia_carmine.context.agent_context.local_ai_enrichment_plan.cli:main",
    "build_music_intermediates": "ia_carmine.context.agent_context.music_intermediates.cli:main",
    "build_workload_quality_lane_routing": "ia_carmine.product.ai_workload.quality_lane_routing.cli:main",
    "check_local_resource_lanes": "ia_carmine.providers.provider_mesh.local_resource_lanes_check.cli:main",
    "compose_external_heap_block_response": "ia_carmine.runtime.external_heap.block_response.cli:main",
    "ensure_ai_context_required_files": "ia_carmine.context.agent_context.ensure_required_files.cli:main",
    "evidence_to_recommendation": "ia_carmine.product.deterministic_recommendations.evidence_to_recommendation.cli:main",
    "heap_event_pointers": "ia_carmine.runtime.heap_runtime.event_pointers.cli:main",
    "heap_provider_budget_governor": "ia_carmine.runtime.heap_provider.budget_governor.cli:main",
    "heap_provider_invocation_contract": "ia_carmine.runtime.heap_provider.invocation_contract.cli:main",
    "merge_ai_candidates": "ia_carmine.context.agent_context.merge_candidates.cli:main",
    "normalize_heap_final_causality": "ia_carmine.product.heap_final_proposals.normalize_final_causality.cli:main",
    "operator_product_view": "ia_carmine.product.operator_product_core.view.cli:main",
    "patch_unified_heap_exchange_lifecycle_wiring": "ia_carmine.runtime.heap_exchange.unified_lifecycle_wiring_patch.cli:main",
    "reconcile_heap_report_with_startup_reload": "ia_carmine.context.heap_context_memory_reload.reconcile_report.cli:main",
    "review_agent_memory": "ia_carmine.memory.agent_memory.review.cli:main",
    "review_wave_entrypoints": "ia_carmine.product.agent_review.wave_entrypoints.cli:main",
    "run_agent_review_decision_loop": "ia_carmine.product.agent_review.decision_loop_runner.cli:main",
    "run_provider_runtime_heap_gpu_peer_smoke": "ia_carmine.runtime.provider_runtime_blackboard.gpu_peer_smoke.cli:main",
    "select_semantic_code_chunks": "ia_carmine.context.agent_context.semantic_evidence_chunks.select_code_chunks.cli:main",
    "smart_ai_gatekeeper": "ia_carmine.runtime.runtime_universe.smart_gatekeeper.cli:main",
    "synthesize_patch_candidates": "ia_carmine.product.patch_product.candidate_synthesis.cli:main",
    "validate_ai_artifacts": "ia_carmine.product.pipeline.validate_ai_artifacts.cli:main",
    "validation_step": "ia_carmine.product.pipeline.validation_step.cli:main",
    "agent_runtime_debug_lab": "ia_carmine.runtime.runtime_tool.agent_runtime_debug_lab.cli:main",
    "full_run_bundle_zip": "ia_carmine.product.code_product.full_run_bundle_zip.cli:main",
    "runtime_file_refs": "ia_carmine.runtime.runtime_tool.file_refs.cli:main",
    "runtime_file_window": "ia_carmine.runtime.runtime_tool.file_window.cli:main",
    "runtime_hardware_capability": "ia_carmine.providers.provider_mesh.hardware_capability.cli:main",
}

LEGACY_NON_RUN_UNICA_COMMANDS: frozenset[str] = frozenset()
TOOL_VISIBILITY: dict[str, str] = {name: INTERNAL for name in TOOL_MAIN_TARGETS}
TOOL_VISIBILITY.update(
    {
        "run": PUBLIC,
        "runtime_tool_broker": PUBLIC,
    }
)


def _dispatcher() -> ToolDispatcher:
    return ToolDispatcher(
        package="ia_carmine",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="AI",
        display_package="ia_carmine.cli",
        visibility=TOOL_VISIBILITY,
        default_visibility=INTERNAL,
    )


def available_tools() -> list[str]:
    return _dispatcher().public_tools()


def resolve_tool(raw_name: str):
    return _dispatcher().resolve_tool(raw_name)


def main(argv: list[str] | None = None) -> int:
    return _dispatcher().main(argv)
