from __future__ import annotations

from pathlib import Path
import argparse
import json
import subprocess
from datetime import datetime
from typing import Any

from build_music_context import build_music_context
from build_npu_code_context import main as build_code_context
from build_blender_manual_context import build_manual_context
from build_ai_service_packet import build_ai_service_packet, slugify as packet_slugify
from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index
from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report
from ollama_runtime import OllamaModelManager, parse_json_response
from run_ollama_music_agent import build_prompt as build_music_prompt
from run_ollama_music_agent import markdown_from_insights

try:
    from pipeline.artifact_paths import is_allowed_generated_artifact_path, normalize_repo_relative_path
    from pipeline.artifact_writer import PlannedArtifactWrite, write_planned_artifact
    from pipeline.context_builder import summarize_music_context
    from pipeline.io_utils import read_json, read_optional_json, read_text, write_json
    from pipeline.prompts import (
        build_creative_scene_prompt_payload,
        build_implementation_retry_payload,
        build_merge_prompt_payload,
    )
    from pipeline.validators import validate_implementation_draft_contract
except ImportError:  # Allows package-style imports from repo-root validation.
    from Tools.npu.pipeline.artifact_paths import is_allowed_generated_artifact_path, normalize_repo_relative_path  # type: ignore
    from Tools.npu.pipeline.artifact_writer import PlannedArtifactWrite, write_planned_artifact  # type: ignore
    from Tools.npu.pipeline.context_builder import summarize_music_context  # type: ignore
    from Tools.npu.pipeline.io_utils import read_json, read_optional_json, read_text, write_json  # type: ignore
    from Tools.npu.pipeline.prompts import (  # type: ignore
        build_creative_scene_prompt_payload,
        build_implementation_retry_payload,
        build_merge_prompt_payload,
    )
    from Tools.npu.pipeline.validators import validate_implementation_draft_contract  # type: ignore


ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = ROOT / "Tools" / "npu"
OUTPUT_DIR = ROOT / "output"

DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
TRACK_STEM = DEFAULT_TRACK_STEM

MUSIC_AI_CONTEXT = OUTPUT_DIR / f"{TRACK_STEM}_analysis_ai_context.json"
DUAL_PLAN_JSON = OUTPUT_DIR / f"{TRACK_STEM}_dual_ai_scene_plan.json"
DUAL_BRIEF_MD = TOOLS_DIR / "dual_ai_blender_agent_brief.md"
OLLAMA_INSIGHTS_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ollama_music_insights.json"
OLLAMA_INSIGHTS_MD = TOOLS_DIR / "ollama_music_insights.md"
NPU_TECH_MD = TOOLS_DIR / "npu_dual_ai_technical_notes.md"
NPU_PREFLIGHT_JSON = TOOLS_DIR / "npu_preflight_report.json"
IMPLEMENTATION_DRAFT_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ai_implementation_draft.json"
IMPLEMENTATION_SCRIPT = TOOLS_DIR / "generated_blender_script_candidate.py"
IMPLEMENTATION_NOTES = TOOLS_DIR / "generated_implementation_notes.md"
NPU_IMPLEMENTATION_NOTES = TOOLS_DIR / "npu_dual_ai_implementation_notes.md"


ALLOWED_NEW_PREFIXES = ("indexAI/scene_scripts/", "indexAI/patch_library/")
PREFERRED_IMPLEMENTATION_FILES = (
    "Scripting/v61b/materials.py",
    "Scripting/v61b/fog_dynamics.py",
    "Scripting/v61b/physics_setup.py",
    "Scripting/v61b/scene_tuning_panel.py",
    "Scripting/v61b/config.py",
    "Scripting/v61b/render_setup.py",
    "Scripting/v61b/hot_update_scene_v61b.py",
)


def update_track_paths(track_stem: str, analysis_ai_context: str | None = None) -> None:
    global TRACK_STEM
    global MUSIC_AI_CONTEXT, DUAL_PLAN_JSON, OLLAMA_INSIGHTS_JSON
    global IMPLEMENTATION_DRAFT_JSON

    TRACK_STEM = track_stem
    MUSIC_AI_CONTEXT = Path(analysis_ai_context) if analysis_ai_context else OUTPUT_DIR / f"{TRACK_STEM}_analysis_ai_context.json"
    DUAL_PLAN_JSON = OUTPUT_DIR / f"{TRACK_STEM}_dual_ai_scene_plan.json"
    OLLAMA_INSIGHTS_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ollama_music_insights.json"
    IMPLEMENTATION_DRAFT_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ai_implementation_draft.json"


def apply_default_input_paths(args: argparse.Namespace) -> None:
    if args.analysis is None:
        args.analysis = str(OUTPUT_DIR / f"{args.track_stem}_analysis.json")
    if args.track_summary is None:
        args.track_summary = str(OUTPUT_DIR / f"{args.track_stem}_track_summary.json")
    if args.compact_json is None:
        args.compact_json = str(OUTPUT_DIR / f"{args.track_stem}_music_context.json")
    if args.analysis_ai_context is None:
        args.analysis_ai_context = str(OUTPUT_DIR / f"{args.track_stem}_analysis_ai_context.json")
    if args.blender_keyframes_json is None:
        args.blender_keyframes_json = str(OUTPUT_DIR / f"{args.track_stem}_analysis_blender_keyframes.json")


def validate_input_files(args: argparse.Namespace) -> None:
    required = [
        ("analysis JSON", Path(args.analysis)),
        ("track summary JSON", Path(args.track_summary)),
        ("compact music context JSON", Path(args.compact_json)),
        ("analysis AI context JSON", Path(args.analysis_ai_context)),
        ("full Blender keyframes JSON", Path(args.blender_keyframes_json)),
    ]
    if args.phase == "implementation":
        required.append(("dual AI scene plan JSON", DUAL_PLAN_JSON))

    missing = [f"{label}: {path}" for label, path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Prerequisiti mancanti per la pipeline AI:\n"
            + "\n".join(f"- {item}" for item in missing)
            + "\nEsegui/rigenera analysis, track summary, music context e piano prima del draft."
        )


def looks_degraded_text(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 260:
        return True
    alnum = sum(ch.isalnum() for ch in stripped)
    visible = sum(not ch.isspace() for ch in stripped)
    if visible and alnum / visible < 0.45:
        return True
    markdown_heads = stripped.count("##")
    useful_words = sum(
        stripped.lower().count(word)
        for word in ["audio", "blender", "segment", "material", "fog", "light", "mesh"]
    )
    return markdown_heads < 2 and useful_words < 5


def deterministic_technical_notes(music_context: dict[str, Any], project_manifest: dict[str, Any], reason: str) -> str:
    music_summary = summarize_music_context(music_context)
    summary = music_summary["analysis_summary"]
    track_summary = music_summary["track_summary"]
    files = project_manifest.get("files") or []
    priority_files = [
        item.get("file")
        for item in files
        if item.get("file", "").endswith((
            "Scripting/v61b/config.py",
            "Scripting/v61b/materials.py",
            "Scripting/v61b/fog_dynamics.py",
            "Scripting/v61b/physics_setup.py",
            "Scripting/v61b/scene_tuning_panel.py",
            "Tools/workflow/workflow_state.py",
            "Tools/npu/run_dual_ai_pipeline.py",
        ))
    ]

    lines = [
        "# Deterministic Technical Notes\n\n",
        f"Reason: NPU output was not trusted (`{reason}`).\n\n",
        "## Track Map\n",
        f"- Duration: `{summary.get('duration_sec', track_summary.get('duration_sec', '?'))}` seconds.\n",
        f"- FPS: `{summary.get('fps', track_summary.get('fps', '?'))}`.\n",
        f"- BPM: `{summary.get('estimated_tempo_bpm', track_summary.get('estimated_tempo_bpm', '?'))}`.\n",
        f"- Segment count: `{music_summary['segment_count']}`.\n\n",
        "## Project Primary Files\n",
    ]
    for file_name in priority_files[:20]:
        lines.append(f"- `{file_name}`\n")

    lines.extend(
        [
            "\n## Safe Implementation Policy\n",
            "- Use full frame-by-frame Blender keyframe JSON as data input only.\n",
            "- Generate patch plans against existing project files, not monolithic replacement scripts.\n",
            "- Prefer hotpatch/panel/update modules for materials, fog, lights and render changes.\n",
            "- Require a reload only when primary object creation or scene topology changes.\n\n",
            "## Audio Control Map\n",
            "- Low band: hero mesh deformation scale, gravity/attractor strength, fog density body.\n",
            "- Mid band: material roughness/emission mix, secondary object motion, fog filament drift.\n",
            "- High band: small emission accents, glints, particle sparkle, sharp camera micro motion.\n",
            "- Onset/beat: short impulses, never a constant global light flash.\n\n",
        ]
    )
    return "".join(lines)


def run_npu_technical_pass(args: argparse.Namespace) -> str:
    script = TOOLS_DIR / "run_npu_review.py"
    python_exe = Path(args.npu_python)
    cmd = [
        str(python_exe),
        str(script),
        "--engine",
        "npu",
        "--domain",
        "music",
        "--mode",
        "chunked",
        "--context",
        str(TOOLS_DIR / "npu_music_context.md"),
        "--chunk-dir",
        str(TOOLS_DIR / "npu_music_chunks"),
        "--out",
        str(NPU_TECH_MD),
        "--notes-out",
        str(TOOLS_DIR / "npu_dual_ai_chunk_notes.md"),
        "--max-context-chars",
        "0",
        "--chunk-chars",
        "10500",
        "--chunk-overlap-chars",
        "700",
        "--max-prompt-chars",
        "15000",
        "--max-chunk-tokens",
        str(args.npu_chunk_tokens),
        "--max-reduce-tokens",
        str(args.npu_reduce_tokens),
        "--max-new-tokens",
        str(args.npu_final_tokens),
        "--max-prompt-len",
        "16384",
        "--min-response-len",
        "64",
    ]

    subprocess.run(cmd, check=True)
    return read_text(NPU_TECH_MD)


def build_creative_scene_prompt(music_context: dict[str, Any], npu_notes: str, project_index: str) -> str:
    payload_data = build_creative_scene_prompt_payload(
        music_context,
        npu_notes=npu_notes,
        project_index=project_index,
    )
    payload = json.dumps(payload_data, indent=2, ensure_ascii=False)
    return f"""
Sei il generatore creativo locale per una scena Blender audio-reactive.

Hai un contesto musicale compatto, scene JSON esistenti e note tecniche NPU.
Devi proporre una scena piu ricca SENZA cambiare direttamente codice Blender.
Il codice reale del progetto e' la fonte primaria: rispetta file, moduli e funzioni esistenti.
Il JSON full frame per Blender deve restare completo e invariato.

Rispondi SOLO con JSON valido.

Schema richiesto:
{{
  "creative_intent": "...",
  "visual_language": {{
    "background": "...",
    "hero": "...",
    "fog": "...",
    "materials": "...",
    "lights": "...",
    "physics": "..."
  }},
  "scene_layers": [
    {{
      "layer": "Hero",
      "objects": ["..."],
      "audio_drivers": ["low", "mid", "high", "onset", "beat"],
      "implementation_hint": "..."
    }}
  ],
  "segment_variations": [
    {{
      "segment": 1,
      "time_range": "0.0-16.0",
      "variation": "...",
      "material_modulation": "...",
      "fog_modulation": "...",
      "light_modulation": "...",
      "camera_modulation": "..."
    }}
  ],
  "render_safety": {{
    "heavy_features_to_avoid": ["..."],
    "fast_preview_strategy": "...",
    "final_strategy": "..."
  }},
  "json_outputs_to_create": ["..."],
  "do_not_touch": ["full analysis frame JSON", "..."]
}}

CONTESTO:
{payload}
""".strip()


def build_merge_prompt(
    music_context: dict[str, Any],
    npu_notes: str,
    creative: dict[str, Any],
    technical: dict[str, Any],
) -> str:
    payload = build_merge_prompt_payload(
        music_context,
        npu_notes=npu_notes,
        project_index=read_text(PROJECT_INDEX_MD),
        creative=creative,
        technical=technical,
    )
    return f"""
Sei l'orchestratore finale NPU+Ollama per Blender.

Devi fondere note tecniche e proposte creative in un piano applicabile, ma NON applicare niente.
Il piano deve essere prudente, modulare e compatibile con hotpatch successivi.

Rispondi SOLO con JSON valido.

Schema:
{{
  "pipeline_policy": {{
    "use_full_blender_keyframes_json": true,
    "ai_context_is_analysis_only": true,
    "ollama_model_switch_policy": "unload previous model before loading next"
  }},
  "recommended_scene_plan": {{
    "summary": "...",
    "priority_changes": ["..."],
    "defer_changes": ["..."]
  }},
  "file_plan": {{
    "read_only": ["..."],
    "hotpatch_candidates": ["..."],
    "json_outputs": ["..."],
    "must_use_existing_files": true
  }},
  "audio_mapping_plan": {{
    "hero_mesh": "...",
    "materials": "...",
    "fog": "...",
    "lights": "...",
    "physics": "...",
    "camera": "..."
  }},
  "safety_checks": ["..."],
  "next_commands": ["..."]
}}

DATI:
{json.dumps(payload, indent=2, ensure_ascii=False)}
""".strip()


def build_implementation_prompt(
    plan: dict[str, Any],
    npu_notes: str,
    include_manual: bool,
    gpu_packet: dict[str, Any] | None = None,
    scene_brief: dict[str, Any] | None = None,
    asset_inventory: dict[str, Any] | None = None,
) -> str:
    manual_index = read_text(TOOLS_DIR / "npu_blender_manual_index.md")[:12000] if include_manual else ""
    project_index = read_text(PROJECT_INDEX_MD)[:14000]
    project_manifest = read_text(PROJECT_MANIFEST_JSON)[:10000]
    guide = read_text(ROOT / "Scripting" / "v61b" / "SCENE_TUNING_GUIDE.md")[:10000]
    project_structure = read_text(ROOT / "Scripting" / "v61b" / "PROJECT_STRUCTURE.md")[:8000]
    previous_scene_script = read_text(generated_scene_script_abspath())[:18000]
    slug = packet_slugify(TRACK_STEM)

    payload = {
        "ai_operating_contract": {
            "role": "GPU code interpreter / Blender Python writer",
            "memory_first": "Apply scene_director_brief and conversation_memory before older plan defaults.",
            "chunk_protocol": "Use gpu_task_packet as compact router; use referenced JSON files at runtime for exact frame data.",
            "full_keyframe_rule": "Generated script must load BLENDER_KEYFRAMES_JSON and iterate keyframes['frames'] without reducing it.",
            "asset_rule": "Use asset_inventory roles. primary_ball_asset is the real ball asset.",
            "failure_rule": "If the model cannot produce valid code, deterministic fallback will be used and marked in validation.",
        },
        "gpu_task_packet": gpu_packet,
        "dual_ai_plan": plan,
        "npu_notes": npu_notes[:14000],
        "primary_project_index": project_index,
        "primary_project_manifest": project_manifest,
        "project_structure": project_structure,
        "scene_tuning_guide": guide,
        "manual_index": manual_index,
        "scene_director_brief": scene_brief or {},
        "asset_inventory": asset_inventory or {},
        "previous_generated_scene_script": previous_scene_script,
    }

    return f"""
Sei un code interpreter Blender Python che lavora come GPU writer.

Devi generare una BOZZA NUOVA, separata dal progetto vivo.
Non devi modificare file esistenti del progetto.
I file esistenti sono SOLO reference/style/source-map.
Devi mantenere stile, nomi e logica del progetto guardando primary_project_index, ma scrivere solo in `indexAI/scene_scripts/`.
Il codice candidato non deve essere vuoto: deve contenere Python Blender eseguibile come script standalone per creare una nuova scena da JSON.
Lo script deve leggere i JSON di contesto, creare materiali, oggetti, modifier/deformazioni, keyframe audio-reactive e camera/luci.
Per l'animazione Blender usa il file full `analysis_blender_keyframes.json` e tutti gli elementi `frames`; i segmenti compatti servono solo per composizione e macro-scelte.
Se l'utente chiede modifiche nel scene_director_brief, applicale come revisione dello script precedente.
Se il brief nomina asset gia presenti, usa asset_inventory. `primary_ball_asset` e' la ball reale del progetto, non sostituirla con una sfera generica salvo fallback.
Se lo script diventa complesso, puoi dividerlo in piu file sotto `indexAI/scene_scripts/{slug}_scene_bundle/` usando `support_files`.
Non accettare placeholder, TODO, `pass`, scene minime con solo camera/luce/piano, o spiegazioni al posto del codice.
Non ridurre il JSON frame-by-frame del brano.
Non inventare API se nel manuale/indice non sono presenti; se non sei sicuro, scrivi note.
Se scene_director_brief contiene "due oggetti centrali" o "ball", lo script deve importare/istanziare `primary_ball_asset` due volte, con animazioni in controfase e mapping audio invertito.

Rispondi SOLO con JSON valido.
Il primo carattere della risposta deve essere {{ e l'ultimo deve essere }}.
Non usare Markdown, non usare blocchi ```json, non scrivere documentazione.

Schema obbligatorio:
{{
  "implementation_kind": "new_blender_scene_script_from_json",
  "safety": {{
    "does_not_modify_full_analysis_json": true,
    "does_not_modify_project_source_files": true,
    "requires_manual_review": true,
      "needs_blender_run": true
  }},
  "reference_files": [
    {{
      "file": "Scripting/v61b/materials.py",
      "exists_in_project_index": true,
      "reason": "style/source reference only"
    }}
  ],
  "proposed_files": [
    {{
      "file": "indexAI/scene_scripts/{slug}_scene_builder_candidate.py",
      "kind": "standalone_blender_scene_builder",
      "why": "new scene script, not a patch to the existing project"
    }}
  ],
  "implementation_plan": [
    {{
      "reference_file": "Scripting/v61b/materials.py",
      "new_file": "indexAI/scene_scripts/{slug}_scene_builder_candidate.py",
      "change": "...",
      "why": "...",
      "risk": "low|medium|high",
      "manual_check": "..."
    }}
  ],
  "new_files_allowed": ["indexAI/scene_scripts/...", "indexAI/patch_library/..."],
  "scene_script": "codice Python Blender completo e non vuoto",
  "support_files": [
    {{
      "file": "indexAI/scene_scripts/{slug}_scene_bundle/README.md",
      "kind": "notes|module|manifest|brief_snapshot",
      "content": "contenuto completo del file"
    }}
  ],
  "notes": ["..."],
  "files_to_review_before_applying": ["..."],
  "expected_panel_or_operator": "..."
}}

CONTESTO:
{json.dumps(payload, indent=2, ensure_ascii=False)}
""".strip()


def build_implementation_retry_prompt(
    plan: dict[str, Any],
    invalid_draft: dict[str, Any],
    validation: dict[str, Any],
) -> str:
    del invalid_draft  # The retry only needs the validation errors, not the full invalid text.

    manifest = read_json(PROJECT_MANIFEST_JSON) if PROJECT_MANIFEST_JSON.exists() else {}
    indexed_files = sorted(
        item.get("file")
        for item in manifest.get("files", [])
        if item.get("file")
    )
    preferred_files = [file_name for file_name in indexed_files if file_name in PREFERRED_IMPLEMENTATION_FILES]

    payload = build_implementation_retry_payload(
        plan,
        preferred_existing_files=preferred_files,
        allowed_new_prefixes=ALLOWED_NEW_PREFIXES,
        validation=validation,
    )

    return f"""
Rispondi esclusivamente con un singolo oggetto JSON valido.

REGOLE OBBLIGATORIE:
- Il primo carattere della risposta deve essere {{.
- L'ultimo carattere della risposta deve essere }}.
- Non usare Markdown.
- Non usare blocchi ```json.
- Non scrivere documentazione.
- Non spiegare il progetto.
- Non includere testo prima o dopo il JSON.
- Usa preferred_existing_files solo come reference/style.
- Scrivi nuovi file solo sotto i prefissi consentiti.
- Non modificare il full analysis JSON frame-by-frame.
- scene_script deve contenere codice Python Blender completo, con lettura JSON, keyframe_insert, materiali e modifier.
- scene_script deve usare tutti i frame del full Blender keyframes JSON, non solo i segmenti compatti.
- Non usare placeholder, TODO, pass, o scene minime con solo camera/luce/piano.

Schema obbligatorio:
{{
  "implementation_kind": "new_blender_scene_script_from_json",
  "safety": {{
    "does_not_modify_full_analysis_json": true,
    "does_not_modify_project_source_files": true,
    "requires_manual_review": true,
    "needs_blender_run": true
  }},
  "reference_files": [
    {{
      "file": "Scripting/v61b/materials.py",
      "exists_in_project_index": true,
      "reason": "style/source reference only"
    }}
  ],
  "proposed_files": [
    {{
      "file": "indexAI/scene_scripts/generated_scene_builder_candidate.py",
      "kind": "standalone_blender_scene_builder",
      "why": "new scene script, not a project patch"
    }}
  ],
  "implementation_plan": [
    {{
      "reference_file": "Scripting/v61b/materials.py",
      "new_file": "indexAI/scene_scripts/generated_scene_builder_candidate.py",
      "change": "...",
      "why": "...",
      "risk": "low",
      "manual_check": "..."
    }}
  ],
  "new_files_allowed": [
    "indexAI/scene_scripts/...",
    "indexAI/patch_library/..."
  ],
  "scene_script": "import bpy\\n...",
  "notes": ["..."],
  "files_to_review_before_applying": ["..."],
  "expected_panel_or_operator": "..."
}}

DATI:
{json.dumps(payload, indent=2, ensure_ascii=False)}
""".strip()


def safe_parse_json(text: str, fallback_key: str) -> dict[str, Any]:
    try:
        parsed = parse_json_response(text)
        return parsed if isinstance(parsed, dict) else {fallback_key: text, "parse_error": True}
    except Exception:
        return {fallback_key: text, "parse_error": True}


def extract_python_script(text: str) -> str:
    stripped = text.strip()
    if "```" in stripped:
        parts = stripped.split("```")
        for index, part in enumerate(parts):
            body = part
            if index % 2 == 1:
                lines = body.splitlines()
                if lines and lines[0].strip().lower() in {"python", "py"}:
                    body = "\n".join(lines[1:])
                if "import bpy" in body:
                    return body.strip()
    if "import bpy" in stripped:
        start = stripped.find("from __future__")
        if start < 0:
            start = stripped.find("import bpy")
        return stripped[start:].strip()
    return ""


def draft_from_raw_python_script(text: str, model: str | None, reason: str) -> dict[str, Any] | None:
    script = extract_python_script(text)
    if not script:
        return None
    new_file = generated_scene_script_relpath()
    reference_files = [
        {
            "file": path,
            "exists_in_project_index": True,
            "reason": "Style/source reference only; not modified by this generated scene script.",
        }
        for path in PREFERRED_IMPLEMENTATION_FILES
        if path in get_indexed_project_files()
    ]
    return {
        "implementation_kind": "new_blender_scene_script_from_json",
        "safety": {
            "does_not_modify_full_analysis_json": True,
            "does_not_modify_project_source_files": True,
            "requires_manual_review": True,
            "needs_blender_run": True,
        },
        "reference_files": reference_files,
        "proposed_files": [
            {
                "file": new_file,
                "kind": "standalone_blender_scene_builder",
                "why": "The model returned raw Python; the pipeline wrapped it into the required review JSON.",
            }
        ],
        "implementation_plan": [
            {
                "reference_file": item["file"],
                "new_file": new_file,
                "change": "Use this source as reference style while reviewing the raw generated Blender script.",
                "why": "Preserve project structure while creating a separate candidate script.",
                "risk": "medium",
                "manual_check": "Run only inside Blender on a disposable scene.",
            }
            for item in reference_files[:6]
        ],
        "new_files_allowed": ["indexAI/scene_scripts/...", "indexAI/patch_library/..."],
        "scene_script": script,
        "support_files": [],
        "notes": [reason, "Raw Python was accepted only after wrapping and normal validation."],
        "files_to_review_before_applying": [item["file"] for item in reference_files],
        "expected_panel_or_operator": "Run as standalone Blender Text script on a new/empty scene.",
        "model": model,
    }


def get_indexed_project_files() -> set[str]:
    manifest = read_json(PROJECT_MANIFEST_JSON) if PROJECT_MANIFEST_JSON.exists() else {}
    return {item.get("file") for item in manifest.get("files", []) if item.get("file")}


def validate_implementation_draft(draft: dict[str, Any]) -> dict[str, Any]:
    indexed_files = get_indexed_project_files()
    contract_validation = validate_implementation_draft_contract(
        draft,
        allowed_prefixes=ALLOWED_NEW_PREFIXES,
    )

    issues: list[str] = list(contract_validation.get("required_key_report", {}).get("issues", []))
    reference_files = draft.get("reference_files") or []
    proposed_files = draft.get("proposed_files") or []
    implementation_plan = draft.get("implementation_plan") or []

    if draft.get("implementation_kind") != "new_blender_scene_script_from_json":
        issues.append("implementation_kind should be new_blender_scene_script_from_json.")

    if not isinstance(reference_files, list) or not reference_files:
        issues.append("No reference_files entries were provided.")
    if not isinstance(proposed_files, list) or not proposed_files:
        issues.append("No proposed_files entries were provided.")
    if not isinstance(implementation_plan, list) or not implementation_plan:
        issues.append("No implementation_plan entries were provided.")

    if isinstance(reference_files, list):
        for item in reference_files:
            if not isinstance(item, dict):
                issues.append("A reference_files entry is not an object.")
                continue
            raw_file_name = str(item.get("file") or "").replace("\\", "/").strip()
            if not raw_file_name:
                issues.append("A reference_files entry has no file.")
                continue
            file_name = normalize_repo_relative_path(raw_file_name)
            if file_name not in indexed_files:
                issues.append(f"Reference file is not in project index: {file_name}")

    if isinstance(proposed_files, list):
        for item in proposed_files:
            if not isinstance(item, dict):
                issues.append("A proposed_files entry is not an object.")
                continue
            raw_file_name = str(item.get("file") or "").replace("\\", "/").strip()
            if not raw_file_name:
                issues.append("A proposed_files entry has no file.")
                continue
            file_name = normalize_repo_relative_path(raw_file_name)
            if file_name in indexed_files:
                issues.append(f"Proposed file must not be an existing source file: {file_name}")
            if not is_allowed_generated_artifact_path(file_name, allowed_prefixes=ALLOWED_NEW_PREFIXES):
                issues.append(f"Proposed file is not under an allowed generated-output prefix: {file_name}")

    support_files = draft.get("support_files") or []
    if support_files and not isinstance(support_files, list):
        issues.append("support_files must be a list when provided.")
    if isinstance(support_files, list):
        for item in support_files:
            if not isinstance(item, dict):
                issues.append("A support_files entry is not an object.")
                continue
            raw_file_name = str(item.get("file") or "").replace("\\", "/").strip()
            if not raw_file_name:
                issues.append("A support_files entry has no file.")
                continue
            file_name = normalize_repo_relative_path(raw_file_name)
            if file_name in indexed_files:
                issues.append(f"Support file must not be an existing source file: {file_name}")
            if not is_allowed_generated_artifact_path(file_name, allowed_prefixes=ALLOWED_NEW_PREFIXES):
                issues.append(f"Support file is not under an allowed generated-output prefix: {file_name}")
            if "content" not in item:
                issues.append(f"Support file has no content: {file_name}")

    script = str(draft.get("scene_script") or draft.get("hotpatch_candidate_script") or draft.get("script") or "")
    script_lower = script.lower()
    stripped_script = script.strip()
    if len(stripped_script) < 2500:
        issues.append("scene_script is missing or too short.")
    if "import bpy" not in script:
        issues.append("scene_script does not appear to be a Blender Python script.")
    if "json" not in script_lower or "load_json" not in script:
        issues.append("scene_script must load and use the JSON context files.")
    if 'keyframes.get("frames"' not in script and "keyframes.get('frames'" not in script:
        issues.append("scene_script must use the full Blender keyframes JSON frames.")
    if "keyframe_insert" not in script:
        issues.append("scene_script must create Blender keyframes from the audio context.")
    if "modifiers.new" not in script and ".modifiers" not in script:
        issues.append("scene_script must include at least one mesh/modifier-driven visual system.")
    if "materials.new" not in script and ".data.materials" not in script:
        issues.append("scene_script must create or assign materials.")
    if any(token in script_lower for token in ["placeholder", "todo", "can't assist", "cannot assist"]):
        issues.append("scene_script contains placeholder/refusal text.")
    if "\n    pass" in script or "\n\tpass" in script:
        issues.append("scene_script contains pass blocks instead of implementation.")
    if "analysis_blender_keyframes" in script and "write" in script.lower():
        issues.append("Candidate script appears to write keyframe analysis data; review required.")
    if any(token in script for token in ["apply_patch", "git ", "Remove-Item", "shutil.rmtree"]):
        issues.append("Candidate script contains project/file mutation commands outside Blender scene creation.")

    return {
        "ok": not issues,
        "issues": issues,
        "indexed_file_count": len(indexed_files),
        "allowed_new_prefixes": list(ALLOWED_NEW_PREFIXES),
        "contract_validation": contract_validation,
    }


def generated_scene_script_relpath() -> str:
    return f"indexAI/scene_scripts/{packet_slugify(TRACK_STEM)}_scene_builder_candidate.py"


def generated_scene_script_abspath() -> Path:
    return ROOT / generated_scene_script_relpath()


def deterministic_scene_builder_script(
    track_stem: str,
    analysis_json: str,
    music_context_json: str,
    ai_context_json: str,
    blender_keyframes_json: str,
    asset_inventory_json: str = "",
    scene_brief: dict[str, Any] | None = None,
) -> str:
    brief_text = json.dumps(scene_brief or {}, ensure_ascii=False).lower()
    use_dual_focus = any(token in brief_text for token in ["dualismo", "doppio", "doppi fuoco", "due oggetti", "contrappost"])
    return f'''# Standalone Blender scene builder generated from Spaziotempo JSON context.
# Review-only draft: run inside Blender Text Editor with Alt+P.
from __future__ import annotations

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector


TRACK_STEM = {track_stem!r}
ANALYSIS_JSON = Path({analysis_json!r})
MUSIC_CONTEXT_JSON = Path({music_context_json!r})
AI_CONTEXT_JSON = Path({ai_context_json!r})
BLENDER_KEYFRAMES_JSON = Path({blender_keyframes_json!r})
ASSET_INVENTORY_JSON = Path({asset_inventory_json!r}) if {bool(asset_inventory_json)!r} else None
USE_DUAL_FOCUS = {use_dual_focus!r}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON: {{path}}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {{}}


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def preferred_ball_asset_path(inventory: dict) -> Path | None:
    for asset in inventory.get("assets", []):
        if asset.get("role") == "primary_ball_asset":
            path = Path(asset.get("path") or "")
            if path.exists():
                return path
    return None


def import_asset_file(asset_file: Path) -> list[bpy.types.Object]:
    before = set(bpy.data.objects.keys())
    ext = asset_file.suffix.lower()
    if ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(asset_file))
    elif ext in {{".glb", ".gltf"}}:
        bpy.ops.import_scene.gltf(filepath=str(asset_file))
    elif ext == ".obj":
        try:
            bpy.ops.wm.obj_import(filepath=str(asset_file))
        except Exception:
            bpy.ops.import_scene.obj(filepath=str(asset_file))
    elif ext == ".blend":
        with bpy.data.libraries.load(str(asset_file), link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
        for obj in data_to.objects:
            if obj:
                bpy.context.collection.objects.link(obj)
    else:
        raise RuntimeError(f"Unsupported asset format: {{asset_file}}")
    new_names = set(bpy.data.objects.keys()) - before
    return [bpy.data.objects[name] for name in new_names if name in bpy.data.objects]


def get_world_bbox(objects: list[bpy.types.Object]):
    coords = []
    bpy.context.view_layer.update()
    for obj in objects:
        if obj.type == "EMPTY":
            coords.append(obj.matrix_world.translation.copy())
            continue
        if not hasattr(obj, "bound_box"):
            continue
        try:
            coords.extend([obj.matrix_world @ Vector(corner) for corner in obj.bound_box])
        except Exception:
            coords.append(obj.matrix_world.translation.copy())
    if not coords:
        return Vector((0, 0, 0)), Vector((1, 1, 1)), Vector((0, 0, 0))
    min_v = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
    max_v = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
    return (min_v + max_v) * 0.5, max_v - min_v, min_v


def make_asset_focus(name: str, asset_path: Path, location, material: bpy.types.Material, fallback_radius: float = 1.0) -> bpy.types.Object:
    try:
        objects = import_asset_file(asset_path)
    except Exception as exc:
        print(f"Asset import failed, using procedural sphere: {{asset_path}} / {{exc}}")
        return add_uv_sphere(name, fallback_radius, location, material, segments=96)
    meshes = [obj for obj in objects if obj.type == "MESH"]
    focus = meshes[0] if meshes else objects[0]
    focus.name = name
    for obj in objects:
        if obj != focus:
            matrix = obj.matrix_world.copy()
            obj.parent = focus
            obj.matrix_world = matrix
        if hasattr(obj.data, "materials"):
            obj.data.materials.clear()
            obj.data.materials.append(material)

    center, size, min_v = get_world_bbox(objects)
    max_dim = max(size.x, size.y, size.z, 0.0001)
    target_dim = fallback_radius * 2.0
    focus.scale = (target_dim / max_dim, target_dim / max_dim, target_dim / max_dim)
    bpy.context.view_layer.update()
    center, _size, min_v = get_world_bbox(objects)
    focus.location += Vector(location) - center
    focus.location.z += float(location[2]) - min_v.z
    focus["imported_asset_children"] = len(objects)
    return focus


def make_collection(name: str) -> bpy.types.Collection:
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection


def link_to(collection: bpy.types.Collection, obj: bpy.types.Object) -> None:
    for parent in list(obj.users_collection):
        parent.objects.unlink(obj)
    collection.objects.link(obj)


def create_material(name: str, color, emission_strength: float = 0.0) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = color
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = color
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.42
    return mat


def add_uv_sphere(name: str, radius: float, location, material: bpy.types.Material, segments: int = 64) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=max(16, segments // 2), radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.name = name + "Mesh"
    obj.data.materials.append(material)
    return obj


def add_text_label(text: str, location, size: float, material: bpy.types.Material) -> bpy.types.Object:
    bpy.ops.object.text_add(location=location, rotation=(math.radians(72), 0.0, 0.0))
    obj = bpy.context.object
    obj.name = "AlbumTitle_Text"
    obj.data.body = text
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.025
    obj.data.materials.append(material)
    return obj


def animate_value(obj: bpy.types.Object, data_path: str, frames: list[tuple[int, float]], index: int | None = None) -> None:
    for frame, value in frames:
        if index is None:
            setattr(obj, data_path, value)
            obj.keyframe_insert(data_path=data_path, frame=frame)
        else:
            current = getattr(obj, data_path)
            current[index] = value
            obj.keyframe_insert(data_path=data_path, frame=frame, index=index)


def keyframe_material_emission(mat: bpy.types.Material, frame: int, strength: float) -> None:
    if not mat.use_nodes or not mat.node_tree:
        return
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if not bsdf or "Emission Strength" not in bsdf.inputs:
        return
    socket = bsdf.inputs["Emission Strength"]
    socket.default_value = strength
    socket.keyframe_insert(data_path="default_value", frame=frame)


def apply_full_audio_keyframes(hero: bpy.types.Object, disp: bpy.types.Modifier, hero_mat: bpy.types.Material, keyframes: dict, fps: float) -> int:
    audio_frames = keyframes.get("frames") or []
    inserted = 0
    for audio in audio_frames:
        time_sec = float(audio.get("time") or 0.0)
        frame = int(round(time_sec * fps)) + 1
        low = float(audio.get("low") or 0.0)
        mid = float(audio.get("mid") or 0.0)
        high = float(audio.get("high") or 0.0)
        onset = float(audio.get("onset") or 0.0)
        beat = float(audio.get("beat") or 0.0)

        # Full-frame audio deformation: not only uniform scale, but an asymmetric pulse plus displacement.
        hero.scale = (
            1.0 + low * 0.12 + beat * 0.025,
            1.0 + mid * 0.075 + onset * 0.018,
            1.0 + high * 0.055 + low * 0.035,
        )
        hero.keyframe_insert(data_path="scale", frame=frame)

        disp.strength = 0.035 + low * 0.11 + mid * 0.045 + onset * 0.025 + beat * 0.018
        disp.keyframe_insert(data_path="strength", frame=frame)

        keyframe_material_emission(hero_mat, frame, 0.28 + high * 0.55 + onset * 0.22 + beat * 0.18)
        inserted += 1
    return inserted


def apply_full_audio_keyframes_inverted(hero: bpy.types.Object, disp: bpy.types.Modifier, hero_mat: bpy.types.Material, keyframes: dict, fps: float) -> int:
    audio_frames = keyframes.get("frames") or []
    inserted = 0
    for audio in audio_frames:
        time_sec = float(audio.get("time") or 0.0)
        frame = int(round(time_sec * fps)) + 1
        low = float(audio.get("low") or 0.0)
        mid = float(audio.get("mid") or 0.0)
        high = float(audio.get("high") or 0.0)
        onset = float(audio.get("onset") or 0.0)
        beat = float(audio.get("beat") or 0.0)
        hero.scale = (
            1.0 + high * 0.12 + onset * 0.018,
            1.0 + low * 0.075 + beat * 0.025,
            1.0 + mid * 0.055 + high * 0.035,
        )
        hero.keyframe_insert(data_path="scale", frame=frame)
        disp.strength = 0.035 + high * 0.11 + low * 0.045 + onset * 0.02
        disp.keyframe_insert(data_path="strength", frame=frame)
        keyframe_material_emission(hero_mat, frame, 0.25 + low * 0.45 + mid * 0.20 + beat * 0.22)
        inserted += 1
    return inserted


def build_scene() -> None:
    analysis = load_json(ANALYSIS_JSON)
    music = load_json(MUSIC_CONTEXT_JSON)
    ai_context = load_json(AI_CONTEXT_JSON)
    keyframes = load_json(BLENDER_KEYFRAMES_JSON)
    asset_inventory = load_json(ASSET_INVENTORY_JSON) if ASSET_INVENTORY_JSON else {{}}

    meta = keyframes.get("meta") or analysis.get("meta") or (ai_context.get("analysis_summary") or {{}}).get("meta") or {{}}
    fps = float(meta.get("fps") or 30.0)
    duration = float(meta.get("duration_sec") or 180.0)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = max(1, int(duration * fps))
    scene.render.fps = int(round(fps))

    clear_scene()
    col_core = make_collection("AI Scene Core")
    col_orbits = make_collection("AI Audio Orbits")
    col_fog = make_collection("AI Volumetric Forms")
    col_refs = make_collection("AI JSON References")

    hero_mat = create_material("AI_Hero_Material_MatterEmission", (0.70, 0.86, 0.88, 1.0), 0.45)
    counter_mat = create_material("AI_Hero_CounterMaterial_Ball", (0.95, 0.72, 0.45, 1.0), 0.55)
    accent_mat = create_material("AI_Accent_Emission_Material", (0.95, 0.72, 0.45, 1.0), 1.2)
    cool_mat = create_material("AI_Cool_Background_Material", (0.13, 0.38, 0.44, 1.0), 0.08)
    fog_mat = create_material("AI_Fog_Filament_Material", (0.48, 0.78, 0.84, 0.35), 0.12)
    text_mat = create_material("AI_Title_Material", (0.82, 0.91, 0.88, 1.0), 0.35)

    ball_asset = preferred_ball_asset_path(asset_inventory)
    hero_location = (-0.95, 0, 1.75) if USE_DUAL_FOCUS else (0, 0, 1.75)
    hero = add_uv_sphere("AI_HeroAura_DeformableCore", 1.20 if USE_DUAL_FOCUS else 1.35, hero_location, hero_mat, segments=96)
    link_to(col_core, hero)
    disp = hero.modifiers.new("AI_Audio_Displace_LowMid", "DISPLACE")
    tex = bpy.data.textures.new("AI_Audio_Deformation_Texture", "VORONOI")
    tex.noise_scale = 1.15
    tex.intensity = 0.42
    disp.texture = tex
    disp.strength = 0.08

    counter_hero = None
    counter_disp = None
    if USE_DUAL_FOCUS:
        if ball_asset:
            counter_hero = make_asset_focus("AI_BallAsset_CounterCore", ball_asset, (0.95, 0, 1.75), counter_mat, fallback_radius=1.12)
        else:
            counter_hero = add_uv_sphere("AI_CounterSphere_DeformableCore", 1.12, (0.95, 0, 1.75), counter_mat, segments=96)
        link_to(col_core, counter_hero)
        counter_disp = counter_hero.modifiers.new("AI_Audio_Displace_InvertedBall", "DISPLACE")
        counter_tex = bpy.data.textures.new("AI_Audio_Deformation_Texture_InvertedBall", "VORONOI")
        counter_tex.noise_scale = 1.35
        counter_tex.intensity = 0.38
        counter_disp.texture = counter_tex
        counter_disp.strength = 0.07

    segments = music.get("segments") or []
    sample_segments = segments[::max(1, len(segments) // 16)] or segments[:16]
    for idx, segment in enumerate(sample_segments[:18]):
        controls = segment.get("controls") or {{}}
        angle = idx * (math.tau / max(1, len(sample_segments[:18])))
        band = segment.get("dominant_band") or controls.get("primary_band") or "mid"
        score = float(segment.get("intensity_score") or 0.2)
        radius = 3.4 + score * 1.8
        z = 1.45 + math.sin(angle * 2.0) * 0.55
        mat = accent_mat if band == "high" else cool_mat if band == "mid" else hero_mat
        sat = add_uv_sphere(f"AI_AudioSatellite_{{idx+1:02d}}_{{band}}", 0.12 + score * 0.18, (math.cos(angle) * radius, math.sin(angle) * radius, z), mat, segments=32)
        link_to(col_orbits, sat)
        sat["segment_index"] = int(segment.get("index") or idx + 1)
        sat["audio_band"] = str(band)
        sat["json_start_sec"] = float(segment.get("start_sec") or 0.0)
        start_frame = int(float(segment.get("start_sec") or 0.0) * fps) + 1
        end_frame = int(float(segment.get("end_sec") or 0.0) * fps) + 1
        for frame, rot in [(start_frame, angle), (end_frame, angle + math.tau * (1.0 + score))]:
            sat.rotation_euler[2] = rot
            sat.keyframe_insert(data_path="rotation_euler", frame=frame, index=2)
        scale = 1.0 + float(controls.get("accent_emission") or score) * 0.85
        sat.scale = (scale, scale, scale)
        sat.keyframe_insert(data_path="scale", frame=start_frame)

    # Procedural fog represented as visible soft filaments instead of heavy volume simulation.
    for idx in range(24):
        angle = idx * math.tau / 24
        length = 0.9 + (idx % 5) * 0.24
        bpy.ops.mesh.primitive_cube_add(size=1, location=(math.cos(angle) * 2.6, math.sin(angle) * 2.6, 1.0 + (idx % 6) * 0.22))
        fog = bpy.context.object
        fog.name = f"AI_FogFilament_{{idx+1:02d}}"
        fog.scale = (0.035, length, 0.035)
        fog.rotation_euler[2] = angle
        fog.data.materials.append(fog_mat)
        link_to(col_fog, fog)
        for frame, mul in [(1, 0.65), (scene.frame_end // 2, 1.35), (scene.frame_end, 0.75)]:
            fog.scale = (0.035 * mul, length * mul, 0.035 * mul)
            fog.keyframe_insert(data_path="scale", frame=frame)

    title = add_text_label(TRACK_STEM.replace("_Master", ""), (0, -3.25, 0.72), 0.34, text_mat)
    link_to(col_refs, title)

    inserted_full_keyframes = apply_full_audio_keyframes(hero, disp, hero_mat, keyframes, fps)
    hero["full_audio_keyframes_inserted"] = inserted_full_keyframes
    if counter_hero and counter_disp:
        counter_inserted = apply_full_audio_keyframes_inverted(counter_hero, counter_disp, counter_mat, keyframes, fps)
        counter_hero["full_audio_keyframes_inserted"] = counter_inserted
        counter_hero["source_asset"] = str(ball_asset) if ball_asset else "procedural_fallback"

    bpy.ops.object.light_add(type="AREA", location=(0, -4.8, 4.8), rotation=(math.radians(60), 0, 0))
    key = bpy.context.object
    key.name = "AI_Soft_Key_Light"
    key.data.energy = 450
    key.data.size = 5.5
    link_to(col_core, key)

    bpy.ops.object.camera_add(location=(0, -7.4, 3.2), rotation=(math.radians(65), 0, 0))
    camera = bpy.context.object
    camera.name = "AI_Album_Camera"
    scene.camera = camera
    camera.data.lens = 42

    world = scene.world or bpy.data.worlds.new("AI_World")
    scene.world = world
    world.color = (0.025, 0.095, 0.105)

    scene["ai_generated_from"] = str(MUSIC_CONTEXT_JSON)
    scene["full_keyframes_reference"] = str(BLENDER_KEYFRAMES_JSON)
    scene["note"] = "Standalone AI scene draft. Existing project files were used only as style reference."


if __name__ == "__main__":
    build_scene()
'''


def deterministic_support_files(track_stem: str, scene_brief: dict[str, Any] | None = None) -> list[dict[str, str]]:
    slug = packet_slugify(track_stem)
    bundle_dir = f"indexAI/scene_scripts/{slug}_scene_bundle"
    manifest = {
        "kind": "spaziotempo_generated_scene_bundle_manifest",
        "track_stem": track_stem,
        "main_script": f"indexAI/scene_scripts/{slug}_scene_builder_candidate.py",
        "npu_service_role": [
            "create split/module plan",
            "maintain manifest of generated files",
            "check naming consistency",
            "summarize previous script for next GPU revision",
            "avoid heavy code generation unless explicitly requested",
        ],
        "gpu_writer_role": [
            "generate Blender Python scene logic",
            "apply scene director changes",
            "keep full audio keyframes as the animation source",
        ],
        "generated_files": [
            f"{bundle_dir}/manifest.json",
            f"{bundle_dir}/director_brief_snapshot.json",
            f"{bundle_dir}/README.md",
        ],
    }
    readme = f"""# {track_stem} Scene Bundle

This folder is generated support context for the standalone Blender scene script.

- Main Blender script: `../{slug}_scene_builder_candidate.py`
- Existing project files are reference only.
- Full audio keyframe JSON remains the source for animation.
- NPU can safely maintain this manifest/split plan; GPU/Ollama should handle heavy Blender code generation.
"""
    return [
        {
            "file": f"{bundle_dir}/manifest.json",
            "kind": "manifest",
            "content": json.dumps(manifest, indent=2, ensure_ascii=False),
        },
        {
            "file": f"{bundle_dir}/director_brief_snapshot.json",
            "kind": "brief_snapshot",
            "content": json.dumps(scene_brief or {}, indent=2, ensure_ascii=False),
        },
        {
            "file": f"{bundle_dir}/README.md",
            "kind": "notes",
            "content": readme,
        },
    ]


def build_fallback_implementation_draft(
    reason: str,
    model: str | None = None,
    args: argparse.Namespace | None = None,
    scene_brief: dict[str, Any] | None = None,
    asset_inventory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    indexed_files = get_indexed_project_files()
    selected_files = [path for path in PREFERRED_IMPLEMENTATION_FILES if path in indexed_files]
    new_file = generated_scene_script_relpath()
    scene_script = deterministic_scene_builder_script(
        track_stem=TRACK_STEM,
        analysis_json=str(Path(args.analysis)) if args else "",
        music_context_json=str(Path(args.compact_json)) if args else "",
        ai_context_json=str(Path(args.analysis_ai_context)) if args else "",
        blender_keyframes_json=str(Path(args.blender_keyframes_json)) if args else "",
        asset_inventory_json=str(Path(args.asset_inventory)) if args and getattr(args, "asset_inventory", None) else "",
        scene_brief=scene_brief,
    )

    reference_files = [
        {
            "file": path,
            "exists_in_project_index": True,
            "reason": "Style/source reference only; not modified by this generated scene script.",
        }
        for path in selected_files
    ]

    implementation_plan = [
        {
            "reference_file": path,
            "new_file": new_file,
            "change": "Use this file as structure/style reference for the standalone scene builder.",
            "why": "The generated product is a new Blender scene script, not a patch to the existing project.",
            "risk": "medium",
            "manual_check": "Open the generated script in Blender Text Editor and run on an empty scene.",
        }
        for path in selected_files
    ]

    draft: dict[str, Any] = {
        "implementation_kind": "new_blender_scene_script_from_json",
        "safety": {
            "does_not_modify_full_analysis_json": True,
            "does_not_modify_project_source_files": True,
            "requires_manual_review": True,
            "needs_blender_run": True,
        },
        "reference_files": reference_files,
        "proposed_files": [
            {
                "file": new_file,
                "kind": "standalone_blender_scene_builder",
                "why": "Creates a new scene from JSON context while preserving the original project as reference only.",
            }
        ],
        "implementation_plan": implementation_plan,
        "new_files_allowed": [
            "indexAI/scene_scripts/...",
            "indexAI/patch_library/...",
        ],
        "scene_script": scene_script,
        "support_files": deterministic_support_files(TRACK_STEM, scene_brief),
        "notes": [
            f"Deterministic fallback generated because implementation draft was invalid: {reason}",
            "This is a standalone scene builder; it does not patch the existing project files.",
            "NPU service work is represented as manifest/split-plan support files.",
        ],
        "files_to_review_before_applying": [item["file"] for item in reference_files],
        "expected_panel_or_operator": "Run as standalone Blender Text script on a new/empty scene.",
    }

    if model:
        draft["model"] = model
    if asset_inventory:
        draft["asset_inventory_used"] = {
            "asset_count": asset_inventory.get("asset_count"),
            "primary_assets": [
                asset for asset in asset_inventory.get("assets", [])
                if asset.get("role") in {"primary_ball_asset", "animated_effect_asset", "blend_scene_reference"}
            ][:10],
        }

    return draft


def normalize_implementation_draft(
    draft: dict[str, Any],
    model: str | None = None,
    args: argparse.Namespace | None = None,
    scene_brief: dict[str, Any] | None = None,
    asset_inventory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(draft, dict):
        return build_fallback_implementation_draft("draft is not a dictionary", model=model, args=args, scene_brief=scene_brief, asset_inventory=asset_inventory)

    validation = validate_implementation_draft(draft)
    if validation.get("ok"):
        return draft

    reason = "; ".join(validation.get("issues", [])) or "unknown validation failure"
    fallback = build_fallback_implementation_draft(reason, model=model, args=args, scene_brief=scene_brief, asset_inventory=asset_inventory)
    fallback["raw_invalid_draft"] = draft
    fallback["original_validation"] = validation
    return fallback


def generate_implementation_draft_with_retry(
    manager: OllamaModelManager,
    model_name: str,
    implementation_prompt: str,
    plan: dict[str, Any],
    max_new_tokens: int,
    args: argparse.Namespace | None = None,
    scene_brief: dict[str, Any] | None = None,
    asset_inventory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    implementation_text, implementation_model = manager.generate(
        model_name,
        implementation_prompt,
        max_new_tokens=max(max_new_tokens, 6000),
        temperature=0.01,
    )

    draft = safe_parse_json(implementation_text, "raw_implementation_response")
    draft["model"] = implementation_model
    if draft.get("parse_error"):
        raw_python = draft_from_raw_python_script(
            implementation_text,
            implementation_model,
            "Model returned raw Python instead of JSON on first implementation pass.",
        )
        if raw_python and validate_implementation_draft(raw_python).get("ok"):
            return raw_python

    validation = validate_implementation_draft(draft)
    if validation.get("ok"):
        return draft

    retry_prompt = build_implementation_retry_prompt(
        plan=plan,
        invalid_draft=draft,
        validation=validation,
    )

    retry_text, retry_model = manager.generate(
        model_name,
        retry_prompt,
        max_new_tokens=max(max_new_tokens, 7000),
        temperature=0.01,
    )

    retry_draft = safe_parse_json(retry_text, "raw_implementation_retry_response")
    retry_draft["model"] = retry_model
    if retry_draft.get("parse_error"):
        raw_python = draft_from_raw_python_script(
            retry_text,
            retry_model,
            "Model returned raw Python instead of JSON on retry pass.",
        )
        if raw_python and validate_implementation_draft(raw_python).get("ok"):
            raw_python["retry_of_invalid_draft"] = draft
            raw_python["first_validation"] = validation
            return raw_python
    retry_draft["retry_of_invalid_draft"] = draft
    retry_draft["first_validation"] = validation

    return normalize_implementation_draft(retry_draft, model=retry_model, args=args, scene_brief=scene_brief, asset_inventory=asset_inventory)


def write_brief(plan: dict[str, Any], creative: dict[str, Any], technical: dict[str, Any], npu_notes: str) -> None:
    lines = [
        "# Dual AI Blender Agent Brief\n\n",
        f"Generated: `{datetime.now().isoformat(timespec='seconds')}`\n\n",
        "## Policy\n",
        "- Full Blender keyframe JSON remains untouched.\n",
        "- AI compact context is analysis only.\n",
        "- Ollama model switch unloads the previous model before loading the next.\n\n",
        "## Recommended Plan\n",
        json.dumps(plan.get("recommended_scene_plan", plan), indent=2, ensure_ascii=False),
        "\n\n## Audio Mapping\n",
        json.dumps(plan.get("audio_mapping_plan", {}), indent=2, ensure_ascii=False),
        "\n\n## Creative Source\n",
        json.dumps(creative, indent=2, ensure_ascii=False)[:12000],
        "\n\n## Technical Source\n",
        json.dumps(technical, indent=2, ensure_ascii=False)[:12000],
        "\n\n## NPU Notes\n",
        npu_notes[:12000],
        "\n",
    ]
    DUAL_BRIEF_MD.write_text("".join(lines), encoding="utf-8")


def write_implementation_draft(draft: dict[str, Any]) -> None:
    draft["validation"] = validate_implementation_draft(draft)
    write_json(IMPLEMENTATION_DRAFT_JSON, draft)

    script = draft.get("scene_script", draft.get("hotpatch_candidate_script", draft.get("script", "")))
    if not script:
        script = (
            "# AI implementation draft did not contain a scene script.\n"
            "# Review the JSON draft for reference_files, proposed_files, validation and notes.\n"
        )
    IMPLEMENTATION_SCRIPT.write_text(str(script).rstrip() + "\n", encoding="utf-8")
    scene_path = generated_scene_script_abspath()
    scene_path.parent.mkdir(parents=True, exist_ok=True)
    scene_path.write_text(str(script).rstrip() + "\n", encoding="utf-8")

    planned_support_writes: list[PlannedArtifactWrite] = []
    for item in draft.get("support_files", []) or []:
        if not isinstance(item, dict):
            continue
        raw_relpath = str(item.get("file") or "").replace("\\", "/").strip()
        if not raw_relpath:
            continue
        relpath = normalize_repo_relative_path(raw_relpath)
        if not is_allowed_generated_artifact_path(relpath, allowed_prefixes=ALLOWED_NEW_PREFIXES):
            continue
        planned_support_writes.append(
            PlannedArtifactWrite(
                repo_relative_path=relpath,
                kind=str(item.get("kind") or "support_file"),
                content=str(item.get("content", "")).rstrip() + "\n",
            )
        )

    written_support_files: list[str] = []
    for planned_write in planned_support_writes:
        support_path = write_planned_artifact(
            ROOT,
            planned_write,
            allowed_prefixes=ALLOWED_NEW_PREFIXES,
        )
        written_support_files.append(str(support_path))
    if written_support_files:
        draft["written_support_files"] = written_support_files
        write_json(IMPLEMENTATION_DRAFT_JSON, draft)

    notes = [
        "# Generated Implementation Notes\n\n",
        "This file is an AI draft. Review before loading in Blender.\n\n",
        "## Validation\n",
        json.dumps(draft.get("validation", {}), indent=2, ensure_ascii=False),
        "\n\n",
        "## Safety\n",
        json.dumps(draft.get("safety", {}), indent=2, ensure_ascii=False),
        "\n\n## Notes\n",
    ]
    for note in draft.get("notes", []):
        notes.append(f"- {note}\n")
    notes.append("\n## Files To Review\n")
    for path in draft.get("files_to_review_before_applying", []):
        notes.append(f"- `{path}`\n")
    notes.append("\n## Generated Scene Script\n")
    notes.append(f"- `{scene_path}`\n")
    if written_support_files:
        notes.append("\n## Generated Support Files\n")
        for path in written_support_files:
            notes.append(f"- `{path}`\n")
    IMPLEMENTATION_NOTES.write_text("".join(notes), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build code/music contexts, run NPU technical pass and Ollama creative passes.")
    parser.add_argument("--phase", choices=["plan", "implementation", "full"], default="plan")
    parser.add_argument("--track-stem", default=DEFAULT_TRACK_STEM)
    parser.add_argument("--analysis", default=None)
    parser.add_argument("--track-summary", default=None)
    parser.add_argument("--compact-json", default=None)
    parser.add_argument("--analysis-ai-context", default=None)
    parser.add_argument("--blender-keyframes-json", default=None)
    parser.add_argument("--skip-npu", action="store_true")
    parser.add_argument("--skip-ollama", action="store_true")
    parser.add_argument("--include-manual", action="store_true")
    parser.add_argument("--creative-model", default="gpt-oss:20b")
    parser.add_argument("--technical-model", default="qwen2.5-coder:14b")
    parser.add_argument("--ollama-base-url", default=None)
    parser.add_argument("--npu-python", default=str(DEFAULT_NPU_PYTHON))
    parser.add_argument("--npu-model-dir", default=str(DEFAULT_MODEL_DIR))
    parser.add_argument("--npu-chunk-tokens", type=int, default=520)
    parser.add_argument("--npu-reduce-tokens", type=int, default=650)
    parser.add_argument("--npu-final-tokens", type=int, default=900)
    parser.add_argument("--max-new-tokens", type=int, default=1800)
    parser.add_argument("--force-npu", action="store_true", help="Re-run NPU notes even when reusable notes exist.")
    parser.add_argument("--scene-brief", default=None, help="Optional scene director brief JSON created by the workflow shell/GUI.")
    parser.add_argument("--asset-inventory", default=None, help="Optional asset inventory JSON with known local Blender/FBX/GLTF assets.")
    args = parser.parse_args()

    apply_default_input_paths(args)
    update_track_paths(args.track_stem, args.analysis_ai_context)

    if not Path(args.analysis).exists():
        raise FileNotFoundError(f"Analysis JSON missing: {args.analysis}")
    if not Path(args.track_summary).exists():
        raise FileNotFoundError(
            f"Track summary missing: {args.track_summary}\n"
            "Crea prima il track summary o usa la workflow shell che ora lo ripara automaticamente."
        )
    if args.phase == "implementation" and not DUAL_PLAN_JSON.exists():
        raise FileNotFoundError(f"Dual AI scene plan missing, run phase plan first: {DUAL_PLAN_JSON}")

    build_code_context()
    project_manifest = build_project_ai_index()
    build_music_context(
        analysis_path=Path(args.analysis),
        track_summary_path=Path(args.track_summary),
        compact_json_path=Path(args.compact_json),
        analysis_ai_context_path=Path(args.analysis_ai_context),
        blender_keyframes_path=Path(args.blender_keyframes_json),
    )
    if args.include_manual:
        build_manual_context(limit_files=80)
    validate_input_files(args)
    music_context = read_json(MUSIC_AI_CONTEXT)
    scene_brief = read_optional_json(args.scene_brief)
    asset_inventory = read_optional_json(args.asset_inventory)

    npu_notes = ""
    if not args.skip_npu:
        if args.phase == "implementation" and not args.force_npu and NPU_TECH_MD.exists():
            npu_notes = read_text(NPU_TECH_MD)
            print(f"[NPU] Reusing plan technical notes: {NPU_TECH_MD}")
        else:
            report = npu_preflight(args.npu_python, args.npu_model_dir)
            write_npu_preflight_report(report, NPU_PREFLIGHT_JSON)
            if report.get("ready"):
                try:
                    npu_notes = run_npu_technical_pass(args)
                except Exception as exc:
                    npu_notes = f"NPU technical pass unavailable after ready preflight: {exc}"
                    NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")
            else:
                npu_notes = "NPU not ready. Preflight:\n" + json.dumps(report, indent=2, ensure_ascii=False)
                NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")

        if looks_degraded_text(npu_notes):
            npu_notes = deterministic_technical_notes(
                music_context=music_context,
                project_manifest=project_manifest,
                reason="degraded_or_too_short_npu_output",
            )
            NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")
            if args.phase == "implementation":
                NPU_IMPLEMENTATION_NOTES.write_text(npu_notes, encoding="utf-8")
            print("[WARN] NPU notes looked degraded; deterministic technical notes were used.")
    else:
        npu_notes = deterministic_technical_notes(
            music_context=music_context,
            project_manifest=project_manifest,
            reason="npu_skipped_gpu_heavy_mode",
        )
        NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")

    service_packet_info = build_ai_service_packet(
        track_stem=TRACK_STEM,
        analysis_path=Path(args.analysis),
        track_summary_path=Path(args.track_summary),
        music_context_path=Path(args.compact_json),
        analysis_ai_context_path=Path(args.analysis_ai_context),
        blender_keyframes_path=Path(args.blender_keyframes_json),
        dual_plan_path=DUAL_PLAN_JSON if DUAL_PLAN_JSON.exists() else None,
        npu_notes=npu_notes,
        npu_status="skipped_gpu_heavy_mode" if args.skip_npu else "router_capsule_ready",
        scene_brief=scene_brief,
        asset_inventory=asset_inventory,
    )
    gpu_task_packet = service_packet_info["gpu_packet"]

    if args.phase == "implementation":
        if args.skip_ollama:
            draft = build_fallback_implementation_draft(
                reason="Ollama skipped; deterministic standalone scene script generated.",
                model=None,
                args=args,
                scene_brief=scene_brief,
                asset_inventory=asset_inventory,
            )
            write_implementation_draft(draft)
        else:
            plan_output = read_json(DUAL_PLAN_JSON)
            plan = plan_output.get("final_plan", plan_output)
            manager_kwargs = {}
            if args.ollama_base_url:
                manager_kwargs["base_url"] = args.ollama_base_url
            with OllamaModelManager(**manager_kwargs) as manager:
                implementation_prompt = build_implementation_prompt(plan, npu_notes, args.include_manual, gpu_task_packet, scene_brief, asset_inventory)
                draft = generate_implementation_draft_with_retry(
                    manager=manager,
                    model_name=args.technical_model,
                    implementation_prompt=implementation_prompt,
                    plan=plan,
                    max_new_tokens=args.max_new_tokens,
                    args=args,
                    scene_brief=scene_brief,
                    asset_inventory=asset_inventory,
                )
                write_implementation_draft(draft)

        print(f"[OK] Wrote: {IMPLEMENTATION_DRAFT_JSON}")
        print(f"[OK] Wrote: {IMPLEMENTATION_SCRIPT}")
        print(f"[OK] Wrote: {IMPLEMENTATION_NOTES}")
        return

    if args.skip_ollama:
        creative = {"skipped": True}
        technical = {"skipped": True}
        plan = {
            "pipeline_policy": {
                "use_full_blender_keyframes_json": True,
                "ai_context_is_analysis_only": True,
                "ollama_model_switch_policy": "unload previous model before loading next",
            },
            "recommended_scene_plan": {
                "summary": "Ollama skipped; use NPU notes only.",
                "priority_changes": [],
                "defer_changes": [],
            },
        }
    else:
        manager_kwargs = {}
        if args.ollama_base_url:
            manager_kwargs["base_url"] = args.ollama_base_url

        with OllamaModelManager(**manager_kwargs) as manager:
            creative_prompt = build_creative_scene_prompt(music_context, npu_notes, read_text(PROJECT_INDEX_MD))
            creative_text, creative_model = manager.generate(
                args.creative_model,
                creative_prompt,
                max_new_tokens=args.max_new_tokens,
                temperature=0.20,
            )
            creative = safe_parse_json(creative_text, "raw_creative_response")
            creative["model"] = creative_model

            technical_prompt = build_music_prompt(music_context)
            technical_text, technical_model = manager.generate(
                args.technical_model,
                technical_prompt,
                max_new_tokens=args.max_new_tokens,
                temperature=0.10,
            )
            technical = safe_parse_json(technical_text, "raw_technical_response")
            technical["model"] = technical_model

            merge_prompt = build_merge_prompt(music_context, npu_notes, creative, technical)
            merge_text, merge_model = manager.generate(
                args.technical_model,
                merge_prompt,
                max_new_tokens=args.max_new_tokens,
                temperature=0.08,
            )
            plan = safe_parse_json(merge_text, "raw_plan_response")
            plan["merge_model"] = merge_model

            if args.phase == "full":
                implementation_prompt = build_implementation_prompt(plan, npu_notes, args.include_manual, gpu_task_packet, scene_brief, asset_inventory)
                draft = generate_implementation_draft_with_retry(
                    manager=manager,
                    model_name=args.technical_model,
                    implementation_prompt=implementation_prompt,
                    plan=plan,
                    max_new_tokens=args.max_new_tokens,
                    args=args,
                    scene_brief=scene_brief,
                    asset_inventory=asset_inventory,
                )
                write_implementation_draft(draft)

    output = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "track_stem": TRACK_STEM,
        "policy": {
            "full_blender_keyframes_json": str(Path(args.blender_keyframes_json)),
            "ai_context_json": str(MUSIC_AI_CONTEXT),
            "model_switch_rule": "Unload/stop previous Ollama model before loading the next model.",
            "phase": args.phase,
            "manual_context_used": args.include_manual,
            "scene_brief_json": str(Path(args.scene_brief)) if args.scene_brief else None,
            "asset_inventory_json": str(Path(args.asset_inventory)) if args.asset_inventory else None,
            "implementation_draft_json": str(IMPLEMENTATION_DRAFT_JSON) if args.phase in {"implementation", "full"} else None,
            "implementation_script": str(IMPLEMENTATION_SCRIPT) if args.phase in {"implementation", "full"} else None,
        },
        "npu_preflight_json": str(NPU_PREFLIGHT_JSON),
        "npu_technical_notes_md": str(NPU_TECH_MD),
        "ai_service_packet": {
            "capsule_json": service_packet_info.get("capsule_json"),
            "gpu_packet_json": service_packet_info.get("gpu_packet_json"),
            "output_gpu_packet_json": service_packet_info.get("output_gpu_packet_json"),
            "capsule_md": service_packet_info.get("capsule_md"),
        },
        "creative_ollama": creative,
        "technical_ollama": technical,
        "final_plan": plan,
    }

    write_json(DUAL_PLAN_JSON, output)
    write_json(OLLAMA_INSIGHTS_JSON, technical)
    OLLAMA_INSIGHTS_MD.write_text(
        markdown_from_insights(technical, technical.get("model", args.technical_model)),
        encoding="utf-8",
    )
    write_brief(plan, creative, technical, npu_notes)

    print(f"[OK] Wrote: {DUAL_PLAN_JSON}")
    print(f"[OK] Wrote: {DUAL_BRIEF_MD}")
    print(f"[OK] Wrote: {NPU_TECH_MD}")
    if args.phase in {"implementation", "full"} and not args.skip_ollama:
        print(f"[OK] Wrote: {IMPLEMENTATION_DRAFT_JSON}")
        print(f"[OK] Wrote: {IMPLEMENTATION_SCRIPT}")
        print(f"[OK] Wrote: {IMPLEMENTATION_NOTES}")


if __name__ == "__main__":
    main()
