"""Compatibility API for scene director brief/chat helpers."""

from __future__ import annotations

try:
    from scene_brief_core.brief import build_scene_brief
    from scene_brief_core.chat_context import (
        build_scene_chat_prompt,
        classify_user_intent,
        compact_awareness_for_chat,
        compact_music_for_chat,
        compact_recent_conversation,
        sanitize_scene_reply,
    )
    from scene_brief_core.chat_reply import generate_scene_chat_reply
    from scene_brief_core.config import MEMORY_VERSION, QUESTION_FIELDS
    from scene_brief_core.interactive import prompt_value, run_interactive_scene_brief
    from scene_brief_core.io import (
        append_scene_runtime_event,
        compact_text,
        default_scene_preferences,
        now_iso,
        read_json,
        trim_jsonable,
        write_json,
    )
    from scene_brief_core.memory import build_conversation_memory
    from scene_brief_core.storage import (
        append_scene_message,
        clear_scene_chat_history,
        load_or_create_scene_brief,
    )
except ImportError:
    from Tools.workflow._shared.scene_brief_core.brief import build_scene_brief
    from Tools.workflow._shared.scene_brief_core.chat_context import (
        build_scene_chat_prompt,
        classify_user_intent,
        compact_awareness_for_chat,
        compact_music_for_chat,
        compact_recent_conversation,
        sanitize_scene_reply,
    )
    from Tools.workflow._shared.scene_brief_core.chat_reply import generate_scene_chat_reply
    from Tools.workflow._shared.scene_brief_core.config import MEMORY_VERSION, QUESTION_FIELDS
    from Tools.workflow._shared.scene_brief_core.interactive import prompt_value, run_interactive_scene_brief
    from Tools.workflow._shared.scene_brief_core.io import (
        append_scene_runtime_event,
        compact_text,
        default_scene_preferences,
        now_iso,
        read_json,
        trim_jsonable,
        write_json,
    )
    from Tools.workflow._shared.scene_brief_core.memory import build_conversation_memory
    from Tools.workflow._shared.scene_brief_core.storage import (
        append_scene_message,
        clear_scene_chat_history,
        load_or_create_scene_brief,
    )

__all__ = [name for name in globals() if not name.startswith("_")]
