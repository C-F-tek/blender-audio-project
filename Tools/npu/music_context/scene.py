"""Scene-spec summarization for music context."""

from __future__ import annotations

import json
from pathlib import Path

from .common import read_text, rel_to_root, sha256_text

def scene_summary_from_json(path: Path, data: dict) -> dict:
    objects = data.get("objects", [])
    materials = data.get("materials", [])
    audio_mapping = data.get("audio_mapping", [])
    node_animation = data.get("node_animation", [])

    return {
        "file": rel_to_root(path),
        "type": "json",
        "keys": sorted(data.keys()),
        "scene_name": data.get("scene_name"),
        "visual_concept": data.get("visual_concept"),
        "style_mode": data.get("style_mode"),
        "environment": data.get("environment"),
        "lighting_style": data.get("lighting_style"),
        "palette": data.get("palette"),
        "camera": data.get("camera") or data.get("camera_style"),
        "objects_count": len(objects) if isinstance(objects, list) else 0,
        "materials_count": len(materials) if isinstance(materials, list) else 0,
        "audio_mapping_count": len(audio_mapping) if isinstance(audio_mapping, list) else 0,
        "node_animation_count": len(node_animation) if isinstance(node_animation, list) else 0,
        "object_names": [
            item.get("name") for item in objects if isinstance(item, dict) and item.get("name")
        ][:30],
        "audio_targets": [
            f"{item.get('target')}:{item.get('property')}:{item.get('band')}"
            for item in audio_mapping
            if isinstance(item, dict)
        ][:40],
    }

def load_scene_records(scene_files: list[Path]) -> list[dict]:
    records = []
    for path in scene_files:
        if not path.exists():
            continue

        text = read_text(path)
        record = {
            "file": rel_to_root(path),
            "chars": len(text),
            "lines": text.count("\n") + 1 if text else 0,
            "sha256": sha256_text(text),
            "content": text,
        }

        if path.suffix.lower() == ".json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError as exc:
                record["summary"] = {"file": rel_to_root(path), "type": "json", "error": str(exc)}
            else:
                record["summary"] = scene_summary_from_json(path, data)
        else:
            record["summary"] = {
                "file": rel_to_root(path),
                "type": "text",
                "chars": len(text),
                "lines": text.count("\n") + 1 if text else 0,
            }

        records.append(record)
    return records
