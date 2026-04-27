# Project Code Chunk 187/212

- File: `Tools/npu/run_ollama_music_agent.py`
- Part: `1`
- Lines: `1-238`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `from datetime import datetime`, `from ollama_runtime import OllamaSession, parse_json_response`
- Functions: `read_json(path)` line 22; `compact_context_for_prompt(context)` line 27; `build_prompt(context)` line 56; `markdown_from_insights(data, model)` line 111; `run_ollama_music_agent(context_json, fallback_context_json, out_json, out_md, model, base_url, keep_alive, max_new_tokens, temperature, keep_server, keep_model)` line 141; `main()` line 207
- Assignments: `ROOT`, `OUTPUT_DIR`, `TOOLS_DIR`, `DEFAULT_TRACK_STEM`, `DEFAULT_CONTEXT_JSON`, `DEFAULT_MUSIC_CONTEXT_JSON`, `DEFAULT_OUT_JSON`, `DEFAULT_OUT_MD`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import argparse
00005: import json
00006: from datetime import datetime
00007: 
00008: from ollama_runtime import OllamaSession, parse_json_response
00009: 
00010: 
00011: ROOT = Path(__file__).resolve().parents[2]
00012: OUTPUT_DIR = ROOT / "output"
00013: TOOLS_DIR = ROOT / "Tools" / "npu"
00014: 
00015: DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
00016: DEFAULT_CONTEXT_JSON = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_analysis_ai_context.json"
00017: DEFAULT_MUSIC_CONTEXT_JSON = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_music_context.json"
00018: DEFAULT_OUT_JSON = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_ollama_music_insights.json"
00019: DEFAULT_OUT_MD = TOOLS_DIR / "ollama_music_insights.md"
00020: 
00021: 
00022: def read_json(path: Path) -> dict:
00023:     with open(path, "r", encoding="utf-8") as handle:
00024:         return json.load(handle)
00025: 
00026: 
00027: def compact_context_for_prompt(context: dict) -> dict:
00028:     analysis = context.get("analysis_summary", {})
00029:     compact = {
00030:         "analysis_summary": analysis,
00031:         "track_summary": context.get("track_summary"),
00032:         "ai_memory_context": context.get("ai_memory_context"),
00033:         "scene_summaries": context.get("scene_summaries", []),
00034:         "segments": [],
00035:     }
00036: 
00037:     for segment in context.get("segments", []):
00038:         compact["segments"].append(
00039:             {
00040:                 "index": segment.get("index"),
00041:                 "start_sec": segment.get("start_sec"),
00042:                 "end_sec": segment.get("end_sec"),
00043:                 "dominant_band": segment.get("dominant_band"),
00044:                 "intensity_score": segment.get("intensity_score"),
00045:                 "intensity": segment.get("intensity"),
00046:                 "beat_count": segment.get("beat_count"),
00047:                 "stats": segment.get("stats"),
00048:                 "controls": segment.get("controls"),
00049:                 "top_events": segment.get("top_events", [])[:8],
00050:             }
00051:         )
00052: 
00053:     return compact
00054: 
00055: 
00056: def build_prompt(context: dict) -> str:
00057:     payload = json.dumps(compact_context_for_prompt(context), indent=2, ensure_ascii=False)
00058:     return f"""
00059: Sei un agente musicale locale per un video Blender audio-reactive.
00060: 
00061: Devi produrre un JSON operativo per aiutare gli script Blender e i prossimi hotpatch.
00062: Il JSON completo frame-by-frame per Blender NON deve essere ridotto, sostituito o riscritto.
00063: Usa questi segmenti solo per analisi, decisioni creative e suggerimenti.
00064: Usa `ai_memory_context` come memoria utente/progetto: preferenze, correzioni, asset e vincoli valgono piu dei default generici.
00065: Non ripetere il brief: interpreta il brano alla luce della memoria e produci decisioni utili.
00066: Se la memoria cita due oggetti centrali ball opposti, pianifica una lettura duale/contrapposta del brano.
00067: 
00068: Rispondi SOLO con JSON valido, senza markdown.
00069: 
00070: Schema richiesto:
00071: {{
00072:   "model_role": "music_scene_agent",
00073:   "global_read": {{
00074:     "mood": "...",
00075:     "tempo_interpretation": "...",
00076:     "energy_shape": "...",
00077:     "key_risks": ["..."]
00078:   }},
00079:   "segment_plan": [
00080:     {{
00081:       "segment": 1,
00082:       "time_range": "0.0-16.0",
00083:       "intent": "...",
00084:       "hero_mesh": "...",
00085:       "materials": "...",
00086:       "fog": "...",
00087:       "lights": "...",
00088:       "camera": "...",
00089:       "physics": "...",
00090:       "avoid": "..."
00091:     }}
00092:   ],
00093:   "scene_json_recommendations": {{
00094:     "keep": ["..."],
00095:     "change_candidates": ["..."],
00096:     "do_not_touch": ["..."]
00097:   }},
00098:   "blender_keyframe_policy": {{
00099:     "use_full_analysis_json": true,
00100:     "do_not_reduce_frames": true,
00101:     "notes": "..."
00102:   }},
00103:   "next_actions": ["..."]
00104: }}
00105: 
00106: CONTESTO:
00107: {payload}
00108: """.strip()
00109: 
00110: 
00111: def markdown_from_insights(data: dict, model: str) -> str:
00112:     lines = [
00113:         "# Ollama Music Insights\n\n",
00114:         f"Generated: `{datetime.now().isoformat(timespec='seconds')}`\n\n",
00115:         f"Model: `{model}`\n\n",
00116:         "## Global Read\n",
00117:     ]
00118:     global_read = data.get("global_read", {})
00119:     for key, value in global_read.items():
00120:         lines.append(f"- `{key}`: {value}\n")
00121: 
00122:     lines.append("\n## Segment Plan\n")
00123:     for item in data.get("segment_plan", []):
00124:         lines.append(
00125:             f"- Segment `{item.get('segment')}` `{item.get('time_range')}`: "
00126:             f"{item.get('intent')} | hero `{item.get('hero_mesh')}` | fog `{item.get('fog')}`\n"
00127:         )
00128: 
00129:     lines.append("\n## Keyframe Policy\n")
00130:     policy = data.get("blender_keyframe_policy", {})
00131:     for key, value in policy.items():
00132:         lines.append(f"- `{key}`: {value}\n")
00133: 
00134:     lines.append("\n## Next Actions\n")
00135:     for item in data.get("next_actions", []):
00136:         lines.append(f"- {item}\n")
00137: 
00138:     return "".join(lines)
00139: 
00140: 
00141: def run_ollama_music_agent(
00142:     context_json: Path | str = DEFAULT_CONTEXT_JSON,
00143:     fallback_context_json: Path | str = DEFAULT_MUSIC_CONTEXT_JSON,
00144:     out_json: Path | str = DEFAULT_OUT_JSON,
00145:     out_md: Path | str = DEFAULT_OUT_MD,
00146:     model: str = "qwen2.5-coder:14b",
00147:     base_url: str | None = None,
00148:     keep_alive: str = "5m",
00149:     max_new_tokens: int = 1800,
00150:     temperature: float = 0.12,
00151:     keep_server: bool = False,
00152:     keep_model: bool = False,
00153: ) -> dict:
00154:     context_path = Path(context_json)
00155:     if not context_path.exists():
00156:         context_path = Path(fallback_context_json)
00157:     if not context_path.exists():
00158:         raise FileNotFoundError(f"Context JSON not found: {context_path}")
00159: 
00160:     context = read_json(context_path)
00161:     prompt = build_prompt(context)
00162: 
00163:     session_kwargs = {
00164:         "model": model,
00165:         "keep_alive": keep_alive,
00166:         "shutdown_server": not keep_server,
00167:         "unload_model": not keep_model,
00168:     }
00169:     if base_url:
00170:         session_kwargs["base_url"] = base_url
00171: 
00172:     with OllamaSession(**session_kwargs) as session:
00173:         text = session.generate(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
00174:         used_model = session.model or model
00175: 
00176:     try:
00177:         insights = parse_json_response(text)
00178:     except Exception:
00179:         insights = {
00180:             "model_role": "music_scene_agent",
00181:             "parse_error": True,
00182:             "raw_response": text,
00183:             "blender_keyframe_policy": {
00184:                 "use_full_analysis_json": True,
00185:                 "do_not_reduce_frames": True,
00186:                 "notes": "Raw model response could not be parsed; keep Blender frame JSON unchanged.",
00187:             },
00188:         }
00189: 
00190:     insights["generated_at"] = datetime.now().isoformat(timespec="seconds")
00191:     insights["model"] = used_model
00192:     insights["source_context"] = str(context_path)
00193: 
00194:     out_json = Path(out_json)
00195:     out_md = Path(out_md)
00196:     out_json.parent.mkdir(parents=True, exist_ok=True)
00197:     out_md.parent.mkdir(parents=True, exist_ok=True)
00198: 
00199:     out_json.write_text(json.dumps(insights, indent=2, ensure_ascii=False), encoding="utf-8")
00200:     out_md.write_text(markdown_from_insights(insights, used_model), encoding="utf-8")
00201: 
00202:     print(f"[OK] Wrote: {out_json}")
00203:     print(f"[OK] Wrote: {out_md}")
00204:     return {"out_json": out_json, "out_md": out_md, "model": used_model}
00205: 
00206: 
00207: def main() -> None:
00208:     parser = argparse.ArgumentParser(description="Run Ollama on compact WAV/scene context and write AI insights.")
00209:     parser.add_argument("--context-json", default=str(DEFAULT_CONTEXT_JSON))
00210:     parser.add_argument("--fallback-context-json", default=str(DEFAULT_MUSIC_CONTEXT_JSON))
00211:     parser.add_argument("--out-json", default=str(DEFAULT_OUT_JSON))
00212:     parser.add_argument("--out-md", default=str(DEFAULT_OUT_MD))
00213:     parser.add_argument("--model", default="qwen2.5-coder:14b")
00214:     parser.add_argument("--base-url", default=None)
00215:     parser.add_argument("--keep-alive", default="5m")
00216:     parser.add_argument("--max-new-tokens", type=int, default=1800)
00217:     parser.add_argument("--temperature", type=float, default=0.12)
00218:     parser.add_argument("--keep-server", action="store_true")
00219:     parser.add_argument("--keep-model", action="store_true")
00220:     args = parser.parse_args()
00221: 
00222:     run_ollama_music_agent(
00223:         context_json=args.context_json,
00224:         fallback_context_json=args.fallback_context_json,
00225:         out_json=args.out_json,
00226:         out_md=args.out_md,
00227:         model=args.model,
00228:         base_url=args.base_url,
00229:         keep_alive=args.keep_alive,
00230:         max_new_tokens=args.max_new_tokens,
00231:         temperature=args.temperature,
00232:         keep_server=args.keep_server,
00233:         keep_model=args.keep_model,
00234:     )
00235: 
00236: 
00237: if __name__ == "__main__":
00238:     main()
```
