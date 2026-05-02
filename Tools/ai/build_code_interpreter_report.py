#!/usr/bin/env python3
"""Build a static code interpreter report for Python source files.

This tool interprets code structure without executing project code. It parses
Python files with AST, extracts symbols/imports, computes lightweight risk and
complexity signals, and emits report-only evidence for later patch-plan and code
edit proposal lanes.

It does not execute providers, run Blender, apply patches or write source files.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[2]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from Tools.ai.code_patch_plan_common import (  # noqa: E402
    compact_text,
    now_iso,
    repo_rel,
    report_only_guardrails,
    write_json_and_markdown,
)

REPORT_KIND = "code_interpreter_report"
DEFAULT_OUTPUT = "output/analysis/code_interpreter_report.json"
DEFAULT_MARKDOWN = "output/analysis/code_interpreter_report.md"
DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "output",
    "renders",
    "venv",
}
RISK_CALLS = {
    "eval": "dynamic_code_execution",
    "exec": "dynamic_code_execution",
    "compile": "dynamic_code_compilation",
    "open": "file_io",
    "subprocess.run": "subprocess_execution",
    "subprocess.Popen": "subprocess_execution",
    "os.system": "shell_execution",
    "shutil.rmtree": "destructive_file_operation",
}
TODO_PATTERN = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.IGNORECASE)
BRANCH_NODES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.ExceptHandler, ast.BoolOp, ast.IfExp, ast.Match)


def split_csv_values(values: list[str]) -> set[str]:
    """Expand repeated comma-separated CLI values into a set."""
    return {item.strip() for value in values for item in value.split(",") if item.strip()}


def excluded_by_dir(path: Path, repo_root: Path, excluded_dirs: set[str]) -> bool:
    """Return true when any relative path component is excluded."""
    try:
        parts = path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).parts
    except ValueError:
        parts = path.parts
    return any(part in excluded_dirs for part in parts)


def iter_python_files(repo_root: Path, roots: list[Path], excluded_dirs: set[str]) -> list[Path]:
    """Return sorted Python source files."""
    candidates: list[Path] = []
    search_roots = roots or [repo_root]
    for root in search_roots:
        if root.is_file() and root.suffix.lower() == ".py":
            candidates.append(root)
        elif root.is_dir():
            candidates.extend(path for path in root.rglob("*.py") if path.is_file())
    filtered = [path for path in candidates if not excluded_by_dir(path, repo_root, excluded_dirs)]
    unique = {path.resolve(strict=False): path for path in filtered}
    return sorted(unique.values(), key=lambda path: repo_rel(repo_root, path).lower())


def resolve_roots(repo_root: Path, values: list[str]) -> list[Path]:
    """Resolve CLI input roots."""
    roots: list[Path] = []
    for value in values:
        raw = Path(value)
        roots.append(raw.resolve() if raw.is_absolute() else (repo_root / raw).resolve())
    return roots


def read_source(path: Path) -> tuple[str, str | None]:
    """Read source text."""
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace"), None
    except OSError as exc:
        return "", f"{type(exc).__name__}: {exc}"


def source_line_count(source: str) -> int:
    """Return a stable physical line count for source text."""
    return source.count("\n") + (0 if source.endswith("\n") else 1) if source else 0


def dotted_name(node: ast.AST) -> str:
    """Return dotted name for call/import expression when possible."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def line_span(node: ast.AST) -> int:
    """Return physical line span for a node."""
    start = getattr(node, "lineno", None)
    end = getattr(node, "end_lineno", None)
    if isinstance(start, int) and isinstance(end, int):
        return max(1, end - start + 1)
    return 0


def function_record(node: ast.AST) -> dict[str, Any]:
    """Return compact function/method metadata."""
    args = getattr(node, "args", None)
    arg_count = len(args.args) + len(args.kwonlyargs) if args else 0
    return {
        "name": getattr(node, "name", ""),
        "lineno": getattr(node, "lineno", None),
        "line_span": line_span(node),
        "arg_count": arg_count,
        "branch_count": sum(1 for child in ast.walk(node) if isinstance(child, BRANCH_NODES)),
        "docstring_present": bool(ast.get_docstring(node)),
        "async": isinstance(node, ast.AsyncFunctionDef),
    }


def class_record(node: ast.ClassDef) -> dict[str, Any]:
    """Return compact class metadata."""
    methods = [child for child in node.body if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))]
    return {
        "name": node.name,
        "lineno": node.lineno,
        "line_span": line_span(node),
        "method_count": len(methods),
        "docstring_present": bool(ast.get_docstring(node)),
    }


def import_records(tree: ast.AST) -> list[dict[str, str]]:
    """Extract imports."""
    imports: list[dict[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({"type": "import", "name": alias.name, "asname": alias.asname or ""})
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append({"type": "from", "module": module, "name": alias.name, "asname": alias.asname or ""})
    return imports


def risk_signals(tree: ast.AST) -> list[dict[str, Any]]:
    """Extract risky/static-interest call signals."""
    signals: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = dotted_name(node.func)
        if name in RISK_CALLS:
            signals.append({"call": name, "category": RISK_CALLS[name], "lineno": getattr(node, "lineno", None)})
    return signals


def todo_signals(source: str) -> list[dict[str, Any]]:
    """Return TODO/FIXME-like comments."""
    out: list[dict[str, Any]] = []
    for index, line in enumerate(source.splitlines(), start=1):
        if TODO_PATTERN.search(line):
            out.append({"lineno": index, "text": compact_text(line.strip(), 240)})
    return out


def analyze_file(repo_root: Path, path: Path) -> dict[str, Any]:
    """Analyze one Python file without executing it."""
    rel = repo_rel(repo_root, path)
    source, read_error = read_source(path)
    base: dict[str, Any] = {
        "path": rel,
        "read_ok": read_error is None,
        "parse_ok": False,
        "errors": [read_error] if read_error else [],
        "line_count": source_line_count(source),
        "char_count": len(source),
    }
    if read_error:
        return base
    try:
        tree = ast.parse(source, filename=rel)
    except SyntaxError as exc:
        base["errors"].append(f"SyntaxError:{exc.lineno}:{exc.offset}: {exc.msg}")
        return base

    functions = [function_record(node) for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [class_record(node) for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    imports = import_records(tree)
    risks = risk_signals(tree)
    todos = todo_signals(source)
    branch_count = sum(1 for node in ast.walk(tree) if isinstance(node, BRANCH_NODES))
    large_functions = [item for item in functions if int(item.get("line_span") or 0) >= 80]
    complex_functions = [item for item in functions if int(item.get("branch_count") or 0) >= 12]

    base.update(
        {
            "parse_ok": True,
            "function_count": len(functions),
            "class_count": len(classes),
            "import_count": len(imports),
            "branch_count": branch_count,
            "todo_count": len(todos),
            "risk_signal_count": len(risks),
            "large_function_count": len(large_functions),
            "complex_function_count": len(complex_functions),
            "functions": sorted(functions, key=lambda item: int(item.get("line_span") or 0), reverse=True)[:30],
            "classes": sorted(classes, key=lambda item: int(item.get("line_span") or 0), reverse=True)[:30],
            "imports": imports[:80],
            "risk_signals": risks[:80],
            "todo_signals": todos[:60],
            "large_functions": large_functions[:20],
            "complex_functions": complex_functions[:20],
        }
    )
    return base


def classify_file_risk(item: dict[str, Any]) -> str:
    """Classify static review risk for one file."""
    if not item.get("parse_ok"):
        return "high"
    if item.get("risk_signal_count", 0) >= 5 or item.get("line_count", 0) >= 800:
        return "high"
    if item.get("large_function_count", 0) or item.get("complex_function_count", 0) or item.get("line_count", 0) >= 400:
        return "medium"
    return "low"


def recommendation_reasons(item: dict[str, Any], risk: str) -> list[str]:
    """Return non-empty reasons for every medium/high static recommendation."""
    reasons: list[str] = []
    if not item.get("parse_ok"):
        reasons.append("file does not parse")
    if item.get("line_count", 0) >= 800:
        reasons.append("large Python module")
    elif risk in {"medium", "high"} and item.get("line_count", 0) >= 400:
        reasons.append("medium-size Python module")
    if item.get("large_function_count", 0):
        reasons.append("large functions detected")
    if item.get("complex_function_count", 0):
        reasons.append("complex functions detected")
    if item.get("risk_signal_count", 0):
        reasons.append("static risk calls detected")
    if item.get("todo_count", 0):
        reasons.append("TODO/FIXME markers detected")
    if risk in {"medium", "high"} and not reasons:
        branch_count = item.get("branch_count", 0)
        function_count = item.get("function_count", 0)
        line_count_value = item.get("line_count", 0)
        reasons.append(f"risk classified as {risk} from aggregate static metrics: lines={line_count_value}, functions={function_count}, branches={branch_count}")
    return reasons


def validation_commands_for(path_value: str) -> list[str]:
    """Return validation commands for one recommendation target."""
    ps_path = str(path_value).replace("/", "\\")
    return [
        f"python -m py_compile .\\{ps_path}",
        "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
        "git diff --check",
    ]


def recommendation_record(index: int, item: dict[str, Any], risk: str, reasons: list[str]) -> dict[str, Any]:
    """Build one static recommendation record."""
    target_file = str(item.get("path") or "")
    return {
        "id": f"code_static_{index:03d}",
        "target_file": item.get("path"),
        "risk": risk,
        "status": "candidate_for_manual_review",
        "reasons": reasons,
        "recommended_next_layer": "agent_review_code_patch_plan" if item.get("parse_ok") else "syntax_fix_before_patch_plan",
        "validation_commands": validation_commands_for(target_file),
    }


def build_recommendations(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build static recommendations suitable for later patch-plan review."""
    recommendations: list[dict[str, Any]] = []
    for item in files:
        risk = classify_file_risk(item)
        if risk == "low" and not item.get("todo_count"):
            continue
        recommendations.append(recommendation_record(len(recommendations) + 1, item, risk, recommendation_reasons(item, risk)))
    return recommendations


def aggregate_imports(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return top imported modules."""
    counter: Counter[str] = Counter()
    for item in files:
        for imp in item.get("imports", []):
            if isinstance(imp, dict):
                module = imp.get("module") or imp.get("name") or ""
                if module:
                    counter[str(module).split(".")[0]] += 1
    return [{"module": module, "count": count} for module, count in counter.most_common(40)]


def aggregate_file_metrics(files: list[dict[str, Any]]) -> dict[str, int]:
    """Return aggregate report counters for analyzed files."""
    return {
        "file_count": len(files),
        "parsed_file_count": sum(1 for item in files if item.get("parse_ok")),
        "total_lines": sum(int(item.get("line_count") or 0) for item in files),
        "total_functions": sum(int(item.get("function_count") or 0) for item in files),
        "total_classes": sum(int(item.get("class_count") or 0) for item in files),
        "total_risk_signals": sum(int(item.get("risk_signal_count") or 0) for item in files),
        "total_todos": sum(int(item.get("todo_count") or 0) for item in files),
    }


def largest_file_entries(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return largest-file summary entries."""
    return sorted(
        [{"path": item.get("path"), "line_count": item.get("line_count"), "risk": classify_file_risk(item)} for item in files],
        key=lambda value: int(value.get("line_count") or 0),
        reverse=True,
    )[:30]


def build_report(repo_root: Path, roots: list[Path], excluded_dirs: set[str]) -> dict[str, Any]:
    """Build full static code interpreter report."""
    files = [analyze_file(repo_root, path) for path in iter_python_files(repo_root, roots, excluded_dirs)]
    errors = [f"{item.get('path')}: {'; '.join(item.get('errors') or [])}" for item in files if item.get("errors")]
    recommendations = build_recommendations(files)
    metrics = aggregate_file_metrics(files)
    return {
        "schema_version": 1,
        "kind": REPORT_KIND,
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "manual_review_required": True,
        "apply_mode": "report_only_static_code_interpreter",
        **metrics,
        "top_imports": aggregate_imports(files),
        "largest_files": largest_file_entries(files),
        "risk_summary": dict(Counter(classify_file_risk(item) for item in files)),
        "recommendation_count": len(recommendations),
        "recommendations": recommendations[:80],
        "files": files,
        "guardrails": report_only_guardrails(
            static_analysis_only=True,
            project_code_executed=False,
            providers_executed=False,
            blender_runtime_executed=False,
            patches_applied=False,
            source_files_written=False,
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render compact Markdown summary."""
    lines = ["# Static Code Interpreter Report", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- File count: `{report['file_count']}`")
    lines.append(f"- Parsed files: `{report['parsed_file_count']}`")
    lines.append(f"- Total lines: `{report['total_lines']}`")
    lines.append(f"- Total functions: `{report['total_functions']}`")
    lines.append(f"- Total classes: `{report['total_classes']}`")
    lines.append(f"- Risk signals: `{report['total_risk_signals']}`")
    lines.append(f"- TODO/FIXME markers: `{report['total_todos']}`")
    lines.append(f"- Recommendation count: `{report['recommendation_count']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Source writes performed: `{report['source_writes_performed']}`")
    lines.append("")
    lines.append("## Largest files")
    lines.append("")
    for item in report.get("largest_files", [])[:20]:
        lines.append(f"- `{item.get('path')}` — `{item.get('line_count')}` lines, risk `{item.get('risk')}`")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("")
    recommendations = report.get("recommendations", [])
    if not recommendations:
        lines.append("- none")
    for item in recommendations[:40]:
        lines.append(f"- `{item.get('id')}` `{item.get('target_file')}` risk `{item.get('risk')}`: {', '.join(item.get('reasons') or ['no reason recorded'])}")
    lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append("This is static interpretation only. It does not execute repository code or apply changes.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--input", action="append", default=[], help="Optional file/dir roots; defaults to repo root.")
    parser.add_argument("--exclude-dir", action="append", default=[], help="Additional directory names to exclude.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    excluded_dirs = set(DEFAULT_EXCLUDED_DIRS)
    excluded_dirs.update(split_csv_values(args.exclude_dir))
    report = build_report(repo_root, resolve_roots(repo_root, args.input), excluded_dirs)
    print(write_json_and_markdown(repo_root, report, args.output, args.markdown_output, render_markdown(report)), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
