#!/usr/bin/env python3
"""Validate local Markdown links in repository documentation.

The validator checks repository-local Markdown links and ignores external URLs,
anchors-only links, mailto links and images.

Generated evidence under docs/LOCAL_VALIDATION_EVIDENCE/ is treated as
nonfatal by default because compact evidence bundles may intentionally reference
local-only chunk/runbook directories that are not committed.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".repo_patch_backups",
    "renders",
    "output",
}

DEFAULT_NONFATAL_PREFIXES = ("docs/LOCAL_VALIDATION_EVIDENCE/",)

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def is_excluded(path: Path, repo_root: Path, excludes: set[str]) -> bool:
    try:
        parts = path.relative_to(repo_root).parts
    except ValueError:
        parts = path.parts
    return any(part in excludes for part in parts)


def iter_markdown_files(repo_root: Path, excludes: set[str]) -> list[Path]:
    """Return Markdown files and expand policy split directories.

    The repository can contain Markdown split containers named like
    ``name.md/README.md`` and ``name.md/part-001.md``. ``Path.rglob("*.md")``
    can match both real Markdown files and these ``*.md`` directories. The
    validator must inspect the path type before reading:

    - if it is a file, read it normally;
    - if it is a directory, enter it and read the Markdown files inside.
    """
    files: dict[str, Path] = {}
    for path in repo_root.rglob("*.md"):
        if is_excluded(path, repo_root, excludes):
            continue
        if path.is_file():
            files[path.resolve().as_posix()] = path
            continue
        if path.is_dir():
            for nested in sorted(path.rglob("*.md")):
                if nested.is_file() and not is_excluded(nested, repo_root, excludes):
                    files[nested.resolve().as_posix()] = nested
    return [files[key] for key in sorted(files)]


def is_external_link(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("tel:")
    )


def normalize_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target:
        target = target.split(" ", 1)[0]
    if "#" in target:
        target = target.split("#", 1)[0]
    return unquote(target.strip())


def normalized_prefix(value: str) -> str:
    return value.replace("\\", "/").strip().lstrip("./")


def is_nonfatal_source(path: str, prefixes: tuple[str, ...]) -> bool:
    normalized = normalized_prefix(path)
    return any(normalized.startswith(prefix) for prefix in prefixes)


def inspect_markdown(
    path: Path, repo_root: Path, nonfatal_prefixes: tuple[str, ...]
) -> dict[str, Any]:
    rel = path.relative_to(repo_root).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    broken: list[dict[str, Any]] = []
    checked = 0
    skipped = 0
    nonfatal = is_nonfatal_source(rel, nonfatal_prefixes)

    for match in LINK_RE.finditer(text):
        raw = match.group(1)
        target = normalize_target(raw)
        if not target or target.startswith("#") or is_external_link(target):
            skipped += 1
            continue
        if (
            target.startswith(".")
            or "/" in target
            or target.endswith((".md", ".py", ".json", ".ps1", ".yml", ".yaml", ".txt"))
        ):
            checked += 1
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(repo_root)
            except ValueError:
                broken.append({"target": raw, "reason": "outside_repo", "fatal": not nonfatal})
                continue
            if not candidate.exists():
                broken.append({"target": raw, "reason": "missing", "fatal": not nonfatal})
        else:
            skipped += 1

    return {
        "path": rel,
        "ok": not broken,
        "fatal": bool(broken and not nonfatal),
        "nonfatal": bool(broken and nonfatal),
        "checked_links": checked,
        "skipped_links": skipped,
        "broken_links": broken,
    }


def build_report(
    repo_root: Path, excludes: set[str], nonfatal_prefixes: tuple[str, ...]
) -> dict[str, Any]:
    files = iter_markdown_files(repo_root, excludes)
    results = [inspect_markdown(path, repo_root, nonfatal_prefixes) for path in files]
    failed = [item for item in results if not item["ok"]]
    fatal_failed = [item for item in failed if item.get("fatal")]
    nonfatal_failed = [item for item in failed if item.get("nonfatal")]

    errors = [
        f"{item['path']}: {broken['target']} ({broken['reason']})"
        for item in fatal_failed
        for broken in item["broken_links"]
        if broken.get("fatal", True)
    ]
    warnings = [
        f"{item['path']}: {broken['target']} ({broken['reason']}; nonfatal_generated_evidence)"
        for item in nonfatal_failed
        for broken in item["broken_links"]
    ]

    return {
        "schema_version": 1,
        "kind": "docs_links",
        "repo_root": str(repo_root),
        "file_count": len(results),
        "failed_count": len(failed),
        "fatal_failed_count": len(fatal_failed),
        "nonfatal_failed_count": len(nonfatal_failed),
        "broken_link_count": sum(len(item["broken_links"]) for item in failed),
        "fatal_broken_link_count": len(errors),
        "nonfatal_broken_link_count": len(warnings),
        "passed": not fatal_failed,
        "errors": errors,
        "warnings": warnings,
        "nonfatal_prefixes": list(nonfatal_prefixes),
        "guardrails": {
            "generated_validation_evidence_links_are_nonfatal": True,
            "source_documentation_links_remain_fatal": True,
        },
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", help="Optional JSON report path.")
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument(
        "--nonfatal-prefix",
        action="append",
        default=list(DEFAULT_NONFATAL_PREFIXES),
        help="Repo-relative Markdown path prefix whose broken local links are warnings instead of fatal errors.",
    )
    parser.add_argument(
        "--strict-local-validation-evidence",
        action="store_true",
        help="Treat docs/LOCAL_VALIDATION_EVIDENCE broken links as fatal, restoring strict historical behavior.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    excludes = set(DEFAULT_EXCLUDES)
    excludes.update(args.exclude)

    nonfatal_prefixes = tuple(
        prefix
        for prefix in (normalized_prefix(item).rstrip("/") + "/" for item in args.nonfatal_prefix)
        if prefix
    )
    if args.strict_local_validation_evidence:
        nonfatal_prefixes = tuple(
            prefix for prefix in nonfatal_prefixes if prefix != "docs/LOCAL_VALIDATION_EVIDENCE/"
        )

    report = build_report(repo_root, excludes, nonfatal_prefixes)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
