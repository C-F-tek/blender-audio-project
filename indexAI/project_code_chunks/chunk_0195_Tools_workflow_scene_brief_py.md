# Project Code Chunk 195/212

- File: `Tools/workflow/scene_brief.py`
- Part: `2`
- Lines: `286-516`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `json`, `sys`, `from project_awareness import build_preflight_answers_for_message, build_project_awareness, deterministic_track_opinion, save_project_awareness`
- Functions: `now_iso()` line 82; `read_json(path)` line 86; `write_json(path, payload)` line 96; `default_scene_preferences()` line 101; `compact_text(value, limit)` line 105; `build_conversation_memory()` line 112; `load_or_create_scene_brief()` line 216; `append_scene_message()` line 240; `clear_scene_chat_history()` line 279; `compact_music_for_chat(music_context)` line 298; `classify_user_intent(user_message)` line 321; `compact_recent_conversation(transcript, limit)` line 332; `build_scene_chat_prompt(brief, user_message, asset_inventory, music_context, project_awareness, preflight_answers)` line 359; `sanitize_scene_reply(reply)` line 412; `generate_scene_chat_reply()` line 456; `build_scene_brief()` line 511; `prompt_value(label, question, default)` line 549; `run_interactive_scene_brief()` line 564
- Assignments: `MEMORY_VERSION`, `QUESTION_FIELDS`

## Content
```py
00286:     updated = build_scene_brief(
00287:         track_stem=track_stem,
00288:         audio_path=audio_path,
00289:         preferences=preferences,
00290:         transcript=[],
00291:         previous={},
00292:     )
00293:     updated["chat_cleared_at"] = now_iso()
00294:     write_json(output_path, updated)
00295:     return updated
00296: 
00297: 
00298: def compact_music_for_chat(music_context: dict | None) -> dict:
00299:     music_context = music_context or {}
00300:     summary = music_context.get("analysis_summary") or {}
00301:     track = music_context.get("track_summary") or {}
00302:     segments = music_context.get("segments") or []
00303:     return {
00304:         "summary": summary,
00305:         "track_summary": track,
00306:         "segment_count": len(segments),
00307:         "first_segments": [
00308:             {
00309:                 "index": item.get("index"),
00310:                 "time": [item.get("start_sec"), item.get("end_sec")],
00311:                 "dominant_band": item.get("dominant_band"),
00312:                 "intensity": item.get("intensity"),
00313:                 "intensity_score": item.get("intensity_score"),
00314:                 "controls": item.get("controls"),
00315:             }
00316:             for item in segments[:8]
00317:         ],
00318:     }
00319: 
00320: 
00321: def classify_user_intent(user_message: str) -> str:
00322:     text = user_message.lower().strip()
00323:     if "script" in text or "codice" in text or "python" in text:
00324:         return "script_or_code_request"
00325:     if "cosa pensi" in text or "che ne pensi" in text or text.endswith("?"):
00326:         return "opinion_or_question"
00327:     if any(word in text for word in ["vorrei", "aggiungi", "modifica", "crea", "usa", "togli", "deve"]):
00328:         return "scene_change_request"
00329:     return "director_note"
00330: 
00331: 
00332: def compact_recent_conversation(transcript: list[dict] | None, limit: int = 12) -> list[dict]:
00333:     transcript = transcript or []
00334:     result: list[dict] = []
00335:     boilerplate_markers = (
00336:         "certo, posso aiutarti",
00337:         "brief aggiornato",
00338:         "### brief",
00339:         "istruzioni operative",
00340:         "coldplay",
00341:         "new beginnings",
00342:     )
00343:     for item in transcript:
00344:         role = str(item.get("role") or "note").lower()
00345:         content = str(item.get("content") or item.get("answer") or "")
00346:         lowered = content.lower()
00347:         if role == "assistant" and any(marker in lowered for marker in boilerplate_markers):
00348:             continue
00349:         result.append(
00350:             {
00351:                 "time": item.get("time"),
00352:                 "role": role,
00353:                 "content": compact_text(content, 700),
00354:             }
00355:         )
00356:     return result[-limit:]
00357: 
00358: 
00359: def build_scene_chat_prompt(
00360:     brief: dict,
00361:     user_message: str,
00362:     asset_inventory: dict | None = None,
00363:     music_context: dict | None = None,
00364:     project_awareness: dict | None = None,
00365:     preflight_answers: list[dict] | None = None,
00366: ) -> str:
00367:     intent = classify_user_intent(user_message)
00368:     compact = {
00369:         "track_stem": brief.get("track_stem"),
00370:         "audio_path": brief.get("audio_path"),
00371:         "user_intent": intent,
00372:         "scene_preferences": brief.get("scene_preferences"),
00373:         "must_keep": brief.get("must_keep"),
00374:         "workflow_policy": brief.get("workflow_policy"),
00375:         "conversation_memory": brief.get("conversation_memory"),
00376:         "project_awareness": project_awareness,
00377:         "preflight_answers": preflight_answers or [],
00378:         "music_context": compact_music_for_chat(music_context),
00379:         "known_assets": (asset_inventory or {}).get("assets", [])[:30],
00380:         "asset_notes": (asset_inventory or {}).get("notes", []),
00381:         "recent_conversation": compact_recent_conversation(brief.get("conversation_transcript"), limit=12),
00382:         "user_message": user_message,
00383:     }
00384:     return f"""
00385: Sei il regista tecnico locale del progetto Blender Spaziotempo.
00386: NON sei un consulente Blender generico: conosci lo stato corrente del progetto tramite project_awareness.
00387: Identita brano: usa solo project_awareness.track_identity. Vietato inventare artista/titolo esterno.
00388: 
00389: Rispondi in italiano, breve ma utile.
00390: Non ripetere il brief intero e non iniziare con formule tipo "Certo, posso aiutarti".
00391: Non generare ancora tutto lo script Blender nella chat: devi dirigere, chiarire e decidere.
00392: Prima di rispondere, controlla project_awareness.pipeline_state e project_awareness.technical_files.
00393: Usa preflight_answers come risposta NPU/service gia verificata: non contraddirla.
00394: Se preflight_answers contiene una lettura del brano, usa quella come base. Non citare Coldplay, New Beginnings o altri brani esterni.
00395: Se i file tecnici sono presenti, non suggerire di importare audio, aprire Blender o rifare setup manuali gia coperti dalla pipeline.
00396: Se manca qualcosa, nomina il file tecnico o l'operazione pipeline precisa, non un consiglio generico.
00397: Se hai un dubbio tecnico, usa project_awareness.npu_context: se NPU e pronta puoi dire quale chunk/file delegare; se non e pronta usa i file tecnici gia presenti e segnala il dubbio.
00398: Vietato scrivere frasi come "assicurati di avere il file WAV", "importa l'audio in Blender", "apri Blender e aggiungi l'audio", se project_awareness dice che l'analisi e pronta.
00399: Se user_intent e' opinion_or_question, rispondi alla domanda usando music_context e memoria, con giudizio artistico concreto.
00400: Se user_intent e' scene_change_request, salva mentalmente la modifica e dai 2-5 punti tecnici precisi su cosa cambiera'.
00401: Se user_intent e' script_or_code_request, spiega quale pipeline/tasto genera codice e quali vincoli dovra' rispettare.
00402: Se manca un dettaglio importante, fai al massimo una domanda.
00403: Ricorda sempre: i keyframe completi del file analysis_blender_keyframes.json non vanno persi.
00404: Se l'utente nomina asset gia presenti, consulta known_assets. Per esempio `primary_ball_asset` e' una ball importabile, non una sfera generica da inventare.
00405: Per la richiesta "due oggetti centrali ball opposti": considera due istanze/import dello stesso primary_ball_asset, materiale/emissione complementare, deformazione e rotazione in controfase, stessi full keyframes ma mapping low/mid/high invertito.
00406: 
00407: Contesto:
00408: {json.dumps(compact, indent=2, ensure_ascii=False)}
00409: """.strip()
00410: 
00411: 
00412: def sanitize_scene_reply(reply: str, *, awareness: dict, preflight_answers: list[dict]) -> str:
00413:     if not reply:
00414:         return ""
00415:     lowered = reply.lower()
00416:     forbidden_markers = [
00417:         "assicurati di avere il file wav",
00418:         "assicurati che il file wav",
00419:         "importa l'audio in blender",
00420:         "importare l'audio in blender",
00421:         "apri blender e importa",
00422:         "aggiungi l'audio in blender",
00423:         "carica il file wav in blender",
00424:         "coldplay",
00425:         "new beginnings",
00426:     ]
00427:     if not any(marker in lowered for marker in forbidden_markers):
00428:         return reply
00429: 
00430:     if "coldplay" in lowered or "new beginnings" in lowered:
00431:         track_identity = awareness.get("track_identity", {})
00432:         files = awareness.get("technical_files", {})
00433:         music_context = read_json(Path(files.get("music_context_json", {}).get("path", "")))
00434:         return deterministic_track_opinion(track_identity, music_context)
00435: 
00436:     correction = [
00437:         "Correzione di contesto progetto: non serve importare manualmente il WAV in Blender.",
00438:     ]
00439:     for item in preflight_answers:
00440:         answer = str(item.get("answer") or "").strip()
00441:         if answer:
00442:             correction.append(f"- {answer}")
00443:     if not preflight_answers:
00444:         files = awareness.get("technical_files", {})
00445:         keyframes = files.get("blender_keyframes_json", {})
00446:         correction.append(f"- Usa il JSON keyframe completo: {keyframes.get('path')}")
00447:     correction.append("")
00448:     correction.append("Risposta utile nel nostro flusso:")
00449:     cleaned = reply
00450:     for marker in forbidden_markers:
00451:         cleaned = cleaned.replace(marker, "[rimosso: consiglio generico non valido per questo progetto]")
00452:         cleaned = cleaned.replace(marker.capitalize(), "[rimosso: consiglio generico non valido per questo progetto]")
00453:     return "\n".join(correction) + "\n" + cleaned.strip()
00454: 
00455: 
00456: def generate_scene_chat_reply(
00457:     *,
00458:     track_stem: str,
00459:     audio_path: str,
00460:     output_path: Path,
00461:     user_message: str,
00462:     model: str = "qwen2.5-coder:14b",
00463:     asset_inventory_path: Path | None = None,
00464: ) -> str:
00465:     brief = load_or_create_scene_brief(track_stem=track_stem, audio_path=audio_path, output_path=output_path)
00466:     asset_inventory = read_json(asset_inventory_path) if asset_inventory_path else {}
00467:     music_context_path = output_path.with_name(f"{track_stem}_music_context.json")
00468:     music_context = read_json(music_context_path)
00469:     awareness = build_project_awareness(
00470:         track_stem=track_stem,
00471:         audio_path=audio_path,
00472:         output_dir=output_path.parent,
00473:         asset_inventory=asset_inventory,
00474:         music_context=music_context,
00475:     )
00476:     save_project_awareness(awareness)
00477:     preflight_answers = build_preflight_answers_for_message(user_message, awareness, music_context)
00478:     prompt = build_scene_chat_prompt(brief, user_message, asset_inventory, music_context, awareness, preflight_answers)
00479: 
00480:     npu_dir = Path(__file__).resolve().parents[1] / "npu"
00481:     if str(npu_dir) not in sys.path:
00482:         sys.path.insert(0, str(npu_dir))
00483: 
00484:     try:
00485:         from ollama_runtime import OllamaSession  # type: ignore
00486: 
00487:         with OllamaSession(model=model, keep_alive="2m", shutdown_server=False, unload_model=False, startup_timeout=20.0) as session:
00488:             reply = session.generate(prompt, max_new_tokens=1200, temperature=0.18)
00489:     except Exception as exc:
00490:         reply = (
00491:             "Errore chiamando Ollama: "
00492:             f"{exc}\n\n"
00493:             "Il tuo messaggio e' comunque salvato nel brief; puoi generare lo script anche senza risposta chat."
00494:         )
00495: 
00496:     reply = sanitize_scene_reply(
00497:         reply.strip(),
00498:         awareness=awareness,
00499:         preflight_answers=preflight_answers,
00500:     ) or "Ollama non ha restituito testo. Il messaggio utente e' comunque salvato nel brief."
00501:     append_scene_message(
00502:         track_stem=track_stem,
00503:         audio_path=audio_path,
00504:         output_path=output_path,
00505:         role="assistant",
00506:         content=reply,
00507:     )
00508:     return reply
00509: 
00510: 
00511: def build_scene_brief(
00512:     *,
00513:     track_stem: str,
00514:     audio_path: str,
00515:     preferences: dict[str, str],
00516:     transcript: list[dict] | None = None,
```
