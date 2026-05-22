#!/usr/bin/env python3
"""Smoke test the runtime universe builder."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

CORE_RUNTIME_GUARD = True

try:
    from ia_carmine.runtime.runtime_universe import RepoRuntimeUniverseBuilder
    from Tools.validation._shared.report_utils import write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.runtime.runtime_universe import RepoRuntimeUniverseBuilder  # type: ignore
    from Tools.validation._shared.report_utils import write_json_report  # type: ignore


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--output", default="output/validation/runtime_universe_smoke.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    universe = RepoRuntimeUniverseBuilder(repo_root, args.run_dir or None).build()
    summary = universe.summary()
    errors: list[str] = []
    if summary["source_count"] <= 0:
        errors.append("source index is empty")
    if summary["validation_count"] <= 0:
        errors.append("validation index is empty")
    if not any(item.startswith("Tools/") for item in universe.source_index):
        errors.append("tools source coverage is missing from universe")
    if not any(not item.startswith("Tools/") for item in universe.file_index):
        errors.append("non-Tools repository coverage is missing from universe")
    report = {
        "schema_version": 1,
        "kind": "runtime_universe_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": not errors,
        "errors": errors,
        "summary": summary,
        "source_writes_performed": False,
        "patch_application_performed": False,
    }
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
