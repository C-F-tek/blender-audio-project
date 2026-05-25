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
    from ia_carmine._shared.process_tree import terminate_process_tree
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from ia_carmine._shared.process_tree import terminate_process_tree  # type: ignore
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


def run_step(
    repo_root: Path,
    name: str,
    script: str,
    timeout_seconds: int,
    extra_args: list[str] | None = None,
) -> dict[str, Any]:
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
    if name in {"full_product_pr_chain", "heap_runtime_completeness_gate_complete"}:
        command.extend(["--timeout-seconds", str(timeout_seconds)])
    if name == "heap_runtime_completeness_gate_contract_only":
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
    if extra_args:
        command.extend(extra_args)

    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.setdefault("IA_CARMINE_PYTHON", sys.executable)
    env.setdefault("SPAZIOTEMPO_NPU_PYTHON", sys.executable)

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
        "provider_execution_performed": report.get("provider_execution_performed"),
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
    parser.add_argument("--complete-provider-smoke", action="store_true")
    parser.add_argument(
        "--downstream-verification",
        action="store_true",
        help="Acknowledge this smoke is downstream verification, not a product entrypoint.",
    )
    parser.add_argument("--provider-model", default="qwen3-coder:latest")
    parser.add_argument("--provider-base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--provider-num-ctx", type=int, default=8192)
    parser.add_argument("--provider-max-new-tokens", type=int, default=700)
    parser.add_argument("--gpu1-native-tool-loop-preflight", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    if args.complete_provider_smoke and not args.downstream_verification:
        report = {
            "schema_version": 1,
            "kind": "real_product_preflight_gate",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "repo_root": repo_root.as_posix(),
            "status": "blocked",
            "passed": False,
            "preflight_only": False,
            "complete_provider_smoke_performed": False,
            "product_entry_allowed": False,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "blender_runtime_execution_performed": False,
            "ffmpeg_execution_performed": False,
            "steps": [],
            "failed_steps": [],
            "errors": [
                "complete provider smoke is downstream verification only; "
                "do not use full smoke as product entry command"
            ],
            "warnings": [],
        }
        write_json_report(report, output)
        write_markdown(report, markdown_output)
        print(write_json_report(report), end="")
        return 2
    heap_gate_step_name = (
        "heap_runtime_completeness_gate_complete"
        if args.complete_provider_smoke
        else "heap_runtime_completeness_gate_contract_only"
    )
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
            "ia_carmine/providers/provider_mesh/local_resource_lanes_check/cli.py",
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
        *(
            [
                (
                    "gpu1_native_tool_loop_preflight",
                    "Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/cli.py",
                )
            ]
            if args.gpu1_native_tool_loop_preflight
            else []
        ),
        (
            heap_gate_step_name,
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
            extra_args = []
            if name == "heap_runtime_completeness_gate_complete":
                extra_args.extend(["--provider-model", args.provider_model])
            if name == "gpu1_native_tool_loop_preflight":
                extra_args.extend(
                    [
                        "--model",
                        args.provider_model,
                        "--base-url",
                        args.provider_base_url,
                        "--num-ctx",
                        str(args.provider_num_ctx),
                        "--max-new-tokens",
                        str(args.provider_max_new_tokens),
                    ]
                )
            step = run_step(repo_root, name, script, args.timeout_seconds, extra_args)
        steps.append(step)
        if not step.get("passed"):
            errors.append(f"preflight step failed: {name}")

    failed_steps = [step for step in steps if not step.get("passed")]
    provider_execution_performed = any(
        step.get("provider_execution_performed") is True for step in steps
    )
    if args.complete_provider_smoke and not provider_execution_performed:
        errors.append("complete provider smoke requested but no provider execution was observed")
    if not args.complete_provider_smoke and not args.gpu1_native_tool_loop_preflight:
        warnings.append(
            "preflight is contract/static coverage only; it is not complete provider smoke evidence"
        )

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
        "passed": not failed_steps and not errors,
        "preflight_only": not args.complete_provider_smoke,
        "complete_provider_smoke_performed": bool(args.complete_provider_smoke),
        "gpu1_native_tool_loop_preflight_performed": bool(
            args.gpu1_native_tool_loop_preflight
        ),
        "product_entry_allowed": not args.complete_provider_smoke
        or args.downstream_verification,
        "provider_execution_performed": provider_execution_performed,
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
