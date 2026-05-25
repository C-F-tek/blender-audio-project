"""Scan docs and validators for risky full/complete/product wording."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

WARNING_PATTERNS = (
    re.compile(r"\bfull smoke passed\b", re.IGNORECASE),
    re.compile(r"\bcomplete run passed\b", re.IGNORECASE),
    re.compile(r"\bproduct ready\b", re.IGNORECASE),
    re.compile(r"\bready\b", re.IGNORECASE),
)
HARD_PATTERNS = (
    re.compile(r"\bdegraded\s+(?:is\s+)?(?:passed|success|acceptable)\b", re.IGNORECASE),
    re.compile(r"\bpreflight passed\s*=\s*product\b", re.IGNORECASE),
    re.compile(r"\bartifact exists\s*=\s*success\b", re.IGNORECASE),
    re.compile(r"\bbundle exists\s*=\s*product\b", re.IGNORECASE),
)
NEGATING_WORDS = (
    "must not",
    "not ",
    "invalid",
    "forbidden",
    "fail",
    "fails",
    "unviable",
    "non-product",
    "not proof",
)


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    hard: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for path in _scan_paths(repo_root):
        text = _read(path)
        guardrail_context_remaining = 0
        for line_no, line in enumerate(text.splitlines(), start=1):
            lowered = line.lower()
            if "do not write docs or code that implies" in lowered:
                guardrail_context_remaining = 14
            in_guardrail_context = guardrail_context_remaining > 0
            if guardrail_context_remaining:
                guardrail_context_remaining -= 1
            if not lowered.strip():
                continue
            for pattern in HARD_PATTERNS:
                if pattern.search(line) and not (in_guardrail_context or _is_guardrail_line(lowered)):
                    hard.append(_entry(repo_root, path, line_no, pattern.pattern, line))
            for pattern in WARNING_PATTERNS:
                if pattern.search(line) and not _is_guardrail_line(lowered):
                    warnings.append(_entry(repo_root, path, line_no, pattern.pattern, line))
    warning_limit = 200
    omitted = max(0, len(warnings) - warning_limit)
    report = {
        "schema_version": 1,
        "kind": "full_complete_wording_contract_check",
        "passed": not hard,
        "repo_root": str(repo_root),
        "checked_file_count": len(_scan_paths(repo_root)),
        "hard_violation_count": len(hard),
        "violations": hard,
        "warning_count": len(warnings),
        "warnings": warnings[:warning_limit],
        "warning_omitted_count": omitted,
        "errors": [f"{item['path']}:{item['line']}: {item['text']}" for item in hard],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    _write_report(repo_root, args.output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def _scan_paths(repo_root: Path) -> list[Path]:
    roots = [repo_root / "docs", repo_root / "Tools" / "validation"]
    paths: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for pattern in ("*.md", "*.py"):
            paths.extend(
                path
                for path in root.rglob(pattern)
                if "__pycache__" not in path.parts and "output" not in path.parts
            )
    return sorted(set(paths))


def _is_guardrail_line(line: str) -> bool:
    if any(word in line for word in NEGATING_WORDS):
        return True
    stripped = line.strip()
    return (
        stripped.startswith("do not ")
        or stripped.startswith("never ")
        or stripped.startswith("- do not ")
        or stripped.startswith("- never ")
    )


def _entry(repo_root: Path, path: Path, line: int, pattern: str, text: str) -> dict[str, Any]:
    return {
        "path": _rel(repo_root, path),
        "line": line,
        "pattern": pattern,
        "text": text.strip()[:240],
    }


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


def _write_report(repo_root: Path, output: str, report: dict[str, Any]) -> None:
    if not output:
        return
    path = Path(output)
    if not path.is_absolute():
        path = repo_root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
