"""Validate that broker allowlisted tools are real dispatcher tools."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def assignment_value(node: ast.AST, name: str) -> ast.AST | None:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == name:
                return node.value
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        if node.target.id == name:
            return node.value
    return None


def dict_string_keys(value: ast.AST | None) -> list[str]:
    if not isinstance(value, ast.Dict):
        return []
    names: list[str] = []
    for key in value.keys:
        if isinstance(key, ast.Constant) and isinstance(key.value, str):
            names.append(key.value)
    return sorted(names)


def dispatch_targets(path: Path, name: str) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    for node in tree.body:
        value = assignment_value(node, name)
        if not isinstance(value, ast.Dict):
            continue
        targets: dict[str, str] = {}
        for key, item in zip(value.keys, value.values):
            if not (
                isinstance(key, ast.Constant)
                and isinstance(key.value, str)
                and isinstance(item, ast.Constant)
                and isinstance(item.value, str)
            ):
                continue
            targets[key.value] = item.value
        return targets
    return {}


def broker_tool_names(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    for node in tree.body:
        value = assignment_value(node, "TOOL_SPECS")
        if value is not None:
            return dict_string_keys(value)
    return []


def target_module(target: str) -> str:
    return str(target or "").split(":", 1)[0]


def module_available(module: str) -> bool:
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, AttributeError, ValueError):
        return False


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Runtime Tool Broker / Dispatcher Alignment",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Broker tool count: `{report.get('broker_tool_count')}`",
        f"- AI dispatcher tool count: `{report.get('ai_dispatch_tool_count')}`",
        f"- Broker missing AI dispatch count: `{len(report.get('broker_missing_ai_dispatch') or [])}`",
        f"- AI dispatch missing module count: `{len(report.get('ai_dispatch_missing_module') or [])}`",
        "",
        "## Errors",
        "",
    ]
    errors = report.get("errors")
    lines.extend([f"- {item}" for item in errors] if errors else ["- none"])
    lines.extend(["", "## Broker Missing AI Dispatch", ""])
    missing = report.get("broker_missing_ai_dispatch")
    lines.extend([f"- `{item}`" for item in missing] if missing else ["- none"])
    lines.extend(["", "## Missing Dispatcher Modules", ""])
    missing_modules = report.get("ai_dispatch_missing_module")
    lines.extend([f"- `{item}`" for item in missing_modules] if missing_modules else ["- none"])
    return "\n".join(lines) + "\n"


def build_report(repo_root: Path) -> dict[str, Any]:
    ai_dispatch = dispatch_targets(repo_root / "ia_carmine/dispatch.py", "TOOL_MAIN_TARGETS")
    validation_dispatch = dispatch_targets(
        repo_root / "Tools/validation/dispatch.py", "TOOL_MAIN_TARGETS"
    )
    broker_tools = broker_tool_names(repo_root / "ia_carmine/runtime/runtime_tool/broker/registry.py")
    ai_tools = sorted(str(key) for key in ai_dispatch)
    validation_tools = sorted(str(key) for key in validation_dispatch)
    command_dispatch = {**validation_dispatch, **ai_dispatch}
    broker_missing = sorted(name for name in broker_tools if name not in command_dispatch)
    missing_modules = sorted(
        f"{name}: {target}"
        for name, target in command_dispatch.items()
        if not module_available(target_module(str(target)))
    )
    errors = []
    if broker_missing:
        errors.append("broker_allowlisted_tools_missing_ai_dispatch")
    if missing_modules:
        errors.append("ai_dispatch_targets_missing_modules")
    return {
        "schema_version": 1,
        "kind": "runtime_tool_broker_dispatch_alignment",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": not errors,
        "errors": errors,
        "broker_tool_count": len(broker_tools),
        "ai_dispatch_tool_count": len(ai_tools),
        "validation_dispatch_tool_count": len(validation_dispatch),
        "broker_missing_ai_dispatch": sorted(name for name in broker_tools if name not in ai_dispatch),
        "broker_missing_command_dispatch": broker_missing,
        "ai_dispatch_missing_module": missing_modules,
        "dispatcher_missing_broker_allowed_count": len(
            [name for name in sorted(set(ai_tools + validation_tools)) if name not in broker_tools]
        ),
        "broker_tools": broker_tools,
        "source_writes_performed": False,
        "patch_application_performed": False,
        "provider_execution_performed": False,
        "git_write_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output",
        default="output/validation/runtime_tool_broker_dispatch_alignment.json",
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/runtime_tool_broker_dispatch_alignment.md",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = Path(args.output)
    markdown = Path(args.markdown_output)
    if not output.is_absolute():
        output = repo_root / output
    if not markdown.is_absolute():
        markdown = repo_root / markdown
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
