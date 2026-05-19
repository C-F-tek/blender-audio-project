"""Workflow paths, session state, and operation result persistence."""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(
    os.environ.get("IA_CARMINE_PROJECT_DIR", Path(__file__).resolve().parents[3])
).resolve()
ROOT = Path(os.environ.get("IA_CARMINE_WORKSPACE_ROOT", PROJECT_DIR.parent)).resolve()
AUDIO_DIR = Path(os.environ.get("IA_CARMINE_AUDIO_DIR", ROOT / "audio")).resolve()
RENDERS_DIR = Path(os.environ.get("IA_CARMINE_RENDERS_DIR", ROOT / "renders")).resolve()
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
        "ai_implementation_draft_json": str(
            OUTPUT_DIR / f"{track_stem}_ai_implementation_draft.json"
        ),
        "gpu_task_packet_json": str(OUTPUT_DIR / f"{track_stem}_gpu_task_packet.json"),
        "scene_brief_json": str(OUTPUT_DIR / f"{track_stem}_scene_brief.json"),
        "asset_inventory_json": str(OUTPUT_DIR / "spaziotempo_asset_inventory.json"),
        "generated_scene_script": str(
            INDEX_AI_DIR / "scene_scripts" / f"{slugify(track_stem)}_scene_builder_candidate.py"
        ),
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
        SESSION_PATH.write_text(
            json.dumps(asdict(self), indent=2, ensure_ascii=False), encoding="utf-8"
        )


def load_session(create: bool = True) -> WorkflowSession:
    if SESSION_PATH.exists():
        try:
            data = json.loads(SESSION_PATH.read_text(encoding="utf-8"))
            base_artifacts = build_artifacts(data.get("current_wav") or DEFAULT_WAV)
            stored_artifacts = data.get("artifacts") or {}
            artifacts = dict(base_artifacts)
            artifacts.update(
                {key: value for key, value in stored_artifacts.items() if value is not None}
            )
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
        from Tools.npu.provider_mesh._shared.ollama_runtime import DEFAULT_BASE_URL, list_models, list_models_from_disk

        models = list_models(DEFAULT_BASE_URL) or list_models_from_disk()
    except Exception:
        models = []
    defaults = [DEFAULT_CREATIVE_MODEL, DEFAULT_TECHNICAL_MODEL, DEFAULT_CHAT_MODEL]
    out: list[str] = []
    for model in [*models, *defaults]:
        if model and model not in out:
            out.append(model)
    return out


def set_ai_models(
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
        session.script_max_tokens = int(script_max_tokens)
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
