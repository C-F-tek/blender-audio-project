#!/usr/bin/env python3
"""Smoke-test provider peer review events scoping in the heap runtime gate.

The 2026-05 heap closure run exposed a runtime crash where
``enrich_provider_report_with_operational_peer_review`` used ``events`` without
receiving it from ``run_provider_teamwork``. This smoke is intentionally static
and bounded: it validates the source-level contract that the peer-review helper
accepts the event list and that the provider teamwork caller passes current heap
events before enriching GPU0/NPU operational reviews.
"""

from __future__ import annotations

import argparse
import ast
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


TARGET = Path("Tools/ai/run_heap_runtime_completeness_gate/cli.py")
LAUNCHER = Path("Tools/ai/run_heap_runtime_context_closure/cli.py")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


class FunctionFinder(ast.NodeVisitor):
    def __init__(self) -> None:
        self.functions: dict[str, ast.FunctionDef] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:  # noqa: N802 - ast API
        self.functions[node.name] = node
        self.generic_visit(node)


def function_arg_names(node: ast.FunctionDef | None) -> list[str]:
    if node is None:
        return []
    return [arg.arg for arg in node.args.args]


def has_read_events_assignment(node: ast.FunctionDef | None) -> bool:
    if node is None:
        return False
    for child in ast.walk(node):
        if not isinstance(child, ast.Assign):
            continue
        target_names = [target.id for target in child.targets if isinstance(target, ast.Name)]
        if "events" not in target_names:
            continue
        value = child.value
        if (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Attribute)
            and value.func.attr == "read_events"
        ):
            return True
    return False


def enrich_call_passes_events(node: ast.FunctionDef | None) -> bool:
    if node is None:
        return False
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        if not isinstance(child.func, ast.Attribute):
            continue
        if child.func.attr != "enrich_provider_report_with_operational_peer_review":
            continue
        if any(isinstance(arg, ast.Name) and arg.id == "events" for arg in child.args):
            return True
        if any(keyword.arg == "events" for keyword in child.keywords):
            return True
    return False


def launcher_summary_exposes_command(node: ast.AST, field_name: str) -> bool:
    for child in ast.walk(node):
        if not isinstance(child, ast.Dict):
            continue
        for key in child.keys:
            if isinstance(key, ast.Constant) and key.value == field_name:
                return True
    return False


def build_report(repo_root: Path) -> dict[str, Any]:
    gate_path = repo_root / TARGET
    launcher_path = repo_root / LAUNCHER
    checks: list[dict[str, Any]] = []
    errors: list[str] = []

    try:
        gate_tree = ast.parse(gate_path.read_text(encoding="utf-8"), filename=str(gate_path))
    except Exception as exc:  # noqa: BLE001 - report syntax failure.
        gate_tree = ast.Module(body=[], type_ignores=[])
        errors.append(f"cannot parse {TARGET}: {type(exc).__name__}: {exc}")

    try:
        launcher_tree = ast.parse(
            launcher_path.read_text(encoding="utf-8"), filename=str(launcher_path)
        )
    except Exception as exc:  # noqa: BLE001 - report syntax failure.
        launcher_tree = ast.Module(body=[], type_ignores=[])
        errors.append(f"cannot parse {LAUNCHER}: {type(exc).__name__}: {exc}")

    finder = FunctionFinder()
    finder.visit(gate_tree)
    enrich_fn = finder.functions.get("enrich_provider_report_with_operational_peer_review")
    provider_fn = finder.functions.get("run_provider_teamwork")
    enrich_args = function_arg_names(enrich_fn)

    checks.append(
        {
            "name": "peer_review_helper_accepts_events",
            "passed": "events" in enrich_args,
            "evidence": enrich_args,
        }
    )
    checks.append(
        {
            "name": "provider_teamwork_reads_current_heap_events",
            "passed": has_read_events_assignment(provider_fn),
            "evidence": "run_provider_teamwork assigns events = self.read_events() before peer enrichment",
        }
    )
    checks.append(
        {
            "name": "provider_teamwork_passes_events_to_peer_review",
            "passed": enrich_call_passes_events(provider_fn),
            "evidence": "enrich_provider_report_with_operational_peer_review(..., events)",
        }
    )
    for field_name in (
        "preflight_command",
        "startup_command",
        "heap_command",
        "composer_command",
        "external_postrun_command",
    ):
        checks.append(
            {
                "name": f"launcher_summary_exposes_{field_name}",
                "passed": launcher_summary_exposes_command(launcher_tree, field_name),
                "evidence": field_name,
            }
        )

    failed = [check["name"] for check in checks if not check.get("passed")]
    return {
        "schema_version": 1,
        "kind": "heap_provider_peer_review_events_scope_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors and not failed,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checked_files": [repo_rel(repo_root, gate_path), repo_rel(repo_root, launcher_path)],
        "checks": checks,
        "errors": errors + failed,
        "warnings": [],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Provider Peer Review Events Scope Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        "",
        "## Checks",
        "",
    ]
    for check in report.get("checks") or []:
        lines.append(f"- `{check.get('name')}`: `{check.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report.get("errors") or [])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/heap_provider_peer_review_events_scope_smoke.json"
    )
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(
        repo_root, args.markdown_output or str(Path(args.output).with_suffix(".md"))
    )
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(
        json.dumps(
            {
                **report,
                "output": repo_rel(repo_root, output),
                "markdown_output": repo_rel(repo_root, markdown_output),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
