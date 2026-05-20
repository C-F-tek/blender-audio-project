from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from Tools.ai._shared.openvino_model_discovery import (
    discover_openvino_tool_model_dir,
    run_openvino_tool_loop_child_payload,
)
from Tools.ai._shared.provider_tool_schemas import broker_tool_schemas
from Tools.ai.provider_mesh.runtime.python_runtime import command_env
def heap_patch_prompt_required(prompt: str) -> bool:
    text = (prompt or "").lower()
    markers = ("heap chunk/composer contract", "startup_context_digest_for_gpu1", "external heap revision context", "target_files", "forced concrete delta required", "proposal chunks")
    return any(marker in text for marker in markers)
def build_heap_patch_proposal_prompt(prompt: str) -> str:
    if not heap_patch_prompt_required(prompt):
        return prompt
    return (
        "IA-CARMINE GPU1 HEAP PARTICIPATION MODE.\n"
        "You are the GPU1 planner/worker inside the existing heap/pointer/veto loop. Do not collapse the run into a tool-only or JSON-only answer.\n"
        "Use startup artifacts, memory, source anchors, tool catalog, prior vetoes and pointer context as evidence.\n"
        "First write the normal heap proposal/revision text. Keep HEAP_POINTER_DELTA_PROTOCOL alive: reason over the universe, choose/reject targets, expose uncertainty and preserve veto/pointer continuity.\n"
        "A provider-native tool-call turn may follow only when the prompt explicitly requires broker execution or the primary text is empty; it is not the proposal itself.\n"
        "Ollama uses /api/chat tools and message.tool_calls only for that continuation. OpenVINO lanes attach equivalent structured reports. Tool calls are extra broker actions, not a replacement for heap text.\n\n"
        "BEGIN_HEAP_CONTEXT_AND_POINTERS\n"
        f"{prompt.rstrip()}\n"
        "END_HEAP_CONTEXT_AND_POINTERS\n\n"
        "GPU1 RESPONSE CONTRACT:\n"
        "- Write Markdown/plain heap-delta text, not a JSON-only envelope.\n"
        "- Include # HEAP_DELTA_PROPOSAL.\n"
        "- Include EXIT_DECISION=PATCHABLE_TARGET or EXIT_DECISION=NO_PATCHABLE_TARGET.\n"
        "- Include POINTER_ACTION=STAY_FORWARD | BACKTRACK_PROPAGATE | RESUME_FORWARD | SPLIT_TASKS | NO_PATCHABLE_TARGET.\n"
        "- Include TARGET_FILES, PROBLEM, EVIDENCE, IMPLEMENTATION_CHANGES, PATCH_SKETCH, VALIDATION_COMMANDS and RISKS.\n"
        "- TARGET_FILES must be exact repo-relative files that exist in the runtime universe.\n"
        "- If no local target is verified, say NO_PATCHABLE_TARGET with a concrete blocked reason.\n"
        "- Never use placeholder paths, output/**, indexAI/** or docs/LOCAL_VALIDATION_EVIDENCE/** as patch targets.\n"
        "- Mention needed tool evidence in the proposal, but do not pretend prose is execution; the native tool-call continuation will execute through the broker.\n"
    )

def ollama_tool_call_tool_names() -> list[str]:
    return [
        "build_agent_agnostic_tool_inventory", "build_agent_memory_inventory", "build_agent_transient_request_context",
        "runtime_sqlite_memory", "select_semantic_code_chunks", "semantic_evidence_chunks",
        "ai_context_pack", "agent_runtime_debug_lab", "run_heap_code_execution_matrix",
        "run_heap_virtual_dev_environment", "synthesize_patch_candidates", "analyze_code_product_artifact",
    ]
def prompt_explicitly_requires_tool_call(prompt: str) -> bool:
    markers = ("must call", "devi chiamare", "use a native tool call", "by calling run_heap", "calling run_heap", "call run_heap")
    return any(marker in (prompt or "").lower() for marker in markers)
def ollama_tool_call_fallback_prompt() -> str:
    return (
        "IA-Carmine native tool decision. If the heap delta needs live broker evidence, call the best broker tool through message.tool_calls; "
        "otherwise answer NO_TOOL_NEEDED with the reason. Matrix, lab and patch synthesis are available, with broker-enriched args. "
        "This is a continuation of the provider heap delta, not a replacement."
    )
def ollama_tool_call_selection_prompt(prompt: str, provider_delta: str) -> str:
    tool_relevant = heap_patch_prompt_required(prompt) or prompt_explicitly_requires_tool_call(prompt)
    tools_available = ", ".join(ollama_tool_call_tool_names())
    decision_rule = (
        "Keep heap proposal text as primary. For code product, matrix, lab, patch synthesis, runtime refs or memory gaps, choose one broker tool through message.tool_calls. "
        "Use NO_TOOL_NEEDED only when current heap/matrix evidence already proves no broker action can improve the delta."
        if tool_relevant
        else "If yes, call one tool through message.tool_calls; otherwise answer NO_TOOL_NEEDED with reason."
    )
    return (
        "IA-Carmine provider continuation. You already produced heap delta content. Decide if that same delta needs a broker tool now. "
        f"{decision_rule} Do not replace the heap delta with tool-only output. "
        f"Broker enriches args. Available broker tools: {tools_available}.\n\nCURRENT_OPERATOR_CONTEXT:\n{(prompt or '')[:3500]}\n\nPROVIDER_HEAP_DELTA_ALREADY_EMITTED:\n{(provider_delta or '')[:1800]}"
    )
def normalize_ollama_tool_calls(chat_response: dict[str, Any]) -> list[dict[str, Any]]:
    message = chat_response.get("message") if isinstance(chat_response, dict) else {}
    if not isinstance(message, dict):
        return []
    calls = message.get("tool_calls")
    if not isinstance(calls, list):
        return []
    normalized: list[dict[str, Any]] = []
    for index, call in enumerate(calls, start=1):
        if not isinstance(call, dict):
            continue
        function = call.get("function") if isinstance(call.get("function"), dict) else {}
        name = str(function.get("name") or "").strip()
        if not name:
            continue
        args = function.get("arguments")
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                args = {"raw_arguments": args}
        if not isinstance(args, dict):
            args = {}
        normalized.append(
            {
                "id": str(call.get("id") or f"ollama_tool_call_{index:03d}"),
                "tool": name,
                "requirement": str(call.get("requirement") or ""),
                "reason": str(call.get("reason") or "ollama_native_tool_call"),
                "args": args,
                "native_provider": "ollama",
                "native_shape": "message.tool_calls[].function",
            }
        )
    return normalized
def parse_json_contract(text: str) -> dict[str, Any]:
    candidate = (text or "").strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            candidate = "\n".join(lines[1:-1]).strip()
    try:
        parsed = json.loads(candidate)
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}
def resolve_provider_python(repo_root: Path, python_exe: str | None = None) -> Path:
    if python_exe:
        return Path(python_exe).expanduser().resolve()
    env_python = os.environ.get("IA_CARMINE_PYTHON", "").strip()
    if env_python:
        return Path(env_python).expanduser().resolve()
    repo_python = repo_root / ".venv" / "Scripts" / "python.exe"
    if repo_python.is_file():
        return repo_python.resolve()
    return Path(sys.executable).resolve()

def _openvino_tool_loop_child_main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        if not isinstance(payload, dict):
            payload = {}
        result = run_openvino_tool_loop_child_payload(payload)
    except Exception as exc:  # noqa: BLE001 - child errors are normalized JSON evidence.
        result = {
            "performed": False,
            "supported": False,
            "classification": "openvino_tool_loop_child_error",
            "errors": [f"{type(exc).__name__}: {exc}"],
        }
    print(json.dumps(result, ensure_ascii=False))
    return 0


def openvino_tool_loop_report(
    *,
    repo_root: Path,
    prompt: str,
    timeout_seconds: float,
    max_new_tokens: int,
    device: str = "GPU.0",
    python_exe: str | None = None,
    allow_discovery: bool = True,
    tool_names: list[str] | None = None,
    max_prompt_chars: int = 900,
) -> dict[str, Any]:
    started = time.perf_counter()
    if allow_discovery:
        model_dir, model_dir_source = discover_openvino_tool_model_dir(repo_root)
    else:
        model_dir = (
            os.environ.get("IA_CARMINE_OPENVINO_TOOL_MODEL_DIR", "").strip()
            or os.environ.get("IA_CARMINE_GPU0_COMPANION_MODEL_DIR", "").strip()
            or os.environ.get("SPAZIOTEMPO_NPU_MODEL_DIR", "").strip()
            or os.environ.get("IA_CARMINE_NPU_MODEL_DIR", "").strip()
        )
        model_dir_source = "environment" if model_dir else "missing"
    base = {
        "native_tool_loop_provider": "openvino_genai",
        "native_tool_loop_requested": True,
        "native_tool_loop_supported": False,
        "native_tool_loop_performed": False,
        "native_tool_decision_prompted": True,
        "native_tool_decision": "unavailable",
        "native_tool_loop_device": device,
        "native_tool_call_count": 0,
        "tool_calls": [],
        "classification": "",
        "model_dir": model_dir,
        "model_dir_source": model_dir_source,
        "errors": [],
        "warnings": [],
        "elapsed_sec": 0.0,
    }
    if not model_dir:
        base["classification"] = "openvino_tool_loop_model_dir_unconfigured"
        base["warnings"].append(
            "No OpenVINO GenAI model dir configured by runtime environment. Configure IA_CARMINE_OPENVINO_TOOL_MODEL_DIR, IA_CARMINE_GPU0_COMPANION_MODEL_DIR, SPAZIOTEMPO_NPU_MODEL_DIR or IA_CARMINE_NPU_MODEL_DIR."
        )
        base["elapsed_sec"] = round(time.perf_counter() - started, 4)
        return base
    if not (Path(model_dir).expanduser() / "openvino_model.xml").is_file():
        base["classification"] = "openvino_tool_loop_model_dir_invalid"
        base["errors"].append(f"OpenVINO model dir lacks openvino_model.xml: {model_dir}")
        base["elapsed_sec"] = round(time.perf_counter() - started, 4)
        return base

    runner = resolve_provider_python(repo_root, python_exe)
    if not tool_names:
        tool_names = (
            ["run_heap_code_execution_matrix", "semantic_evidence_chunks"]
            if device == "NPU"
            else ollama_tool_call_tool_names()
        )
    tools_json = json.dumps(
        broker_tool_schemas(tool_names, compact=device == "NPU"),
        ensure_ascii=False,
    )
    force_tool_call = prompt_explicitly_requires_tool_call(prompt)
    structured_schema_json = json.dumps(
        {
            "type": "object",
            "properties": {
                "decision": {
                    "type": "string",
                    "enum": ["call_tool"] if force_tool_call else ["call_tool", "no_tool_needed"],
                },
                "tool": {"type": "string", "enum": ["", *list(tool_names)]},
                "args": {"type": "object"},
                "reason": {"type": "string"},
            },
            "required": ["decision", "tool", "reason"],
            "additionalProperties": False,
        },
        ensure_ascii=False,
    )
    prompt_limit = int(max_prompt_chars)
    if prompt_limit <= 0:
        base["classification"] = "openvino_tool_loop_invalid_prompt_limit"
        base["errors"].append("max_prompt_chars must be a positive operator/heap propagated value.")
        base["elapsed_sec"] = round(time.perf_counter() - started, 4)
        return base
    token_limit = int(max_new_tokens)
    if token_limit <= 0:
        base["classification"] = "openvino_tool_loop_invalid_token_limit"
        base["errors"].append("max_new_tokens must be a positive operator/heap propagated value.")
        base["elapsed_sec"] = round(time.perf_counter() - started, 4)
        return base
    dialogue_prompt = (
        "You are inside IA-Carmine. Produce a concise provider heap delta for this "
        "task before selecting tools. Include evidence, target/ref uncertainty and "
        "what tool evidence is needed next.\n\nTASK:\n" + (prompt or "")
    )[:prompt_limit]
    tool_prompt = (
        "Using the provider heap delta context, decide whether a native broker "
        "tool call is needed now. If the task asks for live code product, matrix, "
        "lab, validation or patch synthesis evidence, choose decision=call_tool. "
        "Otherwise choose decision=no_tool_needed. Always include tool: use an "
        "empty string only for no_tool_needed, and one broker tool name for call_tool. "
        "Args may be empty because the broker enriches resolved targets and output paths.\n\nTASK:\n"
        + (prompt or "")
    )[:prompt_limit]
    child_payload = {
        "model_dir": str(Path(model_dir).expanduser()),
        "device": device,
        "dialogue_prompt": dialogue_prompt,
        "tool_prompt": tool_prompt,
        "tools": json.loads(tools_json),
        "structured_schema": structured_schema_json,
        "force_tool_call": force_tool_call,
        "max_new_tokens": token_limit,
    }
    child_env = command_env(repo_root)
    child_env["PYTHONIOENCODING"] = "utf-8"
    try:
        hard_timeout = None if float(timeout_seconds or 0) <= 0 else float(timeout_seconds)
        completed = subprocess.run(
            [
                str(runner),
                "-m",
                "Tools.ai._shared.provider_tool_loop",
                "--openvino-tool-loop-child",
            ],
            cwd=str(repo_root),
            input=json.dumps(child_payload, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            env=child_env,
            timeout=hard_timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        report = dict(base)
        report["native_tool_loop_supported"] = True
        report["native_tool_decision"] = "timeout"
        report["classification"] = "openvino_native_tool_loop_timeout"
        report["stdout_tail"] = str(exc.stdout or "")[-2000:]
        report["stderr_tail"] = str(exc.stderr or "")[-2000:]
        report["warnings"].append(f"OpenVINO native tool loop timed out after {timeout_seconds}s.")
        report["elapsed_sec"] = round(time.perf_counter() - started, 4)
        return report
    raw = (completed.stdout or "").strip().splitlines()
    try:
        payload = json.loads(raw[-1]) if raw else {}
    except Exception:
        payload = {}
    report = dict(base)
    report["returncode"] = completed.returncode
    report["stdout_tail"] = (completed.stdout or "")[-2000:]
    report["stderr_tail"] = (completed.stderr or "")[-2000:]
    report["child_payload_model_dir"] = child_payload.get("model_dir")
    report["child_payload_device"] = child_payload.get("device")
    report["native_tool_loop_performed"] = bool(payload.get("performed"))
    report["native_tool_loop_supported"] = bool(payload.get("supported"))
    default_classification = "openvino_tool_loop_execution_failed" if completed.returncode != 0 else "openvino_tool_loop_unparseable"
    report["classification"] = str(payload.get("classification") or default_classification)
    report["available_devices"] = payload.get("devices") or []
    if payload.get("errors"):
        report["errors"].extend(str(item) for item in payload.get("errors") or [])
    report["provider_heap_delta_text"] = str(payload.get("provider_heap_delta_text") or "")
    report["response_text"] = str(payload.get("provider_heap_delta_text") or payload.get("response_text") or "")
    parsed = payload.get("parsed") if isinstance(payload.get("parsed"), dict) else {}
    tool_calls = parsed.get("tool_calls") if isinstance(parsed.get("tool_calls"), list) else []
    structured_call = payload.get("structured_call") if isinstance(payload.get("structured_call"), dict) else {}
    report["structured_tool_call_text"] = str(payload.get("structured_text") or "")
    report["structured_tool_call_payload"] = structured_call
    structured_decision = str(structured_call.get("decision") or "").strip() or ("call_tool" if "call_tool" in report["structured_tool_call_text"] else "")
    if not structured_decision and structured_call.get("tool"):
        structured_decision = "call_tool"
    if not tool_calls and structured_decision == "call_tool" and structured_call.get("tool"):
        tool_calls = [
            {
                "id": "openvino_structured_tool_call_001",
                "tool": str(structured_call.get("tool")),
                "requirement": "",
                "reason": str(structured_call.get("reason") or "openvino_structured_tool_call"),
                "args": structured_call.get("args")
                if isinstance(structured_call.get("args"), dict)
                else {},
                "native_provider": "openvino_genai",
                "native_shape": "StructuredOutputConfig.json_schema",
            }
        ]
    for call in tool_calls:
        if isinstance(call, dict):
            call["semantic_task_excerpt"] = tool_prompt[:500]
            call["semantic_contract"] = "provider_native_tool_call_for_current_operator_task"
    report["tool_calls"] = tool_calls
    report["native_tool_call_count"] = len(tool_calls)
    report["native_tool_loop_requested"] = bool(tool_calls) or structured_decision == "call_tool"
    report["native_tool_decision"] = structured_decision or (
        "call_tool" if tool_calls else "no_tool_needed"
    )
    if tool_calls and structured_call.get("tool"):
        report["classification"] = "openvino_structured_tool_call_emitted"
    elif structured_decision == "call_tool":
        report["classification"] = "openvino_native_tool_call_incomplete"
        report["warnings"].append("OpenVINO selected call_tool but did not provide a broker tool name.")
    elif report["native_tool_loop_performed"] and not tool_calls:
        report["classification"] = "openvino_native_tool_not_selected"
    if completed.returncode != 0 and not report["native_tool_loop_supported"]:
        report["errors"].append(report["stderr_tail"] or report["stdout_tail"])
    report["elapsed_sec"] = round(time.perf_counter() - started, 4)
    return report


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--openvino-tool-loop-child", action="store_true")
    args = parser.parse_args()
    if args.openvino_tool_loop_child:
        return _openvino_tool_loop_child_main()
    parser.error("No provider_tool_loop command selected.")
    return 2


if __name__ == "__main__":
    raise SystemExit(_main())
