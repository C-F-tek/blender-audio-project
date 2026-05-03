# Evidence Chunk 0015/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `2078`
- line_end: `2233`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0014.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0016.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Rilevare e correggere riferimenti a percorsi Python mancanti nei file Markdown del progetto.  
**Segnali principali**: `md_mentions_missing_python_path` con alto punteggio in

## Context before

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

## Chunk content

```json
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
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:666` targeting `File.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md:666`. Target `Tools/npu/npu_blender_manual_chunks/chunk_192_blender_manual_html_keying_sets.md` and resolve `File.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_077",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md:8` targeting `matplotlib.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md:8`. Target `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md` and resolve `matplotlib.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_078",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md:20` targeting `matplotlib.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md:20`. Target `Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md` and resolve `matplotlib.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_079",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md:8` targeting `matplotlib.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md:8`. Target `Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md` and resolve `matplotlib.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_080",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:49` targeting `_scene_builder_candidate.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:49`. Target `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_081",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_python_path` at `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:57` targeting `_scene_builder_candidate.py`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_python_path` using mapper evidence `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md:57`. Target `Tools/npu/npu_code_chunks/chunk_013_Tools_npu_run_dual_ai_pipeline_py.md` and resolve `_scene_builder_candidate.py` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
              "id": "consistency_082",
              "area": "md_python",
```

## Context after

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
