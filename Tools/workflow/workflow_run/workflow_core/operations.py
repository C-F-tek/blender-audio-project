"""Workflow operation runners."""

from __future__ import annotations

import time
from pathlib import Path

from .process import audio_python_executable, finish_session_operation, python_executable, run_command
from .state import (
    DEFAULT_CREATIVE_MODEL,
    DEFAULT_SCRIPT_TOKENS,
    DEFAULT_TECHNICAL_MODEL,
    INDEX_AI_DIR,
    NPU_PYTHON,
    PROJECT_DIR,
    ROOT,
    OperationResult,
    WorkflowSession,
    append_event,
    now_iso,
    save_operation_result,
)


def run_analyze_wav(
    session: WorkflowSession,
    fps: float = 30.0,
    skip_music_context: bool = False,
) -> None:
    py = audio_python_executable()
    args = [
        str(py),
        "-m",
        "Tools.workflow",
        "analyze_audio",
        session.artifacts["audio_path"],
        "--repo-root",
        str(PROJECT_DIR),
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
            "-m",
            "Tools.workflow",
            "audio_summary",
            "--repo-root",
            str(PROJECT_DIR),
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


def run_music_context(
    session: WorkflowSession,
    include_ollama: bool = False,
    ollama_model: str = "qwen2.5-coder:14b",
) -> None:
    py = python_executable()
    args = [
        str(py),
        "-m",
        "Tools.npu",
        "build_music_context",
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
    run_command([str(py), "-m", "Tools.npu", "build_npu_code_context"], operation="build_code_context")
    run_project_ai_index(session)
    finish_session_operation(session, "build_code_context")


def run_project_ai_index(session: WorkflowSession, force: bool = False) -> None:
    py = python_executable()
    args = [str(py), "-m", "Tools.npu", "build_project_ai_index"]
    if force:
        args.append("--force")
    run_command(args, operation="build_project_ai_index", metadata={"force": force})
    finish_session_operation(session, "build_project_ai_index")


def run_asset_inventory(session: WorkflowSession) -> dict:
    try:
        from Tools.workflow.workflow_run._shared.asset_inventory import build_asset_inventory
    except ImportError:
        from Tools.workflow.workflow_run._shared.asset_inventory import build_asset_inventory

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
    try:
        from Tools.workflow.workflow_run._shared.scene_brief import run_interactive_scene_brief
    except ImportError:
        from Tools.workflow.workflow_run._shared.scene_brief import run_interactive_scene_brief

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
        [str(py), "-m", "Tools.npu", "build_blender_manual_context", "--limit-files", str(limit_files)],
        operation="build_manual_context",
        metadata={"limit_files": limit_files},
    )
    finish_session_operation(session, "build_manual_context")


def ensure_manual_library(session: WorkflowSession) -> None:
    py = python_executable()
    run_command(
        [str(py), "-m", "Tools.npu", "build_blender_manual_context", "--ensure-only"],
        operation="ensure_manual_library",
    )
    finish_session_operation(session, "ensure_manual_library")


def artifact_missing(session: WorkflowSession, key: str) -> bool:
    value = session.artifacts.get(key)
    return not value or not Path(value).exists()


def ensure_ai_prerequisites(
    session: WorkflowSession,
    phase: str,
    include_manual: bool = False,
) -> None:
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
    if not (INDEX_AI_DIR / "project_code_index.md").exists() or not (
        INDEX_AI_DIR / "project_code_manifest.json"
    ).exists():
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
        "-m",
        "Tools.npu",
        "run_dual_ai_pipeline",
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
    run_command(args, operation=f"dual_ai_{phase}", metadata={"track_stem": session.track_stem})
    finish_session_operation(session, f"dual_ai_{phase}")


def run_full_audio_prepare(session: WorkflowSession) -> None:
    run_analyze_wav(session, skip_music_context=True)
    run_track_summary(session)
    run_music_context(session)
    run_code_context(session)
    ensure_manual_library(session)
    finish_session_operation(session, "full_audio_prepare")
