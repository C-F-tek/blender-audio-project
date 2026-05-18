#!/usr/bin/env python3
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from Tools.ai._shared.provider_probe_paths import ensure_repo_imports


def run_ollama_probe(
    repo_root: Path,
    model: str | None,
    prompt: str | None = None,
    max_new_tokens: int = 64,
    num_ctx: int | None = None,
) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from Tools.ai._shared.provider_tool_loop import (  # noqa: PLC0415
        broker_tool_schemas,
        heap_patch_prompt_required,
        normalize_ollama_tool_calls,
        ollama_tool_call_fallback_prompt,
        ollama_tool_call_selection_prompt,
        ollama_tool_call_tool_names,
        parse_json_contract,
    )
    from Tools.npu.provider_mesh._shared.ollama_runtime import (  # noqa: PLC0415
        OllamaSession,
        choose_model,
        is_server_ready,
        list_models,
        list_models_from_disk,
    )
    from Tools.ai.runtime_tool.file_refs.classifier import (  # noqa: PLC0415
        extract_target_refs,
        extract_validation_refs,
    )
    from Tools.npu.pipeline import parse_provider_result  # noqa: PLC0415

    started = time.perf_counter()
    models = list_models() if is_server_ready() else list_models_from_disk()
    selected_model = choose_model(model, models)
    if not selected_model:
        return {
            "lane": "ollama",
            "passed": False,
            "provider_execution_performed": False,
            "error": "no Ollama model available",
            "elapsed_sec": round(time.perf_counter() - started, 4),
        }

    text = ""
    raw_chat_response: dict[str, Any] = {}
    native_tool_calls: list[dict[str, Any]] = []
    native_tool_decision_prompted = bool(prompt and prompt.strip())
    native_tool_loop_requested = False
    prompt_attempts: list[dict[str, Any]] = []
    with OllamaSession(
        model=selected_model,
        shutdown_server=False,
        unload_model=True,
        num_ctx=num_ctx,
    ) as session:
        if native_tool_decision_prompted:
            proposal_prompt = (prompt or "").strip()
            proposal_text = session.generate(
                proposal_prompt,
                max_new_tokens=max_new_tokens,
                temperature=0.0,
            )
            text = (proposal_text or "").strip()
            prompt_attempts.append(
                {
                    "attempt": 1,
                    "phase": "heap_delta",
                    "prompt_chars": len(proposal_prompt),
                    "text_chars": len(text),
                    "text_preview": text[:120],
                    "max_new_tokens": max_new_tokens,
                    "native_tool_loop_requested": False,
                    "native_tool_call_count": 0,
                }
            )
            tool_prompts = [ollama_tool_call_selection_prompt(proposal_prompt, text)]
            if not text:
                tool_prompts.append(ollama_tool_call_fallback_prompt())
            for index, tool_prompt in enumerate(tool_prompts, start=2):
                raw_chat_response = session.chat(
                    [{"role": "user", "content": tool_prompt}],
                    tools=broker_tool_schemas(ollama_tool_call_tool_names()),
                    max_new_tokens=max_new_tokens,
                    temperature=0.0,
                )
                message = raw_chat_response.get("message")
                message = message if isinstance(message, dict) else {}
                candidate = str(message.get("content") or "")
                native_tool_calls = normalize_ollama_tool_calls(raw_chat_response)
                for call in native_tool_calls:
                    call["semantic_task_excerpt"] = tool_prompt[:500]
                    call["semantic_contract"] = "provider_native_tool_call_for_current_operator_task"
                prompt_attempts.append(
                    {
                        "attempt": index,
                        "phase": "native_tool_call",
                        "prompt_chars": len(tool_prompt),
                        "text_chars": len(candidate),
                        "text_preview": candidate[:120],
                        "max_new_tokens": max_new_tokens,
                        "native_tool_loop_requested": True,
                        "native_tool_call_count": len(native_tool_calls),
                    }
                )
                if native_tool_calls:
                    if not text and candidate.strip():
                        text = candidate.strip()
                    break
        else:
            prompts = [
                'Return exactly this JSON object and no prose: {"ok": true, "lane": "ollama"}',
                '{"ok": true, "lane": "ollama"}',
            ]
            for index, probe_prompt in enumerate(prompts, start=1):
                candidate = session.generate(
                    probe_prompt,
                    max_new_tokens=max_new_tokens,
                    temperature=0.0,
                )
                candidate = candidate or ""
                prompt_attempts.append(
                    {
                        "attempt": index,
                        "phase": "probe",
                        "prompt_chars": len(probe_prompt),
                        "text_chars": len(candidate),
                        "text_preview": candidate[:120],
                        "max_new_tokens": max_new_tokens,
                        "native_tool_loop_requested": False,
                        "native_tool_call_count": 0,
                    }
                )
                if candidate.strip():
                    text = candidate
                    break

    parsed = parse_provider_result(
        {"response": text},
        provider="ollama",
        model=selected_model,
        executed=True,
        allow_json=True,
    )
    parsed_json = (
        parsed.parsed_json
        if isinstance(parsed.parsed_json, dict)
        else parse_json_contract(text)
    )
    contract_response = str(
        parsed_json.get("response_text")
        or parsed_json.get("markdown")
        or parsed_json.get("proposal")
        or ""
    ).strip()
    textual_tool_calls = parsed_json.get("tool_calls") or parsed_json.get("TOOL_CALLS") or []
    if not isinstance(textual_tool_calls, list):
        textual_tool_calls = []
    if not textual_tool_calls and parsed_json.get("name"):
        textual_tool_calls = [
            {
                "tool": str(parsed_json.get("name")),
                "args": parsed_json.get("arguments")
                if isinstance(parsed_json.get("arguments"), dict)
                else {},
                "native_provider": "ollama",
                "native_shape": "content_json_tool_call_not_native",
            }
        ]
    target_files = parsed_json.get("target_files") or parsed_json.get("TARGET_FILES") or []
    validation_commands = (
        parsed_json.get("validation_commands") or parsed_json.get("VALIDATION_COMMANDS") or []
    )
    if not isinstance(target_files, list):
        target_files = []
    if not isinstance(validation_commands, list):
        validation_commands = []
    response_text = contract_response or text.strip()
    if not target_files:
        target_files = extract_target_refs(response_text)
    if not validation_commands:
        validation_commands = extract_validation_refs(response_text)
    empty_output = not response_text.strip() and not native_tool_calls
    native_classification = "ollama_native_tool_decision_not_prompted"
    warnings: list[str] = []
    native_tool_loop_requested = bool(native_tool_calls)
    if native_tool_calls:
        native_classification = "ollama_native_tool_calls_emitted"
    elif native_tool_decision_prompted:
        native_classification = "ollama_native_tool_not_selected"
    return {
        "lane": "ollama",
        "passed": (not empty_output) and (parsed.ok or bool(prompt and prompt.strip())),
        "provider_execution_performed": True,
        "elapsed_sec": round(time.perf_counter() - started, 4),
        "selected_model": selected_model,
        "num_ctx": num_ctx,
        "request_prompt": prompt or "",
        "response_text": response_text,
        "raw_response_text": text.strip(),
        "json_contract_requested": heap_patch_prompt_required(prompt or ""),
        "json_contract_passed": bool(parsed.json_ok and isinstance(parsed_json, dict)),
        "tool_calls": native_tool_calls,
        "textual_tool_calls": textual_tool_calls,
        "native_tool_loop_provider": "ollama",
        "native_tool_loop_requested": native_tool_loop_requested,
        "native_tool_loop_supported": True,
        "native_tool_loop_performed": bool(native_tool_decision_prompted),
        "native_tool_decision_prompted": native_tool_decision_prompted,
        "native_tool_decision": "call_tool" if native_tool_calls else "no_tool_needed",
        "native_tool_loop_classification": native_classification,
        "native_tool_call_count": len(native_tool_calls),
        "warnings": warnings,
        "raw_chat_response": raw_chat_response,
        "target_files": [str(item) for item in target_files if str(item).strip()],
        "validation_commands": [str(item) for item in validation_commands if str(item).strip()],
        "model_count": len(models),
        "server_ready": is_server_ready(),
        "empty_output": empty_output,
        "error": (
            "empty Ollama generation output"
            if empty_output
            else None
        ),
        "parsed_result": parsed.to_dict(),
        "prompt_attempts": prompt_attempts,
        "text_preview": text[:200],
    }
