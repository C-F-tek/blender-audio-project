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
| provider request/result envelope JSON | Planned or future provider exchange envelopes | partial NPU helper contract only; provider execution adapters remain future work |
| provider preflight report JSON | Provider readiness metadata before execution | normalized by NPU provider helper; does not imply provider execution |
| migration readiness report JSON | Gate report before runtime wiring | partial NPU helper contract only |
| runtime output manifest JSON | Planned or observed runtime output list | helper exists for additive observability; runtime emission is future work |
| patch task packet JSON | Patch or service packet for AI workflows | not fully specified |
| project manifest JSON | File index or project code manifest | present in AI index areas |
| AI dry-run matrix report JSON | Machine-readable dry-run matrix result | contract validator exists |
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
Required decision fields:
ollama_gpu_primary_advisory, npu_excluded_when_unusable, provider_execution_seen
Optional provider decision fields:
npu_decode_smoke_passed
Required report summary fields:
path, exists, json_ok, kind, passed, summary
Current validator:
Tools/validation/check_github_evidence_bundle.py
Notes:
Historical bundles that predate `npu_decode_smoke_passed` should warn instead of failing. Unknown future report kinds remain accepted when the common summary envelope is intact.
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

## Report / artifact contract gap index

| Report / artifact | Typical path | Producer | Current validator | Current required fields | Missing checks / notes |
|---|---|---|---|---|---|
| AI dry-run matrix report | `output/ai_pipeline/dry_run_matrix_report.json` | `Tools/ai/run_pipeline_dry_run_matrix.py` | `Tools/validation/check_ai_dry_run_matrix_contract.py` | `schema_version`, `repo_root`, `output_dir`, `case_count`, `passed`, `results` | Future additive checks should remain warning-first until local samples are reviewed. |
| Individual AI pipeline dry-run report | `output/ai_pipeline/dry_run_matrix/<case>/ai_pipeline_dry_run_report.json` | `Tools/ai/run_parallel_artifact_pipeline.py` through matrix cases | `Tools/validation/check_ai_pipeline_report_contract.py`; also invoked by `check_ai_dry_run_matrix_contract.py` for referenced case reports | schema-v6 root fields plus `summary`, `schedule`, `lanes`, `agent_state_packet`, `steps`, `post_run_expected_outputs` | Unknown future fields remain accepted; `--require-dry-run` enforces `dry_run=true` and planned-only steps for dry-run reports. |
| AI workload quality lane routing report | `output/validation/ai_workload_quality_lane_routing.json` | `Tools/ai/build_workload_quality_lane_routing.py` | `Tools/validation/check_github_evidence_bundle.py` for Git-tracked summarized copies | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `primary_advisory_provider`, `policy`, `mode`, `routing` | Direct raw-output validator remains future work; evidence copies preserve the current provider-lane decision. |
| NPU decode quality remediation report | `output/validation/npu_decode_quality_remediation.json` | `Tools/validation/check_npu_decode_quality_remediation.py` | `Tools/validation/check_github_evidence_bundle.py` for Git-tracked summarized copies | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `policy`, `mode`, `checks` | Report-only; must not promote unusable NPU workload output to advisory context. |
| NPU decode smoke diagnostic report | `output/validation/npu_decode_smoke_diagnostic.json` | `Tools/ai/run_npu_decode_smoke_diagnostic.py` | `Tools/validation/check_github_evidence_bundle.py` for Git-tracked summarized copies | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `policy`, `mode`, `provider`, `checks` | Explicit NPU diagnostic only; passing smoke does not make OpenVINO/NPU the primary advisory lane. |
| GitHub validation evidence bundle | `docs/LOCAL_VALIDATION_EVIDENCE/*_evidence.json` | `Tools/ai/build_github_evidence_bundle.py` | `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_reports`, `reports`, `decision`; each report has `path`, `exists`, `json_ok`, `kind`, `passed`, `summary` | Compact Git-trackable proof for GitHub-only agents; older bundles may warn for missing optional provider decision fields. |
| Repository change proposal report | `output/ai_pipeline/*proposals.json`, `output/ai_packets/*proposals.json` | `Tools/ai/build_repository_change_proposals.py` | `Tools/validation/check_repository_change_proposals.py` | root report fields plus per-proposal `id`, `priority`, `area`, `title`, `target_files`, `patch_sketch`, `validation_commands`, `stop_conditions`, `suggestion_outputs` | Advisory manual-review suggestions for code/MD/JSON/PowerShell targets; no auto-apply. |
| NPU helper module smoke report | `output/validation/npu_pipeline_modules.json` | `Tools/validation/check_npu_pipeline_modules.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | Contract is helper-focused and provider-free; do not use it as provider execution proof. |
| NPU helper unit-test report | `output/validation/npu_pipeline_helper_tests.json` | `Tools/validation/check_npu_pipeline_helper_tests.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks.tests_run`, `checks.error_count`, `checks.failure_count` | Wraps deterministic `unittest`; no Blender/NPU/Ollama/provider execution. |
| NPU helper docs report | `output/validation/npu_pipeline_docs.json` | `Tools/validation/check_npu_pipeline_docs.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | Checks `Tools/npu/pipeline/README.md` against expected helper modules/terms. |
| NPU runtime output manifest | future `output/validation/npu_runtime_output_manifest.json` or runtime-specific path | future runtime/reporting phase using `Tools/npu/pipeline/reports.py` | helper unit tests and smoke check currently cover construction only | `schema_version`, `kind`, `repo_root`, `provider_execution_performed`, `output_count`, `blocked_count`, `passed`, `errors`, `warnings`, `outputs` | Helper exists for additive observability; current phase does not emit it from runtime. |
| Generated artifact path policy report | `output/validation/generated_artifact_path_policy.json` | `Tools/validation/check_generated_artifact_path_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `path_count`, `path_results` | Review common validator report fields with TD-015. |
| Generated Python policy report | `output/validation/generated_python_policy.json` | `Tools/validation/check_generated_python_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Document future adapter composition in a separate template. |
| Generated Blender script policy report | `output/validation/generated_blender_script_policy.json` | `Tools/validation/check_generated_blender_script_policy.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `rules`, `sample_results` | Blender-specific; must not become the generic policy boundary. |
| Agent memory policy report | `output/validation/agent_memory_policy.json` | `Tools/validation/check_agent_memory_policy.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `passed`, policy-specific result fields | Local SQLite inspection requires workstation access. |
| Python syntax report | `output/validation/python_syntax.json` | `Tools/validation/check_python_syntax.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `checked_count`, `failed_count`, `passed`, `results` | Does not currently expose `errors` at root; evaluate in validator report consistency review. |
| Package structure report | `output/validation/package_structure.json` | `Tools/validation/check_package_structure.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `scripting_root`, `package_count`, `warning_count`, `passed`, `packages` | Does not currently expose `errors` at root; warnings are package-level. |
| JSON artifact report | `output/validation/json_artifacts.json` | `Tools/validation/check_json_artifacts.py` | self-report plus JSON parseability | `schema_version`, `repo_root`, `checked_count`, `skipped_count`, `failed_count`, `passed`, `results` | Does not currently expose `errors` at root; failures live in `results`. |
| NPU implementation draft fixture/contract | in-memory fixture or generated artifact | `Tools/npu/pipeline/fixtures.py`, NPU pipeline runtime | `Tools/npu/pipeline/validators.py`; exercised by NPU helper validators | `implementation_kind`, `safety`, `reference_files`, `proposed_files`, `implementation_plan` | Current validator is permissive and preserves unknown future fields. |
| NPU provider request descriptor | in-memory fixture or future provider adapter payload | `Tools/npu/pipeline/providers.py` | `validate_provider_request()`; exercised by NPU helper validators | `provider`, `model`, `prompt`, `max_tokens` | Descriptor only; current helper validators must not execute provider calls. |
| NPU provider preflight report | `Tools/npu/npu_preflight_report.json` or in-memory normalized report | `Tools/npu/pipeline/providers.py`, runtime wrapper | helper smoke/unit tests | `schema_version`, `kind`, `provider`, `model`, `ready`, `provider_execution_performed`, `runtime`, `errors`, `warnings` | Preflight normalization does not imply provider/model execution. |
| NPU migration readiness report | in-memory report, future output if persisted | `Tools/npu/pipeline/migration_readiness.py` | exercised by NPU helper validators | `schema_version`, `kind`, `target_file`, `allowed_to_modify_runtime`, `ready`, `failed_count`, `checks` | Default readiness blocks unvalidated runtime wiring. |
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
- Keep NPU helper report schemas separate from runtime provider execution schemas.
- Do not use provider preflight or runtime output manifests as proof that a provider/model was executed.

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

1. Validate the common NPU report envelope and runtime-output manifest helpers locally.
2. Keep validating local `output/` report samples on the workstation after report-producer changes.
3. Extend strict report validators only when field meanings are already documented.
4. Continue with domain artifacts such as music summaries and scene specs after report contracts remain stable.
5. Keep unknown future fields accepted unless a validator has a clear reason to reject them.
6. If runtime-output manifest emission is added later, make it additive observability only and do not change output paths or generated file content.
