# Evidence Chunk 0018/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `1956`
- line_end: `2073`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0017.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0019.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Correggere riferimenti mancanti a file Python indicati dal mapper di consistenza (`md_mentions_missing_python_path`) nel documento di validazione locale.  
**Segnali principali**: 7 occorrenze (2190‑2195) puntano a file `.cpython-313.py` (scene_tuning_panel, scene_utils, world_setup, __init__).  
**Guardrail/errore**: Nessuna modifica di formattazione; è richiesto aggiornare il link o ripristinare il file target se ancora necessario.  
**Perché serve a una AI cloud**: Garantisce che la documentazione sia coerente con il codice, evitando errori di

## Context before

- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2188` targeting `render_setup.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2188`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `render_setup.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_369 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2189` targeting `scene_tuning_panel.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2189`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `scene_tuning_panel.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Chunk content

````md
#### consistency_370 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2190` targeting `scene_tuning_panel.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2190`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `scene_tuning_panel.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_371 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2191` targeting `scene_utils.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2191`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `scene_utils.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_372 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2192` targeting `scene_utils.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2192`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `scene_utils.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_373 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2193` targeting `world_setup.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2193`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `world_setup.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_374 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2194` targeting `world_setup.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2194`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `world_setup.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_375 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2195` targeting `__init__.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2195`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `__init__.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_376 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2196` targeting `__init__.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2196`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `__init__.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_377 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2197` targeting `accent_patch.cpython-313.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:2197`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `accent_patch.cpython-313.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Artifact manifest

- `output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.json` exists=`True` size=`46914` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.json` exists=`True` size=`241760` suffix=`.json` preview_chars=`1500`
- `output/analysis/repository_consistency_map_full_toolbox_20260503-190820.json` exists=`True` size=`2969389` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_20260503-190820.json` exists=`True` size=`1200` suffix=`.json` preview_chars=`1161`
- `output/analysis/gpu_npu_run_sync_full_toolbox_20260503-190820.json` exists=`True` size=`5624` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json` exists=`True` size=`1563444` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260503-190820_bridge_orchestrator_recovered_220.json` exists=`True` size=`37585` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_20260503-190820_agent_review_decision_loop_recovered_220.json` exists=`True` size=`2734` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.json` exists=`True` size=`3342261` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `213245`
- SHA-256: `224474a615b5dde74727028341451ed70c6e7a6891a136d9940a1bf6e6765fdd`
- Content included: `True`
- Content truncated: `True`

```text
# Deterministic Recommendation Synthesizer

- Passed: `True`
- Recommendation count: `220`
- Deterministic synthesizer used: `True`
- GPU empty recommendations reason: `json_parse_failure`
- Evidence ready for manual patch count: `12`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Recommendations

### consistency_001 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_002 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:368`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

````

## Context after

### consistency_003 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_004 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
