# AI Artifact Schemas

Lightweight schema notes for the additive AI pipeline.

This document records the known minimum keys and current contract gaps for AI pipeline artifacts. It is intentionally not a strict JSON Schema implementation yet.

This file is a compact schema guide. `docs/JSON_SCHEMAS.md` remains a broad schema notebook/catalog and must not override the current run-unica contract.

## Run-unica schema doctrine

AI artifacts that participate in run-unica work follow the current IA-Carmine doctrine:

```text
master contains PR #187 unified launcher baseline
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
400 lines = hard limit for maintained docs and source files
limitations = backlog to overcome, not reasons to skip available tools
```

When a run-unica execution produces evidence, recommendations, patch plans or patch specs, the schema family must also account for the companion artifacts that make the handoff complete:

```text
launcher manifest
phase_status / phase_reports
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox run telemetry summary
shared AI-to-AI bundle/final summary
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
file-line-limit reports when maintainability is in scope
```

Telemetry is not a replacement schema for evidence or patch plans. It is a companion schema that explains whether the producing lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

A schema entry for a run-unica-derived patch plan/spec is incomplete if it omits the companion telemetry/capability/final-summary and relevant discovery/index/CSV/file-line-limit context.

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

Validation command ownership:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Large validator/tool catalogs such as `Tools/validation/README.md` are references only; use them after compact runbook/contract docs when needed.

## Related report contracts

AI artifacts are separate from validation reports. Do not mix input-domain artifact schemas with generic validator report contracts.

| Report | Typical producer | Current validator / checker | Required or common fields | Notes |
|---|---|---|---|---|
| `dry_run_matrix_report.json` | `Tools/ai/run_pipeline_dry_run_matrix.py` | `Tools/validation/check_ai_dry_run_matrix_contract.py` | `schema_version`, `repo_root`, `output_dir`, `case_count`, `passed`, `results` | Report contract, not Blender/audio adapter. |
| `ai_pipeline_dry_run_report.json` | `Tools/ai/run_parallel_artifact_pipeline.py` | `Tools/validation/check_ai_pipeline_report_contract.py` | schema-v6 fields: `schema_version`, `generated_at`, `repo_root`, `output_dir`, `dry_run`, `passed`, `preflight`, `step_count`, `summary`, `schedule`, `lanes`, `steps` | Per-case report contract; use `--require-dry-run` for matrix case reports. |
| `ai_pipeline_dry_run_matrix_evidence.json` | `Tools/ai/build_dry_run_matrix_evidence_bundle.py` | `Tools/validation/check_dry_run_matrix_evidence_bundle.py` | `schema_version`, `kind`, `provider_execution_performed`, `matrix`, `validation_reports`, `case_summary`, `cases`, `decision` | Compact Git-trackable evidence for a local dry-run matrix. It proves planned-only dry-run behavior, not GPU/NPU provider execution. |
| `runtime_tool_usage_telemetry_*.json` | `Tools/ai/build_runtime_tool_usage_telemetry.py` | report-contract validation / bundle validation | `schema_version`, `kind`, `generated_at`, `repo_root`, `inputs`, `summary`, `tool_calls`, `warnings`, `errors` | Companion telemetry for broker/tool execution. Must preserve broker report inputs and executed/failed/blocked counts. |
| `runtime_tool_capability_manifest_*.json` | current runtime capability manifest builder when present | report-contract validation / bundle validation | `schema_version`, `kind`, `generated_at`, `repo_root`, capability/tool entries, `warnings`, `errors` | Capability and guardrail context for broker/tool execution. Historical builder names must be checked against current code. |
| `runtime_hardware_capability_manifest_*.json` | `Tools/ai/build_runtime_hardware_capability_manifest.py` in PR #192 or Full0To10 hardware capability package | report-contract validation / bundle validation | `schema_version`, `kind`, `generated_at`, `repo_root`, hardware/capability entries, side-effect guardrails, `warnings`, `errors` | Report-only hardware/capability context for CPU/GPU.0/NPU/NVIDIA-style lanes. |
| `file_line_limit_report.json` | `Tools/validation/check_file_line_limits.py` | self-report plus JSON parseability | `schema_version`, `kind=file_line_limit_report`, `max_lines`, `checked_file_count`, `violation_count`, `violations`, `errors`, `passed` | Report-only 400-line policy evidence. Does not rewrite, split, delete or apply patches. |
| `full_toolbox_run_telemetry_summary_*.json` | `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | report-contract validation / bundle validation | `schema_version`, `kind`, `generated_at`, `repo_root`, `gpu_npu`, `provider`, `runtime_tools`, `patch_plan`, `guardrails`, `warnings`, `errors` | Production summary that explains provider, GPU/NPU, broker, patch-plan and source-write state. |
| `shared_toolbox_ai_to_ai_bundle_*.json` | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | bundle/final-summary validation | `schema_version`, `kind`, `generated_at`, `repo_root`, `evidence`, `telemetry`, `capabilities`, `recommendations`, `patch_plan`, `provider_diagnostics`, `guardrails` | Production AI-to-AI handoff. Must group evidence, patch plan, telemetry and capability references. |
| `shared_toolbox_ai_to_ai_final_summary_*.json` | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | final-summary validation | `passed`, `patch_plan_summary_seen`, `patch_plan_count`, `provider_advisory_state`, `provider_failure_detected`, `deterministic_recovery_used`, `provider_failure_reasons`, `degraded_provider_components`, `patch_application_performed`, `source_writes_performed` | Compact state used by next AI/operator to avoid opening full bundles first. |
| `*selected_chunks*.json` | `Tools/ai/select_semantic_code_chunks.py` | `Tools/validation/check_selected_semantic_chunks.py` | `schema_version`, `kind`, `selected_count`, `max_chunks`, `total_selected_chars`, `provider_execution_performed`, `source_writes_performed`, `selected_chunks` | Bounded focused context selected from semantic chunks; not a patch or provider execution claim. |
| `*selected_chunks*_evidence.json` | `Tools/validation/check_selected_semantic_chunks.py` | `Tools/validation/check_selected_semantic_chunks.py` | `schema_version`, `kind`, `source_bundle`, `passed`, `selected_count`, `total_selected_chars`, `decision` | Compact Git-trackable evidence for selected focused context. |
| `selective_execution_plan.json` | `Tools/ai/build_selective_execution_plan.py` | `Tools/validation/check_selective_execution_plan.py` | `schema_version`, `kind`, `apply_mode`, `provider_execution_performed`, `recommended_validators`, `recommended_patch_specs`, `next_command_set`, optional telemetry/capability summary fields | Report-only recommendation layer; does not run providers or apply patches. Run-unica-derived recommendations require companion telemetry/capability context. |
| `ai_workload_quality_lane_routing.json` | `Tools/ai/build_workload_quality_lane_routing.py` | summarized in `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `primary_advisory_provider`, `policy`, `mode`, `routing` | Preserves Ollama/GPU as the quality-gated primary advisory lane; excludes unusable NPU workload output from advisory context. Quality state must be carried into telemetry/bundle when provider lanes participate. |
| `npu_decode_quality_remediation.json` | `Tools/validation/check_npu_decode_quality_remediation.py` | summarized in `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `policy`, `mode`, `checks` | Report-only remediation planning; no provider execution or runtime changes. |
| `npu_decode_smoke_diagnostic.json` | `Tools/ai/run_npu_decode_smoke_diagnostic.py` | summarized in `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `policy`, `mode`, `provider`, `checks` | Explicit OpenVINO/NPU probe/guardrail/decode diagnostic; passing smoke is not NPU advisory promotion. |
| `*_evidence.json` | `Tools/ai/build_github_evidence_bundle.py` | `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_reports`, `reports`, `decision` | Compact Git-trackable evidence for GitHub-only agents; full local `output/` remains ignored. When from run unica, include telemetry/capability companion artifacts. |
| `*proposals.json` | `Tools/ai/build_repository_change_proposals.py` | `Tools/validation/check_repository_change_proposals.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `profile`, `apply_mode`, `reports_read`, `proposals` | Manual-review proposal report with `suggestion_outputs` descriptors for code, Markdown, JSON, PowerShell and workflow targets. Run-unica-derived proposals need telemetry/capability context. |
| `full_context_golden_proposals.json` | `Tools/ai/build_full_context_golden_proposals.py` | `Tools/validation/check_repository_change_proposals.py`, `Tools/validation/check_full_context_golden_proposals.py` | Generic proposal fields plus required proposal families P1-P6 | Deterministic full-context proposal coverage; manual-review-only and no source mutation. |
| `proposal_patch_specs*_manifest.json` | `Tools/ai/build_patch_specs_from_proposals.py` | `Tools/validation/check_patch_spec_drafts.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_proposal_report`, `apply_mode`, `draft_status`, `specs` | Inert draft patch-spec manifest under `output/patch_specs/`; no provider execution, no queue write and no concrete replacements. If derived from run-unica evidence, require companion telemetry/capability context in the handoff. |
| `reviewed_patch_spec*_manifest.json` | `Tools/ai/promote_patch_spec_draft.py` | `Tools/validation/check_reviewed_patch_specs.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_draft_spec`, `source_replacement_plan`, `apply_mode`, `review_status`, `specs` | Concrete reviewed patch-spec manifest under `output/patch_specs/`; dry-run required, no source write and no queue write. Still not an automatic apply artifact. |
| `ai_context_pack*.json` | `Tools/ai/build_ai_context_pack.py` | `Tools/validation/check_ai_context_pack_contract.py` | `schema_version`, `kind`, `profile`, `apply_mode`, `provider_execution_performed`, `validation_commands`, `stop_conditions`, `files` | Local task-scoped context under ignored `output/ai_context_packs/`; no provider execution and no source writes. |
| `*context_pack_evidence.json` | `Tools/ai/build_ai_context_pack.py` | `Tools/validation/check_ai_context_pack_contract.py` | `schema_version`, `kind`, `profile`, `passed`, `provider_execution_performed`, `included_paths`, `decision` | Compact Git-trackable summary of a context pack for GitHub-only review. |
| `npu_pipeline_modules.json` | `Tools/validation/check_npu_pipeline_modules.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | NPU helper import/contract smoke; not runtime proof. |
| `npu_pipeline_helper_tests.json` | `Tools/validation/check_npu_pipeline_helper_tests.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | JSON wrapper around deterministic unit tests for helper modules. |
| `npu_pipeline_docs.json` | `Tools/validation/check_npu_pipeline_docs.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | Documentation/module alignment for `Tools/npu/pipeline/`. |
| `generated_python_policy.json` | `Tools/validation/check_generated_python_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Generic generated Python layer. |
| `generated_artifact_path_policy.json` | `Tools/validation/check_generated_artifact_path_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `path_results` | Destination-policy layer only. |
| `generated_blender_script_policy.json` | `Tools/validation/check_generated_blender_script_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Blender-specific adapter composed over generic Python policy. |
| `agent_memory_policy.json` | `Tools/validation/check_agent_memory_policy.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `passed` | Local DB inspection requires workstation access. |

## Discovery/index/CSV/file-line schema notes

These surfaces are evidence and visibility schemas, not source schemas.

Expected artifact families:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV
Python line-count CSV/MD
file-line-limit JSON/MD
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD
repository consistency map/smoke JSON/MD
auto-discovery report
index repair plan/report
```

Schema notes:

```text
provider_execution_performed=false for pure inventory/count/report lanes
source_writes_performed=false unless explicit apply/regeneration is selected
patch_application_performed=false unless explicit patch apply is selected
output paths stay under ignored output/** unless compact evidence is intentionally promoted
indexAI/code_chunks/** is not commit-ready source
index repair is plan/report-first unless explicitly requested
```

## Schema planning rules

- Keep unknown future fields accepted unless a field is unsafe or ambiguous.
- Keep warnings separate from blocking errors.
- Do not enforce Blender-specific rules in generic AI artifact schemas.
- Do not enforce WAV/audio-specific rules in generic generated-file validators.
- Do not use NPU helper validation reports as proof of provider/runtime execution.
- Do not hand-edit generated index manifests to satisfy schema notes.
- Add strict checks only after representative local artifacts are available.
- Do not treat run-unica evidence as complete without telemetry/capability/final summary and relevant discovery/index/CSV/file-line surfaces.
- Do not treat patch-plan or patch-spec artifacts as complete if their producing run state is unknown.
- Do not treat large Markdown, file existence, dry-run matrix success, provider report existence or NPU smoke success as proof of run-unica completion.
- Treat limitations as backlog to overcome, not as static reasons to skip current tools.

## GitHub-only limit

GitHub-only agents may update schema notes and gap indexes, but must not claim validation against local `output/` artifacts unless logs or report files are available in the repository or attached to the task.

Required marker for GitHub-only schema/report PRs:

```text
Local workstation validation pending.
```
