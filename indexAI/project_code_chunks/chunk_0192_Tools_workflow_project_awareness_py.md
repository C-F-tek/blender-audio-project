# Project Code Chunk 192/212

- File: `Tools/workflow/project_awareness.py`
- Part: `1`
- Lines: `1-249`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `from typing import Any`, `json`
- Functions: `now_iso()` line 15; `read_json(path)` line 19; `file_status(path)` line 29; `compact_assets(asset_inventory)` line 39; `infer_track_identity(track_stem)` line 59; `compact_track_read(music_context)` line 77; `deterministic_track_opinion(track_identity, music_context)` line 104; `build_verified_answers(awareness, music_context)` line 135; `build_preflight_answers_for_message(user_message, awareness, music_context)` line 204; `build_project_awareness()` line 237; `save_project_awareness(awareness)` line 330
- Assignments: `ROOT`, `OUTPUT_DIR`, `NPU_DIR`, `INDEX_AI_DIR`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from datetime import datetime
00004: from pathlib import Path
00005: from typing import Any
00006: import json
00007: 
00008: 
00009: ROOT = Path(__file__).resolve().parents[2]
00010: OUTPUT_DIR = ROOT / "output"
00011: NPU_DIR = ROOT / "Tools" / "npu"
00012: INDEX_AI_DIR = ROOT / "indexAI"
00013: 
00014: 
00015: def now_iso() -> str:
00016:     return datetime.now().isoformat(timespec="seconds")
00017: 
00018: 
00019: def read_json(path: Path) -> dict[str, Any]:
00020:     if not path.exists():
00021:         return {}
00022:     try:
00023:         data = json.loads(path.read_text(encoding="utf-8"))
00024:     except Exception:
00025:         return {}
00026:     return data if isinstance(data, dict) else {}
00027: 
00028: 
00029: def file_status(path: Path) -> dict[str, Any]:
00030:     exists = path.exists()
00031:     return {
00032:         "path": str(path),
00033:         "exists": exists,
00034:         "bytes": path.stat().st_size if exists and path.is_file() else 0,
00035:         "updated": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds") if exists else None,
00036:     }
00037: 
00038: 
00039: def compact_assets(asset_inventory: dict[str, Any]) -> list[dict[str, Any]]:
00040:     assets = asset_inventory.get("assets") if isinstance(asset_inventory.get("assets"), list) else []
00041:     result = []
00042:     for asset in assets:
00043:         if not isinstance(asset, dict):
00044:             continue
00045:         role = asset.get("role")
00046:         if role not in {"primary_ball_asset", "animated_effect_asset", "blend_scene_reference"}:
00047:             continue
00048:         result.append(
00049:             {
00050:                 "role": role,
00051:                 "name": asset.get("name"),
00052:                 "path": asset.get("path"),
00053:                 "type": asset.get("type") or asset.get("extension"),
00054:             }
00055:         )
00056:     return result[:24]
00057: 
00058: 
00059: def infer_track_identity(track_stem: str) -> dict[str, Any]:
00060:     clean = track_stem.replace("_Master", "").replace("_master", "").strip()
00061:     title = clean
00062:     artist = None
00063:     if "-" in clean:
00064:         parts = [part.strip() for part in clean.split("-") if part.strip()]
00065:         if len(parts) >= 2:
00066:             title = parts[0]
00067:             artist = " - ".join(parts[1:])
00068:     return {
00069:         "track_stem": track_stem,
00070:         "title": title,
00071:         "artist": artist,
00072:         "identity_source": "current workflow WAV filename/session",
00073:         "external_metadata_allowed": False,
00074:     }
00075: 
00076: 
00077: def compact_track_read(music_context: dict[str, Any] | None) -> dict[str, Any]:
00078:     music_context = music_context or {}
00079:     summary = music_context.get("analysis_summary") or {}
00080:     meta = summary.get("meta") or {}
00081:     segments = music_context.get("segments") or []
00082:     top_energy = summary.get("top_energy_segments") or []
00083:     first = segments[0] if segments else {}
00084:     last = segments[-1] if segments else {}
00085:     return {
00086:         "duration_sec": meta.get("duration_sec"),
00087:         "fps": meta.get("fps"),
00088:         "bpm": meta.get("estimated_tempo_bpm"),
00089:         "segment_count": len(segments),
00090:         "first_segment": {
00091:             "dominant_band": first.get("dominant_band"),
00092:             "intensity": first.get("intensity"),
00093:             "controls": first.get("controls"),
00094:         },
00095:         "last_segment": {
00096:             "dominant_band": last.get("dominant_band"),
00097:             "intensity": last.get("intensity"),
00098:             "controls": last.get("controls"),
00099:         },
00100:         "top_energy_segments": top_energy[:5],
00101:     }
00102: 
00103: 
00104: def deterministic_track_opinion(track_identity: dict[str, Any], music_context: dict[str, Any] | None) -> str:
00105:     read = compact_track_read(music_context)
00106:     title = track_identity.get("title") or track_identity.get("track_stem")
00107:     artist = track_identity.get("artist")
00108:     name = f"{title} - {artist}" if artist else str(title)
00109:     segment_count = read.get("segment_count") or 0
00110:     bpm = read.get("bpm")
00111:     first = read.get("first_segment") or {}
00112:     last = read.get("last_segment") or {}
00113:     top = read.get("top_energy_segments") or []
00114:     top_bits = []
00115:     for item in top[:3]:
00116:         top_bits.append(
00117:             f"segmento {item.get('index')} ({item.get('start_sec')}-{item.get('end_sec')}s, {item.get('dominant_band')}, {item.get('intensity')})"
00118:         )
00119: 
00120:     lines = [
00121:         f"Parlo del brano del progetto, `{name}`, non di metadati esterni.",
00122:         f"Dai JSON lo leggo come una traccia con {segment_count} segmenti compatti" + (f" e BPM stimato {round(float(bpm), 2)}" if bpm else "") + ".",
00123:         (
00124:             f"L'apertura sembra guidata da banda `{first.get('dominant_band')}` con intensita `{first.get('intensity')}`, "
00125:             f"mentre la coda arriva su `{last.get('dominant_band')}` / `{last.get('intensity')}`."
00126:         ),
00127:         "Da art direction lo tratterei come un brano da doppio fulcro: due `primary_ball_asset` centrali in controfase, uno piu materico e uno piu luminoso, usando tutti i frame del `blender_keyframes_json`.",
00128:     ]
00129:     if top_bits:
00130:         lines.append("I punti da far respirare visivamente sono: " + "; ".join(top_bits) + ".")
00131:     lines.append("Quindi: niente narrativa generica da canzone pop; qui conviene costruire una scena audio-reactive precisa, con deformazioni mesh e materiali che seguono low/mid/high/onset/beat.")
00132:     return "\n".join(lines)
00133: 
00134: 
00135: def build_verified_answers(awareness: dict[str, Any], music_context: dict[str, Any] | None = None) -> list[dict[str, Any]]:
00136:     music_context = music_context or {}
00137:     files = awareness.get("technical_files", {})
00138:     state = awareness.get("pipeline_state", {})
00139:     assets = (awareness.get("asset_awareness") or {}).get("primary_assets", [])
00140:     primary_ball = next((asset for asset in assets if asset.get("role") == "primary_ball_asset"), None)
00141:     track_identity = awareness.get("track_identity", {})
00142: 
00143:     answers = [
00144:         {
00145:             "question": "Di che brano stiamo parlando?",
00146:             "answer": (
00147:                 f"Il brano corrente e `{track_identity.get('title')}`"
00148:                 + (f" di `{track_identity.get('artist')}`" if track_identity.get("artist") else "")
00149:                 + ". Non usare titoli/artisti esterni non presenti nei file del progetto."
00150:             ),
00151:             "evidence": track_identity,
00152:         },
00153:         {
00154:             "question": "Cosa pensi della traccia del progetto?",
00155:             "answer": deterministic_track_opinion(track_identity, music_context),
00156:             "evidence": compact_track_read(music_context),
00157:         },
00158:         {
00159:             "question": "Abbiamo qualcosa che puo essere usata sui keyframe dell'audio?",
00160:             "answer": (
00161:                 "Si. Usa `blender_keyframes_json`: contiene il JSON frame-by-frame completo con `frames` "
00162:                 "per low/mid/high/onset/beat. `music_context_json` e i segmenti servono solo per decisioni macro."
00163:             ),
00164:             "evidence": files.get("blender_keyframes_json", {}),
00165:         },
00166:         {
00167:             "question": "Serve importare manualmente il WAV in Blender?",
00168:             "answer": (
00169:                 "No. Il WAV e gia rappresentato dai JSON `analysis_json`, `music_context_json` e "
00170:                 "`blender_keyframes_json`. La chat deve parlare di pipeline/script, non di import audio manuale."
00171:             ),
00172:             "evidence": {
00173:                 "audio_already_loaded_by_pipeline": state.get("audio_already_loaded_by_pipeline"),
00174:                 "analysis_json": files.get("analysis_json", {}),
00175:             },
00176:         },
00177:         {
00178:             "question": "Quale asset va usato quando l'utente dice ball?",
00179:             "answer": (
00180:                 f"Usa `primary_ball_asset`: {primary_ball.get('path')}"
00181:                 if primary_ball
00182:                 else "Cerca un asset con ruolo `primary_ball_asset` nell'asset inventory."
00183:             ),
00184:             "evidence": primary_ball or {},
00185:         },
00186:         {
00187:             "question": "La pipeline e pronta per generare lo script scena?",
00188:             "answer": (
00189:                 "Si: analisi, music context, project index, manual index, service packet e scene brief risultano pronti."
00190:                 if state.get("can_generate_scene_script")
00191:                 else "Non completamente: controlla `missing_or_suspicious` e i technical_files mancanti."
00192:             ),
00193:             "evidence": state,
00194:         },
00195:         {
00196:             "question": "Quanti segmenti musicali compatti sono disponibili?",
00197:             "answer": f"Sono disponibili {state.get('segment_count', len(music_context.get('segments') or []))} segmenti compatti.",
00198:             "evidence": {"segment_count": state.get("segment_count", len(music_context.get("segments") or []))},
00199:         },
00200:     ]
00201:     return answers
00202: 
00203: 
00204: def build_preflight_answers_for_message(
00205:     user_message: str,
00206:     awareness: dict[str, Any],
00207:     music_context: dict[str, Any] | None = None,
00208: ) -> list[dict[str, Any]]:
00209:     text = user_message.lower()
00210:     answers = build_verified_answers(awareness, music_context)
00211:     selected: list[dict[str, Any]] = []
00212:     keyword_map = [
00213:         (("chi", "titolo", "artista", "nome"), 0),
00214:         (("cosa pensi", "traccia", "brano", "musical"), 1),
00215:         (("keyframe", "audio", "wave", "wav"), 2),
00216:         (("import", "blender", "wav", "wave", "audio"), 3),
00217:         (("ball", "sfera", "asset"), 4),
00218:         (("script", "gener", "prossimo", "ora", "pipeline"), 5),
00219:         (("segment", "chunk"), 6),
00220:     ]
00221:     for keywords, index in keyword_map:
00222:         if any(keyword in text for keyword in keywords):
00223:             selected.append(answers[index])
00224:     if not selected:
00225:         selected = [answers[0], answers[3]]
00226:     seen = set()
00227:     unique = []
00228:     for item in selected:
00229:         key = item["question"]
00230:         if key in seen:
00231:             continue
00232:         seen.add(key)
00233:         unique.append(item)
00234:     return unique[:4]
00235: 
00236: 
00237: def build_project_awareness(
00238:     *,
00239:     track_stem: str,
00240:     audio_path: str,
00241:     output_dir: Path | None = None,
00242:     asset_inventory: dict[str, Any] | None = None,
00243:     music_context: dict[str, Any] | None = None,
00244: ) -> dict[str, Any]:
00245:     output_dir = Path(output_dir or OUTPUT_DIR)
00246:     slug = "".join(ch.lower() if ch.isalnum() else "_" for ch in track_stem).strip("_")
00247:     slug = "_".join(part for part in slug.split("_") if part)
00248: 
00249:     key_paths = {
```
