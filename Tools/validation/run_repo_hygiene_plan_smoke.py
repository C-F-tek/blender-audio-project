#!/usr/bin/env python3
"""Smoke-test repository hygiene planner delete guards."""

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
    lines = ["# Repo Hygiene Plan Smoke", "", f"- Passed: `{report.get('passed')}`", ""]
    for case in report.get("cases") or []:
        lines.append(f"- `{case.get('name')}`: `{case.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def run_planner(source_repo: Path, repo: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    planner = source_repo / "Tools/docs/build_repo_hygiene_plan.py"
    report_path = repo / "output/validation/repo_hygiene_plan.json"
    bundle_path = repo / "patch_specs/repo_hygiene_cleanup/bundle.json"
    result = run(
        [
            sys.executable,
            str(planner),
            "--repo-root",
            str(repo),
            "--output",
            str(report_path.relative_to(repo)),
            "--markdown-output",
            "output/validation/repo_hygiene_plan.md",
            "--emit-patchkit-bundle",
            str(bundle_path.relative_to(repo)),
        ],
        repo,
        source_repo,
    )
    report = json.loads(report_path.read_text(encoding="utf-8-sig")) if report_path.exists() else {}
    bundle = json.loads(bundle_path.read_text(encoding="utf-8-sig")) if bundle_path.exists() else {}
    return result, {"report": report, "bundle": bundle}


def smoke_delete_marker_guards(source_repo: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="repo-hygiene-smoke-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        write(repo / ".git/HEAD", "ref: refs/heads/main\n")
        write(
            repo / "docs/LOCAL_AI_TASKS/README.md/part-001.md",
            "<!-- IA-CARMINE-MD-SPLIT: part -->\n# Current operational README\n\nHistorical wording exists, but this path is protected.\n",
        )
        write(
            repo / "docs/OLD_SPLIT.md/part-001.md",
            "<!-- IA-CARMINE-MD-SPLIT: part -->\n# Old split\n\nHistorical obsolete legacy text without an explicit delete marker.\n",
        )
        write(
            repo / "docs/DELETE_ME.md/part-001.md",
            "<!-- IA-CARMINE-MD-SPLIT: part -->\n# Delete me\n\nStatus: obsolete\nHistorical obsolete legacy split snapshot.\n",
        )
        write(repo / "docs/LOCAL_AI_TASKS/README.md/_ia_carmine_md_split_manifest.json", "{}\n")
        write(repo / "docs/OLD_SPLIT.md/_ia_carmine_md_split_manifest.json", "{}\n")
        write(repo / "docs/DELETE_ME.md/_ia_carmine_md_split_manifest.json", "{}\n")

        result, data = run_planner(source_repo, repo)
        bundle = data["bundle"]
        operations = bundle.get("operations") or []
        targets = [item.get("target") for item in operations]
        markers = {item.get("target"): item.get("required_marker") for item in operations}
        ok = (
            result["returncode"] == 0
            and "docs/DELETE_ME.md/part-001.md" in targets
            and markers.get("docs/DELETE_ME.md/part-001.md") == "Status: obsolete"
            and "docs/OLD_SPLIT.md/part-001.md" not in targets
            and "docs/LOCAL_AI_TASKS/README.md/part-001.md" not in targets
        )
        return {
            "name": "delete_marker_required_and_current_paths_protected",
            "passed": ok,
            "result": result,
            "targets": targets,
            "markers": markers,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/repo_hygiene_plan_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/repo_hygiene_plan_smoke.md")
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    cases = [smoke_delete_marker_guards(source_repo)]
    errors = [f"{case['name']} failed" for case in cases if not case.get("passed")]
    report = {
        "schema_version": 1,
        "kind": "repo_hygiene_plan_smoke",
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
