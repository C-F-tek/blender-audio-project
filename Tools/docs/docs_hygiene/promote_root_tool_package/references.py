"""Reference scanning and move helpers for root tool package promotion."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from Tools.docs.docs_hygiene.repo_tool_surface_audit import git_visible_files

TEXT_SUFFIXES = {".py", ".ps1", ".md", ".txt", ".json", ".yml", ".yaml", ".toml"}
CODE_REFERENCE_SUFFIXES = {".py", ".ps1", ".json", ".yml", ".yaml", ".toml"}
ROOT_SCRIPT_ALLOWLIST = {"__init__.py", "__main__.py", "dispatch.py"}
REFERENCE_SKIP_PREFIXES = (
    "output/",
    "indexAI/",
    "renders/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
)


@dataclass(frozen=True)
class Reference:
    path: str
    line: int
    text: str


@dataclass(frozen=True)
class ReferenceRewrite:
    path: str
    old: str
    new: str
    count: int


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def line_count_text(text: str) -> int:
    return len(text.splitlines())


def is_generated_reference_path(rel: str) -> bool:
    normalized = rel.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in REFERENCE_SKIP_PREFIXES)


def increment_parent_indexes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"parents[{int(match.group(1)) + 1}]"

    return re.sub(r"parents\[(\d+)\]", replace, text)


def scan_references(root: Path, area: str, tool: str) -> list[Reference]:
    needles = [
        f"Tools/{area}/{tool}.py",
        f"Tools\\{area}\\{tool}.py",
        f"Tools.{area}.{tool}",
    ]
    refs: list[Reference] = []
    for path in git_visible_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = relative(root, path)
        if is_generated_reference_path(rel):
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if any(needle in line for needle in needles):
                refs.append(Reference(path=rel, line=number, text=line.strip()))
    return refs


def git_mv(root: Path, source: Path, target: Path) -> None:
    source_rel = str(source.relative_to(root))
    target_rel = str(target.relative_to(root))
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", source_rel],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        text=True,
    )
    if tracked.returncode != 0:
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        source.unlink()
        return
    completed = subprocess.run(
        ["git", "mv", source_rel, target_rel],
        cwd=root,
        check=False,
        text=True,
    )
    if completed.returncode != 0:
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        source.unlink()


def script_exposes_main(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return "def main(" in text or "def main()" in text or "if __name__" in text


def candidate_tools(root: Path, area: str) -> list[str]:
    area_dir = root / "Tools" / area
    tools: list[str] = []
    for path in sorted(area_dir.glob("*.py")):
        if path.name in ROOT_SCRIPT_ALLOWLIST:
            continue
        if path.stem.endswith(("_cli", "_core", "_view", "_model", "_controller")):
            continue
        if script_exposes_main(path):
            tools.append(path.stem)
    return tools


def rewrite_code_path_references(
    root: Path,
    *,
    area: str,
    tool: str,
    apply: bool,
) -> list[ReferenceRewrite]:
    old_new_pairs = [
        (f"Tools/{area}/{tool}.py", f"Tools/{area}/{tool}/cli.py"),
        (f"Tools\\{area}\\{tool}.py", f"Tools\\{area}\\{tool}\\cli.py"),
    ]
    rewrites: list[ReferenceRewrite] = []
    for path in git_visible_files(root):
        if path.suffix.lower() not in CODE_REFERENCE_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = relative(root, path)
        if is_generated_reference_path(rel):
            continue
        updated = text
        total = 0
        last_old = ""
        last_new = ""
        for old, new in old_new_pairs:
            count = updated.count(old)
            if count:
                updated = updated.replace(old, new)
                total += count
                last_old = old
                last_new = new
        if total:
            if apply:
                path.write_text(updated, encoding="utf-8")
            rewrites.append(ReferenceRewrite(path=rel, old=last_old, new=last_new, count=total))
    return rewrites
