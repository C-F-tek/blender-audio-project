#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai._shared.process_tree import terminate_process_tree
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.ai._shared.process_tree import terminate_process_tree  # type: ignore
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


PREVIEW_CHARS = 4000


def stream(text: str) -> dict[str, Any]:
    return {
        "chars": len(text),
        "preview": text[:PREVIEW_CHARS],
        "truncated": len(text) > PREVIEW_CHARS,
    }


def run_step(repo_root: Path, name: str, script: str, timeout_seconds: int) -> dict[str, Any]:
    started = time.time()
    output = repo_root / "output/validation" / f"real_product_preflight_{name}.json"
    command = [
        sys.executable,
        str(repo_root / script),
        "--repo-root",
        str(repo_root),
        "--output",
        str(output),
    ]

    process_timeout = timeout_seconds
    if name in {"full_product_pr_chain", "heap_runtime_completeness_gate"}:
        command.extend(["--timeout-seconds", str(timeout_seconds)])
    if name == "heap_runtime_completeness_gate":
        command.append("--contract-only")
    if name == "provider_lane_activation":
        command.extend(
            [
                "--markdown-output",
                str(output.with_suffix(".md")),
                "--model",
                "qwen3-coder:latest",
                "--timeout",
                str(max(10, min(timeout_seconds, 60))),
                "--parallel",
                "--require-lane",
                "ollama",
                "--require-lane",
                "gpu",
                "--require-lane",
                "npu",
            ]
        )

    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    process: subprocess.Popen[str] | None = None
    timed_out = False
    try:
        process = subprocess.Popen(
            command,
            cwd=repo_root,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(timeout=process_timeout)
        returncode = process.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
        if process is not None:
            terminate_process_tree(process)
            stdout, stderr = process.communicate()
        else:
            stdout, stderr = "", ""
        returncode = -9

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
        "returncode": returncode,
        "passed": returncode == 0 and report.get("passed") is True,
        "timeout": timed_out,
        "process_tree_terminated": timed_out and process is not None,
        "process_timeout_seconds": process_timeout,
        "elapsed_seconds": round(max(0.0, time.time() - started), 3),
        "report_passed": report.get("passed"),
        "report_kind": report.get("kind"),
        "report_errors": report.get("errors") or [],
        "report_warnings": report.get("warnings") or [],
        "stdout": stream(stdout or ""),
        "stderr": stream(stderr or ""),
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
        lines.append(
            f"- `{step.get('name')}`: passed=`{step.get('passed')}`, rc=`{step.get('returncode')}`, script=`{step.get('script')}`"
        )
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


def write_progress(
    *,
    repo_root: Path,
    output: Path,
    steps: list[dict[str, Any]],
    current_step: str,
    step_index: int,
    step_count: int,
) -> None:
    report = {
        "schema_version": 1,
        "kind": "real_product_preflight_gate",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "status": "running",
        "current_step": current_step,
        "step_index": step_index,
        "step_count": step_count,
        "completed_step_count": len(steps),
        "passed": False,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "blender_runtime_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "steps": steps,
        "failed_steps": [step for step in steps if not step.get("passed")],
        "errors": [],
        "warnings": [],
    }
    write_json_report(report, output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/real_product_preflight_gate.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/real_product_preflight_gate.md"
    )
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    steps_config = [
        ("real_product_profile", "Tools/validation/real_product/profile_smoke/cli.py"),
        ("core_runtime_guard_suite", "Tools/validation/runtime_universe/run_core_runtime_guard_suite/cli.py"),
        (
            "real_product_single_entry_exit",
            "Tools/validation/real_product/single_entry_exit_smoke/cli.py",
        ),
        (
            "intrinsic_capability_contract",
            "Tools/validation/real_product/intrinsic_capability_contract_smoke/cli.py",
        ),
        (
            "runtime_mesh_contract",
            "Tools/validation/real_product/runtime_mesh_contract_smoke/cli.py",
        ),
        (
            "provider_lane_activation",
            "Tools/ai/provider_mesh/local_resource_lanes_check/cli.py",
        ),
        ("openvino_peer_topology", "Tools/validation/provider_mesh/openvino_peer_topology_contract_smoke/cli.py"),
        ("review_pr_prepare_args", "Tools/validation/repository_product/review_pr_prepare_args_smoke/cli.py"),
        (
            "review_pr_product_readiness",
            "Tools/validation/repository_product/review_pr_product_readiness_smoke/cli.py",
        ),
        (
            "heap_provider_budget_governor",
            "Tools/validation/heap_provider/budget_governor_smoke/cli.py",
        ),
        (
            "heap_provider_invocation_contract",
            "Tools/validation/heap_provider/invocation_contract_smoke/cli.py",
        ),
        (
            "heap_runtime_completeness_gate",
            "Tools/validation/heap_runtime/completeness_gate_smoke/cli.py",
        ),
        (
            "runtime_evidence_correlation",
            "Tools/validation/runtime_universe/run_runtime_evidence_correlation_smoke/cli.py",
        ),
        (
            "runtime_evidence_correlation_launcher_wiring",
            "Tools/validation/workflow_run/runtime_evidence_correlation_launcher_wiring_smoke/cli.py",
        ),
        (
            "manifest_runtime_evidence_correlation_schema",
            "Tools/validation/runtime_universe/unified_manifest_runtime_evidence_correlation_smoke/cli.py",
        ),
        (
            "review_pr_final_product_contract",
            "Tools/validation/repository_product/review_pr_final_product_contract_smoke/cli.py",
        ),
    ]

    steps: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    step_count = len(steps_config)

    for index, (name, script) in enumerate(steps_config, start=1):
        write_progress(
            repo_root=repo_root,
            output=output,
            steps=steps,
            current_step=name,
            step_index=index,
            step_count=step_count,
        )
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
        "status": "completed",
        "current_step": "",
        "step_index": step_count,
        "step_count": step_count,
        "completed_step_count": len(steps),
        "passed": not failed_steps,
        "provider_execution_performed": False,
        "provider_activation_performed": any(
            step.get("name") == "provider_lane_activation" and step.get("passed")
            for step in steps
        ),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "blender_runtime_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "steps": steps,
        "failed_steps": failed_steps,
        "errors": errors,
        "warnings": warnings,
    }

    write_json_report(report, output)
    write_markdown(report, markdown_output)
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
