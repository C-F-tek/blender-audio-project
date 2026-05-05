from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


THIS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = THIS_DIR.parents[1]
WORKSPACE_ROOT = PROJECT_DIR.parent
NPU_DIR = PROJECT_DIR / "Tools" / "npu"

DEFAULT_LOG_DIR = PROJECT_DIR / "output" / "workflow_logs"
DEFAULT_REPORT_JSON = DEFAULT_LOG_DIR / "startup_check.json"


if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))
if str(NPU_DIR) not in sys.path:
    sys.path.insert(0, str(NPU_DIR))


@dataclass
class Check:
    name: str
    status: str
    detail: str
    path: str | None = None


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def add(
    checks: list[Check],
    name: str,
    status: str,
    detail: str,
    path: Path | str | None = None,
) -> None:
    checks.append(
        Check(
            name=name,
            status=status,
            detail=detail,
            path=str(path) if path else None,
        )
    )


def probe_write(path: Path) -> tuple[bool, str]:
    try:
        path.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(
            prefix=".spaziotempo_probe_",
            suffix=".tmp",
            dir=str(path),
        )
        os.close(fd)
        Path(temp_name).unlink(missing_ok=True)
        return True, "temp write ok"
    except Exception as exc:
        return False, str(exc)


def run_probe(
    command: list[str],
    timeout: float = 12.0,
    cwd: Path | None = None,
) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd or PROJECT_DIR),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except Exception as exc:
        return False, str(exc)

    output = (result.stdout or "").strip()
    return result.returncode == 0, output[-1200:] if output else f"exit={result.returncode}"


def powershell_test_path(path: Path) -> bool:
    escaped = str(path).replace("'", "''")
    ok, output = run_probe(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"if (Test-Path -LiteralPath '{escaped}') {{ 'YES' }} else {{ 'NO' }}",
        ],
        timeout=6.0,
    )
    return ok and output.strip().endswith("YES")


def powershell_get_command(name: str) -> str | None:
    ok, output = run_probe(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"$cmd = Get-Command {name} -ErrorAction SilentlyContinue; if ($cmd) {{ $cmd.Source }}",
        ],
        timeout=6.0,
    )
    return output.strip() if ok and output.strip() else None


def visible_path_exists(path: Path) -> bool:
    return path.exists() or powershell_test_path(path)


def fallback_ollama_exe() -> Path | None:
    candidates: list[Path] = []

    value = os.environ.get("OLLAMA_EXE")
    if value:
        candidates.append(Path(value))

    local_app = os.environ.get("LOCALAPPDATA")
    user_profile = os.environ.get("USERPROFILE")
    program_files = os.environ.get("ProgramFiles")

    if local_app:
        candidates.extend(
            [
                Path(local_app) / "Programs" / "Ollama" / "ollama.exe",
                Path(local_app) / "Ollama" / "ollama.exe",
            ]
        )
    if user_profile:
        candidates.append(
            Path(user_profile) / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe"
        )
    if program_files:
        candidates.append(Path(program_files) / "Ollama" / "ollama.exe")

    command_path = powershell_get_command("ollama")
    if command_path:
        candidates.append(Path(command_path))

    for candidate in candidates:
        if visible_path_exists(candidate):
            return candidate
    return None


def check_python_runtime(
    checks: list[Check],
    label: str,
    python_path: Path,
    code: str,
    timeout: float = 20.0,
) -> None:
    if not python_path.exists():
        add(checks, label, "MISS", "python.exe missing", python_path)
        return

    ok, output = run_probe([str(python_path), "-c", code], timeout=timeout)
    add(checks, label, "OK" if ok else "WARN", output or "ok", python_path)


def check_ollama(checks: list[Check]) -> None:
    try:
        from ollama_runtime import (
            DEFAULT_BASE_URL,
            find_ollama_exe,
            is_server_ready,
            list_models,
            list_models_from_disk,
            start_server,
        )

        exe = find_ollama_exe() or fallback_ollama_exe()
        if exe:
            add(checks, "Ollama executable", "OK", str(exe), exe)
        else:
            add(
                checks,
                "Ollama executable",
                "MISS",
                "ollama.exe not found; set OLLAMA_EXE or restart PATH",
            )

        ready = is_server_ready(DEFAULT_BASE_URL, timeout=2.0)
        started = False

        if not ready and exe:
            try:
                start_server(exe, DEFAULT_BASE_URL, startup_timeout=10.0)
                ready = is_server_ready(DEFAULT_BASE_URL, timeout=2.0)
                started = ready
            except Exception as exc:
                add(checks, "Ollama API autostart", "WARN", str(exc), exe)

        if ready:
            try:
                models = list_models(DEFAULT_BASE_URL)
            except Exception:
                models = list_models_from_disk()

            detail = f"{DEFAULT_BASE_URL} UP"
            if started:
                detail += " (started now)"
            detail += f"; models={', '.join(models[:8]) if models else 'none'}"
            add(checks, "Ollama API", "OK", detail)
        else:
            disk_models = list_models_from_disk()
            detail = f"{DEFAULT_BASE_URL} DOWN"
            if disk_models:
                detail += f"; disk models={', '.join(disk_models[:8])}"
            add(checks, "Ollama API", "DOWN", detail)
    except Exception as exc:
        add(checks, "Ollama runtime", "WARN", str(exc))


def build_report(project: Path = PROJECT_DIR, workspace_root: Path = WORKSPACE_ROOT) -> dict:
    checks: list[Check] = []

    add(checks, "Project root", "OK" if project.exists() else "MISS", str(project), project)
    add(
        checks,
        "Workflow state",
        "OK" if (project / "Tools" / "workflow" / "workflow_state.py").exists() else "MISS",
        "workflow_state.py",
        project / "Tools" / "workflow" / "workflow_state.py",
    )
    add(
        checks,
        "Scene brief",
        "OK" if (project / "Tools" / "workflow" / "scene_brief.py").exists() else "MISS",
        "scene_brief.py",
        project / "Tools" / "workflow" / "scene_brief.py",
    )

    for name, path in [
        ("Output dir", project / "output"),
        ("Workflow logs", project / "output" / "workflow_logs"),
        ("indexAI", project / "indexAI"),
        ("Manual library", workspace_root / "manual"),
        ("Renders dir", workspace_root / "renders"),
    ]:
        if name == "Manual library":
            ok = path.exists()
            detail = "read-only library present" if ok else "missing"
        else:
            ok, detail = probe_write(path)
        add(checks, name, "OK" if ok else "WARN", detail, path)

    check_ollama(checks)

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

    ffmpeg = shutil.which("ffmpeg") or powershell_get_command("ffmpeg")
    ffprobe = shutil.which("ffprobe") or powershell_get_command("ffprobe")
    add(checks, "ffmpeg", "OK" if ffmpeg else "MISS", ffmpeg or "ffmpeg not in PATH", ffmpeg)
    add(checks, "ffprobe", "OK" if ffprobe else "MISS", ffprobe or "ffprobe not in PATH", ffprobe)

    try:
        from workflow_state import load_session, operation_status

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
            if key in {"analysis_json", "music_context_json", "blender_keyframes_json"} and not value
        ]
        add(
            checks,
            "Current track inputs",
            "OK" if not missing else "WARN",
            "ready" if not missing else "missing: " + ", ".join(missing),
        )
    except Exception as exc:
        add(checks, "Workflow session", "WARN", str(exc))

    errors = [
        f"{item.name}: {item.detail}"
        for item in checks
        if item.status in {"DOWN", "MISS"}
    ]
    warnings = [
        f"{item.name}: {item.detail}"
        for item in checks
        if item.status == "WARN"
    ]
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

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    txt_path.write_text(format_report(report, json_path) + "\n", encoding="utf-8")
    return json_path, txt_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Spaziotempo startup service check")
    parser.add_argument("--project", default=str(PROJECT_DIR), help="Project/repository directory to inspect.")
    parser.add_argument(
        "--repo-root",
        default="",
        help="Compatibility alias used by IA-Carmine launchers. Maps to the project/repository directory.",
    )
    parser.add_argument(
        "--root",
        default="",
        help="Workspace root. Defaults to the parent of the selected project/repository directory.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_REPORT_JSON),
        help="JSON report output path. Defaults to output/workflow_logs/startup_check.json.",
    )
    parser.add_argument(
        "--text-output",
        default="",
        help="Optional text report output path. Defaults to the JSON output path with .txt suffix.",
    )
    parser.add_argument("--json", action="store_true", help="Print the JSON report to stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    project = Path(args.repo_root or args.project).resolve(strict=False)
    workspace_root = Path(args.root).resolve(strict=False) if args.root else project.parent

    output_path = Path(args.output).resolve(strict=False)
    text_output_path = (
        Path(args.text_output).resolve(strict=False)
        if args.text_output
        else output_path.with_suffix(".txt")
    )

    report = build_report(project, workspace_root)
    save_report(report, output_path, text_output_path)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_report(report, output_path))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())