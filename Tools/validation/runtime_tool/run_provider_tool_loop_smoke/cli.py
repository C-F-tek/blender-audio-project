#!/usr/bin/env python3
from __future__ import annotations

import argparse
import inspect
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from Tools.validation.runtime_tool.provider_tool_loop_search_chain import (
    run_search_window_chain_smoke,
)


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

    from ia_carmine._shared.provider_tool_loop import (
        broker_tool_schemas,
        normalize_ollama_tool_calls,
        openvino_tool_loop_report,
    )
    from ia_carmine._shared.live_flow_lanes import (
        lane_details,
        merge_provider_statuses,
        support_provider_payload,
    )
    from ia_carmine.runtime.heap_gate.provider_prompt import RuntimeGateProviderPromptMixin
    from ia_carmine.runtime.runtime_tool.broker.runtime_builders import run_heap_code_execution_matrix
    from ia_carmine.runtime.runtime_tool.broker.runtime_builders import generic_write
    from ia_carmine._shared.provider_tool_loop import ollama_tool_call_tool_names
    from ia_carmine.providers.ollama.session import OllamaSession
    from ia_carmine._shared.provider_ollama_probe import run_ollama_probe
    from ia_carmine.runtime.heap_gate.run_loop_metrics import build_provider_lane_metrics
    from ia_carmine.runtime.heap_gate.broker_result_validation import broker_result_passed
    from ia_carmine.runtime.heap_gate.gpu1_tool_result_consumption import (
        gpu1_tool_result_consumption_state,
    )
    from ia_carmine.runtime.heap_gate.tool_broker_native_calls import (
        provider_native_tool_request_id,
    )
    from ia_carmine.runtime.runtime_tool.broker.common import validate_request_args
    from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS

    schemas = broker_tool_schemas()
    errors: list[str] = []
    if not any(
        item.get("function", {}).get("name") == "run_heap_code_execution_matrix"
        for item in schemas
    ):
        errors.append("matrix broker tool schema missing")
    if not any(item.get("function", {}).get("name") == "generic_write" for item in schemas):
        errors.append("generic_write broker tool schema missing")
    tool_names = set(ollama_tool_call_tool_names())
    for required in (
        "generic_write",
        "run_heap_virtual_dev_environment",
        "run_heap_code_execution_matrix",
        "agent_runtime_debug_lab",
        "synthesize_patch_candidates",
        "runtime_file_refs",
        "runtime_file_window",
    ):
        if required not in tool_names:
            errors.append(f"Ollama native tool list missing {required}")
    refs_spec = TOOL_SPECS["runtime_file_refs"]
    unknown_arg_errors = validate_request_args(
        refs_spec.name,
        {"not_allowed": True},
        refs_spec.allowed_args,
        refs_spec.input_schema,
    )
    invalid_type_errors = validate_request_args(
        refs_spec.name,
        {"strict_patchable_targets": {"bad": "type"}},
        refs_spec.allowed_args,
        refs_spec.input_schema,
    )
    if not unknown_arg_errors:
        errors.append("broker schema validation accepted unknown runtime_file_refs arg")
    if not invalid_type_errors:
        errors.append("broker schema validation accepted invalid runtime_file_refs arg type")

    fake_chat = {
        "message": {
            "tool_calls": [
                {
                    "function": {
                        "name": "run_heap_code_execution_matrix",
                        "arguments": {"target_file": ["ia_carmine/providers/provider_mesh/local_provider_probe/cli.py"]},
                    }
                }
            ]
        }
    }
    calls = normalize_ollama_tool_calls(fake_chat)
    if not calls or calls[0].get("tool") != "run_heap_code_execution_matrix":
        errors.append("ollama native tool_calls normalization failed")
    qwen_template_chat = {
        "message": {
            "content": (
                '<tool_call>\n'
                '{"name":"runtime_file_window","arguments":{"path":"README.md","offset":0,"limit":200}}\n'
                "</tool_call>"
            )
        }
    }
    qwen_template_calls = normalize_ollama_tool_calls(qwen_template_chat)
    if not qwen_template_calls or qwen_template_calls[0].get("tool") != "runtime_file_window":
        errors.append("qwen template-native <tool_call> normalization failed")
    naked_json_chat = {
        "message": {
            "content": '{"name":"runtime_file_window","arguments":{"path":"README.md"}}'
        }
    }
    if normalize_ollama_tool_calls(naked_json_chat):
        errors.append("naked JSON content must not be normalized as a native Ollama tool call")
    qwen_json_adapter_calls = normalize_ollama_tool_calls(
        naked_json_chat,
        allow_content_json_adapter=True,
    )
    if (
        not qwen_json_adapter_calls
        or qwen_json_adapter_calls[0].get("native_shape")
        != "ollama-qwen2.5-coder.chat_tools.content_json_adapter"
    ):
        errors.append("qwen content JSON adapter did not normalize strict chat-tools JSON")
    fenced_json_chat = {
        "message": {
            "content": '```json\n{"name":"runtime_file_window","arguments":{"path":"README.md"}}\n```'
        }
    }
    if normalize_ollama_tool_calls(fenced_json_chat, allow_content_json_adapter=True):
        errors.append("fenced JSON content must not be normalized as a native Ollama tool call")
    command, _outputs = run_heap_code_execution_matrix(
        repo_root,
        repo_root / "output" / "validation" / "provider_tool_loop_smoke",
        "validation_arg_regression",
        {
            "target_file": ["ia_carmine/providers/provider_mesh/local_provider_probe/cli.py"],
            "validation_script": ["Tools/validation/heap_runtime/code_execution_tool_smoke/cli.py"],
            "validation_arg": ["--validate"],
        },
    )
    if "--validation-arg=--validate" not in command:
        errors.append("broker builder must preserve leading-dash validation args")
    if "--validation-arg" in command:
        errors.append("broker builder emitted split leading-dash validation arg")
    generic_command, generic_outputs = generic_write(
        repo_root,
        repo_root / "output" / "validation" / "provider_tool_loop_smoke",
        "generic_write_regression",
        {"source_lane": "gpu0_peer", "reason": "smoke", "operator_request": "refine"},
    )
    if "generic_write" not in generic_command:
        errors.append("generic_write builder does not invoke ia_carmine generic_write")
    if "--request-file" not in generic_command or "--operator-request" in generic_command:
        errors.append("generic_write builder must materialize operator_request as request-file")
    if not generic_outputs.get("json_report") or not generic_outputs.get("markdown_report"):
        errors.append("generic_write builder does not declare JSON/Markdown outputs")

    search_chain_errors, strict_window_output = run_search_window_chain_smoke(repo_root)
    errors.extend(search_chain_errors)

    if "partial_callback" not in inspect.signature(OllamaSession.generate).parameters:
        errors.append("Ollama generate must expose partial_callback for GPU1 checkpoints")
    if "partial_output" not in inspect.signature(run_ollama_probe).parameters:
        errors.append("run_ollama_probe must expose partial_output for GPU1 checkpoints")
    ollama_probe_source = inspect.getsource(run_ollama_probe)
    if "partial_markdown_output" not in ollama_probe_source:
        errors.append("GPU1 partial checkpoint must expose a human-readable markdown artifact")
    if "explicit_tool_call_required = prompt_explicitly_requires_tool_call" not in ollama_probe_source:
        errors.append("GPU1 native tool loop must require an explicit tool-call request")
    if "messages is not None" not in ollama_probe_source or "session.chat(\n                            chat_messages" not in ollama_probe_source:
        errors.append("GPU1 native tool loop must send the full chat history through session.chat(messages, tools=...)")

    request_id = provider_native_tool_request_id(
        "smoke-stamp",
        {
            "revision": 7,
            "gpu1_tool_loop_subturn": 0,
            "provider_block_id": "block:alpha",
            "output": "provider_teamwork/gpu1_ollama_provider_probe.json",
        },
        {"id": "tool-call:1"},
        tool="runtime_file_window",
        call_index=2,
    )
    for fragment in ("rev7", "sub0", "idx002", "blkblock_alpha", "calltool-call_1", "runtime_file_window"):
        if fragment not in request_id:
            errors.append(f"provider-native request id missing correlation fragment {fragment}")

    class ToolResultOwner:
        def broker_results(self, events: list[dict[str, object]]) -> list[dict[str, object]]:
            return [
                event.get("payload", {})
                for event in events
                if event.get("event_type") == "broker_result"
            ]

        def provider_report_response_text(self, report: dict[str, object]) -> str:
            return str(report.get("response_text") or "")

    tool_result_owner = ToolResultOwner()
    tool_result_owner.repo_root = repo_root

    if strict_window_output is not None:
        strict_request_id = "provider_tool_loop_smoke_strict_window"
        strict_payload = {
            "request_id": strict_request_id,
            "tool": "runtime_file_window",
            "lane": "gpu1_planner",
            "provider_native_tool_call": True,
            "revision": 9,
            "gpu1_tool_loop_subturn": 0,
            "provider_block_id": "block:strict",
            "chat_history_ref": {"path": "chat/history.json"},
            "returncode": 0,
            "executed": True,
            "blocked": False,
            "errors": [],
            "summary": {"passed": True},
            "outputs": {"json_report": str(strict_window_output)},
        }
        strict_events = [
            {"event_type": "broker_request", "payload": strict_payload},
            {"event_type": "broker_result", "payload": strict_payload},
        ]
        strict_consumption = gpu1_tool_result_consumption_state(
            tool_result_owner,
            strict_events,
            response_text=f"CONSUMED_EVIDENCE:\n- {strict_request_id}\n",
            report={
                "revision": 9,
                "gpu1_tool_loop_subturn": 1,
                "chat_history_ref": {"path": "chat/history.json"},
            },
        )
        if strict_consumption.get("tool_result_consumed_by_gpu1") is not True:
            errors.append("passed strict runtime_file_window result was not consumable by GPU1")
        if strict_consumption.get("gpu1_consumed_tool_result_ids") != [strict_request_id]:
            errors.append("GPU1 strict window consumption did not preserve only the passed request id")

    request_payload = {
        "request_id": request_id,
        "tool": "runtime_file_window",
        "lane": "gpu1_planner",
        "provider_native_tool_call": True,
        "revision": 7,
        "gpu1_tool_loop_subturn": 0,
        "provider_block_id": "block:alpha",
        "chat_history_ref": {"path": "chat/history.json"},
    }
    failed_result_payload = {
        **request_payload,
        "returncode": 0,
        "executed": True,
        "blocked": False,
        "errors": [],
        "summary": {"passed": False},
        "outputs": {},
    }
    tool_events = [
        {"event_type": "broker_request", "payload": request_payload},
        {"event_type": "broker_result", "payload": failed_result_payload},
    ]
    consumer_text = f"CONSUMED_EVIDENCE:\n- tool_or_matrix_refs={request_id}\n"
    consumption = gpu1_tool_result_consumption_state(
        tool_result_owner,
        tool_events,
        response_text=consumer_text,
        report={
            "revision": 7,
            "gpu1_tool_loop_subturn": 1,
            "chat_history_ref": {"path": "chat/history.json"},
        },
    )
    if consumption.get("tool_result_consumed_by_gpu1"):
        errors.append("failed broker result must not become consumed GPU1 product evidence")
    if consumption.get("tool_result_consumed_passed_by_gpu1_count") != 0:
        errors.append("failed broker result must not become passed GPU1 product evidence")
    if request_id not in (consumption.get("gpu1_invalid_consumed_failed_tool_result_ids") or []):
        errors.append("failed broker result cited in CONSUMED_EVIDENCE was not typed invalid")
    if broker_result_passed(failed_result_payload):
        errors.append("broker_result_passed accepted summary.passed=false")
    stale_consumption = gpu1_tool_result_consumption_state(
        tool_result_owner,
        tool_events,
        response_text=consumer_text,
        report={
            "revision": 8,
            "gpu1_tool_loop_subturn": 1,
            "chat_history_ref": {"path": "chat/history.json"},
        },
    )
    if stale_consumption.get("tool_result_consumed_by_gpu1"):
        errors.append("GPU1 consumed a tool result from a different revision")

    prompt_source = inspect.getsource(RuntimeGateProviderPromptMixin.startup_context_digest)
    if "STARTUP_CONTEXT_REFS_FOR_GPU1" not in prompt_source or "file_backed_artifact_refs" not in prompt_source:
        errors.append("GPU1 startup context must expose file-backed artifact refs")
    if "artifact_reference_with_excerpt" in prompt_source or "excerpt only" in prompt_source:
        errors.append("GPU1 startup context still exposes operational excerpts")

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

    api_unavailable_fixture = {
        "lane": "gpu1_planner",
        "native_tool_loop_requested": True,
        "native_tool_loop_supported": False,
        "native_tool_loop_performed": False,
        "provider_native_tool_call_required": True,
        "provider_native_tool_api_supported": False,
        "provider_native_tool_api_unavailable": True,
        "provider_native_tool_call_required_unmet": False,
        "native_tool_call_count": 0,
    }
    required_unmet_fixture = {
        "lane": "gpu0_peer",
        "native_tool_loop_requested": True,
        "native_tool_loop_supported": True,
        "native_tool_loop_performed": True,
        "provider_native_tool_call_required": True,
        "provider_native_tool_api_supported": True,
        "provider_native_tool_api_unavailable": False,
        "provider_native_tool_call_required_unmet": True,
        "native_tool_call_count": 0,
    }
    attempt_failed_fixture = {
        "lane": "gpu1_planner",
        "native_tool_loop_requested": True,
        "native_tool_loop_supported": True,
        "native_tool_loop_performed": False,
        "provider_native_tool_call_required": True,
        "provider_native_tool_api_adapter_available": True,
        "provider_native_tool_api_supported": True,
        "provider_native_tool_api_unavailable": False,
        "provider_native_tool_api_attempt_failed": True,
        "provider_native_tool_call_required_unmet": False,
        "native_tool_call_count": 0,
    }
    npu_fixture = {
        "lane": "npu_micro_task_auditor",
        "native_tool_loop_requested": False,
        "native_tool_loop_supported": True,
        "npu_native_tool_loop_required": False,
    }

    class FixtureOwner:
        args = SimpleNamespace(
            allow_provider_generation=True,
            ollama_num_ctx=16384,
            gpu0_ollama_num_ctx=2048,
            max_new_tokens=3400,
            gpu0_max_new_tokens=1296,
            npu_max_context_chars=2000,
            npu_max_prompt_chars=900,
            npu_max_new_tokens=384,
            max_provider_revisions=5,
            keep_alive="120s",
        )
        provider_reports = [api_unavailable_fixture, required_unmet_fixture, npu_fixture]
        provider_replight_reports: list[dict[str, object]] = []
        provider_execution_performed = False
        selected_ollama_num_ctx = 16384
        provider_revision_lane_policy: dict[str, object] = {}
        pending_provider_sidecar_collections: list[dict[str, object]] = []
        provider_recovery_attempt_count = 0
        time_counter_contract: dict[str, object] = {}

        def latest_proposal_iteration_report(self) -> dict[str, object]:
            return {}

        def runtime_soft_close_reached(self) -> bool:
            return False

    fixture_metrics = build_provider_lane_metrics(
        FixtureOwner(),
        {
            "gpu1_planner": api_unavailable_fixture,
            "gpu0_peer": required_unmet_fixture,
            "npu_micro_task_auditor": npu_fixture,
        },
        [api_unavailable_fixture, required_unmet_fixture, npu_fixture],
    )
    if fixture_metrics.get("provider_native_tool_unavailable_required_lanes") != [
        "gpu1_planner"
    ]:
        errors.append("native tool API unavailable lane was not classified separately")
    if fixture_metrics.get("provider_native_tool_missing_required_lanes") != ["gpu0_peer"]:
        errors.append("required native tool miss must exclude API-unavailable lanes")
    attempt_failed_metrics = build_provider_lane_metrics(
        FixtureOwner(),
        {
            "gpu1_planner": attempt_failed_fixture,
            "gpu0_peer": required_unmet_fixture,
            "npu_micro_task_auditor": npu_fixture,
        },
        [attempt_failed_fixture, required_unmet_fixture, npu_fixture],
    )
    if attempt_failed_metrics.get("provider_native_tool_attempt_failed_required_lanes") != [
        "gpu1_planner"
    ]:
        errors.append("native tool API attempt failure was not classified separately")
    if "gpu1_planner" in attempt_failed_metrics.get(
        "provider_native_tool_missing_required_lanes", []
    ):
        errors.append("native tool API attempt failure must not be collapsed into missing tool call")

    live_ollama: dict[str, object] = {"requested": bool(args.run_live_ollama)}
    if args.run_live_ollama:
        from ia_carmine.providers.provider_mesh.local_provider_probe import run_ollama_probe

        live_ollama = run_ollama_probe(
            repo_root,
            "qwen3-coder:latest",
            "TARGET_FILES ia_carmine/providers/provider_mesh/local_provider_probe/cli.py forced concrete delta required. "
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
        "native_tool_api_unavailable_fixture": {
            "provider_native_tool_api_supported": api_unavailable_fixture[
                "provider_native_tool_api_supported"
            ],
            "provider_native_tool_api_unavailable": api_unavailable_fixture[
                "provider_native_tool_api_unavailable"
            ],
            "provider_native_tool_call_required_unmet": api_unavailable_fixture[
                "provider_native_tool_call_required_unmet"
            ],
        },
        "native_tool_required_unmet_fixture": {
            "provider_native_tool_api_supported": required_unmet_fixture[
                "provider_native_tool_api_supported"
            ],
            "provider_native_tool_api_unavailable": required_unmet_fixture[
                "provider_native_tool_api_unavailable"
            ],
            "provider_native_tool_call_required_unmet": required_unmet_fixture[
                "provider_native_tool_call_required_unmet"
            ],
        },
        "native_tool_attempt_failed_fixture": {
            "provider_native_tool_api_supported": attempt_failed_fixture[
                "provider_native_tool_api_supported"
            ],
            "provider_native_tool_api_unavailable": attempt_failed_fixture[
                "provider_native_tool_api_unavailable"
            ],
            "provider_native_tool_api_attempt_failed": attempt_failed_fixture[
                "provider_native_tool_api_attempt_failed"
            ],
            "provider_native_tool_call_required_unmet": attempt_failed_fixture[
                "provider_native_tool_call_required_unmet"
            ],
        },
        "schema_validation_error_counts": {
            "unknown_arg": len(unknown_arg_errors),
            "invalid_type": len(invalid_type_errors),
        },
        "fixture_metrics": fixture_metrics,
        "attempt_failed_metrics": attempt_failed_metrics,
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
