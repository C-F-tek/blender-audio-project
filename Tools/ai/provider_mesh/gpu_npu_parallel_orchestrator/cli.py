from __future__ import annotations

import argparse
import json
from pathlib import Path

from .common import (
    DEFAULT_CHECKPOINT_DIR,
    DEFAULT_GPU0_PEER_SUPPORT_DIR,
    DEFAULT_GPU_MARKDOWN,
    DEFAULT_GPU_OUTPUT,
    DEFAULT_MARKDOWN,
    DEFAULT_NPU_MICRO_SUPPORT_DIR,
    DEFAULT_OUTPUT,
    resolve_path,
    write_json,
)
from .diagnostics import build_markdown
from .runner import run_orchestrator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--budget-minutes", type=int, default=30)
    parser.add_argument("--max-rounds", type=int, default=24)
    parser.add_argument("--files-per-round", type=int, default=10)
    parser.add_argument("--max-context-files", type=int, default=300)
    parser.add_argument("--max-chars-per-file", type=int, default=8000)
    parser.add_argument("--max-new-tokens", type=int, default=4800)
    parser.add_argument("--keep-alive", default="35m")
    parser.add_argument("--ollama-model", default=None)
    parser.add_argument("--ollama-base-url", default=None)
    parser.add_argument(
        "--evidence",
        default="output/ai_pipeline/agent_review_evidence_sufficiency.json",
    )
    parser.add_argument(
        "--refined-review",
        default="output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json",
    )
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--context-root", action="append", default=[])
    parser.add_argument("--enable-runtime-tool-broker", action="store_true", default=True)
    parser.add_argument(
        "--gpu-runner-direct-runtime-tool-broker",
        action="store_true",
        help="Compatibility mode: let the GPU supervised runner execute runtime tools directly instead of routing GPU requests through the orchestrator.",
    )
    parser.add_argument(
        "--runtime-tool-output-dir",
        default="output/ai_runtime_tools/gpu_planner_runtime_tools",
    )
    parser.add_argument("--runtime-tool-timeout-seconds", type=int, default=300)
    parser.add_argument("--runtime-tool-max-requests-per-round", type=int, default=8)
    parser.add_argument("--disable-runtime-tool-bootstrap", action="store_true")
    parser.add_argument("--run-gpu0-peer-support-provider", action="store_true")
    parser.add_argument("--gpu0-peer-support-dir", default=DEFAULT_GPU0_PEER_SUPPORT_DIR)
    parser.add_argument("--gpu0-peer-support-every-rounds", type=int, default=1)
    parser.add_argument("--max-concurrent-gpu0-peer-support", type=int, default=1)
    parser.add_argument("--gpu0-peer-support-iterations", type=int, default=24)
    parser.add_argument("--gpu0-peer-support-min-seconds", type=float, default=1.0)
    parser.add_argument("--gpu0-peer-support-final-wait-seconds", type=int, default=45)
    parser.add_argument("--run-npu-micro-support-provider", action="store_true")
    parser.add_argument("--npu-micro-support-dir", default=DEFAULT_NPU_MICRO_SUPPORT_DIR)
    parser.add_argument("--npu-micro-support-every-rounds", type=int, default=1)
    parser.add_argument("--max-concurrent-npu-micro-support", type=int, default=1)
    parser.add_argument("--npu-micro-support-timeout-seconds", type=int, default=60)
    parser.add_argument("--npu-micro-support-final-wait-seconds", type=int, default=60)
    parser.add_argument("--npu-micro-support-max-context-chars", type=int, default=4000)
    parser.add_argument("--npu-micro-support-max-prompt-chars", type=int, default=900)
    parser.add_argument("--npu-micro-support-max-new-tokens", type=int, default=192)
    parser.add_argument(
        "--npu-micro-support-max-runtime-tool-context-chars", type=int, default=3000
    )
    parser.add_argument("--npu-micro-support-max-tool-requests", type=int, default=4)
    parser.add_argument("--runtime-heap-stamp", default="")
    parser.add_argument("--runtime-heap-events", default="")
    parser.add_argument("--runtime-heap-snapshot", default="")
    parser.add_argument("--runtime-heap-markdown", default="")
    parser.add_argument("--max-degraded-lanes", type=int, default=0)
    parser.add_argument(
        "--enable-runtime-state",
        dest="enable_runtime_state",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--disable-runtime-state",
        dest="enable_runtime_state",
        action="store_false",
    )
    parser.add_argument("--run-npu-auditor-provider", action="store_true")
    parser.add_argument("--npu-python", default=None)
    parser.add_argument("--npu-auditor-every-rounds", type=int, default=4)
    parser.add_argument("--max-concurrent-npu-audits", type=int, default=1)
    parser.add_argument("--npu-auditor-timeout-seconds", type=int, default=600)
    parser.add_argument("--npu-max-context-chars", type=int, default=12000)
    parser.add_argument("--npu-max-prompt-chars", type=int, default=8000)
    parser.add_argument("--npu-max-new-tokens", type=int, default=512)
    parser.add_argument("--npu-final-wait-seconds", type=int, default=120)
    parser.add_argument("--npu-slow-audit-threshold-seconds", type=float, default=60.0)
    parser.add_argument("--npu-slow-auditor-every-rounds", type=int, default=4)
    parser.add_argument("--poll-seconds", type=float, default=2.0)
    parser.add_argument("--checkpoint-dir", default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--gpu-output", default=DEFAULT_GPU_OUTPUT)
    parser.add_argument("--gpu-markdown-output", default=DEFAULT_GPU_MARKDOWN)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_orchestrator(args)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    write_json(output, report)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(build_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown),
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
                "elapsed_seconds": report["elapsed_seconds"],
                "gpu_returncode": report["gpu_returncode"],
                "gpu_round_count": report["gpu_summary"].get("round_count"),
                "gpu_recommendation_count": report["gpu_summary"].get("recommendation_count"),
                "gpu0_peer_support_count": report.get("gpu0_peer_support_count"),
                "gpu0_peer_support_success_count": report.get("gpu0_peer_support_success_count"),
                "gpu0_peer_support_overlap_count": report.get("gpu0_peer_support_overlap_count"),
                "npu_micro_support_count": report.get("npu_micro_support_count"),
                "npu_micro_support_success_count": report.get("npu_micro_support_success_count"),
                "npu_micro_support_overlap_count": report.get("npu_micro_support_overlap_count"),
                "npu_micro_support_tool_request_count": report.get(
                    "npu_micro_support_tool_request_count"
                ),
                "npu_micro_runtime_tool_execution_count": report.get(
                    "npu_micro_runtime_tool_execution_count"
                ),
                "npu_micro_runtime_tool_live_execution_count": report.get(
                    "npu_micro_runtime_tool_live_execution_count"
                ),
                "gpu_empty_recommendations_reason": report.get("gpu_empty_recommendations_reason"),
                "gpu_evidence_ready_for_manual_patch_count": report.get(
                    "gpu_evidence_ready_for_manual_patch_count"
                ),
                "gpu_recommended_next_layer": report.get("gpu_recommended_next_layer"),
                "runtime_tool_broker_enabled": report.get("runtime_tool_broker_enabled"),
                "runtime_tool_bootstrap_executed": report.get("runtime_tool_bootstrap_executed"),
                "runtime_tool_bootstrap_passed": report.get("runtime_tool_bootstrap_passed"),
                "runtime_tool_bootstrap_request_count": report.get(
                    "runtime_tool_bootstrap_request_count"
                ),
                "runtime_tool_bootstrap_execution_count": report.get(
                    "runtime_tool_bootstrap_execution_count"
                ),
                "runtime_tool_bootstrap_failed_count": report.get(
                    "runtime_tool_bootstrap_failed_count"
                ),
                "runtime_tool_bootstrap_blocked_count": report.get(
                    "runtime_tool_bootstrap_blocked_count"
                ),
                "runtime_tool_request_count": report.get("runtime_tool_request_count"),
                "runtime_tool_execution_count": report.get("runtime_tool_execution_count"),
                "runtime_tool_failed_count": report.get("runtime_tool_failed_count"),
                "runtime_tool_blocked_count": report.get("runtime_tool_blocked_count"),
                "runtime_tool_result_count": report.get("runtime_tool_result_count"),
                "runtime_tool_provider_request_count": report.get(
                    "runtime_tool_provider_request_count"
                ),
                "runtime_tool_provider_request_execution_count": report.get(
                    "runtime_tool_provider_request_execution_count"
                ),
                "deterministic_runtime_tool_fallback_execution_count": report.get(
                    "deterministic_runtime_tool_fallback_execution_count"
                ),
                "orchestrator_runtime_tool_bootstrap_execution_count": report.get(
                    "orchestrator_runtime_tool_bootstrap_execution_count"
                ),
                "gpu_orchestrated_runtime_tool_request_count": report.get(
                    "gpu_orchestrated_runtime_tool_request_count"
                ),
                "gpu_orchestrated_runtime_tool_execution_count": report.get(
                    "gpu_orchestrated_runtime_tool_execution_count"
                ),
                "gpu_orchestrated_runtime_tool_failed_count": report.get(
                    "gpu_orchestrated_runtime_tool_failed_count"
                ),
                "gpu_orchestrated_runtime_tool_blocked_count": report.get(
                    "gpu_orchestrated_runtime_tool_blocked_count"
                ),
                "npu_audit_count": report["npu_audit_count"],
                "npu_audit_success_count": report["npu_audit_success_count"],
                "npu_tool_context_seen_count": report.get("npu_tool_context_seen_count"),
                "npu_tool_request_count": report.get("npu_tool_request_count"),
                "npu_deterministic_tool_fallback_count": report.get(
                    "npu_deterministic_tool_fallback_count"
                ),
                "npu_runtime_tool_request_count": report.get("npu_runtime_tool_request_count"),
                "npu_runtime_tool_execution_count": report.get("npu_runtime_tool_execution_count"),
                "npu_runtime_tool_failed_count": report.get("npu_runtime_tool_failed_count"),
                "npu_runtime_tool_blocked_count": report.get("npu_runtime_tool_blocked_count"),
                "npu_runtime_tool_result_count": report.get("npu_runtime_tool_result_count"),
                "gpu_review_blocked_by_npu": report["decision"]["gpu_review_blocked_by_npu"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2
