# Evidence Chunk 0011/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `1256`
- line_end: `1359`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0010.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0012.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Verificare e correggere riferimenti a percorsi Python mancanti nei file Markdown di documentazione tecnica.  
**Segnali principali**: alto valore di `md_mentions_missing_python_path` in vari file Markdown (es. README.md, agent_review_patch_plan_summary, code_refactor_ai_to_ai_bundle, complex

## Context before

- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:247`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_284 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/README.md:164` targeting `text
Tools/ai/analyze_evidence_bundle_retention.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/README.md:164`. Target `docs/LOCAL_VALIDATION_EVIDENCE/README.md` and resolve `text
Tools/ai/analyze_evidence_bundle_retention.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Chunk content

```md
#### consistency_285 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/README.md:165` targeting `Tools/ai/analyze_evidence_bundle_retention.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/README.md:165`. Target `docs/LOCAL_VALIDATION_EVIDENCE/README.md` and resolve `Tools/ai/analyze_evidence_bundle_retention.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_286 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/agent_review_patch_plan_summary_20260501-230858.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/agent_review_patch_plan_summary_20260501-230858.md:21` targeting `Scripting/shared/config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/agent_review_patch_plan_summary_20260501-230858.md:21`. Target `docs/LOCAL_VALIDATION_EVIDENCE/agent_review_patch_plan_summary_20260501-230858.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_287 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md:275` targeting `text
Scripting/v61b/*.py
Scripting/v61b/**/*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md:275`. Target `docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md` and resolve `text
Scripting/v61b/*.py
Scripting/v61b/**/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_288 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md:918` targeting `text
Scripting/v61b/*.py
Scripting/v61b/**/*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md:918`. Target `docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md` and resolve `text
Scripting/v61b/*.py
Scripting/v61b/**/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_289 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md:1255` targeting `Tools/validation/example.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md:1255`. Target `docs/LOCAL_VALIDATION_EVIDENCE/code_refactor_ai_to_ai_bundle_20260502-215518.md` and resolve `Tools/validation/example.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_290 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `Tools/init_db.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `Tools/init_db.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_291 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `app.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `app.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_292 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `python Tools/init_db.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `python Tools/init_db.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_293 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496` targeting `python app.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md:2496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` and resolve `python app.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_294 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_builder_patch_smoke_20260501-232451.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_builder_patch_smoke_20260501-232451.md:97` targeting `Scripting/shared/config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_builder_patch_smoke_20260501-232451.md:97`. Target `docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_builder_patch_smoke_20260501-232451.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_295 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_master_final_smoke_20260501-232755.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_master_final_smoke_20260501-232755.md:75` targeting `Scripting/shared/config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_master_final_smoke_20260501-232755.md:75`. Target `docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_master_final_smoke_20260501-232755.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_296 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-151613.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-151613.md:231` targeting `Scripting/shared/config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-151613.md:231`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-151613.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

```

## Context after

#### consistency_297 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-151613.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-151613.md:496` targeting `text
Scripting/v61b/*.py
Scripting/v61b/**/*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-151613.md:496`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-151613.md` and resolve `text
Scripting/v61b/*.py
Scripting/v61b/**/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

