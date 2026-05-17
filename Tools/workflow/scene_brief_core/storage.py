"""Scene brief persistence and transcript updates."""

from __future__ import annotations

from pathlib import Path

from .brief import build_scene_brief
from .config import MEMORY_VERSION
from .io import compact_text, default_scene_preferences, now_iso, read_json, write_json
from .memory import build_conversation_memory

def load_or_create_scene_brief(*, track_stem: str, audio_path: str, output_path: Path) -> dict:
    existing = read_json(output_path)
    if existing:
        memory = (
            existing.get("conversation_memory")
            if isinstance(existing.get("conversation_memory"), dict)
            else {}
        )
        if memory.get("memory_version") != MEMORY_VERSION:
            preferences = (
                existing.get("scene_preferences")
                if isinstance(existing.get("scene_preferences"), dict)
                else default_scene_preferences()
            )
            transcript = (
                existing.get("conversation_transcript")
                if isinstance(existing.get("conversation_transcript"), list)
                else []
            )
            existing["conversation_memory"] = build_conversation_memory(
                preferences={key: str(value) for key, value in preferences.items()},
                transcript=transcript,
                previous=existing,
            )
            write_json(output_path, existing)
        return existing
    brief = build_scene_brief(
        track_stem=track_stem,
        audio_path=audio_path,
        preferences=default_scene_preferences(),
        transcript=[],
    )
    write_json(output_path, brief)
    return brief


def append_scene_message(
    *, track_stem: str, audio_path: str, output_path: Path, role: str, content: str
) -> dict:
    brief = load_or_create_scene_brief(
        track_stem=track_stem, audio_path=audio_path, output_path=output_path
    )
    transcript = (
        brief.get("conversation_transcript")
        if isinstance(brief.get("conversation_transcript"), list)
        else []
    )
    transcript.append({"time": now_iso(), "role": role, "content": content})
    preferences = (
        brief.get("scene_preferences")
        if isinstance(brief.get("scene_preferences"), dict)
        else default_scene_preferences()
    )
    if role == "user":
        current_notes = str(preferences.get("free_notes") or "").strip()
        preferences["free_notes"] = compact_text(
            (current_notes + "\n" + content).strip() if current_notes else content, 2400
        )
    updated = build_scene_brief(
        track_stem=track_stem,
        audio_path=audio_path,
        preferences={key: str(value) for key, value in preferences.items()},
        transcript=transcript,
        previous=brief,
    )
    write_json(output_path, updated)
    return updated


def clear_scene_chat_history(*, track_stem: str, audio_path: str, output_path: Path) -> dict:
    brief = load_or_create_scene_brief(
        track_stem=track_stem, audio_path=audio_path, output_path=output_path
    )
    preferences = (
        brief.get("scene_preferences")
        if isinstance(brief.get("scene_preferences"), dict)
        else default_scene_preferences()
    )
    preferences = {key: str(value) for key, value in preferences.items()}
    preferences["free_notes"] = ""
    updated = build_scene_brief(
        track_stem=track_stem,
        audio_path=audio_path,
        preferences=preferences,
        transcript=[],
        previous={},
    )
    updated["chat_cleared_at"] = now_iso()
    write_json(output_path, updated)
    return updated
