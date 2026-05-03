# Evidence Chunk 0009/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `994`
- line_end: `1125`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0008.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0010.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Correggere riferimenti mancanti a file Python nei documenti Markdown, garantendo coerenza tra documentazione e codice.  
**Segnali principali

## Context before

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


## Chunk content

```md
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
- Target files: ['docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:201` targeting `text
Tools/workflow/run_local_validation_after_refactor.ps1
Tools/validation/*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:201`. Target `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md` and resolve `text
Tools/workflow/run_local_validation_after_refactor.ps1
Tools/validation/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_261 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:53` targeting `text
Tools/validation/check_generated_<target>_script_policy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:53`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `text
Tools/validation/check_generated_<target>_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_262 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:54` targeting `_script_policy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:54`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_263 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:59` targeting `text
Tools/validation/check_generated_automation_script_policy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:59`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `text
Tools/validation/check_generated_automation_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_264 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:60` targeting `Tools/validation/check_generated_automation_script_policy.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:60`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `Tools/validation/check_generated_automation_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_265 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md:140` targeting `text
Scripting/v61b/*.py
Scripting/v61b/**/*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md:140`. Target `docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md` and resolve `text
Scripting/v61b/*.py
Scripting/v61b/**/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_266 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md:70` targeting `powershell
Select-String -Path ./Tools/ai/*.py, ./Tools/validation/*.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md:70`. Target `docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md` and resolve `powershell
Select-String -Path ./Tools/ai/*.py, ./Tools/validation/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_267 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:82` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:82`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_268 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:763` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:763`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_269 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:769` targeting `run_patch_bundle.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:769`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_270 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md:51` targeting `text
kind: gpu_repair_failure_recommendation
recommendation_count: 1
recommendations[0].id: gpu_repair_failure_001
recommendations[0].status: ready_for_manual_review
recommended_next_layer: build_agent_review_patch_plan.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md:51`. Target `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md` and resolve `text
kind: gpu_repair_failure_recommendation
recommendation_count: 1
recommendations[0].id: gpu_repair_failure_001
recommendations[0].status: ready_for_manual_review
recommended_next_layer: build_agent_review_patch_plan.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_271 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:161` targeting `--output ./output/validation/docs_links_pr108.json

python ./Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:161`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `--output ./output/validation/docs_links_pr108.json

python ./Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

```

## Context after

#### consistency_272 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:164` targeting `check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:164`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_273 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
