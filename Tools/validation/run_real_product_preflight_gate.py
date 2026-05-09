#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


PREVIEW_CHARS = 4000


def stream(text: str) -> dict[str, Any]:
    return {
        "chars": len(text),
        "preview": text[:PREVIEW_CHARS],
        "truncated": len(text) > PREVIEW_CHARS,
    }


def run_step(repo_root: Path, name: str, script: str, timeout_seconds: int) -> dict[str, Any]:
    output = repo_root / "output/validation" / f"real_product_preflight_{name}.json"
    command = [
        sys.executable,
        str(repo_root / script),
        "--repo-root",
        str(repo_root),
        "--output",
        str(output),
    ]

    if name == "full_product_pr_chain":
        command.extend(["--timeout-seconds", str(timeout_seconds)])

    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        command,
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout_seconds,
    )

    report: dict[str, Any] = {}
    if output.exists():
        try:
            report = json.loads(output.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # noqa: BLE001
            report = {
                "passed": False,
                "errors": [f"failed to parse step report: {type(exc).__name__}: {exc}"],
            }

    return {
        "name": name,
        "script": script,
        "output": output.as_posix(),
        "returncode": result.returncode,
        "passed": result.returncode == 0 and report.get("passed") is True,
        "report_passed": report.get("passed"),
        "report_kind": report.get("kind"),
        "report_errors": report.get("errors") or [],
        "report_warnings": report.get("warnings") or [],
        "stdout": stream(result.stdout),
        "stderr": stream(result.stderr),
    }


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = [
        "# Real Product Preflight Gate",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Generated at: `{report.get('generated_at')}`",
        f"- Step count: `{len(report.get('steps') or [])}`",
        f"- Failed step count: `{len(report.get('failed_steps') or [])}`",
        "",
        "## Steps",
        "",
    ]
    for step in report.get("steps") or []:
        lines.append(f"- `{step.get('name')}`: passed=`{step.get('passed')}`, rc=`{step.get('returncode')}`, script=`{step.get('script')}`")
    if report.get("failed_steps"):
        lines.extend(["", "## Failed steps", ""])
        for step in report["failed_steps"]:
            lines.append(f"- `{step.get('name')}`")
            for err in step.get("report_errors") or []:
                lines.append(f"  - {err}")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return write_text_report("\n".join(lines) + "\n", output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/real_product_preflight_gate.json")
    parser.add_argument("--markdown-output", default="output/validation/real_product_preflight_gate.md")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    steps_config = [
        ("real_product_profile", "Tools/validation/run_real_product_profile_smoke.py"),
        ("intrinsic_capability_contract", "Tools/validation/run_real_product_intrinsic_capability_contract_smoke.py"),
        ("runtime_mesh_contract", "Tools/validation/run_real_product_runtime_mesh_contract_smoke.py"),
        ("openvino_peer_topology", "Tools/validation/run_openvino_peer_topology_contract_smoke.py"),
        ("review_pr_prepare_args", "Tools/validation/run_review_pr_prepare_args_smoke.py"),
        ("review_pr_product_readiness", "Tools/validation/run_review_pr_product_readiness_smoke.py"),
        ("full_product_pr_chain", "Tools/validation/run_full0to10_product_pr_chain_smoke.py"),
    ]

    steps: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []

    for name, script in steps_config:
        script_path = repo_root / script
        if not script_path.exists():
            step = {
                "name": name,
                "script": script,
                "returncode": 127,
                "passed": False,
                "report_errors": [f"missing preflight script: {script}"],
                "report_warnings": [],
                "stdout": stream(""),
                "stderr": stream(""),
            }
        else:
            step = run_step(repo_root, name, script, args.timeout_seconds)
        steps.append(step)
        if not step.get("passed"):
            errors.append(f"preflight step failed: {name}")

    failed_steps = [step for step in steps if not step.get("passed")]

    report = {
        "schema_version": 1,
        "kind": "real_product_preflight_gate",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not failed_steps,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "blender_runtime_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "steps": steps,
        "failed_steps": failed_steps,
        "errors": errors,
        "warnings": warnings,
    }

    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_markdown(report, markdown_output)
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
