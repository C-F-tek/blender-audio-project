"""Build structured workflow debug reports."""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import workflow_core as wf
except ImportError:
    from Tools.workflow import workflow_core as wf

from .status import (
    detect_active_operation,
    expected_paths_for_operation,
    iso_to_dt,
    path_check,
    read_events,
    read_json,
    tail_non_empty,
    write_probe,
    format_age,
)


def collect_processes() -> list[dict]:
    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if not powershell:
        return []
    script = (
        "Get-Process | Where-Object { $_.ProcessName -match 'python|ollama|openvino|ffmpeg|blender' } | "
        "Select-Object ProcessName,Id,CPU,WorkingSet64,@{Name='StartTime';Expression={$_.StartTime.ToString('yyyy-MM-dd HH:mm:ss')}},Path | "
        "Sort-Object WorkingSet64 -Descending | ConvertTo-Json -Compress -Depth 3"
    )
    try:
        result = subprocess.run(
            [powershell, "-NoProfile", "-Command", script],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=6,
        )
    except Exception:
        return []
    output = (result.stdout or "").strip()
    if not output:
        return []
    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        return []
    if isinstance(payload, dict):
        payload = [payload]
    return [item for item in payload if isinstance(item, dict)] if isinstance(payload, list) else []


def collect_write_checks(probe_write: bool = True) -> list[dict]:
    targets = [
        ("Project root", wf.PROJECT_DIR),
        ("Output dir", wf.OUTPUT_DIR),
        ("Workflow log dir", wf.LOG_DIR),
        ("NPU tools dir", wf.NPU_DIR),
        ("Renders dir", wf.RENDERS_DIR),
    ]
    checks: list[dict] = []
    for label, path in targets:
        base = path_check(label, path, required=True, expect="dir")
        base["write_probe"] = ""
        if probe_write:
            ok, message = write_probe(Path(path))
            base["writable"] = ok
            base["write_probe"] = message
            if not ok:
                base["status"] = "WARN" if base["status"] == "OK" else base["status"]
                base["message"] = message
        checks.append(base)
    return checks


def active_compute_processes(processes: list[dict], operation: str) -> list[dict]:
    heavy_ops = {"analyze_wav", "build_manual_context", "dual_ai_plan", "dual_ai_implementation", "full_audio_prepare"}
    if operation not in heavy_ops:
        return []
    active: list[dict] = []
    for item in processes:
        name = str(item.get("ProcessName") or "").lower()
        ram = int(item.get("WorkingSet64") or 0)
        path = str(item.get("Path") or "").lower()
        if "ollama app" in name:
            continue
        if name.startswith("python") and ram > 200 * 1024 * 1024:
            active.append(item)
        elif name.startswith("ollama") and ram > 200 * 1024 * 1024:
            active.append(item)
        elif "ffmpeg" in name or "blender" in name:
            active.append(item)
        elif "openvino" in name or "openvino" in path:
            active.append(item)
    return active


def build_debug_report(probe_write: bool = True) -> dict:
    session = wf.load_session(create=True)
    events = read_events()
    active = detect_active_operation(events)
    operation = active["operation"] or session.last_operation or "-"
    expected = expected_paths_for_operation(session, operation)

    common_checks = [path_check(label, path, required=True, expect=expect) for label, path, expect in expected["common_inputs"]]
    input_checks = [path_check(label, path, required=True, expect=expect) for label, path, expect in expected["operation_inputs"]]
    output_checks = [path_check(label, path, required=False, expect=expect) for label, path, expect in expected["operation_outputs"]]
    progress_checks = [path_check(label, path, required=False, expect=expect) for label, path, expect in expected["progress_files"]]

    start_dt = iso_to_dt(active.get("started_at"))
    latest_write = _annotate_latest_write(output_checks + progress_checks, start_dt)
    warnings = _build_warnings(active, input_checks, latest_write)
    progress_previews = [
        {"label": label, "path": str(path), "tail": tail_non_empty(Path(path))}
        for label, path, _expect in expected["progress_files"]
    ]

    processes = collect_processes()
    compute_processes = active_compute_processes(processes, operation)
    active_status = "active" if active.get("active") else "none"
    if active.get("active") and active.get("elapsed_sec") and active["elapsed_sec"] > 120 and not compute_processes:
        active_status = "stale_or_interrupted"
        warnings.append(
            "Log has a start event without a result, but no heavy Python/Ollama/Blender/FFmpeg process is running."
        )

    return {
        "generated_at": wf.now_iso(),
        "session": {
            "path": str(wf.SESSION_PATH),
            "track_stem": session.track_stem,
            "audio_path": session.artifacts.get("audio_path"),
            "debug_enabled": session.debug_enabled,
            "last_operation": session.last_operation,
        },
        "active_operation": active,
        "active_status": active_status,
        "operation_for_checks": operation,
        "last_result": read_json(wf.LAST_RESULT_PATH),
        "common_checks": common_checks,
        "input_checks": input_checks,
        "output_checks": output_checks,
        "progress_checks": progress_checks,
        "write_checks": collect_write_checks(probe_write=probe_write),
        "progress_previews": progress_previews,
        "processes": processes,
        "active_compute_processes": compute_processes,
        "recent_events": events[-8:],
        "warnings": warnings,
    }


def _annotate_latest_write(watched: list[dict], start_dt: datetime | None) -> dict | None:
    latest_write: dict | None = None
    for item in watched:
        item_dt = iso_to_dt(item.get("mtime"))
        if not item_dt:
            continue
        if start_dt and item_dt < start_dt:
            item["message"] = "old file from before active operation"
        if latest_write is None or str(item.get("mtime", "")) > str(latest_write.get("mtime", "")):
            latest_write = item
    return latest_write


def _build_warnings(active: dict, input_checks: list[dict], latest_write: dict | None) -> list[str]:
    warnings: list[str] = []
    if active["active"] and latest_write:
        latest_dt = iso_to_dt(latest_write.get("mtime"))
        if latest_dt:
            idle = (datetime.now() - latest_dt).total_seconds()
            if idle > 600:
                warnings.append(f"No watched output/progress file changed for {format_age(idle)}.")
    if active["active"] and not latest_write and active.get("elapsed_sec") and active["elapsed_sec"] > 300:
        warnings.append("Active operation has no watched output/progress files yet after 5m.")
    if any(item["status"] in {"MISSING", "WARN"} for item in input_checks):
        warnings.append("Some required input paths for the active operation are missing or suspicious.")
    return warnings
