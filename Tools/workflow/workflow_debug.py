from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import time

import workflow_state as wf


def _iso_to_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _format_age(seconds: float | None) -> str:
    if seconds is None:
        return "-"
    seconds = max(0, int(seconds))
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {sec}s"
    if minutes:
        return f"{minutes}m {sec}s"
    return f"{sec}s"


def _format_size(size: int | None) -> str:
    if size is None:
        return "-"
    value = float(size)
    for suffix in ["B", "KB", "MB", "GB"]:
        if value < 1024 or suffix == "GB":
            return f"{value:.1f} {suffix}" if suffix != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} GB"


def _read_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def read_events(max_events: int = 600) -> list[dict]:
    if not wf.EVENT_LOG_PATH.exists():
        return []
    events: list[dict] = []
    try:
        lines = wf.EVENT_LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []
    for line in lines[-max_events:]:
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append({"time": "", "operation": "log_parse", "event": "bad_json", "payload": {"raw": line[:500]}})
    return events


def detect_active_operation(events: list[dict]) -> dict:
    for index in range(len(events) - 1, -1, -1):
        event = events[index]
        if event.get("event") != "start":
            continue

        operation = str(event.get("operation") or "")
        start_time = str(event.get("time") or "")
        has_result = False
        for later in events[index + 1 :]:
            if later.get("operation") == operation and later.get("event") == "result":
                has_result = True
                break
        if has_result:
            continue

        start_dt = _iso_to_dt(start_time)
        elapsed = (datetime.now() - start_dt).total_seconds() if start_dt else None
        return {
            "active": True,
            "operation": operation,
            "started_at": start_time,
            "elapsed_sec": elapsed,
            "payload": event.get("payload") or {},
        }

    last_result = None
    for event in reversed(events):
        if event.get("event") == "result":
            last_result = event
            break

    return {
        "active": False,
        "operation": str(last_result.get("operation") if last_result else ""),
        "started_at": "",
        "elapsed_sec": None,
        "payload": last_result.get("payload") if last_result else {},
    }


def _tail_non_empty(path: Path, max_lines: int = 8) -> list[str]:
    if not path.exists() or not path.is_file():
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        return [f"<read failed: {exc}>"]
    return [line.strip() for line in lines if line.strip()][-max_lines:]


def _write_probe(directory: Path) -> tuple[bool, str]:
    if not directory.exists():
        return False, "directory missing"
    if not directory.is_dir():
        return False, "not a directory"
    probe = directory / f".workflow_debug_probe_{os.getpid()}.tmp"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True, "temp write ok"
    except Exception as exc:
        try:
            if probe.exists():
                probe.unlink()
        except Exception:
            pass
        return False, str(exc)


def path_check(label: str, path: Path | str, required: bool = True, expect: str = "any") -> dict:
    target = Path(path)
    exists = target.exists()
    is_file = target.is_file()
    is_dir = target.is_dir()
    info: dict = {
        "label": label,
        "path": str(target),
        "required": required,
        "expect": expect,
        "exists": exists,
        "readable": os.access(str(target), os.R_OK) if exists else False,
        "writable": os.access(str(target), os.W_OK) if exists else False,
        "size": None,
        "mtime": "",
        "status": "OK",
        "message": "",
    }

    if exists:
        try:
            stat = target.stat()
            info["size"] = int(stat.st_size) if is_file else None
            info["mtime"] = datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds")
        except Exception as exc:
            info["status"] = "WARN"
            info["message"] = f"stat failed: {exc}"

    if required and not exists:
        info["status"] = "MISSING"
        info["message"] = "required path missing"
    elif exists and expect == "file" and not is_file:
        info["status"] = "WARN"
        info["message"] = "expected file"
    elif exists and expect == "dir" and not is_dir:
        info["status"] = "WARN"
        info["message"] = "expected directory"
    elif not required and not exists:
        info["status"] = "PENDING"
        info["message"] = "not created yet"

    return info


def expected_paths_for_operation(session: wf.WorkflowSession, operation: str) -> dict:
    artifacts = session.artifacts
    script = lambda name: wf.PROJECT_DIR / name
    npu = lambda name: wf.NPU_DIR / name

    common_inputs = [
        ("Session JSON", wf.SESSION_PATH, "file"),
        ("Project root", wf.PROJECT_DIR, "dir"),
        ("indexAI dir", wf.INDEX_AI_DIR, "dir"),
        ("indexAI project index", wf.INDEX_AI_DIR / "project_code_index.md", "file"),
        ("Output dir", wf.OUTPUT_DIR, "dir"),
        ("Workflow log dir", wf.LOG_DIR, "dir"),
    ]

    operation_inputs: list[tuple[str, Path | str, str]] = []
    operation_outputs: list[tuple[str, Path | str, str]] = []
    progress_files: list[tuple[str, Path | str, str]] = []

    if operation == "analyze_wav":
        operation_inputs = [
            ("Current WAV", artifacts["audio_path"], "file"),
            ("analyze_wav.py", script("analyze_wav.py"), "file"),
            ("Audio Python", wf.AUDIO_PYTHON, "file"),
        ]
        operation_outputs = [
            ("Analysis JSON", artifacts["analysis_json"], "file"),
            ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
            ("Analysis plot PNG", artifacts["analysis_plot_png"], "file"),
        ]
    elif operation == "build_track_summary":
        operation_inputs = [
            ("Analysis JSON", artifacts["analysis_json"], "file"),
            ("build_track_summary.py", script("build_track_summary.py"), "file"),
        ]
        operation_outputs = [("Track summary JSON", artifacts["track_summary_json"], "file")]
    elif operation == "build_music_context":
        operation_inputs = [
            ("Analysis JSON", artifacts["analysis_json"], "file"),
            ("Track summary JSON", artifacts["track_summary_json"], "file"),
            ("build_music_context.py", npu("build_music_context.py"), "file"),
        ]
        operation_outputs = [
            ("Music context JSON", artifacts["music_context_json"], "file"),
            ("Analysis AI context JSON", artifacts["analysis_ai_context_json"], "file"),
            ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
            ("NPU music chunks", npu("npu_music_chunks"), "dir"),
        ]
    elif operation == "build_code_context":
        operation_inputs = [
            ("Project root", wf.PROJECT_DIR, "dir"),
            ("build_npu_code_context.py", npu("build_npu_code_context.py"), "file"),
        ]
        operation_outputs = [
            ("NPU code context", npu("npu_code_context.md"), "file"),
            ("NPU code index", npu("npu_code_index.md"), "file"),
            ("NPU code manifest", npu("npu_code_manifest.json"), "file"),
            ("NPU code chunks", npu("npu_code_chunks"), "dir"),
        ]
    elif operation in {"build_manual_context", "ensure_manual_library"}:
        operation_inputs = [
            ("Manual root", wf.ROOT / "manual", "dir"),
            ("build_blender_manual_context.py", npu("build_blender_manual_context.py"), "file"),
        ]
        operation_outputs = [
            ("Manual generated index (manual-focused only)", npu("npu_blender_manual_index.md"), "file"),
            ("Manual generated manifest (manual-focused only)", npu("npu_blender_manual_manifest.json"), "file"),
            ("Manual generated chunks (manual-focused only)", npu("npu_blender_manual_chunks"), "dir"),
        ]
    elif operation == "dual_ai_plan":
        operation_inputs = [
            ("Analysis JSON", artifacts["analysis_json"], "file"),
            ("Track summary JSON", artifacts["track_summary_json"], "file"),
            ("Music context JSON", artifacts["music_context_json"], "file"),
            ("Analysis AI context JSON", artifacts["analysis_ai_context_json"], "file"),
            ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
            ("run_dual_ai_pipeline.py", npu("run_dual_ai_pipeline.py"), "file"),
            ("NPU Python", wf.NPU_PYTHON, "file"),
        ]
        operation_outputs = [
            ("Dual AI scene plan JSON", artifacts["dual_ai_plan_json"], "file"),
            ("Dual AI Blender brief", npu("dual_ai_blender_agent_brief.md"), "file"),
            ("NPU technical notes", npu("npu_dual_ai_technical_notes.md"), "file"),
        ]
        progress_files = [("NPU chunk notes", npu("npu_dual_ai_chunk_notes.md"), "file")]
    elif operation == "dual_ai_implementation":
        operation_inputs = [
            ("Analysis JSON", artifacts["analysis_json"], "file"),
            ("Track summary JSON", artifacts["track_summary_json"], "file"),
            ("Music context JSON", artifacts["music_context_json"], "file"),
            ("Analysis AI context JSON", artifacts["analysis_ai_context_json"], "file"),
            ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
            ("Dual AI scene plan JSON", artifacts["dual_ai_plan_json"], "file"),
            ("run_dual_ai_pipeline.py", npu("run_dual_ai_pipeline.py"), "file"),
            ("NPU Python", wf.NPU_PYTHON, "file"),
        ]
        operation_outputs = [
            ("AI implementation draft JSON", artifacts["ai_implementation_draft_json"], "file"),
            ("Generated script candidate", npu("generated_blender_script_candidate.py"), "file"),
            ("Generated implementation notes", npu("generated_implementation_notes.md"), "file"),
            ("NPU implementation notes", npu("npu_dual_ai_implementation_notes.md"), "file"),
        ]
        progress_files = [("NPU chunk notes", npu("npu_dual_ai_chunk_notes.md"), "file")]
    elif operation == "cleanup_intermediates":
        operation_inputs = [("Output dir", wf.OUTPUT_DIR, "dir"), ("NPU dir", wf.NPU_DIR, "dir")]
    elif operation == "cleanup_render_frames":
        operation_inputs = [("Render frames dir", artifacts["render_frames_dir"], "dir")]

    return {
        "common_inputs": common_inputs,
        "operation_inputs": operation_inputs,
        "operation_outputs": operation_outputs,
        "progress_files": progress_files,
    }


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
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


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
            ok, message = _write_probe(Path(path))
            base["writable"] = ok
            base["write_probe"] = message
            if not ok:
                base["status"] = "WARN" if base["status"] == "OK" else base["status"]
                base["message"] = message
        checks.append(base)
    return checks


def active_compute_processes(processes: list[dict], operation: str) -> list[dict]:
    heavy_ops = {
        "analyze_wav",
        "build_manual_context",
        "dual_ai_plan",
        "dual_ai_implementation",
        "full_audio_prepare",
    }
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

    start_dt = _iso_to_dt(active.get("started_at"))
    watched = output_checks + progress_checks
    latest_write: dict | None = None
    for item in watched:
        item_dt = _iso_to_dt(item.get("mtime"))
        if not item_dt:
            continue
        if start_dt and item_dt < start_dt:
            item["message"] = "old file from before active operation"
        if latest_write is None or str(item.get("mtime", "")) > str(latest_write.get("mtime", "")):
            latest_write = item

    warnings: list[str] = []
    if active["active"] and latest_write:
        latest_dt = _iso_to_dt(latest_write.get("mtime"))
        if latest_dt:
            idle = (datetime.now() - latest_dt).total_seconds()
            if idle > 600:
                warnings.append(f"No watched output/progress file changed for {_format_age(idle)}.")
    if active["active"] and not latest_write and active.get("elapsed_sec") and active["elapsed_sec"] > 300:
        warnings.append("Active operation has no watched output/progress files yet after 5m.")

    if any(item["status"] in {"MISSING", "WARN"} for item in input_checks):
        warnings.append("Some required input paths for the active operation are missing or suspicious.")

    progress_previews = []
    for label, path, _expect in expected["progress_files"]:
        progress_previews.append({"label": label, "path": str(path), "tail": _tail_non_empty(Path(path))})

    processes = collect_processes()
    compute_processes = active_compute_processes(processes, operation)
    active_status = "active" if active.get("active") else "none"
    if active.get("active") and active.get("elapsed_sec") and active["elapsed_sec"] > 120 and not compute_processes:
        active_status = "stale_or_interrupted"
        warnings.append(
            "Log has a start event without a result, but no heavy Python/Ollama/Blender/FFmpeg process is running."
        )

    report = {
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
        "last_result": _read_json(wf.LAST_RESULT_PATH),
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
    return report


def _format_check(item: dict) -> str:
    size = _format_size(item.get("size"))
    mtime = item.get("mtime") or "-"
    message = item.get("message") or item.get("write_probe") or ""
    suffix = f" | {message}" if message else ""
    return f"[{item.get('status', 'OK')}] {item.get('label')}: {item.get('path')} | {size} | {mtime}{suffix}"


def _format_process(item: dict) -> str:
    name = item.get("ProcessName", "-")
    pid = item.get("Id", "-")
    cpu = item.get("CPU", "-")
    ram = _format_size(int(item.get("WorkingSet64") or 0))
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
                f"elapsed {_format_age(active.get('elapsed_sec'))}"
            )
        else:
            lines.append(
                f"Active:    {active.get('operation')} since {active.get('started_at')} "
                f"elapsed {_format_age(active.get('elapsed_sec'))}"
            )
    else:
        lines.append(f"Active:    no running operation detected, checks based on {report['operation_for_checks']}")

    last = report.get("last_result") or {}
    if isinstance(last, dict) and last:
        lines.append(
            f"Last:      {last.get('operation')} ok={last.get('ok')} "
            f"ended={last.get('ended_at')} elapsed={last.get('elapsed_sec')}"
        )

    if report["warnings"]:
        lines.append("")
        lines.append("Warnings:")
        for warning in report["warnings"]:
            lines.append(f"  - {warning}")

    lines.append("")
    lines.append("Write Checks:")
    for item in report["write_checks"]:
        lines.append("  " + _format_check(item))

    lines.append("")
    lines.append("Common Paths:")
    for item in report["common_checks"]:
        lines.append("  " + _format_check(item))

    if report["input_checks"]:
        lines.append("")
        lines.append("Inputs For Active Operation:")
        for item in report["input_checks"]:
            lines.append("  " + _format_check(item))

    if report["output_checks"]:
        lines.append("")
        lines.append("Expected Outputs / Pending Files:")
        for item in report["output_checks"]:
            lines.append("  " + _format_check(item))

    if report["progress_checks"]:
        lines.append("")
        lines.append("Progress Files:")
        for item in report["progress_checks"]:
            lines.append("  " + _format_check(item))

    if report["progress_previews"]:
        lines.append("")
        lines.append("Progress Preview:")
        for preview in report["progress_previews"]:
            lines.append(f"  {preview['label']}: {preview['path']}")
            tail = preview.get("tail") or ["<empty or missing>"]
            for line in tail:
                lines.append(f"    {line[:240]}")

    lines.append("")
    lines.append("AI / Render Processes:")
    processes = report.get("processes") or []
    if processes:
        for item in processes[:14]:
            lines.append("  " + _format_process(item))
    else:
        lines.append("  <no process snapshot available>")

    lines.append("")
    lines.append("Recent Events:")
    for event in report["recent_events"]:
        lines.append(f"  {event.get('time')} {event.get('operation')}::{event.get('event')}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Spaziotempo workflow advanced debug checker.")
    parser.add_argument("--json", action="store_true", help="Print raw JSON report.")
    parser.add_argument("--watch", action="store_true", help="Refresh the report in this window.")
    parser.add_argument("--interval", type=float, default=3.0, help="Watch refresh interval in seconds.")
    parser.add_argument("--no-write-probe", action="store_true", help="Use access checks only, no temporary write probes.")
    args = parser.parse_args()

    probe_write = not args.no_write_probe
    if args.watch:
        try:
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                report = build_debug_report(probe_write=probe_write)
                print(format_debug_report(report))
                print("\nCtrl+C per chiudere questa finestra debug.")
                time.sleep(max(1.0, args.interval))
        except KeyboardInterrupt:
            return 0

    report = build_debug_report(probe_write=probe_write)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_debug_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
