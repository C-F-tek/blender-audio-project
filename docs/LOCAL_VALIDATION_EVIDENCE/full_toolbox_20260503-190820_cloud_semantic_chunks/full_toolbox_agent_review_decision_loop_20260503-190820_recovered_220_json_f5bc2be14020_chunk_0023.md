# Evidence Chunk 0023/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `3287`
- line_end: `3438`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0022.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0024.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Correggere i riferimenti mancanti a percorsi Python nei file Markdown (`md_mentions_missing_python_path`) per garantire coerenza documentale.  
**Segnali principali**: 4 casi di alto rischio (medium) in documenti di AI tasks e testing, con evidenza puntuale (es. riga 155, 56, 244).  
**Guardrail / errori**: Non modificare solo spazi, formattazione Markdown o file generati (`output

## Context before

                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_280",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",

## Chunk content

```json
              "target_files": [
                "docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:155` targeting `check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:155`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_281",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/selected-review-workflow-ai-tools-patch-specs.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/selected-review-workflow-ai-tools-patch-specs.md:56` targeting `text\nTools/workflow/*.ps1\nTools/ai/*.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/selected-review-workflow-ai-tools-patch-specs.md:56`. Target `docs/LOCAL_AI_TASKS/selected-review-workflow-ai-tools-patch-specs.md` and resolve `text\nTools/workflow/*.ps1\nTools/ai/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_282",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:244` targeting `--output ./output/validation/docs_links_macro.json\n\npython ./Tools/validation/check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:244`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md` and resolve `--output ./output/validation/docs_links_macro.json\n\npython ./Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_283",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:247` targeting `check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md:247`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_284",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_VALIDATION_EVIDENCE/README.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/README.md:164` targeting `text\nTools/ai/analyze_evidence_bundle_retention.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/README.md:164`. Target `docs/LOCAL_VALIDATION_EVIDENCE/README.md` and resolve `text\nTools/ai/analyze_evidence_bundle_retention.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_285",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_VALIDATION_EVIDENCE/README.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/README.md:165` targeting `Tools/ai/analyze_evidence_bundle_retention.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/README.md:165`. Target `docs/LOCAL_VALIDATION_EVIDENCE/README.md` and resolve `Tools/ai/analyze_evidence_bundle_retention.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_286",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_VALIDATION_EVIDENCE/agent_review_patch_plan_summary_20260501-230858.md"
```

## Context after

              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_VALIDATION_EVIDENCE/agent_review_patch_plan_summary_20260501-230858.md:21` targeting `Scripting/shared/config_model.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/agent_review_patch_plan_summary_20260501-230858.md:21`. Target `docs/LOCAL_VALIDATION_EVIDENCE/agent_review_patch_plan_summary_20260501-230858.md` and resolve `Scripting/shared/config_model.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
