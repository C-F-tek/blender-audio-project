#!/usr/bin/env python3
"""Smoke test for the patch suggestion bundle applier.

The smoke is report-only by default. It creates a temporary mini-repository
outside the project tree, runs the applier in dry-run and apply modes against a
synthetic stamped suggestion report plus current proposal reports, and verifies
that only deterministic operations are applied.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:  # Allows package-style imports during external checks.
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


SMOKE_STAMP = "20990101-010203"
STREAM_PREVIEW_CHARS = 1200


def stream_summary(text: str) -> dict[str, Any]:
    """Return a compact stream preview for nested smoke commands."""
    return {
        "chars": len(text),
        "preview": text[:STREAM_PREVIEW_CHARS],
        "truncated": len(text) > STREAM_PREVIEW_CHARS,
    }


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    """Run command and return a compact result."""
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, check=False)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": stream_summary(result.stdout),
        "stderr": stream_summary(result.stderr),
    }


def build_synthetic_repo(tmp: Path, source_repo: Path) -> tuple[Path, Path]:
    """Create a tiny git repository with the applier and validation helpers."""
    repo = tmp / "repo"
    repo.mkdir()
    subprocess.run(
        ["git", "init", "-b", "codex/smoke"], cwd=repo, check=True, capture_output=True, text=True
    )

    (repo / "Tools" / "ai").mkdir(parents=True)
    (repo / "Tools" / "validation").mkdir(parents=True)
    (repo / "docs" / "LOCAL_VALIDATION_EVIDENCE").mkdir(parents=True)
    (repo / "output" / "ai_pipeline").mkdir(parents=True)
    (repo / "Tools" / "ai" / "apply_patch_suggestion_bundle.py").write_text(
        (source_repo / "Tools" / "ai" / "apply_patch_suggestion_bundle.py").read_text(
            encoding="utf-8"
        ),
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
        ],
    }
    suggestion_path = (
        repo / "docs" / "LOCAL_VALIDATION_EVIDENCE" / f"patch_suggestion_smoke_{SMOKE_STAMP}.json"
    )
    suggestion_path.write_text(json.dumps(suggestion, indent=2) + "\n", encoding="utf-8")

    current_suggestions = {
        "schema_version": 1,
        "kind": "repository_change_proposals",
        "proposals": [
            {
                "proposal_id": "P-SMOKE-MANUAL",
                "priority": "P2",
                "area": "docs",
                "title": "Manual review proposal must not auto-apply",
                "target_files": ["README.md"],
                "patch_sketch": ["Add a reviewed documentation note to README.md."],
                "validation_commands": ["git diff --check"],
                "suggestion_outputs": [
                    {
                        "path": "README.md",
                        "artifact_kind": "markdown",
                        "operation": "manual_patch_suggestion",
                        "content_status": "proposal_only",
                        "write_policy": "manual_review_only",
                    }
                ],
            }
        ],
    }
    (repo / "output" / "ai_pipeline" / "repository_change_proposals.json").write_text(
        json.dumps(current_suggestions, indent=2) + "\n",
        encoding="utf-8",
    )
    current_update_suggestions = {
        "schema_version": 1,
        "kind": "post_validation_ai_work_packet",
        "suggestions": [
            {
                "priority": "P1",
                "area": "validation",
                "title": "Auxiliary validation signal must stay supplemental",
                "details": "output/validation/local_provider_probe.json: ['provider probe failed']",
            }
        ],
    }
    (repo / "output" / "ai_pipeline" / "repository_update_suggestions.json").write_text(
        json.dumps(current_update_suggestions, indent=2) + "\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "config", "user.email", "smoke@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Patch Suggestion Smoke"], cwd=repo, check=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "commit", "-m", "seed synthetic repo"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return repo, suggestion_path


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/patch_suggestion_bundle_apply_smoke.json"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    commands: list[dict[str, Any]] = []
    discovered_reports: list[str] = []
    current_reports: list[str] = []

    with tempfile.TemporaryDirectory(prefix="patch-suggestion-smoke-") as tmp_raw:
        repo, suggestion_path = build_synthetic_repo(Path(tmp_raw), source_repo)
        dry_output = Path(tmp_raw) / "dry.json"
        apply_output = Path(tmp_raw) / "apply.json"
        dry = run_command(
            [
                sys.executable,
                "ia_carmine/product/patch_product/patch_suggestion_bundle/cli.py",
                "--repo-root",
                ".",
                "--Stamp",
                SMOKE_STAMP,
                "--output",
                str(dry_output),
            ],
            repo,
        )
        commands.append(dry)
        if dry["returncode"] != 0:
            errors.append("dry-run failed")

        apply = run_command(
            [
                sys.executable,
                "ia_carmine/product/patch_product/patch_suggestion_bundle/cli.py",
                "--repo-root",
                ".",
                "--Stamp",
                SMOKE_STAMP,
                "--output",
                str(apply_output),
                "--apply",
            ],
            repo,
        )
        commands.append(apply)
        if apply["returncode"] != 0:
            errors.append("apply run failed")

        sample = (repo / "sample.md").read_text(encoding="utf-8")
        apply_report = json.loads(apply_output.read_text(encoding="utf-8"))
        discovered_reports = apply_report.get("discovered_reports") or []
        current_reports = apply_report.get("current_suggestion_reports") or []
        manual_items = apply_report.get("manual_review_items") or []
        manual_product = apply_report.get("manual_review_product") or {}
        if suggestion_path.relative_to(repo).as_posix() not in discovered_reports:
            errors.append("stamped suggestion report was not discovered")
        if "output/ai_pipeline/repository_change_proposals.json" not in current_reports:
            errors.append("current non-stamped proposal report was not discovered")
        if "output/ai_pipeline/repository_update_suggestions.json" not in current_reports:
            errors.append("current non-stamped update suggestion report was not discovered")
        if "new text" not in sample or "Final phase marker" not in sample:
            errors.append("expected deterministic edits were not applied")
        if apply_report.get("applied_count") != 2:
            errors.append("expected exactly two applied operations")
        if not apply_report.get("manual_review_required") or not manual_items:
            errors.append("manual review was not preserved for proposal-only suggestion")
        if manual_product.get("product_facing_manual_review_count") != 1:
            errors.append("expected one product-facing manual review proposal")
        if not manual_product.get("supplemental_manual_review_count"):
            errors.append("expected supplemental debug/evidence suggestions to be separated")
        if apply_report.get("patch_product_status") != "deterministic_patch_operations_ready":
            errors.append("expected deterministic patch product readiness")
        if any(item.get("family") == "synthetic_patch_suggestions" for item in manual_items):
            errors.append("report container was incorrectly classified as manual review item")

    report = {
        "schema_version": 1,
        "kind": "patch_suggestion_bundle_apply_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "smoke_stamp": SMOKE_STAMP,
        "discovered_reports": discovered_reports,
        "current_suggestion_reports": current_reports,
        "commands": commands,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(source_repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
