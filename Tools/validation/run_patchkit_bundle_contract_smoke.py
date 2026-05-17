#!/usr/bin/env python3
"""Smoke-test the PatchKit bundle contract validator."""

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
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def env_for(source_repo: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(source_repo) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    return env


def run(command: list[str], cwd: Path, source_repo: Path) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env_for(source_repo),
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
        "ok": result.returncode == 0,
    }


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# PatchKit Bundle Contract Smoke", "", f"- Passed: `{report.get('passed')}`", ""]
    for case in report.get("cases") or []:
        lines.append(f"- `{case.get('name')}`: `{case.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def smoke_valid_bundle(source_repo: Path, validator: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="patchkit-contract-valid-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        target = repo / "target.ps1"
        write(target, "Write-Host 'before'\nInvoke-Checked \"Demo phase\" { Write-Host 'demo' }\n")
        bundle_dir = repo / "patch_specs/demo"
        write(bundle_dir / "fragment.ps1", "# DEMO-MARKER\nWrite-Host 'inserted'\n")
        bundle = bundle_dir / "bundle.json"
        write(
            bundle,
            json.dumps(
                {
                    "schema_version": 1,
                    "kind": "codemod_patch_bundle",
                    "operations": [
                        {
                            "operation": "insert_after_invoke_checked",
                            "target": "target.ps1",
                            "label": "Demo phase",
                            "marker": "DEMO-MARKER",
                            "content_file": "fragment.ps1",
                        },
                        {
                            "operation": "assert_marker",
                            "target": "target.ps1",
                            "required_marker": "Invoke-Checked",
                        },
                    ],
                    "validators": ["powershell_parser", "git_diff_check"],
                },
                indent=2,
            )
            + "\n",
        )
        result = run(
            [sys.executable, str(validator), "--repo-root", str(repo), "--bundle", str(bundle)],
            repo,
            source_repo,
        )
        return {
            "name": "valid_patchkit_bundle_contract",
            "passed": result["returncode"] == 0,
            "result": result,
        }


def smoke_invalid_delete_bundle(source_repo: Path, validator: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="patchkit-contract-invalid-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        bundle = repo / "patch_specs/bad_delete/bundle.json"
        write(
            bundle,
            json.dumps(
                {
                    "schema_version": 1,
                    "kind": "codemod_patch_bundle",
                    "operations": [
                        {
                            "operation": "delete_file",
                            "target": "output/bad.md",
                            "allow_delete": False,
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
        )
        result = run(
            [sys.executable, str(validator), "--repo-root", str(repo), "--bundle", str(bundle)],
            repo,
            source_repo,
        )
        ok = result["returncode"] != 0 and "delete_file requires allow_delete=true" in (
            result["stdout_tail"] + result["stderr_tail"]
        )
        return {"name": "invalid_delete_bundle_blocked", "passed": ok, "result": result}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/patchkit_bundle_contract_smoke.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/patchkit_bundle_contract_smoke.md"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    validator = source_repo / "Tools/validation/check_patchkit_bundle_contract.py"
    cases = [
        smoke_valid_bundle(source_repo, validator),
        smoke_invalid_delete_bundle(source_repo, validator),
    ]
    errors = [f"{case['name']} failed" for case in cases if not case.get("passed")]
    report = {
        "schema_version": 1,
        "kind": "patchkit_bundle_contract_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "cases": cases,
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(source_repo, args.output)), end="")
    write_text_report(
        render_markdown(report), resolve_output_path(source_repo, args.markdown_output)
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
