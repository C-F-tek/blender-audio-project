#!/usr/bin/env python3
"""Smoke-test the heap code execution matrix tool and broker wiring."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import subprocess
import sys
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from ia_carmine.runtime.runtime_tool.broker.executor import build_report as build_broker_report
    from ia_carmine.runtime.runtime_tool.broker.markdown import render_markdown as render_broker_markdown
    from Tools.validation._shared.report_utils import write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.runtime.runtime_tool.broker.executor import build_report as build_broker_report  # type: ignore
    from ia_carmine.runtime.runtime_tool.broker.markdown import render_markdown as render_broker_markdown  # type: ignore
    from Tools.validation._shared.report_utils import write_json_report, write_text_report  # type: ignore


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def run(command: list[str], repo_root: Path, timeout: int) -> dict[str, Any]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo_root)
    completed = subprocess.run(
        command,
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
        "ok": completed.returncode == 0,
    }


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def run_broker_in_process(
    *,
    repo_root: Path,
    request_data: dict[str, Any],
    tool_output_dir: str,
    output: Path,
    markdown: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    try:
        broker_args = Namespace(
            repo_root=str(repo_root),
            request_data=request_data,
            request_file="",
            request_json="",
            tool_output_dir=tool_output_dir,
            stamp="heap_code_execution_tool_smoke",
            timeout_seconds=timeout_seconds,
            dry_run=False,
        )
        report = build_broker_report(broker_args)
        write_json_report(report, output)
        write_text_report(render_broker_markdown(report), markdown)
        return {
            "command": ["in_process", "ia_carmine.runtime.runtime_tool.broker.executor.build_report"],
            "returncode": 0 if report.get("passed") else 2,
            "stdout_tail": json.dumps(
                {
                    "passed": report.get("passed"),
                    "request_transport": report.get("request_transport"),
                    "tool_execution_count": report.get("tool_execution_count"),
                },
                ensure_ascii=False,
            ),
            "stderr_tail": "",
            "ok": bool(report.get("passed")),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "command": ["in_process", "ia_carmine.runtime.runtime_tool.broker.executor.build_report"],
            "returncode": 1,
            "stdout_tail": "",
            "stderr_tail": f"{type(exc).__name__}: {exc}",
            "ok": False,
        }


def unified_diff(rel_path: str, before: str, after: str) -> str:
    body = "\n".join(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=f"a/{rel_path}",
            tofile=f"b/{rel_path}",
            lineterm="",
        )
    )
    return f"diff --git a/{rel_path} b/{rel_path}\n{body}\n"


def write_evidence_report(repo_root: Path, path: Path) -> None:
    rel_path = "Tools/validation/heap_runtime/code_execution_tool_smoke/cli.py"
    before = (repo_root / rel_path).read_text(encoding="utf-8-sig", errors="replace")
    after = before + "\n# heap_code_execution_tool_smoke evidence-only patch candidate\n"
    report = {
        "kind": "provider_proposal_fixture",
        "target_files": [rel_path],
        "response_text": (
            "TARGET_FILES\n"
            f"- {rel_path}\n\n"
            "PATCH_SKETCH_UNIFIED_DIFF\n"
            "```diff\n"
            f"{unified_diff(rel_path, before, after)}"
            "```\n"
        ),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_broker_request(evidence_report: Path) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "agent_runtime_tool_requests",
        "source": "heap_code_execution_tool_smoke",
        "tool_requests": [
            {
                "id": "code_execution_matrix",
                "tool": "run_heap_code_execution_matrix",
                "reason": "Verify compile/test/diff matrix can be brokered into the heap.",
                "requirement": "code_execution_matrix",
                "args": {
                    "target_file": [
                        "ia_carmine/runtime/heap_runtime/code_execution_tool/cli.py",
                        "ia_carmine/runtime/runtime_tool/agent_runtime_debug_lab/policy.py",
                        "Tools/validation/heap_runtime/code_execution_tool_smoke/cli.py",
                    ],
                    "validation_script": ["Tools/validation/heap_final_proposals/test_proposal_gate/cli.py"],
                    "timeout_seconds": 300,
                    "max_diff_chars": 1000,
                    "operator_request": "refactor duplicated path resolver into runtime file refs",
                    "evidence_report": [str(evidence_report)],
                    "synthesize_patch_candidates": True,
                    "max_patch_candidates": 1,
                },
            }
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Code Execution Tool Smoke", ""]
    for key in (
        "passed",
        "direct_returncode",
        "broker_returncode",
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    run_stamp = stamp()
    direct_output = (
        repo_root / f"output/validation/heap_code_execution_tool_smoke_direct_{run_stamp}.json"
    )
    direct_md = (
        repo_root / f"output/validation/heap_code_execution_tool_smoke_direct_{run_stamp}.md"
    )
    broker_output = (
        repo_root / f"output/validation/heap_code_execution_tool_smoke_broker_{run_stamp}.json"
    )
    broker_md = (
        repo_root / f"output/validation/heap_code_execution_tool_smoke_broker_{run_stamp}.md"
    )
    evidence_report = (
        repo_root / f"output/validation/heap_code_execution_tool_smoke_evidence_{run_stamp}.json"
    )
    write_evidence_report(repo_root, evidence_report)
    broker_request = build_broker_request(evidence_report)

    direct = run(
        [
            sys.executable,
            "ia_carmine/runtime/heap_runtime/code_execution_tool/cli.py",
            "--repo-root",
            ".",
            "--target-file",
            "ia_carmine/runtime/heap_runtime/code_execution_tool/cli.py",
            "--target-file",
            "ia_carmine/runtime/runtime_tool/agent_runtime_debug_lab/policy.py",
            "--target-file",
            "Tools/validation/heap_runtime/code_execution_tool_smoke/cli.py",
            "--validation-script",
            "Tools/validation/heap_final_proposals/test_proposal_gate/cli.py",
            "--output",
            str(direct_output),
            "--markdown-output",
            str(direct_md),
            "--timeout-seconds",
            "300",
            "--max-diff-chars",
            "1000",
            "--operator-request",
            "refactor duplicated path resolver into runtime file refs",
            "--evidence-report",
            str(evidence_report),
            "--synthesize-patch-candidates",
            "--max-patch-candidates",
            "1",
        ],
        repo_root,
        args.timeout_seconds,
    )
    broker = run_broker_in_process(
        repo_root=repo_root,
        request_data=broker_request,
        tool_output_dir=f"output/ai_runtime_tools/heap_code_execution_tool_smoke_{run_stamp}",
        output=broker_output,
        markdown=broker_md,
        timeout_seconds=360,
    )
    direct_data = read_json(direct_output)
    broker_data = read_json(broker_output)
    errors: list[str] = []
    if direct["returncode"] != 0 or direct_data.get("passed") is not True:
        errors.append("direct heap code execution tool did not pass")
    if direct_data.get("verified_target_count", 0) < 2:
        errors.append("direct report did not verify target files")
    if direct_data.get("concrete_code_proposal_count", 0) > direct_data.get("target_count", 0):
        errors.append("direct report emitted more concrete proposals than targets")
    if direct_data.get("patch_candidate_synthesis_requested") is not True:
        errors.append("direct report did not request patch candidate synthesis")
    if direct_data.get("patch_candidate_synthesis_passed_count", 0) < 1:
        errors.append("direct report did not emit a validated patch candidate")
    for item in direct_data.get("concrete_code_proposals", []):
        if item.get("implementation_status") == "verified_target_no_worktree_diff":
            errors.append("no-diff target leaked into concrete code proposals")
    if broker["returncode"] != 0 or broker_data.get("passed") is not True:
        errors.append("brokered heap code execution matrix did not pass")
    if "run_heap_code_execution_matrix" not in broker_data.get("allowlisted_tools", []):
        errors.append("broker allowlist does not expose run_heap_code_execution_matrix")
    if "synthesize_patch_candidates" not in broker_data.get("allowlisted_tools", []):
        errors.append("broker allowlist does not expose synthesize_patch_candidates")
    if broker_data.get("tool_execution_count") != 1:
        errors.append("broker should execute exactly one code execution matrix tool")
    if broker_data.get("request_transport") != "in_memory":
        errors.append("broker request transport must be in_memory")
    for key in (
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
        "git_write_performed",
    ):
        if direct_data.get(key) is not False:
            errors.append(f"direct report guardrail {key} must be false")
        if broker_data.get(key) is not False:
            errors.append(f"broker report guardrail {key} must be false")
    return {
        "schema_version": 1,
        "kind": "heap_code_execution_tool_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "git_write_performed": False,
        "direct_returncode": direct["returncode"],
        "broker_returncode": broker["returncode"],
        "direct_output": str(direct_output),
        "broker_output": str(broker_output),
        "direct_stdout_tail": direct["stdout_tail"],
        "direct_stderr_tail": direct["stderr_tail"],
        "broker_stdout_tail": broker["stdout_tail"],
        "broker_stderr_tail": broker["stderr_tail"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/heap_code_execution_tool_smoke.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/heap_code_execution_tool_smoke.md"
    )
    parser.add_argument("--timeout-seconds", type=int, default=420)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = repo_root / args.output if not Path(args.output).is_absolute() else Path(args.output)
    markdown = (
        repo_root / args.markdown_output
        if not Path(args.markdown_output).is_absolute()
        else Path(args.markdown_output)
    )
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
