from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "output"
NPU_DIR = ROOT / "Tools" / "npu"
INDEX_AI_DIR = ROOT / "indexAI"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def file_status(path: Path) -> dict[str, Any]:
    exists = path.exists()
    return {
        "path": str(path),
        "exists": exists,
        "bytes": path.stat().st_size if exists and path.is_file() else 0,
        "updated": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")
        if exists
        else None,
    }


def compact_assets(asset_inventory: dict[str, Any]) -> list[dict[str, Any]]:
    assets = (
        asset_inventory.get("assets") if isinstance(asset_inventory.get("assets"), list) else []
    )
    result = []
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        role = asset.get("role")
        if role not in {"primary_ball_asset", "animated_effect_asset", "blend_scene_reference"}:
            continue
        result.append(
            {
                "role": role,
                "name": asset.get("name"),
                "path": asset.get("path"),
                "type": asset.get("type") or asset.get("extension"),
            }
        )
    return result[:24]


def infer_track_identity(track_stem: str) -> dict[str, Any]:
    clean = track_stem.replace("_Master", "").replace("_master", "").strip()
    title = clean
    artist = None
    if "-" in clean:
        parts = [part.strip() for part in clean.split("-") if part.strip()]
        if len(parts) >= 2:
            title = parts[0]
            artist = " - ".join(parts[1:])
    return {
        "track_stem": track_stem,
        "title": title,
        "artist": artist,
        "identity_source": "current workflow WAV filename/session",
        "external_metadata_allowed": False,
    }


def compact_track_read(music_context: dict[str, Any] | None) -> dict[str, Any]:
    music_context = music_context or {}
    summary = music_context.get("analysis_summary") or {}
    meta = summary.get("meta") or {}
    segments = music_context.get("segments") or []
    top_energy = summary.get("top_energy_segments") or []
    first = segments[0] if segments else {}
    last = segments[-1] if segments else {}
    return {
        "duration_sec": meta.get("duration_sec"),
        "fps": meta.get("fps"),
        "bpm": meta.get("estimated_tempo_bpm"),
        "segment_count": len(segments),
        "first_segment": {
            "dominant_band": first.get("dominant_band"),
            "intensity": first.get("intensity"),
            "controls": first.get("controls"),
        },
        "last_segment": {
            "dominant_band": last.get("dominant_band"),
            "intensity": last.get("intensity"),
            "controls": last.get("controls"),
        },
        "top_energy_segments": top_energy[:5],
    }


def deterministic_track_opinion(
    track_identity: dict[str, Any], music_context: dict[str, Any] | None
) -> str:
    read = compact_track_read(music_context)
    title = track_identity.get("title") or track_identity.get("track_stem")
    artist = track_identity.get("artist")
    name = f"{title} - {artist}" if artist else str(title)
    segment_count = read.get("segment_count") or 0
    bpm = read.get("bpm")
    first = read.get("first_segment") or {}
    last = read.get("last_segment") or {}
    top = read.get("top_energy_segments") or []
    top_bits = []
    for item in top[:3]:
        top_bits.append(
            f"segmento {item.get('index')} ({item.get('start_sec')}-{item.get('end_sec')}s, {item.get('dominant_band')}, {item.get('intensity')})"
        )

    lines = [
        f"Parlo del brano del progetto, `{name}`, non di metadati esterni.",
        f"Dai JSON lo leggo come una traccia con {segment_count} segmenti compatti"
        + (f" e BPM stimato {round(float(bpm), 2)}" if bpm else "")
        + ".",
        (
            f"L'apertura sembra guidata da banda `{first.get('dominant_band')}` con intensita `{first.get('intensity')}`, "
            f"mentre la coda arriva su `{last.get('dominant_band')}` / `{last.get('intensity')}`."
        ),
        "Da art direction lo tratterei come un brano da doppio fulcro: due `primary_ball_asset` centrali in controfase, uno piu materico e uno piu luminoso, usando tutti i frame del `blender_keyframes_json`.",
    ]
    if top_bits:
        lines.append("I punti da far respirare visivamente sono: " + "; ".join(top_bits) + ".")
    lines.append(
        "Quindi: niente narrativa generica da canzone pop; qui conviene costruire una scena audio-reactive precisa, con deformazioni mesh e materiali che seguono low/mid/high/onset/beat."
    )
    return "\n".join(lines)


def build_verified_answers(
    awareness: dict[str, Any], music_context: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    music_context = music_context or {}
    files = awareness.get("technical_files", {})
    state = awareness.get("pipeline_state", {})
    assets = (awareness.get("asset_awareness") or {}).get("primary_assets", [])
    primary_ball = next(
        (asset for asset in assets if asset.get("role") == "primary_ball_asset"), None
    )
    track_identity = awareness.get("track_identity", {})

    answers = [
        {
            "question": "Di che brano stiamo parlando?",
            "answer": (
                f"Il brano corrente e `{track_identity.get('title')}`"
                + (f" di `{track_identity.get('artist')}`" if track_identity.get("artist") else "")
                + ". Non usare titoli/artisti esterni non presenti nei file del progetto."
            ),
            "evidence": track_identity,
        },
        {
            "question": "Cosa pensi della traccia del progetto?",
            "answer": deterministic_track_opinion(track_identity, music_context),
            "evidence": compact_track_read(music_context),
        },
        {
            "question": "Abbiamo qualcosa che puo essere usata sui keyframe dell'audio?",
            "answer": (
                "Si. Usa `blender_keyframes_json`: contiene il JSON frame-by-frame completo con `frames` "
                "per low/mid/high/onset/beat. `music_context_json` e i segmenti servono solo per decisioni macro."
            ),
            "evidence": files.get("blender_keyframes_json", {}),
        },
        {
            "question": "Serve importare manualmente il WAV in Blender?",
            "answer": (
                "No. Il WAV e gia rappresentato dai JSON `analysis_json`, `music_context_json` e "
                "`blender_keyframes_json`. La chat deve parlare di pipeline/script, non di import audio manuale."
            ),
            "evidence": {
                "audio_already_loaded_by_pipeline": state.get("audio_already_loaded_by_pipeline"),
                "analysis_json": files.get("analysis_json", {}),
            },
        },
        {
            "question": "Quale asset va usato quando l'utente dice ball?",
            "answer": (
                f"Usa `primary_ball_asset`: {primary_ball.get('path')}"
                if primary_ball
                else "Cerca un asset con ruolo `primary_ball_asset` nell'asset inventory."
            ),
            "evidence": primary_ball or {},
        },
        {
            "question": "La pipeline e pronta per generare lo script scena?",
            "answer": (
                "Si: analisi, music context, project index, service packet e scene brief risultano pronti. Il manual corpus Blender e escluso dal contesto default."
                if state.get("can_generate_scene_script")
                else "Non completamente: controlla `missing_or_suspicious` e i technical_files mancanti."
            ),
            "evidence": state,
        },
        {
            "question": "Quanti segmenti musicali compatti sono disponibili?",
            "answer": f"Sono disponibili {state.get('segment_count', len(music_context.get('segments') or []))} segmenti compatti.",
            "evidence": {
                "segment_count": state.get(
                    "segment_count", len(music_context.get("segments") or [])
                )
            },
        },
    ]
    return answers


def build_preflight_answers_for_message(
    user_message: str,
    awareness: dict[str, Any],
    music_context: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    text = user_message.lower()
    answers = build_verified_answers(awareness, music_context)
    selected: list[dict[str, Any]] = []
    keyword_map = [
        (("chi", "titolo", "artista", "nome"), 0),
        (("cosa pensi", "traccia", "brano", "musical"), 1),
        (("keyframe", "audio", "wave", "wav"), 2),
        (("import", "blender", "wav", "wave", "audio"), 3),
        (("ball", "sfera", "asset"), 4),
        (("script", "gener", "prossimo", "ora", "pipeline"), 5),
        (("segment", "chunk"), 6),
    ]
    for keywords, index in keyword_map:
        if any(keyword in text for keyword in keywords):
            selected.append(answers[index])
    if not selected:
        selected = [answers[0], answers[3]]
    seen = set()
    unique = []
    for item in selected:
        key = item["question"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique[:4]


def build_project_awareness(
    *,
    track_stem: str,
    audio_path: str,
    output_dir: Path | None = None,
    asset_inventory: dict[str, Any] | None = None,
    music_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    output_dir = Path(output_dir or OUTPUT_DIR)
    slug = "".join(ch.lower() if ch.isalnum() else "_" for ch in track_stem).strip("_")
    slug = "_".join(part for part in slug.split("_") if part)

    key_paths = {
        "analysis_json": output_dir / f"{track_stem}_analysis.json",
        "track_summary_json": output_dir / f"{track_stem}_track_summary.json",
        "music_context_json": output_dir / f"{track_stem}_music_context.json",
        "analysis_ai_context_json": output_dir / f"{track_stem}_analysis_ai_context.json",
        "blender_keyframes_json": output_dir / f"{track_stem}_analysis_blender_keyframes.json",
        "scene_brief_json": output_dir / f"{track_stem}_scene_brief.json",
        "asset_inventory_json": output_dir / "spaziotempo_asset_inventory.json",
        "dual_ai_plan_json": output_dir / f"{track_stem}_dual_ai_scene_plan.json",
        "gpu_task_packet_json": output_dir / f"{track_stem}_gpu_task_packet.json",
        "ai_implementation_draft_json": output_dir / f"{track_stem}_ai_implementation_draft.json",
        "generated_scene_script": INDEX_AI_DIR
        / "scene_scripts"
        / f"{slug}_scene_builder_candidate.py",
        "project_code_index": INDEX_AI_DIR / "project_code_index.md",
        "project_code_manifest": INDEX_AI_DIR / "project_code_manifest.json",
        "npu_music_context_md": NPU_DIR / "npu_music_context.md",
        "npu_music_manifest": NPU_DIR / "npu_music_manifest.json",
        "npu_code_index": NPU_DIR / "npu_code_index.md",
        "npu_manual_generator": NPU_DIR / "build_blender_manual_context.py",
        "npu_preflight": NPU_DIR / "npu_preflight_report.json",
    }

    statuses = {name: file_status(path) for name, path in key_paths.items()}
    missing = [
        name
        for name, item in statuses.items()
        if not item["exists"]
        and name not in {"ai_implementation_draft_json", "generated_scene_script"}
    ]
    ready_inputs = all(
        statuses[name]["exists"]
        for name in [
            "analysis_json",
            "music_context_json",
            "analysis_ai_context_json",
            "blender_keyframes_json",
        ]
    )
    can_generate_script = (
        ready_inputs
        and statuses["scene_brief_json"]["exists"]
        and statuses["asset_inventory_json"]["exists"]
    )

    music_context = music_context or read_json(key_paths["music_context_json"])
    asset_inventory = asset_inventory or read_json(output_dir / "spaziotempo_asset_inventory.json")
    npu_preflight = read_json(key_paths["npu_preflight"])
    segment_count = len(music_context.get("segments") or [])

    awareness = {
        "format": "SPAZIOTEMPO_PROJECT_AWARENESS_V1",
        "generated_at": now_iso(),
        "track_stem": track_stem,
        "audio_path": audio_path,
        "track_identity": infer_track_identity(track_stem),
        "project_identity": {
            "name": "Spaziotempo Blender audio-reactive album visual pipeline",
            "root": str(ROOT),
            "user_runs_blender_and_render": True,
            "assistant_should_not_launch_blender_or_render": True,
            "current_goal": "Generate/review standalone Blender scene scripts from WAV-derived JSON, memory, assets and project style.",
        },
        "pipeline_state": {
            "audio_already_loaded_by_pipeline": Path(audio_path).exists(),
            "wav_analysis_ready": ready_inputs,
            "music_context_ready": statuses["music_context_json"]["exists"],
            "project_index_ready": statuses["project_code_index"]["exists"],
            "manual_corpus_default_excluded": True,
            "manual_generator_ready": statuses["npu_manual_generator"]["exists"],
            "service_packet_ready": statuses["gpu_task_packet_json"]["exists"],
            "scene_brief_ready": statuses["scene_brief_json"]["exists"],
            "can_generate_scene_script": can_generate_script,
            "segment_count": segment_count,
        },
        "technical_files": statuses,
        "asset_awareness": {
            "asset_count": asset_inventory.get("asset_count", 0),
            "primary_assets": compact_assets(asset_inventory),
        },
        "npu_context": {
            "preflight_ready": bool(npu_preflight.get("ready")) if npu_preflight else False,
            "available_devices": npu_preflight.get("available_devices", [])
            if npu_preflight
            else [],
            "can_delegate_uncertainty": bool(npu_preflight.get("ready")),
            "fallback": "If NPU is not ready, use deterministic project awareness and existing chunks instead of pretending uncertainty.",
        },
        "director_rules": [
            "Never suggest manually importing audio into Blender; the WAV is already represented by analysis/music/keyframe JSON.",
            "Never suggest opening Blender as the next generic step; the user decides when to run Blender.",
            "Do not suggest rebuilding from scratch if technical files already exist.",
            "When technical files exist, refer to the pipeline action: scene brief, dual AI plan, scene script draft, hot update, or review generated script.",
            "Use project asset roles. If user says ball, prefer primary_ball_asset.",
            "Full analysis_blender_keyframes JSON is authoritative and must not be summarized away.",
            "If unsure, say which technical file/chunk should be checked, not generic Blender advice.",
        ],
        "missing_or_suspicious": missing,
    }
    awareness["verified_answers"] = build_verified_answers(awareness, music_context)
    return awareness


def save_project_awareness(awareness: dict[str, Any]) -> dict[str, str]:
    patch_dir = INDEX_AI_DIR / "patch_library"
    patch_dir.mkdir(parents=True, exist_ok=True)
    slug = "".join(
        ch.lower() if ch.isalnum() else "_" for ch in str(awareness.get("track_stem", "track"))
    ).strip("_")
    slug = "_".join(part for part in slug.split("_") if part)
    json_path = patch_dir / f"{slug}_project_awareness.json"
    md_path = patch_dir / f"{slug}_project_awareness.md"
    json_path.write_text(json.dumps(awareness, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# Spaziotempo Project Awareness\n\n",
        f"Generated: `{awareness.get('generated_at')}`\n\n",
        f"Track: `{awareness.get('track_stem')}`\n\n",
        "## Pipeline State\n",
    ]
    for key, value in (awareness.get("pipeline_state") or {}).items():
        lines.append(f"- `{key}`: `{value}`\n")
    lines.append("\n## Director Rules\n")
    for rule in awareness.get("director_rules", []):
        lines.append(f"- {rule}\n")
    lines.append("\n## Primary Assets\n")
    for asset in (awareness.get("asset_awareness") or {}).get("primary_assets", []):
        lines.append(f"- `{asset.get('role')}`: `{asset.get('path')}`\n")
    md_path.write_text("".join(lines), encoding="utf-8")
    return {"json": str(json_path), "md": str(md_path)}
