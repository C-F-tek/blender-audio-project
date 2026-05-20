#!/usr/bin/env python3
from __future__ import annotations

import argparse
import inspect
import json
import os
import sys
from pathlib import Path


def ensure_repo(repo_root: Path) -> None:
    text = str(repo_root)
    if text not in sys.path:
        sys.path.insert(0, text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--run-live-ollama", action="store_true")
    parser.add_argument("--run-live-openvino", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    ensure_repo(repo_root)

    from Tools.ai._shared.provider_tool_loop import (
        broker_tool_schemas,
        normalize_ollama_tool_calls,
        openvino_tool_loop_report,
    )
    from Tools.ai._shared.live_flow_lanes import (
        lane_details,
        merge_provider_statuses,
        support_provider_payload,
    )
    from Tools.ai.heap_gate.provider_prompt import RuntimeGateProviderPromptMixin
    from Tools.ai.runtime_tool.broker.runtime_builders import run_heap_code_execution_matrix
    from Tools.npu.provider_mesh.ollama_runtime_core.session import OllamaSession
    from Tools.ai._shared.provider_ollama_probe import run_ollama_probe

    schemas = broker_tool_schemas()
    errors: list[str] = []
    if not any(
        item.get("function", {}).get("name") == "run_heap_code_execution_matrix"
        for item in schemas
    ):
        errors.append("matrix broker tool schema missing")

    fake_chat = {
        "message": {
            "tool_calls": [
                {
                    "function": {
                        "name": "run_heap_code_execution_matrix",
                        "arguments": {"target_file": ["Tools/ai/provider_mesh/local_provider_probe/cli.py"]},
                    }
                }
            ]
        }
    }
    calls = normalize_ollama_tool_calls(fake_chat)
    if not calls or calls[0].get("tool") != "run_heap_code_execution_matrix":
        errors.append("ollama native tool_calls normalization failed")
    command, _outputs = run_heap_code_execution_matrix(
        repo_root,
        repo_root / "output" / "validation" / "provider_tool_loop_smoke",
        "validation_arg_regression",
        {
            "target_file": ["Tools/ai/provider_mesh/local_provider_probe/cli.py"],
            "validation_script": ["Tools/validation/heap_runtime/code_execution_tool_smoke/cli.py"],
            "validation_arg": ["--validate"],
        },
    )
    if "--validation-arg=--validate" not in command:
        errors.append("broker builder must preserve leading-dash validation args")
    if "--validation-arg" in command:
        errors.append("broker builder emitted split leading-dash validation arg")
    if "partial_callback" not in inspect.signature(OllamaSession.generate).parameters:
        errors.append("Ollama generate must expose partial_callback for GPU1 checkpoints")
    if "partial_output" not in inspect.signature(run_ollama_probe).parameters:
        errors.append("run_ollama_probe must expose partial_output for GPU1 checkpoints")
    ollama_probe_source = inspect.getsource(run_ollama_probe)
    if "partial_markdown_output" not in ollama_probe_source:
        errors.append("GPU1 partial checkpoint must expose a human-readable markdown artifact")
    if "explicit_tool_call_required = prompt_explicitly_requires_tool_call" not in ollama_probe_source:
        errors.append("GPU1 native tool loop must require an explicit tool-call request")
    native_gate = ollama_probe_source.find("if native_tool_loop_relevant:")
    native_chat = ollama_probe_source.find("raw_chat_response = session.chat(")
    if native_gate < 0 or native_chat < native_gate:
        errors.append("GPU1 must not start a second native chat outside the explicit tool-call gate")

    prompt_source = inspect.getsource(RuntimeGateProviderPromptMixin.startup_context_digest)
    if "artifact_reference_with_excerpt" not in prompt_source or "excerpt only" not in prompt_source:
        errors.append("GPU1 startup context must use artifact refs with bounded excerpts")

    live_status = {
        "provider_lane_statuses": [
            {"lane": "orchestrator", "status": "running", "role": "support"},
            {"lane": "gpu1_planner", "status": "running", "role": "primary"},
        ]
    }
    rendered_lanes = lane_details(live_status)
    if "orchestrator" in rendered_lanes or "gpu1_planner" not in rendered_lanes:
        errors.append("live flow must render only real provider lanes, not support orchestration")
    merged_lanes = merge_provider_statuses(
        [{"lane": "orchestrator", "status": "running", "role": "support"}],
        [{"lane": "gpu0_peer", "status": "running", "role": "peer"}],
    )
    if support_provider_payload("orchestrator", {"role": "support"}) is not True:
        errors.append("support orchestrator provider payload must be filtered")
    if any(item.get("lane") == "orchestrator" for item in merged_lanes):
        errors.append("support orchestrator lane must not merge into provider status")

    old_tool_dir = os.environ.pop("IA_CARMINE_OPENVINO_TOOL_MODEL_DIR", None)
    old_gpu0_dir = os.environ.pop("IA_CARMINE_GPU0_COMPANION_MODEL_DIR", None)
    try:
        ov_report = openvino_tool_loop_report(
            repo_root=repo_root,
            prompt="Call a code validation broker tool.",
            timeout_seconds=5,
            max_new_tokens=16,
            allow_discovery=False,
        )
    finally:
        if old_tool_dir is not None:
            os.environ["IA_CARMINE_OPENVINO_TOOL_MODEL_DIR"] = old_tool_dir
        if old_gpu0_dir is not None:
            os.environ["IA_CARMINE_GPU0_COMPANION_MODEL_DIR"] = old_gpu0_dir
    if ov_report.get("classification") != "openvino_tool_loop_model_dir_unconfigured":
        errors.append("OpenVINO unconfigured tool loop classification not explicit")

    live_ollama: dict[str, object] = {"requested": bool(args.run_live_ollama)}
    if args.run_live_ollama:
        from Tools.ai.provider_mesh.local_provider_probe import run_ollama_probe

        live_ollama = run_ollama_probe(
            repo_root,
            "qwen3-coder:latest",
            "TARGET_FILES Tools/ai/provider_mesh/local_provider_probe/cli.py forced concrete delta required. "
            "Use a native tool call to run_heap_code_execution_matrix.",
            max_new_tokens=96,
        )
        if int(live_ollama.get("native_tool_call_count") or 0) <= 0:
            errors.append("live Ollama did not emit message.tool_calls")

    live_openvino_gpu0: dict[str, object] = {"requested": bool(args.run_live_openvino)}
    live_openvino_npu: dict[str, object] = {"requested": bool(args.run_live_openvino)}
    if args.run_live_openvino:
        live_openvino_gpu0 = openvino_tool_loop_report(
            repo_root=repo_root,
            prompt="validate code product by calling run_heap_code_execution_matrix",
            timeout_seconds=args.timeout_seconds,
            max_new_tokens=64,
            device="GPU.0",
        )
        if int(live_openvino_gpu0.get("native_tool_call_count") or 0) <= 0:
            errors.append("live OpenVINO GPU0 did not emit a structured native tool call")
        live_openvino_npu = openvino_tool_loop_report(
            repo_root=repo_root,
            prompt="validate code product by calling run_heap_code_execution_matrix",
            timeout_seconds=args.timeout_seconds,
            max_new_tokens=64,
            device="NPU",
        )
        if int(live_openvino_npu.get("native_tool_call_count") or 0) <= 0:
            errors.append("live OpenVINO NPU did not emit a structured native tool call")

    report = {
        "passed": not errors,
        "broker_tool_schema_count": len(schemas),
        "ollama_native_tool_call_count": len(calls),
        "openvino_classification": ov_report.get("classification"),
        "live_ollama": {
            "requested": args.run_live_ollama,
            "native_tool_call_count": live_ollama.get("native_tool_call_count"),
            "classification": live_ollama.get("native_tool_loop_classification"),
        },
        "live_openvino_gpu0": {
            "requested": args.run_live_openvino,
            "native_tool_call_count": live_openvino_gpu0.get("native_tool_call_count"),
            "classification": live_openvino_gpu0.get("classification"),
        },
        "live_openvino_npu": {
            "requested": args.run_live_openvino,
            "native_tool_call_count": live_openvino_npu.get("native_tool_call_count"),
            "classification": live_openvino_npu.get("classification"),
        },
        "errors": errors,
    }
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
