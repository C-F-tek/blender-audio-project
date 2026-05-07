# Evidence Chunk 0007/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `1403`
- line_end: `1553`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0006.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0008.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: reports. Preview: "edit_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_mark...

## Context before

              "manual_review_required": true
            },
            {
              "id": "consistency_013",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256` targeting `Tools/validation/check_markdown_command_hygiene.py`.",

## Chunk content

```json
              "edit_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md:256`. Target `docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
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
              "id": "consistency_045",
              "area": "md_powershell",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292` targeting `some_script.ps1`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:292`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_script.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_046",
              "area": "md_powershell",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325` targeting `some_runner.ps1`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md:325`. Target `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` and resolve `some_runner.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_047",
              "area": "md_powershell",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29` targeting `run_patch_bundle.ps1`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md:29`. Target `CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md` and resolve `run_patch_bundle.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_048",
              "area": "md_powershell",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/AUTO_PUSH_GENERATED_ARTIFACTS.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106` targeting `your_app_regenerate_indexes.ps1`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md:106`. Target `docs/AUTO_PUSH_GENERATED_ARTIFACTS.md` and resolve `your_app_regenerate_indexes.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_049",
              "area": "md_powershell",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7` targeting `text\nrun_unified_full0to10_quality_supervisor.ps1`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md:7`. Target `docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md` and resolve `text\nrun_unified_full0to10_quality_supervisor.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_050",
              "area": "md_powershell",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101` targeting `validate_after_patch.ps1`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
