# Local Validation Evidence Bundle

- Generated at: `2026-05-01T23:27:56`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `False`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `patch_plan_summary_seen`: `True`

## Reports

### `output/patch_specs/agent_review_patch_plan.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `12`
- Patch plan summary count: `12`
- Fallback used: `True`
- Manual review required: `True`

### `output/patch_specs/agent_review_patch_plan.md`

- Exists: `True`
- JSON OK: `False`
- Kind: `None`
- Passed: `None`

### `output/validation/agent_review_patch_plan_smoke_full_after_fallback_fix.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `12`

### `output/validation/validation_report_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

## Patch plan summary

### `output/patch_specs/agent_review_patch_plan.json`

- Patch plan count: `12`
- Fallback used: `True`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

#### fallback_doc_code_001 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/config_model.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.

#### fallback_doc_code_002 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/diagnostics.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.

#### fallback_doc_code_003 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

#### fallback_doc_code_004 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

#### fallback_doc_code_005 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

#### fallback_doc_code_006 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

#### fallback_doc_code_007 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code-quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code-quality.yml`.

#### fallback_doc_code_008 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code_quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code_quality.yml`.

#### fallback_doc_code_009 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/ci.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/ci.yml`.

#### fallback_doc_doc_001 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `provider_execution_performed`, `patch_application_performed`, `manual_review_only`, `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

#### fallback_doc_doc_002 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['docs/JSON_SCHEMAS.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

#### fallback_doc_doc_003 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: `['Tools/validation/README.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.


## Artifact manifest

- `output/patch_specs/agent_review_patch_plan.json` exists=`True` size=`54841` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/agent_review_patch_plan.md` exists=`True` size=`7059` suffix=`.md` preview_chars=`1500`
- `output/validation/agent_review_patch_plan_smoke_full_after_fallback_fix.json` exists=`True` size=`1227` suffix=`.json` preview_chars=`1203`
- `output/validation/validation_report_contract.json` exists=`True` size=`25662` suffix=`.json` preview_chars=`1500`

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
