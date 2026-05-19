"""CLI for agnostic context stack smoke."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report

from .common import run_step
from .defaults import DEFAULT_MARKDOWN, DEFAULT_OUTPUT, DEFAULT_WORK_DIR
from .markdown import render_markdown
from .steps import build_step_specs

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--work-dir", default=DEFAULT_WORK_DIR)
    parser.add_argument("--memory-db", default="indexAI/agent_memory/agent_memory.sqlite")
    parser.add_argument(
        "--objective",
        default="Smoke-test the request-scoped agnostic context stack for megalithic review.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    work_dir = args.work_dir
    step_specs = build_step_specs(args)

    steps = [
        run_step(repo_root, name, command, outputs, args.timeout_seconds, args.dry_run)
        for name, command, outputs in step_specs
    ]
    errors = [f"{step['name']}: {error}" for step in steps for error in step.get("errors", [])]
    report = {
        "schema_version": 1,
        "kind": "agnostic_context_stack_smoke",
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [warning for step in steps for warning in step.get("warnings", [])],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "dry_run": bool(args.dry_run),
        "work_dir": work_dir,
        "step_count": len(steps),
        "steps": steps,
        "guardrails": {
            "provider_execution_default_off": True,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_read_only": True,
            "transient_context_request_scoped": True,
            "output_artifacts_should_not_be_committed": True,
        },
    }

    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
