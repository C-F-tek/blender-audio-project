# Project Code Chunk 118/212

- File: `Tools/npu/build_music_context.py`
- Part: `1`
- Lines: `1-285`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `hashlib`, `json`, `math`, `statistics`, `from datetime import datetime`, `from ai_memory_context import build_ai_memory_context`
- Functions: `sha256_text(text)` line 41; `rel_to_root(path)` line 45; `read_text(path)` line 52; `load_json(path)` line 56; `round_float(value, digits)` line 61; `quantile(values, ratio)` line 71; `avg_top(values, ratio)` line 85; `value_stats(values)` line 92; `frame_values(frames, key)` line 117; `energy_stats(frames)` line 121; `dominant_band(stats)` line 131; `intensity_label(score)` line 140; `segment_score(stats)` line 152; `control_suggestions(stats, beat_count)` line 162; `split_segments(frames, segment_seconds, duration)` line 176; `sampled_frames(frames, max_rows)` line 189; `top_events(frames, limit)` line 210; `beats_in_range(beats, start, end)` line 235; `build_segments(analysis, segment_seconds)` line 239; `summarize_analysis(analysis_path, segment_seconds)` line 273; `scene_summary_from_json(path, data)` line 319; `load_scene_records(scene_files)` line 353; `markdown_table_rows(rows, keys)` line 387; `write_chunk(path, title, body)` line 394; `write_music_chunks(context, scene_records)` line 404; `write_music_context_md(context, scene_records, chunks)` line 481; `build_analysis_ai_context(context)` line 538; `write_blender_keyframe_alias(analysis_path, blender_keyframes_path)` line 572; `build_music_context(analysis_path, track_summary_path, scene_files, segment_seconds, compact_json_path, analysis_ai_context_path, blender_keyframes_path, run_ollama, ollama_model)` line 579; `main()` line 676
- Assignments: `ROOT`, `OUTPUT_DIR`, `OUT_DIR`, `CHUNK_DIR`, `DEFAULT_TRACK_STEM`, `DEFAULT_ANALYSIS`, `DEFAULT_TRACK_SUMMARY`, `DEFAULT_COMPACT_JSON`, `DEFAULT_ANALYSIS_AI_CONTEXT`, `DEFAULT_BLENDER_KEYFRAMES_JSON`, `OUT_MD`, `OUT_JSON`, `DEFAULT_SCENE_FILES`, `DEFAULT_SEGMENT_SECONDS`, `SAMPLE_ROWS_PER_SEGMENT`, `TOP_EVENTS_PER_SEGMENT`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import argparse
00005: import hashlib
00006: import json
00007: import math
00008: import statistics
00009: from datetime import datetime
00010: 
00011: from ai_memory_context import build_ai_memory_context
00012: 
00013: 
00014: ROOT = Path(__file__).resolve().parents[2]
00015: OUTPUT_DIR = ROOT / "output"
00016: OUT_DIR = ROOT / "Tools" / "npu"
00017: CHUNK_DIR = OUT_DIR / "npu_music_chunks"
00018: 
00019: DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
00020: DEFAULT_ANALYSIS = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_analysis.json"
00021: DEFAULT_TRACK_SUMMARY = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_track_summary.json"
00022: DEFAULT_COMPACT_JSON = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_music_context.json"
00023: DEFAULT_ANALYSIS_AI_CONTEXT = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_analysis_ai_context.json"
00024: DEFAULT_BLENDER_KEYFRAMES_JSON = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_analysis_blender_keyframes.json"
00025: OUT_MD = OUT_DIR / "npu_music_context.md"
00026: OUT_JSON = OUT_DIR / "npu_music_manifest.json"
00027: 
00028: DEFAULT_SCENE_FILES = [
00029:     ROOT / "scene_spec_album_driven.json",
00030:     ROOT / "scene_spec_album_driven_normalized.json",
00031:     ROOT / "scene_spec_album_driven_raw.txt",
00032:     ROOT / "scene_spec_from_npu.json",
00033:     ROOT / "scene_spec_from_npu_raw.txt",
00034: ]
00035: 
00036: DEFAULT_SEGMENT_SECONDS = 16.0
00037: SAMPLE_ROWS_PER_SEGMENT = 64
00038: TOP_EVENTS_PER_SEGMENT = 12
00039: 
00040: 
00041: def sha256_text(text: str) -> str:
00042:     return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
00043: 
00044: 
00045: def rel_to_root(path: Path) -> str:
00046:     try:
00047:         return str(path.relative_to(ROOT)).replace("\\", "/")
00048:     except ValueError:
00049:         return str(path)
00050: 
00051: 
00052: def read_text(path: Path) -> str:
00053:     return path.read_text(encoding="utf-8", errors="replace")
00054: 
00055: 
00056: def load_json(path: Path) -> dict:
00057:     with open(path, "r", encoding="utf-8") as handle:
00058:         return json.load(handle)
00059: 
00060: 
00061: def round_float(value: object, digits: int = 4) -> float:
00062:     try:
00063:         number = float(value)
00064:     except Exception:
00065:         number = 0.0
00066:     if math.isnan(number) or math.isinf(number):
00067:         number = 0.0
00068:     return round(number, digits)
00069: 
00070: 
00071: def quantile(values: list[float], ratio: float) -> float:
00072:     if not values:
00073:         return 0.0
00074:     ordered = sorted(values)
00075:     if len(ordered) == 1:
00076:         return ordered[0]
00077:     pos = max(0.0, min(1.0, ratio)) * (len(ordered) - 1)
00078:     lo = int(math.floor(pos))
00079:     hi = int(math.ceil(pos))
00080:     if lo == hi:
00081:         return ordered[lo]
00082:     return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)
00083: 
00084: 
00085: def avg_top(values: list[float], ratio: float = 0.1) -> float:
00086:     if not values:
00087:         return 0.0
00088:     count = max(1, int(len(values) * ratio))
00089:     return statistics.mean(sorted(values, reverse=True)[:count])
00090: 
00091: 
00092: def value_stats(values: list[float]) -> dict:
00093:     if not values:
00094:         return {
00095:             "avg": 0.0,
00096:             "min": 0.0,
00097:             "max": 0.0,
00098:             "std": 0.0,
00099:             "p50": 0.0,
00100:             "p90": 0.0,
00101:             "p98": 0.0,
00102:             "top10_avg": 0.0,
00103:         }
00104: 
00105:     return {
00106:         "avg": round_float(statistics.mean(values)),
00107:         "min": round_float(min(values)),
00108:         "max": round_float(max(values)),
00109:         "std": round_float(statistics.pstdev(values) if len(values) > 1 else 0.0),
00110:         "p50": round_float(quantile(values, 0.50)),
00111:         "p90": round_float(quantile(values, 0.90)),
00112:         "p98": round_float(quantile(values, 0.98)),
00113:         "top10_avg": round_float(avg_top(values)),
00114:     }
00115: 
00116: 
00117: def frame_values(frames: list[dict], key: str) -> list[float]:
00118:     return [round_float(frame.get(key, 0.0), 8) for frame in frames]
00119: 
00120: 
00121: def energy_stats(frames: list[dict]) -> dict:
00122:     return {
00123:         "low": value_stats(frame_values(frames, "low")),
00124:         "mid": value_stats(frame_values(frames, "mid")),
00125:         "high": value_stats(frame_values(frames, "high")),
00126:         "onset": value_stats(frame_values(frames, "onset")),
00127:         "beat": value_stats(frame_values(frames, "beat")),
00128:     }
00129: 
00130: 
00131: def dominant_band(stats: dict) -> str:
00132:     candidates = {
00133:         "low": stats["low"]["avg"],
00134:         "mid": stats["mid"]["avg"],
00135:         "high": stats["high"]["avg"],
00136:     }
00137:     return max(candidates, key=candidates.get)
00138: 
00139: 
00140: def intensity_label(score: float) -> str:
00141:     if score >= 0.72:
00142:         return "peak"
00143:     if score >= 0.52:
00144:         return "high"
00145:     if score >= 0.34:
00146:         return "medium"
00147:     if score >= 0.18:
00148:         return "low"
00149:     return "quiet"
00150: 
00151: 
00152: def segment_score(stats: dict) -> float:
00153:     return round_float(
00154:         stats["low"]["avg"] * 0.30
00155:         + stats["mid"]["avg"] * 0.25
00156:         + stats["high"]["avg"] * 0.20
00157:         + stats["onset"]["p90"] * 0.20
00158:         + stats["beat"]["avg"] * 0.05
00159:     )
00160: 
00161: 
00162: def control_suggestions(stats: dict, beat_count: int) -> dict:
00163:     band = dominant_band(stats)
00164:     score = segment_score(stats)
00165:     return {
00166:         "primary_band": band,
00167:         "intensity": intensity_label(score),
00168:         "hero_deformation": round_float(stats["low"]["p90"] * 0.55 + stats["onset"]["p90"] * 0.20),
00169:         "material_shimmer": round_float(stats["mid"]["p90"] * 0.45 + stats["high"]["p90"] * 0.35),
00170:         "fog_motion": round_float(stats["low"]["avg"] * 0.35 + stats["mid"]["avg"] * 0.25),
00171:         "accent_emission": round_float(stats["high"]["p90"] * 0.65 + min(1.0, beat_count / 32.0) * 0.20),
00172:         "camera_pressure": round_float(stats["onset"]["p98"] * 0.28 + stats["beat"]["avg"] * 0.12),
00173:     }
00174: 
00175: 
00176: def split_segments(frames: list[dict], segment_seconds: float, duration: float) -> list[list[dict]]:
00177:     segment_count = max(1, int(math.ceil(duration / segment_seconds)))
00178:     buckets: list[list[dict]] = [[] for _ in range(segment_count)]
00179: 
00180:     for frame in frames:
00181:         time = round_float(frame.get("time", 0.0), 8)
00182:         index = int(time // segment_seconds)
00183:         index = max(0, min(segment_count - 1, index))
00184:         buckets[index].append(frame)
00185: 
00186:     return buckets
00187: 
00188: 
00189: def sampled_frames(frames: list[dict], max_rows: int = SAMPLE_ROWS_PER_SEGMENT) -> list[dict]:
00190:     if not frames:
00191:         return []
00192:     if len(frames) <= max_rows:
00193:         indices = list(range(len(frames)))
00194:     else:
00195:         indices = sorted({round(i * (len(frames) - 1) / (max_rows - 1)) for i in range(max_rows)})
00196: 
00197:     return [
00198:         {
00199:             "time": round_float(frames[index].get("time", 0.0), 3),
00200:             "low": round_float(frames[index].get("low", 0.0), 3),
00201:             "mid": round_float(frames[index].get("mid", 0.0), 3),
00202:             "high": round_float(frames[index].get("high", 0.0), 3),
00203:             "onset": round_float(frames[index].get("onset", 0.0), 3),
00204:             "beat": round_float(frames[index].get("beat", 0.0), 3),
00205:         }
00206:         for index in indices
00207:     ]
00208: 
00209: 
00210: def top_events(frames: list[dict], limit: int = TOP_EVENTS_PER_SEGMENT) -> list[dict]:
00211:     ranked = sorted(
00212:         frames,
00213:         key=lambda frame: (
00214:             round_float(frame.get("onset", 0.0)) * 1.00
00215:             + round_float(frame.get("beat", 0.0)) * 0.35
00216:             + round_float(frame.get("high", 0.0)) * 0.15
00217:         ),
00218:         reverse=True,
00219:     )
00220:     events = []
00221:     for frame in ranked[:limit]:
00222:         events.append(
00223:             {
00224:                 "time": round_float(frame.get("time", 0.0), 3),
00225:                 "low": round_float(frame.get("low", 0.0), 3),
00226:                 "mid": round_float(frame.get("mid", 0.0), 3),
00227:                 "high": round_float(frame.get("high", 0.0), 3),
00228:                 "onset": round_float(frame.get("onset", 0.0), 3),
00229:                 "beat": round_float(frame.get("beat", 0.0), 3),
00230:             }
00231:         )
00232:     return events
00233: 
00234: 
00235: def beats_in_range(beats: list[float], start: float, end: float) -> list[float]:
00236:     return [round_float(beat, 3) for beat in beats if start <= beat < end]
00237: 
00238: 
00239: def build_segments(analysis: dict, segment_seconds: float) -> list[dict]:
00240:     meta = analysis.get("meta", {})
00241:     frames = analysis.get("frames", [])
00242:     beats = [round_float(beat, 8) for beat in analysis.get("beats", [])]
00243:     duration = round_float(meta.get("duration_sec") or (frames[-1].get("time", 0.0) if frames else 0.0), 8)
00244: 
00245:     segments = []
00246:     for index, segment_frames in enumerate(split_segments(frames, segment_seconds, duration), 1):
00247:         start = (index - 1) * segment_seconds
00248:         end = min(index * segment_seconds, duration)
00249:         stats = energy_stats(segment_frames)
00250:         beat_times = beats_in_range(beats, start, end)
00251:         score = segment_score(stats)
00252:         segments.append(
00253:             {
00254:                 "index": index,
00255:                 "start_sec": round_float(start, 3),
00256:                 "end_sec": round_float(end, 3),
00257:                 "duration_sec": round_float(max(0.0, end - start), 3),
00258:                 "frame_count": len(segment_frames),
00259:                 "beat_count": len(beat_times),
00260:                 "dominant_band": dominant_band(stats),
00261:                 "intensity_score": score,
00262:                 "intensity": intensity_label(score),
00263:                 "stats": stats,
00264:                 "controls": control_suggestions(stats, len(beat_times)),
00265:                 "beat_times": beat_times,
00266:                 "top_events": top_events(segment_frames),
00267:                 "sampled_frames": sampled_frames(segment_frames),
00268:             }
00269:         )
00270:     return segments
00271: 
00272: 
00273: def summarize_analysis(analysis_path: Path, segment_seconds: float) -> tuple[dict, list[dict]]:
00274:     analysis = load_json(analysis_path)
00275:     meta = analysis.get("meta", {})
00276:     frames = analysis.get("frames", [])
00277:     beats = analysis.get("beats", [])
00278:     stats = energy_stats(frames)
00279:     segments = build_segments(analysis, segment_seconds)
00280: 
00281:     top_by_energy = sorted(segments, key=lambda item: item["intensity_score"], reverse=True)[:8]
00282:     top_by_onset = sorted(segments, key=lambda item: item["stats"]["onset"]["p98"], reverse=True)[:8]
00283: 
00284:     summary = {
00285:         "source": rel_to_root(analysis_path),
```
