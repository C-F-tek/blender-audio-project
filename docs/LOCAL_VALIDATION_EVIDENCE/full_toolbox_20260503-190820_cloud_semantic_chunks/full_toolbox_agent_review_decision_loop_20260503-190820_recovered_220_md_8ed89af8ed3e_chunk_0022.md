# Evidence Chunk 0022/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `2426`
- line_end: `2523`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0021.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0023.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Correggere riferimenti a script PowerShell e Python mancanti nei documenti di validazione e patching, garantendo coerenza del repository.  
**Segnali principali**: `md_python_command_script_missing` (run_agent.py) e `md_mentions_missing_powershell_path` (varie .ps1) con rischio medio.  
**Guardrail/errore**: Evitare modifiche solo di formattazione; aggiornare il percorso dello script o rimuovere il comando obsoleto.  
**Perché serve a una AI cloud**: Assicura che le istruzioni di esecuzione siano valide e accessibili, permettendo all’AI di orchestrare correttamente i task di patch

## Context before

- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md:267` targeting `run_agent.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md:267`. Target `docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md` and resolve `run_agent.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_012 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md:272` targeting `run_agent.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md:272`. Target `docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md` and resolve `run_agent.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.


## Chunk content

```md
### consistency_013 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md:1514` targeting `run_agent.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md:1514`. Target `docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md` and resolve `run_agent.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_014 — md_python
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md:1519` targeting `run_agent.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md:1519`. Target `docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md` and resolve `run_agent.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_015 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_016 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_017 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_018 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:83` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:83`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_019 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:775` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:775`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_020 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:362` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:362`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_021 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:363` targeting `some_script.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:363`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_022 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:370` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:370`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_023 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:371` targeting `some_runner.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:371`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_024 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:378` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:378`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_025 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:379` targeting `your_app_regenerate_indexes.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:379`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_026 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:386` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:386`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

```

## Context after

### consistency_027 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:387` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md:387`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

### consistency_028 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md']`
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loo
