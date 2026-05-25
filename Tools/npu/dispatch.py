"""Retired NPU dispatcher surface.

NPU/provider behavior is selected through the canonical run or broker helper
with explicit flags. This dispatcher intentionally exposes no direct tools.
"""

from pathlib import Path

from ia_carmine._shared.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {}
TOOL_VISIBILITY: dict[str, str] = {}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.npu",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="NPU",
        visibility=TOOL_VISIBILITY,
    ).main(argv)
