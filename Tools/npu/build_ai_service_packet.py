from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import json
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "output"
INDEX_AI_DIR = ROOT / "indexAI"
PATCH_LIBRARY_DIR = INDEX_AI_DIR / "patch_library"
SCENE_SCRIPTS_DIR = INDEX_AI_DIR / "scene_scripts"
PROJECT_MANIFEST_JSON = INDEX_AI_DIR / "project_code_manifest.json"


def slugify(value: str, max_len: int = 72) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return slug[:max_len] or "track"


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def sha256_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return round(float(value), 4)
    except Exception:
        return default


def top_project_files(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    priority = (
        "Scripting/v61b/config.py",
        "Scripting/v61b/main_v61b.py",
        "Scripting/v61b/animation.py",
        "Scripting/v61b/materials.py",
        "Scripting/v61b/fog_dynamics.py",
        "Scripting/v61b/fog_filaments.py",
        "Scripting/v61b/physics_setup.py",
        "Scripting/v61b/render_setup.py",
        "Scripting/v61b/scene_tuning_panel.py",
        "Scripting/v61b/hot_update_scene_v61b.py",
        "Tools/workflow/workflow_state.py",
        "Tools/npu/run_dual_ai_pipeline.py",
    )
    files = {item.get("file"): item for item in manifest.get("files", []) if item.get("file")}
    selected = []
    for index, file_name in enumerate(priority, 1):
        item = files.get(file_name)
        if not item:
            continue
        selected.append(
            {
                "id": f"F{index:03d}",
                "file": file_name,
                "lines": item.get("lines"),
                "sha": str(item.get("sha256", ""))[:12],
                "role": role_for_file(file_name),
            }
        )
    return selected


def role_for_file(file_name: str) -> str:
    name = Path(file_name).name
    roles = {
        "config.py": "CFG profile/path/render/audio constants",
        "main_v61b.py": "MAIN build orchestration",
        "animation.py": "ANIM keyframes/audio driven transforms",
        "materials.py": "MAT shader/node/material setup",
        "fog_dynamics.py": "FOG audio reactive volume controls",
        "fog_filaments.py": "FOG_FILAMENT procedural fog strands",
        "physics_setup.py": "PHYS orbit/force/particle setup",
        "render_setup.py": "RENDER compositor/quality profiles",
        "scene_tuning_panel.py": "PANEL Blender UI/operators",
        "hot_update_scene_v61b.py": "HOT_UPDATE partial scene refresh",
        "workflow_state.py": "WF shell/GUI operation orchestration",
        "run_dual_ai_pipeline.py": "AI_PIPELINE NPU/GPU routing",
    }
    return roles.get(name, "PROJECT source")


def compact_segments(music_context: dict[str, Any], limit: int = 32) -> list[dict[str, Any]]:
    segments = music_context.get("segments") or []
    compact = []
    for segment in segments[:limit]:
        controls = segment.get("controls") or {}
        compact.append(
            {
                "id": f"S{int(segment.get('index', len(compact) + 1)):03d}",
                "t": [safe_float(segment.get("start_sec")), safe_float(segment.get("end_sec"))],
                "b": segment.get("dominant_band"),
                "i": segment.get("intensity"),
                "score": safe_float(segment.get("intensity_score")),
                "beats": int(segment.get("beat_count") or 0),
                "ctl": {
                    "hero": safe_float(controls.get("hero_deformation")),
                    "mat": safe_float(controls.get("material_shimmer")),
                    "fog": safe_float(controls.get("fog_motion")),
                    "emit": safe_float(controls.get("accent_emission")),
                    "cam": safe_float(controls.get("camera_pressure")),
                },
                "evt": [
                    {
                        "t": safe_float(event.get("time")),
                        "lo": safe_float(event.get("low")),
                        "mi": safe_float(event.get("mid")),
                        "hi": safe_float(event.get("high")),
                        "on": safe_float(event.get("onset")),
                        "bt": safe_float(event.get("beat")),
                    }
                    for event in (segment.get("top_events") or [])[:3]
                ],
            }
        )
    return compact


def build_ai_service_packet(
    track_stem: str,
    analysis_path: Path,
    track_summary_path: Path,
    music_context_path: Path,
    analysis_ai_context_path: Path,
    blender_keyframes_path: Path,
    dual_plan_path: Path | None = None,
    npu_notes: str = "",
    npu_status: str = "service_packet",
    scene_brief: dict[str, Any] | None = None,
    asset_inventory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    PATCH_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    slug = slugify(track_stem)

    music_context = read_json(music_context_path)
    ai_context = read_json(analysis_ai_context_path)
    track_summary = read_json(track_summary_path)
    project_manifest = read_json(PROJECT_MANIFEST_JSON)
    dual_plan = read_json(dual_plan_path) if dual_plan_path else {}
    scene_brief = scene_brief or {}
    asset_inventory = asset_inventory or {}

    meta = (ai_context.get("analysis_summary") or {}).get("meta") or {}
    overall = (ai_context.get("analysis_summary") or {}).get("overall_stats") or {}
    ai_memory_context = music_context.get("ai_memory_context") or ai_context.get("ai_memory_context") or {}
    project_awareness = ai_memory_context.get("project_awareness") or {}

    capsule = {
        "format": "SPAZIOTEMPO_AI_SERVICE_CAPSULE_V1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "routing_policy": {
            "heavy_reasoning": "GPU_OLLAMA",
            "code_generation": "GPU_OLLAMA_SCENE_SCRIPT_WRITER",
            "npu_role": "service_data_router_compact_capsule",
            "npu_heavy_generation": False,
            "full_keyframes_policy": "reference_only_never_compact_for_blender",
            "memory_policy": "Every AI call receives compact user memory, scene brief, asset inventory and project/audio chunk references.",
        },
        "track": {
            "stem": track_stem,
            "duration": safe_float(meta.get("duration_sec", track_summary.get("duration_sec"))),
            "fps": safe_float(meta.get("fps", track_summary.get("fps"))),
            "bpm": safe_float(meta.get("estimated_tempo_bpm", track_summary.get("estimated_tempo_bpm"))),
            "frames": (ai_context.get("analysis_summary") or {}).get("frame_count"),
            "segments": len(music_context.get("segments") or []),
        },
        "refs": {
            "analysis_json": str(analysis_path),
            "track_summary_json": str(track_summary_path),
            "music_context_json": str(music_context_path),
            "analysis_ai_context_json": str(analysis_ai_context_path),
            "full_blender_keyframes_json": str(blender_keyframes_path),
            "full_blender_keyframes_sha": sha256_file(blender_keyframes_path),
            "dual_plan_json": str(dual_plan_path) if dual_plan_path else "",
            "project_manifest_json": str(PROJECT_MANIFEST_JSON),
        },
        "audio_language": {
            "legend": "S{id}: t=[sec0,sec1], b=band, i=intensity, ctl={hero,mat,fog,emit,cam}, evt=top events.",
            "overall": {
                "low": safe_float((overall.get("low") or {}).get("avg")),
                "mid": safe_float((overall.get("mid") or {}).get("avg")),
                "high": safe_float((overall.get("high") or {}).get("avg")),
                "onset": safe_float((overall.get("onset") or {}).get("avg")),
                "beat": safe_float((overall.get("beat") or {}).get("avg")),
            },
            "segments": compact_segments(music_context),
        },
        "director_memory": {
            "scene_preferences": scene_brief.get("scene_preferences", {}),
            "conversation_memory": scene_brief.get("conversation_memory", {}),
            "ai_memory_context": ai_memory_context,
            "project_awareness": project_awareness,
            "verified_answers": project_awareness.get("verified_answers", []),
            "recent_conversation": (scene_brief.get("conversation_transcript") or [])[-8:],
            "must_apply": [
                "Respect user corrections from scene brief over generic defaults.",
                "Do not echo the whole brief as an answer.",
                "Use primary_ball_asset when the user says ball.",
                "For dual central ball objects, animate/deform them in counterphase using the full keyframe JSON.",
            ],
        },
        "asset_language": {
            "asset_count": asset_inventory.get("asset_count", 0),
            "known_primary_assets": [
                asset
                for asset in asset_inventory.get("assets", [])
                if asset.get("role") in {"primary_ball_asset", "animated_effect_asset", "blend_scene_reference"}
            ][:20],
            "notes": asset_inventory.get("notes", []),
        },
        "project_language": {
            "legend": "F{id}: existing source file reference; GPU may propose new draft files but must not modify these directly.",
            "files": top_project_files(project_manifest),
            "source_fingerprint": project_manifest.get("source_fingerprint"),
        },
        "style_contract": {
            "do_not_modify_project_source": True,
            "propose_new_files_only": [
                "indexAI/scene_scripts/",
                "indexAI/patch_library/",
            ],
            "match_existing_style": True,
            "preserve_current_scene_logic": True,
            "all_existing_files_are_reference_only": True,
        },
        "task_contract": {
            "gpu_director": "create scene plan using capsule, manual, and project style",
            "gpu_code_interpreter": "write review-only standalone Blender Python scene builder in allowed output path",
            "validator": "reject empty scripts, markdown answers, existing-source modifications, missing reference files",
            "chunk_protocol": [
                "Treat capsule refs as authoritative file handles.",
                "Ask for or load exact source chunks only when needed.",
                "Never replace full keyframes with compact segments; compact segments are only semantic guidance.",
                "Return structured JSON for machine use, not prose, during plan/script phases.",
            ],
        },
        "npu_service": {
            "status": npu_status,
            "notes_digest": npu_notes[:2400],
        },
        "plan_digest": {
            "has_plan": bool(dual_plan),
            "summary": (dual_plan.get("final_plan") or dual_plan).get("recommended_scene_plan", {}),
        },
    }

    gpu_packet = {
        "format": "SPAZIOTEMPO_GPU_TASK_PACKET_V1",
        "generated_at": capsule["generated_at"],
        "track_stem": track_stem,
        "capsule": capsule,
        "required_output_schema": {
            "implementation_kind": "new_blender_scene_script_from_json",
            "reference_files": [{"file": "existing project file", "reason": "style/source reference only"}],
            "proposed_files": [{"file": f"indexAI/scene_scripts/{slug}_scene_builder_candidate.py", "kind": "standalone_blender_scene_builder"}],
            "scene_script": "non-empty Python code",
            "notes": ["short implementation notes"],
        },
    }

    capsule_json = PATCH_LIBRARY_DIR / f"{slug}_npu_service_capsule.json"
    packet_json = PATCH_LIBRARY_DIR / f"{slug}_gpu_task_packet.json"
    output_packet_json = OUTPUT_DIR / f"{track_stem}_gpu_task_packet.json"
    capsule_md = PATCH_LIBRARY_DIR / f"{slug}_npu_service_capsule.md"

    SCENE_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    (SCENE_SCRIPTS_DIR / "README.md").write_text(
        "# AI Scene Scripts\n\nStandalone Blender scene-builder drafts generated from intermediate JSON files.\n",
        encoding="utf-8",
    )
    capsule_json.write_text(json.dumps(capsule, indent=2, ensure_ascii=False), encoding="utf-8")
    packet_json.write_text(json.dumps(gpu_packet, indent=2, ensure_ascii=False), encoding="utf-8")
    output_packet_json.write_text(json.dumps(gpu_packet, indent=2, ensure_ascii=False), encoding="utf-8")
    capsule_md.write_text(format_capsule_md(capsule), encoding="utf-8")

    return {
        "capsule": capsule,
        "gpu_packet": gpu_packet,
        "capsule_json": str(capsule_json),
        "gpu_packet_json": str(packet_json),
        "output_gpu_packet_json": str(output_packet_json),
        "capsule_md": str(capsule_md),
    }


def format_capsule_md(capsule: dict[str, Any]) -> str:
    lines = [
        "# Spaziotempo NPU Service Capsule\n\n",
        f"Generated: `{capsule['generated_at']}`\n\n",
        "## Routing\n",
        json.dumps(capsule["routing_policy"], indent=2, ensure_ascii=False),
        "\n\n## Track\n",
        json.dumps(capsule["track"], indent=2, ensure_ascii=False),
        "\n\n## Project Files\n",
    ]
    for item in capsule["project_language"]["files"]:
        lines.append(f"- `{item['id']}` `{item['file']}`: {item['role']}\n")
    lines.append("\n## Audio Segments\n")
    for segment in capsule["audio_language"]["segments"]:
        lines.append(
            f"- `{segment['id']}` t={segment['t']} b={segment['b']} i={segment['i']} ctl={segment['ctl']}\n"
        )
    return "".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build compact NPU service capsule and GPU task packet.")
    parser.add_argument("--track-stem", required=True)
    parser.add_argument("--analysis", required=True)
    parser.add_argument("--track-summary", required=True)
    parser.add_argument("--music-context", required=True)
    parser.add_argument("--analysis-ai-context", required=True)
    parser.add_argument("--blender-keyframes-json", required=True)
    parser.add_argument("--dual-plan", default="")
    parser.add_argument("--npu-notes", default="")
    parser.add_argument("--npu-status", default="service_packet")
    args = parser.parse_args()

    result = build_ai_service_packet(
        track_stem=args.track_stem,
        analysis_path=Path(args.analysis),
        track_summary_path=Path(args.track_summary),
        music_context_path=Path(args.music_context),
        analysis_ai_context_path=Path(args.analysis_ai_context),
        blender_keyframes_path=Path(args.blender_keyframes_json),
        dual_plan_path=Path(args.dual_plan) if args.dual_plan else None,
        npu_notes=Path(args.npu_notes).read_text(encoding="utf-8", errors="replace") if args.npu_notes else "",
        npu_status=args.npu_status,
    )
    print(f"[OK] Wrote: {result['capsule_json']}")
    print(f"[OK] Wrote: {result['gpu_packet_json']}")
    print(f"[OK] Wrote: {result['output_gpu_packet_json']}")


if __name__ == "__main__":
    main()
