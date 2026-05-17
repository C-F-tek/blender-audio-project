from __future__ import annotations

import argparse
from pathlib import Path

try:
    from check_ai_context_pack_contract import (
        resolve_repo_path,
        split_path_values,
        validate_ai_context_packs,
    )
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ModuleNotFoundError:
    from Tools.validation.check_ai_context_pack_contract import (
        resolve_repo_path,
        split_path_values,
        validate_ai_context_packs,
    )
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--pack", action="append", default=[], help="Context pack JSON path.")
    parser.add_argument("--evidence", action="append", default=[], help="Context pack evidence JSON path.")
    parser.add_argument("--output", help="Optional JSON validation report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    pack_paths = [resolve_repo_path(repo_root, raw) for raw in split_path_values(list(args.pack or []))]
    evidence_paths = [
        resolve_repo_path(repo_root, raw) for raw in split_path_values(list(args.evidence or []))
    ]
    if not pack_paths and not evidence_paths:
        pack_paths = [repo_root / "output" / "ai_context_packs" / "project_self_improvement.json"]
        evidence_paths = [
            repo_root / "docs" / "LOCAL_VALIDATION_EVIDENCE" / "project_self_improvement_context_pack_evidence.json"
        ]
    report = validate_ai_context_packs(repo_root, pack_paths, evidence_paths)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2
