from __future__ import annotations

from .common import *  # noqa: F403
from .reporting import build_markdown
from .runner import run_supervised

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--objective",
        default="Use explicit local GPU/Ollama reasoning to derive the safest next IA-Carmine patch plan while a non-blocking NPU auditor checks intermediate artifacts.",
    )
    parser.add_argument("--evidence", default=DEFAULT_EVIDENCE)
    parser.add_argument("--refined-review", default=DEFAULT_REFINED)
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--live-context-report", action="append", default=[])
    parser.add_argument("--refresh-live-context-each-round", action="store_true")
    parser.add_argument("--context-root", action="append", default=[])
    parser.add_argument("--max-context-files", type=int, default=160)
    parser.add_argument("--max-chars-per-file", type=int, default=8000)
    parser.add_argument("--files-per-round", type=int, default=10)
    parser.add_argument("--budget-minutes", type=int, default=30)
    parser.add_argument("--max-rounds", type=int, default=24)
    parser.add_argument("--use-ollama", action="store_true")
    parser.add_argument("--ollama-model", default=None)
    parser.add_argument("--ollama-base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--keep-alive", default="35m")
    parser.add_argument("--startup-timeout", type=float, default=30.0)
    parser.add_argument("--max-new-tokens", type=int, default=1800)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--enable-runtime-tool-broker", action="store_true")
    parser.add_argument(
        "--runtime-tool-output-dir",
        default="output/ai_runtime_tools/gpu_planner_runtime_tools",
    )
    parser.add_argument("--runtime-tool-timeout-seconds", type=int, default=300)
    parser.add_argument("--runtime-tool-max-requests-per-round", type=int, default=8)
    parser.add_argument("--disable-runtime-tool-bootstrap", action="store_true")
    parser.add_argument("--include-npu-auditor", action="store_true")
    parser.add_argument(
        "--run-npu-auditor-provider",
        action="store_true",
        help="Actually execute OpenVINO/NPU auditor. Without this, auditor uses metadata-only mode.",
    )
    parser.add_argument("--npu-auditor-every-rounds", type=int, default=1)
    parser.add_argument("--npu-auditor-timeout-seconds", type=int, default=900)
    parser.add_argument("--checkpoint-dir", default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_supervised(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json(output, report)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(build_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
                "elapsed_seconds": report["elapsed_seconds"],
                "round_count": report["round_count"],
                "npu_audit_count": report["npu_audit_count"],
                "npu_audit_success_count": report.get("npu_audit_success_count", 0),
                "npu_auditor_disabled_reason": report.get("npu_auditor_disabled_reason", ""),
                "recommendation_count": report["recommendation_count"],
                "raw_recommendation_candidate_count": report.get(
                    "raw_recommendation_candidate_count"
                ),
                "filtered_recommendation_count": report.get("filtered_recommendation_count"),
                "tool_request_count": report.get("tool_request_count"),
                "valid_tool_request_count": report.get("valid_tool_request_count"),
                "invalid_tool_request_count": report.get("invalid_tool_request_count"),
                "empty_recommendations_reason": report.get("empty_recommendations_reason"),
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
                "provider_empty_response_count": report.get("provider_empty_response_count"),
                "evidence_ready_for_manual_patch_count": report.get(
                    "evidence_ready_for_manual_patch_count"
                ),
                "ready_for_patch_plan": report["decision"].get("ready_for_patch_plan"),
                "recommended_next_layer": report["decision"].get("recommended_next_layer"),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2
