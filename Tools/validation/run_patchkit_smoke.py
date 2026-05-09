#!/usr/bin/env python3
"""Smoke-test the reusable controlled patchkit runner."""
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
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


def env_for(source_repo: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(source_repo) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def run(command: list[str], cwd: Path, source_repo: Path) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, env=env_for(source_repo), capture_output=True, text=True, check=False, timeout=120)
    return {"command": command, "returncode": result.returncode, "stdout_tail": result.stdout[-6000:], "stderr_tail": result.stderr[-6000:], "ok": result.returncode == 0}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def init_git_repo(repo: Path, source_repo: Path) -> list[dict[str, Any]]:
    commands = [
        ["git", "init"],
        ["git", "config", "user.email", "patchkit-smoke@example.invalid"],
        ["git", "config", "user.name", "Patchkit Smoke"],
        ["git", "add", "."],
        ["git", "commit", "-m", "initial smoke fixture"],
    ]
    return [run(command, repo, source_repo) for command in commands]


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Patchkit Smoke", "", f"- Passed: `{report.get('passed')}`", ""]
    for case in report.get("cases") or []:
        lines.append(f"- `{case.get('name')}`: `{case.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/patchkit_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/patchkit_smoke.md")
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    runner = source_repo / "Tools/ai/patchkit/apply_patch_bundle.py"
    cases: list[dict[str, Any]] = []
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="patchkit-smoke-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        target = repo / "target.ps1"
        write(target, "Write-Host 'before'\nInvoke-Checked \"Demo phase\" {\n    Write-Host 'demo'\n}\nWrite-Host 'after'\n")
        bundle_dir = repo / "patch_specs/demo"
        fragment = bundle_dir / "fragment.ps1"
        write(fragment, "# PATCHKIT-SMOKE-FRAGMENT\nWrite-Host 'inserted by patchkit'\n")
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
                            "marker": "PATCHKIT-SMOKE-FRAGMENT",
                            "content_file": "fragment.ps1",
                        },
                        {"operation": "assert_marker", "target": "target.ps1", "required_marker": "PATCHKIT-SMOKE-FRAGMENT"},
                        {"operation": "assert_no_naked_throw", "target": "target.ps1"},
                    ],
                    "validators": ["powershell_parser", "git_diff_check"],
                },
                indent=2,
            )
            + "\n",
        )
        git_setup = init_git_repo(repo, source_repo)
        dry = run([sys.executable, str(runner), "--repo-root", str(repo), "--bundle", str(bundle), "--dry-run"], repo, source_repo)
        apply = run([sys.executable, str(runner), "--repo-root", str(repo), "--bundle", str(bundle)], repo, source_repo)
        second = run([sys.executable, str(runner), "--repo-root", str(repo), "--bundle", str(bundle)], repo, source_repo)
        target_text = target.read_text(encoding="utf-8")
        ok = (
            all(item["returncode"] == 0 for item in git_setup)
            and dry["returncode"] == 0
            and apply["returncode"] == 0
            and second["returncode"] == 0
            and target_text.count("PATCHKIT-SMOKE-FRAGMENT") == 1
        )
        cases.append({"name": "dry_apply_idempotent_patch_bundle", "passed": ok, "git_setup": git_setup, "dry": dry, "apply": apply, "second": second})
        if not ok:
            errors.append("patchkit dry/apply/idempotency smoke failed")

    report = {
        "schema_version": 1,
        "kind": "patchkit_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "cases": cases,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(source_repo, args.output)
    markdown = resolve_output_path(source_repo, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
