from __future__ import annotations

import json
import shutil
from dataclasses import asdict
from pathlib import Path

from .common import (
    DEFAULT_REPORT_JSON,
    PROJECT_DIR,
    WORKSPACE_ROOT,
    Check,
    add,
    check_ollama,
    check_python_runtime,
    now_iso,
    powershell_get_command,
    probe_write,
)


def build_report(project: Path = PROJECT_DIR, workspace_root: Path = WORKSPACE_ROOT) -> dict:
    checks: list[Check] = []
    add(checks, "Project root", "OK" if project.exists() else "MISS", str(project), project)
    add(
        checks,
        "Workflow state",
        "OK" if (project / "Tools" / "workflow" / "workflow_core" / "__init__.py").exists() else "MISS",
        "workflow_core",
        project / "Tools" / "workflow" / "workflow_core" / "__init__.py",
    )
    add(
        checks,
        "Scene brief",
        "OK" if (project / "Tools" / "workflow" / "scene_brief.py").exists() else "MISS",
        "scene_brief.py",
        project / "Tools" / "workflow" / "scene_brief.py",
    )

    for name, path in _startup_paths(project, workspace_root):
        if name == "Manual library":
            ok = path.exists()
            detail = "read-only library present" if ok else "missing"
        else:
            ok, detail = probe_write(path)
        add(checks, name, "OK" if ok else "WARN", detail, path)

    check_ollama(checks)
    _check_python_lanes(checks, workspace_root)
    _check_media_tools(checks)
    _check_workflow_session(checks)
    return _report_from_checks(project, workspace_root, checks)


def _startup_paths(project: Path, workspace_root: Path) -> list[tuple[str, Path]]:
    return [
        ("Output dir", project / "output"),
        ("Workflow logs", project / "output" / "workflow_logs"),
        ("indexAI", project / "indexAI"),
        ("Manual library", workspace_root / "manual"),
        ("Renders dir", workspace_root / "renders"),
    ]


def _check_python_lanes(checks: list[Check], workspace_root: Path) -> None:
    npu_python = workspace_root / "venvs" / "blender-npu-ai" / "Scripts" / "python.exe"
    audio_python = workspace_root / "venvs" / "blender-audio-ai" / "Scripts" / "python.exe"
    check_python_runtime(
        checks,
        "NPU/OpenVINO runtime",
        npu_python,
        "import json; import openvino as ov; print(json.dumps({'devices': list(ov.Core().available_devices)}))",
        timeout=25.0,
    )
    check_python_runtime(
        checks,
        "Audio analysis runtime",
        audio_python,
        "import librosa, numpy, matplotlib; print('audio deps ok')",
        timeout=25.0,
    )


def _check_media_tools(checks: list[Check]) -> None:
    ffmpeg = shutil.which("ffmpeg") or powershell_get_command("ffmpeg")
    ffprobe = shutil.which("ffprobe") or powershell_get_command("ffprobe")
    add(checks, "ffmpeg", "OK" if ffmpeg else "MISS", ffmpeg or "ffmpeg not in PATH", ffmpeg)
    add(checks, "ffprobe", "OK" if ffprobe else "MISS", ffprobe or "ffprobe not in PATH", ffprobe)


def _check_workflow_session(checks: list[Check]) -> None:
    try:
        try:
            from workflow_core import load_session, operation_status
        except ImportError:
            from Tools.workflow.workflow_core import load_session, operation_status

        session = load_session(create=True)
        status = operation_status(session)
        add(
            checks,
            "Workflow session",
            "OK",
            f"track={session.track_stem}; chat={session.chat_model}; script_tokens={session.script_max_tokens}",
        )
        missing = [
            key
            for key, value in status.items()
            if key in {"analysis_json", "music_context_json", "blender_keyframes_json"}
            and not value
        ]
        add(
            checks,
            "Current track inputs",
            "OK" if not missing else "WARN",
            "ready" if not missing else "missing: " + ", ".join(missing),
        )
    except Exception as exc:
        add(checks, "Workflow session", "WARN", str(exc))


def _report_from_checks(project: Path, workspace_root: Path, checks: list[Check]) -> dict:
    errors = [f"{item.name}: {item.detail}" for item in checks if item.status in {"DOWN", "MISS"}]
    warnings = [f"{item.name}: {item.detail}" for item in checks if item.status == "WARN"]
    passed = not errors
    return {
        "schema_version": 1,
        "kind": "startup_check",
        "repo_root": str(project),
        "workspace_root": str(workspace_root),
        "generated_at": now_iso(),
        "project": str(project),
        "root": str(workspace_root),
        "passed": passed,
        "ok": passed,
        "warning_count": len(warnings) + len(errors),
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "blender_runtime_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "checks": [asdict(item) for item in checks],
    }


def format_report(report: dict, report_json: Path | str = DEFAULT_REPORT_JSON) -> str:
    lines = [
        "=" * 78,
        "SPAZIOTEMPO STARTUP SERVICE CHECK",
        "=" * 78,
        f"Generated: {report.get('generated_at')}",
        f"Project:   {report.get('project')}",
        f"Workspace: {report.get('workspace_root')}",
        "",
    ]
    for item in report.get("checks", []):
        path = f" | {item.get('path')}" if item.get("path") else ""
        lines.append(f"[{item.get('status')}] {item.get('name')}: {item.get('detail')}{path}")
    lines.append("")
    lines.append(f"Warnings: {report.get('warning_count', 0)}")
    lines.append(f"Report:   {report_json}")
    return "\n".join(lines)


def save_report(
    report: dict,
    report_json: Path | str = DEFAULT_REPORT_JSON,
    report_txt: Path | str | None = None,
) -> tuple[Path, Path]:
    json_path = Path(report_json)
    txt_path = Path(report_txt) if report_txt else json_path.with_suffix(".txt")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    report["report_json"] = str(json_path)
    report["report_txt"] = str(txt_path)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    txt_path.write_text(format_report(report, json_path) + "\n", encoding="utf-8")
    return json_path, txt_path
