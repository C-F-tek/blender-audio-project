#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/generated_patch_specs_empty_product_smoke.json"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="generated-patch-empty-product-") as temp_dir:
        repo = Path(temp_dir) / "repo"
        repo.mkdir(parents=True)
        (repo / "Tools/example.py").parent.mkdir(parents=True)
        (repo / "Tools/example.py").write_text("VALUE = 1\n", encoding="utf-8")
        subprocess.run(["git", "init"], cwd=repo, capture_output=True, text=True, check=False)
        subprocess.run(
            ["git", "config", "user.email", "smoke@example.invalid"], cwd=repo, check=False
        )
        subprocess.run(["git", "config", "user.name", "Smoke"], cwd=repo, check=False)
        subprocess.run(["git", "add", "."], cwd=repo, check=False)
        subprocess.run(
            ["git", "commit", "-m", "init"], cwd=repo, capture_output=True, text=True, check=False
        )
        spec = repo / "output/patch_specs/spec.json"
        manifest = repo / "output/patch_specs/spec_manifest.json"
        write_json(
            spec,
            {
                "kind": "proposal_patch_spec_draft",
                "operations": [
                    {
                        "proposal_id": "P-EMPTY",
                        "operation": "manual_patch_suggestion",
                        "path": "Tools/example.py",
                        "draft_status": "needs_concrete_replacements",
                        "replacements": [],
                    }
                ],
            },
        )
        write_json(
            manifest,
            {
                "kind": "proposal_patch_spec_manifest",
                "specs": [{"path": "output/patch_specs/spec.json"}],
            },
        )
        out = repo / "output/validation/apply.json"
        cmd = [
            "python",
            str(source_repo / "Tools/ai/apply_generated_patch_specs_for_review_pr.py"),
            "--repo-root",
            str(repo),
            "--manifest",
            "output/patch_specs/spec_manifest.json",
            "--output",
            str(out),
            "--apply",
            "--allow-dirty",
            "--create-review-branch",
            "codex/empty-product-smoke",
            "--allow-dirty-branch",
        ]
        proc = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, check=False)
        apply_report = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}

    if proc.returncode == 0:
        errors.append("metadata-only generated patch specs should fail under --apply")
    if apply_report.get("passed") is not False:
        errors.append("apply report should be passed=false for metadata-only specs")
    if apply_report.get("operation_count") != 0:
        errors.append("metadata-only specs should have operation_count=0")
    if not apply_report.get("errors"):
        errors.append("metadata-only specs should emit a concrete-product error")
    if apply_report.get("patch_application_performed") is not False:
        errors.append("metadata-only specs should not report patch_application_performed")

    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "generated_patch_specs_empty_product_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "case": {
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
            "apply_report": apply_report,
        },
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(source_repo, args.output)), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
