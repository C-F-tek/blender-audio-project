# Evidence Chunk 0019/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `2692`
- line_end: `2841`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0018.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0020.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Verificare e correggere riferimenti a percorsi Python mancanti nei file Markdown, garantendo coerenza tra documentazione e codice.  
**Segnali principali**: `md_mentions_missing_python_path` con alto valore di rilevamento in vari file (`DEVELOPER_GUIDE.md`, `2026-04-29_superseded

## Context before

            },
            {
              "id": "consistency_256",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/CODE_CONSULTATION_REPORT.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/CODE_CONSULTATION_REPORT.md:264` targeting `Tools/validation/check_docs_paths.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/CODE_CONSULTATION_REPORT.md:264`. Target `docs/CODE_CONSULTATION_REPORT.md` and resolve `Tools/validation/check_docs_paths.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",

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
              "id": "consistency_257",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/DEVELOPER_GUIDE.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/DEVELOPER_GUIDE.md:152` targeting `text\nTools/npu/pipeline/\n  config.py\n  context_builder.py\n  prompts.py\n  providers.py\n  validators.py\n  artifact_writer.py\n  runner.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/DEVELOPER_GUIDE.md:152`. Target `docs/DEVELOPER_GUIDE.md` and resolve `text\nTools/npu/pipeline/\n  config.py\n  context_builder.py\n  prompts.py\n  providers.py\n  validators.py\n  artifact_writer.py\n  runner.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_258",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:42` targeting `text\nTools/workflow/smart_ai_context.py\nTools/npu/npu_guardrail_service.py\nAI pipeline smart context stage\nNPU guardrail lane\nschema-v6 pipeline report\nrun_pipeline_dry_run_matrix.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:42`. Target `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md` and resolve `text\nTools/workflow/smart_ai_context.py\nTools/npu/npu_guardrail_service.py\nAI pipeline smart context stage\nNPU guardrail lane\nschema-v6 pipeline report\nrun_pipeline_dry_run_matrix.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_259",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:138` targeting `Tools/ai_core/json_utils.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:138`. Target `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md` and resolve `Tools/ai_core/json_utils.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_260",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:201` targeting `text\nTools/workflow/run_local_validation_after_refactor.ps1\nTools/validation/*.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md:201`. Target `docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md` and resolve `text\nTools/workflow/run_local_validation_after_refactor.ps1\nTools/validation/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_261",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:53` targeting `text\nTools/validation/check_generated_<target>_script_policy.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:53`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `text\nTools/validation/check_generated_<target>_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_262",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:54` targeting `_script_policy.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md:54`. Target `docs/GENERATED_PYTHON_ADAPTER_TEMPLATE.md` and resolve `_script_policy.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
```

## Context after

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
