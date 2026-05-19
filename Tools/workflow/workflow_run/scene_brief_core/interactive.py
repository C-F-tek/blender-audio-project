"""Interactive scene brief collection."""

from __future__ import annotations

from pathlib import Path

from .brief import build_scene_brief
from .config import QUESTION_FIELDS
from .io import default_scene_preferences, read_json, write_json

def prompt_value(label: str, question: str, default: str) -> tuple[str, dict]:
    print(f"\n[{label}]")
    print(question)
    if default:
        print(f"Default: {default}")
    value = input("> ").strip()
    answer = value or default
    return answer, {"label": label, "question": question, "default": default, "answer": answer}


def run_interactive_scene_brief(*, track_stem: str, audio_path: str, output_path: Path) -> dict:
    previous = read_json(output_path)
    previous_preferences = (
        previous.get("scene_preferences")
        if isinstance(previous.get("scene_preferences"), dict)
        else {}
    )
    defaults = default_scene_preferences()
    preferences: dict[str, str] = {}
    transcript: list[dict] = []

    print("\n" + "=" * 72)
    print("SPAZIOTEMPO SCENE DIRECTOR CHAT")
    print("=" * 72)
    print("Rispondi liberamente. Invio mantiene il default o la risposta precedente.")
    print(f"Track: {track_stem}")
    print(f"Output: {output_path}")

    for field, label, question, default in QUESTION_FIELDS:
        current_default = str(previous_preferences.get(field) or defaults.get(field) or default)
        answer, item = prompt_value(label, question, current_default)
        preferences[field] = answer
        item["field"] = field
        transcript.append(item)

    brief = build_scene_brief(
        track_stem=track_stem,
        audio_path=audio_path,
        preferences=preferences,
        transcript=transcript,
        previous=previous,
    )
    write_json(output_path, brief)
    print(f"\n[OK] Scene director brief salvato: {output_path}")
    return brief
