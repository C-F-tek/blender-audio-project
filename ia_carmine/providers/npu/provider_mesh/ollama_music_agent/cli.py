from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from ia_carmine.providers.npu.paths import find_repo_root

from ia_carmine.providers.ollama.json_response import parse_json_response
from ia_carmine.providers.ollama.session import OllamaSession

ROOT = find_repo_root(__file__)
OUTPUT_DIR = ROOT / "output"
TOOLS_DIR = ROOT / "Tools" / "npu"

DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
DEFAULT_CONTEXT_JSON = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_analysis_ai_context.json"
DEFAULT_MUSIC_CONTEXT_JSON = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_music_context.json"
DEFAULT_OUT_JSON = OUTPUT_DIR / f"{DEFAULT_TRACK_STEM}_ollama_music_insights.json"
DEFAULT_OUT_MD = TOOLS_DIR / "ollama_music_insights.md"


def read_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def compact_context_for_prompt(context: dict) -> dict:
    analysis = context.get("analysis_summary", {})
    compact = {
        "analysis_summary": analysis,
        "track_summary": context.get("track_summary"),
        "ai_memory_context": context.get("ai_memory_context"),
        "scene_summaries": context.get("scene_summaries", []),
        "segments": [],
    }

    for segment in context.get("segments", []):
        compact["segments"].append(
            {
                "index": segment.get("index"),
                "start_sec": segment.get("start_sec"),
                "end_sec": segment.get("end_sec"),
                "dominant_band": segment.get("dominant_band"),
                "intensity_score": segment.get("intensity_score"),
                "intensity": segment.get("intensity"),
                "beat_count": segment.get("beat_count"),
                "stats": segment.get("stats"),
                "controls": segment.get("controls"),
                "top_events": segment.get("top_events", [])[:8],
            }
        )

    return compact


def build_prompt(context: dict) -> str:
    payload = json.dumps(compact_context_for_prompt(context), indent=2, ensure_ascii=False)
    return f"""
Sei un agente musicale locale per un video Blender audio-reactive.

Devi produrre un JSON operativo per aiutare gli script Blender e i prossimi hotpatch.
Il JSON completo frame-by-frame per Blender NON deve essere ridotto, sostituito o riscritto.
Usa questi segmenti solo per analisi, decisioni creative e suggerimenti.
Usa `ai_memory_context` come memoria utente/progetto: preferenze, correzioni, asset e vincoli valgono piu dei default generici.
Non ripetere il brief: interpreta il brano alla luce della memoria e produci decisioni utili.
Se la memoria cita due oggetti centrali ball opposti, pianifica una lettura duale/contrapposta del brano.

Rispondi SOLO con JSON valido, senza markdown.

Schema richiesto:
{{
  "model_role": "music_scene_agent",
  "global_read": {{
    "mood": "...",
    "tempo_interpretation": "...",
    "energy_shape": "...",
    "key_risks": ["..."]
  }},
  "segment_plan": [
    {{
      "segment": 1,
      "time_range": "0.0-16.0",
      "intent": "...",
      "hero_mesh": "...",
      "materials": "...",
      "fog": "...",
      "lights": "...",
      "camera": "...",
      "physics": "...",
      "avoid": "..."
    }}
  ],
  "scene_json_recommendations": {{
    "keep": ["..."],
    "change_candidates": ["..."],
    "do_not_touch": ["..."]
  }},
  "blender_keyframe_policy": {{
    "use_full_analysis_json": true,
    "do_not_reduce_frames": true,
    "notes": "..."
  }},
  "next_actions": ["..."]
}}

CONTESTO:
{payload}
""".strip()


def markdown_from_insights(data: dict, model: str) -> str:
    lines = [
        "# Ollama Music Insights\n\n",
        f"Generated: `{datetime.now().isoformat(timespec='seconds')}`\n\n",
        f"Model: `{model}`\n\n",
        "## Global Read\n",
    ]
    global_read = data.get("global_read", {})
    for key, value in global_read.items():
        lines.append(f"- `{key}`: {value}\n")

    lines.append("\n## Segment Plan\n")
    for item in data.get("segment_plan", []):
        lines.append(
            f"- Segment `{item.get('segment')}` `{item.get('time_range')}`: "
            f"{item.get('intent')} | hero `{item.get('hero_mesh')}` | fog `{item.get('fog')}`\n"
        )

    lines.append("\n## Keyframe Policy\n")
    policy = data.get("blender_keyframe_policy", {})
    for key, value in policy.items():
        lines.append(f"- `{key}`: {value}\n")

    lines.append("\n## Next Actions\n")
    for item in data.get("next_actions", []):
        lines.append(f"- {item}\n")

    return "".join(lines)


def run_ollama_music_agent(
    context_json: Path | str = DEFAULT_CONTEXT_JSON,
    fallback_context_json: Path | str = DEFAULT_MUSIC_CONTEXT_JSON,
    out_json: Path | str = DEFAULT_OUT_JSON,
    out_md: Path | str = DEFAULT_OUT_MD,
    model: str = "",
    base_url: str | None = None,
    keep_alive: str = "",
    max_new_tokens: int = 1800,
    temperature: float = 0.12,
    keep_server: bool = False,
    keep_model: bool = False,
) -> dict:
    if not str(model or "").strip():
        raise ValueError("ollama_model_explicit_required")
    if not str(keep_alive or "").strip():
        raise ValueError("ollama_keep_alive_explicit_required")
    context_path = Path(context_json)
    if not context_path.exists():
        context_path = Path(fallback_context_json)
    if not context_path.exists():
        raise FileNotFoundError(f"Context JSON not found: {context_path}")

    context = read_json(context_path)
    prompt = build_prompt(context)

    session_kwargs = {
        "model": model,
        "keep_alive": keep_alive,
        "shutdown_server": not keep_server,
        "unload_model": not keep_model,
    }
    if base_url:
        session_kwargs["base_url"] = base_url

    with OllamaSession(**session_kwargs) as session:
        text = session.generate(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
        used_model = session.model or model

    try:
        insights = parse_json_response(text)
    except Exception:
        insights = {
            "model_role": "music_scene_agent",
            "parse_error": True,
            "raw_response": text,
            "blender_keyframe_policy": {
                "use_full_analysis_json": True,
                "do_not_reduce_frames": True,
                "notes": "Raw model response could not be parsed; keep Blender frame JSON unchanged.",
            },
        }

    insights["generated_at"] = datetime.now().isoformat(timespec="seconds")
    insights["model"] = used_model
    insights["source_context"] = str(context_path)

    out_json = Path(out_json)
    out_md = Path(out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(insights, indent=2, ensure_ascii=False), encoding="utf-8")
    out_md.write_text(markdown_from_insights(insights, used_model), encoding="utf-8")

    print(f"[OK] Wrote: {out_json}")
    print(f"[OK] Wrote: {out_md}")
    return {"out_json": out_json, "out_md": out_md, "model": used_model}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Ollama on compact WAV/scene context and write AI insights."
    )
    parser.add_argument("--context-json", default=str(DEFAULT_CONTEXT_JSON))
    parser.add_argument("--fallback-context-json", default=str(DEFAULT_MUSIC_CONTEXT_JSON))
    parser.add_argument("--out-json", default=str(DEFAULT_OUT_JSON))
    parser.add_argument("--out-md", default=str(DEFAULT_OUT_MD))
    parser.add_argument("--model", default="")
    parser.add_argument("--base-url", default="")
    parser.add_argument("--keep-alive", default="")
    parser.add_argument("--max-new-tokens", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0.12)
    parser.add_argument("--keep-server", action="store_true")
    parser.add_argument("--keep-model", action="store_true")
    args = parser.parse_args()
    missing = []
    if not str(args.model or "").strip():
        missing.append("--model")
    if not str(args.base_url or "").strip():
        missing.append("--base-url")
    if not str(args.keep_alive or "").strip():
        missing.append("--keep-alive")
    if int(args.max_new_tokens or 0) <= 0:
        missing.append("--max-new-tokens")
    if missing:
        parser.error("missing explicit Ollama music agent parameter(s): " + ", ".join(missing))

    run_ollama_music_agent(
        context_json=args.context_json,
        fallback_context_json=args.fallback_context_json,
        out_json=args.out_json,
        out_md=args.out_md,
        model=args.model,
        base_url=args.base_url,
        keep_alive=args.keep_alive,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        keep_server=args.keep_server,
        keep_model=args.keep_model,
    )


if __name__ == "__main__":
    main()
