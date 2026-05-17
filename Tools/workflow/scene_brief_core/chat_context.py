"""Prompt context builders for scene director chat."""

from __future__ import annotations

import json
from pathlib import Path

from Tools.workflow._shared.project_awareness import deterministic_track_opinion

from .config import MAX_SCENE_CHAT_PROMPT_CHARS
from .io import compact_text, read_json, trim_jsonable

def compact_music_for_chat(music_context: dict | None) -> dict:
    music_context = music_context or {}
    summary = music_context.get("analysis_summary") or {}
    track = music_context.get("track_summary") or {}
    segments = music_context.get("segments") or []
    return {
        "summary": trim_jsonable(summary, 900),
        "track_summary": trim_jsonable(track, 900),
        "segment_count": len(segments),
        "first_segments": [
            {
                "index": item.get("index"),
                "time": [item.get("start_sec"), item.get("end_sec")],
                "dominant_band": item.get("dominant_band"),
                "intensity": item.get("intensity"),
                "intensity_score": item.get("intensity_score"),
                "controls": trim_jsonable(item.get("controls"), 500),
            }
            for item in segments[:5]
            if isinstance(item, dict)
        ],
    }


def compact_awareness_for_chat(project_awareness: dict | None) -> dict:
    data = project_awareness or {}
    return {
        "track_identity": trim_jsonable(data.get("track_identity"), 800),
        "pipeline_state": trim_jsonable(data.get("pipeline_state"), 1200),
        "technical_files": trim_jsonable(data.get("technical_files"), 1500),
        "npu_context": trim_jsonable(data.get("npu_context"), 800),
        "asset_summary": trim_jsonable(data.get("asset_summary") or data.get("assets"), 800),
        "warnings": trim_jsonable(data.get("warnings"), 700),
    }


def classify_user_intent(user_message: str) -> str:
    text = user_message.lower().strip()
    if "script" in text or "codice" in text or "python" in text:
        return "script_or_code_request"
    if "cosa pensi" in text or "che ne pensi" in text or text.endswith("?"):
        return "opinion_or_question"
    if any(
        word in text
        for word in [
            "vorrei",
            "aggiungi",
            "modifica",
            "crea",
            "usa",
            "togli",
            "deve",
            "fammi vedere",
        ]
    ):
        return "scene_change_request"
    return "director_note"


def compact_recent_conversation(transcript: list[dict] | None, limit: int = 6) -> list[dict]:
    transcript = transcript or []
    result: list[dict] = []
    skip_markers = (
        "ollama non ha restituito testo",
        "errore chiamando ollama",
        "certo, posso aiutarti",
        "brief aggiornato",
        "coldplay",
        "new beginnings",
    )
    for item in transcript:
        role = str(item.get("role") or "note").lower()
        content = str(item.get("content") or item.get("answer") or "")
        if role == "assistant" and any(marker in content.lower() for marker in skip_markers):
            continue
        result.append(
            {"time": item.get("time"), "role": role, "content": compact_text(content, 420)}
        )
    return result[-limit:]


def build_scene_chat_prompt(
    brief: dict,
    user_message: str,
    asset_inventory: dict | None = None,
    music_context: dict | None = None,
    project_awareness: dict | None = None,
    preflight_answers: list[dict] | None = None,
) -> str:
    intent = classify_user_intent(user_message)
    compact = {
        "track_stem": brief.get("track_stem"),
        "user_intent": intent,
        "scene_preferences": trim_jsonable(brief.get("scene_preferences"), 1800),
        "must_keep": brief.get("must_keep"),
        "workflow_policy": brief.get("workflow_policy"),
        "conversation_memory": trim_jsonable(brief.get("conversation_memory"), 2200),
        "project_awareness": compact_awareness_for_chat(project_awareness),
        "preflight_answers": trim_jsonable(preflight_answers or [], 1200),
        "music_context": compact_music_for_chat(music_context),
        "known_assets": trim_jsonable((asset_inventory or {}).get("assets", [])[:10], 1200),
        "recent_conversation": compact_recent_conversation(
            brief.get("conversation_transcript"), limit=6
        ),
        "user_message": compact_text(user_message, 1000),
    }
    prompt = f"""
Sei il regista tecnico locale del progetto Blender Spaziotempo.
Rispondi in italiano, diretto, operativo, da art director tecnico Blender 5.1 e Python.
Non scrivere lo script completo in chat: dai direzione, scelte tecniche e prossimi vincoli per il generatore.
Usa solo l'identita del brano presente nel contesto. Non citare brani esterni.
Non suggerire setup gia fatto dalla pipeline. Se serve codice, indica quale fase/pulsante lo genera.
Rispondi con massimo 8 punti, concreti, senza preamboli.
Mantieni i keyframe completi del JSON Blender come vincolo centrale.

CONTESTO_COMPATTO:
{json.dumps(compact, indent=2, ensure_ascii=False)}
""".strip()
    if len(prompt) <= MAX_SCENE_CHAT_PROMPT_CHARS:
        return prompt
    compact["project_awareness"] = trim_jsonable(compact.get("project_awareness"), 1500)
    compact["conversation_memory"] = trim_jsonable(compact.get("conversation_memory"), 1200)
    compact["known_assets"] = trim_jsonable(compact.get("known_assets"), 600)
    prompt = f"""
Sei il regista tecnico locale del progetto Blender Spaziotempo.
Rispondi in italiano con massimo 6 punti tecnici.
Non generare script completo in chat. Usa i dati compatti e conserva il vincolo: usare tutti i keyframe del JSON Blender.

CONTESTO_COMPATTO:
{json.dumps(compact, indent=2, ensure_ascii=False)}
""".strip()
    return prompt[:MAX_SCENE_CHAT_PROMPT_CHARS]


def sanitize_scene_reply(reply: str, *, awareness: dict, preflight_answers: list[dict]) -> str:
    if not reply:
        return ""
    lowered = reply.lower()
    forbidden_markers = [
        "assicurati di avere il file wav",
        "importa l'audio in blender",
        "apri blender e importa",
        "aggiungi l'audio in blender",
        "carica il file wav in blender",
        "coldplay",
        "new beginnings",
    ]
    if not any(marker in lowered for marker in forbidden_markers):
        return reply
    if "coldplay" in lowered or "new beginnings" in lowered:
        track_identity = awareness.get("track_identity", {})
        files = awareness.get("technical_files", {})
        music_context = read_json(Path(files.get("music_context_json", {}).get("path", "")))
        return deterministic_track_opinion(track_identity, music_context)
    correction = [
        "Correzione di contesto progetto: non serve importare manualmente il WAV in Blender."
    ]
    for item in preflight_answers:
        answer = str(item.get("answer") or "").strip()
        if answer:
            correction.append(f"- {answer}")
    cleaned = reply
    for marker in forbidden_markers:
        cleaned = cleaned.replace(
            marker, "[rimosso: consiglio generico non valido per questo progetto]"
        )
    return "\n".join(correction) + "\n\n" + cleaned.strip()
