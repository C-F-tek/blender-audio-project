# Evidence Chunk 0008/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `848`
- line_end: `993`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0007.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0009.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Correggere riferimenti mancanti a percorsi Python in documentazione markdown per mantenere coerenza del repository.  
**Segnali principali**: `md_mentions_missing_python_path` elevato in 10 file markdown (es. `chunk_064_Scripting_v61b_README_md.md`, `chunk_080_Scripting_v61b_spaziotempo_core_registry_py.md`, ecc.).  
**Guardrail

## Context before

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


## Chunk content

```md
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
- Target files: ['Tools/npu/npu_code_chunks/chunk_080_Scripting_v61b_spaziotempo_core_registry_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_080_Scripting_v61b_spaziotempo_core_registry_py.md:230` targeting `spaziotempo/features/water.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_080_Scripting_v61b_spaziotempo_core_registry_py.md:230`. Target `Tools/npu/npu_code_chunks/chunk_080_Scripting_v61b_spaziotempo_core_registry_py.md` and resolve `spaziotempo/features/water.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_091 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_085_Tools_npu_build_ai_service_packet_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_085_Tools_npu_build_ai_service_packet_py.md:76` targeting `_scene_builder_candidate.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_085_Tools_npu_build_ai_service_packet_py.md:76`. Target `Tools/npu/npu_code_chunks/chunk_085_Tools_npu_build_ai_service_packet_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_092 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/npu/npu_code_chunks/chunk_102_Tools_npu_npu_guardrail_service_py.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_102_Tools_npu_npu_guardrail_service_py.md:19` targeting `args.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_102_Tools_npu_npu_guardrail_service_py.md:19`. Target `Tools/npu/npu_code_chunks/chunk_102_Tools_npu_npu_guardrail_service_py.md` and resolve `args.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_093 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/repo_patch_runner/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/repo_patch_runner/README.md:34` targeting `Scripting/example.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/repo_patch_runner/README.md:34`. Target `Tools/repo_patch_runner/README.md` and resolve `Scripting/example.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_094 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/README.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/validation/README.md:172` targeting `un_npu_review.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/validation/README.md:172`. Target `Tools/validation/README.md` and resolve `un_npu_review.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_251 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AGENT_REVIEW_CODE_PATCH_PLAN.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/AGENT_REVIEW_CODE_PATCH_PLAN.md:117` targeting `Tools/validation/example.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/AGENT_REVIEW_CODE_PATCH_PLAN.md:117`. Target `docs/AGENT_REVIEW_CODE_PATCH_PLAN.md` and resolve `Tools/validation/example.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_252 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_ONBOARDING.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/AI_ONBOARDING.md:44` targeting `Scripting/shared/config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/AI_ONBOARDING.md:44`. Target `docs/AI_ONBOARDING.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_253 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_ONBOARDING.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/AI_ONBOARDING.md:142` targeting `Scripting/shared/config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/AI_ONBOARDING.md:142`. Target `docs/AI_ONBOARDING.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_254 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_ONBOARDING.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/AI_ONBOARDING.md:186` targeting `Scripting/shared/config_model.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/AI_ONBOARDING.md:186`. Target `docs/AI_ONBOARDING.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_255 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/CODE_CONSULTATION_REPORT.md:261` targeting `text
Tools/validation/check_python_syntax.py
Tools/validation/check_package_structure.py
Tools/validation/check_docs_paths.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/CODE_CONSULTATION_REPORT.md:261`. Target `docs/CODE_CONSULTATION_REPORT.md` and resolve `text
Tools/validation/check_python_syntax.py
Tools/validation/check_package_structure.py
Tools/validation/check_docs_paths.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_256 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/CODE_CONSULTATION_REPORT.md:264` targeting `Tools/validation/check_docs_paths.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/CODE_CONSULTATION_REPORT.md:264`. Target `docs/CODE_CONSULTATION_REPORT.md` and resolve `Tools/validation/check_docs_paths.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_257 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/DEVELOPER_GUIDE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/DEVELOPER_GUIDE.md:152` targeting `text
Tools/npu/pipeline/
  config.py
  context_builder.py
  prompts.py
  providers.py
  validators.py
  artifact_writer.py
  runner.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/DEVELOPER_GUIDE.md:152`. Target `docs/DEVELOPER_GUIDE.md` and resolve `text
Tools/npu/pipeline/
  config.py
  context_builder.py
  prompts.py
  providers.py
  validators.py
  artifact_writer.py
  runner.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_258 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:42` targeting `text
Tools/workflow/smart_ai_context.py
Tools/npu/npu_guardrail_service.py
AI pipeline smart context stage
NPU guardrail lane
schema-v6 pipeline report
run_pipeline_dry_run_matrix.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:42`. Target `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md` and resolve `text
Tools/workflow/smart_ai_context.py
Tools/npu/npu_guardrail_service.py
AI pipeline smart context stage
NPU guardrail lane
schema-v6 pipeline report
run_pipeline_dry_run_matrix.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

```

## Context after

#### consistency_259 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:138` targeting `Tools/ai_core/json_utils.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:138`. Target `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md` and resolve `Tools/ai_core/json_utils.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_260 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
