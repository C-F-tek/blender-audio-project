"""Central dispatcher for NPU tools.

Use ``python -m Tools.npu <tool> ...`` instead of launching scripts by file
path. Packaged tools resolve to their package CLIs; remaining maintained tools
fall back to ``Tools.npu.<tool>:main``.
"""

from pathlib import Path

from Tools.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {
    "build_music_context": "Tools.npu.music_context.cli:main",
    "build_npu_knowledge_broker_packet": "Tools.npu.npu_knowledge_broker_packet.cli:main",
    "build_project_ai_index": "Tools.npu.project_ai_index.cli:main",
    "npu_guardrail_service": "Tools.npu.npu_guardrail.cli:main",
    "run_dual_ai_pipeline": "Tools.npu.dual_ai_pipeline.cli:main",
    "run_npu_context": "ps1:_powershell/run_npu_context.ps1",
    "run_npu_review": "Tools.npu.npu_review_runner.cli:main",
}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.npu",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="NPU",
    ).main(argv)
