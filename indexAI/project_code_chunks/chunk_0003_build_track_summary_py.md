# Project Code Chunk 3/212

- File: `build_track_summary.py`
- Part: `1`
- Lines: `1-113`

## Symbol Map
- Imports: `from pathlib import Path`, `argparse`, `json`, `sys`, `from statistics import mean`
- Functions: `avg_top(values, ratio)` line 15; `safe_mean(values)` line 22; `build_summary(analysis_json, out_json, update_music_context)` line 26; `main()` line 98
- Assignments: `ROOT`, `PROJECT_DIR`, `OUTPUT_DIR`, `ANALYSIS_JSON`, `OUT_JSON`

## Content
```py
00001: from pathlib import Path
00002: import argparse
00003: import json
00004: import sys
00005: from statistics import mean
00006: 
00007: ROOT = Path.home() / "blender"
00008: PROJECT_DIR = ROOT / "blender-audio-project"
00009: OUTPUT_DIR = PROJECT_DIR / "output"
00010: 
00011: ANALYSIS_JSON = OUTPUT_DIR / "Feel The Light-Luca Vera_Master_analysis.json"
00012: OUT_JSON = OUTPUT_DIR / "Feel The Light-Luca Vera_Master_track_summary.json"
00013: 
00014: 
00015: def avg_top(values, ratio=0.1):
00016:     if not values:
00017:         return 0.0
00018:     n = max(1, int(len(values) * ratio))
00019:     return mean(sorted(values, reverse=True)[:n])
00020: 
00021: 
00022: def safe_mean(values):
00023:     return mean(values) if values else 0.0
00024: 
00025: 
00026: def build_summary(analysis_json: Path, out_json: Path, update_music_context: bool = True) -> dict:
00027:     with open(analysis_json, "r", encoding="utf-8") as f:
00028:         data = json.load(f)
00029: 
00030:     meta = data["meta"]
00031:     frames = data["frames"]
00032: 
00033:     low_vals = [float(x.get("low", 0.0)) for x in frames]
00034:     mid_vals = [float(x.get("mid", 0.0)) for x in frames]
00035:     high_vals = [float(x.get("high", 0.0)) for x in frames]
00036:     onset_vals = [float(x.get("onset", 0.0)) for x in frames]
00037:     beat_vals = [float(x.get("beat", 0.0)) for x in frames]
00038: 
00039:     track_name = analysis_json.stem.replace("_analysis", "")
00040:     ai_memory_context = {}
00041:     tools_dir = PROJECT_DIR / "Tools" / "npu"
00042:     if tools_dir.exists():
00043:         if str(tools_dir) not in sys.path:
00044:             sys.path.insert(0, str(tools_dir))
00045:         try:
00046:             from ai_memory_context import build_ai_memory_context
00047: 
00048:             ai_memory_context = build_ai_memory_context(track_stem=track_name, output_dir=out_json.parent)
00049:         except Exception:
00050:             ai_memory_context = {}
00051: 
00052:     summary = {
00053:         "track_name": track_name,
00054:         "source_analysis_json": str(analysis_json),
00055:         "duration_sec": meta.get("duration_sec"),
00056:         "fps": meta.get("fps"),
00057:         "estimated_tempo_bpm": meta.get("estimated_tempo_bpm"),
00058:         "ai_memory_context": ai_memory_context,
00059:         "energy_profile": {
00060:             "low_avg": round(safe_mean(low_vals), 4),
00061:             "mid_avg": round(safe_mean(mid_vals), 4),
00062:             "high_avg": round(safe_mean(high_vals), 4),
00063:             "low_peak_avg": round(avg_top(low_vals), 4),
00064:             "mid_peak_avg": round(avg_top(mid_vals), 4),
00065:             "high_peak_avg": round(avg_top(high_vals), 4),
00066:             "onset_avg": round(safe_mean(onset_vals), 4),
00067:             "beat_avg": round(safe_mean(beat_vals), 4),
00068:         },
00069:     }
00070: 
00071:     out_json.parent.mkdir(parents=True, exist_ok=True)
00072:     with open(out_json, "w", encoding="utf-8") as f:
00073:         json.dump(summary, f, indent=2, ensure_ascii=False)
00074: 
00075:     print(f"[OK] Summary salvato in: {out_json}")
00076:     print(json.dumps(summary, indent=2, ensure_ascii=False))
00077: 
00078:     if update_music_context:
00079:         if tools_dir.exists():
00080:             if str(tools_dir) not in sys.path:
00081:                 sys.path.insert(0, str(tools_dir))
00082:             try:
00083:                 from build_music_context import build_music_context
00084: 
00085:                 manifest = build_music_context(
00086:                     analysis_path=analysis_json,
00087:                     track_summary_path=out_json,
00088:                     compact_json_path=OUTPUT_DIR / f"{summary['track_name']}_music_context.json",
00089:                 )
00090:             except Exception as exc:
00091:                 print(f"[WARN] Contesto musicale NPU non aggiornato: {exc}")
00092:             else:
00093:                 print(f"[OK] Contesto musicale NPU aggiornato: {manifest['context_md']}")
00094: 
00095:     return summary
00096: 
00097: 
00098: def main() -> None:
00099:     parser = argparse.ArgumentParser(description="Crea un riassunto tecnico da un analysis JSON.")
00100:     parser.add_argument("--analysis-json", default=str(ANALYSIS_JSON))
00101:     parser.add_argument("--out-json", default=str(OUT_JSON))
00102:     parser.add_argument("--skip-music-context", action="store_true")
00103:     args = parser.parse_args()
00104: 
00105:     build_summary(
00106:         analysis_json=Path(args.analysis_json).expanduser().resolve(),
00107:         out_json=Path(args.out_json).expanduser().resolve(),
00108:         update_music_context=not args.skip_music_context,
00109:     )
00110: 
00111: 
00112: if __name__ == "__main__":
00113:     main()
```
