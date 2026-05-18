#!/usr/bin/env python3
"""Smoke test the heap virtual development environment tool and broker wiring."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(command: list[str], cwd: Path, timeout: int) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
        "ok": completed.returncode == 0,
    }


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def build_broker_request(path: Path) -> None:
    write_json(
        path,
        {
            "schema_version": 1,
            "kind": "agent_runtime_tool_requests",
            "tool_requests": [
                {
                    "id": "virtual-dev-smoke",
                    "tool": "run_heap_virtual_dev_environment",
                    "requirement": "virtual_dev_environment",
                    "reason": "verify broker-callable virtual dev environment",
                    "args": {
                        "target_file": [
                            "Tools/ai/heap_runtime/virtual_dev_environment/cli.py",
                            "Tools/ai/code_product/final_readable_product/cli.py",
                        ],
                        "validation_script": [
                            "Tools/validation/heap_runtime/run_heap_final_readable_product_smoke/cli.py"
                        ],
                        "dynamic_import": True,
                        "help_probe": True,
                        "timeout_seconds": 120,
                    },
                }
            ],
        },
    )


def run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or now_stamp()
    direct_output = (
        repo_root
        / "output"
        / "validation"
        / f"heap_virtual_dev_environment_smoke_direct_{stamp}.json"
    )
    direct_markdown = direct_output.with_suffix(".md")
    broker_request = (
        repo_root
        / "output"
        / "validation"
        / f"heap_virtual_dev_environment_smoke_broker_request_{stamp}.json"
    )
    broker_output = (
        repo_root
        / "output"
        / "validation"
        / f"heap_virtual_dev_environment_smoke_broker_{stamp}.json"
    )
    broker_markdown = broker_output.with_suffix(".md")
    broker_tool_dir = (
        repo_root / "output" / "ai_runtime_tools" / f"heap_virtual_dev_environment_smoke_{stamp}"
    )
    build_broker_request(broker_request)
    direct = run(
        [
            sys.executable,
            "Tools/ai/heap_runtime/virtual_dev_environment/cli.py",
            "--repo-root",
            ".",
            "--target-file",
            "Tools/ai/heap_runtime/virtual_dev_environment/cli.py",
            "--target-file",
            "Tools/ai/code_product/final_readable_product/cli.py",
            "--validation-script",
            "Tools/validation/heap_runtime/run_heap_final_readable_product_smoke/cli.py",
            "--dynamic-import",
            "--help-probe",
            "--output",
            str(direct_output),
            "--markdown-output",
            str(direct_markdown),
        ],
        repo_root,
        args.timeout_seconds,
    )
    broker = run(
        [
            sys.executable,
            "Tools/ai/runtime_tool/agent_broker/cli.py",
            "--repo-root",
            ".",
            "--request-file",
            str(broker_request),
            "--tool-output-dir",
            str(broker_tool_dir),
            "--output",
            str(broker_output),
            "--markdown-output",
            str(broker_markdown),
            "--timeout-seconds",
            str(args.timeout_seconds),
        ],
        repo_root,
        args.timeout_seconds,
    )
    direct_report = read_json(direct_output)
    broker_report = read_json(broker_output)
    passed = (
        direct.get("ok")
        and broker.get("ok")
        and direct_report.get("passed") is True
        and broker_report.get("tool_execution_count") == 1
        and broker_report.get("failed_tool_count") == 0
    )
    report = {
        "schema_version": 1,
        "kind": "heap_virtual_dev_environment_smoke",
        "passed": bool(passed),
        "direct_output": str(direct_output),
        "broker_output": str(broker_output),
        "direct": direct,
        "broker": broker,
        "direct_passed": direct_report.get("passed"),
        "broker_tool_execution_count": broker_report.get("tool_execution_count"),
        "broker_failed_tool_count": broker_report.get("failed_tool_count"),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": [] if passed else ["virtual dev environment smoke failed"],
        "warnings": [],
    }
    output = (
        Path(args.output).resolve()
        if args.output
        else repo_root
        / "output"
        / "validation"
        / f"heap_virtual_dev_environment_smoke_{stamp}.json"
    )
    write_json(output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    return parser.parse_args()


def main() -> int:
    return 0 if run_smoke(parse_args()).get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
