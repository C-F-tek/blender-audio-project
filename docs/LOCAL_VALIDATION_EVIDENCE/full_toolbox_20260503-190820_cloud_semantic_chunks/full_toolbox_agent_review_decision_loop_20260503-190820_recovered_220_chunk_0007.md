# Evidence Chunk 0007/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `736`
- line_end: `847`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0006.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0008.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Correggere riferimenti a percorsi Python mancanti nei file Markdown di documentazione tecnica.  
**Segnali principali**: Mapper di consistenza segnala `md_mentions_missing_python_path` in 8 file (chunk_192, chunk_001, chunk_002, chunk_013).  
**Guardrail / errori**: Rischio medio; intervento manuale richiesto, evitare modifiche solo di formattazione.  
**Azioni consigliate**: Creare patch mirate per correggere o ripristinare i riferimenti a `File.py`, `matplotlib.py`, `_scene_builder_candidate.py`.  
**Perché serve a una AI cloud**: Garantisce coerenza e integrità delle dip

## Context before

- Target files: ['Tools/npu/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/README.md:19` targeting `run_*pipeline*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/README.md:19`. Target `Tools/npu/README.md` and resolve `run_*pipeline*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_074 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:663` targeting `File.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:663`. Target `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md` and resolve `File.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Chunk content

```md
#### consistency_075 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:665` targeting `File.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:665`. Target `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md` and resolve `File.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_076 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:666` targeting `File.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:666`. Target `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md` and resolve `File.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_077 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md:8` targeting `matplotlib.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md:8`. Target `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md` and resolve `matplotlib.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_078 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md:20` targeting `matplotlib.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md:20`. Target `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md` and resolve `matplotlib.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_079 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md:8` targeting `matplotlib.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md:8`. Target `Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md` and resolve `matplotlib.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_080 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:49` targeting `_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:49`. Target `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_081 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:57` targeting `_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:57`. Target `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_082 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:141` targeting `indexAI/scene_scripts/generated_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:141`. Target `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `indexAI/scene_scripts/generated_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_083 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:149` targeting `indexAI/scene_scripts/generated_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:149`. Target `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `indexAI/scene_scripts/generated_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_084 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md:137` targeting `_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md:137`. Target `Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_085 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md:131` targeting `_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md:131`. Target `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_086 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md:154` targeting `_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md:154`. Target `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_087 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md:42` targeting `spaziotempo/features/water.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md:42`. Target `Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md` and resolve `spaziotempo/features/water.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_088 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md:96` targeting `Scripting/shared/panel_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md:96`. Target `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md` and resolve `Scripting/shared/panel_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

```

## Context after

#### consistency_089 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md:97` targeting `Scripting/shared/hotpatch_base.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md:97`. Target `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md` and resolve `Scripting/shared/hotpatch_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_090 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
