#!/usr/bin/env python3
from __future__ import annotations
import time
from pathlib import Path
from typing import Any
from ia_carmine._shared.ollama_gpu_residency import gpu_residency_summary, ollama_ps_snapshot
from ia_carmine._shared.ollama_server_process import server_process_evidence
from ia_carmine._shared.gpu_runtime_sampling import GpuRuntimeSampler
from ia_carmine._shared.ollama_provider_selection import operator_gpu_observation_block_reason, select_ollama_provider_model
from ia_carmine._shared.provider_ollama_report import build_ollama_probe_report, ollama_report_context
from ia_carmine._shared.provider_ollama_probe_helpers import PartialWriter, parsed_contract_fields, positive_provider_value, selection_blocked_report
from ia_carmine._shared.provider_ollama_unload import finalize_ollama_unload_snapshots
from ia_carmine._shared.provider_replight import provider_replight_fields
from ia_carmine._shared.provider_probe_paths import ensure_repo_imports
from ia_carmine._shared.provider_work_verification import full_gpu_requested, provider_work_status, response_likely_incomplete as is_response_likely_incomplete
from ia_carmine.providers.ollama.runtime_evidence import apply_ollama_lane_evidence, ollama_lane_role
def run_ollama_probe(
    repo_root: Path,
    model: str | None,
    prompt: str | None = None,
    max_new_tokens: int = 64,
    num_ctx: int | None = None,
    gpu_layers: str | int | None = "all",
    num_thread: int | None = None,
    keep_alive: str = "0s",
    partial_output: str | Path | None = None,
    require_gpu_residency: bool = True,
    replight_mode: bool = False,
    context_candidates: str = "8192,4096",
    strict_provider_model: bool = False,
    operator_gpu_observation: str = "",
    lane: str = "gpu1_planner",
    role: str = "",
    base_url: str | None = None,
    gpu0_vulkan_policy_verified: bool = False,
    unload_model: bool = True,
) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from ia_carmine._shared.provider_tool_loop import (  # noqa: PLC0415
        broker_tool_schemas,
        heap_patch_prompt_required,
        normalize_ollama_tool_calls,
        ollama_tool_call_fallback_prompt,
        ollama_tool_call_selection_prompt,
        ollama_tool_call_tool_names,
        parse_json_contract,
        prompt_explicitly_requires_tool_call,
    )
    from ia_carmine.providers.ollama import DEFAULT_BASE_URL, OllamaSession, is_server_ready, list_models, list_models_from_disk  # noqa: PLC0415
    from ia_carmine.runtime.runtime_tool.file_refs.classifier import extract_rejected_validation_refs, extract_target_refs, extract_validation_refs  # noqa: PLC0415
    from ia_carmine.providers.npu.pipeline import parse_provider_result  # noqa: PLC0415
    started = time.perf_counter()
    provider_lane = str(lane or "gpu1_planner").strip()
    provider_role = str(role or ollama_lane_role(provider_lane)).strip()
    effective_base_url = str(base_url or DEFAULT_BASE_URL)
    server_process = server_process_evidence(effective_base_url)
    propagated_max_new_tokens = positive_provider_value("max_new_tokens", max_new_tokens)
    server_ready = is_server_ready(effective_base_url)
    models = list_models(effective_base_url) if server_ready else list_models_from_disk()
    selection = select_ollama_provider_model(
        model or "auto",
        models,
        num_ctx=int(num_ctx or 0),
        context_candidates=context_candidates,
        strict=bool(strict_provider_model),
    )
    selected_model = str(selection.get("selected_provider_model") or "").strip()
    if selection.get("selected_ollama_num_ctx"):
        num_ctx = int(selection["selected_ollama_num_ctx"])
    if selection.get("blocked") or not selected_model:
        reason = str(selection.get("blocked_reason") or "no Ollama model available")
        return selection_blocked_report(
            lane=provider_lane,
            role=provider_role,
            model=model,
            selected_model=selected_model,
            reason=reason,
            selection=selection,
            elapsed_sec=time.perf_counter() - started,
            base_url=effective_base_url,
            server_process=server_process,
        )

    text = ""
    raw_chat_response: dict[str, Any] = {}
    native_tool_calls: list[dict[str, Any]] = []
    native_tool_decision_prompted = bool(prompt and prompt.strip())
    heap_delta_text_required = bool(heap_patch_prompt_required(prompt or ""))
    explicit_tool_call_required = prompt_explicitly_requires_tool_call(prompt or "")
    native_tool_loop_relevant = bool(
        native_tool_decision_prompted
        and (explicit_tool_call_required or heap_delta_text_required)
    )
    prompt_attempts: list[dict[str, Any]] = []
    partial_json = Path(partial_output).expanduser() if partial_output else None
    partial_markdown_output = partial_json.with_suffix(".md") if partial_json else None
    generation_stats: dict[str, Any] = {}
    gpu_runtime_summary: dict[str, Any] = {}
    provider_native_tool_api_adapter_available = callable(getattr(OllamaSession, "chat", None))
    provider_native_tool_api_supported = provider_native_tool_api_adapter_available
    provider_native_tool_api_error = ""
    provider_native_tool_api_attempt_error = ""
    native_tool_api_attempted = False
    native_tool_api_completed = False
    write_partial = PartialWriter(
        path=partial_json,
        markdown_path=partial_markdown_output,
        lane=provider_lane,
        selected_model=selected_model,
        num_ctx=num_ctx,
        gpu_layers=gpu_layers,
        num_thread=num_thread,
        prompt=prompt,
        started=started,
    )
    ollama_ps_snapshots: list[dict[str, Any]] = []
    session_ollama_exe: Any = None
    with OllamaSession(
        model=selected_model,
        keep_alive=keep_alive,
        shutdown_server=False,
        unload_model=bool(unload_model),
        base_url=effective_base_url,
        gpu_layers=gpu_layers,
        num_thread=num_thread,
        num_ctx=num_ctx,
    ) as session:
        session_ollama_exe = getattr(session, "ollama_exe", None)
        ollama_ps_snapshots.append(
            ollama_ps_snapshot(
                session_ollama_exe,
                selected_model,
                "before",
                base_url=effective_base_url,
            )
        )
        gpu_sampler = GpuRuntimeSampler(target_pid=server_process.get("ollama_server_pid"))
        gpu_sampler.start()
        try:
            if native_tool_decision_prompted:
                proposal_prompt = (prompt or "").strip()
                proposal_text = session.generate(
                    proposal_prompt,
                    max_new_tokens=propagated_max_new_tokens,
                    temperature=0.0,
                    partial_callback=write_partial if partial_json else None,
                )
                generation_stats = dict(getattr(session, "last_generate_result", {}) or {})
                text = (proposal_text or "").strip()
                prompt_attempts.append(
                    {
                        "attempt": 1,
                        "phase": "heap_delta",
                        "prompt_chars": len(proposal_prompt),
                        "text_chars": len(text),
                        "text_present": bool(text),
                        "max_new_tokens": propagated_max_new_tokens,
                        "max_new_tokens_source": "operator_heap_propagated",
                        "native_tool_loop_requested": False,
                        "native_tool_call_count": 0,
                    }
                )
                if not text:
                    native_tool_loop_relevant = True
                if native_tool_loop_relevant:
                    tool_prompts = [ollama_tool_call_selection_prompt(proposal_prompt, text)]
                    if not text:
                        tool_prompts.append(ollama_tool_call_fallback_prompt())
                    for index, tool_prompt in enumerate(tool_prompts, start=2):
                        if not provider_native_tool_api_adapter_available:
                            provider_native_tool_api_error = "provider_adapter_missing_chat_method"
                            provider_native_tool_api_attempt_error = provider_native_tool_api_error
                            prompt_attempts.append(
                                {
                                    "attempt": index,
                                    "phase": "native_tool_call_api_error",
                                    "prompt_chars": len(tool_prompt),
                                    "text_chars": 0,
                                    "text_present": False,
                                    "max_new_tokens": propagated_max_new_tokens,
                                    "max_new_tokens_source": "operator_heap_propagated",
                                    "native_tool_loop_requested": True,
                                    "native_tool_api_supported": False,
                                    "native_tool_api_error": provider_native_tool_api_error,
                                    "native_tool_call_count": 0,
                                }
                            )
                            break
                        try:
                            native_tool_api_attempted = True
                            raw_chat_response = session.chat(
                                [{"role": "user", "content": tool_prompt}],
                                tools=broker_tool_schemas(ollama_tool_call_tool_names()),
                                max_new_tokens=propagated_max_new_tokens,
                                temperature=0.0,
                            )
                        except Exception as exc:  # noqa: BLE001
                            provider_native_tool_api_attempt_error = f"{type(exc).__name__}: {exc}"
                            provider_native_tool_api_error = provider_native_tool_api_attempt_error
                            raw_chat_response = {}
                            prompt_attempts.append(
                                {
                                    "attempt": index,
                                    "phase": "native_tool_call_api_attempt_failed",
                                    "prompt_chars": len(tool_prompt),
                                    "text_chars": 0,
                                    "text_present": False,
                                    "max_new_tokens": propagated_max_new_tokens,
                                    "max_new_tokens_source": "operator_heap_propagated",
                                    "native_tool_loop_requested": True,
                                    "native_tool_api_supported": True,
                                    "native_tool_api_attempted": True,
                                    "native_tool_api_completed": False,
                                    "native_tool_api_error": provider_native_tool_api_error,
                                    "native_tool_call_count": 0,
                                }
                            )
                            break
                        if not isinstance(raw_chat_response, dict):
                            provider_native_tool_api_attempt_error = (
                                f"invalid_chat_response_type:{type(raw_chat_response).__name__}"
                            )
                            provider_native_tool_api_error = provider_native_tool_api_attempt_error
                            raw_chat_response = {}
                            prompt_attempts.append(
                                {
                                    "attempt": index,
                                    "phase": "native_tool_call_api_attempt_failed",
                                    "prompt_chars": len(tool_prompt),
                                    "text_chars": 0,
                                    "text_present": False,
                                    "max_new_tokens": propagated_max_new_tokens,
                                    "max_new_tokens_source": "operator_heap_propagated",
                                    "native_tool_loop_requested": True,
                                    "native_tool_api_supported": True,
                                    "native_tool_api_attempted": True,
                                    "native_tool_api_completed": False,
                                    "native_tool_api_error": provider_native_tool_api_error,
                                    "native_tool_call_count": 0,
                                }
                            )
                            break
                        native_tool_api_completed = True
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
                                "text_present": bool(candidate.strip()),
                                "max_new_tokens": propagated_max_new_tokens,
                                "max_new_tokens_source": "operator_heap_propagated",
                                "native_tool_loop_requested": True,
                                "native_tool_api_supported": True,
                                "native_tool_api_completed": True,
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
                        max_new_tokens=propagated_max_new_tokens,
                        temperature=0.0,
                    )
                    generation_stats = dict(getattr(session, "last_generate_result", {}) or {})
                    candidate = candidate or ""
                    prompt_attempts.append(
                        {
                            "attempt": index,
                            "phase": "probe",
                            "prompt_chars": len(probe_prompt),
                            "text_chars": len(candidate),
                            "text_present": bool(candidate.strip()),
                            "max_new_tokens": propagated_max_new_tokens,
                            "max_new_tokens_source": "operator_heap_propagated",
                            "native_tool_loop_requested": False,
                            "native_tool_call_count": 0,
                        }
                    )
                    if candidate.strip():
                        text = candidate
                        break
            ollama_ps_snapshots.append(
                ollama_ps_snapshot(
                    session_ollama_exe,
                    selected_model,
                    "during",
                    base_url=effective_base_url,
                )
            )
        finally:
            gpu_runtime_summary = gpu_sampler.stop()
    ollama_ps_snapshots.append(
        ollama_ps_snapshot(session_ollama_exe, selected_model, "after", base_url=effective_base_url)
    )
    unload_performed, unload_verified = finalize_ollama_unload_snapshots(
        snapshots=ollama_ps_snapshots,
        session_ollama_exe=session_ollama_exe,
        selected_model=selected_model,
        base_url=effective_base_url,
        unload_model=bool(unload_model),
    )

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
    parsed_fields = parsed_contract_fields(
        parsed_json=parsed_json,
        text=text,
        native_tool_calls=native_tool_calls,
        extract_target_refs=extract_target_refs,
        extract_validation_refs=extract_validation_refs,
        extract_rejected_validation_refs=extract_rejected_validation_refs,
    )
    response_text = parsed_fields["response_text"]
    textual_tool_calls = parsed_fields["textual_tool_calls"]
    target_files = parsed_fields["target_files"]
    validation_commands = parsed_fields["validation_commands"]
    rejected_validation_refs = parsed_fields["rejected_validation_refs"]
    empty_output = parsed_fields["empty_output"]
    response_likely_incomplete = bool(
        heap_delta_text_required and is_response_likely_incomplete(response_text)
    )
    native_classification = "ollama_native_tool_decision_not_prompted"
    warnings: list[str] = []
    errors: list[str] = []
    provider_native_tool_call_required = bool(explicit_tool_call_required)
    native_tool_loop_requested = bool(native_tool_calls or provider_native_tool_call_required)
    provider_native_tool_api_unavailable = bool(
        provider_native_tool_call_required and not provider_native_tool_api_adapter_available
    )
    provider_native_tool_api_attempt_failed = bool(
        provider_native_tool_call_required
        and provider_native_tool_api_adapter_available
        and native_tool_api_attempted
        and not native_tool_api_completed
        and provider_native_tool_api_attempt_error
    )
    provider_native_tool_call_required_unmet = bool(
        provider_native_tool_call_required
        and provider_native_tool_api_adapter_available
        and not provider_native_tool_api_attempt_failed
        and native_tool_loop_relevant
        and not native_tool_calls
    )
    if native_tool_calls:
        native_classification = "ollama_native_tool_calls_emitted"
    elif native_tool_loop_relevant:
        native_classification = "ollama_native_tool_not_selected_for_heap_delta"
        warnings.append(
            "Heap/code-product provider task did not emit a native broker tool_call; text heap delta is raw evidence only."
        )
    if provider_native_tool_api_unavailable:
        native_classification = "ollama_native_tool_api_unavailable"
        errors.append("provider_native_tool_api_unavailable")
    elif provider_native_tool_api_attempt_failed:
        native_classification = "ollama_native_tool_api_attempt_failed"
        errors.append("provider_native_tool_api_attempt_failed")
    elif provider_native_tool_call_required_unmet:
        errors.append("provider_native_tool_call_required_unmet")
    if rejected_validation_refs:
        warnings.append(
            "Rejected bare file refs in VALIDATION_COMMANDS: "
            + ", ".join(str(item) for item in rejected_validation_refs[:6])
        )
    elif heap_patch_prompt_required(prompt or ""):
        native_classification = "ollama_native_tool_not_requested_text_delta_primary"
    elif native_tool_decision_prompted:
        native_classification = "ollama_native_tool_not_selected"
    if heap_delta_text_required and not response_text.strip():
        warnings.append(
            "Heap/code-product provider task requires normal heap proposal text in addition to tool calls."
        )
    if response_likely_incomplete:
        warnings.append(
            f"{provider_lane} heap proposal text looks incomplete; keep the lane operational but reject this proposal chunk for refinement."
        )
    passed = (not empty_output) and (parsed.ok or bool(prompt and prompt.strip()))
    if heap_delta_text_required and not response_text.strip():
        passed = False
    residency = gpu_residency_summary(
        ollama_ps_snapshots,
        full_gpu_requested=full_gpu_requested(gpu_layers),
    )
    operator_block_reason = operator_gpu_observation_block_reason(operator_gpu_observation)
    if operator_block_reason:
        residency["provider_device_verified"] = False
        residency["product_blocked_reason"] = operator_block_reason
        residency["operator_gpu_observation_blocked"] = True
    residency = apply_ollama_lane_evidence(
        lane=provider_lane,
        residency=residency,
        require_gpu_residency=require_gpu_residency,
    )
    if require_gpu_residency and not residency["provider_device_verified"]:
        errors.append(str(residency.get("product_blocked_reason") or "gpu1_ollama_gpu_residency_unproven_or_cpu_bound"))
        passed = False
    ollama_residency_verified = bool(residency.get("provider_device_verified"))
    gpu0_vulkan_compute_observed = bool(
        provider_lane == "gpu0_peer"
        and float(gpu_runtime_summary.get("windows_gpu_engine_phys0_utilization_peak_percent") or 0.0)
        >= 1.0
    )
    gpu0_vulkan_sdk_workload_verified = bool(
        provider_lane == "gpu0_peer"
        and gpu0_vulkan_policy_verified
        and int(generation_stats.get("eval_count") or 0) > 0
        and ollama_residency_verified
    )
    ollama_compute_verified = bool(
        not replight_mode
        and not residency.get("operator_gpu_observation_blocked")
        and ollama_residency_verified
        and (
            gpu0_vulkan_compute_observed
            or gpu0_vulkan_sdk_workload_verified
            if provider_lane == "gpu0_peer"
            else gpu_runtime_summary.get("gpu_compute_observed")
        )
    )
    work_status = provider_work_status(
        lane=provider_lane,
        report={
            **residency,
            **generation_stats,
            **gpu_runtime_summary,
            "provider_device_verified": ollama_residency_verified,
            "ollama_residency_verified": ollama_residency_verified,
            "ollama_compute_verified": ollama_compute_verified,
            "selected_model": selected_model,
            "response_text": response_text,
            "replight_mode": replight_mode,
            "provider_loaded": True,
            "gpu0_vulkan_compute_observed": gpu0_vulkan_compute_observed,
            "gpu0_vulkan_sdk_workload_verified": gpu0_vulkan_sdk_workload_verified,
            "gpu0_vulkan_policy_verified": gpu0_vulkan_policy_verified,
            "ollama_unload_performed": unload_performed,
            "ollama_unload_verified": unload_verified,
        },
        default_role=provider_role,
    )
    provider_work_verified = bool(work_status.get("provider_work_verified"))
    if (
        provider_native_tool_api_unavailable
        or provider_native_tool_api_attempt_failed
        or provider_native_tool_call_required_unmet
    ):
        provider_work_verified = False
        work_status["provider_work_verified"] = False
        work_status["provider_requirement_complete"] = False
        work_status["semantic_contract_passed"] = False
        work_status["provider_rejection_reason"] = (
            "provider_native_tool_api_unavailable"
            if provider_native_tool_api_unavailable
            else (
                "provider_native_tool_api_attempt_failed"
                if provider_native_tool_api_attempt_failed
                else "provider_native_tool_call_required_unmet"
            )
        )
    provider_execution_attempted = bool(
        response_text
        or prompt_attempts
        or generation_stats.get("eval_count")
        or generation_stats.get("prompt_eval_count")
        or generation_stats.get("total_duration")
    )
    provider_io_observed = provider_execution_attempted
    provider_execution_performed = provider_work_verified
    if not provider_work_verified and work_status.get("provider_rejection_reason"):
        target = warnings if replight_mode else errors
        target.append(str(work_status["provider_rejection_reason"]))
        if not replight_mode:
            passed = False
    replight = provider_replight_fields(
        lane=provider_lane,
        role=provider_role,
        report={
            **residency,
            **generation_stats,
            **gpu_runtime_summary,
            **work_status,
            "provider_execution_performed": provider_execution_performed,
            "provider_execution_attempted": provider_execution_attempted,
            "provider_io_observed": provider_io_observed,
            "ollama_residency_verified": ollama_residency_verified,
            "ollama_compute_verified": ollama_compute_verified,
            "selected_model": selected_model,
            "response_text": response_text,
            "request_prompt": prompt or "",
            "native_tool_loop_supported": provider_native_tool_api_supported,
            "ollama_base_url": effective_base_url,
            "ollama_unload_performed": unload_performed,
            "ollama_unload_verified": unload_verified,
            "gpu0_vulkan_compute_observed": gpu0_vulkan_compute_observed,
            "gpu0_vulkan_sdk_workload_verified": gpu0_vulkan_sdk_workload_verified,
            "gpu0_vulkan_policy_verified": gpu0_vulkan_policy_verified,
            **server_process,
        },
        default_model=selected_model,
    )
    if replight_mode and not replight["replight_passed"]:
        errors.append(str(replight["replight_blocked_reason"]))
        passed = False
    return build_ollama_probe_report(ollama_report_context(locals()))
