"""Command builders for heap context closure."""

from __future__ import annotations

from typing import Any


def request_args(state: dict[str, Any]) -> list[str]:
    request_file = str(state.get("operator_request_file") or "").strip()
    if request_file:
        return ["--request-file", request_file]
    return ["--request", str(state.get("heap_request") or "")]


def startup_command(args: Any, state: dict[str, Any]) -> list[str]:
    return [
        state["project_python"],
        "-m",
        "Tools.ai",
        "heap_context_memory_reload",
        "--repo-root",
        ".",
        *request_args(state),
        "--stamp",
        state["stamp"],
        "--python-exe",
        state["project_python"],
        "--output-dir",
        str(state["startup_dir"]),
        "--max-memory-chars",
        str(args.startup_max_memory_chars),
        "--max-context-files",
        str(args.startup_max_context_files),
        "--startup-scan-context-files",
        str(args.startup_scan_context_files),
        "--max-chars-per-file",
        str(args.startup_max_chars_per_file),
    ]


def heap_command(args: Any, state: dict[str, Any]) -> list[str]:
    return [
        state["project_python"],
        "-m",
        "Tools.ai",
        "run_heap_runtime_completeness_gate",
        "--repo-root",
        ".",
        *request_args(state),
        "--budget-minutes",
        str(args.budget_minutes),
        "--max-iterations",
        str(args.max_iterations),
        "--min-runtime-rounds",
        str(args.min_runtime_rounds),
        "--min-proposal-iterations",
        str(args.min_proposal_iterations),
        "--max-rounds",
        str(args.max_rounds),
        "--max-provider-revisions",
        str(args.max_provider_revisions),
        "--provider-model",
        str(args.provider_model),
        "--ollama-num-ctx",
        str(args.ollama_num_ctx),
        "--max-new-tokens",
        str(args.max_new_tokens),
        "--keep-alive",
        str(args.keep_alive),
        "--gpu0-iterations",
        str(args.gpu0_iterations),
        "--gpu0-min-seconds",
        str(args.gpu0_min_seconds),
        "--npu-micro-timeout-seconds",
        str(args.npu_micro_timeout_seconds),
        "--npu-max-context-chars",
        str(args.npu_max_context_chars),
        "--npu-max-prompt-chars",
        str(args.npu_max_prompt_chars),
        "--npu-max-new-tokens",
        str(args.npu_max_new_tokens),
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--allow-npu-device-workload",
        "--npu-device-workload-seconds",
        str(args.npu_device_workload_seconds),
        "--npu-device-workload-iterations",
        str(args.npu_device_workload_iterations),
        "--output-dir",
        str(state["run_dir"]),
        "--output",
        str(state["report_file"]),
        "--markdown-output",
        str(state["markdown_file"]),
    ]
