"""Reusable dispatcher for ``python -m Tools.<area> <tool>`` entrypoints."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path
from typing import Callable

ToolMain = Callable[[], int | None]
HIDDEN_TOOL_SUFFIXES = ("_cli", "_core", "_view", "_model", "_controller")


class ToolDispatcher:
    """Resolve named tool CLIs from an explicit registry with package fallback."""

    def __init__(
        self,
        *,
        package: str,
        package_dir: Path,
        targets: dict[str, str],
        label: str,
    ) -> None:
        self.package = package
        self.package_dir = package_dir
        self.targets = targets
        self.label = label
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

    @staticmethod
    def _file_exposes_main(path: Path) -> bool:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return False
        return (
            "def main(" in text
            or "def main()" in text
            or "main =" in text
            or "import main" in text
        )

    def discovered_tools(self) -> list[str]:
        names = set(self.targets)
        for path in self.package_dir.glob("*.py"):
            if path.name in {"__init__.py", "__main__.py", "dispatch.py"}:
                continue
            if path.stem.endswith(HIDDEN_TOOL_SUFFIXES):
                continue
            if self._file_exposes_main(path):
                names.add(path.stem)
        for path in self.package_dir.iterdir():
            if not path.is_dir() or path.name.startswith("__"):
                continue
            if path.name.endswith(HIDDEN_TOOL_SUFFIXES):
                continue
            init = path / "__init__.py"
            cli = path / "cli.py"
            if self._file_exposes_main(init) or self._file_exposes_main(cli):
                names.add(path.name)
        return sorted(names)

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
                print(f"Usage: python -m {self.package} {name} [native PowerShell args...]")
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
            package_cli = self.package_dir / name / "cli.py"
            if self._file_exposes_main(package_cli):
                target = f"{self.package}.{name}.cli:main"
            else:
                target = f"{self.package}.{name}:main"
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
        usage = f"python -m {self.package} <tool> [tool args...]"
        if not args or args[0] in {"--help", "-h"}:
            print(f"Usage: {usage}")
            print(f"Available {self.label} tools:")
            for tool in self.discovered_tools():
                print(f"  {tool}")
            return 0
        if args[0] == "--list":
            for tool in self.discovered_tools():
                print(tool)
            return 0

        raw_tool = args[0]
        tool_args = args[1:]
        try:
            tool_main = self.resolve_tool(raw_tool, tool_args)
        except (AttributeError, ImportError, ModuleNotFoundError) as exc:
            print(f"Unknown {self.label} tool '{raw_tool}': {exc}", file=sys.stderr)
            return 2

        name = self.normalize_tool_name(raw_tool)
        sys.argv = [f"python -m {self.package} {name}", *tool_args]
        result = tool_main()
        return int(result or 0)
