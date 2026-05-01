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
| `ai_pipeline_dry_run_report.json` | `Tools/ai/run_parallel_artifact_pipeline.py` | `Tools/validation/check_ai_pipeline_report_contract.py` | schema-v6 fields: `schema_version`, `generated_at`, `repo_root`, `output_dir`, `dry_run`, `passed`, `preflight`, `step_count`, `summary`, `schedule`, `lanes`, `steps` | Per-case report contract; use `--require-dry-run` for matrix case reports. |
| `ai_pipeline_dry_run_matrix_evidence.json` | `Tools/ai/build_dry_run_matrix_evidence_bundle.py` | `Tools/validation/check_dry_run_matrix_evidence_bundle.py` | `schema_version`, `kind`, `provider_execution_performed`, `matrix`, `validation_reports`, `case_summary`, `cases`, `decision` | Compact Git-trackable evidence for a local dry-run matrix. It proves planned-only dry-run behavior, not GPU/NPU provider execution. |
| `*selected_chunks*.json` | `Tools/ai/select_semantic_code_chunks.py` | `Tools/validation/check_selected_semantic_chunks.py` | `schema_version`, `kind`, `selected_count`, `max_chunks`, `total_selected_chars`, `provider_execution_performed`, `source_writes_performed`, `selected_chunks` | Bounded focused context selected from semantic chunks; not a patch or provider execution claim. |
| `*selected_chunks*_evidence.json` | `Tools/validation/check_selected_semantic_chunks.py` | `Tools/validation/check_selected_semantic_chunks.py` | `schema_version`, `kind`, `source_bundle`, `passed`, `selected_count`, `total_selected_chars`, `decision` | Compact Git-trackable evidence for selected focused context. |
| `selective_execution_plan.json` | `Tools/ai/build_selective_execution_plan.py` | `Tools/validation/check_selective_execution_plan.py` | `schema_version`, `kind`, `apply_mode`, `provider_execution_performed`, `recommended_validators`, `recommended_patch_specs`, `next_command_set` | Report-only recommendation layer; does not run providers or apply patches. |
| `ai_workload_quality_lane_routing.json` | `Tools/ai/build_workload_quality_lane_routing.py` | summarized in `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `primary_advisory_provider`, `policy`, `mode`, `routing` | Preserves Ollama/GPU as the quality-gated primary advisory lane; excludes unusable NPU workload output from advisory context. |
| `npu_decode_quality_remediation.json` | `Tools/validation/check_npu_decode_quality_remediation.py` | summarized in `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `policy`, `mode`, `checks` | Report-only remediation planning; no provider execution or runtime changes. |
| `npu_decode_smoke_diagnostic.json` | `Tools/ai/run_npu_decode_smoke_diagnostic.py` | summarized in `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `policy`, `mode`, `provider`, `checks` | Explicit OpenVINO/NPU probe/guardrail/decode diagnostic; passing smoke is not NPU advisory promotion. |
| `*_evidence.json` | `Tools/ai/build_github_evidence_bundle.py` | `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_reports`, `reports`, `decision` | Compact Git-trackable evidence for GitHub-only agents; full local `output/` remains ignored. |
| `*proposals.json` | `Tools/ai/build_repository_change_proposals.py` | `Tools/validation/check_repository_change_proposals.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `profile`, `apply_mode`, `reports_read`, `proposals` | Manual-review proposal report with `suggestion_outputs` descriptors for code, Markdown, JSON, PowerShell and workflow targets. |
| `full_context_golden_proposals.json` | `Tools/ai/build_full_context_golden_proposals.py` | `Tools/validation/check_repository_change_proposals.py`, `Tools/validation/check_full_context_golden_proposals.py` | Generic proposal fields plus required proposal families P1-P6 | Deterministic full-context proposal coverage; manual-review-only and no source mutation. |
| `proposal_patch_specs*_manifest.json` | `Tools/ai/build_patch_specs_from_proposals.py` | `Tools/validation/check_patch_spec_drafts.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_proposal_report`, `apply_mode`, `draft_status`, `specs` | Inert draft patch-spec manifest under `output/patch_specs/`; no provider execution, no queue write and no concrete replacements. |
| `reviewed_patch_spec*_manifest.json` | `Tools/ai/promote_patch_spec_draft.py` | `Tools/validation/check_reviewed_patch_specs.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_draft_spec`, `source_replacement_plan`, `apply_mode`, `review_status`, `specs` | Concrete reviewed patch-spec manifest under `output/patch_specs/`; dry-run required, no source write and no queue write. |
| `ai_context_pack*.json` | `Tools/ai/build_ai_context_pack.py` | `Tools/validation/check_ai_context_pack_contract.py` | `schema_version`, `kind`, `profile`, `apply_mode`, `provider_execution_performed`, `validation_commands`, `stop_conditions`, `files` | Local task-scoped context under ignored `output/ai_context_packs/`; no provider execution and no source writes. |
| `*context_pack_evidence.json` | `Tools/ai/build_ai_context_pack.py` | `Tools/validation/check_ai_context_pack_contract.py` | `schema_version`, `kind`, `profile`, `passed`, `provider_execution_performed`, `included_paths`, `decision` | Compact Git-trackable summary of a context pack for GitHub-only review. |
| `npu_pipeline_modules.json` | `Tools/validation/check_npu_pipeline_modules.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | NPU helper import/contract smoke; not runtime proof. |
| `npu_pipeline_helper_tests.json` | `Tools/validation/check_npu_pipeline_helper_tests.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | JSON wrapper around deterministic unit tests for helper modules. |
| `npu_pipeline_docs.json` | `Tools/validation/check_npu_pipeline_docs.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | Documentation/module alignment for `Tools/npu/pipeline/`. |
| `generated_python_policy.json` | `Tools/validation/check_generated_python_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Generic generated Python layer. |
| `generated_artifact_path_policy.json` | `Tools/validation/check_generated_artifact_path_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `path_results` | Destination-policy layer only. |
| `generated_blender_script_policy.json` | `Tools/validation/check_generated_blender_script_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Blender-specific adapter composed over generic Python policy. |
| `agent_memory_policy.json` | `Tools/validation/check_agent_memory_policy.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `passed` | Local DB inspection requires workstation access. |

## Schema planning rules

- Keep unknown future fields accepted unless a field is unsafe or ambiguous.
- Keep warnings separate from blocking errors.
- Do not enforce Blender-specific rules in generic AI artifact schemas.
- Do not enforce WAV/audio-specific rules in generic generated-file validators.
- Do not use NPU helper validation reports as proof of provider/runtime execution.
- Do not hand-edit generated index manifests to satisfy schema notes.
- Add strict checks only after representative local artifacts are available.

## GitHub-only limit

GitHub-only agents may update schema notes and gap indexes, but must not claim validation against local `output/` artifacts unless logs or report files are available in the repository or attached to the task.

Required marker for GitHub-only schema/report PRs:

```text
Local workstation validation pending.
```
