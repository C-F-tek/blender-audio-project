"""Central dispatcher for repository patch-runner tools."""

from pathlib import Path

from ia_carmine._shared.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {
    "apply_repo_mods": "Tools.repo_patch_runner.apply_repo_mods.cli:main",
}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.repo_patch_runner",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="repo patch-runner",
    ).main(argv)
