from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import json
import sys
from typing import Any

ROOT = Path.home() / "blender"
PROJECT_DIR = ROOT / "blender-audio-project"
OUTPUT_DIR = PROJECT_DIR / "output"
LOG_DIR = OUTPUT_DIR / "workflow_logs"
SESSION_PATH = OUTPUT_DIR / "spaziotempo_workflow_session.json"
LAST_RESULT_PATH = LOG_DIR / "last_operation_result.json"
EVENT_LOG_PATH = LOG_DIR / "workflow_events.jsonl"
OLLAMA_LOG_PATH = LOG_DIR / "ollama_runtime_events.jsonl"
SCENE_DIRECTOR_LOG_PATH = LOG_DIR / "scene_director_runtime_events.jsonl"
NPU_TRACE_PATH = LOG_DIR / "npu_runtime_trace.jsonl"
DIAG_JSON = LOG_DIR / "ai_runtime_diagnostics.json"
DIAG_MD = LOG_DIR / "ai_runtime_diagnostics.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return {"read_error": str(exc), "path": str(path)}


def read_text(path: Path, limit: int | None = None) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text if limit is None else text[:limit]


def tail_jsonl(path: Path, limit: int = 80) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]:
        try:
            rows.append(json.loads(line))
        except Exception:
            rows.append({"raw": line})
    return rows


def append_jsonl(path: Path, event: str, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"time": now_iso(), "event": event, "payload": payload}, ensure_ascii=False) + "\n")


def file_info(path: Path) -> dict[str, Any]:
    info = {"path": str(path), "exists": path.exists()}
    if path.exists() and path.is_file():
        stat = path.stat()
        info.update({"size_bytes": stat.st_size, "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds")})
    return info


def slugify(value: str) -> str:
    import re
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_") or "track"


def artifacts_for_track(track_stem: str) -> dict[str, Path]:
    slug = slugify(track_stem)
    return {
        "analysis_json": OUTPUT_DIR / f"{track_stem}_analysis.json",
        "music_context_json": OUTPUT_DIR / f"{track_stem}_music_context.json",
        "scene_brief_json": OUTPUT_DIR / f"{track_stem}_scene_brief.json",
        "dual_ai_plan_json": OUTPUT_DIR / f"{track_stem}_dual_ai_scene_plan.json",
        "implementation_draft_json": OUTPUT_DIR / f"{track_stem}_ai_implementation_draft.json",
        "generated_scene_script": PROJECT_DIR / "indexAI" / "scene_scripts" / f"{slug}_scene_builder_candidate.py",
        "legacy_generated_script": PROJECT_DIR / "Tools" / "npu" / "generated_blender_script_candidate.py",
        "generated_notes": PROJECT_DIR / "Tools" / "npu" / "generated_implementation_notes.md",
    }


def analyze_scene_brief(path: Path) -> dict[str, Any]:
    data = read_json(path)
    if not isinstance(data, dict):
        return {"available": False, "path": str(path)}
    transcript = data.get("conversation_transcript") if isinstance(data.get("conversation_transcript"), list) else []
    assistant_empty = [
        item for item in transcript
        if str(item.get("role", "")).lower() == "assistant" and "Ollama non ha restituito testo" in str(item.get("content", ""))
    ]
    return {
        "available": True,
        "path": str(path),
        "message_count": len(transcript),
        "assistant_empty_response_count": len(assistant_empty),
        "memory": data.get("conversation_memory") if isinstance(data.get("conversation_memory"), dict) else {},
        "recent_messages": transcript[-8:],
    }


def analyze_implementation(path: Path, script_path: Path, notes_path: Path) -> dict[str, Any]:
    draft = read_json(path)
    script = read_text(script_path, limit=40000)
    notes = read_text(notes_path, limit=12000)
    markers = []
    haystack = "\n".join([json.dumps(draft, ensure_ascii=False) if isinstance(draft, dict) else "", script, notes]).lower()
    for marker in ["deterministic", "fallback", "invalid", "scene_script is missing", "too short", "parse_error"]:
        if marker in haystack:
            markers.append(marker)
    return {
        "draft_file": file_info(path),
        "script_file": file_info(script_path),
        "notes_file": file_info(notes_path),
        "fallback_markers": sorted(set(markers)),
        "script_chars": len(script),
        "script_has_import_bpy": "import bpy" in script,
        "script_has_keyframe_insert": "keyframe_insert" in script,
        "draft_keys": sorted(draft.keys()) if isinstance(draft, dict) else [],
        "validation": draft.get("validation") if isinstance(draft, dict) else None,
    }


def analyze_workflow_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    dual_events = [row for row in events if str(row.get("operation", "")).startswith("dual_ai") or row.get("operation") in {"run_dual_ai", "dual_ai_plan", "dual_ai_implementation"}]
    ai_ops = []
    for row in events:
        payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
        metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else payload.get("metadata")
        if isinstance(metadata, dict):
            item = {
                "time": row.get("time"),
                "operation": row.get("operation"),
                "event": row.get("event"),
                "skip_npu_heavy_pass": metadata.get("skip_npu") if "skip_npu" in metadata else metadata.get("skip_npu_heavy_pass"),
                "skip_ollama": metadata.get("skip_ollama"),
                "creative_model": metadata.get("creative_model"),
                "technical_model": metadata.get("technical_model"),
                "max_new_tokens": metadata.get("max_new_tokens"),
                "script_max_tokens": metadata.get("script_max_tokens"),
            }
            if any(value is not None for value in item.values()):
                ai_ops.append(item)
    return {"dual_event_count": len(dual_events), "recent_ai_operation_metadata": ai_ops[-12:]}


def analyze_ollama(events: list[dict[str, Any]]) -> dict[str, Any]:
    generate_results = [row for row in events if row.get("event") == "generate_result"]
    generate_errors = [row for row in events if row.get("event") == "generate_error"]
    empty = [row for row in generate_results if (row.get("payload") or {}).get("empty_response")]
    return {
        "log_path": str(OLLAMA_LOG_PATH),
        "event_count": len(events),
        "generate_result_count": len(generate_results),
        "generate_error_count": len(generate_errors),
        "empty_response_count": len(empty),
        "recent_empty_responses": empty[-8:],
        "recent_errors": generate_errors[-8:],
        "recent_results": generate_results[-8:],
    }


def run_npu_preflight() -> dict[str, Any]:
    npu_dir = PROJECT_DIR / "Tools" / "npu"
    if str(npu_dir) not in sys.path:
        sys.path.insert(0, str(npu_dir))
    try:
        from npu_runtime import npu_preflight, DEFAULT_NPU_PYTHON, DEFAULT_MODEL_DIR, write_npu_preflight_report  # type: ignore

        report = npu_preflight(DEFAULT_NPU_PYTHON, DEFAULT_MODEL_DIR)
        report_path = PROJECT_DIR / "Tools" / "npu" / "npu_preflight_report.json"
        write_npu_preflight_report(report, report_path)
        payload = {"ready": report.get("ready"), "devices": report.get("openvino_available_devices"), "report_path": str(report_path), "errors": report.get("errors", [])}
        append_jsonl(NPU_TRACE_PATH, "npu_preflight", payload)
        return {"available": True, "report": report, "trace_path": str(NPU_TRACE_PATH), "report_path": str(report_path)}
    except Exception as exc:
        payload = {"available": False, "error_type": type(exc).__name__, "error": str(exc)}
        append_jsonl(NPU_TRACE_PATH, "npu_preflight_error", payload)
        return payload


def build_report(track_stem: str | None = None) -> dict[str, Any]:
    session = read_json(SESSION_PATH)
    session_track = session.get("track_stem") if isinstance(session, dict) else None
    track = track_stem or session_track or "unknown"
    artifacts = artifacts_for_track(track)
    workflow_events = tail_jsonl(EVENT_LOG_PATH, limit=240)
    ollama_events = tail_jsonl(OLLAMA_LOG_PATH, limit=240)
    scene_events = tail_jsonl(SCENE_DIRECTOR_LOG_PATH, limit=120)
    npu_events_before = tail_jsonl(NPU_TRACE_PATH, limit=120)
    npu_preflight = run_npu_preflight()
    npu_events_after = tail_jsonl(NPU_TRACE_PATH, limit=120)

    report = {
        "schema_version": 2,
        "generated_at": now_iso(),
        "track_stem": track,
        "session": session if isinstance(session, dict) else {},
        "last_result": read_json(LAST_RESULT_PATH),
        "files": {key: file_info(path) for key, path in artifacts.items()},
        "scene_brief_analysis": analyze_scene_brief(artifacts["scene_brief_json"]),
        "implementation_analysis": analyze_implementation(artifacts["implementation_draft_json"], artifacts["generated_scene_script"], artifacts["generated_notes"]),
        "workflow_event_analysis": analyze_workflow_events(workflow_events),
        "ollama_analysis": analyze_ollama(ollama_events),
        "scene_director_runtime_events": {"log_path": str(SCENE_DIRECTOR_LOG_PATH), "event_count": len(scene_events), "recent_events": scene_events[-12:]},
        "npu_analysis": {"preflight": npu_preflight, "trace_path": str(NPU_TRACE_PATH), "previous_event_count": len(npu_events_before), "event_count": len(npu_events_after), "recent_events": npu_events_after[-12:]},
        "recommendations": [],
    }

    recs = report["recommendations"]
    if report["scene_brief_analysis"].get("assistant_empty_response_count", 0) > 0:
        recs.append("Scene Director Chat has empty Ollama replies; inspect ollama_runtime_events.jsonl for done_reason, prompt size and eval_count.")
    if report["implementation_analysis"].get("fallback_markers"):
        recs.append("Generated script appears to come from fallback or invalid draft recovery; inspect implementation_draft validation and Ollama raw output.")
    last_ai = report["workflow_event_analysis"].get("recent_ai_operation_metadata", [])[-1:] or []
    if last_ai and last_ai[0].get("skip_npu_heavy_pass") is True:
        recs.append("Skip NPU heavy pass is active: Dual AI will not call the legacy heavy NPU pass by design; NPU preflight is still logged in npu_runtime_trace.jsonl.")
    npu_report = report["npu_analysis"].get("preflight", {})
    if isinstance(npu_report, dict) and isinstance(npu_report.get("report"), dict) and not npu_report["report"].get("ready"):
        recs.append("NPU preflight is not ready; check Tools/npu/npu_preflight_report.json for missing runtime/model/device.")
    return report


def markdown_report(report: dict[str, Any]) -> str:
    lines = ["# AI Runtime Diagnostics", "", f"Generated: {report.get('generated_at')}", f"Track: `{report.get('track_stem')}`", "", "## Scene Director Chat"]
    chat = report.get("scene_brief_analysis", {})
    lines.extend([f"- Messages: `{chat.get('message_count', 0)}`", f"- Empty Ollama assistant replies: `{chat.get('assistant_empty_response_count', 0)}`", "", "## Ollama"])
    ollama = report.get("ollama_analysis", {})
    lines.extend([f"- Events: `{ollama.get('event_count', 0)}`", f"- Generate results: `{ollama.get('generate_result_count', 0)}`", f"- Generate errors: `{ollama.get('generate_error_count', 0)}`", f"- Empty responses: `{ollama.get('empty_response_count', 0)}`", f"- Log: `{ollama.get('log_path')}`", "", "## NPU"])
    npu = report.get("npu_analysis", {})
    preflight = npu.get("preflight", {}) if isinstance(npu, dict) else {}
    preflight_report = preflight.get("report", {}) if isinstance(preflight, dict) else {}
    lines.extend([f"- Trace log: `{npu.get('trace_path')}`", f"- Event count: `{npu.get('event_count', 0)}`", f"- Preflight ready: `{preflight_report.get('ready')}`", f"- Devices: `{preflight_report.get('openvino_available_devices')}`", f"- Errors: `{preflight_report.get('errors')}`", "", "## Implementation Draft / Script"])
    impl = report.get("implementation_analysis", {})
    lines.extend([f"- Script chars: `{impl.get('script_chars', 0)}`", f"- Has import bpy: `{impl.get('script_has_import_bpy')}`", f"- Has keyframe_insert: `{impl.get('script_has_keyframe_insert')}`", f"- Fallback markers: `{', '.join(impl.get('fallback_markers', [])) or '-'}`", "", "## Recent AI Operation Metadata"])
    for item in report.get("workflow_event_analysis", {}).get("recent_ai_operation_metadata", [])[-8:]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Recommendations"])
    for rec in report.get("recommendations", []):
        lines.append(f"- {rec}")
    if not report.get("recommendations"):
        lines.append("- No immediate runtime anomaly detected in collected logs.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track-stem")
    parser.add_argument("--json-out", default=str(DIAG_JSON))
    parser.add_argument("--md-out", default=str(DIAG_MD))
    args = parser.parse_args()

    report = build_report(args.track_stem)
    json_out = Path(args.json_out)
    md_out = Path(args.md_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    md_out.write_text(markdown_report(report), encoding="utf-8")
    print(f"[OK] Wrote: {json_out}")
    print(f"[OK] Wrote: {md_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
