from __future__ import annotations

from .common import *  # noqa: F403

def normalize_tool_result(
    *,
    caller: str,
    phase: str,
    round_id: int | None,
    broker_source: str,
    broker_path: str,
    request: dict[str, Any] | None,
    result: dict[str, Any],
) -> dict[str, Any]:
    request = request or {}
    tool_name = (
        result.get("tool")
        or result.get("tool_name")
        or request.get("tool")
        or request.get("tool_name")
        or result.get("name")
        or "unknown"
    )
    started = result.get("started_at") or result.get("start_time")
    finished = result.get("finished_at") or result.get("end_time")
    elapsed = (
        safe_float(result.get("elapsed_seconds"))
        or safe_float(result.get("duration_seconds"))
        or elapsed_from_timestamps(started, finished)
    )
    return normalize_tool_entry(
        {
            "caller_ai": caller,
            "phase": phase,
            "round": round_id,
            "broker_source": broker_source,
            "broker_report": broker_path,
            "tool_request_id": result.get("id") or result.get("request_id") or request.get("id"),
            "tool": tool_name,
            "reason": request.get("reason") or result.get("reason"),
            "requested_args": (
                request.get("args") if isinstance(request.get("args"), dict) else {}
            ),
            "status": result.get("status") or result.get("state"),
            "executed": result.get("executed"),
            "blocked": result.get("blocked"),
            "failed": result.get("failed"),
            "elapsed_seconds": elapsed,
            "started_at": started,
            "finished_at": finished,
            "result": summarize_result_output(result),
        }
    )

def requests_by_id(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    mapping: dict[str, dict[str, Any]] = {}
    for raw in safe_list(report.get("tool_requests")):
        if not isinstance(raw, dict):
            continue
        request_id = str(raw.get("id") or raw.get("request_id") or "")
        if request_id:
            mapping[request_id] = raw
    return mapping

def collect_from_broker_report(
    *,
    repo_root: Path,
    broker_report: dict[str, Any],
    broker_path: str,
    caller: str,
    phase: str,
    round_id: int | None,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    request_map = requests_by_id(broker_report)
    results = safe_list(broker_report.get("tool_results"))
    for index, raw_result in enumerate(results, start=1):
        if not isinstance(raw_result, dict):
            continue
        result_id = str(raw_result.get("id") or raw_result.get("request_id") or "")
        request = request_map.get(result_id) if result_id else None
        entries.append(
            normalize_tool_result(
                caller=caller,
                phase=phase,
                round_id=round_id,
                broker_source=str(
                    broker_report.get("source")
                    or broker_report.get("source_classification")
                    or broker_report.get("kind")
                    or phase
                ),
                broker_path=broker_path,
                request=request,
                result=raw_result,
            )
        )
    if (not entries) and (
        broker_report.get("tool_request_count") or broker_report.get("requested_tool_count")
    ):
        entries.append(
            normalize_tool_entry(
                {
                    "caller_ai": caller,
                    "phase": phase,
                    "round": round_id,
                    "broker_source": str(
                        broker_report.get("source") or broker_report.get("kind") or phase
                    ),
                    "broker_report": broker_path,
                    "tool_request_id": None,
                    "tool": "broker_summary_only",
                    "status": "summary_only",
                    "requested_args": {},
                    "elapsed_seconds": safe_float(broker_report.get("elapsed_seconds")),
                    "result": {
                        "passed": broker_report.get("passed"),
                        "tool_request_count": broker_report.get("tool_request_count")
                        or broker_report.get("requested_tool_count"),
                        "tool_execution_count": broker_report.get("tool_execution_count"),
                        "blocked_tool_count": broker_report.get("blocked_tool_count"),
                        "failed_tool_count": broker_report.get("failed_tool_count"),
                        "output_paths": [
                            path
                            for path in (
                                broker_report.get("broker_output"),
                                broker_report.get("broker_markdown"),
                            )
                            if path
                        ],
                    },
                }
            )
        )
    return entries

def collect_broker_pointer_entries(
    repo_root: Path, raw_items: Any, caller: str, phase: str
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for raw in safe_list(raw_items):
        if not isinstance(raw, dict):
            continue
        round_id = safe_int(raw.get("round"), -1)
        round_value = round_id if round_id >= 0 else None
        broker_report = safe_dict(raw.get("broker_report"))
        broker_path = str(raw.get("broker_output") or raw.get("broker_report") or "")
        if not broker_report and broker_path:
            broker_report = maybe_read_broker_report(repo_root, broker_path)
        if broker_report:
            entries.extend(
                collect_from_broker_report(
                    repo_root=repo_root,
                    broker_report=broker_report,
                    broker_path=broker_path,
                    caller=caller,
                    phase=phase,
                    round_id=round_value,
                )
            )
            continue
        entries.append(
            normalize_tool_entry(
                {
                    "caller_ai": caller,
                    "phase": phase,
                    "round": round_value,
                    "broker_source": str(raw.get("source") or phase),
                    "broker_report": broker_path,
                    "tool_request_id": None,
                    "tool": "broker_packet_summary",
                    "status": "summary_only",
                    "requested_args": {},
                    "elapsed_seconds": safe_float(raw.get("elapsed_seconds")),
                    "result": {
                        "passed": raw.get("passed"),
                        "tool_request_count": raw.get("tool_request_count")
                        or raw.get("requested_tool_count"),
                        "tool_execution_count": raw.get("tool_execution_count"),
                        "blocked_tool_count": raw.get("blocked_tool_count"),
                        "failed_tool_count": raw.get("failed_tool_count"),
                        "output_paths": [
                            path
                            for path in (
                                raw.get("broker_output"),
                                raw.get("broker_markdown"),
                                raw.get("request_file"),
                            )
                            if path
                        ],
                        "stdout_tail": compact_text(raw.get("stdout_tail"), 600),
                        "stderr_tail": compact_text(raw.get("stderr_tail"), 600),
                        "error": compact_text(raw.get("error"), 600),
                    },
                }
            )
        )
    return entries

def append_default_broker_report_if_present(repo_root: Path, stamp: str, values: Any) -> list[str]:
    # Preserve final broker telemetry even if a caller omits --broker-report.
    paths = split_path_values(values)
    if not stamp:
        return paths

    default_path = (
        repo_root / "output" / "validation" / f"runtime_tool_broker_full_toolbox_{stamp}.json"
    )
    if not default_path.exists():
        return paths

    default_rel = repo_rel(repo_root, default_path)
    normalized_existing = {
        repo_rel(repo_root, resolve_output_path(repo_root, item)) for item in paths if item
    }
    if default_rel not in normalized_existing:
        paths.append(default_rel)
    return paths

def classify_broker_caller_phase(
    broker_report: dict[str, Any],
    broker_path: str,
    default_caller: str,
    default_phase: str,
) -> tuple[str, str]:
    source = str(
        broker_report.get("source") or broker_report.get("source_classification") or ""
    ).lower()
    path_text = broker_path.lower()
    marker = f"{source} {path_text}"

    if "gpu0" in marker:
        return "gpu0", "gpu0_peer_runtime_tool_broker"
    if "npu" in marker:
        return "npu", "npu_micro_runtime_tool_broker"
    if "gpu1" in marker:
        return "gpu", "gpu1_runtime_tool_broker"
    if "gpu" in marker:
        return "gpu", "gpu_runtime_tool_broker"
    return default_caller, default_phase

def collect_explicit_broker_reports(
    repo_root: Path, values: Any
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    entries: list[dict[str, Any]] = []
    warnings: list[str] = []
    paths: list[str] = []
    for index, raw_path in enumerate(split_path_values(values), start=1):
        path = resolve_output_path(repo_root, raw_path)
        rel = repo_rel(repo_root, path)
        paths.append(rel)
        if not path.exists():
            warnings.append(f"optional broker report missing: {rel}")
            continue
        data, read_errors = read_json_object(path, missing_is_error=True)
        if read_errors:
            warnings.extend(f"{rel}: {err}" for err in read_errors)
            continue
        if not isinstance(data, dict):
            warnings.append(f"{rel}: broker report is not a JSON object")
            continue
        caller, phase = classify_broker_caller_phase(
            data,
            rel,
            "orchestrator",
            "explicit_runtime_tool_broker_bootstrap",
        )
        entries.extend(
            collect_from_broker_report(
                repo_root=repo_root,
                broker_report=data,
                broker_path=rel,
                caller=caller,
                phase=phase,
                round_id=index,
            )
        )
    return entries, warnings, paths

def collect_gpu_declared_requests(gpu_report: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for round_item in safe_list(gpu_report.get("rounds")):
        if not isinstance(round_item, dict):
            continue
        round_id = safe_int(round_item.get("round"), -1)
        parsed = safe_dict(round_item.get("parsed_response"))
        for index, request in enumerate(safe_list(parsed.get("tool_requests")), start=1):
            if not isinstance(request, dict):
                continue
            entries.append(
                normalize_tool_entry(
                    {
                        "caller_ai": "gpu",
                        "phase": "gpu_planner_declared_tool_requests",
                        "round": round_id if round_id >= 0 else None,
                        "broker_source": "gpu_planner_response",
                        "broker_report": "",
                        "tool_request_id": request.get("id")
                        or f"gpu_round_{round_id:03d}_declared_{index:03d}",
                        "tool": request.get("tool") or request.get("tool_name") or "unknown",
                        "reason": request.get("reason"),
                        "requested_args": (
                            request.get("args") if isinstance(request.get("args"), dict) else {}
                        ),
                        "status": "declared_not_necessarily_executed",
                        "executed": False,
                        "blocked": None,
                        "failed": None,
                        "elapsed_seconds": 0.0,
                        "result": {
                            "summary": "Declared by GPU planner; execution is represented by broker records when available."
                        },
                    }
                )
            )
    return entries

def collect_npu_declared_requests(orchestrator: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for audit in safe_list(orchestrator.get("npu_audits")):
        if not isinstance(audit, dict):
            continue
        round_id = safe_int(audit.get("round"), -1)
        for index, request in enumerate(safe_list(audit.get("npu_tool_requests")), start=1):
            if not isinstance(request, dict):
                continue
            entries.append(
                normalize_tool_entry(
                    {
                        "caller_ai": "npu",
                        "phase": "npu_auditor_declared_tool_requests",
                        "round": round_id if round_id >= 0 else None,
                        "broker_source": audit.get("audit_output"),
                        "broker_report": "",
                        "tool_request_id": request.get("id")
                        or f"npu_round_{round_id:03d}_declared_{index:03d}",
                        "tool": request.get("tool") or request.get("tool_name") or "unknown",
                        "reason": request.get("reason"),
                        "requested_args": (
                            request.get("args") if isinstance(request.get("args"), dict) else {}
                        ),
                        "status": "declared_not_necessarily_executed",
                        "executed": False,
                        "blocked": None,
                        "failed": None,
                        "elapsed_seconds": 0.0,
                        "result": {
                            "summary": "Declared by NPU auditor; execution is represented by broker records when available."
                        },
                    }
                )
            )
    return entries

def collect_npu_micro_support_broker_entries(
    repo_root: Path, orchestrator: dict[str, Any]
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for micro in safe_list(orchestrator.get("npu_micro_supports")):
        if not isinstance(micro, dict):
            continue
        round_id = safe_int(micro.get("round"), -1)
        brokers = [
            ("provider_micro", safe_dict(micro.get("npu_runtime_tool_broker"))),
            (
                "live_tool_seed",
                safe_dict(micro.get("npu_live_seed_runtime_tool_broker")),
            ),
        ]
        for broker_source, broker in brokers:
            if not broker:
                continue
            phase = (
                "npu_micro_runtime_tool_broker_live"
                if broker.get("executed_while_gpu1_active") is True
                else "npu_micro_runtime_tool_broker"
            )
            broker_entries = collect_from_broker_report(
                repo_root=repo_root,
                broker_report=broker,
                broker_path=str(broker.get("broker_output") or ""),
                caller="npu",
                phase=phase,
                round_id=round_id if round_id >= 0 else None,
            )
            for entry in broker_entries:
                entry["npu_micro_support_live"] = broker.get("executed_while_gpu1_active") is True
                entry["npu_micro_support_status"] = micro.get("status")
                entry["npu_micro_broker_source"] = broker_source
            entries.extend(broker_entries)
    return entries
