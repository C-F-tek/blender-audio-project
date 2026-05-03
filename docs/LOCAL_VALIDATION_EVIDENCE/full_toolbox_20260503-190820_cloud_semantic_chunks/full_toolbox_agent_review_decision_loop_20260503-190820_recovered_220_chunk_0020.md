# Evidence Chunk 0020/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `2178`
- line_end: `2309`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0019.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0021.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Generare un piano di patch mirato per correggere riferimenti mancanti a script PowerShell nei documenti di patch bundle.  
**Segnali principali**: alto `md_mentions_missing_powershell_path` in 8 file (AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md, AUTO_PUSH_GENERATED_ARTIF

## Context before

- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md:1519` targeting `run_agent.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md:1519`. Target `docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md` and resolve `run_agent.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_015 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.


## Chunk content

````md
### consistency_016 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_017 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_018 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:83` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:83`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_019 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:775` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:775`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_020 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:362` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:362`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_021 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:363` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:363`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_022 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:370` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:370`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_023 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:371` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:371`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_024 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:378` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:378`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_025 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:379` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:379`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_026 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:386` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:386`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_027 — md_powershell
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:387` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loo
```

### `output/ai_pipeline/full_toolbox_20260503-190820_agent_review_decision_loop_recovered_220.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1138`
- SHA-256: `a65f9f3ca65459ca80640d0c6c4215f867fab4d2b0de21f44e881997134c155c`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Decision Loop

- Passed: `True`
- Recommendation count: `220`
- Patch plan count: `220`
- Deterministic synthesizer used: `True`
- Patch plan fallback used: `False`
- Provider execution performed: `False`
- Patch application performed: `False`

## Outputs

- `recommendations`: `output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json` exists=`True` size=`1563444`
- `recommendations_markdown`: `output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.md` exists=`True` size=`213245`
- `bridge_orchestrator`: `output/ai_pipeline/full_toolbox_20260503-190820_bridge_orchestrator_recovered_220.json` exists=`True` size=`37585`
- `patch_plan`: `output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.json` exists=`True` size=`3342261`
- `patch_plan_markdown`: `output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md` exists=`True` size=`191577`

## Guardrails

Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.

```

````

## Context after

### `output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `191577`
- SHA-256: `4cbc2e3fa6818435a83e28d32b687c5720cd437b23ae1c92a7b5dafa81df3b71`
- Content included: `True`
- Content truncated: `True`

```text
# Agent Review Patch Plan
