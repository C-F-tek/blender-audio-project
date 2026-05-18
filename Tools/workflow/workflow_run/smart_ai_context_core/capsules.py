from __future__ import annotations

from typing import Any

from .core import compact, capsule


IMPORTANT_JSON_KEYS = [
    "track_identity",
    "analysis_summary",
    "track_summary",
    "scene_preferences",
    "conversation_memory",
    "pipeline_state",
    "technical_files",
    "must_keep",
    "workflow_policy",
    "segments",
    "frames",
    "recommended_scene_plan",
    "audio_mapping_plan",
    "implementation_plan",
    "scene_script",
    "support_files",
    "safety",
]

HIGH_PRIORITY_KEYS = {
    "scene_preferences",
    "conversation_memory",
    "pipeline_state",
    "technical_files",
}


def json_capsules(source: str, path: str, data: Any, max_chars: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(data, dict):
        out.extend(_dict_capsules(source, path, data, max_chars))
    elif isinstance(data, list):
        for idx, start in enumerate(range(0, len(data), 12), start=1):
            out.append(
                capsule(
                    source,
                    f"{path}[{start}:{start + 12}]",
                    "json_list_chunk",
                    f"List chunk {idx}",
                    data[start : start + 12],
                    5,
                    max_chars,
                )
            )
    return out


def _dict_capsules(source: str, path: str, data: dict[str, Any], max_chars: int) -> list[dict]:
    out: list[dict[str, Any]] = []
    for key in IMPORTANT_JSON_KEYS:
        if key not in data:
            continue
        value = data[key]
        if key == "frames" and isinstance(value, list):
            value = {"frame_count": len(value), "first": value[:2], "last": value[-2:]}
            out.append(
                capsule(
                    source,
                    f"{path}.frames.manifest",
                    "frame_manifest",
                    "Full Blender keyframes manifest",
                    value,
                    10,
                    max_chars,
                )
            )
        elif key == "segments" and isinstance(value, list):
            out.extend(_segment_capsules(source, path, value, max_chars))
        else:
            priority = 9 if key in HIGH_PRIORITY_KEYS else 7
            out.append(capsule(source, f"{path}.{key}", "json_section", key, value, priority, max_chars))
    rest = {k: v for k, v in data.items() if k not in IMPORTANT_JSON_KEYS}
    if rest:
        out.append(
            capsule(
                source,
                f"{path}.remaining",
                "json_remainder",
                f"Remainder of {path}",
                rest,
                4,
                max_chars,
            )
        )
    return out


def _segment_capsules(source: str, path: str, value: list[Any], max_chars: int) -> list[dict]:
    out: list[dict[str, Any]] = []
    for idx, start in enumerate(range(0, len(value), 8), start=1):
        out.append(
            capsule(
                source,
                f"{path}.segments[{start}:{start + 8}]",
                "music_segments",
                f"Music segment capsule {idx}",
                value[start : start + 8],
                8,
                max_chars,
            )
        )
    return out


def text_capsules(source: str, path: str, text: str, max_chars: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, start in enumerate(range(0, len(text), max_chars), start=1):
        chunk = text[start : start + max_chars]
        if chunk.strip():
            title = compact(chunk.splitlines()[0] if chunk.splitlines() else path, 120)
            out.append(
                capsule(source, f"{path}#chunk-{idx}", "text_chunk", title, chunk, 5, max_chars)
            )
    return out
