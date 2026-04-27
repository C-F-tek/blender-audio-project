# Project Code Chunk 113/212

- File: `Tools/npu/ai_memory_context.py`
- Part: `1`
- Lines: `1-111`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `from typing import Any`, `json`
- Functions: `read_json(path)` line 13; `compact_asset_inventory(asset_inventory)` line 23; `slugify(value)` line 43; `compact_project_awareness(track_stem)` line 48; `build_ai_memory_context()` line 76
- Assignments: `ROOT`, `OUTPUT_DIR`, `INDEX_AI_DIR`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: from typing import Any
00005: import json
00006: 
00007: 
00008: ROOT = Path(__file__).resolve().parents[2]
00009: OUTPUT_DIR = ROOT / "output"
00010: INDEX_AI_DIR = ROOT / "indexAI"
00011: 
00012: 
00013: def read_json(path: Path) -> dict[str, Any]:
00014:     if not path.exists():
00015:         return {}
00016:     try:
00017:         data = json.loads(path.read_text(encoding="utf-8"))
00018:     except Exception:
00019:         return {}
00020:     return data if isinstance(data, dict) else {}
00021: 
00022: 
00023: def compact_asset_inventory(asset_inventory: dict[str, Any]) -> dict[str, Any]:
00024:     assets = asset_inventory.get("assets") if isinstance(asset_inventory.get("assets"), list) else []
00025:     primary = [
00026:         {
00027:             "role": asset.get("role"),
00028:             "name": asset.get("name"),
00029:             "path": asset.get("path"),
00030:             "type": asset.get("type") or asset.get("extension"),
00031:         }
00032:         for asset in assets
00033:         if isinstance(asset, dict)
00034:         and asset.get("role") in {"primary_ball_asset", "animated_effect_asset", "blend_scene_reference"}
00035:     ][:24]
00036:     return {
00037:         "asset_count": asset_inventory.get("asset_count", len(assets)),
00038:         "primary_assets": primary,
00039:         "notes": asset_inventory.get("notes", [])[:12] if isinstance(asset_inventory.get("notes"), list) else [],
00040:     }
00041: 
00042: 
00043: def slugify(value: str) -> str:
00044:     slug = "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")
00045:     return "_".join(part for part in slug.split("_") if part) or "track"
00046: 
00047: 
00048: def compact_project_awareness(track_stem: str) -> dict[str, Any]:
00049:     awareness = read_json(INDEX_AI_DIR / "patch_library" / f"{slugify(track_stem)}_project_awareness.json")
00050:     if not awareness:
00051:         return {}
00052:     verified_answers = awareness.get("verified_answers", [])
00053:     if not verified_answers:
00054:         verified_answers = [
00055:             {
00056:                 "question": "Abbiamo qualcosa che puo essere usata sui keyframe dell'audio?",
00057:                 "answer": "Si. Usa il full `analysis_blender_keyframes.json` del brano: contiene `frames` con low/mid/high/onset/beat. I segmenti compatti sono solo guida macro.",
00058:             },
00059:             {
00060:                 "question": "Serve importare manualmente il WAV in Blender?",
00061:                 "answer": "No. Nel progetto il WAV passa da analysis/music/keyframe JSON; le AI devono ragionare su quei file e sulla pipeline.",
00062:             },
00063:         ]
00064:     return {
00065:         "format": awareness.get("format"),
00066:         "generated_at": awareness.get("generated_at"),
00067:         "track_identity": awareness.get("track_identity", {}),
00068:         "pipeline_state": awareness.get("pipeline_state", {}),
00069:         "npu_context": awareness.get("npu_context", {}),
00070:         "verified_answers": verified_answers,
00071:         "director_rules": awareness.get("director_rules", []),
00072:         "missing_or_suspicious": awareness.get("missing_or_suspicious", []),
00073:     }
00074: 
00075: 
00076: def build_ai_memory_context(
00077:     *,
00078:     track_stem: str,
00079:     output_dir: Path | None = None,
00080:     scene_brief_path: Path | None = None,
00081:     asset_inventory_path: Path | None = None,
00082: ) -> dict[str, Any]:
00083:     output_dir = Path(output_dir or OUTPUT_DIR)
00084:     scene_brief_path = scene_brief_path or output_dir / f"{track_stem}_scene_brief.json"
00085:     asset_inventory_path = asset_inventory_path or output_dir / "spaziotempo_asset_inventory.json"
00086: 
00087:     scene_brief = read_json(scene_brief_path)
00088:     asset_inventory = read_json(asset_inventory_path)
00089:     memory = scene_brief.get("conversation_memory") if isinstance(scene_brief.get("conversation_memory"), dict) else {}
00090: 
00091:     return {
00092:         "format": "SPAZIOTEMPO_AI_MEMORY_CONTEXT_V1",
00093:         "track_stem": track_stem,
00094:         "scene_brief_json": str(scene_brief_path),
00095:         "asset_inventory_json": str(asset_inventory_path),
00096:         "has_scene_brief": bool(scene_brief),
00097:         "scene_preferences": scene_brief.get("scene_preferences", {}) if scene_brief else {},
00098:         "conversation_memory": memory,
00099:         "recent_user_requests": memory.get("recent_user_requests", []) if memory else [],
00100:         "durable_constraints": memory.get("durable_constraints", []) if memory else [],
00101:         "asset_memory": compact_asset_inventory(asset_inventory),
00102:         "project_awareness": compact_project_awareness(track_stem),
00103:         "operating_rules": [
00104:             "Use this memory as interpretation context for AI outputs, never to alter numeric audio analysis.",
00105:             "Respect user corrections over generic defaults.",
00106:             "If the user mentions ball, prefer asset role primary_ball_asset.",
00107:             "Full analysis_blender_keyframes frames must remain complete and authoritative.",
00108:             "For two central ball objects, use counterphase animation and inverted audio mapping.",
00109:             "Do not suggest manual Blender/audio import steps already handled by the project pipeline.",
00110:         ],
00111:     }
```
