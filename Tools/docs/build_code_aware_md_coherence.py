#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

EXCLUDE_DIR_NAMES = {
    ".git", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache",
    "node_modules", "output", "renders",
}
EXCLUDE_PREFIXES = (
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "Tools/npu/npu_blender_manual_chunks/",
)
ACTIVE_DOC_PREFIXES = ("docs/", "CHATGPT/", "Tools/", "README.md", "AGENTS.md", "WORKFLOW.md", "FULL_RUN_UNICA_TUTTO_SU_TUTTO.md")
PATH_RE = re.compile(r"(?P<path>(?:\\.\\\\|\\./)?(?:[A-Za-z0-9_.-]+[\\\\/])+[A-Za-z0-9_.-]+\\.(?:md|py|ps1|json|csv|txt|yaml|yml))")
INLINE_PATH_RE = re.compile(r"`([^`]+\\.(?:md|py|ps1|json|csv|txt|yaml|yml))`")
LONG_FLAG_RE = re.compile(r"(?<![\\w-])--[A-Za-z0-9][A-Za-z0-9_-]*")
PS_FLAG_RE = re.compile(r"(?<![\\w-])-[A-Z][A-Za-z0-9_]*")
HEADING_RE = re.compile(r"^(#{1,6})\\s+(.+?)\\s*$")
PY_COMMAND_RE = re.compile(r"(?:^|\\s)(?:python|py|python3|&\\s*\\$PythonExe)\\s+(?P<script>[^\\s`'\"]+\\.py)")
PS_COMMAND_RE = re.compile(r"(?:powershell(?:\\.exe)?[^\
]*-File\\s+|^\\s*&\\s+|^\\s*)?(?P<script>(?:\\.\\\\|\\./|Tools[\\\\/])[^\\s`'\"]+\\.ps1)", re.IGNORECASE)


def repo_root_from(start: Path) -> Path:
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"Repository root not found from {start}")


def rel_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def is_excluded_rel(rel: str) -> bool:
    lower = rel.replace("\\", "/")
    return any(lower.startswith(prefix) for prefix in EXCLUDE_PREFIXES)


def iter_files(root: Path, suffixes: set[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = rel_path(path, root)
        parts = set(Path(rel).parts)
        if parts & EXCLUDE_DIR_NAMES:
            continue
        if is_excluded_rel(rel):
            continue
        if path.suffix.lower() in suffixes:
            yield path


def clean_ref(raw: str) -> str:
    value = raw.strip().strip("`'\".,);]")
    value = value.replace("\\", "/")
    if value.startswith("./"):
        value = value[2:]
    if value.startswith(".//"):
        value = value[3:]
    return value


def path_exists(root: Path, ref: str) -> bool:
    ref = clean_ref(ref)
    if not ref:
        return False
    return (root / ref).exists()


def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def line_count(text: str) -> int:
    return len(text.splitlines())


@dataclass
class ScriptInfo:
    path: str
    suffix: str
    lines: int
    argparse_flags: list[str]
    ps_params: list[str]
    functions: list[str]
    classes: list[str]
    has_main: bool
    command_like: bool


@dataclass
class MarkdownInfo:
    path: str
    lines: int
    headings: list[str]
    referenced_paths: list[str]
    commands: list[dict[str, Any]]
    flags: list[str]


@dataclass
class Finding:
    severity: str
    kind: str
    path: str
    detail: str
    target: str | None = None


class ArgparseVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.flags: set[str] = set()
        self.functions: list[str] = []
        self.classes: list[str] = []
        self.has_main = False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> Any:
        try:
            if isinstance(node.test, ast.Compare):
                left = node.test.left
                if isinstance(left, ast.Name) and left.id == "__name__":
                    self.has_main = True
        except Exception:
            pass
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "add_argument":
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and arg.value.startswith("-"):
                    self.flags.add(arg.value)
        self.generic_visit(node)


def parse_python(path: Path, root: Path) -> ScriptInfo:
    text = safe_read(path)
    visitor = ArgparseVisitor()
    try:
        visitor.visit(ast.parse(text))
    except SyntaxError:
        pass
    rel = rel_path(path, root)
    return ScriptInfo(
        path=rel,
        suffix=".py",
        lines=line_count(text),
        argparse_flags=sorted(visitor.flags),
        ps_params=[],
        functions=sorted(set(visitor.functions))[:200],
        classes=sorted(set(visitor.classes))[:200],
        has_main=visitor.has_main,
        command_like=bool(visitor.flags or visitor.has_main or rel.startswith("Tools/")),
    )


def parse_ps1(path: Path, root: Path) -> ScriptInfo:
    text = safe_read(path)
    params: set[str] = set()
    m = re.search(r"param\\s*\\((.*?)\\)", text, flags=re.IGNORECASE | re.DOTALL)
    if m:
        block = m.group(1)
        for match in re.finditer(r"\\$([A-Za-z_][A-Za-z0-9_]*)", block):
            params.add("-" + match.group(1))
    rel = rel_path(path, root)
    return ScriptInfo(
        path=rel,
        suffix=".ps1",
        lines=line_count(text),
        argparse_flags=[],
        ps_params=sorted(params),
        functions=sorted(set(re.findall(r"function\\s+([A-Za-z_][A-Za-z0-9_-]*)", text, flags=re.IGNORECASE)))[:200],
        classes=[],
        has_main=True,
        command_like=rel.startswith("Tools/") or bool(params),
    )


def parse_markdown(path: Path, root: Path) -> MarkdownInfo:
    text = safe_read(path)
    refs: set[str] = set()
    for m in PATH_RE.finditer(text):
        refs.add(clean_ref(m.group("path")))
    for m in INLINE_PATH_RE.finditer(text):
        refs.add(clean_ref(m.group(1)))

    commands: list[dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        py_match = PY_COMMAND_RE.search(line)
        ps_match = PS_COMMAND_RE.search(line)
        script = None
        kind = None
        if py_match:
            script = clean_ref(py_match.group("script"))
            kind = "python"
        elif ps_match and ".ps1" in ps_match.group("script"):
            script = clean_ref(ps_match.group("script"))
            kind = "powershell"
        if script:
            commands.append({
                "line": line_no,
                "kind": kind,
                "script": script,
                "flags": sorted(set(LONG_FLAG_RE.findall(line) + PS_FLAG_RE.findall(line))),
                "text": line.strip()[:500],
            })
            refs.add(script)

    headings = []
    for line in text.splitlines():
        h = HEADING_RE.match(line)
        if h:
            headings.append(h.group(2).strip())

    return MarkdownInfo(
        path=rel_path(path, root),
        lines=line_count(text),
        headings=headings[:200],
        referenced_paths=sorted(refs),
        commands=commands,
        flags=sorted(set(LONG_FLAG_RE.findall(text) + PS_FLAG_RE.findall(text))),
    )


def active_doc(rel: str, include_evidence: bool) -> bool:
    if rel.startswith("docs/LOCAL_VALIDATION_EVIDENCE/") and not include_evidence:
        return False
    return rel.startswith(ACTIVE_DOC_PREFIXES) or rel in {"README.md", "AGENTS.md", "WORKFLOW.md", "FULL_RUN_UNICA_TUTTO_SU_TUTTO.md"}


def build_report(repo_root: Path, max_lines: int, include_evidence: bool) -> dict[str, Any]:
    scripts: dict[str, ScriptInfo] = {}
    for path in iter_files(repo_root, {".py", ".ps1"}):
        rel = rel_path(path, repo_root)
        try:
            scripts[rel] = parse_python(path, repo_root) if path.suffix.lower() == ".py" else parse_ps1(path, repo_root)
        except Exception as exc:
            scripts[rel] = ScriptInfo(rel, path.suffix.lower(), 0, [], [], [], [], False, False)

    markdowns: dict[str, MarkdownInfo] = {}
    for path in iter_files(repo_root, {".md"}):
        rel = rel_path(path, repo_root)
        if not active_doc(rel, include_evidence):
            continue
        markdowns[rel] = parse_markdown(path, repo_root)

    findings: list[Finding] = []
    referenced_paths: Counter[str] = Counter()
    script_mentioned_by: dict[str, list[str]] = defaultdict(list)

    for md in markdowns.values():
        if md.lines > max_lines:
            findings.append(Finding("high", "markdown_line_budget_exceeded", md.path, f"{md.lines} lines > {max_lines}", md.path))
        for ref in md.referenced_paths:
            if not ref or ref.startswith("http"):
                continue
            referenced_paths[ref] += 1
            if ref.endswith((".py", ".ps1")):
                script_mentioned_by[ref].append(md.path)
            if not path_exists(repo_root, ref):
                sev = "high" if ref.endswith((".py", ".ps1")) else "medium"
                findings.append(Finding(sev, "markdown_references_missing_path", md.path, f"Missing referenced path: {ref}", ref))
        for cmd in md.commands:
            script = clean_ref(str(cmd.get("script") or ""))
            if not script:
                continue
            if script not in scripts:
                sev = "high" if not path_exists(repo_root, script) else "medium"
                findings.append(Finding(sev, "markdown_command_script_not_in_inventory", md.path, f"Command references script not in active script inventory at line {cmd.get('line')}: {script}", script))
                continue
            available = set(scripts[script].argparse_flags or scripts[script].ps_params)
            documented_flags = [f for f in cmd.get("flags", []) if f.startswith("--") or (script.endswith(".ps1") and f.startswith("-"))]
            for flag in documented_flags:
                if available and flag not in available:
                    findings.append(Finding("medium", "markdown_command_flag_not_in_script_contract", md.path, f"Flag {flag} not found in {script} contract at line {cmd.get('line')}", script))

    for script, info in scripts.items():
        if not info.command_like:
            continue
        if not script.startswith("Tools/"):
            continue
        if not script_mentioned_by.get(script):
            severity = "medium" if script.startswith(("Tools/ai/", "Tools/validation/", "Tools/workflow/")) else "low"
            findings.append(Finding(severity, "active_script_not_documented_in_markdown", script, "Active command-like script not referenced by active Markdown", script))

    by_severity = Counter(f.severity for f in findings)
    by_kind = Counter(f.kind for f in findings)
    top_missing = referenced_paths.most_common(50)

    patch_plan = []
    if by_kind.get("markdown_line_budget_exceeded"):
        patch_plan.append({
            "id": "md_code_coherence_001_split_large_markdown",
            "area": "documentation_size",
            "risk": "medium",
            "status": "ready_for_local_review",
            "rationale": "Active Markdown exceeds line budget and should become an index/stub plus directory parts.",
            "strategy": "Run Tools/docs/split_large_markdown.py or equivalent controlled splitter; keep generated parts under 400 lines recursively.",
        })
    if by_kind.get("markdown_references_missing_path"):
        patch_plan.append({
            "id": "md_code_coherence_002_fix_or_demote_missing_refs",
            "area": "documentation_links",
            "risk": "medium",
            "status": "requires_manual_review",
            "rationale": "Markdown references paths that do not exist in the current branch; some may be historical/evidence-only.",
            "strategy": "Classify missing refs as active/current, historical, evidence, or stale; update docs only after classification.",
        })
    if by_kind.get("active_script_not_documented_in_markdown"):
        patch_plan.append({
            "id": "md_code_coherence_003_generate_code_aware_tool_index",
            "area": "tool_documentation",
            "risk": "low",
            "status": "ready_for_local_review",
            "rationale": "Command-like Tools scripts exist without active Markdown references.",
            "strategy": "Generate compact code-aware index from script inventory and link it from LOCAL_AI_TASKS/README.md only after review.",
        })
    if by_kind.get("markdown_command_flag_not_in_script_contract"):
        patch_plan.append({
            "id": "md_code_coherence_004_update_command_contracts",
            "area": "command_contracts",
            "risk": "medium",
            "status": "requires_manual_review",
            "rationale": "Some documented command flags are not visible in script argparse/PowerShell param contracts.",
            "strategy": "Verify whether docs are stale or parser extraction missed dynamic flags; then patch docs or script contracts explicitly.",
        })

    return {
        "kind": "md_code_coherence_report",
        "schema_version": 1,
        "repo_root": str(repo_root),
        "max_lines": max_lines,
        "include_evidence": include_evidence,
        "source_writes_performed": False,
        "patch_application_performed": False,
        "summary": {
            "markdown_count": len(markdowns),
            "script_count": len(scripts),
            "finding_count": len(findings),
            "by_severity": dict(sorted(by_severity.items())),
            "by_kind": dict(sorted(by_kind.items())),
            "patch_plan_count": len(patch_plan),
        },
        "scripts": [asdict(x) for x in sorted(scripts.values(), key=lambda s: s.path)],
        "markdowns": [asdict(x) for x in sorted(markdowns.values(), key=lambda m: m.path)],
        "findings": [asdict(x) for x in findings],
        "top_referenced_paths": [{"path": p, "count": c, "exists": path_exists(repo_root, p)} for p, c in top_missing],
        "patch_plan": patch_plan,
    }


def render_markdown(report: dict[str, Any]) -> str:
    s = report["summary"]
    lines = [
        "# Markdown/code coherence report",
        "",
        f"- Kind: `{report['kind']}`",
        f"- Max Markdown lines: `{report['max_lines']}`",
        f"- Markdown scanned: `{s['markdown_count']}`",
        f"- Scripts scanned: `{s['script_count']}`",
        f"- Findings: `{s['finding_count']}`",
        f"- Patch plan count: `{s['patch_plan_count']}`",
        "",
        "## Findings by severity",
        "",
    ]
    for k, v in s["by_severity"].items():
        lines.append(f"- `{k}`: `{v}`")
    lines += ["", "## Findings by kind", ""]
    for k, v in s["by_kind"].items():
        lines.append(f"- `{k}`: `{v}`")
    lines += ["", "## Patch plan candidates", ""]
    for plan in report.get("patch_plan", []):
        lines.append(f"### {plan['id']} — {plan['area']}")
        lines.append(f"- Risk: `{plan['risk']}`")
        lines.append(f"- Status: `{plan['status']}`")
        lines.append(f"- Rationale: {plan['rationale']}")
        lines.append(f"- Strategy: {plan['strategy']}")
        lines.append("")
    lines += ["## Top findings", ""]
    for item in report.get("findings", [])[:120]:
        lines.append(f"- `{item['severity']}` `{item['kind']}` `{item['path']}` -> {item['detail']}")
    lines += ["", "## Top referenced paths", ""]
    for item in report.get("top_referenced_paths", [])[:50]:
        lines.append(f"- `{item['path']}` count=`{item['count']}` exists=`{item['exists']}`")
    lines.append("")
    return "\
".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build code-aware Markdown coherence report for IA-Carmine.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-lines", type=int, default=400)
    parser.add_argument("--include-evidence", action="store_true")
    parser.add_argument("--output", default="output/validation/md_code_coherence_report.json")
    parser.add_argument("--markdown-output", default="output/validation/md_code_coherence_report.md")
    args = parser.parse_args()

    repo = repo_root_from(Path(args.repo_root))
    report = build_report(repo, args.max_lines, args.include_evidence)
    out = repo / args.output
    md = repo / args.markdown_output
    out.parent.mkdir(parents=True, exist_ok=True)
    md.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8", newline="\
")
    md.write_text(render_markdown(report), encoding="utf-8", newline="\
")
    print(f"[OK] Wrote {out}")
    print(f"[OK] Wrote {md}")
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
