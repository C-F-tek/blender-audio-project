from __future__ import annotations

from typing import Any


def compact_segments_for_prompt(
    music_context: dict[str, Any],
    *,
    max_events_per_segment: int = 6,
) -> list[dict[str, Any]]:
    """Build deterministic compact segment records for prompt payloads."""

    segments = music_context.get("segments") or []
    if not isinstance(segments, list):
        return []
    compact: list[dict[str, Any]] = []
    for segment in segments:
        if not isinstance(segment, dict):
            continue
        compact.append(
            {
                "index": segment.get("index"),
                "start_sec": segment.get("start_sec"),
                "end_sec": segment.get("end_sec"),
                "dominant_band": segment.get("dominant_band"),
                "intensity": segment.get("intensity"),
                "intensity_score": segment.get("intensity_score"),
                "controls": segment.get("controls"),
                "top_events": (segment.get("top_events") or [])[:max_events_per_segment],
            }
        )
    return compact


def build_creative_scene_prompt_payload(
    music_context: dict[str, Any],
    *,
    npu_notes: str,
    project_index: str,
) -> dict[str, Any]:
    """Return the data payload used by the creative scene prompt."""

    return {
        "analysis_summary": music_context.get("analysis_summary"),
        "track_summary": music_context.get("track_summary"),
        "scene_summaries": music_context.get("scene_summaries"),
        "ai_operating_contract": {
            "memory_first": "Use director memory and user corrections before generic defaults.",
            "chunk_first": "Use compact chunks for reasoning and refs for exact data.",
            "full_keyframes": "Never summarize or discard full Blender keyframes; scripts must read the full frames list.",
            "answer_shape": "Return only the requested JSON schema during pipeline calls.",
        },
        "segments": compact_segments_for_prompt(music_context),
        "npu_technical_notes": npu_notes[:18000],
        "primary_project_index": project_index[:14000],
    }


def build_merge_prompt_payload(
    music_context: dict[str, Any],
    *,
    npu_notes: str,
    project_index: str,
    creative: dict[str, Any],
    technical: dict[str, Any],
) -> dict[str, Any]:
    """Return the data payload used by the NPU/Ollama merge prompt."""

    return {
        "music_summary": music_context.get("analysis_summary"),
        "ai_operating_contract": {
            "memory_first": True,
            "use_director_brief": True,
            "use_assets_by_role": True,
            "full_keyframes_json_is_authoritative": True,
        },
        "npu_technical_notes": npu_notes[:14000],
        "primary_project_index": project_index[:12000],
        "ollama_creative": creative,
        "ollama_technical": technical,
    }


def build_implementation_retry_payload(
    plan: dict[str, Any],
    *,
    preferred_existing_files: list[str],
    allowed_new_prefixes: tuple[str, ...],
    validation: dict[str, Any],
) -> dict[str, Any]:
    """Return the deterministic payload for retrying invalid implementation JSON."""

    return {
        "dual_ai_plan": plan,
        "preferred_existing_files": preferred_existing_files,
        "allowed_new_prefixes": list(allowed_new_prefixes),
        "previous_validation_errors": validation.get("issues", []),
        "previous_response_was_invalid": True,
    }
