from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys
import time


ROOT = Path.home() / "blender"
PROJECT_DIR = ROOT / "blender-audio-project"
AUDIO_DIR = ROOT / "audio"
RENDERS_DIR = ROOT / "renders"
OUTPUT_DIR = PROJECT_DIR / "output"
TOOLS_DIR = PROJECT_DIR / "Tools"
NPU_DIR = TOOLS_DIR / "npu"
INDEX_AI_DIR = PROJECT_DIR / "indexAI"
SESSION_PATH = OUTPUT_DIR / "spaziotempo_workflow_session.json"
LOG_DIR = OUTPUT_DIR / "workflow_logs"
EVENT_LOG_PATH = LOG_DIR / "workflow_events.jsonl"
LAST_RESULT_PATH = LOG_DIR / "last_operation_result.json"

DEFAULT_WAV = AUDIO_DIR / "Feel The Light-Luca Vera_Master.wav"
DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
DEFAULT_RENDER_STEM = "spaziotempo_asset_visual_v61b"
DEFAULT_FRAME_PREFIX = "spaziotempo_v61b_"
NPU_PYTHON = ROOT / "venvs" / "blender-npu-ai" / "Scripts" / "python.exe"
AUDIO_PYTHON = ROOT / "venvs" / "blender-audio-ai" / "Scripts" / "python.exe"
DEFAULT_CREATIVE_MODEL = "qwen2.5-coder:14b"
DEFAULT_TECHNICAL_MODEL = "qwen2.5-coder:14b"
DEFAULT_CHAT_MODEL = "qwen2.5-coder:14b"
DEFAULT_SCRIPT_TOKENS = 7000


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class OperationResult:
    operation: str
    ok: bool
    started_at: str
    ended_at: str
    elapsed_sec: float
    command: list[str] | None = None
    cwd: str | None = None
    returncode: int | None = None
    stdout_tail: str = ""
    error: str | None = None
    metadata: dict | None = None


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def append_event(operation: str, event: str, payload: dict | None = None) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = {
        "time": now_iso(),
        "operation": operation,
        "event": event,
        "payload": payload or {},
    }
    with EVENT_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(line, ensure_ascii=False) + "\n")


def save_operation_result(result: OperationResult) -> OperationResult:
    write_json(LAST_RESULT_PATH, asdict(result))
    append_event(result.operation, "result", asdict(result))
    return result


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "track"


def track_stem_from_wav(wav_path: Path) -> str:
    return wav_path.stem or DEFAULT_TRACK_STEM


def build_artifacts(wav_path: Path | str | None = None) -> dict:
    wav = Path(wav_path or DEFAULT_WAV).expanduser()
    track_stem = track_stem_from_wav(wav)
    is_default = track_stem == DEFAULT_TRACK_STEM
    render_stem = DEFAULT_RENDER_STEM if is_default else f"spaziotempo_{slugify(track_stem)}"
    frame_prefix = DEFAULT_FRAME_PREFIX if is_default else f"{slugify(track_stem)}_"

    return {
        "track_stem": track_stem,
        "audio_path": str(wav),
        "output_dir": str(OUTPUT_DIR),
        "analysis_json": str(OUTPUT_DIR / f"{track_stem}_analysis.json"),
        "analysis_plot_png": str(OUTPUT_DIR / f"{track_stem}_analysis.png"),
        "blender_keyframes_json": str(OUTPUT_DIR / f"{track_stem}_analysis_blender_keyframes.json"),
        "track_summary_json": str(OUTPUT_DIR / f"{track_stem}_track_summary.json"),
        "music_context_json": str(OUTPUT_DIR / f"{track_stem}_music_context.json"),
        "analysis_ai_context_json": str(OUTPUT_DIR / f"{track_stem}_analysis_ai_context.json"),
        "dual_ai_plan_json": str(OUTPUT_DIR / f"{track_stem}_dual_ai_scene_plan.json"),
        "ollama_music_insights_json": str(OUTPUT_DIR / f"{track_stem}_ollama_music_insights.json"),
        "ai_implementation_draft_json": str(OUTPUT_DIR / f"{track_stem}_ai_implementation_draft.json"),
        "gpu_task_packet_json": str(OUTPUT_DIR / f"{track_stem}_gpu_task_packet.json"),
        "scene_brief_json": str(OUTPUT_DIR / f"{track_stem}_scene_brief.json"),
        "asset_inventory_json": str(OUTPUT_DIR / "spaziotempo_asset_inventory.json"),
        "generated_scene_script": str(INDEX_AI_DIR / "scene_scripts" / f"{slugify(track_stem)}_scene_builder_candidate.py"),
        "render_mp4": str(RENDERS_DIR / f"{render_stem}.mp4"),
        "render_ffmpeg_mp4": str(RENDERS_DIR / f"{render_stem}_ffmpeg.mp4"),
        "render_frames_dir": str(RENDERS_DIR / f"{render_stem}_frames"),
        "render_frame_prefix": frame_prefix,
    }


@dataclass
class WorkflowSession:
    version: int
    updated_at: str
    use_session_track: bool
    debug_enabled: bool
    current_wav: str
    track_stem: str
    artifacts: dict
    creative_model: str = DEFAULT_CREATIVE_MODEL
    technical_model: str = DEFAULT_TECHNICAL_MODEL
    chat_model: str = DEFAULT_CHAT_MODEL
    script_max_tokens: int = DEFAULT_SCRIPT_TOKENS
    last_operation: str | None = None
    last_result_path: str | None = None

    @classmethod
    def default(cls) -> "WorkflowSession":
        artifacts = build_artifacts(DEFAULT_WAV)
        return cls(
            version=1,
            updated_at=now_iso(),
            use_session_track=False,
            debug_enabled=False,
            current_wav=str(DEFAULT_WAV),
            track_stem=artifacts["track_stem"],
            artifacts=artifacts,
        )

    def save(self) -> None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.updated_at = now_iso()
        SESSION_PATH.write_text(json.dumps(asdict(self), indent=2, ensure_ascii=False), encoding="utf-8")


def load_session(create: bool = True) -> WorkflowSession:
    if SESSION_PATH.exists():
        try:
            data = json.loads(SESSION_PATH.read_text(encoding="utf-8"))
            base_artifacts = build_artifacts(data.get("current_wav") or DEFAULT_WAV)
            stored_artifacts = data.get("artifacts") or {}
            artifacts = dict(base_artifacts)
            artifacts.update({key: value for key, value in stored_artifacts.items() if value is not None})
            return WorkflowSession(
                version=int(data.get("version", 1)),
                updated_at=str(data.get("updated_at") or now_iso()),
                use_session_track=bool(data.get("use_session_track", False)),
                debug_enabled=bool(data.get("debug_enabled", False)),
                current_wav=str(data.get("current_wav") or DEFAULT_WAV),
                track_stem=str(data.get("track_stem") or artifacts["track_stem"]),
                artifacts=artifacts,
                creative_model=str(data.get("creative_model") or DEFAULT_CREATIVE_MODEL),
                technical_model=str(data.get("technical_model") or DEFAULT_TECHNICAL_MODEL),
                chat_model=str(data.get("chat_model") or DEFAULT_CHAT_MODEL),
                script_max_tokens=int(data.get("script_max_tokens") or DEFAULT_SCRIPT_TOKENS),
                last_operation=data.get("last_operation"),
                last_result_path=data.get("last_result_path"),
            )
        except Exception:
            pass

    session = WorkflowSession.default()
    if create:
        session.save()
    return session


def set_current_wav(wav_path: Path | str) -> WorkflowSession:
    wav = Path(wav_path).expanduser().resolve()
    if not wav.exists():
        raise FileNotFoundError(f"WAV non trovato: {wav}")
    if wav.suffix.lower() != ".wav":
        raise ValueError(f"Serve un file .wav, ricevuto: {wav}")

    previous = load_session(create=False)
    artifacts = build_artifacts(wav)
    session = WorkflowSession(
        version=1,
        updated_at=now_iso(),
        use_session_track=True,
        debug_enabled=previous.debug_enabled,
        current_wav=str(wav),
        track_stem=artifacts["track_stem"],
        artifacts=artifacts,
        creative_model=previous.creative_model,
        technical_model=previous.technical_model,
        chat_model=previous.chat_model,
        script_max_tokens=previous.script_max_tokens,
        last_operation="set_current_wav",
    )
    session.save()
    return session


def reset_to_default_wav() -> WorkflowSession:
    previous = load_session(create=False)
    artifacts = build_artifacts(DEFAULT_WAV)
    session = WorkflowSession(
        version=1,
        updated_at=now_iso(),
        use_session_track=False,
        debug_enabled=previous.debug_enabled,
        current_wav=str(DEFAULT_WAV),
        track_stem=artifacts["track_stem"],
        artifacts=artifacts,
        creative_model=previous.creative_model,
        technical_model=previous.technical_model,
        chat_model=previous.chat_model,
        script_max_tokens=previous.script_max_tokens,
        last_operation="reset_to_default_wav",
    )
    session.save()
    return session


def set_debug_enabled(enabled: bool) -> WorkflowSession:
    session = load_session()
    session.debug_enabled = bool(enabled)
    session.last_operation = "set_debug_enabled"
    session.save()
    append_event("set_debug_enabled", "updated", {"debug_enabled": session.debug_enabled})
    return session


def available_ollama_models() -> list[str]:
    npu_path = str(NPU_DIR)
    if npu_path not in sys.path:
        sys.path.insert(0, npu_path)
    try:
        from ollama_runtime import list_models, list_models_from_disk, DEFAULT_BASE_URL

        models: list[str] = []
        try:
            models.extend(list_models(DEFAULT_BASE_URL))
        except Exception:
            pass
        models.extend(list_models_from_disk())
        return sorted(set(model for model in models if model))
    except Exception:
        return sorted({DEFAULT_CREATIVE_MODEL, DEFAULT_TECHNICAL_MODEL, DEFAULT_CHAT_MODEL})


def set_ai_models(
    *,
    creative_model: str | None = None,
    technical_model: str | None = None,
    chat_model: str | None = None,
    script_max_tokens: int | None = None,
) -> WorkflowSession:
    session = load_session()
    if creative_model:
        session.creative_model = creative_model
    if technical_model:
        session.technical_model = technical_model
    if chat_model:
        session.chat_model = chat_model
    if script_max_tokens:
        session.script_max_tokens = max(1200, int(script_max_tokens))
    session.last_operation = "set_ai_models"
    session.save()
    append_event(
        "set_ai_models",
        "updated",
        {
            "creative_model": session.creative_model,
            "technical_model": session.technical_model,
            "chat_model": session.chat_model,
            "script_max_tokens": session.script_max_tokens,
        },
    )
    return session


def python_executable() -> Path:
    if NPU_PYTHON.exists():
        result = run_command(
            [str(NPU_PYTHON), "-c", "print('ok')"],
            operation="probe_python",
            check=False,
            echo=False,
            debug=False,
            print_output=False,
            log=False,
        )
        if result.ok:
            return NPU_PYTHON
    return Path(sys.executable)


def audio_python_executable() -> Path:
    if AUDIO_PYTHON.exists():
        result = run_command(
            [str(AUDIO_PYTHON), "-c", "import librosa, numpy, matplotlib; print('audio ok')"],
            operation="probe_audio_python",
            check=False,
            echo=False,
            debug=False,
            print_output=False,
            log=False,
        )
        if result.ok:
            return AUDIO_PYTHON

    fallback = Path(sys.executable)
    result = run_command(
        [str(fallback), "-c", "import librosa, numpy, matplotlib; print('audio ok')"],
        operation="probe_audio_python_fallback",
        check=False,
        echo=False,
        debug=False,
        print_output=False,
        log=False,
    )
    if result.ok:
        return fallback

    raise RuntimeError(
        "Runtime audio non disponibile: serve un Python con librosa, numpy e matplotlib. "
        f"Atteso: {AUDIO_PYTHON}"
    )


def run_command(
    command: list[str],
    operation: str = "command",
    check: bool = True,
    echo: bool = True,
    debug: bool | None = None,
    print_output: bool = True,
    metadata: dict | None = None,
    log: bool = True,
) -> OperationResult:
    session_debug = load_session(create=False).debug_enabled if debug is None else debug
    started_at = now_iso()
    start = time.perf_counter()
    cwd = str(PROJECT_DIR)
    metadata = metadata or {}

    if log:
        append_event(
            operation,
            "start",
            {
                "command": command,
                "cwd": cwd,
                "metadata": metadata,
                "debug": session_debug,
            },
        )

    if echo:
        print("\n$ " + " ".join(f'"{part}"' if " " in part else part for part in command))
    if session_debug:
        print(f"[DEBUG] operation={operation}")
        print(f"[DEBUG] cwd={cwd}")
        print(f"[DEBUG] metadata={json.dumps(metadata, ensure_ascii=False)}")

    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout or ""
    if output and print_output:
        print(output.rstrip())

    ended_at = now_iso()
    op_result = OperationResult(
        operation=operation,
        ok=result.returncode == 0,
        started_at=started_at,
        ended_at=ended_at,
        elapsed_sec=round(time.perf_counter() - start, 4),
        command=command,
        cwd=cwd,
        returncode=result.returncode,
        stdout_tail=output[-8000:],
        metadata=metadata,
    )

    if log:
        save_operation_result(op_result)

    if session_debug:
        print(f"[DEBUG] returncode={result.returncode}")
        print(f"[DEBUG] elapsed_sec={op_result.elapsed_sec}")
        print(f"[DEBUG] last_result={LAST_RESULT_PATH}")
        print(f"[DEBUG] event_log={EVENT_LOG_PATH}")

    if check and result.returncode != 0:
        op_result.error = f"Comando fallito con exit code {result.returncode}"
        if log:
            save_operation_result(op_result)
        raise RuntimeError(op_result.error)

    return op_result


def finish_session_operation(session: WorkflowSession, operation: str) -> None:
    session.last_operation = operation
    session.last_result_path = str(LAST_RESULT_PATH)
    session.save()


def path_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def is_safe_intermediate_target(path: Path) -> bool:
    allowed = path_within(path, OUTPUT_DIR) or path_within(path, NPU_DIR) or path_within(path, INDEX_AI_DIR)
    forbidden = (
        path_within(path, AUDIO_DIR)
        or path_within(path, RENDERS_DIR)
        or path == PROJECT_DIR
        or path == ROOT
    )
    return allowed and not forbidden


def cleanup_intermediate_targets(session: WorkflowSession, include_all_tracks: bool = True, include_logs: bool = True) -> dict:
    file_targets: set[Path] = set()
    dir_targets: set[Path] = set()

    artifact_keys = [
        "analysis_json",
        "analysis_plot_png",
        "blender_keyframes_json",
        "track_summary_json",
        "music_context_json",
        "analysis_ai_context_json",
        "dual_ai_plan_json",
        "ollama_music_insights_json",
        "ai_implementation_draft_json",
        "gpu_task_packet_json",
        "scene_brief_json",
        "asset_inventory_json",
        "generated_scene_script",
    ]
    for key in artifact_keys:
        value = session.artifacts.get(key)
        if value:
            file_targets.add(Path(value))

    if include_all_tracks and OUTPUT_DIR.exists():
        patterns = [
            "*_analysis.json",
            "*_analysis.png",
            "*_analysis_blender_keyframes.json",
            "*_track_summary.json",
            "*_music_context.json",
            "*_analysis_ai_context.json",
            "*_dual_ai_scene_plan.json",
            "*_ollama_music_insights.json",
            "*_ai_implementation_draft.json",
            "*_gpu_task_packet.json",
            "*_scene_brief.json",
        ]
        for pattern in patterns:
            file_targets.update(path for path in OUTPUT_DIR.glob(pattern) if path.is_file())

    npu_files = [
        "npu_code_context.md",
        "npu_code_index.md",
        "npu_code_manifest.json",
        "npu_context_for_aider.md",
        "npu_chunk_notes.md",
        "npu_music_context.md",
        "npu_music_manifest.json",
        "npu_music_context_for_aider.md",
        "npu_music_chunk_notes.md",
        "npu_dual_ai_technical_notes.md",
        "npu_dual_ai_implementation_notes.md",
        "npu_dual_ai_chunk_notes.md",
        "dual_ai_blender_agent_brief.md",
        "ollama_music_insights.md",
        "npu_preflight_report.json",
        "npu_smoke_chunk_notes.md",
        "npu_smoke_context_for_aider.md",
        "generated_blender_script_candidate.py",
        "generated_implementation_notes.md",
    ]
    file_targets.update(NPU_DIR / name for name in npu_files)

    slug = slugify(session.track_stem)
    generated_ai_files = [
        INDEX_AI_DIR / "scene_scripts" / f"{slug}_scene_builder_candidate.py",
        INDEX_AI_DIR / "patch_library" / f"{slug}_npu_service_capsule.json",
        INDEX_AI_DIR / "patch_library" / f"{slug}_npu_service_capsule.md",
        INDEX_AI_DIR / "patch_library" / f"{slug}_gpu_task_packet.json",
    ]
    file_targets.update(generated_ai_files)
    if include_all_tracks:
        for pattern in [
            "*_scene_builder_candidate.py",
            "*_npu_service_capsule.json",
            "*_npu_service_capsule.md",
            "*_gpu_task_packet.json",
        ]:
            file_targets.update(path for path in INDEX_AI_DIR.glob(f"**/{pattern}") if path.is_file())

    npu_dirs = [
        "npu_code_chunks",
        "npu_music_chunks",
    ]
    dir_targets.update(NPU_DIR / name for name in npu_dirs)

    if include_logs:
        dir_targets.add(LOG_DIR)

    existing_files = sorted(
        {
            path.resolve(strict=False)
            for path in file_targets
            if path.exists() and path.is_file() and is_safe_intermediate_target(path)
        },
        key=lambda item: str(item).lower(),
    )
    existing_dirs = sorted(
        {
            path.resolve(strict=False)
            for path in dir_targets
            if path.exists() and path.is_dir() and is_safe_intermediate_target(path)
        },
        key=lambda item: len(str(item)),
        reverse=True,
    )

    return {
        "files": [str(path) for path in existing_files],
        "dirs": [str(path) for path in existing_dirs],
        "protected_roots": [str(AUDIO_DIR), str(RENDERS_DIR)],
    }


def cleanup_render_frame_targets(session: WorkflowSession) -> dict:
    frame_dir = Path(session.artifacts.get("render_frames_dir", ""))
    targets = []
    if frame_dir.exists() and frame_dir.is_dir() and path_within(frame_dir, RENDERS_DIR):
        targets.append(str(frame_dir.resolve(strict=False)))

    return {
        "files": [],
        "dirs": targets,
        "protected_roots": [str(AUDIO_DIR)],
        "preserved_video_outputs": [
            session.artifacts.get("render_mp4"),
            session.artifacts.get("render_ffmpeg_mp4"),
        ],
    }


def delete_target_set(operation: str, targets: dict, session: WorkflowSession) -> OperationResult:
    started_at = now_iso()
    start = time.perf_counter()
    deleted: list[str] = []
    errors: list[str] = []

    append_event(operation, "start", {"targets": targets})

    for file_name in targets.get("files", []):
        path = Path(file_name)
        try:
            if path.exists() and is_safe_intermediate_target(path):
                path.unlink()
                deleted.append(str(path))
        except Exception as exc:
            errors.append(f"{path}: {exc}")

    for dir_name in targets.get("dirs", []):
        path = Path(dir_name)
        try:
            allowed = is_safe_intermediate_target(path) or path_within(path, RENDERS_DIR)
            if path.exists() and allowed and not path_within(path, AUDIO_DIR):
                shutil.rmtree(path)
                deleted.append(str(path))
        except Exception as exc:
            errors.append(f"{path}: {exc}")

    result = OperationResult(
        operation=operation,
        ok=not errors,
        started_at=started_at,
        ended_at=now_iso(),
        elapsed_sec=round(time.perf_counter() - start, 4),
        command=None,
        cwd=str(PROJECT_DIR),
        returncode=0 if not errors else 1,
        stdout_tail="\n".join(deleted[-200:]),
        error="\n".join(errors) if errors else None,
        metadata={
            "deleted_count": len(deleted),
            "deleted": deleted,
            "errors": errors,
            "targets": targets,
        },
    )
    save_operation_result(result)
    finish_session_operation(session, operation)
    return result


def human_bytes(size: int | float) -> str:
    value = float(size or 0)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024.0 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024.0
    return f"{value:.1f} TB"


def scan_path_stats(path: Path) -> dict:
    path = Path(path)
    stats = {
        "path": str(path),
        "exists": path.exists(),
        "bytes": 0,
        "files": 0,
        "dirs": 0,
        "errors": [],
    }
    if not stats["exists"]:
        return stats

    try:
        if path.is_file():
            stats["bytes"] = path.stat().st_size
            stats["files"] = 1
            return stats
    except OSError as exc:
        stats["errors"].append(f"{path}: {exc}")
        return stats

    stack = [path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            stats["dirs"] += 1
                            stack.append(Path(entry.path))
                        elif entry.is_file(follow_symlinks=False):
                            stats["files"] += 1
                            stats["bytes"] += entry.stat(follow_symlinks=False).st_size
                    except OSError as exc:
                        stats["errors"].append(f"{entry.path}: {exc}")
        except OSError as exc:
            stats["errors"].append(f"{current}: {exc}")
    return stats


def collect_matching_files(root: Path, patterns: list[str]) -> list[Path]:
    if not root.exists():
        return []
    found: set[Path] = set()
    for pattern in patterns:
        found.update(path for path in root.glob(pattern) if path.is_file())
    return sorted(found, key=lambda item: str(item).lower())


def file_set_stats(name: str, paths: list[Path]) -> dict:
    total = 0
    existing: list[str] = []
    for path in paths:
        try:
            if path.exists() and path.is_file():
                total += path.stat().st_size
                existing.append(str(path))
        except OSError:
            pass
    return {
        "name": name,
        "path": "<file set>",
        "exists": bool(existing),
        "bytes": total,
        "files": len(existing),
        "dirs": 0,
        "errors": [],
        "sample_files": existing[:12],
    }


def build_project_storage_stats(session: WorkflowSession) -> dict:
    scene_scripts_dir = INDEX_AI_DIR / "scene_scripts"
    patch_library_dir = INDEX_AI_DIR / "patch_library"
    manual_dir = ROOT / "manual"
    frame_dir = Path(session.artifacts.get("render_frames_dir", ""))
    venvs_dir = ROOT / "venvs"

    sections = [
        ("Workspace root", ROOT),
        ("Project total", PROJECT_DIR),
        ("Output/intermedi", OUTPUT_DIR),
        ("Workflow logs", LOG_DIR),
        ("indexAI total", INDEX_AI_DIR),
        ("Generated scene scripts", scene_scripts_dir),
        ("AI patch/service library", patch_library_dir),
        ("Manual library", manual_dir),
        ("Tools NPU/workflow", TOOLS_DIR),
        ("Renders total", RENDERS_DIR),
        ("Current frame render dir", frame_dir),
        ("Audio library", AUDIO_DIR),
        ("Python venvs", venvs_dir),
    ]

    section_stats = []
    for name, path in sections:
        item = scan_path_stats(path)
        item["name"] = name
        section_stats.append(item)

    ai_chat_files = collect_matching_files(
        OUTPUT_DIR,
        [
            "*_scene_brief.json",
            "*_dual_ai_scene_plan.json",
            "*_ai_implementation_draft.json",
            "*_gpu_task_packet.json",
            "workflow_logs/*.json",
            "workflow_logs/*.jsonl",
        ],
    )
    generated_ai_files = collect_matching_files(
        INDEX_AI_DIR,
        [
            "scene_scripts/*_scene_builder_candidate.py",
            "scene_scripts/**/*",
            "patch_library/*_npu_service_capsule.json",
            "patch_library/*_npu_service_capsule.md",
            "patch_library/*_gpu_task_packet.json",
        ],
    )

    artifact_stats = [
        file_set_stats("AI chats/briefs/logs", ai_chat_files),
        file_set_stats("Generated AI scripts/bundles", generated_ai_files),
    ]

    current_artifacts = []
    for key, value in session.artifacts.items():
        path = Path(value) if isinstance(value, str) else None
        if path and path.suffix:
            current_artifacts.append({
                "key": key,
                "path": str(path),
                "exists": path.exists(),
                "bytes": path.stat().st_size if path.exists() and path.is_file() else 0,
            })

    return {
        "generated_at": now_iso(),
        "track_stem": session.track_stem,
        "audio_path": session.artifacts.get("audio_path"),
        "sections": section_stats,
        "artifact_sets": artifact_stats,
        "current_artifacts": current_artifacts,
        "notes": [
            "GPU 0 / iGPU can be considered for Intel/OpenVINO service tasks when supported by drivers/runtime.",
            "NVIDIA GPU should stay reserved for Blender/Ollama/render-heavy work when possible.",
        ],
    }


def format_project_storage_stats(stats: dict) -> str:
    lines = [
        "=" * 78,
        "SPAZIOTEMPO PROJECT STORAGE STATS",
        "=" * 78,
        f"Generated: {stats.get('generated_at')}",
        f"Track:     {stats.get('track_stem')}",
        f"Audio:     {stats.get('audio_path')}",
        "",
        "Main Areas:",
    ]
    for item in stats.get("sections", []):
        mark = "OK" if item.get("exists") else "MISSING"
        lines.append(
            f"  [{mark}] {item.get('name')}: {human_bytes(item.get('bytes', 0))} | "
            f"files={item.get('files', 0)} dirs={item.get('dirs', 0)}"
        )
        lines.append(f"       {item.get('path')}")
        if item.get("errors"):
            lines.append(f"       errors={len(item.get('errors', []))}")

    lines.append("")
    lines.append("AI / Chat / Generated Artifacts:")
    for item in stats.get("artifact_sets", []):
        lines.append(
            f"  {item.get('name')}: {human_bytes(item.get('bytes', 0))} | files={item.get('files', 0)}"
        )
        for sample in item.get("sample_files", [])[:8]:
            lines.append(f"       {sample}")
        if item.get("files", 0) > 8:
            lines.append(f"       ... altri {item.get('files', 0) - 8} file")

    lines.append("")
    lines.append("Current Track Artifacts:")
    for item in stats.get("current_artifacts", []):
        mark = "OK" if item.get("exists") else "--"
        lines.append(f"  [{mark}] {item.get('key')}: {human_bytes(item.get('bytes', 0))}")
        lines.append(f"       {item.get('path')}")

    lines.append("")
    lines.append("Notes:")
    for note in stats.get("notes", []):
        lines.append(f"  - {note}")
    return "\n".join(lines)


def cleanup_intermediates(session: WorkflowSession, include_all_tracks: bool = True, include_logs: bool = True) -> OperationResult:
    targets = cleanup_intermediate_targets(session, include_all_tracks=include_all_tracks, include_logs=include_logs)
    targets["preserved"] = {
        "audio_dir": str(AUDIO_DIR),
        "renders_dir": str(RENDERS_DIR),
        "current_audio": session.artifacts.get("audio_path"),
        "render_mp4": session.artifacts.get("render_mp4"),
        "render_ffmpeg_mp4": session.artifacts.get("render_ffmpeg_mp4"),
        "render_frames_dir": session.artifacts.get("render_frames_dir"),
    }
    return delete_target_set("cleanup_intermediates", targets, session)


def cleanup_render_frames(session: WorkflowSession) -> OperationResult:
    targets = cleanup_render_frame_targets(session)
    return delete_target_set("cleanup_render_frames", targets, session)


def operation_status(session: WorkflowSession) -> dict:
    artifacts = session.artifacts
    checks = {
        "audio_path": bool(artifacts.get("audio_path")) and Path(artifacts["audio_path"]).exists(),
        "analysis_json": bool(artifacts.get("analysis_json")) and Path(artifacts["analysis_json"]).exists(),
        "track_summary_json": bool(artifacts.get("track_summary_json")) and Path(artifacts["track_summary_json"]).exists(),
        "music_context_json": bool(artifacts.get("music_context_json")) and Path(artifacts["music_context_json"]).exists(),
        "analysis_ai_context_json": bool(artifacts.get("analysis_ai_context_json")) and Path(artifacts["analysis_ai_context_json"]).exists(),
        "blender_keyframes_json": bool(artifacts.get("blender_keyframes_json")) and Path(artifacts["blender_keyframes_json"]).exists(),
        "dual_ai_plan_json": bool(artifacts.get("dual_ai_plan_json")) and Path(artifacts["dual_ai_plan_json"]).exists(),
        "scene_brief_json": bool(artifacts.get("scene_brief_json")) and Path(artifacts["scene_brief_json"]).exists(),
        "asset_inventory_json": bool(artifacts.get("asset_inventory_json")) and Path(artifacts["asset_inventory_json"]).exists(),
        "ai_implementation_draft_json": bool(artifacts.get("ai_implementation_draft_json")) and Path(artifacts["ai_implementation_draft_json"]).exists(),
        "generated_scene_script": bool(artifacts.get("generated_scene_script")) and Path(artifacts["generated_scene_script"]).exists(),
    }
    return checks


def run_analyze_wav(session: WorkflowSession, fps: float = 30.0, skip_music_context: bool = False) -> None:
    py = audio_python_executable()
    args = [
        str(py),
        str(PROJECT_DIR / "analyze_wav.py"),
        session.artifacts["audio_path"],
        "--output-dir",
        session.artifacts["output_dir"],
        "--fps",
        str(fps),
    ]
    if skip_music_context:
        args.append("--skip-music-context")
    run_command(args, operation="analyze_wav", metadata={"track_stem": session.track_stem, "fps": fps})
    finish_session_operation(session, "analyze_wav")


def run_track_summary(session: WorkflowSession) -> None:
    py = python_executable()
    run_command(
        [
            str(py),
            str(PROJECT_DIR / "build_track_summary.py"),
            "--analysis-json",
            session.artifacts["analysis_json"],
            "--out-json",
            session.artifacts["track_summary_json"],
            "--skip-music-context",
        ],
        operation="build_track_summary",
        metadata={"track_stem": session.track_stem},
    )
    finish_session_operation(session, "build_track_summary")


def run_music_context(session: WorkflowSession, include_ollama: bool = False, ollama_model: str = "qwen2.5-coder:14b") -> None:
    py = python_executable()
    args = [
        str(py),
        str(NPU_DIR / "build_music_context.py"),
        "--analysis",
        session.artifacts["analysis_json"],
        "--track-summary",
        session.artifacts["track_summary_json"],
        "--compact-json",
        session.artifacts["music_context_json"],
        "--analysis-ai-context",
        session.artifacts["analysis_ai_context_json"],
        "--blender-keyframes-json",
        session.artifacts["blender_keyframes_json"],
    ]
    if include_ollama:
        args.extend(["--run-ollama", "--ollama-model", ollama_model])
    run_command(args, operation="build_music_context", metadata={"track_stem": session.track_stem})
    finish_session_operation(session, "build_music_context")


def run_code_context(session: WorkflowSession) -> None:
    py = python_executable()
    run_command([str(py), str(NPU_DIR / "build_npu_code_context.py")], operation="build_code_context")
    run_project_ai_index(session)
    finish_session_operation(session, "build_code_context")


def run_project_ai_index(session: WorkflowSession, force: bool = False) -> None:
    py = python_executable()
    args = [str(py), str(NPU_DIR / "build_project_ai_index.py")]
    if force:
        args.append("--force")
    run_command(args, operation="build_project_ai_index", metadata={"force": force})
    finish_session_operation(session, "build_project_ai_index")


def run_asset_inventory(session: WorkflowSession) -> dict:
    from asset_inventory import build_asset_inventory

    output_json = Path(session.artifacts["asset_inventory_json"])
    output_md = INDEX_AI_DIR / "asset_inventory.md"
    inventory = build_asset_inventory(ROOT, PROJECT_DIR, output_json, output_md)
    append_event(
        "build_asset_inventory",
        "result",
        {
            "asset_count": inventory.get("asset_count"),
            "output_json": str(output_json),
            "output_md": str(output_md),
        },
    )
    return inventory


def run_scene_director_brief(session: WorkflowSession) -> OperationResult:
    from scene_brief import run_interactive_scene_brief

    started_at = now_iso()
    start = time.perf_counter()
    append_event("scene_director_brief", "start", {"track_stem": session.track_stem})
    output_path = Path(session.artifacts["scene_brief_json"])
    brief = run_interactive_scene_brief(
        track_stem=session.track_stem,
        audio_path=session.artifacts["audio_path"],
        output_path=output_path,
    )
    result = OperationResult(
        operation="scene_director_brief",
        ok=True,
        started_at=started_at,
        ended_at=now_iso(),
        elapsed_sec=round(time.perf_counter() - start, 4),
        command=None,
        cwd=str(PROJECT_DIR),
        returncode=0,
        stdout_tail=f"Wrote {output_path}",
        metadata={
            "track_stem": session.track_stem,
            "scene_brief_json": str(output_path),
            "field_count": len(brief.get("scene_preferences", {})),
        },
    )
    save_operation_result(result)
    finish_session_operation(session, "scene_director_brief")
    return result


def run_manual_index(session: WorkflowSession, limit_files: int = 80) -> None:
    py = python_executable()
    run_command(
        [str(py), str(NPU_DIR / "build_blender_manual_context.py"), "--limit-files", str(limit_files)],
        operation="build_manual_context",
        metadata={"limit_files": limit_files},
    )
    finish_session_operation(session, "build_manual_context")


def ensure_manual_library(session: WorkflowSession) -> None:
    py = python_executable()
    run_command([str(py), str(NPU_DIR / "build_blender_manual_context.py"), "--ensure-only"], operation="ensure_manual_library")
    finish_session_operation(session, "ensure_manual_library")


def artifact_missing(session: WorkflowSession, key: str) -> bool:
    value = session.artifacts.get(key)
    return not value or not Path(value).exists()


def ensure_ai_prerequisites(session: WorkflowSession, phase: str, include_manual: bool = False) -> None:
    if artifact_missing(session, "analysis_json") or artifact_missing(session, "blender_keyframes_json"):
        raise RuntimeError("Manca l'analisi WAV completa: esegui prima 3 Analizza WAV.")

    if artifact_missing(session, "track_summary_json"):
        print("[AUTO] Track summary mancante: lo genero ora.")
        run_track_summary(session)

    if (
        artifact_missing(session, "music_context_json")
        or artifact_missing(session, "analysis_ai_context_json")
        or artifact_missing(session, "blender_keyframes_json")
    ):
        print("[AUTO] Music context mancante o incompleto: lo genero ora.")
        run_music_context(session)

    project_index = INDEX_AI_DIR / "project_code_index.md"
    project_manifest = INDEX_AI_DIR / "project_code_manifest.json"
    if not project_index.exists() or not project_manifest.exists():
        print("[AUTO] indexAI project index mancante: lo genero ora.")
        run_project_ai_index(session)

    if include_manual:
        ensure_manual_library(session)

    run_asset_inventory(session)

    if phase == "implementation" and artifact_missing(session, "dual_ai_plan_json"):
        raise RuntimeError("Manca il piano Dual AI: esegui prima 9 Dual AI plan.")


def run_dual_ai(
    session: WorkflowSession,
    phase: str = "plan",
    include_manual: bool = False,
    skip_npu: bool = True,
    skip_ollama: bool = False,
    creative_model: str | None = None,
    technical_model: str | None = None,
    max_new_tokens: int | None = None,
) -> None:
    ensure_ai_prerequisites(session, phase=phase, include_manual=include_manual)
    creative_model = creative_model or session.creative_model or DEFAULT_CREATIVE_MODEL
    technical_model = technical_model or session.technical_model or DEFAULT_TECHNICAL_MODEL
    max_new_tokens = max_new_tokens or session.script_max_tokens or DEFAULT_SCRIPT_TOKENS
    py = python_executable()
    args = [
        str(py),
        str(NPU_DIR / "run_dual_ai_pipeline.py"),
        "--phase",
        phase,
        "--track-stem",
        session.track_stem,
        "--analysis",
        session.artifacts["analysis_json"],
        "--track-summary",
        session.artifacts["track_summary_json"],
        "--compact-json",
        session.artifacts["music_context_json"],
        "--analysis-ai-context",
        session.artifacts["analysis_ai_context_json"],
        "--blender-keyframes-json",
        session.artifacts["blender_keyframes_json"],
        "--creative-model",
        creative_model,
        "--technical-model",
        technical_model,
        "--npu-python",
        str(NPU_PYTHON),
        "--max-new-tokens",
        str(max_new_tokens),
    ]
    if include_manual:
        args.append("--include-manual")
    if skip_npu:
        args.append("--skip-npu")
    if skip_ollama:
        args.append("--skip-ollama")
    scene_brief = Path(session.artifacts.get("scene_brief_json", ""))
    if scene_brief.exists():
        args.extend(["--scene-brief", str(scene_brief)])
    asset_inventory = Path(session.artifacts.get("asset_inventory_json", ""))
    if asset_inventory.exists():
        args.extend(["--asset-inventory", str(asset_inventory)])
    run_command(
        args,
        operation=f"dual_ai_{phase}",
        metadata={
            "track_stem": session.track_stem,
            "include_manual": include_manual,
            "skip_npu": skip_npu,
            "skip_ollama": skip_ollama,
            "creative_model": creative_model,
            "technical_model": technical_model,
            "max_new_tokens": max_new_tokens,
            "project_index": str(INDEX_AI_DIR / "project_code_index.md"),
        },
    )
    finish_session_operation(session, f"dual_ai_{phase}")


def run_full_audio_prepare(session: WorkflowSession) -> None:
    run_analyze_wav(session, skip_music_context=True)
    run_track_summary(session)
    run_music_context(session)
    run_code_context(session)
    ensure_manual_library(session)
    finish_session_operation(session, "full_audio_prepare")


def run_advanced_debug_check(probe_write: bool = True) -> str:
    from workflow_debug import build_debug_report, format_debug_report

    report = build_debug_report(probe_write=probe_write)
    return format_debug_report(report)


def run_startup_service_check() -> str:
    from startup_check import build_report, format_report, save_report

    report = build_report(PROJECT_DIR, ROOT)
    save_report(report)
    return format_report(report)


def _powershell_quote(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def open_debug_monitor_window(interval: float = 3.0, probe_write: bool = True) -> subprocess.Popen:
    py = NPU_PYTHON if NPU_PYTHON.exists() else Path(sys.executable)
    script = Path(__file__).with_name("workflow_debug.py")
    args = [
        _powershell_quote(py),
        _powershell_quote(script),
        "--watch",
        "--interval",
        str(max(1.0, interval)),
    ]
    if not probe_write:
        args.append("--no-write-probe")
    command_text = "& " + " ".join(args)
    command = [
        "powershell",
        "-NoExit",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        command_text,
    ]
    creationflags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    process = subprocess.Popen(command, cwd=str(PROJECT_DIR), creationflags=creationflags)
    append_event(
        "debug_monitor",
        "opened",
        {
            "pid": process.pid,
            "interval": interval,
            "probe_write": probe_write,
            "script": str(script),
        },
    )
    return process


def mark_active_operation_interrupted(reason: str = "manual interrupt") -> OperationResult:
    from workflow_debug import detect_active_operation, read_events

    session = load_session(create=True)
    active = detect_active_operation(read_events())
    operation = active.get("operation") or session.last_operation or "unknown_operation"
    result = OperationResult(
        operation=str(operation),
        ok=False,
        started_at=str(active.get("started_at") or now_iso()),
        ended_at=now_iso(),
        elapsed_sec=round(float(active.get("elapsed_sec") or 0.0), 4),
        command=(active.get("payload") or {}).get("command"),
        cwd=str(PROJECT_DIR),
        returncode=130,
        stdout_tail="",
        error=reason,
        metadata={"marked_interrupted": True, "reason": reason},
    )
    save_operation_result(result)
    finish_session_operation(session, f"{operation}_interrupted")
    return result


def available_operations() -> list[dict]:
    return [
        {"id": "set_wav", "label": "Scegli WAV", "gui_ready": True, "heavy": False},
        {"id": "reset_wav", "label": "Ripristina WAV default", "gui_ready": True, "heavy": False},
        {"id": "analyze_wav", "label": "Analizza WAV", "gui_ready": True, "heavy": True},
        {"id": "build_track_summary", "label": "Crea track summary", "gui_ready": True, "heavy": False},
        {"id": "build_music_context", "label": "Crea/aggiorna music context", "gui_ready": True, "heavy": False},
        {"id": "build_code_context", "label": "Crea/aggiorna code context + indexAI", "gui_ready": True, "heavy": False},
        {"id": "build_project_ai_index", "label": "Rigenera indexAI progetto", "gui_ready": True, "heavy": False},
        {"id": "full_audio_prepare", "label": "Prepara audio completo", "gui_ready": True, "heavy": True},
        {"id": "build_manual_context", "label": "Indicizza manuali locali", "gui_ready": True, "heavy": True},
        {"id": "dual_ai_plan", "label": "Dual AI plan", "gui_ready": True, "heavy": True},
        {"id": "dual_ai_implementation", "label": "Dual AI scene script draft", "gui_ready": True, "heavy": True},
        {"id": "cleanup_intermediates", "label": "Pulisci intermedi", "gui_ready": True, "heavy": False},
        {"id": "cleanup_render_frames", "label": "Pulisci frame render", "gui_ready": True, "heavy": False},
        {"id": "advanced_debug_check", "label": "Debug advanced check", "gui_ready": True, "heavy": False},
        {"id": "startup_service_check", "label": "Startup service check", "gui_ready": True, "heavy": False},
        {"id": "debug_monitor_window", "label": "Apri debug monitor", "gui_ready": True, "heavy": False},
        {"id": "mark_interrupted", "label": "Registra operazione interrotta", "gui_ready": True, "heavy": False},
    ]
