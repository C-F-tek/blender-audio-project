"""Ollama-backed scene director chat reply generation."""

from __future__ import annotations

import sys
from pathlib import Path

from Tools.workflow.workflow_run._shared.project_awareness import (
    build_preflight_answers_for_message,
    build_project_awareness,
    save_project_awareness,
)

from .chat_context import build_scene_chat_prompt, sanitize_scene_reply
from .config import MAX_SCENE_CHAT_PROMPT_CHARS
from .io import append_scene_runtime_event, read_json
from .storage import append_scene_message, load_or_create_scene_brief

def generate_scene_chat_reply(
    *,
    track_stem: str,
    audio_path: str,
    output_path: Path,
    user_message: str,
    model: str = "",
    asset_inventory_path: Path | None = None,
) -> str:
    if not str(model or "").strip():
        raise ValueError("scene_chat_model_explicit_required")
    brief = load_or_create_scene_brief(
        track_stem=track_stem, audio_path=audio_path, output_path=output_path
    )
    asset_inventory = read_json(asset_inventory_path) if asset_inventory_path else {}
    music_context = read_json(output_path.with_name(f"{track_stem}_music_context.json"))
    awareness = build_project_awareness(
        track_stem=track_stem,
        audio_path=audio_path,
        output_dir=output_path.parent,
        asset_inventory=asset_inventory,
        music_context=music_context,
    )
    save_project_awareness(awareness)
    preflight_answers = build_preflight_answers_for_message(user_message, awareness, music_context)
    prompt = build_scene_chat_prompt(
        brief, user_message, asset_inventory, music_context, awareness, preflight_answers
    )

    npu_dir = Path(__file__).resolve().parents[2] / "npu"
    if str(npu_dir) not in sys.path:
        sys.path.insert(0, str(npu_dir))

    response_meta = {
        "track_stem": track_stem,
        "model": model,
        "prompt_chars": len(prompt),
        "prompt_limit_chars": MAX_SCENE_CHAT_PROMPT_CHARS,
        "user_message_chars": len(user_message),
        "output_path": str(output_path),
    }
    try:
        from ia_carmine.providers.ollama.config import ollama_runtime_log_path
        from ia_carmine.providers.ollama.session import OllamaSession

        with OllamaSession(
            model=model,
            keep_alive="2m",
            shutdown_server=False,
            unload_model=True,
            startup_timeout=20.0,
        ) as session:
            reply = session.generate(prompt, max_new_tokens=900, temperature=0.22)
            response_meta["selected_model"] = session.model
            response_meta["ollama_runtime_log"] = str(ollama_runtime_log_path())
    except Exception as exc:
        response_meta["error_type"] = type(exc).__name__
        response_meta["error"] = str(exc)
        append_scene_runtime_event("scene_chat_error", response_meta)
        reply = f"Errore chiamando Ollama: {exc}\n\nIl tuo messaggio e' comunque salvato nel brief; puoi generare lo script anche senza risposta chat."

    response_meta["raw_reply_chars"] = len(str(reply or ""))
    response_meta["empty_response"] = response_meta["raw_reply_chars"] == 0
    append_scene_runtime_event(
        "scene_chat_empty_response" if response_meta["empty_response"] else "scene_chat_response",
        response_meta,
    )

    reply = sanitize_scene_reply(
        str(reply or "").strip(), awareness=awareness, preflight_answers=preflight_answers
    )
    if not reply:
        reply = (
            "Ollama non ha restituito testo. Il messaggio utente e' comunque salvato nel brief.\n\n"
            f"Diagnostica: modello={response_meta.get('selected_model') or model}, prompt_chars={response_meta.get('prompt_chars')}, "
            f"log={response_meta.get('ollama_runtime_log', 'output/workflow_logs/ollama_runtime_events.jsonl')}"
        )
    append_scene_message(
        track_stem=track_stem,
        audio_path=audio_path,
        output_path=output_path,
        role="assistant",
        content=reply,
    )
    return reply
