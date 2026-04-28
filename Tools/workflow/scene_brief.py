from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import sys

from project_awareness import (
    build_preflight_answers_for_message,
    build_project_awareness,
    deterministic_track_opinion,
    save_project_awareness,
)

MEMORY_VERSION = 3


QUESTION_FIELDS = [
    ("creative_intent", "Idea generale / mood", "Che sensazione deve dare la scena?", "cinematica, audio-reactive, materia luminosa, spazio profondo non troppo nero"),
    ("hero_object", "Oggetto centrale", "Come deve comportarsi l'oggetto centrale?", "sfera/aura viva con deformazione mesh completa su tutti i keyframe audio"),
    ("background", "Sfondo", "Che sfondo vuoi?", "azzurro/verde sfumato coerente con cover, niente nero piatto, niente linee/pannelli visibili"),
    ("fog", "Nebbia", "Come deve muoversi la nebbia?", "filamenti o banchi morbidi tipo fumo, visibili ma leggeri, compressi/decompressi dal suono"),
    ("particles_orbits", "Particelle/orbite", "Che comportamento vuoi per satelliti/particelle?", "orbite attorno al centro come atomo musicale, mini-satelliti, emissione sugli oggetti fisici esistenti"),
    ("materials_lights", "Materiali/luci", "Come devono reagire materiali e luci?", "materia + emissione fusi, luce generale stabile, no strobo forte, accenti su oggetti secondari"),
    ("camera_motion", "Camera", "Che tipo di camera vuoi?", "movimento lento e musicale, micro pressione sui beat, niente scatti aggressivi"),
    ("avoid", "Da evitare", "Cosa non vuoi vedere?", "placeholder, scena vuota, oggetti importati brutti, nero dominante, nebbia squadrettata, perdita di keyframe"),
    ("render_target", "Target render", "A cosa deve stare attento il generatore per i tempi render?", "test veloce con NPU spenta, qualita alta ma evitando volumi pesanti e luci globali variabili"),
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
            handle.write(json.dumps({"time": now_iso(), "event": event, "payload": payload}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def default_scene_preferences() -> dict[str, str]:
    return {field: default for field, _label, _question, default in QUESTION_FIELDS}


def compact_text(value: str, limit: int = 900) -> str:
    value = " ".join(str(value or "").split())
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 3)].rstrip() + "..."


def build_conversation_memory(*, preferences: dict[str, str], transcript: list[dict] | None, previous: dict | None = None) -> dict:
    previous = previous or {}
    transcript = transcript or []
    user_requests: list[str] = []
    assistant_notes: list[str] = []
    asset_mentions: list[str] = []
    durable_constraints: list[str] = []
    question_history: list[str] = []

    boilerplate_markers = ("certo, posso aiutarti", "brief aggiornato", "istruzioni operative", "traccia audio", "percorso audio", "coldplay", "new beginnings")
    keywords = ("keyframe", "audio", "asset", "ball", "sfera", "hero", "aura", "fog", "nebbia", "luce", "emission", "nero", "sfondo", "render", "npu", "ollama", "gpu", "script", "blender", "memoria", "chat")

    for item in transcript:
        role = str(item.get("role") or "note").lower()
        content = str(item.get("content") or item.get("answer") or "").strip()
        if not content:
            continue
        lowered = content.lower()
        if role == "user":
            user_requests.append(compact_text(content, 500))
            if "?" in content or lowered.startswith(("cosa", "come", "perche", "perché", "quale", "dimmi")):
                question_history.append(compact_text(content, 260))
            if any(word in lowered for word in keywords):
                durable_constraints.append(compact_text(content, 420))
        elif role == "assistant":
            if not any(marker in lowered for marker in boilerplate_markers):
                if any(marker in lowered for marker in ("salvato", "applicher", "usero", "uso", "pipeline", "script")):
                    assistant_notes.append(compact_text(content, 300))
        for token in ("ball", "primary_ball_asset", "fbx", "cover", "manual", "indexai"):
            if token.lower() in lowered:
                asset_mentions.append(token)

    preference_summary = [f"{key}: {compact_text(value, 260)}" for key, value in preferences.items() if value]
    previous_memory = previous.get("conversation_memory") if isinstance(previous.get("conversation_memory"), dict) else {}
    previous_constraints = previous_memory.get("durable_constraints") if isinstance(previous_memory, dict) else []
    if isinstance(previous_constraints, list) and previous_memory.get("memory_version") == MEMORY_VERSION:
        durable_constraints = [str(item) for item in previous_constraints] + durable_constraints

    def unique_recent(values: list[str], limit: int) -> list[str]:
        seen = set()
        result = []
        for value in values:
            key = value.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            result.append(value)
        return result[-limit:]

    return {
        "updated_at": now_iso(),
        "memory_version": MEMORY_VERSION,
        "message_count": len(transcript),
        "preference_summary": preference_summary,
        "recent_user_requests": user_requests[-18:],
        "recent_user_questions": question_history[-8:],
        "recent_assistant_notes": assistant_notes[-10:],
        "durable_constraints": unique_recent(durable_constraints, 24),
        "asset_mentions": sorted(set(asset_mentions)),
        "memory_policy": "This compact memory is always passed to the local chat/model; recent_conversation is only the short working window.",
    }


def load_or_create_scene_brief(*, track_stem: str, audio_path: str, output_path: Path) -> dict:
    existing = read_json(output_path)
    if existing:
        memory = existing.get("conversation_memory") if isinstance(existing.get("conversation_memory"), dict) else {}
        if memory.get("memory_version") != MEMORY_VERSION:
            preferences = existing.get("scene_preferences") if isinstance(existing.get("scene_preferences"), dict) else default_scene_preferences()
            transcript = existing.get("conversation_transcript") if isinstance(existing.get("conversation_transcript"), list) else []
            existing["conversation_memory"] = build_conversation_memory(preferences={key: str(value) for key, value in preferences.items()}, transcript=transcript, previous=existing)
            write_json(output_path, existing)
        return existing
    brief = build_scene_brief(track_stem=track_stem, audio_path=audio_path, preferences=default_scene_preferences(), transcript=[])
    write_json(output_path, brief)
    return brief


def append_scene_message(*, track_stem: str, audio_path: str, output_path: Path, role: str, content: str) -> dict:
    brief = load_or_create_scene_brief(track_stem=track_stem, audio_path=audio_path, output_path=output_path)
    transcript = brief.get("conversation_transcript")
    if not isinstance(transcript, list):
        transcript = []
    transcript.append({"time": now_iso(), "role": role, "content": content})

    preferences = brief.get("scene_preferences")
    if not isinstance(preferences, dict):
        preferences = default_scene_preferences()

    if role == "user":
        current_notes = str(preferences.get("free_notes") or "").strip()
        preferences["free_notes"] = (current_notes + "\n" + content).strip() if current_notes else content

    updated = build_scene_brief(track_stem=track_stem, audio_path=audio_path, preferences={key: str(value) for key, value in preferences.items()}, transcript=transcript, previous=brief)
    write_json(output_path, updated)
    return updated


def clear_scene_chat_history(*, track_stem: str, audio_path: str, output_path: Path) -> dict:
    brief = load_or_create_scene_brief(track_stem=track_stem, audio_path=audio_path, output_path=output_path)
    preferences = brief.get("scene_preferences")
    if not isinstance(preferences, dict):
        preferences = default_scene_preferences()
    preferences = {key: str(value) for key, value in preferences.items()}
    preferences["free_notes"] = ""
    updated = build_scene_brief(track_stem=track_stem, audio_path=audio_path, preferences=preferences, transcript=[], previous={})
    updated["chat_cleared_at"] = now_iso()
    write_json(output_path, updated)
    return updated


def compact_music_for_chat(music_context: dict | None) -> dict:
    music_context = music_context or {}
    summary = music_context.get("analysis_summary") or {}
    track = music_context.get("track_summary") or {}
    segments = music_context.get("segments") or []
    return {
        "summary": summary,
        "track_summary": track,
        "segment_count": len(segments),
        "first_segments": [
            {"index": item.get("index"), "time": [item.get("start_sec"), item.get("end_sec")], "dominant_band": item.get("dominant_band"), "intensity": item.get("intensity"), "intensity_score": item.get("intensity_score"), "controls": item.get("controls")}
            for item in segments[:8]
        ],
    }


def classify_user_intent(user_message: str) -> str:
    text = user_message.lower().strip()
    if "script" in text or "codice" in text or "python" in text:
        return "script_or_code_request"
    if "cosa pensi" in text or "che ne pensi" in text or text.endswith("?"):
        return "opinion_or_question"
    if any(word in text for word in ["vorrei", "aggiungi", "modifica", "crea", "usa", "togli", "deve", "procedi", "analizza"]):
        return "scene_change_request"
    return "director_note"


def compact_recent_conversation(transcript: list[dict] | None, limit: int = 12) -> list[dict]:
    transcript = transcript or []
    result: list[dict] = []
    boilerplate_markers = ("certo, posso aiutarti", "brief aggiornato", "### brief", "istruzioni operative", "coldplay", "new beginnings")
    for item in transcript:
        role = str(item.get("role") or "note").lower()
        content = str(item.get("content") or item.get("answer") or "")
        lowered = content.lower()
        if role == "assistant" and any(marker in lowered for marker in boilerplate_markers):
            continue
        result.append({"time": item.get("time"), "role": role, "content": compact_text(content, 700)})
    return result[-limit:]


def build_scene_chat_prompt(brief: dict, user_message: str, asset_inventory: dict | None = None, music_context: dict | None = None, project_awareness: dict | None = None, preflight_answers: list[dict] | None = None) -> str:
    intent = classify_user_intent(user_message)
    compact = {
        "track_stem": brief.get("track_stem"),
        "audio_path": brief.get("audio_path"),
        "user_intent": intent,
        "scene_preferences": brief.get("scene_preferences"),
        "must_keep": brief.get("must_keep"),
        "workflow_policy": brief.get("workflow_policy"),
        "conversation_memory": brief.get("conversation_memory"),
        "project_awareness": project_awareness,
        "preflight_answers": preflight_answers or [],
        "music_context": compact_music_for_chat(music_context),
        "known_assets": (asset_inventory or {}).get("assets", [])[:30],
        "asset_notes": (asset_inventory or {}).get("notes", []),
        "recent_conversation": compact_recent_conversation(brief.get("conversation_transcript"), limit=12),
        "user_message": user_message,
    }
    return f"""
Sei il regista tecnico locale del progetto Blender Spaziotempo.
NON sei un consulente Blender generico: conosci lo stato corrente del progetto tramite project_awareness.
Identita brano: usa solo project_awareness.track_identity. Vietato inventare artista/titolo esterno.

Rispondi in italiano, breve ma utile.
Non ripetere il brief intero e non iniziare con formule tipo "Certo, posso aiutarti".
Non generare ancora tutto lo script Blender nella chat: devi dirigere, chiarire e decidere.
Prima di rispondere, controlla project_awareness.pipeline_state e project_awareness.technical_files.
Usa preflight_answers come risposta NPU/service gia verificata: non contraddirla.
Se preflight_answers contiene una lettura del brano, usa quella come base. Non citare Coldplay, New Beginnings o altri brani esterni.
Se i file tecnici sono presenti, non suggerire di importare audio, aprire Blender o rifare setup manuali gia coperti dalla pipeline.
Se manca qualcosa, nomina il file tecnico o l'operazione pipeline precisa, non un consiglio generico.
Se hai un dubbio tecnico, usa project_awareness.npu_context: se NPU e pronta puoi dire quale chunk/file delegare; se non e pronta usa i file tecnici gia presenti e segnala il dubbio.
Vietato scrivere frasi come "assicurati di avere il file WAV", "importa l'audio in Blender", "apri Blender e aggiungi l'audio", se project_awareness dice che l'analisi e pronta.
Se user_intent e' opinion_or_question, rispondi alla domanda usando music_context e memoria, con giudizio artistico concreto.
Se user_intent e' scene_change_request, salva mentalmente la modifica e dai 2-5 punti tecnici precisi su cosa cambiera'.
Se user_intent e' script_or_code_request, spiega quale pipeline/tasto genera codice e quali vincoli dovra' rispettare.
Se manca un dettaglio importante, fai al massimo una domanda.
Ricorda sempre: i keyframe completi del file analysis_blender_keyframes.json non vanno persi.

Contesto:
{json.dumps(compact, indent=2, ensure_ascii=False)}
""".strip()


def deterministic_scene_director_reply(*, user_message: str, awareness: dict, music_context: dict, response_meta: dict) -> str:
    files = awareness.get("technical_files", {}) if isinstance(awareness, dict) else {}
    pipeline = awareness.get("pipeline_state", {}) if isinstance(awareness, dict) else {}
    track_identity = awareness.get("track_identity", {}) if isinstance(awareness, dict) else {}
    music = compact_music_for_chat(music_context)
    track_name = track_identity.get("track_stem") or awareness.get("track_stem") or "traccia corrente"
    keyframes_path = (files.get("blender_keyframes_json") or {}).get("path") if isinstance(files.get("blender_keyframes_json"), dict) else None
    music_path = (files.get("music_context_json") or {}).get("path") if isinstance(files.get("music_context_json"), dict) else None
    intent = classify_user_intent(user_message)
    return "\n".join([
        "Fallback regia tecnica attivo: Ollama non ha prodotto una risposta utilizzabile, quindi uso i dati locali gia disponibili.",
        f"Brano/sessione: {track_name}.",
        f"Intento rilevato: {intent}.",
        "Decisione operativa:",
        "- Usa i file tecnici gia generati; non rifare import manuali in Blender.",
        f"- Keyframe autorevoli: {keyframes_path or 'analysis_blender_keyframes.json non rilevato nel project awareness'}.",
        f"- Contesto musicale compatto: {music_path or 'music_context_json non rilevato'}.",
        f"- Segmenti musicali disponibili: {music.get('segment_count', 0)}.",
        "- Per la prossima generazione script: mantenere tutti i frame JSON, usare materiali/emissione/fog/camera come reazione audio, evitare placeholder e scene minime.",
        "- Se vuoi una direzione alien/futuristic, applico: doppio centro luminoso in controfase, orbite audio-reactive, fog volumetrico leggero, emissioni controllate sui beat e camera lenta con micro-pressioni.",
        "Diagnostica:",
        f"- Modello chat: {response_meta.get('selected_model') or response_meta.get('model')}",
        f"- prompt_chars: {response_meta.get('prompt_chars')}",
        f"- log Ollama: {response_meta.get('ollama_runtime_log', 'output/workflow_logs/ollama_runtime_events.jsonl')}",
    ])


def sanitize_scene_reply(reply: str, *, awareness: dict, preflight_answers: list[dict]) -> str:
    if not reply:
        return ""
    lowered = reply.lower()
    forbidden_markers = ["assicurati di avere il file wav", "assicurati che il file wav", "importa l'audio in blender", "importare l'audio in blender", "apri blender e importa", "aggiungi l'audio in blender", "carica il file wav in blender", "coldplay", "new beginnings"]
    if not any(marker in lowered for marker in forbidden_markers):
        return reply
    if "coldplay" in lowered or "new beginnings" in lowered:
        track_identity = awareness.get("track_identity", {})
        files = awareness.get("technical_files", {})
        music_context = read_json(Path(files.get("music_context_json", {}).get("path", "")))
        return deterministic_track_opinion(track_identity, music_context)
    correction = ["Correzione di contesto progetto: non serve importare manualmente il WAV in Blender."]
    for item in preflight_answers:
        answer = str(item.get("answer") or "").strip()
        if answer:
            correction.append(f"- {answer}")
    if not preflight_answers:
        files = awareness.get("technical_files", {})
        keyframes = files.get("blender_keyframes_json", {})
        correction.append(f"- Usa il JSON keyframe completo: {keyframes.get('path')}")
    correction.append("")
    correction.append("Risposta utile nel nostro flusso:")
    cleaned = reply
    for marker in forbidden_markers:
        cleaned = cleaned.replace(marker, "[rimosso: consiglio generico non valido per questo progetto]")
        cleaned = cleaned.replace(marker.capitalize(), "[rimosso: consiglio generico non valido per questo progetto]")
    return "\n".join(correction) + "\n" + cleaned.strip()


def generate_scene_chat_reply(*, track_stem: str, audio_path: str, output_path: Path, user_message: str, model: str = "qwen2.5-coder:14b", asset_inventory_path: Path | None = None) -> str:
    brief = load_or_create_scene_brief(track_stem=track_stem, audio_path=audio_path, output_path=output_path)
    asset_inventory = read_json(asset_inventory_path) if asset_inventory_path else {}
    music_context_path = output_path.with_name(f"{track_stem}_music_context.json")
    music_context = read_json(music_context_path)
    awareness = build_project_awareness(track_stem=track_stem, audio_path=audio_path, output_dir=output_path.parent, asset_inventory=asset_inventory, music_context=music_context)
    save_project_awareness(awareness)
    preflight_answers = build_preflight_answers_for_message(user_message, awareness, music_context)
    prompt = build_scene_chat_prompt(brief, user_message, asset_inventory, music_context, awareness, preflight_answers)
    npu_dir = Path(__file__).resolve().parents[1] / "npu"
    if str(npu_dir) not in sys.path:
        sys.path.insert(0, str(npu_dir))
    response_meta: dict = {"track_stem": track_stem, "model": model, "prompt_chars": len(prompt), "user_message_chars": len(user_message), "output_path": str(output_path)}
    try:
        from ollama_runtime import OllamaSession, ollama_runtime_log_path  # type: ignore
        with OllamaSession(model=model, keep_alive="2m", shutdown_server=False, unload_model=False, startup_timeout=20.0) as session:
            reply = session.generate(prompt, max_new_tokens=1200, temperature=0.18)
            response_meta["selected_model"] = session.model
            response_meta["ollama_runtime_log"] = str(ollama_runtime_log_path())
    except Exception as exc:
        response_meta["error_type"] = type(exc).__name__
        response_meta["error"] = str(exc)
        append_scene_runtime_event("scene_chat_error", response_meta)
        reply = ""
    raw_reply_chars = len(str(reply or ""))
    response_meta["raw_reply_chars"] = raw_reply_chars
    response_meta["empty_response"] = raw_reply_chars == 0
    if raw_reply_chars == 0:
        append_scene_runtime_event("scene_chat_empty_response", response_meta)
    else:
        append_scene_runtime_event("scene_chat_response", response_meta)
    reply = sanitize_scene_reply(str(reply or "").strip(), awareness=awareness, preflight_answers=preflight_answers)
    if not reply:
        reply = deterministic_scene_director_reply(user_message=user_message, awareness=awareness, music_context=music_context, response_meta=response_meta)
    append_scene_message(track_stem=track_stem, audio_path=audio_path, output_path=output_path, role="assistant", content=reply)
    return reply


def build_scene_brief(*, track_stem: str, audio_path: str, preferences: dict[str, str], transcript: list[dict] | None = None, previous: dict | None = None) -> dict:
    previous = previous or {}
    active_transcript = transcript if transcript is not None else previous.get("conversation_transcript", [])
    memory = build_conversation_memory(preferences=preferences, transcript=active_transcript, previous=previous)
    return {
        "version": 1,
        "kind": "spaziotempo_scene_director_brief",
        "generated_at": now_iso(),
        "track_stem": track_stem,
        "audio_path": audio_path,
        "scene_preferences": preferences,
        "must_keep": ["Use the full analysis_blender_keyframes JSON frames for animation.", "Use compact music segments only for composition and macro decisions.", "Create a standalone Blender Python scene script under indexAI/scene_scripts.", "Do not modify existing project source files."],
        "workflow_policy": {"npu_role": "optional compact service/router, not heavy generator", "gpu_or_ollama_role": "heavy reasoning and code generation", "manual_review_required": True},
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
    previous_preferences = previous.get("scene_preferences") if isinstance(previous.get("scene_preferences"), dict) else {}
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
    brief = build_scene_brief(track_stem=track_stem, audio_path=audio_path, preferences=preferences, transcript=transcript, previous=previous)
    write_json(output_path, brief)
    print(f"\n[OK] Scene director brief salvato: {output_path}")
    return brief
