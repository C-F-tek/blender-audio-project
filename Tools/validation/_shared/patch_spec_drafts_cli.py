from __future__ import annotations

import argparse
from pathlib import Path

try:
    from check_patch_spec_drafts import (
        resolve_repo_path,
        split_path_values,
        validate_patch_spec_drafts,
    )
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ModuleNotFoundError:
    from Tools.validation.check_patch_spec_drafts import (
        resolve_repo_path,
        split_path_values,
        validate_patch_spec_drafts,
    )
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", action="append", default=[], help="Patch spec draft manifest path.")
    parser.add_argument("--spec", action="append", default=[], help="Patch spec draft JSON path.")
    parser.add_argument("--output", help="Optional JSON validation report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest_paths = [
        resolve_repo_path(repo_root, raw) for raw in split_path_values(list(args.manifest or []))
    ]
    spec_paths = [
        resolve_repo_path(repo_root, raw) for raw in split_path_values(list(args.spec or []))
    ]
    if not manifest_paths and not spec_paths:
        manifest_paths = [repo_root / "output/patch_specs/proposal_patch_specs_manifest.json"]
    report = validate_patch_spec_drafts(repo_root, manifest_paths, spec_paths)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2
