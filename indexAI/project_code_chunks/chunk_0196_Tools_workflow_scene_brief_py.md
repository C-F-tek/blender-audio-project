# Project Code Chunk 196/212

- File: `Tools/workflow/scene_brief.py`
- Part: `3`
- Lines: `517-599`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `json`, `sys`, `from project_awareness import build_preflight_answers_for_message, build_project_awareness, deterministic_track_opinion, save_project_awareness`
- Functions: `now_iso()` line 82; `read_json(path)` line 86; `write_json(path, payload)` line 96; `default_scene_preferences()` line 101; `compact_text(value, limit)` line 105; `build_conversation_memory()` line 112; `load_or_create_scene_brief()` line 216; `append_scene_message()` line 240; `clear_scene_chat_history()` line 279; `compact_music_for_chat(music_context)` line 298; `classify_user_intent(user_message)` line 321; `compact_recent_conversation(transcript, limit)` line 332; `build_scene_chat_prompt(brief, user_message, asset_inventory, music_context, project_awareness, preflight_answers)` line 359; `sanitize_scene_reply(reply)` line 412; `generate_scene_chat_reply()` line 456; `build_scene_brief()` line 511; `prompt_value(label, question, default)` line 549; `run_interactive_scene_brief()` line 564
- Assignments: `MEMORY_VERSION`, `QUESTION_FIELDS`

## Content
```py
00517:     previous: dict | None = None,
00518: ) -> dict:
00519:     previous = previous or {}
00520:     active_transcript = transcript if transcript is not None else previous.get("conversation_transcript", [])
00521:     memory = build_conversation_memory(
00522:         preferences=preferences,
00523:         transcript=active_transcript,
00524:         previous=previous,
00525:     )
00526:     return {
00527:         "version": 1,
00528:         "kind": "spaziotempo_scene_director_brief",
00529:         "generated_at": now_iso(),
00530:         "track_stem": track_stem,
00531:         "audio_path": audio_path,
00532:         "scene_preferences": preferences,
00533:         "must_keep": [
00534:             "Use the full analysis_blender_keyframes JSON frames for animation.",
00535:             "Use compact music segments only for composition and macro decisions.",
00536:             "Create a standalone Blender Python scene script under indexAI/scene_scripts.",
00537:             "Do not modify existing project source files.",
00538:         ],
00539:         "workflow_policy": {
00540:             "npu_role": "optional compact service/router, not heavy generator",
00541:             "gpu_or_ollama_role": "heavy reasoning and code generation",
00542:             "manual_review_required": True,
00543:         },
00544:         "conversation_memory": memory,
00545:         "conversation_transcript": active_transcript,
00546:     }
00547: 
00548: 
00549: def prompt_value(label: str, question: str, default: str) -> tuple[str, dict]:
00550:     print(f"\n[{label}]")
00551:     print(question)
00552:     if default:
00553:         print(f"Default: {default}")
00554:     value = input("> ").strip()
00555:     answer = value or default
00556:     return answer, {
00557:         "label": label,
00558:         "question": question,
00559:         "default": default,
00560:         "answer": answer,
00561:     }
00562: 
00563: 
00564: def run_interactive_scene_brief(
00565:     *,
00566:     track_stem: str,
00567:     audio_path: str,
00568:     output_path: Path,
00569: ) -> dict:
00570:     previous = read_json(output_path)
00571:     previous_preferences = previous.get("scene_preferences") if isinstance(previous.get("scene_preferences"), dict) else {}
00572:     defaults = default_scene_preferences()
00573:     preferences: dict[str, str] = {}
00574:     transcript: list[dict] = []
00575: 
00576:     print("\n" + "=" * 72)
00577:     print("SPAZIOTEMPO SCENE DIRECTOR CHAT")
00578:     print("=" * 72)
00579:     print("Rispondi liberamente. Invio mantiene il default o la risposta precedente.")
00580:     print(f"Track: {track_stem}")
00581:     print(f"Output: {output_path}")
00582: 
00583:     for field, label, question, default in QUESTION_FIELDS:
00584:         current_default = str(previous_preferences.get(field) or defaults.get(field) or default)
00585:         answer, item = prompt_value(label, question, current_default)
00586:         preferences[field] = answer
00587:         item["field"] = field
00588:         transcript.append(item)
00589: 
00590:     brief = build_scene_brief(
00591:         track_stem=track_stem,
00592:         audio_path=audio_path,
00593:         preferences=preferences,
00594:         transcript=transcript,
00595:         previous=previous,
00596:     )
00597:     write_json(output_path, brief)
00598:     print(f"\n[OK] Scene director brief salvato: {output_path}")
00599:     return brief
```
