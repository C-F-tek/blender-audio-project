"""Central dispatcher for documentation hygiene tools.

Use ``python -m Tools.docs <tool> ...`` instead of launching scripts by file
path. Packaged tools resolve to focused CLI modules; remaining maintained tools
fall back to ``Tools.docs.<tool>:main``.
"""

from pathlib import Path

from Tools.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {
    "build_code_aware_md_coherence": "Tools.docs._shared.code_aware_md_coherence_cli:main",
    "apply_md_code_coherence_refactor": "Tools.docs.docs_hygiene.md_code_coherence_refactor_core.cli:main",
    "build_repo_hygiene_plan": "Tools.docs._shared.repo_hygiene_plan_cli:main",
    "promote_root_tool_package": "Tools.docs.docs_hygiene.promote_root_tool_package:main",
    "refactor_markdown_splits": "Tools.docs._shared.refactor_markdown_splits_cli:main",
    "repo_tool_surface_audit": "Tools.docs.docs_hygiene.repo_tool_surface_audit.cli:main",
    "rewrite_legacy_tool_invocations": "Tools.docs.docs_hygiene.rewrite_legacy_tool_invocations:main",
    "split_large_markdown": "Tools.docs._shared.split_large_markdown_cli:main",
    "tool_package_family_audit": "Tools.docs.docs_hygiene.tool_package_family_audit.cli:main",
    "tool_root_inventory": "Tools.docs.docs_hygiene.tool_root_inventory.cli:main",
    "code_aware_md_coherence_render": "Tools.docs.docs_hygiene.code_aware_md_coherence_render.cli:main",
    "code_aware_md_refs": "Tools.docs.docs_hygiene.code_aware_md_refs.cli:main",
    "markdown_split_tool_guide": "Tools.docs.docs_hygiene.markdown_split_tool_guide.cli:main",
    "md_code_coherence_refactor_core": "Tools.docs.docs_hygiene.md_code_coherence_refactor_core.cli:main",
    "module_duplication_audit": "Tools.docs.docs_hygiene.module_duplication_audit.cli:main",
    "move_tool_package": "Tools.docs.docs_hygiene.tool_package_move.cli:main",
}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.docs",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="documentation",
    ).main(argv)
