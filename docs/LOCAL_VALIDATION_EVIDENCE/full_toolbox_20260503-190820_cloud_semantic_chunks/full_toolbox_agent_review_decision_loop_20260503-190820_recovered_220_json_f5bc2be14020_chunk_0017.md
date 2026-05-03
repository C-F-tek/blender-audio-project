# Evidence Chunk 0017/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `2377`
- line_end: `2527`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0016.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0018.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Verificare la coerenza tra documentazione Markdown e file Python, correggendo riferimenti mancanti (`md_mentions_missing_python_path`).  
**Segnali principali**: Alti punteggi di mancata

## Context before

              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md:42` targeting `spaziotempo/features/water.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md:42`. Target `Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md` and resolve `spaziotempo/features/water.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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

## Chunk content

```json
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_088",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md:96` targeting `Scripting/shared/panel_base.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md:96`. Target `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md` and resolve `Scripting/shared/panel_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_089",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md:97` targeting `Scripting/shared/hotpatch_base.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md:97`. Target `Tools/npu/npu_code_chunks/chunk_064_Scripting_v61b_README_md.md` and resolve `Scripting/shared/hotpatch_base.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_090",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_080_Scripting_v61b_spaziotempo_core_registry_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_080_Scripting_v61b_spaziotempo_core_registry_py.md:230` targeting `spaziotempo/features/water.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_080_Scripting_v61b_spaziotempo_core_registry_py.md:230`. Target `Tools/npu/npu_code_chunks/chunk_080_Scripting_v61b_spaziotempo_core_registry_py.md` and resolve `spaziotempo/features/water.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_091",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_085_Tools_npu_build_ai_service_packet_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_085_Tools_npu_build_ai_service_packet_py.md:76` targeting `_scene_builder_candidate.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_085_Tools_npu_build_ai_service_packet_py.md:76`. Target `Tools/npu/npu_code_chunks/chunk_085_Tools_npu_build_ai_service_packet_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_092",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_102_Tools_npu_npu_guardrail_service_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_102_Tools_npu_npu_guardrail_service_py.md:19` targeting `args.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_102_Tools_npu_npu_guardrail_service_py.md:19`. Target `Tools/npu/npu_code_chunks/chunk_102_Tools_npu_npu_guardrail_service_py.md` and resolve `args.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_093",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/repo_patch_runner/README.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/repo_patch_runner/README.md:34` targeting `Scripting/example.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/repo_patch_runner/README.md:34`. Target `Tools/repo_patch_runner/README.md` and resolve `Scripting/example.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_094",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/validation/README.md"
              ],
