#!/usr/bin/env python3
from __future__ import annotations

import ast
import re
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PS_PARAM_RE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")

try:
    from Tools.docs.docs_hygiene.code_aware_md_refs import (
        build_file_index,
        classify_missing_ref,
        collect_doc_command_refs,
        collect_md_refs,
        is_active_md,
        is_excluded_rel,
        reference_exists,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script fallback
    from code_aware_md_refs import (
        build_file_index,
        classify_missing_ref,
        collect_doc_command_refs,
        collect_md_refs,
        is_active_md,
        is_excluded_rel,
        reference_exists,
    )


@dataclass
class Finding:
    severity: str
    kind: str
    path: str
    target: str
    detail: str
    classification: str


def repo_root_from(start: Path) -> Path:
    cur = start.resolve()
    for candidate in (cur, *cur.parents):
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"[FAIL] Repository root not found from {start}")


def repo_relative(path: Path, repo: Path) -> str:
    return path.resolve().relative_to(repo.resolve()).as_posix()


def iter_repo_files(repo: Path, suffixes: tuple[str, ...]) -> Iterable[Path]:
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        rel = repo_relative(path, repo)
        if is_excluded_rel(rel):
            continue
        if path.suffix.lower() in suffixes:
            yield path


def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def line_count(text: str) -> int:
    if not text:
        return 0
    return len(text.splitlines())


def extract_python_args(path: Path) -> list[str]:
    text = safe_read(path)
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    args: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "add_argument":
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if arg.value.startswith("-"):
                        args.add(arg.value)
    return sorted(args)


def extract_python_symbols(path: Path) -> dict[str, int]:
    text = safe_read(path)
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {"functions": 0, "classes": 0}
    functions = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree))
    classes = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
    return {"functions": functions, "classes": classes}


def extract_ps_params(text: str) -> list[str]:
    start = text.lower().find("param(")
    if start < 0:
        return []
    depth = 0
    end = start
    for idx, char in enumerate(text[start:], start=start):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                end = idx + 1
                break
    block = text[start:end]
    return sorted({f"-{name}" for name in PS_PARAM_RE.findall(block)})


def build_script_maps(repo: Path) -> dict[str, Any]:
    python_scripts: dict[str, Any] = {}
    powershell_scripts: dict[str, Any] = {}
    for path in iter_repo_files(repo, (".py",)):
        rel = repo_relative(path, repo)
        text = safe_read(path)
        python_scripts[rel] = {
            "path": rel,
            "line_count": line_count(text),
            "args": extract_python_args(path),
            **extract_python_symbols(path),
        }
    for path in iter_repo_files(repo, (".ps1",)):
        rel = repo_relative(path, repo)
        text = safe_read(path)
        powershell_scripts[rel] = {
            "path": rel,
            "line_count": line_count(text),
            "params": extract_ps_params(text),
        }
    return {"python": python_scripts, "powershell": powershell_scripts}


def build_existing_file_index(repo: Path) -> dict[str, Any]:
    suffixes = (".md", ".py", ".ps1", ".json", ".csv", ".txt", ".yaml", ".yml")
    paths = sorted(repo_relative(path, repo) for path in iter_repo_files(repo, suffixes))
    return build_file_index(paths)


def analyze_markdown(repo: Path, scripts: dict[str, Any], max_lines: int) -> dict[str, Any]:
    findings: list[Finding] = []
    docs: dict[str, Any] = {}
    python_scripts = scripts["python"]
    powershell_scripts = scripts["powershell"]
    file_index = build_existing_file_index(repo)
    for path in iter_repo_files(repo, (".md",)):
        rel = repo_relative(path, repo)
        text = safe_read(path)
        lines = line_count(text)
        refs = sorted(collect_md_refs(text))
        py_cmds, ps_cmds = collect_doc_command_refs(text)
        docs[rel] = {
            "path": rel,
            "line_count": lines,
            "active": is_active_md(rel),
            "reference_count": len(refs),
            "python_command_count": len(py_cmds),
            "powershell_command_count": len(ps_cmds),
        }
        if is_active_md(rel) and lines > max_lines:
            findings.append(
                Finding(
                    "high",
                    "active_markdown_over_line_budget",
                    rel,
                    rel,
                    f"{lines} lines > {max_lines}; split into stub + directory parts.",
                    "active-current",
                )
            )
        for ref in refs:
            if is_excluded_rel(ref):
                continue
            if not reference_exists(repo, path, ref, file_index):
                severity, classification = classify_missing_ref(ref, rel)
                findings.append(
                    Finding(
                        severity,
                        "markdown_reference_missing",
                        rel,
                        ref,
                        "Referenced path does not exist in current working tree.",
                        classification,
                    )
                )
        for script, flags in py_cmds:
            if script not in python_scripts:
                severity, classification = classify_missing_ref(script, rel)
                findings.append(
                    Finding(
                        severity,
                        "markdown_python_command_missing_script",
                        rel,
                        script,
                        "Documented Python command points to a missing script.",
                        classification,
                    )
                )
                continue
            known = set(python_scripts[script].get("args") or [])
            for flag in flags:
                if known and flag not in known:
                    findings.append(
                        Finding(
                            "medium",
                            "markdown_python_flag_not_in_argparse",
                            rel,
                            f"{script} {flag}",
                            "Documented long flag is not present in argparse.add_argument().",
                            "stale-or-future",
                        )
                    )
        for script, flags in ps_cmds:
            if script not in powershell_scripts:
                severity, classification = classify_missing_ref(script, rel)
                findings.append(
                    Finding(
                        severity,
                        "markdown_powershell_command_missing_script",
                        rel,
                        script,
                        "Documented PowerShell command points to a missing script.",
                        classification,
                    )
                )
                continue
            known = set(powershell_scripts[script].get("params") or [])
            for flag in flags:
                if (
                    known
                    and flag not in known
                    and flag not in {"-NoProfile", "-ExecutionPolicy", "-File"}
                ):
                    findings.append(
                        Finding(
                            "medium",
                            "markdown_powershell_flag_not_in_param_block",
                            rel,
                            f"{script} {flag}",
                            "Documented PowerShell parameter is not visible in param() block.",
                            "stale-or-future",
                        )
                    )
    return {"documents": docs, "findings": [asdict(f) for f in findings]}


def summarize(report: dict[str, Any]) -> dict[str, Any]:
    findings = report["findings"]
    by_severity = Counter(f["severity"] for f in findings)
    by_kind = Counter(f["kind"] for f in findings)
    by_classification = Counter(f["classification"] for f in findings)
    return {
        "finding_count": len(findings),
        "by_severity": dict(sorted(by_severity.items())),
        "by_kind": dict(by_kind.most_common()),
        "by_classification": dict(by_classification.most_common()),
    }
