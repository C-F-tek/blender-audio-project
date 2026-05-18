#!/usr/bin/env python3
"""Validate Markdown line-count budgets for IA-Carmine documentation.

The validator supports both normal Markdown files and the IA-Carmine split
directory layout:

    name.md/README.md
    name.md/part-001.md

A path ending in ``.md`` may therefore be either a readable file or a split
container directory. The validator reads only real Markdown files and records
split-container metadata in the report.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

DEFAULT_MAX_LINES = 400
DEFAULT_SCOPES = (
    "AGENTS.md",
    "CHATGPT.md",
    "FULL_RUN_UNICA_TUTTO_SU_TUTTO.md",
    "README.md",
    "WORKFLOW.md",
    "docs",
    "CHATGPT",
)
EXCLUDED_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "output",
    "renders",
    "venv",
}
EXCLUDED_PREFIXES = (
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "Tools/npu/npu_blender_manual_chunks/",
)


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"Cannot find repository root from {start}")


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def split_container_for(path: Path, root: Path) -> str | None:
    """Return the repo-relative split container when path lives under *.md/."""
    try:
        relative_parts = path.resolve().relative_to(root.resolve()).parts
    except ValueError:
        return None
    for index, part in enumerate(relative_parts[:-1]):
        if part.endswith(".md"):
            return "/".join(relative_parts[: index + 1])
    return None


def is_split_markdown_file(path: Path, root: Path) -> bool:
    return split_container_for(path, root) is not None


def markdown_role(path: Path, root: Path) -> str:
    if not is_split_markdown_file(path, root):
        return "markdown_file"
    name = path.name.lower()
    if name == "readme.md":
        return "split_index"
    if name.startswith("part-") and name.endswith(".md"):
        return "split_part"
    return "split_auxiliary_markdown"


def should_skip(path: Path, root: Path, include_evidence: bool) -> bool:
    try:
        rel_parts = path.resolve().relative_to(root.resolve()).parts
    except ValueError:
        rel_parts = path.parts
    if any(part in EXCLUDED_DIR_NAMES for part in rel_parts):
        return True
    prefixes = (
        EXCLUDED_PREFIXES
        if not include_evidence
        else tuple(p for p in EXCLUDED_PREFIXES if p != "docs/LOCAL_VALIDATION_EVIDENCE/")
    )
    path_rel = rel(path, root)
    return any(path_rel.startswith(prefix) for prefix in prefixes)


def collect_split_containers(root: Path, scopes: list[str], include_evidence: bool) -> list[Path]:
    """Collect directory-form Markdown containers under the selected scopes."""
    containers: dict[str, Path] = {}
    for scope in scopes:
        base = (root / scope).resolve()
        if not base.exists():
            continue
        candidates = [base] if base.is_dir() and base.name.endswith(".md") else base.rglob("*.md")
        for path in candidates:
            if (
                path.is_dir()
                and path.name.endswith(".md")
                and not should_skip(path, root, include_evidence)
            ):
                containers[rel(path, root)] = path
    return [containers[key] for key in sorted(containers)]


def iter_markdown(root: Path, scopes: list[str], include_evidence: bool) -> list[Path]:
    """Return real Markdown files, including files inside directory-form splits."""
    files: dict[str, Path] = {}
    for scope in scopes:
        base = (root / scope).resolve()
        if not base.exists():
            continue
        if base.is_file():
            candidates = [base]
        elif base.is_dir() and base.name.endswith(".md"):
            candidates = base.rglob("*.md")
        else:
            candidates = base.rglob("*.md")
        for path in candidates:
            if path.is_dir():
                continue
            if (
                path.is_file()
                and path.suffix.lower() == ".md"
                and not should_skip(path, root, include_evidence)
            ):
                files[rel(path, root)] = path
    return [files[key] for key in sorted(files)]


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Markdown line limit validation",
        "",
        f"- Kind: `{report['kind']}`",
        f"- Passed: `{report['passed']}`",
        f"- Max lines: `{report['max_lines']}`",
        f"- Checked files: `{report['checked_file_count']}`",
        f"- Split container count: `{report['split_container_count']}`",
        f"- Split markdown file count: `{report['split_markdown_file_count']}`",
        f"- Violation count: `{report['violation_count']}`",
        "",
    ]
    violations = report.get("violations") or []
    if violations:
        lines.extend(["## Violations", ""])
        for item in violations:  # type: ignore[assignment]
            lines.append(
                f"- `{item['path']}` role=`{item['markdown_role']}` lines=`{item['line_count']}`"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--include-evidence", action="store_true")
    parser.add_argument("--output", default="output/validation/markdown_line_limit_validation.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/markdown_line_limit_validation.md"
    )
    args = parser.parse_args()

    root = find_repo_root(Path(args.repo_root))
    scopes = args.scope or list(DEFAULT_SCOPES)
    containers = collect_split_containers(root, scopes, args.include_evidence)
    files = iter_markdown(root, scopes, args.include_evidence)
    checked = []
    violations = []
    for path in files:
        line_count = len(path.read_text(encoding="utf-8-sig", errors="replace").splitlines())
        container = split_container_for(path, root)
        item = {
            "path": rel(path, root),
            "line_count": line_count,
            "markdown_role": markdown_role(path, root),
            "split_container": container or "",
            "directory_form_md_suffix": bool(container),
        }
        checked.append(item)
        if line_count > args.max_lines:
            violations.append(item)

    report = {
        "kind": "ia_carmine_markdown_line_limit_validation",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": not violations,
        "max_lines": args.max_lines,
        "scopes": scopes,
        "include_evidence": bool(args.include_evidence),
        "checked_file_count": len(checked),
        "split_container_count": len(containers),
        "split_containers": [rel(path, root) for path in containers],
        "split_markdown_file_count": sum(1 for item in checked if item["directory_form_md_suffix"]),
        "violation_count": len(violations),
        "violations": violations,
    }
    out = root / args.output
    md = root / args.markdown_output
    out.parent.mkdir(parents=True, exist_ok=True)
    md.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md.write_text(render_markdown(report), encoding="utf-8")
    print(
        f"[OK] Checked={len(checked)} split_containers={len(containers)} violations={len(violations)}"
    )
    print(f"[OK] Report: {rel(out, root)}")
    print(f"[OK] Markdown report: {rel(md, root)}")
    return 0 if not violations else 2


if __name__ == "__main__":
    raise SystemExit(main())
