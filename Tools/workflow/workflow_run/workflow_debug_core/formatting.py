"""Format workflow debug reports for console display."""

from __future__ import annotations

from .status import format_age, format_size


def format_check(item: dict) -> str:
    size = format_size(item.get("size"))
    mtime = item.get("mtime") or "-"
    message = item.get("message") or item.get("write_probe") or ""
    suffix = f" | {message}" if message else ""
    return f"[{item.get('status', 'OK')}] {item.get('label')}: {item.get('path')} | {size} | {mtime}{suffix}"


def format_process(item: dict) -> str:
    name = item.get("ProcessName", "-")
    pid = item.get("Id", "-")
    cpu = item.get("CPU", "-")
    ram = format_size(int(item.get("WorkingSet64") or 0))
    start = item.get("StartTime", "-")
    path = item.get("Path") or ""
    return f"{name} pid={pid} cpu={cpu} ram={ram} start={start} {path}"


def format_debug_report(report: dict) -> str:
    active = report["active_operation"]
    session = report["session"]
    lines: list[str] = []
    lines.append("=" * 78)
    lines.append("SPAZIOTEMPO ADVANCED DEBUG CHECK")
    lines.append("=" * 78)
    lines.append(f"Generated: {report['generated_at']}")
    lines.append(f"Track:     {session['track_stem']}")
    lines.append(f"Audio:     {session['audio_path']}")
    lines.append(f"Debug:     {'ON' if session['debug_enabled'] else 'OFF'}")
    if active.get("active"):
        status = report.get("active_status", "active")
        if status == "stale_or_interrupted":
            lines.append(
                f"Active:    stale/interrupted log for {active.get('operation')} since {active.get('started_at')} "
                f"elapsed {format_age(active.get('elapsed_sec'))}"
            )
        else:
            lines.append(
                f"Active:    {active.get('operation')} since {active.get('started_at')} "
                f"elapsed {format_age(active.get('elapsed_sec'))}"
            )
    else:
        lines.append(
            f"Active:    no running operation detected, checks based on {report['operation_for_checks']}"
        )

    last = report.get("last_result") or {}
    if isinstance(last, dict) and last:
        lines.append(
            f"Last:      {last.get('operation')} ok={last.get('ok')} "
            f"ended={last.get('ended_at')} elapsed={last.get('elapsed_sec')}"
        )

    _append_warnings(lines, report)
    _append_checks(lines, "Write Checks", report["write_checks"])
    _append_checks(lines, "Common Paths", report["common_checks"])
    _append_checks(lines, "Inputs For Active Operation", report["input_checks"])
    _append_checks(lines, "Expected Outputs / Pending Files", report["output_checks"])
    _append_checks(lines, "Progress Files", report["progress_checks"])
    _append_progress(lines, report)
    _append_processes(lines, report)
    _append_recent_events(lines, report)
    return "\n".join(lines)


def _append_warnings(lines: list[str], report: dict) -> None:
    if not report["warnings"]:
        return
    lines.extend(["", "Warnings:"])
    for warning in report["warnings"]:
        lines.append(f"  - {warning}")


def _append_checks(lines: list[str], title: str, checks: list[dict]) -> None:
    if not checks:
        return
    lines.extend(["", f"{title}:"])
    for item in checks:
        lines.append("  " + format_check(item))


def _append_progress(lines: list[str], report: dict) -> None:
    if not report["progress_previews"]:
        return
    lines.extend(["", "Progress Preview:"])
    for preview in report["progress_previews"]:
        lines.append(f"  {preview['label']}: {preview['path']}")
        tail = preview.get("tail") or ["<empty or missing>"]
        for line in tail:
            lines.append(f"    {line[:240]}")


def _append_processes(lines: list[str], report: dict) -> None:
    lines.extend(["", "AI / Render Processes:"])
    processes = report.get("processes") or []
    if processes:
        for item in processes[:14]:
            lines.append("  " + format_process(item))
    else:
        lines.append("  <no process snapshot available>")


def _append_recent_events(lines: list[str], report: dict) -> None:
    lines.extend(["", "Recent Events:"])
    for event in report["recent_events"]:
        lines.append(f"  {event.get('time')} {event.get('operation')}::{event.get('event')}")
