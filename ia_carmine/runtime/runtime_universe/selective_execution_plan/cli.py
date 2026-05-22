"""CLI entrypoint for selective execution plans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .common import (
    DEFAULT_CONTEXT_EVIDENCE,
    DEFAULT_CONTEXT_EVIDENCE_MD,
    DEFAULT_DRY_RUN_EVIDENCE,
    DEFAULT_EXECUTION_PLAN_DIR,
    DEFAULT_PROVIDER_EVIDENCE,
    DEFAULT_TECH_DEBT,
    DEFAULT_VALIDATION_CONTRACT,
    repo_relative,
    resolve_repo_path,
)
from .markdown import render_markdown
from .planner import build_plan

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--context-pack-evidence", default=DEFAULT_CONTEXT_EVIDENCE)
    parser.add_argument("--context-pack-evidence-md", default=DEFAULT_CONTEXT_EVIDENCE_MD)
    parser.add_argument("--dry-run-evidence", default=DEFAULT_DRY_RUN_EVIDENCE)
    parser.add_argument("--provider-evidence", default=DEFAULT_PROVIDER_EVIDENCE)
    parser.add_argument("--validation-report-contract", default=DEFAULT_VALIDATION_CONTRACT)
    parser.add_argument("--execution-plan-dir", default=DEFAULT_EXECUTION_PLAN_DIR)
    parser.add_argument("--tech-debt", default=DEFAULT_TECH_DEBT)
    parser.add_argument("--output", default="output/ai_pipeline/selective_execution_plan.json")
    parser.add_argument(
        "--markdown-output", default="output/ai_pipeline/selective_execution_plan.md"
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    plan = build_plan(args)

    output = resolve_repo_path(repo_root, args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    markdown_output = resolve_repo_path(repo_root, args.markdown_output)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(plan), encoding="utf-8")

    print(
        json.dumps(
            {
                "passed": plan["passed"],
                "kind": plan["kind"],
                "output": repo_relative(output, repo_root),
                "markdown_output": repo_relative(markdown_output, repo_root),
                "provider_execution_performed": False,
                "patch_application_performed": False,
                "recommended_validator_count": len(plan["recommended_validators"]),
                "recommended_patch_spec_count": len(plan["recommended_patch_specs"]),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if plan["passed"] else 2
