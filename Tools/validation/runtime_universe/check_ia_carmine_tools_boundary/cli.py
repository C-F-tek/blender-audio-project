"""Check that ia_carmine core code does not depend on Tools internals."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    violations: list[dict[str, Any]] = []
    warnings: list[str] = []
    checked = 0
    for path in sorted((repo_root / "ia_carmine").rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        checked += 1
        violations.extend(_scan_file(repo_root, path))
    hard = [item for item in violations if item.get("classification") == "hard_violation"]
    report = {
        "schema_version": 1,
        "kind": "ia_carmine_tools_boundary_check",
        "passed": not hard,
        "repo_root": str(repo_root),
        "checked_file_count": checked,
        "violation_count": len(hard),
        "allowed_temporary_exception_count": 0,
        "violations": hard,
        "allowed_temporary_exceptions": [],
        "warnings": warnings,
        "errors": [f"{item['path']}:{item['line']}: {item['import']}" for item in hard],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    _write_report(repo_root, args.output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def _scan_file(repo_root: Path, path: Path) -> list[dict[str, Any]]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    except SyntaxError as exc:
        return [
            {
                "path": _rel(repo_root, path),
                "line": exc.lineno or 0,
                "import": "syntax_error",
                "classification": "hard_violation",
                "reason": str(exc),
            }
        ]
    found: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if _is_tools_import(name):
                    found.append(_entry(repo_root, path, node.lineno, name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if _is_tools_import(module):
                found.append(_entry(repo_root, path, node.lineno, module))
        elif isinstance(node, ast.Call):
            name = _dynamic_tools_import_name(node)
            if name:
                found.append(_entry(repo_root, path, node.lineno, name))
    return found


def _entry(repo_root: Path, path: Path, line: int, import_name: str) -> dict[str, Any]:
    return {
        "path": _rel(repo_root, path),
        "line": line,
        "import": import_name,
        "classification": "hard_violation",
        "reason": "ia_carmine core must not import Tools",
    }


def _is_tools_import(name: str) -> bool:
    return name == "Tools" or name.startswith("Tools.")


def _dynamic_tools_import_name(node: ast.Call) -> str:
    if not node.args:
        return ""
    func = node.func
    is_import_module = (
        isinstance(func, ast.Attribute)
        and func.attr == "import_module"
        and isinstance(func.value, ast.Name)
        and func.value.id == "importlib"
    )
    is_dunder_import = isinstance(func, ast.Name) and func.id == "__import__"
    if not (is_import_module or is_dunder_import):
        return ""
    first = node.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value if _is_tools_import(first.value) else ""
    return ""


def _write_report(repo_root: Path, output: str, report: dict[str, Any]) -> None:
    if not output:
        return
    path = Path(output)
    if not path.is_absolute():
        path = repo_root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
