"""CLI entrypoint for the NPU/GPU deep review auditor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .common import (
    DEFAULT_CONTEXT,
    DEFAULT_GPU_REVIEW,
    DEFAULT_MARKDOWN,
    DEFAULT_NPU_METADATA,
    DEFAULT_NPU_NOTES,
    DEFAULT_NPU_OUT,
    DEFAULT_OUTPUT,
    resolve_path,
    write_json,
)
from .markdown import render_markdown
from .runner import run_auditor

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--gpu-review", default=DEFAULT_GPU_REVIEW)
    parser.add_argument(
        "--run-npu",
        action="store_true",
        help="Explicitly execute OpenVINO/NPU auditor. Without this, only context is prepared.",
    )
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Ask the brokered NPU review helper to write metadata only without loading provider.",
    )
    parser.add_argument(
        "--npu-python",
        default=None,
        help="Python executable for the NPU/OpenVINO GenAI environment. Defaults to SPAZIOTEMPO_NPU_PYTHON or ia_carmine.providers.npu.provider_mesh._shared.npu_runtime.DEFAULT_NPU_PYTHON.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--max-context-chars", type=int, default=42000)
    parser.add_argument("--max-prompt-chars", type=int, default=15000)
    parser.add_argument("--max-new-tokens", type=int, default=900)
    parser.add_argument(
        "--runtime-tool-context-report",
        action="append",
        default=[],
        help="Broker/toolbox JSON report to include as read-only NPU audit context.",
    )
    parser.add_argument("--max-runtime-tool-context-chars", type=int, default=6000)
    parser.add_argument("--max-npu-tool-requests", type=int, default=8)
    parser.add_argument(
        "--disable-npu-tool-fallback",
        action="store_true",
        help="Disable deterministic NPU fallback tool_requests when NPU emits none despite runtime context.",
    )
    parser.add_argument("--context-output", default=DEFAULT_CONTEXT)
    parser.add_argument("--npu-output", default=DEFAULT_NPU_OUT)
    parser.add_argument("--npu-notes-output", default=DEFAULT_NPU_NOTES)
    parser.add_argument("--npu-metadata-output", default=DEFAULT_NPU_METADATA)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_auditor(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json(output, report)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "npu_python": report["npu_python"],
                "npu_python_exists": report["npu_python_exists"],
                "provider_execution_requested": report["provider_execution_requested"],
                "provider_load_attempted": report["provider_load_attempted"],
                "provider_execution_succeeded": report["provider_execution_succeeded"],
                "provider_empty_response": report.get("provider_empty_response"),
                "dependency_missing": report["dependency_missing"],
                "patch_application_performed": report["patch_application_performed"],
                "non_blocking": report["non_blocking"],
                "classification": report["npu_auditor"]["classification"],
                "runtime_tool_context_seen": report.get("runtime_tool_context_seen"),
                "runtime_tool_context_report_count": report.get(
                    "runtime_tool_context_report_count"
                ),
                "tool_request_count": report.get("tool_request_count"),
                "valid_tool_request_count": report.get("valid_tool_request_count"),
                "invalid_tool_request_count": report.get("invalid_tool_request_count"),
                "npu_deterministic_tool_fallback_used": report.get(
                    "npu_deterministic_tool_fallback_used"
                ),
                "npu_deterministic_tool_fallback_count": report.get(
                    "npu_deterministic_tool_fallback_count"
                ),
                "gpu_review_blocked": report["decision"]["gpu_review_blocked"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0
