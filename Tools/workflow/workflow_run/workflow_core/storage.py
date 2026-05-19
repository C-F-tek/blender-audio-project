"""Storage inventory and artifact-status helpers."""

from __future__ import annotations

import os
from pathlib import Path

from .state import (
    AUDIO_DIR,
    INDEX_AI_DIR,
    LOG_DIR,
    OUTPUT_DIR,
    PROJECT_DIR,
    RENDERS_DIR,
    ROOT,
    TOOLS_DIR,
    WorkflowSession,
    now_iso,
)


def human_bytes(size: int | float) -> str:
    value = float(size or 0)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024.0 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024.0
    return f"{value:.1f} TB"


def scan_path_stats(path: Path) -> dict:
    path = Path(path)
    stats = {"path": str(path), "exists": path.exists(), "bytes": 0, "files": 0, "dirs": 0, "errors": []}
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

    current_artifacts = []
    for key, value in session.artifacts.items():
        path = Path(value) if isinstance(value, str) else None
        if path and path.suffix:
            current_artifacts.append(
                {
                    "key": key,
                    "path": str(path),
                    "exists": path.exists(),
                    "bytes": path.stat().st_size if path.exists() and path.is_file() else 0,
                }
            )

    return {
        "generated_at": now_iso(),
        "track_stem": session.track_stem,
        "audio_path": session.artifacts.get("audio_path"),
        "sections": section_stats,
        "artifact_sets": [
            file_set_stats("AI chats/briefs/logs", ai_chat_files),
            file_set_stats("Generated AI scripts/bundles", generated_ai_files),
        ],
        "current_artifacts": current_artifacts,
        "notes": [
            "GPU 0 / iGPU can be considered for Intel/OpenVINO service tasks when supported.",
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

    lines.extend(["", "AI / Chat / Generated Artifacts:"])
    for item in stats.get("artifact_sets", []):
        lines.append(
            f"  {item.get('name')}: {human_bytes(item.get('bytes', 0))} | files={item.get('files', 0)}"
        )
        for sample in item.get("sample_files", [])[:8]:
            lines.append(f"       {sample}")
        if item.get("files", 0) > 8:
            lines.append(f"       ... altri {item.get('files', 0) - 8} file")

    lines.extend(["", "Current Track Artifacts:"])
    for item in stats.get("current_artifacts", []):
        mark = "OK" if item.get("exists") else "--"
        lines.append(f"  [{mark}] {item.get('key')}: {human_bytes(item.get('bytes', 0))}")
        lines.append(f"       {item.get('path')}")

    lines.extend(["", "Notes:"])
    for note in stats.get("notes", []):
        lines.append(f"  - {note}")
    return "\n".join(lines)


def operation_status(session: WorkflowSession) -> dict:
    artifacts = session.artifacts
    checks = {
        "audio_path": bool(artifacts.get("audio_path")) and Path(artifacts["audio_path"]).exists(),
        "analysis_json": bool(artifacts.get("analysis_json"))
        and Path(artifacts["analysis_json"]).exists(),
        "track_summary_json": bool(artifacts.get("track_summary_json"))
        and Path(artifacts["track_summary_json"]).exists(),
        "music_context_json": bool(artifacts.get("music_context_json"))
        and Path(artifacts["music_context_json"]).exists(),
        "analysis_ai_context_json": bool(artifacts.get("analysis_ai_context_json"))
        and Path(artifacts["analysis_ai_context_json"]).exists(),
        "blender_keyframes_json": bool(artifacts.get("blender_keyframes_json"))
        and Path(artifacts["blender_keyframes_json"]).exists(),
        "dual_ai_plan_json": bool(artifacts.get("dual_ai_plan_json"))
        and Path(artifacts["dual_ai_plan_json"]).exists(),
        "scene_brief_json": bool(artifacts.get("scene_brief_json"))
        and Path(artifacts["scene_brief_json"]).exists(),
        "asset_inventory_json": bool(artifacts.get("asset_inventory_json"))
        and Path(artifacts["asset_inventory_json"]).exists(),
        "ai_implementation_draft_json": bool(artifacts.get("ai_implementation_draft_json"))
        and Path(artifacts["ai_implementation_draft_json"]).exists(),
        "generated_scene_script": bool(artifacts.get("generated_scene_script"))
        and Path(artifacts["generated_scene_script"]).exists(),
    }
    return checks
