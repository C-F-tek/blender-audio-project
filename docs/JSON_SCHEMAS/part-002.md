<!-- IA-CARMINE-MD-SPLIT: part -->
# JSON_SCHEMAS — parte 002 di 002

Sorgente indice: [`../JSON_SCHEMAS.md`](../JSON_SCHEMAS.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

### Proposal patch-spec drafts

```text
File pattern:
output/patch_specs/*_manifest.json
output/patch_specs/<basename>/*.json
Producer:
Tools/ai/build_patch_specs_from_proposals.py
Consumer:
Maintainers and future trusted patch builders.
Required manifest fields:
schema_version, kind, generated_at, repo_root, source_proposal_report, output_dir, passed, errors, warnings, provider_execution_performed, apply_mode, draft_status, patch_spec_count, specs
Required spec fields:
version, schema_version, kind, generated_at, source_proposal_report, proposal_id, apply_mode, draft_status, provider_execution_performed, description, operations
Required kind:
proposal_patch_spec_manifest
proposal_patch_spec_draft
Required apply mode:
manual_review_only
Required draft status:
needs_concrete_replacements
Provider semantics:
Draft building does not execute providers. It reads proposal reports produced by earlier explicit workflow steps.
Current validator:
Tools/validation/check_patch_spec_drafts.py
Notes:
Draft specs are inert and must keep `replacements` empty. They must remain outside `patch_specs/inbox/` until a reviewed concrete patch is intentionally prepared and dry-run.
```

### Reviewed patch specs

```text
File pattern:
output/patch_specs/reviewed*.json
output/patch_specs/reviewed*_manifest.json
Producer:
Tools/ai/promote_patch_spec_draft.py
Consumer:
Maintainers and future trusted patch builders.
Required manifest fields:
schema_version, kind, generated_at, repo_root, passed, errors, warnings, provider_execution_performed, apply_mode, review_status, source_draft_spec, source_replacement_plan, reviewed_spec_count, specs
Required spec fields:
version, schema_version, kind, generated_at, source_draft_spec, source_replacement_plan, apply_mode, review_status, provider_execution_performed, description, operations, dry_run
Required kind:
reviewed_patch_spec_manifest
reviewed_patch_spec
Required apply mode:
manual_review_only
Required review status:
dry_run_passed
Provider semantics:
Reviewed spec promotion does not execute providers. It only reads a draft spec and explicit replacement plan.
Current validator:
Tools/validation/check_reviewed_patch_specs.py
Notes:
Reviewed specs contain concrete replacements and must pass dry-run. They still remain outside `patch_specs/inbox/` and are not applied by the promotion or validation tools.
```

### AI context packs

```text
File pattern:
output/ai_context_packs/*.json
docs/LOCAL_VALIDATION_EVIDENCE/*context_pack_evidence.json
Producer:
Tools/ai/build_ai_context_pack.py
Consumer:
Human maintainers, AI coding agents, proposal builders and future selective execution planners.
Required context pack fields:
schema_version, kind, generated_at, repo_root, profile, apply_mode, provider_execution_performed, passed, errors, warnings, validation_commands, stop_conditions, files
Required evidence fields:
schema_version, kind, generated_at, repo_root, profile, source_pack, passed, provider_execution_performed, file_count, included_file_count, required_missing, forbidden_path_count, included_paths, decision
Required kinds:
ai_context_pack
ai_context_pack_evidence
Provider semantics:
Context-pack generation does not execute providers and does not modify source files. It only reads bounded repository files and writes ignored local context plus compact tracked evidence.
Current validator:
Tools/validation/check_ai_context_pack_contract.py
Notes:
Context packs must avoid generated indexes, local output, Ready To Jazz runtime, blender_compat.py and full analysis JSON. The tracked evidence is reviewable on GitHub; the full pack remains local under output/.
```

## Report / artifact contract gap index

| Report / artifact | Typical path | Producer | Current validator | Current required fields | Missing checks / notes |
|---|---|---|---|---|---|
| AI dry-run matrix report | `output/ai_pipeline/dry_run_matrix_report.json` | `Tools/ai/run_pipeline_dry_run_matrix.py` | `Tools/validation/check_ai_dry_run_matrix_contract.py` | `schema_version`, `repo_root`, `output_dir`, `case_count`, `passed`, `results` | Future additive checks should remain warning-first until local samples are reviewed. |
| Individual AI pipeline dry-run report | `output/ai_pipeline/dry_run_matrix/<case>/ai_pipeline_dry_run_report.json` | `Tools/ai/run_parallel_artifact_pipeline.py` through matrix cases | `Tools/validation/check_ai_pipeline_report_contract.py`; also invoked by `check_ai_dry_run_matrix_contract.py` for referenced case reports | schema-v6 root fields plus `summary`, `schedule`, `lanes`, `agent_state_packet`, `steps`, `post_run_expected_outputs` | Unknown future fields remain accepted; `--require-dry-run` enforces `dry_run=true` and planned-only steps for dry-run reports. |
| AI dry-run matrix evidence bundle | `docs/LOCAL_VALIDATION_EVIDENCE/ai_pipeline_dry_run_matrix_evidence.json` | `Tools/ai/build_dry_run_matrix_evidence_bundle.py` | `Tools/validation/check_dry_run_matrix_evidence_bundle.py` | `schema_version`, `kind`, `provider_execution_performed`, `matrix`, `validation_reports`, `case_summary`, `cases`, `decision` | Compact Git-trackable proof that the local matrix ran as dry-run/planned-only with no provider execution claim. |
| Selected semantic chunks | `output/ai_context_packs/*selected_chunks*.json` | `Tools/ai/select_semantic_code_chunks.py` | `Tools/validation/check_selected_semantic_chunks.py` | `schema_version`, `kind`, `selected_count`, `max_chunks`, `total_selected_chars`, `provider_execution_performed`, `source_writes_performed`, `selected_chunks` | Focused context only; compact evidence can be emitted under `docs/LOCAL_VALIDATION_EVIDENCE/`. |
| Selective execution plan | `output/ai_pipeline/selective_execution_plan.json` | `Tools/ai/build_selective_execution_plan.py` | `Tools/validation/check_selective_execution_plan.py` | `schema_version`, `kind`, `apply_mode`, `provider_execution_performed`, `recommended_validators`, `recommended_patch_specs`, `next_command_set` | Report-only next-action recommendations; no provider execution or patch application. |
| AI workload quality lane routing report | `output/validation/ai_workload_quality_lane_routing.json` | `Tools/ai/build_workload_quality_lane_routing.py` | `Tools/validation/check_github_evidence_bundle.py` for Git-tracked summarized copies | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `primary_advisory_provider`, `policy`, `mode`, `routing` | Direct raw-output validator remains future work; evidence copies preserve the current provider-lane decision. |
| NPU decode quality remediation report | `output/validation/npu_decode_quality_remediation.json` | `Tools/validation/check_npu_decode_quality_remediation.py` | `Tools/validation/check_github_evidence_bundle.py` for Git-tracked summarized copies | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `policy`, `mode`, `checks` | Report-only; must not promote unusable NPU workload output to advisory context. |
| NPU decode smoke diagnostic report | `output/validation/npu_decode_smoke_diagnostic.json` | `Tools/ai/run_npu_decode_smoke_diagnostic.py` | `Tools/validation/check_github_evidence_bundle.py` for Git-tracked summarized copies | `schema_version`, `kind`, `passed`, `provider_execution_performed`, `errors`, `warnings`, `policy`, `mode`, `provider`, `checks` | Explicit NPU diagnostic only; passing smoke does not make OpenVINO/NPU the primary advisory lane. |
| GitHub validation evidence bundle | `docs/LOCAL_VALIDATION_EVIDENCE/*_evidence.json` | `Tools/ai/build_github_evidence_bundle.py` | `Tools/validation/check_github_evidence_bundle.py` | `schema_version`, `kind`, `generated_at`, `repo_root`, `source_reports`, `reports`, `decision`; each report has `path`, `exists`, `json_ok`, `kind`, `passed`, `summary` | Compact Git-trackable proof for GitHub-only agents; older bundles may warn for missing optional provider decision fields. |
| Repository change proposal report | `output/ai_pipeline/*proposals.json`, `output/ai_packets/*proposals.json` | `Tools/ai/build_repository_change_proposals.py` | `Tools/validation/check_repository_change_proposals.py` | root report fields plus per-proposal `id`, `priority`, `area`, `title`, `target_files`, `patch_sketch`, `validation_commands`, `stop_conditions`, `suggestion_outputs` | Advisory manual-review suggestions for code/MD/JSON/PowerShell targets; no auto-apply. |
| Full-context golden proposals | `output/ai_pipeline/full_context_golden_proposals.json` | `Tools/ai/build_full_context_golden_proposals.py` | `Tools/validation/check_repository_change_proposals.py`, `Tools/validation/check_full_context_golden_proposals.py` | Generic proposal fields plus required families P1-P6 | Deterministic manual-review-only proposal coverage for controlled complexity escalation. |
| Proposal patch-spec draft manifest/spec | `output/patch_specs/*_manifest.json`, `output/patch_specs/<basename>/*.json` | `Tools/ai/build_patch_specs_from_proposals.py` | `Tools/validation/check_patch_spec_drafts.py` | manifest/spec root fields plus draft `operations` with empty `replacements` | Drafts must not be queued under `patch_specs/inbox/`; use reviewed patch-spec promotion for concrete replacements. |
| Reviewed patch-spec manifest/spec | `output/patch_specs/reviewed*.json`, `output/patch_specs/reviewed*_manifest.json` | `Tools/ai/promote_patch_spec_draft.py` | `Tools/validation/check_reviewed_patch_specs.py` | manifest/spec root fields plus concrete replacements and `dry_run.passed=true` | Apply/queue approval remains future work; reviewed specs must not be auto-applied. |
| NPU helper module smoke report | `output/validation/npu_pipeline_modules.json` | `Tools/validation/check_npu_pipeline_modules.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | Contract is helper-focused and provider-free; do not use it as provider execution proof. |
| NPU helper unit-test report | `output/validation/npu_pipeline_helper_tests.json` | `Tools/validation/check_npu_pipeline_helper_tests.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks.tests_run`, `checks.error_count`, `checks.failure_count` | Wraps deterministic `unittest`; no Blender/NPU/Ollama/provider execution. |
| NPU helper docs report | `output/validation/npu_pipeline_docs.json` | `Tools/validation/check_npu_pipeline_docs.py` | self-report plus JSON parseability | `schema_version`, `kind`, `repo_root`, `passed`, `errors`, `warnings`, `checks` | Checks `Tools/npu/pipeline/README.md` against expected helper modules/terms. |
| AI context pack | `output/ai_context_packs/*.json` | `Tools/ai/build_ai_context_pack.py` | `Tools/validation/check_ai_context_pack_contract.py` | `schema_version`, `kind`, `profile`, `provider_execution_performed`, `validation_commands`, `stop_conditions`, `files` | Local context artifact under ignored `output/`; compact evidence belongs under `docs/LOCAL_VALIDATION_EVIDENCE/`. |
| AI context pack evidence | `docs/LOCAL_VALIDATION_EVIDENCE/*context_pack_evidence.json` | `Tools/ai/build_ai_context_pack.py` | `Tools/validation/check_ai_context_pack_contract.py` | `schema_version`, `kind`, `profile`, `passed`, `provider_execution_performed`, `included_paths`, `decision` | Git-trackable proof that a bounded context pack was built without provider execution or source writes. |
| NPU runtime output manifest | `output/validation/npu_runtime_output_manifest.json` or runtime-specific path | `Tools/npu/build_runtime_output_manifest.py` and future runtime/reporting phases | helper unit tests, NPU module smoke and evidence summary validation | `schema_version`, `kind`, `repo_root`, `provider_execution_performed`, `output_count`, `blocked_count`, `passed`, `errors`, `warnings`, `outputs` | Current local/evidence copies are observability-only and must not be treated as provider execution proof; runtime-native emission remains future work. |
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

## Agent review patch-plan validation bundle

```text
File pattern:
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
Producer:
Tools/validation/run_agent_review_patch_plan_full_validation.py
Consumer:
GitHub-only review agents, manual-review documentation patch tasks and PR summaries.
Required fields:
schema_version, kind, generated_at, repo_root, source_reports, reports, selected_chunks_evidence, decision
Required kind:
github_validation_evidence_bundle
Required source reports:
output/patch_specs/agent_review_patch_plan.json
output/validation/agent_review_patch_plan_smoke.json
output/validation/docs_links.json
output/validation/python_syntax.json
output/validation/validation_report_contract.json
Provider semantics:
The wrapper must keep provider_execution_performed=false and must not run Ollama, OpenVINO, GPU, NPU or Blender.
Patch semantics:
The wrapper must keep patch_application_performed=false. Documentation edits remain manual-review-only.
Notes:
This bundle is task-scoped. For this lane, selected semantic chunk evidence is intentionally disabled unless explicitly requested by a future task.
```

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:START -->

## IA-Carmine patch-plan application notes

This managed block was generated from `output/patch_specs/agent_review_patch_plan.json`.
It records the manual-review patch-plan decisions for this file without applying runtime/provider changes.

### `det_doc_doc_002` — `doc_doc`

- Source: `gpu_recommendation`
- Status: `ready_for_manual_review`
- Risk: `low`
- Target file: `docs/JSON_SCHEMAS.md`
- Manual review required: `True`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the missing terms are already present after refreshing master.
  - Stop if the edit would duplicate large generated artifacts.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:END -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_doc_002:docs-json_schemas.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_doc_002`
- Area: `doc_doc`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/JSON_SCHEMAS.md`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the missing terms are already present after refreshing master.
  - Stop if the edit would duplicate large generated artifacts.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_doc_002:docs-json_schemas.md -->
