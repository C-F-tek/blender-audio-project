"""CLI for proposal-derived patch specs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .proposal_common import DEFAULT_BASENAME, DEFAULT_OUTPUT_DIR, resolve_repo_path
from .proposal_manifest import build_patch_specs

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--proposal",
        default="output/ai_pipeline/repository_change_proposals.json",
        help="Repository change proposal JSON report.",
    )
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=DEFAULT_BASENAME)
    parser.add_argument("--max-proposals", type=int)
    parser.add_argument(
        "--require-concrete",
        action="store_true",
        help="Fail when generated specs contain no concrete deterministic operations. Disables metadata-only fallback.",
    )
    parser.add_argument(
        "--require-provider-execution",
        action="store_true",
        help="Fail unless the proposal report proves provider_execution_performed=true.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    proposal_path = resolve_repo_path(repo_root, args.proposal)
    output_dir = resolve_repo_path(repo_root, args.output_dir)
    manifest = build_patch_specs(
        repo_root=repo_root,
        proposal_path=proposal_path,
        output_dir=output_dir,
        basename=args.basename,
        max_proposals=args.max_proposals,
        require_concrete=bool(args.require_concrete),
        require_provider_execution=bool(args.require_provider_execution),
    )
    print(
        json.dumps(
            {
                "passed": manifest["passed"],
                "manifest_json": manifest["manifest_json"],
                "manifest_markdown": manifest["manifest_markdown"],
                "patch_spec_count": manifest["patch_spec_count"],
                "concrete_spec_count": manifest["concrete_spec_count"],
                "skipped_target_count": manifest["skipped_target_count"],
            },
            indent=2,
        )
    )
    return 0 if manifest["passed"] else 2
