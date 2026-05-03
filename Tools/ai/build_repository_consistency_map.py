#!/usr/bin/env python3
"""Build a deterministic repository consistency map before provider review.

The mapper is intentionally CPU/deterministic and report-only. It scans
Markdown, Python and PowerShell references to give GPU/NPU provider lanes a
structured discrepancy table instead of raw repository noise.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    from Tools.validation.report_utils import write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.validation.report_utils import write_json_report, write_text_report  # type: ignore

DEFAULT_OUTPUT = "output/analysis/repository_consistency_map.json"
DEFAULT_MARKDOWN = "output/analysis/repository_consistency_map.md"
DEFAULT_MAX_SNIPPET_CHARS = 220
EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "output",
    "renders",
    ".mypy_cache",
    ".pytest_cache",
}
TEXT_EXTENSIONS = {".md", ".markdown", ".py", ".ps1"}
SCRIPT_EXTENSIONS = {".py", ".ps1"}
DOC_EXTENSIONS = {".md", ".markdown"}
PATH_TOKEN_RE = re.compile(
    r"(?P<path>(?:\.?[A-Za-z0-9_./\\-]+/)?[A-Za-z0-9_.-]+\.(?:py|ps1|md|markdown|json|csv|sqlite|db))",
    re.IGNORECASE,
)
PY_COMMAND_RE = re.compile(
    r"(?:^|[\s`>])(?P<python>python(?:\.exe)?|py)\s+(?P<script>[A-Za-z0-9_./\\-]+\.py)(?P<args>[^\n`]*)",
    re.IGNORECASE,
)
FLAG_RE = re.compile(r"(?<![\w-])--[A-Za-z0-9][A-Za-z0-9_-]*")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<link>[^)]+)\)")
BACKTICK_RE = re.compile(r"`([^`]+)`")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def elapsed_seconds(started: float) -> float:
    return round(time.perf_counter() - started, 3)

def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def normalize_ref(value: str) -> str:
    normalized = value.strip().strip("'\"<>()[]{}.,:;").replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.strip("/")


def should_skip(path: Path, repo_root: Path) -> bool:
    try:
        rel_parts = path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).parts
    except ValueError:
        return True
    return any(part in EXCLUDE_DIRS for part in rel_parts)


def iter_files(repo_root: Path, extensions: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path, repo_root):
            continue
        if path.suffix.lower() in extensions:
            files.append(path)
    return sorted(files, key=lambda item: repo_rel(item, repo_root))


def read_text(path: Path) -> tuple[str, str | None]:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace"), None
    except OSError as exc:
        return "", f"{type(exc).__name__}: {exc}"


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def snippet_for_line(text: str, line_no: int, *, max_chars: int) -> str:
    lines = text.splitlines()
    if line_no < 1 or line_no > len(lines):
        return ""
    snippet = lines[line_no - 1].strip()
    if len(snippet) > max_chars:
        return snippet[: max_chars - 3] + "..."
    return snippet


def build_existing_path_index(repo_root: Path) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in iter_files(repo_root, TEXT_EXTENSIONS | {".json", ".csv"}):
        rel = repo_rel(path, repo_root)
        index[rel.lower()] = rel
        index[path.name.lower()] = rel
    return index


def resolve_repo_reference(repo_root: Path, source: str, raw_ref: str, path_index: dict[str, str]) -> tuple[str, bool, str]:
    ref = normalize_ref(raw_ref)
    if not ref or ref.startswith(("http://", "https://", "mailto:")):
        return ref, True, "external_or_empty"
    direct = (repo_root / ref).resolve(strict=False)
    if direct.exists():
        return repo_rel(direct, repo_root), True, "direct"
    source_parent = (repo_root / source).parent
    relative = (source_parent / ref).resolve(strict=False)
    if relative.exists():
        return repo_rel(relative, repo_root), True, "relative_to_source"
    indexed = path_index.get(ref.lower()) or path_index.get(Path(ref).name.lower())
    if indexed:
        return indexed, True, "basename_index"
    return ref, False, "missing"


def bounded_worker_count(requested: int, workload_count: int) -> int:
    # Conservative worker cap for repository scans.
    if workload_count <= 1:
        return 1
    if requested <= 0:
        requested = 8
    return max(1, min(requested, workload_count))

def extract_markdown_references(repo_root: Path, path_index: dict[str, str], *, max_snippet_chars: int, workers: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    references: list[dict[str, Any]] = []
    commands: list[dict[str, Any]] = []
    warnings: list[str] = []
    markdown_files = iter_files(repo_root, DOC_EXTENSIONS)

    def scan_markdown_file(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
        file_references: list[dict[str, Any]] = []
        file_commands: list[dict[str, Any]] = []
        file_warnings: list[str] = []
        rel = repo_rel(path, repo_root)
        text, error = read_text(path)
        if error:
            file_warnings.append(f"{rel}: {error}")
            return file_references, file_commands, file_warnings
        seen_refs: set[tuple[str, int]] = set()
        candidates: list[tuple[str, int]] = []
        for match in PATH_TOKEN_RE.finditer(text):
            candidates.append((match.group("path"), match.start()))
        for match in MD_LINK_RE.finditer(text):
            link = match.group("link").split("#", 1)[0]
            if Path(link).suffix.lower() in TEXT_EXTENSIONS | {".json", ".csv"}:
                candidates.append((link, match.start()))
        for match in BACKTICK_RE.finditer(text):
            value = match.group(1).strip()
            if Path(value).suffix.lower() in TEXT_EXTENSIONS | {".json", ".csv"}:
                candidates.append((value, match.start()))
        for raw_ref, offset in candidates:
            line_no = line_for_offset(text, offset)
            key = (normalize_ref(raw_ref), line_no)
            if key in seen_refs:
                continue
            seen_refs.add(key)
            resolved, exists, mode = resolve_repo_reference(repo_root, rel, raw_ref, path_index)
            ext = Path(normalize_ref(raw_ref)).suffix.lower()
            kind = "python" if ext == ".py" else "powershell" if ext == ".ps1" else "markdown" if ext in DOC_EXTENSIONS else "artifact"
            file_references.append(
                {
                    "source": rel,
                    "line": line_no,
                    "raw_ref": normalize_ref(raw_ref),
                    "resolved": resolved,
                    "exists": exists,
                    "resolution": mode,
                    "kind": kind,
                    "snippet": snippet_for_line(text, line_no, max_chars=max_snippet_chars),
                }
            )
        for match in PY_COMMAND_RE.finditer(text):
            line_no = line_for_offset(text, match.start())
            script_raw = normalize_ref(match.group("script"))
            resolved, exists, mode = resolve_repo_reference(repo_root, rel, script_raw, path_index)
            args_text = match.group("args") or ""
            flags = sorted(set(FLAG_RE.findall(args_text)))
            file_commands.append(
                {
                    "source": rel,
                    "line": line_no,
                    "script_raw": script_raw,
                    "script_resolved": resolved,
                    "script_exists": exists,
                    "resolution": mode,
                    "flags": flags,
                    "snippet": snippet_for_line(text, line_no, max_chars=max_snippet_chars),
                }
            )
        return file_references, file_commands, file_warnings

    worker_count = bounded_worker_count(workers, len(markdown_files))
    if worker_count > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            for file_references, file_commands, file_warnings in executor.map(scan_markdown_file, markdown_files):
                references.extend(file_references)
                commands.extend(file_commands)
                warnings.extend(file_warnings)
    else:
        for path in markdown_files:
            file_references, file_commands, file_warnings = scan_markdown_file(path)
            references.extend(file_references)
            commands.extend(file_commands)
            warnings.extend(file_warnings)
    return references, commands, warnings

def literal_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def extract_argparse_flags(tree: ast.AST) -> list[str]:
    flags: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        attr = node.func
        if not isinstance(attr, ast.Attribute) or attr.attr != "add_argument":
            continue
        for arg in node.args:
            value = literal_string(arg)
            if value and value.startswith("--"):
                flags.add(value)
    return sorted(flags)


def extract_python_symbols(tree: ast.AST) -> dict[str, list[str]]:
    functions: list[str] = []
    classes: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
    return {"functions": sorted(set(functions)), "classes": sorted(set(classes))}


def module_to_paths(module: str, repo_root: Path) -> list[str]:
    parts = [part for part in module.split(".") if part]
    if not parts:
        return []
    return [
        (repo_root / Path(*parts)).with_suffix(".py").as_posix(),
        (repo_root / Path(*parts) / "__init__.py").as_posix(),
    ]


def local_module_exists(module: str, repo_root: Path) -> bool:
    for candidate in module_to_paths(module, repo_root):
        if Path(candidate).exists():
            return True
    return False


def extract_local_import_findings(tree: ast.AST, source: str, repo_root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    local_prefixes = ("Tools", "Scripting", "indexAI")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in local_prefixes and not local_module_exists(alias.name, repo_root):
                    findings.append(
                        {
                            "source": source,
                            "line": getattr(node, "lineno", 0),
                            "module": alias.name,
                            "kind": "python_import_missing",
                        }
                    )
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                continue
            module = node.module or ""
            root = module.split(".", 1)[0]
            if root in local_prefixes and not local_module_exists(module, repo_root):
                findings.append(
                    {
                        "source": source,
                        "line": getattr(node, "lineno", 0),
                        "module": module,
                        "kind": "python_import_missing",
                    }
                )
    return findings


def extract_python_inventory(repo_root: Path, *, workers: int) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[str]]:
    inventory: dict[str, dict[str, Any]] = {}
    import_findings: list[dict[str, Any]] = []
    warnings: list[str] = []
    python_files = iter_files(repo_root, {".py"})

    def scan_python_file(path: Path) -> tuple[str, dict[str, Any], list[dict[str, Any]], list[str]]:
        rel = repo_rel(path, repo_root)
        text, error = read_text(path)
        file_warnings: list[str] = []
        if error:
            file_warnings.append(f"{rel}: {error}")
            return rel, {"argparse_flags": [], "functions": [], "classes": [], "syntax_error": error}, [], file_warnings
        try:
            tree = ast.parse(text, filename=rel)
        except SyntaxError as exc:
            file_warnings.append(f"{rel}: SyntaxError line {exc.lineno}: {exc.msg}")
            return rel, {"argparse_flags": [], "functions": [], "classes": [], "syntax_error": str(exc)}, [], file_warnings
        symbols = extract_python_symbols(tree)
        item = {
            "argparse_flags": extract_argparse_flags(tree),
            "functions": symbols["functions"],
            "classes": symbols["classes"],
            "syntax_error": "",
        }
        return rel, item, extract_local_import_findings(tree, rel, repo_root), file_warnings

    worker_count = bounded_worker_count(workers, len(python_files))
    if worker_count > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            for rel, item, file_import_findings, file_warnings in executor.map(scan_python_file, python_files):
                inventory[rel] = item
                import_findings.extend(file_import_findings)
                warnings.extend(file_warnings)
    else:
        for path in python_files:
            rel, item, file_import_findings, file_warnings = scan_python_file(path)
            inventory[rel] = item
            import_findings.extend(file_import_findings)
            warnings.extend(file_warnings)
    return inventory, import_findings, warnings

def smoke_candidates_for_script(script: str, all_python_files: Iterable[str]) -> list[str]:
    stem = Path(script).stem.lower()
    candidates: list[str] = []
    for path in all_python_files:
        lowered = path.lower()
        if "/validation/" not in lowered and not lowered.startswith("tools/validation/"):
            continue
        if stem in lowered and ("smoke" in lowered or "check" in lowered or "test" in lowered):
            candidates.append(path)
    return sorted(candidates)


def build_findings(
    *,
    md_refs: list[dict[str, Any]],
    md_commands: list[dict[str, Any]],
    py_inventory: dict[str, dict[str, Any]],
    import_findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for ref in md_refs:
        if ref["kind"] in {"python", "powershell", "markdown"} and not ref["exists"]:
            severity = "high" if ref["kind"] in {"python", "powershell"} else "medium"
            findings.append(
                {
                    "kind": f"md_mentions_missing_{ref['kind']}_path",
                    "severity": severity,
                    "source": ref["source"],
                    "line": ref["line"],
                    "target": ref["raw_ref"],
                    "evidence": ref["snippet"],
                    "recommendation": "Correct the documentation reference or restore the missing target if it is still required.",
                }
            )
    for command in md_commands:
        if not command["script_exists"]:
            findings.append(
                {
                    "kind": "md_python_command_script_missing",
                    "severity": "high",
                    "source": command["source"],
                    "line": command["line"],
                    "target": command["script_raw"],
                    "evidence": command["snippet"],
                    "recommendation": "Update the command to a real script path or remove the obsolete command.",
                }
            )
            continue
        script = command["script_resolved"]
        known_flags = set(py_inventory.get(script, {}).get("argparse_flags", []))
        for flag in command["flags"]:
            if known_flags and flag not in known_flags:
                findings.append(
                    {
                        "kind": "md_cli_arg_not_in_argparse",
                        "severity": "medium",
                        "source": command["source"],
                        "line": command["line"],
                        "target": script,
                        "flag": flag,
                        "known_flags_sample": sorted(known_flags)[:40],
                        "evidence": command["snippet"],
                        "recommendation": "Correct the documented CLI flag or update the script argparse contract in a focused PR.",
                    }
                )
    for item in import_findings:
        findings.append(
            {
                "kind": item["kind"],
                "severity": "high",
                "source": item["source"],
                "line": item["line"],
                "target": item["module"],
                "evidence": f"local import `{item['module']}` cannot be resolved to a repository Python module",
                "recommendation": "Fix the import or add the missing module in a focused code PR.",
            }
        )
    all_py = sorted(py_inventory)
    cited_scripts = sorted({command["script_resolved"] for command in md_commands if command.get("script_exists")})
    for script in cited_scripts:
        if script not in py_inventory:
            continue
        if not smoke_candidates_for_script(script, all_py):
            findings.append(
                {
                    "kind": "documented_python_script_without_obvious_smoke",
                    "severity": "low",
                    "source": script,
                    "line": 0,
                    "target": script,
                    "evidence": "Script is cited by documentation commands but no obvious smoke/check/test file references its stem under Tools/validation.",
                    "recommendation": "Consider adding a smoke validator or documenting why none is needed.",
                }
            )
    return findings


def build_provider_hints(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_kind: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for finding in findings:
        by_kind[str(finding.get("kind"))].append(finding)
    hints: list[dict[str, Any]] = []
    for kind, items in sorted(by_kind.items(), key=lambda pair: (-len(pair[1]), pair[0])):
        targets = sorted({str(item.get("target") or item.get("source") or "") for item in items if item.get("target") or item.get("source")})
        sources = sorted({str(item.get("source") or "") for item in items if item.get("source")})
        hints.append(
            {
                "kind": kind,
                "count": len(items),
                "severity_counts": dict(Counter(str(item.get("severity")) for item in items)),
                "sample_sources": sources[:12],
                "sample_targets": targets[:12],
                "planner_instruction": "Prioritize concrete patch plans that correct the cited source/target pairs without touching generated output, SQLite, provider settings or Blender runtime.",
            }
        )
    return hints


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    total_started = time.perf_counter()
    repo_root = Path(args.repo_root).resolve()
    timings: dict[str, float] = {}

    phase_started = time.perf_counter()
    markdown_file_count = len(iter_files(repo_root, DOC_EXTENSIONS))
    python_file_count = len(iter_files(repo_root, {".py"}))
    timings["file_discovery_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    path_index = build_existing_path_index(repo_root)
    timings["path_index_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    md_refs, md_commands, md_warnings = extract_markdown_references(
        repo_root,
        path_index,
        max_snippet_chars=args.max_snippet_chars,
        workers=args.workers,
    )
    timings["markdown_scan_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    py_inventory, import_findings, py_warnings = extract_python_inventory(repo_root, workers=args.workers)
    timings["python_inventory_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    findings = build_findings(
        md_refs=md_refs,
        md_commands=md_commands,
        py_inventory=py_inventory,
        import_findings=import_findings,
    )
    severity_counts = Counter(str(item.get("severity")) for item in findings)
    kind_counts = Counter(str(item.get("kind")) for item in findings)
    references_by_kind = Counter(str(item.get("kind")) for item in md_refs)
    provider_hints = build_provider_hints(findings)
    timings["findings_build_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    scope = {
        "markdown_file_count": markdown_file_count,
        "python_file_count": python_file_count,
        "markdown_reference_count": len(md_refs),
        "markdown_python_command_count": len(md_commands),
        "python_inventory_count": len(py_inventory),
    }
    performance = {
        "workers_requested": args.workers,
        "markdown_scan_workers": bounded_worker_count(args.workers, markdown_file_count),
        "python_scan_workers": bounded_worker_count(args.workers, python_file_count),
        **timings,
    }
    performance["report_assembly_seconds"] = elapsed_seconds(phase_started)
    performance["total_build_report_seconds"] = elapsed_seconds(total_started)

    report = {
        "schema_version": 1,
        "kind": "repository_consistency_map",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": True,
        "errors": [],
        "warnings": md_warnings + py_warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "scope": scope,
        "finding_count": len(findings),
        "severity_counts": dict(sorted(severity_counts.items())),
        "finding_kind_counts": dict(sorted(kind_counts.items())),
        "markdown_reference_kind_counts": dict(sorted(references_by_kind.items())),
        "findings": findings,
        "markdown_references": md_refs[: args.max_detail_items] if args.max_detail_items else md_refs,
        "markdown_python_commands": md_commands[: args.max_detail_items] if args.max_detail_items else md_commands,
        "python_inventory": py_inventory,
        "provider_hints_for_gpu_planner": provider_hints,
        "performance": performance,
        "guardrails": {
            "report_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "do_not_commit_output": True,
        },
    }
    return report

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Repository Consistency Map", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Finding count: `{report['finding_count']}`")
    lines.append(f"- Markdown files: `{report['scope']['markdown_file_count']}`")
    lines.append(f"- Python files: `{report['scope']['python_file_count']}`")
    lines.append(f"- Markdown references: `{report['scope']['markdown_reference_count']}`")
    lines.append(f"- Markdown Python commands: `{report['scope']['markdown_python_command_count']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    if report.get("performance"):
        performance = report["performance"]
        lines.append(f"- Workers requested: `{performance.get('workers_requested')}`")
        lines.append(f"- Total build seconds: `{performance.get('total_build_report_seconds')}`")
        lines.append(f"- Markdown scan seconds: `{performance.get('markdown_scan_seconds')}`")
        lines.append(f"- Python inventory seconds: `{performance.get('python_inventory_seconds')}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append("")
    lines.append("## Severity counts")
    lines.append("")
    if report.get("severity_counts"):
        for key, value in report["severity_counts"].items():
            lines.append(f"- `{key}`: `{value}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Finding kind counts")
    lines.append("")
    if report.get("finding_kind_counts"):
        for key, value in report["finding_kind_counts"].items():
            lines.append(f"- `{key}`: `{value}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    lines.append("| Severity | Kind | Source | Line | Target | Recommendation |")
    lines.append("|---|---|---|---:|---|---|")
    for item in report.get("findings", [])[:200]:
        lines.append(
            f"| `{item.get('severity')}` | `{item.get('kind')}` | `{item.get('source')}` | {item.get('line') or 0} | `{item.get('target') or item.get('flag') or ''}` | {str(item.get('recommendation') or '').replace('|', '/')} |"
        )
    if len(report.get("findings", [])) > 200:
        lines.append(f"| ... | ... | ... | ... | ... | truncated in Markdown; JSON contains {len(report['findings'])} findings |")
    lines.append("")
    lines.append("## Provider hints")
    lines.append("")
    for hint in report.get("provider_hints_for_gpu_planner", [])[:40]:
        lines.append(f"- `{hint.get('kind')}` count `{hint.get('count')}`; sample targets: {', '.join('`' + item + '`' for item in hint.get('sample_targets', [])[:5])}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument("--max-detail-items", type=int, default=2000)
    parser.add_argument("--max-snippet-chars", type=int, default=DEFAULT_MAX_SNIPPET_CHARS)
    parser.add_argument("--workers", type=int, default=8, help="Bounded worker count for Markdown/Python repository scans.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    report = build_report(args)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "finding_count": report["finding_count"],
                "severity_counts": report["severity_counts"],
                "markdown_reference_count": report["scope"]["markdown_reference_count"],
                "markdown_python_command_count": report["scope"]["markdown_python_command_count"],
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
                "sqlite_write_performed": report["sqlite_write_performed"],
                "workers_requested": report.get("performance", {}).get("workers_requested"),
                "performance": report.get("performance", {}),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
