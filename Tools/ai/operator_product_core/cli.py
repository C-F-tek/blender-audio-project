"""CLI for operator product launcher core."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .io_utils import now_stamp
from .models import DEFAULT_PROFILE, LauncherConfig
from .profiles import build_heap_command, profile_names, resolve_config, run_dir_for
from .runner import analyze_code_product, run_heap, run_operator_lab


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument(
        "--intermediate-root", default="output/validation/operator_product_launcher"
    )
    parser.add_argument("--final-root", default="")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--revision-context", default="auto_latest")
    parser.add_argument("--code-product", default="")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--run-and-review", action="store_true")
    parser.add_argument("--review-code-product", action="store_true")
    parser.add_argument("--apply-safe", action="store_true")
    parser.add_argument("--confirm", default="")
    parser.add_argument("--require-all-integrated", action="store_true")
    parser.add_argument("--list-profiles", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--startup-max-memory-chars", type=int, default=0)
    parser.add_argument("--startup-max-context-files", type=int, default=0)
    parser.add_argument("--startup-scan-context-files", type=int, default=0)
    parser.add_argument("--startup-max-chars-per-file", type=int, default=0)
    parser.add_argument("--context-document-count", type=int, default=0)
    parser.add_argument("--context-document-preview-chars", type=int, default=0)
    parser.add_argument("--semantic-code-chunk-limit", type=int, default=0)
    parser.add_argument("--semantic-code-chunk-preview-chars", type=int, default=0)
    parser.add_argument("--semantic-evidence-chunk-limit", type=int, default=0)
    parser.add_argument("--memory-search-limit", type=int, default=0)
    parser.add_argument("--tool-catalog-limit", type=int, default=0)
    return parser.parse_args()


def build_config(args: argparse.Namespace, repo_root: Path, stamp: str) -> LauncherConfig:
    final_root = args.final_root or str(
        Path.home() / "Documents" / f"aicarmine_operator_launcher_{stamp}"
    )
    request_file = (
        Path(args.request_file) if args.request_file else repo_root / "docs" / "README.md"
    )
    return LauncherConfig(
        repo_root=repo_root,
        request_file=request_file,
        intermediate_root=Path(args.intermediate_root),
        final_root=Path(final_root),
        profile_name=args.profile,
        python_exe=args.python_exe,
        stamp=stamp,
        revision_context=args.revision_context,
        profile_overrides={
            key: value
            for key, value in {
                "startup_max_memory_chars": args.startup_max_memory_chars,
                "startup_max_context_files": args.startup_max_context_files,
                "startup_scan_context_files": args.startup_scan_context_files,
                "startup_max_chars_per_file": args.startup_max_chars_per_file,
                "context_document_count": args.context_document_count,
                "context_document_preview_chars": args.context_document_preview_chars,
                "semantic_code_chunk_limit": args.semantic_code_chunk_limit,
                "semantic_code_chunk_preview_chars": args.semantic_code_chunk_preview_chars,
                "semantic_evidence_chunk_limit": args.semantic_evidence_chunk_limit,
                "memory_search_limit": args.memory_search_limit,
                "tool_catalog_limit": args.tool_catalog_limit,
            }.items()
            if value
        },
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    if args.list_profiles:
        print(json.dumps({"profiles": profile_names(repo_root)}, indent=2))
        return 0
    stamp = args.stamp or now_stamp()
    config = build_config(args, repo_root, stamp)
    if args.apply_safe and args.confirm != "safe_apply":
        raise SystemExit("--apply-safe requires --confirm safe_apply")
    if args.run_and_review:
        report = run_operator_lab(
            config,
            timeout=args.timeout_seconds,
            apply_safe=args.apply_safe,
            require_all_integrated=args.require_all_integrated,
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report.get("passed") else 2
    if args.run:
        report = run_heap(config, timeout=args.timeout_seconds)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report.get("passed") else 2
    code_product = Path(args.code_product)
    if not args.code_product and args.request_file:
        code_product = Path(args.request_file)
    if args.review_code_product or args.apply_safe:
        output_dir = run_dir_for(resolve_config(config))
        report = analyze_code_product(
            repo_root,
            code_product,
            output_dir,
            apply_safe=args.apply_safe,
            require_all_integrated=args.require_all_integrated,
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report.get("passed") else 2
    command = build_heap_command(config)
    print(
        json.dumps(
            {"command": command, "profiles": profile_names(repo_root)}, indent=2, ensure_ascii=False
        )
    )
    return 0
