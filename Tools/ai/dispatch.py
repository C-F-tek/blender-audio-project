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
    "gpu_npu_run_sync_analysis": "Tools.ai.provider_mesh.gpu_npu_run_sync_analysis.cli:main",
    "apply_patch_bundle": "Tools.ai.patchkit.apply_patch_bundle:main",
    "generated_patch_specs_apply": "Tools.ai.generated_patch_specs.apply_cli:main",
    "build_dry_run_matrix_evidence_bundle": "Tools.ai.pipeline.dry_run_matrix.evidence_cli:main",
    "build_patch_notes_quality_product": "Tools.ai.patch_product.patch_notes_quality_product.cli:main",
    "build_repository_consistency_map": "Tools.ai.repository_product.repository_consistency_map.cli:main",
    "heap_exchange_closure_audit": "Tools.ai.heap_exchange.closure_audit.cli:main",
    "heap_exchange_runtime_entry": "Tools.ai.heap_exchange.runtime_entry.cli:main",
    "heap_exchange_runtime_exit": "Tools.ai.heap_exchange.runtime_exit.cli:main",
    "heap_exchange_peer_runtime_manifest": "Tools.ai.heap_exchange.peer_runtime_manifest.cli:main",
    "heap_exchange_task_ingress_contract": "Tools.ai.heap_exchange.task_ingress_contract.cli:main",
    "build_agent_agnostic_tool_inventory": "Tools.ai.agent_context.agnostic_tool_inventory.cli:main",
    "build_agent_memory_inventory": "Tools.ai.agent_context.memory_inventory.cli:main",
    "build_agent_state_packet": "Tools.ai.agent_context.state_packet.cli:main",
    "build_agent_transient_request_context": "Tools.ai.agent_context.transient_request_context.cli:main",
    "agent_review_code_patch_plan": "Tools.ai.agent_review.code_patch_plan_cli:main",
    "agent_review_evidence_sufficiency": "Tools.ai.agent_review.evidence_cli:main",
    "agent_review_patch_bundle": "Tools.ai.agent_review.patch_bundle_cli:main",
    "agent_review_patch_plan": "Tools.ai.agent_review.patch_plan.cli:main",
    "agent_review_warning_policy": "Tools.ai.agent_review.warning_policy.cli:main",
    "ai_context_pack": "Tools.ai.ai_context_pack.cli:main",
    "peer_exchange_packet": "Tools.ai.peer_exchange_packet.cli:main",
    "deterministic_recommendations": "Tools.ai.deterministic_recommendations.cli:main",
    "build_code_interpreter_report": "Tools.ai.code_product.interpreter_report.cli:main",
    "build_code_edit_proposal_from_plan": "Tools.ai.code_product.edit_proposal_from_plan.cli:main",
    "build_code_patch_artifact_pack": "Tools.ai.code_product.patch_artifact_pack.cli:main",
    "build_code_patch_docs_followup": "Tools.ai.code_product.patch_docs_followup.cli:main",
    "code_product_artifact_intake": "Tools.ai.code_product.artifact_intake.cli:main",
    "build_external_heap_revision_context": "Tools.ai.external_heap.revision_context.cli:main",
    "full_toolbox_telemetry_summary": "Tools.ai.full_toolbox_telemetry_summary.cli:main",
    "heap_runtime_launcher_command": "Tools.ai.heap_runtime.launcher_command.cli:main",
    "generated_patch_specs_from_proposals": "Tools.ai.generated_patch_specs.proposal_cli:main",
    "refactor_duplication_audit": "Tools.ai.refactor_duplication_audit.cli:main",
    "repository_change_proposals": "Tools.ai.repository_product.repository_change_proposals.cli:main",
    "runtime_flow_map": "Tools.ai.runtime_flow_map.cli:main",
    "build_unified_ai_conversation_feed": "Tools.ai.runtime_universe.unified.ai_conversation_feed.cli:main",
    "build_unified_chain_contract_args": "Tools.ai.runtime_universe.unified.chain_contract_args.cli:main",
    "build_unified_raw_debug_good_info_feed": "Tools.ai.runtime_universe.unified.raw_debug_good_info_feed.cli:main",
    "build_unified_run_observer_snapshot": "Tools.ai.runtime_universe.unified.run_observer_snapshot.cli:main",
    "runtime_tool_usage_telemetry": "Tools.ai.runtime_tool.usage_telemetry.cli:main",
    "selective_execution_plan": "Tools.ai.selective_execution_plan.cli:main",
    "semantic_evidence_chunks": "Tools.ai.semantic_evidence_chunks.cli:main",
    "shared_toolbox_bundle": "Tools.ai.shared_toolbox_bundle.cli:main",
    "heap_final_proposals": "Tools.ai.heap_final_proposals.cli:main",
    "ollama_tool_gateway": "Tools.ai.provider_mesh.ollama_tool_gateway.cli:main",
    "operator_product_gui": "Tools.ai.operator_product_view.cli:main",
    "heap_context_memory_reload": "Tools.ai.heap_context_memory_reload.cli:main",
    "agent_review_prepare_pr": "Tools.ai.agent_review.review_pr_cli:main",
    "generated_patch_specs_promote_draft": "Tools.ai.generated_patch_specs.review_cli:main",
    "provider_runtime_blackboard": "Tools.ai.provider_runtime_blackboard.cli:main",
    "provider_runtime_broker_bridge": "Tools.ai.provider_runtime_blackboard.broker_bridge.cli:main",
    "provider_runtime_live_signals": "Tools.ai.provider_runtime_blackboard.live_signals.cli:main",
    "provider_runtime_validation_bridge": "Tools.ai.provider_runtime_blackboard.validation_bridge.cli:main",
    "build_provider_runtime_heap_from_peer_reports": "Tools.ai.provider_runtime_blackboard.peer_reports.cli:main",
    "build_provider_runtime_heap_telemetry": "Tools.ai.provider_runtime_blackboard.telemetry.cli:main",
    "megalithic_review_refinement": "Tools.ai.repository_product.megalithic_review_refinement.cli:main",
    "gpu_deep_planning_review": "Tools.ai.provider_mesh.gpu_deep_planning_review.cli:main",
    "gpu_deep_planning_supervised": "Tools.ai.provider_mesh.gpu_deep_planning_supervised.cli:main",
    "gpu_npu_parallel_orchestrator": "Tools.ai.provider_mesh.gpu_npu_parallel_orchestrator.cli:main",
    "run": "Tools.ai.run.cli:main",
    "run_heap_code_execution_tool": "Tools.ai.heap_runtime.code_execution_tool.cli:main",
    "run_heap_runtime_completeness_gate": "Tools.ai.heap_runtime.completeness_gate.cli:main",
    "run_heap_virtual_dev_environment": "Tools.ai.heap_runtime.virtual_dev_environment.cli:main",
    "megalithic_repo_review": "Tools.ai.megalithic_repo_review.cli:main",
    "npu_gpu_deep_review_auditor": "Tools.ai.provider_mesh.npu_gpu_deep_review_auditor.cli:main",
    "pipeline_dry_run_matrix": "Tools.ai.pipeline.dry_run_matrix.cli:main",
    "repository_update_suggestions": "Tools.ai.repository_product.repository_update_suggestions.cli:main",
    "run_parallel_artifact_pipeline": "Tools.ai.pipeline.artifact_runner.cli:main",
    "agent_runtime_tool_broker": "Tools.ai.runtime_tool.agent_broker.cli:main",
    "build_analysis_input_bundle": "Tools.ai.provider_mesh.analysis_input_bundle.cli:main",
    "build_external_heap_block_pointer_manifest": "Tools.ai.external_heap.block_pointer_manifest.cli:main",
    "build_github_evidence_bundle": "Tools.ai.repository_product.github_evidence_bundle.cli:main",
    "build_gpu0_companion_task_lane": "Tools.ai.provider_mesh.gpu0_companion_task_lane.cli:main",
    "build_gpu_repair_failure_recommendation": "Tools.ai.provider_mesh.gpu_repair_failure_recommendation.cli:main",
    "build_heap_runtime_product_package": "Tools.ai.heap_runtime.product_package.cli:main",
    "build_megalithic_review_pr_draft": "Tools.ai.repository_product.megalithic_review_pr_draft.cli:main",
    "build_npu_micro_task_companion_report": "Tools.ai.provider_mesh.npu_micro_task_companion_report.cli:main",
    "build_openvino_gpu0_workload_report": "Tools.ai.provider_mesh.openvino_gpu0_workload_report.cli:main",
    "build_openvino_hardware_governance_report": "Tools.ai.provider_mesh.openvino_hardware_governance_report.cli:main",
    "build_patch_plan_quality_product_report": "Tools.ai.patch_product.patch_plan_quality_product_report.cli:main",
    "build_review_pr_prepare_args": "Tools.ai.repository_product.review_pr_prepare_args.cli:main",
    "build_runtime_tool_capability_manifest": "Tools.ai.runtime_tool.capability_manifest.cli:main",
    "build_task_patch_suggestion_report": "Tools.ai.patch_product.task_patch_suggestion_report.cli:main",
    "check_npu_provider_environment": "Tools.ai.provider_mesh.npu_provider_environment_check.cli:main",
    "code_interpreter_report": "Tools.ai.code_product.interpreter_report.cli:main",
    "create_task_patch_suggestion_markdown": "Tools.ai.patch_product.task_patch_suggestion_markdown.cli:main",
    "enrich_github_evidence_bundle_code_plan": "Tools.ai.repository_product.github_evidence_bundle_code_plan_enrichment.cli:main",
    "external_heap_revision_context": "Tools.ai.external_heap.revision_context.cli:main",
    "github_evidence_bundle_build_github_evidence_bundle_ready": "Tools.ai.repository_product.github_evidence_bundle_ready.cli:main",
    "patch_notes_quality_product": "Tools.ai.patch_product.patch_notes_quality_product.cli:main",
    "patch_plan_generator": "Tools.ai.patch_product.patch_plan_generator.cli:main",
    "patch_plan_quality_product": "Tools.ai.patch_product.patch_plan_quality_product.cli:main",
    "patch_suggestion_bundle": "Tools.ai.patch_product.patch_suggestion_bundle.cli:main",
    "patch_unified_chain_contract_wiring": "Tools.ai.runtime_universe.unified_chain_contract_wiring_patch.cli:main",
    "patch_unified_launcher_error_policy": "Tools.ai.runtime_universe.unified_launcher_error_policy_patch.cli:main",
    "provider_mesh_runtime": "Tools.ai.provider_mesh.runtime.cli:main",
    "replay_gpu_planner_json_contract": "Tools.ai.provider_mesh.gpu_planner_json_contract_replay.cli:main",
    "repository_consistency_map": "Tools.ai.repository_product.repository_consistency_map.cli:main",
    "run_external_heap_postrun_package": "Tools.ai.external_heap.postrun_package.cli:main",
    "run_gpu0_peer_companion_worker": "Tools.ai.provider_mesh.gpu0_peer_companion_worker.cli:main",
    "run_local_provider_probe": "Tools.ai.provider_mesh.local_provider_probe.cli:main",
    "run_npu_decode_smoke_diagnostic": "Tools.ai.provider_mesh.npu_decode_smoke_diagnostic.cli:main",
    "runtime_tool_broker": "Tools.ai.runtime_tool.broker.cli:main",
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
