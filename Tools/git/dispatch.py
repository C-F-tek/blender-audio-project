"""Dispatcher for Git tools behind ``python -m Tools.git``."""

from __future__ import annotations

from pathlib import Path

from Tools.tool_dispatch import ToolDispatcher

TARGETS = {
    "auto_push_generated_artifacts": "ps1:_powershell/auto_push_generated_artifacts.ps1",
    "auto_push_generated_data": "ps1:_powershell/auto_push_generated_data.ps1",
}


def main(argv: list[str] | None = None) -> int:
    return ToolDispatcher(
        package="Tools.git",
        package_dir=Path(__file__).resolve().parent,
        targets=TARGETS,
        label="git",
    ).main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
