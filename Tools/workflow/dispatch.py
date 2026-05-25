"""Retired workflow dispatcher surface.

Workflow wrappers are no longer public or internal command surfaces. Operator
runs must enter through ``python -m ia_carmine.cli run`` with explicit flags;
validators, smoke tests and helper calls use their canonical dispatchers.
"""

from pathlib import Path

from ia_carmine._shared.tool_dispatch import ToolDispatcher

TOOL_MAIN_TARGETS: dict[str, str] = {}
TOOL_VISIBILITY: dict[str, str] = {}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.workflow",
        package_dir=Path(__file__).resolve().parent,
        targets=TOOL_MAIN_TARGETS,
        label="workflow",
        visibility=TOOL_VISIBILITY,
    ).main(argv)
