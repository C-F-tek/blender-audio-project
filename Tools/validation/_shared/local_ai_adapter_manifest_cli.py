from __future__ import annotations

import argparse
from pathlib import Path

try:
    from check_local_ai_adapter_manifest import (
        resolve_repo_path,
        split_manifest_values,
        validate_manifests,
    )
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ModuleNotFoundError:
    from Tools.validation.check_local_ai_adapter_manifest import (
        resolve_repo_path,
        split_manifest_values,
        validate_manifests,
    )
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", action="append", default=[], help="Manifest path.")
    parser.add_argument("--output", help="Optional JSON validation report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    raw_paths = split_manifest_values(list(args.manifest or []))
    if not raw_paths:
        raw_paths = ["output/local_ai_runs/latest/pipeline/local_ai_task_pipeline_adapter_manifest.json"]
    manifests = [resolve_repo_path(repo_root, raw) for raw in raw_paths]
    report = validate_manifests(repo_root, manifests)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2
