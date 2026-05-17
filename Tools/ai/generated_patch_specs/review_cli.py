"""CLI for reviewed patch-spec promotion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .review_builder import build_reviewed_spec
from .review_common import DEFAULT_BASENAME, DEFAULT_OUTPUT_DIR, resolve_repo_path, sanitize_filename

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--draft", required=True, help="Draft proposal patch spec JSON.")
    parser.add_argument("--replacement-plan", required=True, help="Explicit replacement plan JSON.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=DEFAULT_BASENAME)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    draft_path = resolve_repo_path(repo_root, args.draft)
    plan_path = resolve_repo_path(repo_root, args.replacement_plan)
    output_dir = resolve_repo_path(repo_root, args.output_dir)
    manifest = build_reviewed_spec(
        repo_root=repo_root,
        draft_path=draft_path,
        plan_path=plan_path,
        output_dir=output_dir,
        basename=sanitize_filename(args.basename),
    )
    print(
        json.dumps(
            {
                "passed": manifest["passed"],
                "manifest_json": manifest["manifest_json"],
                "manifest_markdown": manifest["manifest_markdown"],
                "reviewed_spec": manifest["reviewed_spec"],
                "reviewed_spec_count": manifest["reviewed_spec_count"],
            },
            indent=2,
        )
    )
    return 0 if manifest["passed"] else 2
