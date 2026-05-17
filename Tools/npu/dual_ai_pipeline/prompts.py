from __future__ import annotations

from .common import *  # noqa: F403

def build_creative_scene_prompt(
    music_context: dict[str, Any], npu_notes: str, project_index: str
) -> str:
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
    manual_index_path = TOOLS_DIR / "npu_blender_manual_index.md"
    manual_index = (
        read_text(manual_index_path)[:12000]
        if include_manual and manual_index_path.exists()
        else ""
    )
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
        item.get("file") for item in manifest.get("files", []) if item.get("file")
    )
    preferred_files = [
        file_name for file_name in indexed_files if file_name in PREFERRED_IMPLEMENTATION_FILES
    ]

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
