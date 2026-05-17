from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from project_awareness import (
    build_preflight_answers_for_message,
    build_project_awareness,
    deterministic_track_opinion,
    save_project_awareness,
)

MEMORY_VERSION = 4
MAX_SCENE_CHAT_PROMPT_CHARS = 14000

QUESTION_FIELDS = [
    (
        "creative_intent",
        "Idea generale / mood",
        "Che sensazione deve dare la scena?",
        "cinematica, audio-reactive, materia luminosa, spazio profondo non troppo nero",
    ),
    (
        "hero_object",
        "Oggetto centrale",
        "Come deve comportarsi l'oggetto centrale?",
        "sfera/aura viva con deformazione mesh completa su tutti i keyframe audio",
    ),
    (
        "background",
        "Sfondo",
        "Che sfondo vuoi?",
        "azzurro/verde sfumato coerente con cover, niente nero piatto, niente linee/pannelli visibili",
    ),
    (
        "fog",
        "Nebbia",
        "Come deve muoversi la nebbia?",
        "filamenti o banchi morbidi tipo fumo, visibili ma leggeri, compressi/decompressi dal suono",
    ),
    (
        "particles_orbits",
        "Particelle/orbite",
        "Che comportamento vuoi per satelliti/particelle?",
        "orbite attorno al centro come atomo musicale, mini-satelliti, emissione sugli oggetti fisici esistenti",
    ),
    (
        "materials_lights",
        "Materiali/luci",
        "Come devono reagire materiali e luci?",
        "materia + emissione fusi, luce generale stabile, no strobo forte, accenti su oggetti secondari",
    ),
    (
        "camera_motion",
        "Camera",
        "Che tipo di camera vuoi?",
        "movimento lento e musicale, micro pressione sui beat, niente scatti aggressivi",
    ),
    (
        "avoid",
        "Da evitare",
        "Cosa non vuoi vedere?",
        "placeholder, scena vuota, oggetti importati brutti, nero dominante, nebbia squadrettata, perdita di keyframe",
    ),
    (
        "render_target",
        "Target render",
        "A cosa deve stare attento il generatore per i tempi render?",
        "test veloce con NPU spenta, qualita alta ma evitando volumi pesanti e luci globali variabili",
    ),
    ("free_notes", "Note libere", "Aggiungi istruzioni extra per la scena.", ""),
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def append_scene_runtime_event(event: str, payload: dict) -> None:
    try:
        root = Path(__file__).resolve().parents[2]
        path = root / "output" / "workflow_logs" / "scene_director_runtime_events.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {"time": now_iso(), "event": event, "payload": payload}, ensure_ascii=False
                )
                + "\n"
            )
    except Exception:
        pass


def default_scene_preferences() -> dict[str, str]:
    return {field: default for field, _label, _question, default in QUESTION_FIELDS}


def compact_text(value: object, limit: int = 900) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def trim_jsonable(value: object, limit: int = 1200) -> object:
    if isinstance(value, dict):
        return {str(k): trim_jsonable(v, max(240, limit // 2)) for k, v in list(value.items())[:24]}
    if isinstance(value, list):
        return [trim_jsonable(item, max(240, limit // 2)) for item in value[:16]]
    if isinstance(value, str):
        return compact_text(value, limit)
    return value


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


def generate_scene_chat_reply(
    *,
    track_stem: str,
    audio_path: str,
    output_path: Path,
    user_message: str,
    model: str = "qwen2.5-coder:14b",
    asset_inventory_path: Path | None = None,
) -> str:
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

    npu_dir = Path(__file__).resolve().parents[1] / "npu"
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
        from ollama_runtime import OllamaSession, ollama_runtime_log_path  # type: ignore

        with OllamaSession(
            model=model,
            keep_alive="2m",
            shutdown_server=False,
            unload_model=False,
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
