"""Parent-orchestrated GPU1 native tool chat loop."""

from __future__ import annotations

from copy import deepcopy

from ia_carmine._shared.file_backed_transport import artifact_ref
from ia_carmine.runtime.heap_gate.provider_lane_launch import (
    start_provider_item,
    write_provider_launch_manifest,
)
from ia_carmine.runtime.heap_gate.provider_process_collection import collect_provider_processes
from ia_carmine.runtime.heap_gate.broker_result_validation import broker_result_passed
from ia_carmine.runtime.heap_gate.gpu1_tool_result_messages import gpu1_tool_result_payload
from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, json, read_json, repo_rel, write_json_report
from ia_carmine.runtime.heap_gate.tool_broker_native_calls import (
    provider_native_tool_request_id,
    publish_provider_report_native_tool_calls,
)

MAX_GPU1_NATIVE_TOOL_SUBTURNS = 5


def run_gpu1_native_tool_chat_loop(
    gate: Any,
    *,
    primary_item: dict[str, Any],
    prepared: list[dict[str, Any]],
    work_dir: Path,
    launch_manifest: Path,
    round_id: int,
    revision: int,
    timeout_seconds: int,
    time_contract: dict[str, Any],
    leader_prompt: str,
    absorb: Any,
) -> dict[str, Any]:
    """Run GPU1 as chat(messages, tools=...), resuming after broker results."""
    chat_dir = work_dir / "gpu1_native_tool_chat_loop"
    chat_dir.mkdir(parents=True, exist_ok=True)
    history_path = chat_dir / f"gpu1_chat_history_revision_{revision:03d}.json"
    write_json_report([{"role": "user", "content": leader_prompt}], history_path)
    base_command = list(primary_item["command"])
    base_spec = deepcopy(primary_item["spec"])
    last_item = primary_item
    max_subturns = max(1, min(MAX_GPU1_NATIVE_TOOL_SUBTURNS, int(getattr(gate.args, "max_provider_revisions", 5) or 5)))
    passed_request_ids: list[str] = []
    failed_request_ids: list[str] = []
    for subturn in range(max_subturns):
        output_path = _subturn_output_path(work_dir, revision, subturn)
        history_output = chat_dir / f"gpu1_chat_history_revision_{revision:03d}_subturn_{subturn:02d}.json"
        item = primary_item if subturn == 0 else _clone_subturn_item(primary_item, subturn)
        if subturn > 0:
            prepared.append(item)
        item["gpu1_tool_loop_subturn"] = subturn
        item["spec"] = deepcopy(base_spec)
        item["spec"]["output"] = output_path
        item["command"] = _subturn_command(
            base_command,
            output_path=output_path,
            history_path=history_path,
            history_output=history_output,
            subturn=subturn,
        )
        start_provider_item(gate, item, round_id, revision)
        write_provider_launch_manifest(
            gate,
            launch_manifest,
            prepared,
            round_id,
            revision,
            time_contract,
            f"gpu1_native_tool_chat_subturn_{subturn}_started",
        )
        collect_provider_processes(
            gate,
            [item],
            timeout_seconds,
            round_id,
            revision,
            on_completed=absorb,
        )
        if item.get("completed") is not None:
            absorb(item)
        report = item.get("provider_report") if isinstance(item.get("provider_report"), dict) else {}
        _append_assistant_message(gate, history_path, report)
        calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
        if not calls:
            _persist_loop_state(gate, report, history_path, closed=True, subturn=subturn)
            last_item = item
            break
        request_links = _expected_request_links(gate, report)
        request_ids = [item["request_id"] for item in request_links]
        published = publish_provider_report_native_tool_calls(
            gate, report, round_id, gate.read_events()
        )
        if not published:
            _persist_loop_state(gate, report, history_path, closed=False, subturn=subturn)
            last_item = item
            break
        gate.run_bridge()
        results = _matching_broker_results(gate, request_ids)
        missing_result_ids = [
            request_id
            for request_id in request_ids
            if not any(
                str(result.get("request_id") or "") == request_id
                or str(result.get("normalized_request_id") or "") == request_id
                for result in results
            )
        ]
        if missing_result_ids:
            gate.errors.append(
                "gpu1_tool_result_pending:" + ",".join(missing_result_ids[:6])
            )
            _persist_loop_state(gate, report, history_path, closed=False, subturn=subturn)
            last_item = item
            break
        _append_tool_result_messages(gate, history_path, results, request_links)
        for result in results:
            request_id = str(result.get("request_id") or result.get("normalized_request_id") or "")
            if broker_result_passed(result, repo_root=gate.repo_root):
                passed_request_ids.append(request_id)
            else:
                failed_request_ids.append(request_id)
        _persist_loop_state(gate, report, history_path, closed=False, subturn=subturn)
        last_item = item
    else:
        last_item = _run_soft_stop_finalization(
            gate,
            primary_item=primary_item,
            prepared=prepared,
            base_command=base_command,
            base_spec=base_spec,
            work_dir=work_dir,
            launch_manifest=launch_manifest,
            round_id=round_id,
            revision=revision,
            timeout_seconds=timeout_seconds,
            time_contract=time_contract,
            history_path=history_path,
            subturn=max_subturns,
            passed_request_ids=passed_request_ids,
            failed_request_ids=failed_request_ids,
            absorb=absorb,
        )
    return last_item


def _clone_subturn_item(item: dict[str, Any], subturn: int) -> dict[str, Any]:
    clone = deepcopy(item)
    clone.update(
        {
            "process": None,
            "completed": None,
            "started_at": "",
            "completed_at": "",
            "elapsed_seconds": None,
            "pid": None,
            "absorbed": False,
            "provider_report": {},
            "gpu1_tool_loop_subturn": subturn,
        }
    )
    return clone


def _run_soft_stop_finalization(
    gate: Any,
    *,
    primary_item: dict[str, Any],
    prepared: list[dict[str, Any]],
    base_command: list[Any],
    base_spec: dict[str, Any],
    work_dir: Path,
    launch_manifest: Path,
    round_id: int,
    revision: int,
    timeout_seconds: int,
    time_contract: dict[str, Any],
    history_path: Path,
    subturn: int,
    passed_request_ids: list[str],
    failed_request_ids: list[str],
    absorb: Any,
) -> dict[str, Any]:
    _append_soft_stop_message(history_path, subturn, passed_request_ids, failed_request_ids)
    output_path = _subturn_output_path(work_dir, revision, subturn)
    history_output = work_dir / "gpu1_native_tool_chat_loop" / (
        f"gpu1_chat_history_revision_{revision:03d}_subturn_{subturn:02d}.json"
    )
    item = _clone_subturn_item(primary_item, subturn)
    prepared.append(item)
    item["gpu1_tool_loop_subturn"] = subturn
    item["spec"] = deepcopy(base_spec)
    item["spec"]["output"] = output_path
    item["command"] = _subturn_command(
        base_command,
        output_path=output_path,
        history_path=history_path,
        history_output=history_output,
        subturn=subturn,
        disable_tools=True,
    )
    start_provider_item(gate, item, round_id, revision)
    write_provider_launch_manifest(
        gate,
        launch_manifest,
        prepared,
        round_id,
        revision,
        time_contract,
        "gpu1_native_tool_chat_soft_stop_finalization_started",
    )
    collect_provider_processes(
        gate,
        [item],
        timeout_seconds,
        round_id,
        revision,
        on_completed=absorb,
    )
    if item.get("completed") is not None:
        absorb(item)
    report = item.get("provider_report") if isinstance(item.get("provider_report"), dict) else {}
    _append_assistant_message(gate, history_path, report)
    calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
    _persist_loop_state(gate, report, history_path, closed=not bool(calls), subturn=subturn)
    if calls:
        gate.errors.append("gpu1_native_tool_loop_soft_stop_still_requested_tool")
    return item


def _append_soft_stop_message(
    history_path: Path,
    subturn: int,
    passed_request_ids: list[str],
    failed_request_ids: list[str],
) -> None:
    history = _read_history(history_path)
    ids = [item for item in passed_request_ids if item]
    failed = [item for item in failed_request_ids if item]
    joined = "\n".join(f"- {item}" for item in ids) or "- <no passed broker result ids>"
    failed_joined = "\n".join(f"- {item}" for item in failed) or "- none"
    history.append(
        {
            "role": "user",
            "content": (
                "GPU1_TOOL_LOOP_SOFT_STOP_FINALIZE.\n"
                f"Tool subturn budget reached: {subturn}.\n"
                "This is not context truncation: the full prompt, pointer context, "
                "runtime universe refs and role=tool results remain in this chat history.\n"
                "This finalization subturn has no tools in the API payload. "
                "Do not print tool JSON and do not request another tool.\n"
                "Do not answer with a meta-status such as 'tool execution completed' or "
                "'review the reports'. The delta must contain concrete findings from the "
                "tool outputs: tool names, file paths/read windows, discovered runtime facts, "
                "and the next operator-relevant correction.\n"
                "Write the assistant FINAL_PRODUCT_DELTA now using the consumed broker results.\n"
                "Passed broker request_id values allowed as product evidence:\n"
                f"{joined}\n"
                "Failed tool results are diagnostic only; do not put failed ids in CONSUMED_EVIDENCE:\n"
                f"{failed_joined}\n"
                "Required format:\n"
                "FINAL_PRODUCT_KIND: text\n"
                "FINAL_PRODUCT_ACTION: append\n"
                "CURRENT_POINTER:\n"
                f"- previous_block_id={ids[-1] if ids else f'subturn{subturn}'}\n"
                "- refines_block_id=\n"
                f"- resume_from_block_id=subturn{subturn}\n"
                "CONSUMED_EVIDENCE:\n"
                f"{joined}\n"
                "NEXT_RUNTIME_INTENT:\n"
                "- close_gpu1_tool_loop_after_soft_stop\n"
                "DIAGNOSTIC_TOOL_FAILURES:\n"
                f"{failed_joined}\n"
                "FINAL_PRODUCT_DELTA:\n"
                "Write the actual operator-facing product now, grounded in concrete tool facts.\n"
            ),
        }
    )
    write_json_report(history, history_path)


def _subturn_output_path(work_dir: Path, revision: int, subturn: int) -> Path:
    suffix = f"_revision{revision}" if revision else ""
    if subturn == 0:
        return work_dir / f"gpu1_ollama_provider_probe{suffix}.json"
    return work_dir / f"gpu1_ollama_provider_probe{suffix}_tool_subturn{subturn:02d}.json"


def _subturn_command(
    command: list[Any],
    *,
    output_path: Path,
    history_path: Path,
    history_output: Path,
    subturn: int,
    disable_tools: bool = False,
) -> list[str]:
    rewritten = _remove_option_value([str(part) for part in command], "--prompt")
    rewritten = _remove_option_value(rewritten, "--prompt-file")
    rewritten = _remove_option_value(rewritten, "--chat-history-file")
    rewritten = _remove_option_value(rewritten, "--chat-history-output")
    rewritten = _remove_option_value(rewritten, "--gpu1-tool-loop-subturn")
    rewritten = [part for part in rewritten if part != "--disable-native-chat-tools"]
    rewritten = _replace_option_value(rewritten, "--output", str(output_path))
    rewritten.extend(
        [
            "--chat-history-file",
            str(history_path),
            "--chat-history-output",
            str(history_output),
            "--gpu1-tool-loop-subturn",
            str(subturn),
        ]
    )
    if disable_tools:
        rewritten.append("--disable-native-chat-tools")
    return rewritten


def _remove_option_value(command: list[str], option: str) -> list[str]:
    out: list[str] = []
    skip_next = False
    for index, item in enumerate(command):
        if skip_next:
            skip_next = False
            continue
        if item == option:
            skip_next = index + 1 < len(command)
            continue
        out.append(item)
    return out


def _replace_option_value(command: list[str], option: str, value: str) -> list[str]:
    out = list(command)
    if option in out:
        index = out.index(option)
        if index + 1 < len(out):
            out[index + 1] = value
            return out
    out.extend([option, value])
    return out


def _append_assistant_message(gate: Any, history_path: Path, report: dict[str, Any]) -> None:
    history = _read_history(history_path)
    message = report.get("assistant_message") if isinstance(report.get("assistant_message"), dict) else {}
    calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
    if not message:
        message = {"role": "assistant", "content": gate.provider_report_response_text(report)}
    out = {key: value for key, value in message.items() if key in {"role", "content", "tool_calls"}}
    if calls and not out.get("tool_calls"):
        out["tool_calls"] = calls
    if calls or out.get("tool_calls"):
        out["content"] = ""
    history.append(out)
    write_json_report(history, history_path)


def _append_tool_result_messages(
    gate: Any,
    history_path: Path,
    results: list[dict[str, Any]],
    request_links: list[dict[str, str]],
) -> None:
    history = _read_history(history_path)
    by_id = {str(item.get("request_id") or ""): item for item in results}
    for link in request_links:
        request_id = str(link.get("request_id") or "")
        tool_call_id = str(link.get("tool_call_id") or request_id)
        result = by_id.get(request_id)
        if not result:
            continue
        history.append(
            {
                "role": "tool",
                "tool_name": str(result.get("tool") or ""),
                "content": json.dumps(
                    {
                        **_tool_result_message_payload(gate, result),
                        "tool_call_id": tool_call_id,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                    default=str,
                ),
            }
        )
    write_json_report(history, history_path)


def _tool_result_message_payload(gate: Any, result: dict[str, Any]) -> dict[str, Any]:
    return gpu1_tool_result_payload(gate.repo_root, result)


def _expected_request_links(gate: Any, report: dict[str, Any]) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
    for index, call in enumerate(calls, start=1):
        tool = str(call.get("tool") or "").strip()
        call_id = str(call.get("id") or f"{tool}_{index:03d}").strip()
        if tool and call_id:
            links.append(
                {
                    "request_id": provider_native_tool_request_id(
                        str(gate.stamp),
                        report,
                        call,
                        tool=tool,
                        call_index=index,
                    ),
                    "tool_call_id": call_id,
                    "tool": tool,
                }
            )
    return links


def _matching_broker_results(gate: Any, request_ids: list[str]) -> list[dict[str, Any]]:
    wanted = set(request_ids)
    return [
        payload
        for payload in gate.broker_results(gate.read_events())
        if str(payload.get("request_id") or "") in wanted
        or str(payload.get("normalized_request_id") or "") in wanted
    ]


def _persist_loop_state(
    gate: Any,
    report: dict[str, Any],
    history_path: Path,
    *,
    closed: bool,
    subturn: int,
) -> None:
    if not report:
        return
    output_ref = str(report.get("output") or "")
    if not output_ref:
        return
    output_path = Path(output_ref)
    if not output_path.is_absolute():
        output_path = gate.repo_root / output_path
    persisted = read_json(output_path)
    persisted.update(
        {
            "gpu1_native_tool_chat_loop": True,
            "gpu1_tool_loop_subturn": subturn,
            "gpu1_tool_loop_closed": closed,
            "gpu1_waiting_for_tool_result": not closed,
            "chat_history_ref": artifact_ref(
                history_path,
                gate.repo_root,
                kind="gpu1_native_tool_chat_history",
                producer="gpu1_native_tool_chat_loop",
            ),
        }
    )
    write_json_report(persisted, output_path)
    report.update(persisted)


def _read_history(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return []
    return payload if isinstance(payload, list) else []
