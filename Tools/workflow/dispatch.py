"""Central dispatcher for workflow tools.

Use ``python -m Tools.workflow <tool> ...`` instead of launching scripts by
file path. This keeps workflow entrypoints discoverable while implementations
can live in focused packages.
"""

from pathlib import Path

from Tools.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {
    "analyze_audio": "Tools.workflow.workflow_run.audio_analysis.analyze_cli:main",
    "audio_summary": "Tools.workflow.workflow_run.audio_analysis.summary_cli:main",
    "heap_exchange_review_bridge": "ps1:_powershell/heap_exchange_review_bridge.ps1",
    "install_weekly_local_ai_reset_task": "ps1:_powershell/install_weekly_local_ai_reset_task.ps1",
    "repair_full_toolbox_datastamp_doc": "ps1:_powershell/repair_full_toolbox_datastamp_doc.ps1",
    "run_agent_review_full_toolbox_decision_loop": (
        "Tools.workflow.run_agent_review_full_toolbox_decision_loop:main"
    ),
    "run_agent_review_full_toolbox_decision_loop_integrated": (
        "ps1:_powershell/run_agent_review_full_toolbox_decision_loop_integrated.ps1"
    ),
    "run_ai_cycle_startup_preflight": "ps1:_powershell/run_ai_cycle_startup_preflight.ps1",
    "run_docs_md_refactor_10min": "ps1:_powershell/run_docs_md_refactor_10min.ps1",
    "run_full_memory_tool_regeneration": "ps1:_powershell/run_full_memory_tool_regeneration.ps1",
    "run_local_ai_core_tool_activation": "ps1:_powershell/run_local_ai_core_tool_activation.ps1",
    "run_local_ai_markdown_task": "ps1:_powershell/run_local_ai_markdown_task.ps1",
    "run_local_ai_task_via_pipeline": "ps1:_powershell/run_local_ai_task_via_pipeline.ps1",
    "run_local_validation_after_refactor": "ps1:_powershell/run_local_validation_after_refactor.ps1",
    "run_npu_pipeline_helper_validation": "ps1:_powershell/run_npu_pipeline_helper_validation.ps1",
    "run_parallel_ai_provider_multistep": "ps1:_powershell/run_parallel_ai_provider_multistep.ps1",
    "run_post_validation_ai_packet": "ps1:_powershell/run_post_validation_ai_packet.ps1",
    "run_unified_local_ai_refactor": "ps1:_powershell/run_unified_local_ai_refactor.ps1",
    "run_unified_real_product_pr": "ps1:_powershell/run_unified_real_product_pr.ps1",
    "scene_spec": "Tools.workflow.workflow_run.scene_spec.cli:main",
    "smart_ai_context": "Tools.workflow.workflow_run.smart_ai_context_core.cli:main",
    "start_workflow": "ps1:_powershell/start_workflow.ps1",
    "startup_check": "Tools.workflow.workflow_run.startup_check_core.cli:main",
    "startup_preflight": "ps1:_powershell/startup_preflight.ps1",
    "unified_phase_visibility": "ps1:_powershell/unified_phase_visibility.ps1",
    "unified_run_observer": "ps1:_powershell/unified_run_observer.ps1",
    "watch_unified_ai_conversation": "ps1:_powershell/watch_unified_ai_conversation.ps1",
    "watch_unified_ai_public_exchange": "ps1:_powershell/watch_unified_ai_public_exchange.ps1",
    "watch_unified_raw_debug_good_info": "ps1:_powershell/watch_unified_raw_debug_good_info.ps1",
    "watch_unified_run_telemetry": "ps1:_powershell/watch_unified_run_telemetry.ps1",
    "workflow_debug": "Tools.workflow.workflow_run.workflow_debug_core.cli:main",
    "workflow_gui": "Tools.workflow.gui.workflow_gui:main",
    "gui": "Tools.workflow.gui.workflow_gui:main",
    "workflow_shell": "Tools.workflow.workflow_run.workflow_shell.cli:main",
    "workflow_shell_with_push": "Tools.workflow.workflow_run.workflow_shell_with_push.cli:main",
    "ai_runtime_diagnostics": "Tools.workflow.workflow_run.ai_runtime_diagnostics.cli:main",
    "git_auto_push": "Tools.workflow.workflow_run.git_auto_push.cli:main",
    "run_local_ai_artifact_reset": "Tools.workflow.workflow_run.local_ai_artifact_reset.cli:main",
    "smart_ai_context_core": "Tools.workflow.workflow_run.smart_ai_context_core.cli:main",
    "startup_check_core": "Tools.workflow.workflow_run.startup_check_core.cli:main",
    "workflow_debug_core": "Tools.workflow.workflow_run.workflow_debug_core.cli:main",
}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.workflow",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="workflow",
    ).main(argv)
