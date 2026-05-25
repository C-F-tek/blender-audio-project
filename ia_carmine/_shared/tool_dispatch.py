"""Reusable dispatcher for IA-Carmine command surfaces."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path
from typing import Callable

ToolMain = Callable[[], int | None]
HIDDEN_TOOL_SUFFIXES = ("_cli", "_core", "_view", "_model", "_controller")
PUBLIC = "public"
COMPAT = "compat"
INTERNAL = "internal"
VISIBLE_STATES = {PUBLIC, COMPAT, INTERNAL}
ALLOW_INTERNAL_ENV = "IA_CARMINE_ALLOW_INTERNAL_DISPATCH"
ALLOW_COMPAT_ENV = "IA_CARMINE_ALLOW_COMPAT_DISPATCH"


class ToolDispatcher:
    """Resolve named tool CLIs from an explicit registry."""

    def __init__(
        self,
        *,
        package: str,
        package_dir: Path,
        targets: dict[str, str],
        label: str,
        display_package: str | None = None,
        visibility: dict[str, str] | None = None,
        default_visibility: str = PUBLIC,
    ) -> None:
        self.package = package
        self.display_package = display_package or package
        self.package_dir = package_dir
        self.targets = targets
        self.label = label
        if default_visibility not in VISIBLE_STATES:
            raise ValueError(f"invalid default dispatcher visibility: {default_visibility}")
        self.default_visibility = default_visibility
        self.visibility = {
            name: state
            for name, state in (visibility or {}).items()
            if state in VISIBLE_STATES
        }
        repo_root = package_dir.parents[1]
        for path in (repo_root, package_dir):
            path_text = str(path)
            if path_text not in sys.path:
                sys.path.insert(0, path_text)

    @staticmethod
    def normalize_tool_name(raw_name: str) -> str:
        name = Path(raw_name).name
        if name.endswith(".py"):
            name = name[:-3]
        if name.endswith(".ps1"):
            name = name[:-4]
        return name.strip().replace("-", "_")

    def discovered_tools(self) -> list[str]:
        return sorted(self.targets)

    def tool_visibility(self, name: str) -> str:
        return self.visibility.get(name, self.default_visibility)

    def public_tools(self) -> list[str]:
        return [
            name
            for name in self.discovered_tools()
            if self.tool_visibility(name) == PUBLIC
        ]

    def visible_tools(self) -> list[str]:
        allow_compat = os.environ.get(ALLOW_COMPAT_ENV) == "1"
        allow_internal = os.environ.get(ALLOW_INTERNAL_ENV) == "1"
        tools: list[str] = []
        for name in self.discovered_tools():
            state = self.tool_visibility(name)
            if state == PUBLIC or (state == COMPAT and allow_compat) or allow_internal:
                tools.append(name)
        return tools

    def _tool_allowed(self, name: str) -> tuple[bool, str]:
        state = self.tool_visibility(name)
        if state == PUBLIC:
            return True, ""
        if state == COMPAT and os.environ.get(ALLOW_COMPAT_ENV) == "1":
            return True, ""
        if os.environ.get(ALLOW_INTERNAL_ENV) == "1":
            return True, ""
        return (
            False,
            f"{name} is {state}; use the canonical public command or set "
            f"{ALLOW_INTERNAL_ENV}=1 for controlled validation/internal execution",
        )

    def _resolve_powershell_tool(
        self,
        *,
        name: str,
        script_name: str,
        tool_args: list[str],
    ) -> ToolMain:
        script_path = self.package_dir / script_name

        def run_powershell_tool() -> int:
            if tool_args and tool_args[0] in {"--help", "-h"}:
                print(f"Usage: python -m {self.display_package} {name} [native PowerShell args...]")
                print(f"Implementation: {script_path.relative_to(self.package_dir.parents[1])}")
                return 0
            env = os.environ.copy()
            env["IA_CARMINE_TOOL_DISPATCHER"] = self.package
            command = [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script_path),
                *tool_args,
            ]
            return subprocess.call(command, cwd=str(self.package_dir.parents[1]), env=env)

        return run_powershell_tool

    def resolve_tool(self, raw_name: str, tool_args: list[str] | None = None) -> ToolMain:
        name = self.normalize_tool_name(raw_name)
        target = self.targets.get(name)
        if target is None:
            if name.endswith(HIDDEN_TOOL_SUFFIXES):
                raise AttributeError(f"'{name}' is an internal implementation module")
            raise AttributeError(f"'{name}' is not registered in dispatcher")
        allowed, reason = self._tool_allowed(name)
        if not allowed:
            raise PermissionError(reason)
        if target.startswith("ps1:"):
            return self._resolve_powershell_tool(
                name=name,
                script_name=target.removeprefix("ps1:"),
                tool_args=list(tool_args or []),
            )
        module_name, function_name = target.split(":", 1)
        module = importlib.import_module(module_name)
        return getattr(module, function_name)

    def main(self, argv: list[str] | None = None) -> int:
        args = list(sys.argv[1:] if argv is None else argv)
        usage = f"python -m {self.display_package} <tool> [tool args...]"
        if not args or args[0] in {"--help", "-h"}:
            print(f"Usage: {usage}")
            print(f"Public {self.label} tools:")
            for tool in self.public_tools():
                print(f"  {tool}")
            print(
                f"Internal/compat tools are hidden; set {ALLOW_INTERNAL_ENV}=1 "
                "for controlled validation/internal execution."
            )
            return 0
        if args[0] == "--list":
            for tool in self.public_tools():
                print(tool)
            return 0
        if args[0] == "--list-visible":
            for tool in self.visible_tools():
                print(tool)
            return 0
        if args[0] == "--list-all":
            for tool in self.discovered_tools():
                print(tool)
            return 0

        raw_tool = args[0]
        tool_args = args[1:]
        try:
            tool_main = self.resolve_tool(raw_tool, tool_args)
        except (AttributeError, ImportError, ModuleNotFoundError, PermissionError) as exc:
            print(f"Unknown {self.label} tool '{raw_tool}': {exc}", file=sys.stderr)
            return 2

        name = self.normalize_tool_name(raw_tool)
        sys.argv = [f"python -m {self.display_package} {name}", *tool_args]
        result = tool_main()
        return int(result or 0)
