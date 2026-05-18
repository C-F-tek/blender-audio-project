from __future__ import annotations

import argparse
from pathlib import Path

try:
    from check_github_evidence_bundle import (
        default_bundle_paths,
        split_path_values,
        validate_github_evidence_bundles,
    )
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ModuleNotFoundError:
    from Tools.validation._shared.github_evidence_bundle_cli import (
        default_bundle_paths,
        split_path_values,
        validate_github_evidence_bundles,
    )
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--bundle", action="append", default=[], help="Bundle JSON path.")
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    raw_bundles = split_path_values(list(args.bundle or []))
    if raw_bundles:
        paths = [
            Path(item).resolve() if Path(item).is_absolute() else (repo_root / item).resolve()
            for item in raw_bundles
        ]
    else:
        paths = default_bundle_paths(repo_root)
    report = validate_github_evidence_bundles(repo_root, paths)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2
