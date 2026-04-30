# JSON Schemas

## Purpose

This document records known and expected JSON data structures used by the project.

The goal is to make report and artifact contracts explicit before adding strict validators.

## Current status

Formal JSON schemas are partial.

The repository has deterministic validators for JSON parseability, generated artifact destinations, generated Python policy, AI dry-run matrix report contracts and NPU helper smoke/unit/docs reports, but many domain artifacts still have only lightweight notes.

GitHub-only agents must not infer local report contents that are not present in the repository. When local `output/` reports are required, mark validation as pending.

## Expected JSON categories

| Category | Typical role | Status |
|---|---|---|
| audio analysis JSON | Technical audio data used by Blender scripts | not fully specified |
| track summary JSON | Compact track-level summary | partially specified in `docs/AI_ARTIFACT_SCHEMAS.md` |
| music context JSON | Semantic and musical context for AI-assisted workflows | not fully specified |
| keyframe JSON | Animation and timing data for Blender | not fully specified |
| implementation draft JSON | AI-generated implementation plan | partially covered by NPU helper contract validators |
| generated artifact plan JSON | Proposed generated artifact paths and content descriptors | partially covered by generated artifact path policy and NPU helper validators |
| provider request/result envelope JSON | Planned or future provider exchange envelopes | partial NPU helper contract only; no runtime provider execution |
| migration readiness report JSON | Gate report before runtime wiring | partial NPU helper contract only |
| patch task packet JSON | Patch or service packet for AI workflows | not fully specified |
| project manifest JSON | File index or project code manifest | present in AI index areas |
| AI dry-run matrix report JSON | Machine-readable dry-run matrix result | contract validator exists |
| NPU helper validation report JSON | Machine-readable NPU helper validation result | focused validators exist |
| validator report JSON | Machine-readable validation result | common fields under review |
| generated artifact path report JSON | Destination-policy result for generated files | validator exists |

## Report / artifact contract gap index

| Report / artifact | Typical path | Producer | Current validator | Current required fields | Missing checks / notes |
|---|---|---|---|---|---|
| AI dry-run matrix report | `output/ai_pipeline/dry_run_matrix_report.json` | `Tools/ai/run_pipeline_dry_run_matrix.py` | `Tools/validation/check_ai_dry_run_matrix_contract.py` | `schema_version`, `repo_root`, `output_dir`, `case_count`, `passed`, `results` | Future additive checks should remain warning-first until local samples are reviewed. |
| Individual AI pipeline dry-run report | `output/ai_pipeline/dry_run_matrix/<case>/ai_pipeline_dry_run_report.json` | `Tools/ai/run_parallel_artifact_pipeline.py` through matrix cases | `Tools/validation/check_ai_pipeline_report_contract.py`; also invoked by `check_ai_dry_run_matrix_contract.py` for referenced case reports | schema-v6 root fields plus `summary`, `schedule`, `lanes`, `agent_state_packet`, `steps`, `post_run_expected_outputs` | Unknown future fields remain accepted; `--require-dry-run` enforces `dry_run=true` and planned-only steps for dry-run reports. |
| NPU helper module smoke report | `output/validation/npu_pipeline_modules.json` | `Tools/validation/check_npu_pipeline_modules.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | Contract is helper-focused and provider-free; do not use it as runtime proof. |
| NPU helper unit-test report | `output/validation/npu_pipeline_helper_tests.json` | `Tools/validation/check_npu_pipeline_helper_tests.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks.tests_run`, `checks.error_count`, `checks.failure_count` | Wraps deterministic `unittest`; no Blender/NPU/Ollama/provider execution. |
| NPU helper docs report | `output/validation/npu_pipeline_docs.json` | `Tools/validation/check_npu_pipeline_docs.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | Checks `Tools/npu/pipeline/README.md` against expected helper modules/terms. |
| Generated artifact path policy report | `output/validation/generated_artifact_path_policy.json` | `Tools/validation/check_generated_artifact_path_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `path_count`, `path_results` | Review common validator report fields with TD-015. |
| Generated Python policy report | `output/validation/generated_python_policy.json` | `Tools/validation/check_generated_python_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Document future adapter composition in a separate template. |
| Generated Blender script policy report | `output/validation/generated_blender_script_policy.json` | `Tools/validation/check_generated_blender_script_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Blender-specific; must not become the generic policy boundary. |
| Agent memory policy report | `output/validation/agent_memory_policy.json` | `Tools/validation/check_agent_memory_policy.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `passed`, policy-specific result fields | Local SQLite inspection requires workstation access. |
| Python syntax report | `output/validation/python_syntax.json` | `Tools/validation/check_python_syntax.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `checked_count`, `failed_count`, `passed`, `results` | Does not currently expose `errors` at root; evaluate in validator report consistency review. |
| Package structure report | `output/validation/package_structure.json` | `Tools/validation/check_package_structure.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `scripting_root`, `package_count`, `warning_count`, `passed`, `packages` | Does not currently expose `errors` at root; warnings are package-level. |
| JSON artifact report | `output/validation/json_artifacts.json` | `Tools/validation/check_json_artifacts.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `checked_count`, `skipped_count`, `failed_count`, `passed`, `results` | Does not currently expose `errors` at root; failures live in `results`. |
| NPU implementation draft fixture/contract | in-memory fixture or future generated artifact | `Tools/npu/pipeline/fixtures.py`, future NPU pipeline runtime | `Tools/npu/pipeline/validators.py`; exercised by NPU helper validators | `implementation_kind`, `safety`, `reference_files`, `proposed_files`, `implementation_plan` | Current validator is permissive and preserves unknown future fields. |
| NPU provider request descriptor | in-memory fixture or future provider adapter payload | `Tools/npu/pipeline/providers.py` | `validate_provider_request()`; exercised by NPU helper validators | `provider`, `model`, `prompt`, `max_tokens` | Descriptor only; current helper validators must not execute provider calls. |
| NPU migration readiness report | in-memory report, future output if persisted | `Tools/npu/pipeline/migration_readiness.py` | exercised by NPU helper validators | `schema_version`, `kind`, `target_file`, `allowed_to_modify_runtime`, `ready`, `failed_count`, `checks` | Default readiness blocks runtime wiring. |
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
- Keep NPU helper report schemas separate from runtime provider schemas until runtime wiring exists.

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

1. Keep validating local `output/` report samples on the workstation after report-producer changes.
2. Extend `check_ai_pipeline_report_contract.py` only when field meanings are already documented.
3. Continue with domain artifacts such as music summaries and scene specs after report contracts remain stable.
4. Keep unknown future fields accepted unless a validator has a clear reason to reject them.
5. After PR #41 local validation, review the generated `npu_pipeline_*.json` reports before tightening any NPU helper report contract.
