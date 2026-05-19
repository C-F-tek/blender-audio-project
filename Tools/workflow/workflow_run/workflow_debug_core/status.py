"""Path and event status helpers for workflow debugging."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

try:
    import workflow_core as wf
except ImportError:
    from Tools.workflow import workflow_core as wf


def iso_to_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def format_age(seconds: float | None) -> str:
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


def format_size(size: int | None) -> str:
    if size is None:
        return "-"
    value = float(size)
    for suffix in ["B", "KB", "MB", "GB"]:
        if value < 1024 or suffix == "GB":
            return f"{value:.1f} {suffix}" if suffix != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} GB"


def read_json(path: Path) -> dict | list | None:
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
            events.append(
                {
                    "time": "",
                    "operation": "log_parse",
                    "event": "bad_json",
                    "payload": {"raw": line[:500]},
                }
            )
    return events


def detect_active_operation(events: list[dict]) -> dict:
    for index in range(len(events) - 1, -1, -1):
        event = events[index]
        if event.get("event") != "start":
            continue
        operation = str(event.get("operation") or "")
        start_time = str(event.get("time") or "")
        has_result = any(
            later.get("operation") == operation and later.get("event") == "result"
            for later in events[index + 1 :]
        )
        if has_result:
            continue
        start_dt = iso_to_dt(start_time)
        elapsed = (datetime.now() - start_dt).total_seconds() if start_dt else None
        return {
            "active": True,
            "operation": operation,
            "started_at": start_time,
            "elapsed_sec": elapsed,
            "payload": event.get("payload") or {},
        }

    last_result = next((event for event in reversed(events) if event.get("event") == "result"), None)
    return {
        "active": False,
        "operation": str(last_result.get("operation") if last_result else ""),
        "started_at": "",
        "elapsed_sec": None,
        "payload": last_result.get("payload") if last_result else {},
    }


def tail_non_empty(path: Path, max_lines: int = 8) -> list[str]:
    if not path.exists() or not path.is_file():
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        return [f"<read failed: {exc}>"]
    return [line.strip() for line in lines if line.strip()][-max_lines:]


def write_probe(directory: Path) -> tuple[bool, str]:
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
    npu = lambda name: wf.NPU_DIR / name
    audio = lambda name: wf.PROJECT_DIR / "Tools" / "workflow" / "audio_analysis" / name
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
            ("audio_analysis.analyze_cli", audio("analyze_cli.py"), "file"),
            ("audio_analysis.analyzer", audio("analyzer.py"), "file"),
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
            ("audio_analysis.summary_cli", audio("summary_cli.py"), "file"),
            ("audio_analysis.summary", audio("summary.py"), "file"),
        ]
        operation_outputs = [("Track summary JSON", artifacts["track_summary_json"], "file")]
    elif operation == "build_music_context":
        operation_inputs = [
            ("Analysis JSON", artifacts["analysis_json"], "file"),
            ("Track summary JSON", artifacts["track_summary_json"], "file"),
            ("Tools.npu build_music_context", npu("music_context/cli.py"), "file"),
        ]
        operation_outputs = [
            ("Music context JSON", artifacts["music_context_json"], "file"),
            ("Analysis AI context JSON", artifacts["analysis_ai_context_json"], "file"),
            ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
            ("NPU music chunks", npu("npu_music_chunks"), "dir"),
        ]
    elif operation == "build_code_context":
        operation_inputs = [("Project root", wf.PROJECT_DIR, "dir"), ("build_npu_code_context.py", npu("build_npu_code_context.py"), "file")]
        operation_outputs = [
            ("NPU code context", npu("context_artifacts/npu_code_context.md"), "file"),
            ("NPU code index", npu("context_artifacts/npu_code_index.md"), "file"),
            ("NPU code manifest", npu("context_artifacts/npu_code_manifest.json"), "file"),
            ("NPU code chunks", npu("npu_code_chunks"), "dir"),
        ]
    elif operation in {"build_manual_context", "ensure_manual_library"}:
        operation_inputs = [
            ("Manual root", wf.ROOT / "manual", "dir"),
            ("build_blender_manual_context.py", npu("build_blender_manual_context.py"), "file"),
        ]
        operation_outputs = [
            ("Manual generated index", npu("npu_blender_manual_index.md"), "file"),
            ("Manual generated manifest", npu("npu_blender_manual_manifest.json"), "file"),
            ("Manual generated chunks", npu("npu_blender_manual_chunks"), "dir"),
        ]
    elif operation == "dual_ai_plan":
        operation_inputs = _dual_ai_inputs(artifacts, npu, include_plan=False)
        operation_outputs = [
            ("Dual AI scene plan JSON", artifacts["dual_ai_plan_json"], "file"),
            ("Dual AI Blender brief", npu("context_artifacts/dual_ai_blender_agent_brief.md"), "file"),
            ("NPU technical notes", npu("context_artifacts/npu_dual_ai_technical_notes.md"), "file"),
        ]
        progress_files = [("NPU chunk notes", npu("npu_dual_ai_chunk_notes.md"), "file")]
    elif operation == "dual_ai_implementation":
        operation_inputs = _dual_ai_inputs(artifacts, npu, include_plan=True)
        scene_script = artifacts.get("generated_scene_script")
        operation_outputs = [
            ("AI implementation draft JSON", artifacts["ai_implementation_draft_json"], "file"),
            ("Generated script candidate", Path(scene_script) if scene_script else wf.INDEX_AI_DIR / "scene_scripts", "file"),
            ("Generated implementation notes", npu("context_artifacts/generated_implementation_notes.md"), "file"),
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


def _dual_ai_inputs(artifacts: dict, npu, include_plan: bool) -> list[tuple[str, Path | str, str]]:
    inputs = [
        ("Analysis JSON", artifacts["analysis_json"], "file"),
        ("Track summary JSON", artifacts["track_summary_json"], "file"),
        ("Music context JSON", artifacts["music_context_json"], "file"),
        ("Analysis AI context JSON", artifacts["analysis_ai_context_json"], "file"),
        ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
        ("Tools.npu run_dual_ai_pipeline", npu("dual_ai_pipeline/cli.py"), "file"),
        ("NPU Python", wf.NPU_PYTHON, "file"),
    ]
    if include_plan:
        inputs.insert(5, ("Dual AI scene plan JSON", artifacts["dual_ai_plan_json"], "file"))
    return inputs
