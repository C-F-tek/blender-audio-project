from __future__ import annotations

import json
from pathlib import Path

from ia_carmine.providers.npu.paths import find_repo_root
from typing import Any

ROOT = find_repo_root(__file__)
OUTPUT_DIR = ROOT / "output"
INDEX_AI_DIR = ROOT / "indexAI"


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def compact_asset_inventory(asset_inventory: dict[str, Any]) -> dict[str, Any]:
    assets = (
        asset_inventory.get("assets") if isinstance(asset_inventory.get("assets"), list) else []
    )
    primary = [
        {
            "role": asset.get("role"),
            "name": asset.get("name"),
            "path": asset.get("path"),
            "type": asset.get("type") or asset.get("extension"),
        }
        for asset in assets
        if isinstance(asset, dict)
        and asset.get("role")
        in {"primary_ball_asset", "animated_effect_asset", "blend_scene_reference"}
    ][:24]
    return {
        "asset_count": asset_inventory.get("asset_count", len(assets)),
        "primary_assets": primary,
        "notes": asset_inventory.get("notes", [])[:12]
        if isinstance(asset_inventory.get("notes"), list)
        else [],
    }


def slugify(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")
    return "_".join(part for part in slug.split("_") if part) or "track"


def compact_project_awareness(track_stem: str) -> dict[str, Any]:
    awareness = read_json(
        INDEX_AI_DIR / "patch_library" / f"{slugify(track_stem)}_project_awareness.json"
    )
    if not awareness:
        return {}
    verified_answers = awareness.get("verified_answers", [])
    if not verified_answers:
        verified_answers = [
            {
                "question": "Abbiamo qualcosa che puo essere usata sui keyframe dell'audio?",
                "answer": "Si. Usa il full `analysis_blender_keyframes.json` del brano: contiene `frames` con low/mid/high/onset/beat. I segmenti compatti sono solo guida macro.",
            },
            {
                "question": "Serve importare manualmente il WAV in Blender?",
                "answer": "No. Nel progetto il WAV passa da analysis/music/keyframe JSON; le AI devono ragionare su quei file e sulla pipeline.",
            },
        ]
    return {
        "format": awareness.get("format"),
        "generated_at": awareness.get("generated_at"),
        "track_identity": awareness.get("track_identity", {}),
        "pipeline_state": awareness.get("pipeline_state", {}),
        "npu_context": awareness.get("npu_context", {}),
        "verified_answers": verified_answers,
        "director_rules": awareness.get("director_rules", []),
        "missing_or_suspicious": awareness.get("missing_or_suspicious", []),
    }


def build_ai_memory_context(
    *,
    track_stem: str,
    output_dir: Path | None = None,
    scene_brief_path: Path | None = None,
    asset_inventory_path: Path | None = None,
) -> dict[str, Any]:
    output_dir = Path(output_dir or OUTPUT_DIR)
    scene_brief_path = scene_brief_path or output_dir / f"{track_stem}_scene_brief.json"
    asset_inventory_path = asset_inventory_path or output_dir / "spaziotempo_asset_inventory.json"

    scene_brief = read_json(scene_brief_path)
    asset_inventory = read_json(asset_inventory_path)
    memory = (
        scene_brief.get("conversation_memory")
        if isinstance(scene_brief.get("conversation_memory"), dict)
        else {}
    )

    return {
        "format": "SPAZIOTEMPO_AI_MEMORY_CONTEXT_V1",
        "track_stem": track_stem,
        "scene_brief_json": str(scene_brief_path),
        "asset_inventory_json": str(asset_inventory_path),
        "has_scene_brief": bool(scene_brief),
        "scene_preferences": scene_brief.get("scene_preferences", {}) if scene_brief else {},
        "conversation_memory": memory,
        "recent_user_requests": memory.get("recent_user_requests", []) if memory else [],
        "durable_constraints": memory.get("durable_constraints", []) if memory else [],
        "asset_memory": compact_asset_inventory(asset_inventory),
        "project_awareness": compact_project_awareness(track_stem),
        "operating_rules": [
            "Use this memory as interpretation context for AI outputs, never to alter numeric audio analysis.",
            "Respect user corrections over generic defaults.",
            "If the user mentions ball, prefer asset role primary_ball_asset.",
            "Full analysis_blender_keyframes frames must remain complete and authoritative.",
            "For two central ball objects, use counterphase animation and inverted audio mapping.",
            "Do not suggest manual Blender/audio import steps already handled by the project pipeline.",
        ],
    }
