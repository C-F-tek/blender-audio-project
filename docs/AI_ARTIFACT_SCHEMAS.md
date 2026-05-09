# AI Artifact Schemas

## Status

Current lightweight schema notes for additive AI pipeline and run-unica artifacts.

Read together with:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

This document records known minimum keys and current contract gaps. It is intentionally not a strict JSON Schema implementation yet.

This file is a compact schema guide. `docs/JSON_SCHEMAS.md` is a historical/reference notebook and must not override current source code, launcher manifests, validators or run-unica contracts.

## Current code-driven references

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

## Run-unica schema doctrine

AI artifacts that participate in run-unica work follow current IA-Carmine doctrine:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
heap/exchange entry and exit are deterministic boundaries around the dynamic center
patchkit is the preferred deterministic source-write boundary for reviewed bundles
preferred active runbook/docs size <=400 lines
active Markdown hard threshold <=500 lines
maintained source/script target <=400 lines
limitations = backlog to overcome, not reasons to skip available tools
```

When a run-unica execution produces evidence, recommendations, patch suggestions, patch plans or patch specs, the schema family must also account for companion artifacts that make the handoff complete:

```text
launcher manifest
phase_status / phase_reports
heap/exchange runtime entry
heap/exchange runtime state
heap/exchange runtime exit product
heap/exchange lifecycle report
patchkit report when source-write boundary is selected
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox run telemetry summary
shared AI-to-AI bundle/final summary
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
file-line-limit reports when maintainability is in scope
patch suggestion product/separation reports when review PR flow is selected
```

Telemetry is not a replacement schema for evidence or patch plans. It is a companion schema that explains whether producing lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

## Required keys for legacy/audio-domain artifacts

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
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Large validator/tool catalogs such as `Tools/validation/README.md` are references only; use them after compact runbook/contract docs when needed.

## Related report contracts

AI artifacts are separate from validation reports. Do not mix input-domain artifact schemas with generic validator report contracts.

| Report | Typical producer | Current validator / checker | Required or common fields | Notes |
|---|---|---|---|---|
| `heap_exchange_runtime_entry.json` | `Tools/ai/build_heap_exchange_runtime_entry.py` | `Tools/validation/check_heap_exchange_runtime_lifecycle.py` | `schema_version`, `kind=heap_exchange_runtime_entry`, `stamp`, `repo_root`, `runtime_state`, `observer_dir`, `center_is_dynamic`, `lanes`, `available_lane_count`, safety flags | Dynamic heap/exchange entry boundary. Records available lanes; does not apply patches or run Blender/FFmpeg. |
| `heap_exchange_runtime_state.jsonl` | heap/exchange entry/exit builders | `Tools/validation/check_heap_exchange_runtime_lifecycle.py` | JSONL events such as `heap_entry`, `lane_registered`, `heap_exit` | Runtime event ledger for the dynamic center. Must be paired with public exchange events when required. |
| `heap_exchange_runtime_exit_product.json` | `Tools/ai/build_heap_exchange_runtime_exit.py` | `Tools/validation/check_heap_exchange_runtime_lifecycle.py` | `schema_version`, `kind=heap_exchange_runtime_exit_product`, `center_was_dynamic`, `runtime_event_count`, `operation_count`, `changed_count`, `concrete_operation_count`, `manual_review_required`, `passed`, safety flags | Deterministic OUT boundary. Product paths requiring review PR must not pass with metadata-only drafts. |
| `heap_exchange_runtime_lifecycle_*.json` | `Tools/validation/check_heap_exchange_runtime_lifecycle.py` | self-report plus report-contract validation | `schema_version`, `kind=heap_exchange_runtime_lifecycle`, `passed`, `checks`, `broken_checks`, `errors`, `warnings` | Validates entry, lane availability, runtime events, public events and concrete exit product when required. |
| `patchkit_apply_report` | `Tools/ai/patchkit/apply_patch_bundle.py` | patchkit validators and local review | `schema_version`, `kind=patchkit_apply_report`, `bundle`, `dry_run`, `operation_count`, `changed_count`, `results`, `validators`, `line_counts`, `passed`, safety flags | Preferred deterministic source-write report for reviewed patchkit bundles. |
| `dry_run_matrix_report.json` | `Tools/ai/run_pipeline_dry_run_matrix.py` | `Tools/validation/check_ai_dry_run_matrix_contract.py` | `schema_version`, `repo_root`, `output_dir`, `case_count`, `passed`, `results` | Report contract, not Blender/audio adapter. |
| `ai_pipeline_dry_run_report.json` | `Tools/ai/run_parallel_artifact_pipeline.py` | `Tools/validation/check_ai_pipeline_report_contract.py` | schema-v6 fields: `schema_version`, `generated_at`, `repo_root`, `output_dir`, `dry_run`, `passed`, `preflight`, `step_count`, `summary`, `schedule`, `lanes`, `steps` | Per-case report contract; use `--require-dry-run` for matrix case reports. |
| `patch_suggestion_bundle_apply*.json` | `Tools/ai/apply_patch_suggestion_bundle.py` | `Tools/validation/check_patch_suggestion_product_separation.py` | `schema_version`, `kind`, `discovered_reports`, `current_suggestion_reports`, `deterministic_operations`, `manual_review_product`, `failed_count`, `patch_product_status`, `ready_for_patch_suggestion_review` | Legacy/bridge product report for deterministic/manual-review patch suggestions. Published review-item counts may be capped; total counts remain available separately. |
| `patch_suggestion_product_separation*.json` | `Tools/validation/check_patch_suggestion_product_separation.py` | self-report plus report-contract validation | `schema_version`, `kind`, `passed`, `metrics`, `errors`, `warnings` | Validates essential product vs supplemental telemetry/debug separation. Deterministic-only product can pass when operations are ready and `failed_count=0`. |
| `full0to10_product_pr_chain_smoke*.json` | `Tools/validation/run_full0to10_product_pr_chain_smoke.py` | self-report plus report-contract validation | `schema_version`, `kind`, `passed`, `commands`, `workflow_trace`, `errors`, `warnings` | Focused temporary-repo smoke that verifies task report -> patch suggestion final phase -> product separation -> review PR prepare chain and launcher trace. |
| `review_pr_prepare*.json` | `Tools/ai/prepare_review_pr.py` | report-contract validation / manual review | `schema_version`, `kind`, `passed`, `repo_root`, `branch`, `include_paths`, `staged_paths`, `commit`, `push`, `pr`, `errors`, `warnings` | Review PR preparation evidence. Current include paths are explicit; draft PR creation and include-path autodiscovery are not implemented yet. |
| `runtime_tool_usage_telemetry_*.json` | `Tools/ai/build_runtime_tool_usage_telemetry.py` | report-contract validation / bundle validation | `schema_version`, `kind`, `generated_at`, `repo_root`, `inputs`, `summary`, `tool_calls`, `warnings`, `errors` | Companion telemetry for broker/tool execution. Must preserve broker report inputs and executed/failed/blocked counts. |
| `runtime_tool_capability_manifest_*.json` | current runtime capability manifest builder when present | report-contract validation / bundle validation | `schema_version`, `kind`, `generated_at`, `repo_root`, capability/tool entries, `warnings`, `errors` | Capability and guardrail context for broker/tool execution. Historical builder names must be checked against current code. |
| `file_line_limit_report.json` | `Tools/validation/check_file_line_limits.py` | self-report plus JSON parseability | `schema_version`, `kind=file_line_limit_report`, `max_lines`, `checked_file_count`, `violation_count`, `violations`, `errors`, `passed` | Report-only line-budget evidence. Does not rewrite, split, delete or apply patches. |
| `full0to10_final_tool_product_manifest.json` | `Tools/ai/full0to10_final_product/*` | report-contract validation / future focused validator | `kind=full0to10_final_tool_product_manifest`, `passed`, `request`, `outputs`, `evidence`, `readiness`, `run_product_evidence`, component reports, `errors`, `warnings` | Product/evidence/readiness package. When run reports/artifacts are supplied, it indexes active mesh/telemetry/patch-plan product evidence. |
| `full_toolbox_run_telemetry_summary_*.json` | `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | report-contract validation / bundle validation | `schema_version`, `kind`, `generated_at`, `repo_root`, `gpu_npu`, `provider`, `runtime_tools`, `patch_plan`, `guardrails`, `warnings`, `errors` | Production summary that explains provider, GPU/NPU, broker, patch-plan and source-write state. |
| `shared_toolbox_ai_to_ai_bundle_*.json` | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | bundle/final-summary validation | `schema_version`, `kind`, `generated_at`, `repo_root`, `evidence`, `telemetry`, `capabilities`, `recommendations`, `patch_plan`, `provider_diagnostics`, `guardrails` | Production AI-to-AI handoff. Must group evidence, patch plan, telemetry and capability references. |
| `shared_toolbox_ai_to_ai_final_summary_*.json` | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | final-summary validation | `passed`, `patch_plan_summary_seen`, `patch_plan_count`, `provider_advisory_state`, `provider_failure_detected`, `deterministic_recovery_used`, `provider_failure_reasons`, `degraded_provider_components`, `patch_application_performed`, `source_writes_performed` | Compact state used by next AI/operator to avoid opening full bundles first. |
| `*selected_chunks*.json` | `Tools/ai/select_semantic_code_chunks.py` | `Tools/validation/check_selected_semantic_chunks.py` | `schema_version`, `kind`, `selected_count`, `max_chunks`, `total_selected_chars`, `provider_execution_performed`, `source_writes_performed`, `selected_chunks` | Bounded focused context selected from semantic chunks; not a patch or provider execution claim. |
| `selective_execution_plan.json` | `Tools/ai/build_selective_execution_plan.py` | `Tools/validation/check_selective_execution_plan.py` | `schema_version`, `kind`, `apply_mode`, `provider_execution_performed`, `recommended_validators`, `recommended_patch_specs`, `next_command_set`, optional telemetry/capability summary fields | Report-only recommendation layer; does not run providers or apply patches. Run-unica-derived recommendations require companion telemetry/capability context. |
| `ai_workload_quality_lane_routing.json` | `Tools/ai/build_workload_quality_lane_routing.py` | summarized in GitHub evidence/bundle validators | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `primary_advisory_provider`, `policy`, `mode`, `routing` | Preserves Ollama/GPU as the quality-gated primary advisory lane; excludes unusable output from advisory context. |
| `npu_decode_smoke_diagnostic.json` | `Tools/ai/run_npu_decode_smoke_diagnostic.py` | summarized in GitHub evidence/bundle validators | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `policy`, `mode`, `provider`, `checks` | Explicit OpenVINO/NPU probe/guardrail/decode diagnostic; passing smoke is not NPU advisory promotion. |
| `*_evidence.json` | `Tools/ai/build_github_evidence_bundle.py` | `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_reports`, `reports`, `decision` | Compact Git-trackable evidence for GitHub-only agents; full local `output/` remains ignored. When from run unica, include telemetry/capability companion artifacts. |
| `*proposals.json` | `Tools/ai/build_repository_change_proposals.py` | `Tools/validation/check_repository_change_proposals.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `profile`, `apply_mode`, `reports_read`, `proposals` | Manual-review proposal report with `suggestion_outputs` descriptors. Run-unica-derived proposals need telemetry/capability context. |
| `proposal_patch_specs*_manifest.json` | `Tools/ai/build_patch_specs_from_proposals.py` | `Tools/validation/check_patch_spec_drafts.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_proposal_report`, `apply_mode`, `draft_status`, `specs` | Inert draft patch-spec manifest under `output/patch_specs/`; no provider execution, no queue write and no concrete replacements. |
| `ai_context_pack*.json` | `Tools/ai/build_ai_context_pack.py` | `Tools/validation/check_ai_context_pack_contract.py` | `schema_version`, `kind`, `profile`, `apply_mode`, `provider_execution_performed`, `validation_commands`, `stop_conditions`, `files` | Local task-scoped context under ignored `output/ai_context_packs/`; no provider execution and no source writes. |
| `generated_python_policy.json` | `Tools/validation/check_generated_python_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Generic generated Python layer. |
| `generated_artifact_path_policy.json` | `Tools/validation/check_generated_artifact_path_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `path_results`, optional path-length limits | Destination-policy and push-safe bundle-name layer. |
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
SQLite DB files under output/** are local/private and non-commit-ready
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
- Do not treat run-unica evidence as complete without telemetry/capability/final summary and relevant heap/exchange/discovery/index/CSV/file-line surfaces.
- Do not treat patch-plan or patch-spec artifacts as complete if their producing run state is unknown.
- Do not treat quality/product/readiness artifacts as provider runtime proof when their safety flags say otherwise.
- Do not treat local output SQLite DB writes as source writes, and do not commit generated DB files.
- Do not treat large Markdown, file existence, dry-run matrix success, provider report existence or NPU smoke success as proof of run-unica completion.
- Do not treat metadata-only patch specs as concrete product.
- Treat limitations as backlog to overcome, not as static reasons to skip current tools.

## GitHub-only limit

GitHub-only agents may update schema notes and gap indexes, but must not claim validation against local `output/` artifacts unless logs or report files are available in the repository or attached to the task.

Required marker for GitHub-only schema/report PRs:

```text
Local workstation validation pending.
```
