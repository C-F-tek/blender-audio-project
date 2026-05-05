#!/usr/bin/env python3
"""Check AI workload report quality for one report or a report directory."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - diagnostic report.
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "top-level JSON is not an object"
    return data, None


def quality_for_report(path: Path, repo_root: Path) -> dict[str, Any]:
    data, error = read_json(path)
    rel = path.resolve()
    try:
        rel_text = rel.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        rel_text = path.as_posix()
    if error:
        return {"path": rel_text, "passed": False, "errors": [error], "warnings": []}

    errors = []
    warnings = []
    if data.get("provider_execution_performed") is True and not data.get("provider"):
        warnings.append("provider execution flag is true but provider field is missing")
    if data.get("patch_application_performed") is True:
        errors.append("patch application performed in quality/report lane")
    if "passed" not in data:
        warnings.append("report has no passed field")
    if "kind" not in data and "report_kind" not in data:
        warnings.append("report has no kind/report_kind field")

    return {
        "path": rel_text,
        "passed": not errors,
        "kind": data.get("kind") or data.get("report_kind"),
        "errors": errors,
        "warnings": warnings,
    }


def iter_report_files(report: str | None, report_dir: str | None, repo_root: Path) -> list[Path]:
    if report:
        return [Path(report)]
    if report_dir:
        root = Path(report_dir)
        if not root.is_absolute():
            root = repo_root / root
        return sorted(root.rglob("*.json")) if root.exists() else []
    return []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report")
    parser.add_argument("--report-dir")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    reports = iter_report_files(args.report, args.report_dir, repo_root)
    checks = [quality_for_report(path, repo_root) for path in reports]
    errors = [error for check in checks for error in check["errors"]]
    warnings = [warning for check in checks for warning in check["warnings"]]

    result = {
        "kind": "ai_workload_report_quality",
        "passed": not errors,
        "repo_root": str(repo_root),
        "report": args.report,
        "report_dir": args.report_dir,
        "report_count": len(checks),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "persistent_memory_write_performed": False,
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
