"""Central dispatcher for NPU tools.

Use ``python -m Tools.npu <tool> ...`` instead of launching scripts by file
path. Packaged tools resolve to their package CLIs; remaining maintained tools
fall back to ``Tools.npu.<tool>:main``.
"""

from pathlib import Path

from Tools.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {
    "build_music_context": "Tools.npu.provider_mesh.music_context.cli:main",
    "build_npu_knowledge_broker_packet": "Tools.npu.provider_mesh.npu_knowledge_broker_packet.cli:main",
    "build_project_ai_index": "Tools.npu.provider_mesh.project_ai_index.cli:main",
    "npu_guardrail_service": "Tools.npu.provider_mesh.npu_guardrail.cli:main",
    "run_dual_ai_pipeline": "Tools.npu.dual_ai_pipeline.cli:main",
    "run_npu_context": "ps1:_powershell/run_npu_context.ps1",
    "run_npu_review": "Tools.npu.provider_mesh.npu_review_runner.cli:main",
    "build_ai_service_packet": "Tools.npu.provider_mesh.ai_service_packet.cli:main",
    "build_blender_manual_context": "Tools.npu.provider_mesh.blender_manual_context.cli:main",
    "build_npu_code_context": "Tools.npu.provider_mesh.npu_code_context.cli:main",
    "build_provider_result_report": "Tools.npu.provider_mesh.provider_result_report.cli:main",
    "build_runtime_output_manifest": "Tools.npu.provider_mesh.runtime_output_manifest.cli:main",
    "build_semantic_code_chunks": "Tools.npu.provider_mesh.semantic_code_chunks.cli:main",
    "music_context": "Tools.npu.provider_mesh.music_context.cli:main",
    "npu_guardrail": "Tools.npu.provider_mesh.npu_guardrail.cli:main",
    "npu_knowledge_broker_packet": "Tools.npu.provider_mesh.npu_knowledge_broker_packet.cli:main",
    "npu_review_runner": "Tools.npu.provider_mesh.npu_review_runner.cli:main",
    "project_ai_index": "Tools.npu.provider_mesh.project_ai_index.cli:main",
    "run_npu_artifact_reviewer": "Tools.npu.provider_mesh.npu_artifact_reviewer.cli:main",
    "run_ollama_music_agent": "Tools.npu.provider_mesh.ollama_music_agent.cli:main",
}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.npu",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="NPU",
    ).main(argv)
