#!/usr/bin/env python3
"""Smoke test for the patch suggestion bundle applier.

The smoke is report-only by default. It creates a temporary mini-repository
outside the project tree, runs the applier in dry-run and apply modes against a
synthetic suggestion report, and verifies that only deterministic operations are
applied.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:  # Allows package-style imports during external checks.
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    """Run command and return a compact result."""
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def build_synthetic_repo(tmp: Path, source_repo: Path) -> tuple[Path, Path]:
    """Create a tiny git repository with the applier and validation helpers."""
    repo = tmp / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-b", "codex/smoke"], cwd=repo, check=True, capture_output=True, text=True)

    (repo / "Tools" / "ai").mkdir(parents=True)
    (repo / "Tools" / "validation").mkdir(parents=True)
    (repo / "Tools" / "ai" / "apply_patch_suggestion_bundle.py").write_text(
        (source_repo / "Tools" / "ai" / "apply_patch_suggestion_bundle.py").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (repo / "Tools" / "validation" / "report_utils.py").write_text(
        (source_repo / "Tools" / "validation" / "report_utils.py").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (repo / "sample.md").write_text("# Sample\n\nold text\n", encoding="utf-8")

    suggestion = {
        "schema_version": 1,
        "kind": "synthetic_patch_suggestions",
        "suggestions": [
            {
                "id": "smoke_replace",
                "family": "doc_doc",
                "operation": "replace_once",
                "target_file": "sample.md",
                "find": "old text",
                "replace": "new text",
            },
            {
                "id": "smoke_append",
                "family": "python_doc",
                "operation": "append_once",
                "target_file": "sample.md",
                "marker": "Final phase marker",
                "content": "\nFinal phase marker\n",
            },
            {
                "id": "manual_only",
                "family": "doc_python",
                "rationale": "Natural-language suggestion must remain manual-review only.",
            },
        ],
    }
    suggestion_path = repo / "suggestions.json"
    suggestion_path.write_text(json.dumps(suggestion, indent=2) + "\n", encoding="utf-8")
    return repo, suggestion_path


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/patch_suggestion_bundle_apply_smoke.json")
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    commands: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="patch-suggestion-smoke-") as tmp_raw:
        repo, suggestion_path = build_synthetic_repo(Path(tmp_raw), source_repo)
        dry = run_command(
            [
                sys.executable,
                "Tools/ai/apply_patch_suggestion_bundle.py",
                "--repo-root",
                ".",
                "--suggestion-report",
                suggestion_path.name,
                "--output",
                "dry.json",
            ],
            repo,
        )
        commands.append(dry)
        if dry["returncode"] != 0:
            errors.append("dry-run failed")

        apply = run_command(
            [
                sys.executable,
                "Tools/ai/apply_patch_suggestion_bundle.py",
                "--repo-root",
                ".",
                "--suggestion-report",
                suggestion_path.name,
                "--output",
                "apply.json",
                "--apply",
            ],
            repo,
        )
        commands.append(apply)
        if apply["returncode"] != 0:
            errors.append("apply run failed")

        sample = (repo / "sample.md").read_text(encoding="utf-8")
        apply_report = json.loads((repo / "apply.json").read_text(encoding="utf-8"))
        if "new text" not in sample or "Final phase marker" not in sample:
            errors.append("expected deterministic edits were not applied")
        if apply_report.get("applied_count") != 2:
            errors.append("expected exactly two applied operations")
        if not apply_report.get("manual_review_required"):
            errors.append("manual review was not preserved for natural-language suggestion")

    report = {
        "schema_version": 1,
        "kind": "patch_suggestion_bundle_apply_smoke",
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "commands": commands,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(source_repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
