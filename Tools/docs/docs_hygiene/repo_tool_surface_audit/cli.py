"""Audit the repository tool surface for legacy entrypoints and large files."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

CODE_SUFFIXES = {".py", ".ps1"}
TEXT_SUFFIXES = {".py", ".ps1", ".md", ".txt", ".json", ".yml", ".yaml", ".toml"}
IGNORE_DIRS = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".venv", "__pycache__"}
IGNORE_PATH_PREFIXES = (
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "indexAI/",
    "output/",
    "renders/",
)
ROOT_SCRIPT_ALLOWLIST = {"__init__.py", "__main__.py", "dispatch.py"}
HIDDEN_PACKAGE_SUFFIXES = ("_cli", "_core", "_view", "_model", "_controller")
LEGACY_COMMAND_PATTERNS = [
    re.compile(
        r"(?P<prefix>\bpython(?:\.exe)?\b|\bpy\b|"
        r"\$[A-Za-z_][A-Za-z0-9_]*(?:py|python)[A-Za-z0-9_]*|"
        r"\$env:[A-Za-z_][A-Za-z0-9_]*(?:py|python)[A-Za-z0-9_]*)"
        r"[^\n\r`|&;]*\s+"
        r"(?P<path>(?:\.?[\\/])?Tools[\\/][A-Za-z0-9_.-]+[\\/][A-Za-z0-9_.\\/-]+\.(?:py|ps1))"
        ,
        re.IGNORECASE,
    ),
    re.compile(
        r"(?P<prefix>-File)\s+[`\"']?"
        r"(?P<path>(?:\.?[\\/])?Tools[\\/][A-Za-z0-9_.-]+[\\/][A-Za-z0-9_.\\/-]+\.ps1)"
    ),
]


@dataclass(frozen=True)
class Finding:
    kind: str
    severity: str
    path: str
    line: int
    detail: str
    replacement: str = ""


def repo_root_from(path: Path) -> Path:
    root = path.resolve()
    if (root / ".git").exists():
        return root
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode == 0 and completed.stdout.strip():
        return Path(completed.stdout.strip()).resolve()
    return root


def is_ignored_path(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in IGNORE_PATH_PREFIXES)


def git_visible_files(root: Path) -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode == 0:
        return [
            root / line.strip()
            for line in completed.stdout.splitlines()
            if line.strip() and not is_ignored_path(line.strip())
        ]
    paths: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.relative_to(root).parts):
            continue
        if is_ignored_path(relative(root, path)):
            continue
        paths.append(path)
    return paths


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def path_matches_area(root: Path, path: Path, areas: set[str]) -> bool:
    if not areas:
        return True
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    return len(parts) >= 2 and parts[0] == "Tools" and parts[1] in areas


def line_count(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
    except OSError:
        return 0


def tool_module_for(legacy_path: str) -> str:
    cleaned = legacy_path.strip("`\"'").replace("\\", "/")
    cleaned = cleaned.removeprefix("./").removeprefix(".")
    parts = [part for part in cleaned.split("/") if part]
    if len(parts) < 3 or parts[0] != "Tools":
        return ""
    area = parts[1]
    stem = Path(parts[-1]).stem
    return f"python -m Tools.{area} {stem}"


def iter_tool_roots(root: Path) -> Iterable[Path]:
    tools_root = root / "Tools"
    if not tools_root.exists():
        return []
    return sorted(path for path in tools_root.iterdir() if path.is_dir() and not path.name.startswith("__"))


def scan_root_scripts(root: Path, areas: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    for area_dir in iter_tool_roots(root):
        if areas and area_dir.name not in areas:
            continue
        for path in sorted(area_dir.iterdir()):
            if not path.is_file() or path.suffix not in CODE_SUFFIXES:
                continue
            if path.name in ROOT_SCRIPT_ALLOWLIST:
                continue
            if path.name.endswith(("_cli.py", "_core.py", "_view.py", "_model.py", "_controller.py")):
                continue
            rel = relative(root, path)
            findings.append(
                Finding(
                    kind="root_script_entrypoint",
                    severity="medium",
                    path=rel,
                    line=1,
                    detail="Script lives directly in a Tools/<area> root instead of a package/dispatcher surface.",
                    replacement=f"python -m Tools.{area_dir.name} {path.stem}",
                )
            )
    return findings


def _alias_target_package(text: str, area: str) -> str:
    if re.search(r"^\s*(def|class)\s+", text, flags=re.MULTILINE):
        return ""
    patterns = [
        re.compile(
            rf"^\s*from\s+Tools\.{re.escape(area)}\.(?P<target>[A-Za-z0-9_]+)(?:\.|\s+import\s+main)",
            flags=re.MULTILINE,
        ),
        re.compile(
            r"^\s*from\s+(?P<target>[A-Za-z0-9_]+)(?:\.|\s+import\s+main)",
            flags=re.MULTILINE,
        ),
    ]
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            return match.group("target")
    return ""


def scan_alias_tool_packages(root: Path, areas: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    tools_root = root / "Tools"
    if not tools_root.exists():
        return findings
    for area_dir in iter_tool_roots(root):
        area = area_dir.name
        if areas and area not in areas:
            continue
        for package_dir in sorted(path for path in area_dir.iterdir() if path.is_dir()):
            package = package_dir.name
            if package.startswith("__") or package.endswith(HIDDEN_PACKAGE_SUFFIXES):
                continue
            cli = package_dir / "cli.py"
            if not cli.exists():
                continue
            try:
                text = cli.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            target = _alias_target_package(text, area)
            if not target or target == package:
                continue
            if target.startswith("_") or target.endswith(HIDDEN_PACKAGE_SUFFIXES):
                continue
            target_cli = area_dir / target / "cli.py"
            target_init = area_dir / target / "__init__.py"
            if not target_cli.exists() and not target_init.exists():
                continue
            findings.append(
                Finding(
                    kind="alias_tool_package",
                    severity="high",
                    path=relative(root, cli),
                    line=1,
                    detail=f"`{package}` only delegates to `{target}` while both packages exist.",
                    replacement=f"python -m Tools.{area} {target}",
                )
            )
    return findings


def scan_legacy_invocations(root: Path, files: list[Path], areas: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = relative(root, path)
        if is_ignored_path(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            for pattern in LEGACY_COMMAND_PATTERNS:
                for match in pattern.finditer(line):
                    legacy_path = match.group("path")
                    before_path = line[: match.start("path")]
                    if "-m py_compile" in before_path:
                        continue
                    normalized = legacy_path.replace("\\", "/")
                    parts = [part for part in normalized.split("/") if part and part != "."]
                    if len(parts) >= 3 and areas and parts[1] not in areas:
                        continue
                    findings.append(
                        Finding(
                            kind="legacy_direct_invocation",
                            severity="high",
                            path=rel,
                            line=number,
                            detail=legacy_path,
                            replacement=tool_module_for(legacy_path),
                        )
                    )
    return findings


def scan_large_files(
    root: Path,
    files: list[Path],
    code_max: int,
    md_max: int,
    areas: set[str],
) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        if not path_matches_area(root, path, areas):
            continue
        suffix = path.suffix.lower()
        if suffix not in CODE_SUFFIXES and suffix != ".md":
            continue
        count = line_count(path)
        limit = md_max if suffix == ".md" else code_max
        if count <= limit:
            continue
        findings.append(
            Finding(
                kind="line_budget_exceeded",
                severity="high" if suffix in CODE_SUFFIXES else "medium",
                path=relative(root, path),
                line=limit + 1,
                detail=f"{count} lines exceeds limit {limit}",
            )
        )
    return findings


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Repository Tool Surface Audit",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Findings: `{report['summary']['finding_count']}`",
        f"- Provider execution: `{report['provider_execution_performed']}`",
        f"- Source writes: `{report['source_writes_performed']}`",
        "",
        "## Summary",
        "",
        f"- By kind: `{json.dumps(report['summary']['by_kind'], ensure_ascii=False)}`",
        f"- By severity: `{json.dumps(report['summary']['by_severity'], ensure_ascii=False)}`",
        "",
        "## Findings",
        "",
        "| Severity | Kind | Path | Line | Detail | Replacement |",
        "|---|---|---|---:|---|---|",
    ]
    findings = report["findings"]
    assert isinstance(findings, list)
    for item in findings[:250]:
        assert isinstance(item, dict)
        detail = str(item["detail"]).replace("|", "\\|")
        replacement = str(item.get("replacement", "")).replace("|", "\\|")
        lines.append(
            f"| {item['severity']} | {item['kind']} | `{item['path']}` | {item['line']} | {detail} | `{replacement}` |"
        )
    if len(findings) > 250:
        lines.append(f"\n_Truncated {len(findings) - 250} more findings; see JSON._")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "This audit is report-only. Deletions, moves and source rewrites require explicit reviewed refactor steps.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_summary(findings: list[Finding]) -> dict[str, object]:
    return {
        "finding_count": len(findings),
        "by_kind": dict(Counter(item.kind for item in findings).most_common()),
        "by_severity": dict(Counter(item.severity for item in findings).most_common()),
    }


def parse_areas(values: list[str]) -> set[str]:
    areas: set[str] = set()
    for value in values:
        areas.update(part.strip() for part in value.split(",") if part.strip())
    return areas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--area", action="append", default=[], help="Limit to Tools area names.")
    parser.add_argument("--code-max-lines", type=int, default=400)
    parser.add_argument("--md-max-lines", type=int, default=500)
    parser.add_argument("--output", default="output/validation/repo_tool_surface_audit.json")
    parser.add_argument("--markdown-output", default="output/validation/repo_tool_surface_audit.md")
    parser.add_argument("--fail-on-findings", action="store_true")
    args = parser.parse_args()

    root = repo_root_from(Path(args.repo_root))
    areas = parse_areas(args.area)
    files = git_visible_files(root)
    findings: list[Finding] = []
    findings.extend(scan_root_scripts(root, areas))
    findings.extend(scan_alias_tool_packages(root, areas))
    findings.extend(scan_legacy_invocations(root, files, areas))
    findings.extend(scan_large_files(root, files, args.code_max_lines, args.md_max_lines, areas))
    findings = sorted(findings, key=lambda item: (item.severity, item.kind, item.path, item.line))
    report: dict[str, object] = {
        "schema_version": 1,
        "kind": "repo_tool_surface_audit",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": root.as_posix(),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "summary": build_summary(findings),
        "findings": [asdict(item) for item in findings],
    }
    output = root / args.output
    markdown_output = root / args.markdown_output
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": not (args.fail_on_findings and findings), "summary": report["summary"]}, indent=2))
    return 1 if args.fail_on_findings and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
