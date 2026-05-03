# Evidence Chunk 0022/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `3141`
- line_end: `3286`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0021.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0023.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Redigere patch mirati per risolvere i riferimenti mancanti a percorsi Python (`md_mentions_missing_python_path`) nei documenti Markdown.  
**Segnali principali**: alto livello di `md_mentions_missing_python_path` in vari file di documentazione (`macro-local-validation-prototype-gate.md`, `next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md`, ecc.).  
**Guardrail / errori**: fermarsi se l’edit è solo sp

## Context before

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

## Chunk content

```json
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
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_275",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:445` targeting `check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:445`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_276",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md:247` targeting `text\nScripting/v61b/*.py\nScripting/v61b/**/*.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md:247`. Target `docs/LOCAL_AI_TASKS/next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md` and resolve `text\nScripting/v61b/*.py\nScripting/v61b/**/*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_277",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:78` targeting `check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:78`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_278",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap.md:85` targeting `text\nempty_recommendations_reason: context_echo_detected\nschema_status: wrong_json_shape\nrecommended_next_layer: compact_prompt_retry or build_agent_review_patch_plan.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap.md:85`. Target `docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap.md` and resolve `text\nempty_recommendations_reason: context_echo_detected\nschema_status: wrong_json_shape\nrecommended_next_layer: compact_prompt_retry or build_agent_review_patch_plan.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_279",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154` targeting `powershell\npython ./Tools/validation/check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md:154`. Target `docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md` and resolve `powershell\npython ./Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_280",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
```

## Context after

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
