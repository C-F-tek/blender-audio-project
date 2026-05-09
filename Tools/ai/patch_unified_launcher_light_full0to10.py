#!/usr/bin/env python3
"""Deprecated report-only shim for the legacy LightFull0To10 launcher patcher.

This tool used to patch run_unified_local_ai_refactor.ps1. That behavior is now
forbidden because Full0To10/LightFull0To10 are legacy compatibility aliases of
the single unified heap/exchange run. The launcher already owns the compatibility
dispatch. This script remains only to produce a migration/deprecation report for
old automation that still invokes it.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--launcher", default="Tools/workflow/run_unified_local_ai_refactor.ps1")
    parser.add_argument("--backup-dir", default="output/validation/unified_launcher_lightfull0to10_patch_deprecated")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo_root).resolve()
    launcher = repo / args.launcher
    report_path = Path(args.report) if args.report else repo / args.backup_dir / "launcher_lightfull0to10_patch_deprecated.json"

    errors: list[str] = []
    warnings = [
        "deprecated tool: launcher patching is disabled",
        "LightFull0To10 is a legacy compatibility alias of the unified run",
        "use Tools/workflow/run_unified_local_ai_refactor.ps1 directly",
    ]

    if args.apply:
        errors.append("--apply is forbidden for this deprecated patcher; no source writes are allowed")
    if not launcher.exists():
        errors.append(f"launcher not found: {launcher}")

    report = {
        "schema_version": 1,
        "kind": "deprecated_unified_launcher_lightfull0to10_patcher",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo.as_posix(),
        "passed": not errors,
        "deprecated": True,
        "quarantined": True,
        "legacy_alias": "LightFull0To10",
        "operational_model": "single_dynamic_heap_exchange_run",
        "standalone_pipeline": False,
        "apply_requested": bool(args.apply),
        "changed": False,
        "launcher": launcher.as_posix(),
        "source_writes_performed": False,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "errors": errors,
        "warnings": warnings,
    }
    write_report(report_path, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
