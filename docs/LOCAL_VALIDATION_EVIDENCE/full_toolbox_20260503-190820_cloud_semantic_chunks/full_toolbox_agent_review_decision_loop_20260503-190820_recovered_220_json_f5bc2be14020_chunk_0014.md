# Evidence Chunk 0014/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `1919`
- line_end: `2077`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0013.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0015.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Correggere riferimenti mancanti a percorsi Python nei file Markdown (`Scripting/v61b/README.md`, `Tools/npu/README.md`).  
**Segnali principali**

## Context before

              "id": "consistency_069",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Scripting/v61b/README.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/v61b/README.md:23` targeting `text\nmain_v61b.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/v61b/README.md:23`. Target `Scripting/v61b/README.md` and resolve `text\nmain_v61b.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",

## Chunk content

```json
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
              "id": "consistency_070",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Scripting/v61b/README.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/v61b/README.md:88` targeting `Scripting/shared/panel_base.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/v61b/README.md:88`. Target `Scripting/v61b/README.md` and resolve `Scripting/shared/panel_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_071",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Scripting/v61b/README.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Scripting/v61b/README.md:89` targeting `Scripting/shared/hotpatch_base.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Scripting/v61b/README.md:89`. Target `Scripting/v61b/README.md` and resolve `Scripting/shared/hotpatch_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_072",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/README.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/README.md:18` targeting `build_*context*.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/README.md:18`. Target `Tools/npu/README.md` and resolve `build_*context*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_073",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/README.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/README.md:19` targeting `run_*pipeline*.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/README.md:19`. Target `Tools/npu/README.md` and resolve `run_*pipeline*.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_074",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:663` targeting `File.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:663`. Target `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md` and resolve `File.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_075",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:665` targeting `File.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:665`. Target `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md` and resolve `File.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
```

## Context after

              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_076",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md"
              ],
