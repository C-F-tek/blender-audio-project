"""CLI for reviewed patch-spec contract validation."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report

from .common import split_path_values, resolve_repo_path
from .validators import validate_reviewed_patch_specs

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", action="append", default=[])
    parser.add_argument("--spec", action="append", default=[])
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
        manifest_paths = [repo_root / "output/patch_specs/reviewed_patch_spec_manifest.json"]

    report = validate_reviewed_patch_specs(repo_root, manifest_paths, spec_paths)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
