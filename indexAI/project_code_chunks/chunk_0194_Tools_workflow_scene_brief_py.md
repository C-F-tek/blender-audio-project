# Project Code Chunk 194/212

- File: `Tools/workflow/scene_brief.py`
- Part: `1`
- Lines: `1-285`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `json`, `sys`, `from project_awareness import build_preflight_answers_for_message, build_project_awareness, deterministic_track_opinion, save_project_awareness`
- Functions: `now_iso()` line 82; `read_json(path)` line 86; `write_json(path, payload)` line 96; `default_scene_preferences()` line 101; `compact_text(value, limit)` line 105; `build_conversation_memory()` line 112; `load_or_create_scene_brief()` line 216; `append_scene_message()` line 240; `clear_scene_chat_history()` line 279; `compact_music_for_chat(music_context)` line 298; `classify_user_intent(user_message)` line 321; `compact_recent_conversation(transcript, limit)` line 332; `build_scene_chat_prompt(brief, user_message, asset_inventory, music_context, project_awareness, preflight_answers)` line 359; `sanitize_scene_reply(reply)` line 412; `generate_scene_chat_reply()` line 456; `build_scene_brief()` line 511; `prompt_value(label, question, default)` line 549; `run_interactive_scene_brief()` line 564
- Assignments: `MEMORY_VERSION`, `QUESTION_FIELDS`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from datetime import datetime
00004: from pathlib import Path
00005: import json
00006: import sys
00007: 
00008: from project_awareness import (
00009:     build_preflight_answers_for_message,
00010:     build_project_awareness,
00011:     deterministic_track_opinion,
00012:     save_project_awareness,
00013: )
00014: 
00015: MEMORY_VERSION = 3
00016: 
00017: 
00018: QUESTION_FIELDS = [
00019:     (
00020:         "creative_intent",
00021:         "Idea generale / mood",
00022:         "Che sensazione deve dare la scena?",
00023:         "cinematica, audio-reactive, materia luminosa, spazio profondo non troppo nero",
00024:     ),
00025:     (
00026:         "hero_object",
00027:         "Oggetto centrale",
00028:         "Come deve comportarsi l'oggetto centrale?",
00029:         "sfera/aura viva con deformazione mesh completa su tutti i keyframe audio",
00030:     ),
00031:     (
00032:         "background",
00033:         "Sfondo",
00034:         "Che sfondo vuoi?",
00035:         "azzurro/verde sfumato coerente con cover, niente nero piatto, niente linee/pannelli visibili",
00036:     ),
00037:     (
00038:         "fog",
00039:         "Nebbia",
00040:         "Come deve muoversi la nebbia?",
00041:         "filamenti o banchi morbidi tipo fumo, visibili ma leggeri, compressi/decompressi dal suono",
00042:     ),
00043:     (
00044:         "particles_orbits",
00045:         "Particelle/orbite",
00046:         "Che comportamento vuoi per satelliti/particelle?",
00047:         "orbite attorno al centro come atomo musicale, mini-satelliti, emissione sugli oggetti fisici esistenti",
00048:     ),
00049:     (
00050:         "materials_lights",
00051:         "Materiali/luci",
00052:         "Come devono reagire materiali e luci?",
00053:         "materia + emissione fusi, luce generale stabile, no strobo forte, accenti su oggetti secondari",
00054:     ),
00055:     (
00056:         "camera_motion",
00057:         "Camera",
00058:         "Che tipo di camera vuoi?",
00059:         "movimento lento e musicale, micro pressione sui beat, niente scatti aggressivi",
00060:     ),
00061:     (
00062:         "avoid",
00063:         "Da evitare",
00064:         "Cosa non vuoi vedere?",
00065:         "placeholder, scena vuota, oggetti importati brutti, nero dominante, nebbia squadrettata, perdita di keyframe",
00066:     ),
00067:     (
00068:         "render_target",
00069:         "Target render",
00070:         "A cosa deve stare attento il generatore per i tempi render?",
00071:         "test veloce con NPU spenta, qualita alta ma evitando volumi pesanti e luci globali variabili",
00072:     ),
00073:     (
00074:         "free_notes",
00075:         "Note libere",
00076:         "Aggiungi istruzioni extra per la scena.",
00077:         "",
00078:     ),
00079: ]
00080: 
00081: 
00082: def now_iso() -> str:
00083:     return datetime.now().isoformat(timespec="seconds")
00084: 
00085: 
00086: def read_json(path: Path) -> dict:
00087:     if not path.exists():
00088:         return {}
00089:     try:
00090:         data = json.loads(path.read_text(encoding="utf-8"))
00091:     except Exception:
00092:         return {}
00093:     return data if isinstance(data, dict) else {}
00094: 
00095: 
00096: def write_json(path: Path, payload: dict) -> None:
00097:     path.parent.mkdir(parents=True, exist_ok=True)
00098:     path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
00099: 
00100: 
00101: def default_scene_preferences() -> dict[str, str]:
00102:     return {field: default for field, _label, _question, default in QUESTION_FIELDS}
00103: 
00104: 
00105: def compact_text(value: str, limit: int = 900) -> str:
00106:     value = " ".join(str(value or "").split())
00107:     if len(value) <= limit:
00108:         return value
00109:     return value[: max(0, limit - 3)].rstrip() + "..."
00110: 
00111: 
00112: def build_conversation_memory(
00113:     *,
00114:     preferences: dict[str, str],
00115:     transcript: list[dict] | None,
00116:     previous: dict | None = None,
00117: ) -> dict:
00118:     previous = previous or {}
00119:     transcript = transcript or []
00120:     user_requests: list[str] = []
00121:     assistant_notes: list[str] = []
00122:     asset_mentions: list[str] = []
00123:     durable_constraints: list[str] = []
00124:     question_history: list[str] = []
00125: 
00126:     boilerplate_markers = (
00127:         "certo, posso aiutarti",
00128:         "brief aggiornato",
00129:         "istruzioni operative",
00130:         "traccia audio",
00131:         "percorso audio",
00132:         "coldplay",
00133:         "new beginnings",
00134:     )
00135: 
00136:     keywords = (
00137:         "keyframe",
00138:         "audio",
00139:         "asset",
00140:         "ball",
00141:         "sfera",
00142:         "hero",
00143:         "aura",
00144:         "fog",
00145:         "nebbia",
00146:         "luce",
00147:         "emission",
00148:         "nero",
00149:         "sfondo",
00150:         "render",
00151:         "npu",
00152:         "ollama",
00153:         "gpu",
00154:         "script",
00155:         "blender",
00156:         "memoria",
00157:         "chat",
00158:     )
00159: 
00160:     for item in transcript:
00161:         role = str(item.get("role") or "note").lower()
00162:         content = str(item.get("content") or item.get("answer") or "").strip()
00163:         if not content:
00164:             continue
00165:         lowered = content.lower()
00166:         if role == "user":
00167:             user_requests.append(compact_text(content, 500))
00168:             if "?" in content or lowered.startswith(("cosa", "come", "perche", "perché", "quale", "dimmi")):
00169:                 question_history.append(compact_text(content, 260))
00170:             if any(word in lowered for word in keywords):
00171:                 durable_constraints.append(compact_text(content, 420))
00172:         elif role == "assistant":
00173:             if not any(marker in lowered for marker in boilerplate_markers):
00174:                 # Keep only small assistant decisions, not model-written music criticism.
00175:                 if any(marker in lowered for marker in ("salvato", "applicher", "usero", "uso", "pipeline", "script")):
00176:                     assistant_notes.append(compact_text(content, 300))
00177:         for token in ("ball", "primary_ball_asset", "fbx", "cover", "manual", "indexai"):
00178:             if token.lower() in lowered:
00179:                 asset_mentions.append(token)
00180: 
00181:     preference_summary = []
00182:     for key, value in preferences.items():
00183:         if value:
00184:             preference_summary.append(f"{key}: {compact_text(value, 260)}")
00185: 
00186:     previous_memory = previous.get("conversation_memory") if isinstance(previous.get("conversation_memory"), dict) else {}
00187:     previous_constraints = previous_memory.get("durable_constraints") if isinstance(previous_memory, dict) else []
00188:     if isinstance(previous_constraints, list) and previous_memory.get("memory_version") == MEMORY_VERSION:
00189:         durable_constraints = [str(item) for item in previous_constraints] + durable_constraints
00190: 
00191:     def unique_recent(values: list[str], limit: int) -> list[str]:
00192:         seen = set()
00193:         result = []
00194:         for value in values:
00195:             key = value.strip().lower()
00196:             if not key or key in seen:
00197:                 continue
00198:             seen.add(key)
00199:             result.append(value)
00200:         return result[-limit:]
00201: 
00202:     return {
00203:         "updated_at": now_iso(),
00204:         "memory_version": MEMORY_VERSION,
00205:         "message_count": len(transcript),
00206:         "preference_summary": preference_summary,
00207:         "recent_user_requests": user_requests[-18:],
00208:         "recent_user_questions": question_history[-8:],
00209:         "recent_assistant_notes": assistant_notes[-10:],
00210:         "durable_constraints": unique_recent(durable_constraints, 24),
00211:         "asset_mentions": sorted(set(asset_mentions)),
00212:         "memory_policy": "This compact memory is always passed to the local chat/model; recent_conversation is only the short working window.",
00213:     }
00214: 
00215: 
00216: def load_or_create_scene_brief(*, track_stem: str, audio_path: str, output_path: Path) -> dict:
00217:     existing = read_json(output_path)
00218:     if existing:
00219:         memory = existing.get("conversation_memory") if isinstance(existing.get("conversation_memory"), dict) else {}
00220:         if memory.get("memory_version") != MEMORY_VERSION:
00221:             preferences = existing.get("scene_preferences") if isinstance(existing.get("scene_preferences"), dict) else default_scene_preferences()
00222:             transcript = existing.get("conversation_transcript") if isinstance(existing.get("conversation_transcript"), list) else []
00223:             existing["conversation_memory"] = build_conversation_memory(
00224:                 preferences={key: str(value) for key, value in preferences.items()},
00225:                 transcript=transcript,
00226:                 previous=existing,
00227:             )
00228:             write_json(output_path, existing)
00229:         return existing
00230:     brief = build_scene_brief(
00231:         track_stem=track_stem,
00232:         audio_path=audio_path,
00233:         preferences=default_scene_preferences(),
00234:         transcript=[],
00235:     )
00236:     write_json(output_path, brief)
00237:     return brief
00238: 
00239: 
00240: def append_scene_message(
00241:     *,
00242:     track_stem: str,
00243:     audio_path: str,
00244:     output_path: Path,
00245:     role: str,
00246:     content: str,
00247: ) -> dict:
00248:     brief = load_or_create_scene_brief(track_stem=track_stem, audio_path=audio_path, output_path=output_path)
00249:     transcript = brief.get("conversation_transcript")
00250:     if not isinstance(transcript, list):
00251:         transcript = []
00252:     transcript.append(
00253:         {
00254:             "time": now_iso(),
00255:             "role": role,
00256:             "content": content,
00257:         }
00258:     )
00259: 
00260:     preferences = brief.get("scene_preferences")
00261:     if not isinstance(preferences, dict):
00262:         preferences = default_scene_preferences()
00263: 
00264:     if role == "user":
00265:         current_notes = str(preferences.get("free_notes") or "").strip()
00266:         preferences["free_notes"] = (current_notes + "\n" + content).strip() if current_notes else content
00267: 
00268:     updated = build_scene_brief(
00269:         track_stem=track_stem,
00270:         audio_path=audio_path,
00271:         preferences={key: str(value) for key, value in preferences.items()},
00272:         transcript=transcript,
00273:         previous=brief,
00274:     )
00275:     write_json(output_path, updated)
00276:     return updated
00277: 
00278: 
00279: def clear_scene_chat_history(*, track_stem: str, audio_path: str, output_path: Path) -> dict:
00280:     brief = load_or_create_scene_brief(track_stem=track_stem, audio_path=audio_path, output_path=output_path)
00281:     preferences = brief.get("scene_preferences")
00282:     if not isinstance(preferences, dict):
00283:         preferences = default_scene_preferences()
00284:     preferences = {key: str(value) for key, value in preferences.items()}
00285:     preferences["free_notes"] = ""
```
