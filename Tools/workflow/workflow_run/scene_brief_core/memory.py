"""Conversation memory compaction for scene director chat."""

from __future__ import annotations

from .config import MEMORY_VERSION
from .io import compact_text, now_iso

def build_conversation_memory(
    *, preferences: dict[str, str], transcript: list[dict] | None, previous: dict | None = None
) -> dict:
    previous = previous or {}
    transcript = transcript or []
    user_requests: list[str] = []
    assistant_notes: list[str] = []
    durable_constraints: list[str] = []
    question_history: list[str] = []
    asset_mentions: list[str] = []

    keywords = (
        "keyframe",
        "audio",
        "asset",
        "ball",
        "sfera",
        "hero",
        "aura",
        "fog",
        "nebbia",
        "luce",
        "emission",
        "nero",
        "sfondo",
        "render",
        "npu",
        "ollama",
        "gpu",
        "script",
        "blender",
        "memoria",
        "chat",
    )
    boilerplate_markers = (
        "certo, posso aiutarti",
        "brief aggiornato",
        "istruzioni operative",
        "coldplay",
        "new beginnings",
        "ollama non ha restituito testo",
    )

    for item in transcript:
        role = str(item.get("role") or "note").lower()
        content = str(item.get("content") or item.get("answer") or "").strip()
        if not content:
            continue
        lowered = content.lower()
        if role == "user":
            user_requests.append(compact_text(content, 420))
            if "?" in content or lowered.startswith(
                ("cosa", "come", "perche", "perché", "quale", "dimmi")
            ):
                question_history.append(compact_text(content, 240))
            if any(word in lowered for word in keywords):
                durable_constraints.append(compact_text(content, 360))
        elif role == "assistant" and not any(marker in lowered for marker in boilerplate_markers):
            assistant_notes.append(compact_text(content, 280))
        for token in ("ball", "primary_ball_asset", "fbx", "cover", "manual", "indexai"):
            if token.lower() in lowered:
                asset_mentions.append(token)

    preference_summary = [
        f"{key}: {compact_text(value, 220)}" for key, value in preferences.items() if value
    ]
    previous_memory = (
        previous.get("conversation_memory")
        if isinstance(previous.get("conversation_memory"), dict)
        else {}
    )
    previous_constraints = (
        previous_memory.get("durable_constraints") if isinstance(previous_memory, dict) else []
    )
    if isinstance(previous_constraints, list):
        durable_constraints = [str(item) for item in previous_constraints] + durable_constraints

    def unique_recent(values: list[str], limit: int) -> list[str]:
        seen = set()
        result = []
        for value in values:
            key = value.strip().lower()
            if key and key not in seen:
                seen.add(key)
                result.append(value)
        return result[-limit:]

    return {
        "updated_at": now_iso(),
        "memory_version": MEMORY_VERSION,
        "message_count": len(transcript),
        "preference_summary": preference_summary[-12:],
        "recent_user_requests": user_requests[-10:],
        "recent_user_questions": question_history[-5:],
        "recent_assistant_notes": assistant_notes[-6:],
        "durable_constraints": unique_recent(durable_constraints, 14),
        "asset_mentions": sorted(set(asset_mentions)),
        "memory_policy": "Compact director memory. Full files are used by generation pipeline, not by chat prompt.",
    }
