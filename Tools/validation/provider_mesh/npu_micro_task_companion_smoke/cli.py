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
            str(repo_root / "Tools/ai/provider_mesh/npu_micro_task_companion_report/cli.py"),
            "--repo-root",
            str(repo_root),
            "--output",
            str(companion_json),
            "--markdown-output",
            str(companion_md),
            "--timeout-seconds",
            "10",
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
    )

    passed = result.returncode == 0
    companion = {}
    if companion_json.is_file():
        companion = json.loads(companion_json.read_text(encoding="utf-8"))

    passed = passed and companion.get("guardrails", {}).get("legacy_npu_auditor_used") is False
    passed = passed and companion.get("guardrails", {}).get("provider_execution_performed") is False

    report = {
        "kind": "npu_micro_task_companion_smoke",
        "schema_version": 1,
        "passed": passed,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-1000:],
        "stderr_tail": result.stderr[-1000:],
        "provider_execution_performed": False,
        "legacy_npu_auditor_used": False,
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
