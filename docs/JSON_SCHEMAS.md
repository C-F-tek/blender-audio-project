# JSON Schemas

## Purpose

This document records known and expected JSON data structures used by the project.

The goal is to make report and artifact contracts explicit before adding strict validators.

## Current status

Formal JSON schemas are partial.

The repository has deterministic validators for JSON parseability, generated artifact destinations, generated Python policy and dry-run matrix report contracts, but many domain artifacts still have only lightweight notes.

GitHub-only agents must not infer local report contents that are not present in the repository. When local `output/` reports are required, mark validation as pending.

## Expected JSON categories

| Category | Typical role | Status |
|---|---|---|
| audio analysis JSON | Technical audio data used by Blender scripts | not fully specified |
| track summary JSON | Compact track-level summary | partially specified in `docs/AI_ARTIFACT_SCHEMAS.md` |
| music context JSON | Semantic and musical context for AI-assisted workflows | not fully specified |
| keyframe JSON | Animation and timing data for Blender | not fully specified |
| implementation draft JSON | AI-generated implementation plan | not fully specified |
| patch task packet JSON | Patch or service packet for AI workflows | not fully specified |
| project manifest JSON | File index or project code manifest | present in AI index areas |
| AI dry-run matrix report JSON | Machine-readable dry-run matrix result | contract validator exists |
| validator report JSON | Machine-readable validation result | common fields under review |
| generated artifact path report JSON | Destination-policy result for generated files | validator exists |

## Report / artifact contract gap index

| Report / artifact | Typical path | Producer | Current validator | Current required fields | Missing checks / notes |
|---|---|---|---|---|---|
| AI dry-run matrix report | `output/ai_pipeline/dry_run_matrix_report.json` | `Tools/ai/run_pipeline_dry_run_matrix.py` | `Tools/validation/check_ai_dry_run_matrix_contract.py` | `schema_version`, `repo_root`, `output_dir`, `case_count`, `passed`, `results` | Future additive checks should remain warning-first until local samples are reviewed. |
| Individual AI pipeline dry-run report | `output/ai_pipeline/dry_run_matrix/<case>/ai_pipeline_dry_run_report.json` | `Tools/ai/run_parallel_artifact_pipeline.py` through matrix cases | partially covered through matrix contract | `passed`, `summary`, `schedule`, `lanes`, `agent_state_packet`, `steps` | Need explicit per-report contract notes before strict validation. |
| Generated artifact path policy report | `output/validation/generated_artifact_path_policy.json` | `Tools/validation/check_generated_artifact_path_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `path_count`, `path_results` | Review common validator report fields with GHO-010. |
| Generated Python policy report | `output/validation/generated_python_policy.json` | `Tools/validation/check_generated_python_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Document future adapter composition in a separate template. |
| Generated Blender script policy report | `output/validation/generated_blender_script_policy.json` | `Tools/validation/check_generated_blender_script_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Blender-specific; must not become the generic policy boundary. |
| Agent memory policy report | `output/validation/agent_memory_policy.json` | `Tools/validation/check_agent_memory_policy.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `passed`, policy-specific result fields | Local SQLite inspection requires workstation access. |
| Python syntax report | `output/validation/python_syntax.json` | `Tools/validation/check_python_syntax.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `checked_count`, `failed_count`, `passed`, `results` | Does not currently expose `errors` at root; evaluate in validator report consistency review. |
| Package structure report | `output/validation/package_structure.json` | `Tools/validation/check_package_structure.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `scripting_root`, `package_count`, `warning_count`, `passed`, `packages` | Does not currently expose `errors` at root; warnings are package-level. |
| JSON artifact report | `output/validation/json_artifacts.json` | `Tools/validation/check_json_artifacts.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `checked_count`, `skipped_count`, `failed_count`, `passed`, `results` | Does not currently expose `errors` at root; failures live in `results`. |
| Track summary artifact | `output/*_track_summary.json` or AI pipeline artifact dir | `build_track_summary.py` or AI pipeline step | `Tools/ai/validate_ai_artifacts.py` for AI pipeline artifacts | `schema_version`, `source_analysis` | Confirm current local examples before strict schema. |
| Music segments artifact | `output/ai_pipeline/music_segments.json` | AI pipeline | `Tools/ai/validate_ai_artifacts.py` | `schema_version`, `segments` | Need segment item shape and timing units. |
| Audio event map artifact | `output/ai_pipeline/audio_event_map.json` | AI pipeline | `Tools/ai/validate_ai_artifacts.py` | `schema_version` | Need event item shape and required timing fields. |
| AI scene brief artifact | `output/ai_pipeline/ai_scene_brief.json` | AI pipeline / model provider | `Tools/ai/validate_ai_artifacts.py` | `schema_version`, `creative_intent`, `technical_intent` | Need deterministic checks for model-output shape without inventing fields. |
| AI resource budget artifact | `output/ai_pipeline/ai_resource_budget.json` | AI pipeline / model provider | `Tools/ai/validate_ai_artifacts.py` | `schema_version`, `recommendations` | Need explicit CPU/GPU/NPU field semantics before enforcing. |
| AI selected mapping artifact | `output/ai_pipeline/ai_selected_mapping.json` | AI pipeline / model provider | `Tools/ai/validate_ai_artifacts.py` | `schema_version`, `selected` | Need mapping item schema and target-runtime semantics. |
| AI validation report artifact | `output/ai_pipeline/ai_validation_report.json` | AI pipeline validator step | `Tools/ai/validate_ai_artifacts.py` | `schema_version`, `passed`, `score`, `blocking_errors`, `warnings` | Candidate for common validator-report alignment. |
| Project code manifest | `indexAI/project_code_manifest.json` | `Tools/npu/build_project_ai_index.py` | JSON parseability only | not fully specified | Generated index; do not hand-edit. |
| NPU code manifest | `Tools/npu/npu_code_manifest.json` | `Tools/npu/build_npu_code_context.py` | JSON parseability only | not fully specified | Generated index; do not hand-edit. |

## AI handling rules

- Never overwrite full analysis JSON files without explicit instruction.
- When producing derived summaries, write new files instead of replacing originals.
- Preserve unknown fields.
- Avoid destructive normalization.
- Mark inferred fields as assumptions.
- Prefer compact summaries for AI context while keeping originals intact.
- Keep strict schema enforcement additive and warning-first until current local report samples are reviewed.

## Recommended schema documentation format

For every confirmed JSON file type, document:

```text
File pattern:
Producer:
Consumer:
Required fields:
Optional fields:
Large fields:
Do not overwrite:
Current validator:
Missing checks:
Notes:
```

## Next action

1. Review current local `output/` report samples on the workstation.
2. Confirm field meanings before creating stricter schema validators.
3. Start with validator-report consistency: `schema_version`, `repo_root`, `passed`, `errors`.
4. Keep unknown future fields accepted unless a validator has a clear reason to reject them.
