from __future__ import annotations

from .builder import build_proposals, proposal_concrete_operation_count, proposals_concrete_operation_count
from .common import *  # noqa: F403
from .markdown import render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--profile", default="core")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=DEFAULT_BASENAME)
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--runtime-report-stamp", default="")
    parser.add_argument("--runtime-report-max-files", type=int, default=40)
    parser.add_argument("--no-discover-runtime-reports", action="store_true")
    parser.add_argument(
        "--require-concrete-proposals",
        action="store_true",
        help="Fail instead of emitting fallback/backlog-only proposals when no concrete_operations are produced.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    explicit_report_paths = split_path_values(list(args.report_file or []))
    stamp = args.runtime_report_stamp or infer_stamp_from_values(
        args.basename, *explicit_report_paths
    )
    runtime_report_paths: list[str] = []
    if not args.no_discover_runtime_reports:
        runtime_report_paths = discover_runtime_report_paths(
            repo_root, stamp, args.runtime_report_max_files
        )

    report_paths = list(DEFAULT_REPORTS) + explicit_report_paths + runtime_report_paths
    loaded_reports = [read_json_if_exists(repo_root / path) for path in dict.fromkeys(report_paths)]
    proposals = build_proposals(
        loaded_reports,
        profile=args.profile,
        require_concrete=bool(args.require_concrete_proposals),
    )
    concrete_operation_count = proposals_concrete_operation_count(proposals)
    errors: list[str] = []
    warnings: list[str] = []
    if args.require_concrete_proposals and concrete_operation_count <= 0:
        errors.append(
            "concrete repository proposals are required for this real-product run, "
            "but no concrete_operations were produced"
        )

    output_dir = repo_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_json = output_dir / f"{args.basename}.json"
    output_md = output_dir / f"{args.basename}.md"

    report = {
        "schema_version": 1,
        "kind": "repository_change_proposals",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "profile": args.profile,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "apply_mode": "manual_review_only",
        "runtime_report_stamp": stamp,
        "runtime_report_paths": runtime_report_paths,
        "concrete_proposals_required": bool(args.require_concrete_proposals),
        "metadata_only_fallback_enabled": not bool(args.require_concrete_proposals),
        "concrete_operation_count": concrete_operation_count,
        "suggestion_contract": {
            "schema_version": 1,
            "supported_output_kinds": list(SUPPORTED_SUGGESTION_OUTPUT_KINDS),
            "default_operation": "manual_patch_suggestion",
            "default_write_policy": "manual_review_only",
            "supported_concrete_operations": sorted(CONCRETE_OPERATION_NAMES),
            "provider_execution_performed": False,
        },
        "reports_read": [item["path"] for item in loaded_reports],
        "proposals": proposals,
    }

    output_json.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    output_md.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": not errors,
                "json": str(output_json),
                "markdown": str(output_md),
                "proposal_count": len(proposals),
                "concrete_operation_count": concrete_operation_count,
                "errors": errors,
            },
            indent=2,
        )
    )
    return 0 if not errors else 2
