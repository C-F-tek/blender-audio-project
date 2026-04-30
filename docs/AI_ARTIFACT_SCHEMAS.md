# AI Artifact Schemas

Lightweight schema notes for the additive AI pipeline.

This document records the known minimum keys and current contract gaps for AI pipeline artifacts. It is intentionally not a strict JSON Schema implementation yet.

## Required keys

| Artifact | Required keys | Producer | Current validator | Missing checks |
|---|---|---|---|---|
| `track_summary.json` | `schema_version`, `source_analysis` | `build_track_summary.py` or AI pipeline summary step | `Tools/ai/validate_ai_artifacts.py` | Confirm compact track metadata fields, source path semantics and optional analysis stats. |
| `music_segments.json` | `schema_version`, `segments` | AI pipeline segmentation step | `Tools/ai/validate_ai_artifacts.py` | Define segment item shape, timing units, ordering and overlap policy. |
| `audio_event_map.json` | `schema_version` | AI pipeline event-map step | `Tools/ai/validate_ai_artifacts.py` | Define event categories, timing fields and confidence ranges. |
| `ai_scene_brief.json` | `schema_version`, `creative_intent`, `technical_intent` | AI/model scene-brief step | `Tools/ai/validate_ai_artifacts.py` | Define stable top-level model-output fields without allowing invented required keys. |
| `ai_resource_budget.json` | `schema_version`, `recommendations` | AI/model budget step | `Tools/ai/validate_ai_artifacts.py` | Define CPU/GPU/NPU terms and keep workstation-specific values as local validation data. |
| `ai_selected_mapping.json` | `schema_version`, `selected` | AI/model mapping-selection step | `Tools/ai/validate_ai_artifacts.py` | Define mapping item shape and target-runtime adapter boundary. |
| `ai_validation_report.json` | `schema_version`, `passed`, `score`, `blocking_errors`, `warnings` | AI pipeline validation step | `Tools/ai/validate_ai_artifacts.py` | Align report fields with common validator report contract where practical. |

Validation command:

```powershell
py .\Tools\ai\validate_ai_artifacts.py --repo-root . --artifact-dir .\output\ai_pipeline
```

## Related report contracts

AI artifacts are separate from validation reports. Do not mix input-domain artifact schemas with generic validator report contracts.

| Report | Typical producer | Current validator / checker | Required or common fields | Notes |
|---|---|---|---|---|
| `dry_run_matrix_report.json` | `Tools/ai/run_pipeline_dry_run_matrix.py` | `Tools/validation/check_ai_dry_run_matrix_contract.py` | `schema_version`, `repo_root`, `output_dir`, `case_count`, `passed`, `results` | Report contract, not Blender/audio adapter. |
| `generated_python_policy.json` | `Tools/validation/check_generated_python_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Generic generated Python layer. |
| `generated_artifact_path_policy.json` | `Tools/validation/check_generated_artifact_path_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `path_results` | Destination-policy layer only. |
| `generated_blender_script_policy.json` | `Tools/validation/check_generated_blender_script_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Blender-specific adapter composed over generic Python policy. |
| `agent_memory_policy.json` | `Tools/validation/check_agent_memory_policy.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `passed` | Local DB inspection requires workstation access. |

## Schema planning rules

- Keep unknown future fields accepted unless a field is unsafe or ambiguous.
- Keep warnings separate from blocking errors.
- Do not enforce Blender-specific rules in generic AI artifact schemas.
- Do not enforce WAV/audio-specific rules in generic generated-file validators.
- Do not hand-edit generated index manifests to satisfy schema notes.
- Add strict checks only after representative local artifacts are available.

## GitHub-only limit

GitHub-only agents may update schema notes and gap indexes, but must not claim validation against local `output/` artifacts unless logs or report files are available in the repository or attached to the task.

Required marker for GitHub-only schema/report PRs:

```text
Local workstation validation pending.
```
