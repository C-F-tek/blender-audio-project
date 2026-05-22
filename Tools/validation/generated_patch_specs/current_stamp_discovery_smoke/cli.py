#!/usr/bin/env python3
"""Smoke-test generated patch spec discovery does not reuse stale manifests."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def run(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, text=True, check=False, timeout=120
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
        "ok": result.returncode == 0,
    }


def write_stale_manifest(repo: Path) -> Path:
    specs_dir = repo / "output/patch_specs/stale_20260509-102706_specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    spec = specs_dir / "stale.json"
    spec.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "kind": "proposal_patch_spec_draft",
                "operations": [
                    {
                        "operation": "write_file",
                        "path": "docs/LOCAL_AI_TASKS/stale-target.md",
                        "content": "stale\n",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    manifest = repo / "output/patch_specs/stale_20260509-102706_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "kind": "proposal_patch_spec_manifest",
                "specs": [{"path": spec.relative_to(repo).as_posix()}],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return manifest


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Generated Patch Specs Current Stamp Discovery Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        "",
    ]
    for item in report.get("commands", []):
        lines.append(
            f"- `{item['name']}` rc=`{item['result']['returncode']}` ok=`{item['result']['ok']}`"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output",
        default="output/validation/generated_patch_specs_current_stamp_discovery_smoke.json",
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/generated_patch_specs_current_stamp_discovery_smoke.md",
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    commands: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="generated-patch-spec-stamp-smoke-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        run(["git", "init"], repo)
        run(["git", "config", "user.email", "smoke@example.invalid"], repo)
        run(["git", "config", "user.name", "Smoke"], repo)
        (repo / "docs/LOCAL_AI_TASKS").mkdir(parents=True, exist_ok=True)
        (repo / "docs/LOCAL_AI_TASKS/.keep").write_text("", encoding="utf-8")
        run(["git", "add", "."], repo)
        run(["git", "commit", "-m", "seed"], repo)

        stale_manifest = write_stale_manifest(repo)
        current_stamp = "20260509-103204"
        output = f"output/validation/generated_patch_specs_review_pr_apply_{current_stamp}.json"
        command = [
            sys.executable,
            str(source_repo / "ia_carmine/product/generated_patch_specs/apply_cli.py"),
            "--repo-root",
            str(repo),
            "--output",
            output,
            "--apply",
            "--allow-dirty",
            "--create-review-branch",
            f"codex/generated-spec-smoke-{current_stamp}",
            "--allow-dirty-branch",
        ]
        result = run(command, source_repo)
        commands.append(
            {
                "name": "apply_generated_patch_specs_for_review_pr_no_current_manifest",
                "result": result,
            }
        )

        report_path = repo / output
        data = (
            json.loads(report_path.read_text(encoding="utf-8-sig")) if report_path.exists() else {}
        )
        manifest = data.get("manifest") or {}
        if result["returncode"] == 0:
            errors.append("tool unexpectedly passed with only stale manifest available")
        if manifest.get("discovered"):
            errors.append(
                f"stale manifest was discovered unexpectedly: {manifest.get('discovered')}"
            )
        if manifest.get("discovery_filter_stamp") != current_stamp:
            errors.append("current stamp was not inferred from output path")
        if str(stale_manifest.relative_to(repo).as_posix()) == str(manifest.get("path")):
            errors.append("stale manifest was selected as manifest path")
        if data.get("operation_count") not in (None, 0):
            errors.append("stale manifest produced operations unexpectedly")

    report = {
        "schema_version": 1,
        "kind": "generated_patch_specs_current_stamp_discovery_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "commands": commands,
        "errors": errors,
        "warnings": [],
    }
    output_path = resolve_output_path(source_repo, args.output)
    markdown_path = resolve_output_path(source_repo, args.markdown_output)
    print(write_json_report(report, output_path), end="")
    write_text_report(render_markdown(report), markdown_path)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
