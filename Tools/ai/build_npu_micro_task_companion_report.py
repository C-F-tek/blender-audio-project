#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--task-file", default="")
    parser.add_argument("--request", default="", help="Optional heap request observed by NPU micro-task lane.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--max-context-chars", type=int, default=4000)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    task_path = repo_root / args.task_file if args.task_file else None
    task_preview = ""
    if task_path and task_path.is_file():
        task_preview = task_path.read_text(encoding="utf-8", errors="replace")[: args.max_context_chars]
    request_input = str(args.request or "").strip()
    response_text = (
        "NPU micro-task: richiesta osservata; nessuna micro-azione necessaria per un saluto casuale."
        if request_input
        else "NPU micro-task: companion report disponibile; nessuna micro-azione richiesta."
    )

    report = {
        "kind": "npu_micro_task_companion_report",
        "schema_version": 2,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": True,
        "mode": "report_only",
        "timeout_seconds": args.timeout_seconds,
        "task_file": args.task_file,
        "task_preview_chars": len(task_preview),
        "request_input": request_input,
        "response_text": response_text,
        "npu_peer_activity_requested": True,
        "npu_peer_activity_performed": False,
        "npu_device_execution_performed": False,
        "npu_provider_execution_performed": False,
        "npu_activity_classification": "diagnostic_report_only",
        "npu_activity_limit": "No NPU model load or device workload is performed by this companion report.",
        "recommendations": [
            {
                "id": "npu_companion_policy",
                "summary": "Use NPU as non-blocking companion lane for micro validation and diagnostics, not as legacy auditor or primary advisory.",
                "classification": "SAFE_MECHANICAL",
            }
        ],
        "guardrails": {
            "legacy_npu_auditor_used": False,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "git_write_performed": False,
            "blender_runtime_execution_performed": False,
            "ffmpeg_runtime_execution_performed": False,
        },
    }

    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# NPU Micro-task Companion Report",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Mode: `{report['mode']}`",
        f"- NPU peer activity requested: `{report['npu_peer_activity_requested']}`",
        f"- NPU peer activity performed: `{report['npu_peer_activity_performed']}`",
        f"- NPU device execution performed: `{report['npu_device_execution_performed']}`",
        f"- NPU provider execution performed: `{report['npu_provider_execution_performed']}`",
        f"- NPU activity classification: `{report['npu_activity_classification']}`",
        f"- Request input: `{report['request_input']}`",
        f"- Response text: {report['response_text']}",
        f"- NPU activity limit: {report['npu_activity_limit']}",
        f"- Legacy NPU auditor used: `{report['guardrails']['legacy_npu_auditor_used']}`",
        f"- Provider execution performed: `{report['guardrails']['provider_execution_performed']}`",
        "",
        "## Recommendation",
        "",
        report["recommendations"][0]["summary"],
    ]
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"passed": True, "output": str(output), "markdown_output": str(markdown)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
