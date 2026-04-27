from pathlib import Path
import argparse
import json
import sys
from statistics import mean

ROOT = Path.home() / "blender"
PROJECT_DIR = ROOT / "blender-audio-project"
OUTPUT_DIR = PROJECT_DIR / "output"

ANALYSIS_JSON = OUTPUT_DIR / "Feel The Light-Luca Vera_Master_analysis.json"
OUT_JSON = OUTPUT_DIR / "Feel The Light-Luca Vera_Master_track_summary.json"


def avg_top(values, ratio=0.1):
    if not values:
        return 0.0
    n = max(1, int(len(values) * ratio))
    return mean(sorted(values, reverse=True)[:n])


def safe_mean(values):
    return mean(values) if values else 0.0


def build_summary(analysis_json: Path, out_json: Path, update_music_context: bool = True) -> dict:
    with open(analysis_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["meta"]
    frames = data["frames"]

    low_vals = [float(x.get("low", 0.0)) for x in frames]
    mid_vals = [float(x.get("mid", 0.0)) for x in frames]
    high_vals = [float(x.get("high", 0.0)) for x in frames]
    onset_vals = [float(x.get("onset", 0.0)) for x in frames]
    beat_vals = [float(x.get("beat", 0.0)) for x in frames]

    track_name = analysis_json.stem.replace("_analysis", "")
    ai_memory_context = {}
    tools_dir = PROJECT_DIR / "Tools" / "npu"
    if tools_dir.exists():
        if str(tools_dir) not in sys.path:
            sys.path.insert(0, str(tools_dir))
        try:
            from ai_memory_context import build_ai_memory_context

            ai_memory_context = build_ai_memory_context(track_stem=track_name, output_dir=out_json.parent)
        except Exception:
            ai_memory_context = {}

    summary = {
        "track_name": track_name,
        "source_analysis_json": str(analysis_json),
        "duration_sec": meta.get("duration_sec"),
        "fps": meta.get("fps"),
        "estimated_tempo_bpm": meta.get("estimated_tempo_bpm"),
        "ai_memory_context": ai_memory_context,
        "energy_profile": {
            "low_avg": round(safe_mean(low_vals), 4),
            "mid_avg": round(safe_mean(mid_vals), 4),
            "high_avg": round(safe_mean(high_vals), 4),
            "low_peak_avg": round(avg_top(low_vals), 4),
            "mid_peak_avg": round(avg_top(mid_vals), 4),
            "high_peak_avg": round(avg_top(high_vals), 4),
            "onset_avg": round(safe_mean(onset_vals), 4),
            "beat_avg": round(safe_mean(beat_vals), 4),
        },
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"[OK] Summary salvato in: {out_json}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if update_music_context:
        if tools_dir.exists():
            if str(tools_dir) not in sys.path:
                sys.path.insert(0, str(tools_dir))
            try:
                from build_music_context import build_music_context

                manifest = build_music_context(
                    analysis_path=analysis_json,
                    track_summary_path=out_json,
                    compact_json_path=OUTPUT_DIR / f"{summary['track_name']}_music_context.json",
                )
            except Exception as exc:
                print(f"[WARN] Contesto musicale NPU non aggiornato: {exc}")
            else:
                print(f"[OK] Contesto musicale NPU aggiornato: {manifest['context_md']}")

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea un riassunto tecnico da un analysis JSON.")
    parser.add_argument("--analysis-json", default=str(ANALYSIS_JSON))
    parser.add_argument("--out-json", default=str(OUT_JSON))
    parser.add_argument("--skip-music-context", action="store_true")
    args = parser.parse_args()

    build_summary(
        analysis_json=Path(args.analysis_json).expanduser().resolve(),
        out_json=Path(args.out_json).expanduser().resolve(),
        update_music_context=not args.skip_music_context,
    )


if __name__ == "__main__":
    main()
