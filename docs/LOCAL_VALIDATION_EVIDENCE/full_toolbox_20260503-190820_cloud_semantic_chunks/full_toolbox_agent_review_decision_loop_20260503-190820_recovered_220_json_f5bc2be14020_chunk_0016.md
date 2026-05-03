# Evidence Chunk 0016/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `2234`
- line_end: `2376`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0015.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0017.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Correggere riferimenti a percorsi Python mancanti nei file Markdown dei moduli NPU, garantendo coerenza documentale per il pipeline AI.  
**Segnali principali**: `md_mentions_missing_python_path` alto in `chunk_013` (linee 141 e 149) e `chunk_014` (linea 137), puntando a `generated_scene_builder_candidate.py` o `_scene

## Context before

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
              "id": "consistency_082",
              "area": "md_python",

## Chunk content

```json
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:141` targeting `indexAI/scene_scripts/generated_scene_builder_candidate.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:141`. Target `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `indexAI/scene_scripts/generated_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_083",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:149` targeting `indexAI/scene_scripts/generated_scene_builder_candidate.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:149`. Target `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `indexAI/scene_scripts/generated_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_084",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md:137` targeting `_scene_builder_candidate.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md:137`. Target `Tools/npu/npu_code_chunks/chunk_014_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_085",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md:131` targeting `_scene_builder_candidate.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md:131`. Target `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_086",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md:154` targeting `_scene_builder_candidate.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md:154`. Target `Tools/npu/npu_code_chunks/chunk_016_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_087",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_053_Scripting_v61b_PROJECT_STRUCTURE_md.md"
              ],
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
```

## Context after

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
