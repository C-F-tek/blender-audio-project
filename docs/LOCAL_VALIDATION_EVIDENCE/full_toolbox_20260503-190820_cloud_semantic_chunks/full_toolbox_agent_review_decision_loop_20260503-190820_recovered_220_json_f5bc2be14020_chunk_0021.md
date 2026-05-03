# Evidence Chunk 0021/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `2992`
- line_end: `3140`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0020.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0022.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Verificare e correg

## Context before

            },
            {
              "id": "consistency_268",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:763` targeting `run_patch_bundle.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:763`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",

## Chunk content

```json
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_269",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:769` targeting `run_patch_bundle.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md:769`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` and resolve `run_patch_bundle.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_270",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md:51` targeting `text\nkind: gpu_repair_failure_recommendation\nrecommendation_count: 1\nrecommendations[0].id: gpu_repair_failure_001\nrecommendations[0].status: ready_for_manual_review\nrecommended_next_layer: build_agent_review_patch_plan.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md:51`. Target `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md` and resolve `text\nkind: gpu_repair_failure_recommendation\nrecommendation_count: 1\nrecommendations[0].id: gpu_repair_failure_001\nrecommendations[0].status: ready_for_manual_review\nrecommended_next_layer: build_agent_review_patch_plan.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_271",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:161` targeting `--output ./output/validation/docs_links_pr108.json\n\npython ./Tools/validation/check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:161`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `--output ./output/validation/docs_links_pr108.json\n\npython ./Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_272",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:164` targeting `check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:164`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_273",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:366` targeting `--markdown-output ./output/validation/docs_contract_drift.md\n\npython ./Tools/validation/check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:366`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `--markdown-output ./output/validation/docs_contract_drift.md\n\npython ./Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_274",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:369` targeting `check_markdown_command_hygiene.py`.",
```

## Context after

              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:369`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
