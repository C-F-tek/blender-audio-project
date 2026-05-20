"""Status rendering helpers for live operator flow monitoring."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from Tools.ai._shared.live_flow_lanes import (
    lane_details,
    merge_provider_statuses,
    provider_status,
    support_provider_payload,
)


def collect_flow_status(run_dir: Path | None) -> dict[str, Any]:
    if not run_dir:
        return {}
    root = Path(run_dir)
    events_path = root / "events.jsonl"
    event_counts, last_event, event_providers = _event_summary(events_path)
    child_flow = _child_flow_status(root)
    provider_dir = root / "provider_teamwork"
    providers = merge_provider_statuses(event_providers, provider_status(provider_dir))
    proposal_dir = root / "team_context" / "proposal_iterations"
    proposal_count = len(list(proposal_dir.glob("*.json"))) if proposal_dir.exists() else 0
    preflight = _preflight_status(root)
    return {
        "run_dir": str(root),
        "phase_hint": _phase_hint(root, event_counts, providers, proposal_count, preflight),
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
        "preflight": preflight,
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
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_console_line(payload: dict[str, Any]) -> str:
    run_status = payload.get("run_status") if isinstance(payload.get("run_status"), dict) else {}
    return (
        "[flow] phase={phase} status={status} elapsed={elapsed}s "
        "child={child} step={step} hint={hint} last={last} "
        "events={events} event_mix={event_mix} broker=req:{broker_req}/res:{broker_res} "
        "provider_blocks={blocks} proposals={proposals} lanes={lanes} crlf_warnings={crlf}"
    ).format(
        phase=payload.get("phase"),
        status=payload.get("status"),
        elapsed=payload.get("elapsed_seconds"),
        child=_child_label(run_status),
        step=_human_step(run_status),
        hint=run_status.get("phase_hint", ""),
        last=_last_event_label(run_status),
        events=run_status.get("events_count", 0),
        event_mix=_event_mix_label(run_status),
        broker_req=run_status.get("broker_request_count", 0),
        broker_res=run_status.get("broker_result_count", 0),
        blocks=run_status.get("provider_peer_block_count", 0),
        proposals=run_status.get("proposal_iteration_count", 0),
        lanes=lane_details(run_status),
        crlf=payload.get("crlf_warning_count", 0),
    )


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
            if not isinstance(item, dict):
                continue
            lane = str(item.get("lane") or "").strip()
            if not lane or support_provider_payload(lane, item):
                continue
            current = providers.get(lane, {})
            current.update(
                {
                    "lane": lane,
                    "status": payload.get("status") or current.get("status") or "running",
                    "pid": item.get("pid") or current.get("pid"),
                    "elapsed_seconds": item.get("elapsed_seconds")
                    or current.get("elapsed_seconds"),
                    "timeout_seconds": item.get("timeout_seconds")
                    or current.get("timeout_seconds"),
                    "budget_counter_seconds": item.get("budget_counter_seconds")
                    or current.get("budget_counter_seconds"),
                    "soft_close_after_seconds": item.get("soft_close_after_seconds")
                    or current.get("soft_close_after_seconds"),
                    "watchdog_timeout_seconds": item.get("watchdog_timeout_seconds")
                    or current.get("watchdog_timeout_seconds"),
                    "output": item.get("output") or current.get("output"),
                    "source": "provider_heartbeat",
                }
            )
            providers[lane] = current
        return
    lane = str(payload.get("lane") or "").strip()
    if not lane or support_provider_payload(lane, payload):
        return
    current = providers.get(lane, {})
    current.update(
        {
            "lane": lane,
            "status": payload.get("status") or current.get("status"),
            "pid": payload.get("pid") or current.get("pid"),
            "started_at": payload.get("started_at") or current.get("started_at"),
            "elapsed_seconds": payload.get("elapsed_seconds") or current.get("elapsed_seconds"),
            "timeout_seconds": payload.get("timeout_seconds") or current.get("timeout_seconds"),
            "budget_counter_seconds": payload.get("budget_counter_seconds")
            or current.get("budget_counter_seconds"),
            "soft_close_after_seconds": payload.get("soft_close_after_seconds")
            or current.get("soft_close_after_seconds"),
            "watchdog_timeout_seconds": payload.get("watchdog_timeout_seconds")
            or current.get("watchdog_timeout_seconds"),
            "output": payload.get("output") or current.get("output"),
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


def _human_step(run_status: dict[str, Any]) -> str:
    hint = str(run_status.get("phase_hint") or "")
    preflight = run_status.get("preflight") if isinstance(run_status.get("preflight"), dict) else {}
    providers = run_status.get("provider_lane_statuses") or []
    if hint == "starting":
        return "boot"
    if hint == "preflight_running":
        return "preflight:{0}:{1}/{2}".format(
            preflight.get("current_step") or "?",
            preflight.get("completed_step_count", 0),
            preflight.get("step_count", 0),
        )
    if hint == "preflight_done":
        return "preflight-complete"
    if hint == "startup_reload_done":
        return "startup-memory-loaded"
    if hint == "heap_event_loop_active":
        return "broker/evidence-loop"
    if hint == "provider_lanes_running_or_written":
        running = [str(item.get("lane")) for item in providers if item.get("status") == "running"]
        degraded = [str(item.get("lane")) for item in providers if item.get("status") == "degraded"]
        if running:
            return "providers-active:" + ",".join(running[:3])
        if degraded:
            return "providers-degraded:" + ",".join(degraded[:3])
        return "provider-artifacts-present"
    if hint == "proposal_iterations_materialized":
        return "proposal-materialized"
    if hint == "heap_gate_report_written":
        return "heap-report-written"
    if hint == "launcher_summary_written":
        return "launcher-summary-written"
    return hint or "-"


def _last_event_label(run_status: dict[str, Any]) -> str:
    event_type = str(run_status.get("last_event_type") or "").strip()
    source = str(run_status.get("last_event_source") or "").strip()
    if not event_type:
        return "-"
    return f"{event_type}/{source or '?'}"


def _event_mix_label(run_status: dict[str, Any]) -> str:
    counts = run_status.get("event_type_counts")
    if not isinstance(counts, dict) or not counts:
        return "-"
    priority = [
        "need",
        "broker_request",
        "broker_result",
        "provider_state",
        "provider_peer_block",
        "claim",
        "validation_signal",
        "provider_evidence",
        "fact",
    ]
    parts = []
    for key in priority:
        value = counts.get(key)
        if value:
            parts.append(f"{key}:{value}")
    return ",".join(parts[:7]) or "-"


def _preflight_status(root: Path) -> dict[str, Any]:
    path = root / "heap_context_preflight_gate.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig", errors="replace"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    return dict(
        status=data.get("status") or ("completed" if data.get("steps") else ""),
        current_step=data.get("current_step") or "",
        step_index=data.get("step_index"),
        step_count=data.get("step_count"),
        completed_step_count=data.get("completed_step_count") or len(data.get("steps") or []),
        failed_step_count=len(data.get("failed_steps") or []),
    )


def _phase_hint(
    root: Path,
    event_counts: dict[str, int],
    providers: list[dict[str, Any]],
    proposal_count: int,
    preflight: dict[str, Any],
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
    if preflight:
        if preflight.get("status") != "completed":
            return "preflight_running"
        return "preflight_done"
    return "starting"
