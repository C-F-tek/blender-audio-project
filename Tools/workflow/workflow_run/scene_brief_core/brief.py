"""Scene brief builder."""

from __future__ import annotations

from .config import MAX_SCENE_CHAT_PROMPT_CHARS
from .io import now_iso
from .memory import build_conversation_memory

def build_scene_brief(
    *,
    track_stem: str,
    audio_path: str,
    preferences: dict[str, str],
    transcript: list[dict] | None = None,
    previous: dict | None = None,
) -> dict:
    previous = previous or {}
    active_transcript = (
        transcript if transcript is not None else previous.get("conversation_transcript", [])
    )
    memory = build_conversation_memory(
        preferences=preferences, transcript=active_transcript, previous=previous
    )
    return {
        "version": 1,
        "kind": "spaziotempo_scene_director_brief",
        "generated_at": now_iso(),
        "track_stem": track_stem,
        "audio_path": audio_path,
        "scene_preferences": preferences,
        "must_keep": [
            "Use the full analysis_blender_keyframes JSON frames for animation.",
            "Use compact music segments only for composition and macro decisions.",
            "Create a standalone Blender Python scene script under indexAI/scene_scripts.",
            "Do not modify existing project source files.",
        ],
        "workflow_policy": {
            "npu_role": "optional compact service/router, not heavy generator",
            "gpu_or_ollama_role": "heavy reasoning and code generation",
            "manual_review_required": True,
            "chat_prompt_policy": f"Scene Director chat prompt is capped to {MAX_SCENE_CHAT_PROMPT_CHARS} chars; full files are used by generation phases.",
        },
        "conversation_memory": memory,
        "conversation_transcript": active_transcript,
    }
