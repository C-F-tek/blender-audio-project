#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    companion_json = repo_root / "output/validation/npu_micro_task_companion_report_smoke.json"
    companion_md = repo_root / "output/validation/npu_micro_task_companion_report_smoke.md"

    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "ia_carmine/providers/provider_mesh/npu_micro_task_companion_report/cli.py"),
            "--repo-root",
            str(repo_root),
            "--output",
            str(companion_json),
            "--markdown-output",
            str(companion_md),
            "--timeout-seconds",
            "10",
            "--python-exe",
            sys.executable,
            "--request",
            "# HEAP_DELTA_PROPOSAL\nTARGET_FILES=\nVALIDATION_COMMANDS=\nRISKS=",
            "--tool-loop-timeout-seconds",
            "5",
            "--tool-loop-max-new-tokens",
            "64",
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
    )

    passed = companion_json.is_file()
    companion = {}
    if companion_json.is_file():
        companion = json.loads(companion_json.read_text(encoding="utf-8"))

    passed = passed and companion.get("guardrails", {}).get("legacy_npu_auditor_used") is False
    passed = passed and companion.get("npu_micro_task_closed") is True
    passed = passed and companion.get("npu_micro_task_kind") in {
        "section_presence_audit",
        "target_reference_audit",
        "validation_command_audit",
        "risk_guardrail_audit",
    }
    passed = passed and companion.get("npu_micro_decision") in {
        "NPU_DONE",
        "NPU_REJECT",
        "NPU_NO_ACTION",
        "NPU_TIMEOUT_BOUNDARY",
    }

    report = {
        "kind": "npu_micro_task_companion_smoke",
        "schema_version": 1,
        "repo_root": repo_root.as_posix(),
        "passed": passed,
        "errors": [] if passed else ["npu micro task companion smoke failed"],
        "warnings": [],
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-1000:],
        "stderr_tail": result.stderr[-1000:],
        "provider_execution_performed": bool(companion.get("provider_execution_performed")),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "legacy_npu_auditor_used": False,
        "npu_micro_task_kind": companion.get("npu_micro_task_kind"),
        "npu_micro_decision": companion.get("npu_micro_decision"),
        "npu_micro_task_closed": companion.get("npu_micro_task_closed"),
    }

    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    markdown.write_text(
        f"# NPU Micro-task Companion Smoke\n\n- Passed: `{passed}`\n", encoding="utf-8"
    )
    print(json.dumps({"passed": passed, "output": str(output)}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
