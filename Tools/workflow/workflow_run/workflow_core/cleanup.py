"""Cleanup helpers for generated workflow intermediates."""

from __future__ import annotations

import shutil
import time
from pathlib import Path

from .process import finish_session_operation
from .state import (
    AUDIO_DIR,
    INDEX_AI_DIR,
    LOG_DIR,
    NPU_DIR,
    OUTPUT_DIR,
    PROJECT_DIR,
    RENDERS_DIR,
    ROOT,
    OperationResult,
    WorkflowSession,
    append_event,
    now_iso,
    save_operation_result,
    slugify,
)


def path_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def is_safe_intermediate_target(path: Path) -> bool:
    allowed = (
        path_within(path, OUTPUT_DIR)
        or path_within(path, NPU_DIR)
        or path_within(path, INDEX_AI_DIR)
    )
    forbidden = (
        path_within(path, AUDIO_DIR)
        or path_within(path, RENDERS_DIR)
        or path == PROJECT_DIR
        or path == ROOT
    )
    return allowed and not forbidden


def cleanup_intermediate_targets(
    session: WorkflowSession,
    include_all_tracks: bool = True,
    include_logs: bool = True,
) -> dict:
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
        "context_artifacts/npu_code_context.md",
        "context_artifacts/npu_code_index.md",
        "context_artifacts/npu_code_manifest.json",
        "npu_context_for_aider.md",
        "npu_chunk_notes.md",
        "context_artifacts/npu_music_context.md",
        "context_artifacts/npu_music_manifest.json",
        "npu_music_context_for_aider.md",
        "npu_music_chunk_notes.md",
        "context_artifacts/npu_dual_ai_technical_notes.md",
        "npu_dual_ai_implementation_notes.md",
        "npu_dual_ai_chunk_notes.md",
        "context_artifacts/dual_ai_blender_agent_brief.md",
        "context_artifacts/ollama_music_insights.md",
        "npu_preflight_report.json",
        "npu_smoke_chunk_notes.md",
        "npu_smoke_context_for_aider.md",
        "context_artifacts/generated_implementation_notes.md",
    ]
    file_targets.update(NPU_DIR / name for name in npu_files)

    slug = slugify(session.track_stem)
    file_targets.update(
        [
            INDEX_AI_DIR / "scene_scripts" / f"{slug}_scene_builder_candidate.py",
            INDEX_AI_DIR / "patch_library" / f"{slug}_npu_service_capsule.json",
            INDEX_AI_DIR / "patch_library" / f"{slug}_npu_service_capsule.md",
            INDEX_AI_DIR / "patch_library" / f"{slug}_gpu_task_packet.json",
        ]
    )
    if include_all_tracks:
        for pattern in [
            "*_scene_builder_candidate.py",
            "*_npu_service_capsule.json",
            "*_npu_service_capsule.md",
            "*_gpu_task_packet.json",
        ]:
            file_targets.update(
                path for path in INDEX_AI_DIR.glob(f"**/{pattern}") if path.is_file()
            )

    dir_targets.update([NPU_DIR / "npu_code_chunks", NPU_DIR / "npu_music_chunks"])
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
        cwd=str(PROJECT_DIR),
        returncode=0 if not errors else 1,
        stdout_tail="\n".join(deleted[-200:]),
        error="\n".join(errors) if errors else None,
        metadata={"deleted_count": len(deleted), "deleted": deleted, "errors": errors},
    )
    save_operation_result(result)
    finish_session_operation(session, operation)
    return result


def cleanup_intermediates(
    session: WorkflowSession,
    include_all_tracks: bool = True,
    include_logs: bool = True,
) -> OperationResult:
    targets = cleanup_intermediate_targets(
        session,
        include_all_tracks=include_all_tracks,
        include_logs=include_logs,
    )
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
    return delete_target_set("cleanup_render_frames", cleanup_render_frame_targets(session), session)
