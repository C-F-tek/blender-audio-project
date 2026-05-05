<!-- IA-CARMINE-MD-SPLIT: part -->
# JSON_SCHEMAS — parte 001 di 002

Sorgente indice: [`../JSON_SCHEMAS.md`](../JSON_SCHEMAS.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

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
| selected semantic chunks JSON | Bounded focused source/docs context selected from semantic chunk index | validator exists |
| selected semantic chunks evidence JSON | Compact tracked proof for selected focused context | validator exists |
| AI context pack JSON | Task-scoped source/docs context and validation plan for AI/human continuation | validator exists |
| AI context pack evidence JSON | Compact tracked summary of a generated context pack | validator exists |
| selective execution plan JSON | Report-only recommendation plan for validators and patch-spec candidates | validator exists |
| full-context golden proposal JSON | Deterministic manual-review-only proposal families P1-P6 | validator exists |
| proposal patch-spec draft JSON | Reviewable shell for future deterministic patch specs | validator exists |
| reviewed patch-spec JSON | Dry-run-proven concrete patch candidate | validator exists |
| provider request/result envelope JSON | Planned or future provider exchange envelopes | partial NPU helper contract only; provider execution adapters remain future work |
| provider preflight report JSON | Provider readiness metadata before execution | normalized by NPU provider helper; does not imply provider execution |
| migration readiness report JSON | Gate report before runtime wiring | partial NPU helper contract only |
| runtime output manifest JSON | Planned or observed runtime output list | helper exists for additive observability; runtime emission is future work |
| patch task packet JSON | Patch or service packet for AI workflows | not fully specified |
| project manifest JSON | File index or project code manifest | present in AI index areas |
| AI dry-run matrix report JSON | Machine-readable dry-run matrix result | contract validator exists |
| AI dry-run matrix evidence JSON | Compact Git-trackable summary of a local dry-run matrix run | validator exists |
| NPU helper validation report JSON | Machine-readable NPU helper validation result | focused validators exist |
| validator report JSON | Machine-readable validation result | common fields under review and helper envelope exists |
| generated artifact path report JSON | Destination-policy result for generated files | validator exists |

## Common NPU validation report envelope

New NPU helper validators and smoke checks should prefer this common root envelope where practical:

```text
schema_version
kind
repo_root
passed
errors
warnings
checks
```

Helper functions:

```text
Tools/npu/pipeline/reports.py
  build_validation_report()
  validation_report_has_common_keys()
```

The helper does not force older repository validators to change shape immediately. It provides a consistent target for new NPU/backend report contracts.

## AI orchestration report contracts

These contracts describe report artifacts used by the local AI/provider orchestration workflow. They are not Blender runtime schemas and must not be used to change prompt prose, model settings, provider execution behavior or generated analysis JSON.

### AI workload report quality

```text
File pattern:
output/validation/ai_workload_report_quality.json
Producer:
Tools/validation/check_ai_workload_report_quality.py
Consumer:
Tools/ai/workload_quality.py
Tools/ai/build_workload_quality_lane_routing.py
Tools/ai/suggest_repository_updates.py
Tools/ai/build_repository_change_proposals.py
Tools/ai/build_github_evidence_bundle.py
Required fields:
schema_version, kind, repo_root, passed, errors, warnings, provider_execution_performed, source_writes_performed, policy, mode, usable_lanes, unusable_lanes, decision, checks
Required kind:
ai_workload_report_quality
Required policy:
usable_text_lanes_only_for_advisory_context
Provider semantics:
This report is built from already-generated workload reports and must keep provider_execution_performed=false.
Notes:
Each checks.results entry exposes path, lane, provider, compute_lane, exists, usable, classification, advisory_use, provider_execution_performed, errors, warnings and metrics.
Ollama/GPU/CUDA can be primary advisory only when classified usable_text.
NPU/OpenVINO reports classified unusable_output are excluded from advisory context.
```

### NPU review metadata

```text
File pattern:
output/validation/npu_review_metadata.json
Producer:
Tools/npu/run_npu_review.py --metadata-out
Consumer:
validation report contract checks, workload-gate reviewers and local AI handoffs.
Required fields:
schema_version, kind, repo_root, passed, errors, warnings, engine, provider, device, metadata_only, provider_execution_performed, generated_output_written, source_writes_performed, patch_application_performed, advisory_role, quality_gate_required_before_advisory_use
Required kind:
npu_review_metadata
Provider semantics:
metadata_only=true means no provider was loaded, no generated review text was written and provider_execution_performed=false.
Notes:
A metadata sidecar does not make NPU advisory. It records that quality_gate_required_before_advisory_use is true.
```

### AI workload quality lane routing

```text
File pattern:
output/validation/ai_workload_quality_lane_routing.json
Producer:
Tools/ai/build_workload_quality_lane_routing.py
Consumer:
Tools/ai/suggest_repository_updates.py
Tools/ai/build_github_evidence_bundle.py
Required fields:
schema_version, kind, passed, provider_execution_performed, errors, warnings, primary_advisory_provider, policy, mode, routing
Required kind:
ai_workload_quality_lane_routing
Provider semantics:
Ollama/GPU/CUDA remains the primary advisory provider when quality routing allows it.
OpenVINO/NPU reports may be excluded from advisory context when workload quality is unusable.
provider_execution_performed=false means this report selected lanes from existing quality reports and did not execute a provider.
Current validator:
Tools/validation/check_github_evidence_bundle.py validates the summarized copy stored in GitHub evidence bundles.
Missing checks:
Direct validation of the raw output/validation report can be added after more local samples are reviewed.
```

### NPU decode quality remediation

```text
File pattern:
output/validation/npu_decode_quality_remediation.json
Producer:
Tools/validation/check_npu_decode_quality_remediation.py
Consumer:
Tools/ai/build_github_evidence_bundle.py
Required fields:
schema_version, kind, passed, provider_execution_performed, errors, warnings, policy, mode, checks
Required kind:
npu_decode_quality_remediation
Provider semantics:
Report-only remediation planning must not execute OpenVINO/NPU and must not promote NPU output to advisory context.
Current validator:
Tools/validation/check_github_evidence_bundle.py validates the summarized copy stored in GitHub evidence bundles.
Missing checks:
Direct raw-report validation should remain warning-first until representative workstation reports are stable.
```

### NPU decode smoke diagnostic

```text
File pattern:
output/validation/npu_decode_smoke_diagnostic.json
Producer:
Tools/ai/run_npu_decode_smoke_diagnostic.py
Consumer:
Tools/ai/build_github_evidence_bundle.py
Required fields:
schema_version, kind, passed, provider_execution_performed, errors, warnings, policy, mode, provider, checks
Required kind:
npu_decode_smoke_diagnostic
Provider semantics:
This is an explicit OpenVINO/NPU probe/guardrail/decode diagnostic. Passing it does not make NPU a primary advisory provider.
Current validator:
Tools/validation/check_github_evidence_bundle.py validates the summarized copy stored in GitHub evidence bundles.
Missing checks:
Future direct checks can validate `provider=openvino_npu` and `device=NPU` when local samples are present.
```

### GitHub validation evidence bundle

```text
File pattern:
docs/LOCAL_VALIDATION_EVIDENCE/*_evidence.json
Producer:
Tools/ai/build_github_evidence_bundle.py
Consumer:
GitHub-only review agents, local validation handoffs and PR summaries.
Required fields:
schema_version, kind, generated_at, repo_root, source_reports, reports, decision
Required kind:
github_validation_evidence_bundle
Optional current fields:
artifact_manifest
Required decision fields:
ollama_gpu_primary_advisory, npu_excluded_when_unusable, provider_execution_seen
Optional provider decision fields:
npu_decode_smoke_passed
Optional current decision fields:
artifact_manifest_built, patch_plan_summary_seen
Required report summary fields:
path, exists, json_ok, kind, passed, summary
Optional report summary fields:
patch_plan_summary
Current validator:
Tools/validation/check_github_evidence_bundle.py
Notes:
Historical bundles that predate `npu_decode_smoke_passed`, `artifact_manifest` or `patch_plan_summary` should warn instead of failing. Unknown future report kinds remain accepted when the common summary envelope is intact.
```

### AI dry-run matrix evidence bundle

```text
File pattern:
docs/LOCAL_VALIDATION_EVIDENCE/ai_pipeline_dry_run_matrix_evidence.json
Producer:
Tools/ai/build_dry_run_matrix_evidence_bundle.py
Consumer:
GitHub-only review agents, local validation handoffs and future selective execution planners.
Required fields:
schema_version, kind, generated_at, repo_root, source_matrix_report, source_validation_reports, provider_execution_performed, passed, errors, warnings, matrix, validation_reports, case_summary, cases, decision
Required kind:
dry_run_matrix_evidence_bundle
Required decision fields:
matrix_passed, all_validation_reports_passed, all_case_reports_present, all_cases_dry_run, all_steps_planned_only, provider_execution_seen, gpu_npu_workloads_executed, parallel_execution_seen, repeat_cases_seen
Provider semantics:
This evidence summarizes dry-run planning only. It must keep provider_execution_performed=false and must not be used as proof that GPU/NPU workloads executed.
Current validator:
Tools/validation/check_dry_run_matrix_evidence_bundle.py
Notes:
The full matrix report remains under ignored output. The evidence records enough per-case status to prove dry-run-only, planned-only behavior without committing long stdout/stderr tails.
```

### Repository change proposals

```text
File pattern:
output/ai_pipeline/*proposals.json
output/ai_packets/*proposals.json
Producer:
Tools/ai/build_repository_change_proposals.py
Consumer:
Maintainer review, future trusted patch builders and GitHub-only agents.
Required fields:
schema_version, kind, generated_at, repo_root, profile, passed, errors, warnings, apply_mode, reports_read, proposals
Required kind:
repository_change_proposals
Required apply mode:
manual_review_only
Required proposal fields:
id, priority, area, title, rationale, target_files, change_type, apply_mode, patch_sketch, validation_commands, stop_conditions
Suggestion descriptor fields:
path, artifact_kind, operation, content_status, write_policy
Supported artifact kinds:
python_code, markdown, json, powershell, workflow_yaml, path_group, text_or_config
Provider semantics:
Proposal building does not execute providers. Provider/GPU/NPU evidence is read only from reports that were produced by explicit workflow steps.
Current validator:
Tools/validation/check_repository_change_proposals.py
Notes:
Suggestion descriptors describe code/MD/JSON/PowerShell targets for future manual patches. They are not source writes and must not auto-apply.
```

### Selected semantic chunks

```text
File pattern:
output/ai_context_packs/*selected_chunks*.json
docs/LOCAL_VALIDATION_EVIDENCE/*selected_chunks*_evidence.json
Producer:
Tools/ai/select_semantic_code_chunks.py
Tools/validation/check_selected_semantic_chunks.py for compact evidence
Consumer:
Local AI task adapter, context-pack builder, advisory packet builder, GitHub-only reviewers.
Required selected-bundle fields:
schema_version, kind, generated_at, repo_root, source_manifest, query, selected_count, max_chunks, max_total_chars, total_selected_chars, provider_execution_performed, source_writes_performed, selected_chunks
Required evidence fields:
schema_version, kind, generated_at, repo_root, source_bundle, passed, errors, warnings, selected_count, total_selected_chars, decision
Required kind:
semantic_code_chunk_selection
selected_semantic_chunks_evidence
Provider semantics:
Selection and selected-chunks validation do not execute providers and do not write source files.
Current validator:
Tools/validation/check_selected_semantic_chunks.py
Notes:
Selected chunks are bounded context, not patch instructions. Compact evidence may be committed for GitHub review; full selected context remains under ignored output paths.
```

### Selective execution plans

```text
File pattern:
output/ai_pipeline/selective_execution_plan.json
Producer:
Tools/ai/build_selective_execution_plan.py
Consumer:
Human maintainers, GitHub-only agents and future local runners.
Required fields:
schema_version, kind, generated_at, repo_root, apply_mode, provider_execution_performed, patch_application_performed, inputs, provider_evidence_summary, dry_run_summary, validation_health, recommended_validators, recommended_patch_specs, blocked_actions, local_only_actions_for_carmine, github_only_actions_for_ai, risks, next_command_set, passed, errors, warnings
Required kind:
selective_execution_plan
Provider semantics:
The planner does not execute providers. It may recommend explicit local GPU/NPU evidence commands for Carmine.
Current validator:
Tools/validation/check_selective_execution_plan.py
Notes:
Recommendations are report-only and should distinguish GitHub-only work from local-only work.
```

### Full-context golden proposals

```text
File pattern:
output/ai_pipeline/full_context_golden_proposals.json
Producer:
Tools/ai/build_full_context_golden_proposals.py
Consumer:
Maintainers, proposal validators and future patch-spec promotion tools.
Required fields:
Same generic `repository_change_proposals` root/proposal fields plus coverage of required proposal families P1-P6.
Required kind:
repository_change_proposals
Required proposal families:
P1 adapter manifest validator
P2 reusable enrichment-plan helper
P3 full-context golden path docs contract
P4 optional wrapper preset flag
P5 selected-chunks evidence standard validation block
P6 NPU knowledge-broker / context-oracle prototype
Provider semantics:
The generator is deterministic and report-only. It does not execute providers, apply patches or mutate source.
Current validators:
Tools/validation/check_repository_change_proposals.py
Tools/validation/check_full_context_golden_proposals.py
Notes:
The full-context validator catches semantic insufficiency even when the generic proposal schema passes.
```
