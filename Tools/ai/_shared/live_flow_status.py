"""Status rendering helpers for live operator flow monitoring."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def collect_flow_status(run_dir: Path | None) -> dict[str, Any]:
    if not run_dir:
        return {}
    root = Path(run_dir)
    events_path = root / "events.jsonl"
    event_counts, last_event, event_providers = _event_summary(events_path)
    child_flow = _child_flow_status(root)
    provider_dir = root / "provider_teamwork"
    providers = _merge_provider_statuses(event_providers, _provider_status(provider_dir))
    proposal_dir = root / "team_context" / "proposal_iterations"
    proposal_count = len(list(proposal_dir.glob("*.json"))) if proposal_dir.exists() else 0
    return {
        "run_dir": str(root),
        "phase_hint": _phase_hint(root, event_counts, providers, proposal_count),
        "events_count": sum(event_counts.values()),
        "event_type_counts": event_counts,
        "last_event_type": last_event.get("event_type", ""),
        "last_event_source": last_event.get("source", ""),
        "child_phase": child_flow.get("phase", ""),
        "child_status": child_flow.get("status", ""),
        "child_elapsed_seconds": child_flow.get("elapsed_seconds", ""),
        "broker_request_count": event_counts.get("broker_request", 0),
        "broker_result_count": event_counts.get("broker_result", 0),
        "provider_peer_block_count": event_counts.get("provider_peer_block", 0),
        "provider_lane_statuses": providers,
        "proposal_iteration_count": proposal_count,
        "heap_report_exists": (root / "heap_runtime_completeness_gate_report.json").exists(),
        "launcher_summary_exists": (root / "heap_runtime_context_closure_launcher.json").exists(),
    }


def render_flow_markdown(payload: dict[str, Any]) -> str:
    run_status = payload.get("run_status") if isinstance(payload.get("run_status"), dict) else {}
    lines = [
        "# Operator Live Flow",
        "",
        f"- Phase: `{payload.get('phase')}`",
        f"- Status: `{payload.get('status')}`",
        f"- PID: `{payload.get('pid')}`",
        f"- Elapsed seconds: `{payload.get('elapsed_seconds')}`",
        f"- CRLF warnings compressed: `{payload.get('crlf_warning_count')}`",
        f"- Phase hint: `{run_status.get('phase_hint', '')}`",
        f"- Child phase: `{run_status.get('child_phase', '')}`",
        f"- Child status: `{run_status.get('child_status', '')}`",
        f"- Events: `{run_status.get('events_count', 0)}`",
        f"- Broker results: `{run_status.get('broker_result_count', 0)}`",
        f"- Provider blocks: `{run_status.get('provider_peer_block_count', 0)}`",
        f"- Proposal iterations: `{run_status.get('proposal_iteration_count', 0)}`",
        "",
        "## Provider Lanes",
        "",
    ]
    for lane in run_status.get("provider_lane_statuses") or []:
        lines.append(
            "- `{lane}` status=`{status}` passed=`{passed}` semantic=`{semantic}` "
            "model=`{model}` output=`{output}`".format(
                lane=lane.get("lane", ""),
                status=lane.get("status", ""),
                passed=lane.get("passed", ""),
                semantic=lane.get("semantic_provider_execution_performed", ""),
                model=lane.get("selected_model", ""),
                output=lane.get("output", ""),
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def render_console_line(payload: dict[str, Any]) -> str:
    run_status = payload.get("run_status") if isinstance(payload.get("run_status"), dict) else {}
    providers = run_status.get("provider_lane_statuses") or []
    lanes = ",".join(_lane_details(item) for item in providers[:4] if item.get("lane"))
    return (
        "[flow] phase={phase} status={status} elapsed={elapsed}s "
        "child={child} step={step} hint={hint} last={last} events={events} "
        "event_mix={event_mix} broker=req:{broker_req}/res:{broker_res} provider_blocks={blocks} "
        "proposals={proposals} lanes={lanes} crlf_warnings={crlf}"
    ).format(
        phase=payload.get("phase"),
        status=payload.get("status"),
        elapsed=payload.get("elapsed_seconds"),
        child=_child_label(run_status),
        step=_human_step(run_status, providers),
        hint=run_status.get("phase_hint", ""),
        last=_last_event_label(run_status),
        events=run_status.get("events_count", 0),
        event_mix=_event_mix(run_status.get("event_type_counts") or {}),
        broker_req=run_status.get("broker_request_count", 0),
        broker_res=run_status.get("broker_result_count", 0),
        blocks=run_status.get("provider_peer_block_count", 0),
        proposals=run_status.get("proposal_iteration_count", 0),
        lanes=lanes or "-",
        crlf=payload.get("crlf_warning_count", 0),
    )


def _human_step(run_status: dict[str, Any], providers: list[dict[str, Any]]) -> str:
    active = [
        str(item.get("lane"))
        for item in providers
        if str(item.get("status") or "").strip() in {"running", "partial"}
    ]
    if active:
        return "providers-active:" + ",".join(active)
    if run_status.get("proposal_iteration_count", 0):
        return "proposal-materialized"
    if providers:
        return "provider-artifacts-present"
    if run_status.get("broker_result_count", 0) or run_status.get("broker_request_count", 0):
        return "broker/evidence-loop"
    hint = str(run_status.get("phase_hint") or "").strip()
    if hint == "preflight_done":
        return "preflight-complete"
    if hint == "startup_reload_done":
        return "startup-reload-complete"
    return "boot"


def _last_event_label(run_status: dict[str, Any]) -> str:
    event_type = str(run_status.get("last_event_type") or "").strip()
    source = str(run_status.get("last_event_source") or "").strip()
    if not event_type and not source:
        return "-"
    return f"{event_type or '?'}/{source or '?'}"


def _event_mix(counts: dict[str, int]) -> str:
    items = [(key, value) for key, value in counts.items() if value]
    if not items:
        return "-"
    items.sort(key=lambda item: (-item[1], item[0]))
    return ",".join(f"{key}:{value}" for key, value in items[:6])


def _lane_details(item: dict[str, Any]) -> str:
    lane = str(item.get("lane") or "")
    parts = [str(item.get("status") or item.get("passed") or "?")]
    for label, key in (
        ("role", "role"),
        ("model", "selected_model"),
        ("t", "elapsed_seconds"),
        ("pid", "pid"),
        ("partial", "partial_response_chars"),
        ("done", "done"),
        ("semantic", "semantic_provider_execution_performed"),
        ("op", "operational_provider_activity"),
        ("native", "native_tool_call_count"),
        ("class", "native_tool_loop_classification"),
    ):
        value = item.get(key)
        if value not in ("", None):
            parts.append(f"{label}={_compact(value)}")
    output = str(item.get("output") or "").replace("\\", "/").rsplit("/", 1)[-1]
    if output:
        parts.append(f"out={output}")
    return f"{lane}[{','.join(parts)}]"


def _compact(value: Any, limit: int = 32) -> str:
    text = str(value).replace(",", "~").replace(" ", "_")
    if len(text) <= limit:
        return text
    return text[: max(1, limit - 1)] + "~"


def _event_summary(path: Path) -> tuple[dict[str, int], dict[str, Any], list[dict[str, Any]]]:
    counts: dict[str, int] = {}
    last: dict[str, Any] = {}
    providers: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return counts, last, []
    try:
        with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
            for line in handle:
                _read_event_line(line, counts, providers)
                if line.strip():
                    try:
                        last = json.loads(line)
                    except Exception:
                        pass
    except Exception:
        return counts, last, list(providers.values())
    return counts, last, list(providers.values())


def _read_event_line(
    line: str, counts: dict[str, int], providers: dict[str, dict[str, Any]]
) -> None:
    try:
        event = json.loads(line)
    except Exception:
        return
    if not isinstance(event, dict):
        return
    key = str(event.get("event_type") or event.get("kind") or "unknown")
    counts[key] = counts.get(key, 0) + 1
    if key != "provider_state":
        return
    payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
    pending = payload.get("pending_lanes")
    if isinstance(pending, list):
        for item in pending:
            if isinstance(item, dict):
                _merge_provider_event(providers, item)
            elif isinstance(item, str) and item.strip():
                _merge_provider_event(providers, {"lane": item.strip(), "status": "running"})
    source = str(event.get("source") or "").strip()
    known_source = source in {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}
    lane = str(payload.get("lane") or (source if known_source else "")).strip()
    if not lane:
        return
    _merge_provider_event(providers, payload | {"lane": lane})


def _merge_provider_event(providers: dict[str, dict[str, Any]], payload: dict[str, Any]) -> None:
    lane = str(payload.get("lane") or "").strip()
    if not lane:
        return
    current = providers.get(lane, {})
    current.update(
        {
            "lane": lane,
            "role": payload.get("role") or current.get("role"),
            "status": payload.get("status") or current.get("status"),
            "pid": payload.get("pid") or current.get("pid"),
            "started_at": payload.get("started_at") or current.get("started_at"),
            "elapsed_seconds": payload.get("elapsed_seconds") or current.get("elapsed_seconds"),
            "timeout_seconds": payload.get("timeout_seconds") or current.get("timeout_seconds"),
            "output": payload.get("output") or current.get("output"),
            "selected_model": payload.get("selected_model") or payload.get("model") or current.get("selected_model"),
            "partial_response_chars": payload.get("partial_response_chars") or current.get("partial_response_chars"),
            "done": payload.get("done") if payload.get("done") is not None else current.get("done"),
            "semantic_provider_execution_performed": payload.get("semantic_provider_execution_performed") if payload.get("semantic_provider_execution_performed") is not None else current.get("semantic_provider_execution_performed"),
            "operational_provider_activity": payload.get("operational_provider_activity") if payload.get("operational_provider_activity") is not None else current.get("operational_provider_activity"),
            "native_tool_call_count": payload.get("native_tool_call_count") if payload.get("native_tool_call_count") is not None else current.get("native_tool_call_count"),
            "native_tool_loop_classification": payload.get("native_tool_loop_classification") or payload.get("classification") or current.get("native_tool_loop_classification"),
            "source": "heap_event",
        }
    )
    providers[lane] = current


def _child_flow_status(root: Path) -> dict[str, Any]:
    path = root / "heap_context_closure_live_flow.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig", errors="replace"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _child_label(run_status: dict[str, Any]) -> str:
    phase = str(run_status.get("child_phase") or "").strip()
    status = str(run_status.get("child_status") or "").strip()
    elapsed = run_status.get("child_elapsed_seconds")
    if not phase and not status:
        return "-"
    suffix = f":{elapsed}s" if elapsed not in ("", None) else ""
    return f"{phase or '?'}:{status or '?'}{suffix}"


def _provider_status(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    result: list[dict[str, Any]] = []
    for item in sorted(path.glob("*.json")):
        if item.name.startswith(("provider_launch_manifest", "provider_teamwork_leader_packet")):
            continue
        try:
            data = json.loads(item.read_text(encoding="utf-8-sig", errors="replace"))
        except Exception:
            data = {}
        if not isinstance(data, dict):
            data = {}
        result.append(
            {
                "lane": data.get("lane") or _lane_from_name(item.name),
                "status": data.get("status") or ("written" if data else "pending"),
                "passed": data.get("passed"),
                "role": data.get("role"),
                "selected_model": data.get("selected_model") or data.get("model"),
                "elapsed_seconds": data.get("elapsed_seconds") or data.get("elapsed_sec"),
                "partial_response_chars": data.get("partial_response_chars"),
                "done": data.get("done"),
                "semantic_provider_execution_performed": data.get("semantic_provider_execution_performed"),
                "operational_provider_activity": data.get("operational_provider_activity"),
                "native_tool_call_count": data.get("native_tool_call_count"),
                "native_tool_loop_classification": data.get("native_tool_loop_classification"),
                "output": str(item),
            }
        )
    return result


def _merge_provider_statuses(
    event_statuses: list[dict[str, Any]], file_statuses: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for item in event_statuses:
        lane = str(item.get("lane") or "").strip()
        if lane:
            merged[lane] = dict(item)
    for item in file_statuses:
        lane = str(item.get("lane") or "").strip()
        if not lane:
            continue
        current = merged.get(lane, {})
        current.update({key: value for key, value in item.items() if value not in ("", None)})
        current["source"] = "heap_event+artifact" if lane in merged else "artifact"
        merged[lane] = current
    return [merged[key] for key in sorted(merged)]


def _lane_from_name(name: str) -> str:
    if name.startswith("gpu1_"):
        return "gpu1_planner"
    if name.startswith("gpu0_"):
        return "gpu0_peer"
    if name.startswith("npu_"):
        return "npu_micro_task_auditor"
    return name.rsplit(".", 1)[0]


def _phase_hint(
    root: Path,
    event_counts: dict[str, int],
    providers: list[dict[str, Any]],
    proposal_count: int,
) -> str:
    if (root / "heap_runtime_context_closure_launcher.json").exists():
        return "launcher_summary_written"
    if (root / "heap_runtime_completeness_gate_report.json").exists():
        return "heap_gate_report_written"
    if proposal_count:
        return "proposal_iterations_materialized"
    if providers:
        return "provider_lanes_running_or_written"
    if event_counts:
        return "heap_event_loop_active"
    if (root / "startup_context_memory_reload" / "heap_context_memory_reload_manifest.json").exists():
        return "startup_reload_done"
    if (root / "heap_context_preflight_gate.json").exists():
        return "preflight_done"
    return "starting"
