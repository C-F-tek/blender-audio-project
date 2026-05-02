#!/usr/bin/env python3
"""Build deterministic Python line-count CSV evidence.

This utility replaces ad-hoc shell snippets for repository Python line-count
collection. It is report-only: it reads source files and writes CSV/JSON/MD
summary artifacts to explicit output paths.

It does not execute providers, run Blender, apply patches or modify source
files.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


REPORT_KIND = "python_line_count_csv"
DEFAULT_CSV = "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_latest.csv"
DEFAULT_REPORT = "output/validation/python_line_count_latest.json"
DEFAULT_MARKDOWN = "output/validation/python_line_count_latest.md"
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
DEFAULT_EXCLUDED_SUFFIXES = {
    ".db",
    ".sqlite",
    ".sqlite3",
}


def now_stamp() -> str:
    """Return a compact local timestamp safe for filenames."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def repo_rel(repo_root: Path, path: Path) -> str:
    """Return repository-relative POSIX path when possible."""
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def split_csv_values(values: list[str]) -> set[str]:
    """Expand repeated comma-separated CLI values into a set."""
    items: set[str] = set()
    for value in values:
        for item in value.split(","):
            normalized = item.strip()
            if normalized:
                items.add(normalized)
    return items


def excluded_by_dir(path: Path, repo_root: Path, excluded_dirs: set[str]) -> bool:
    """Return true when any path component belongs to an excluded directory."""
    try:
        parts = path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).parts
    except ValueError:
        parts = path.parts
    return any(part in excluded_dirs for part in parts)


def should_include_python(path: Path, repo_root: Path, excluded_dirs: set[str], excluded_suffixes: set[str]) -> bool:
    """Return true when a path should be counted as source Python."""
    if path.suffix.lower() != ".py":
        return False
    if path.suffix.lower() in excluded_suffixes:
        return False
    return not excluded_by_dir(path, repo_root, excluded_dirs)


def count_lines(path: Path) -> tuple[int, str | None]:
    """Count physical lines in a UTF-8-compatible way."""
    try:
        with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
            return sum(1 for _ in handle), None
    except OSError as exc:
        return 0, f"{type(exc).__name__}: {exc}"


def collect_python_counts(repo_root: Path, excluded_dirs: set[str], excluded_suffixes: set[str]) -> tuple[list[dict[str, Any]], list[str]]:
    """Collect line counts for included Python files."""
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in sorted(repo_root.rglob("*.py"), key=lambda value: repo_rel(repo_root, value).lower()):
        if not should_include_python(path, repo_root, excluded_dirs, excluded_suffixes):
            continue
        lines, error = count_lines(path)
        rel = repo_rel(repo_root, path)
        if error:
            errors.append(f"{rel}: {error}")
            continue
        rows.append({"File": rel, "Lines": lines})
    rows.sort(key=lambda row: (-int(row["Lines"]), str(row["File"]).lower()))
    return rows, errors


def write_csv(rows: list[dict[str, Any]], output: Path) -> None:
    """Write line-count rows to CSV."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["File", "Lines"])
        writer.writeheader()
        writer.writerows(rows)


def top_rows(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """Return the largest files by line count."""
    return rows[: max(limit, 0)]


def build_report(repo_root: Path, rows: list[dict[str, Any]], errors: list[str], csv_path: Path, excluded_dirs: set[str]) -> dict[str, Any]:
    """Build JSON validation/evidence summary for the CSV output."""
    total_lines = sum(int(row["Lines"]) for row in rows)
    return {
        "schema_version": 1,
        "kind": REPORT_KIND,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "csv_written": repo_rel(repo_root, csv_path),
        "file_count": len(rows),
        "total_lines": total_lines,
        "top_files": top_rows(rows, 20),
        "excluded_dirs": sorted(excluded_dirs),
        "guardrails": {
            "report_only": True,
            "source_files_modified": False,
            "providers_executed": False,
            "blender_runtime_executed": False,
            "patches_applied": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render a compact Markdown summary for human review."""
    lines = ["# Python Line Count CSV", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- CSV: `{report['csv_written']}`")
    lines.append(f"- File count: `{report['file_count']}`")
    lines.append(f"- Total lines: `{report['total_lines']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Source writes performed: `{report['source_writes_performed']}`")
    lines.append("")
    lines.append("## Largest Python files")
    lines.append("")
    if not report.get("top_files"):
        lines.append("- none")
    for row in report.get("top_files", []):
        lines.append(f"- `{row['File']}` — `{row['Lines']}` lines")
    lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append("This artifact is line-count evidence only. It is not a patch plan and it must not be committed from `output/**`.")
    return "\n".join(lines) + "\n"


def default_csv_path(repo_root: Path, timestamped: bool) -> Path:
    """Return default CSV path, optionally timestamped."""
    if not timestamped:
        return resolve_output_path(repo_root, DEFAULT_CSV)
    return repo_root / "docs" / "LOCAL_VALIDATION_EVIDENCE" / f"python_line_count_{now_stamp()}.csv"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--csv-output", help="CSV output path. Defaults to docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_latest.csv")
    parser.add_argument("--report-output", default=DEFAULT_REPORT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument("--timestamped", action="store_true", help="Write a timestamped CSV under docs/LOCAL_VALIDATION_EVIDENCE/.")
    parser.add_argument("--exclude-dir", action="append", default=[], help="Additional directory name to exclude; comma-separated values are accepted.")
    parser.add_argument("--include-default-excludes", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    excluded_dirs = set(DEFAULT_EXCLUDED_DIRS) if args.include_default_excludes else set()
    excluded_dirs.update(split_csv_values(args.exclude_dir))
    excluded_suffixes = set(DEFAULT_EXCLUDED_SUFFIXES)
    csv_path = resolve_output_path(repo_root, args.csv_output) if args.csv_output else default_csv_path(repo_root, args.timestamped)

    rows, errors = collect_python_counts(repo_root, excluded_dirs, excluded_suffixes)
    write_csv(rows, csv_path)
    report = build_report(repo_root, rows, errors, csv_path, excluded_dirs)
    write_json_report(report, resolve_output_path(repo_root, args.report_output))
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), end="\n")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
