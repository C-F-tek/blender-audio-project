# Local Validation Evidence Bundle

- Generated at: `2026-05-02T20:45:49`
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
- `included_artifacts_built`: `True`
- `included_artifact_count`: `2`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/validation/gpu_planner_json_contract_smoke_20260502-204507.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Artifact manifest

- `output/validation/gpu_planner_json_contract_smoke_20260502-204507.json` exists=`True` size=`3635` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/validation/gpu_planner_json_contract_smoke_20260502-204507.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `925`
- SHA-256: `d98845c217da543038e9253b5f6b4df26e2f5337ab6bf4dde9d275b759811061`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Smoke

- Passed: `True`
- Case count: `4`
- Failed case count: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## `valid_recommendation`

- Passed: `True`
- Expected reason: ``
- Reason: ``
- JSON OK: `True`
- Schema OK: `True`
- Context echo detected: `False`

## `context_echo`

- Passed: `True`
- Expected reason: `context_echo_detected`
- Reason: `context_echo_detected`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `True`

## `malformed_json`

- Passed: `True`
- Expected reason: `json_parse_failure`
- Reason: `json_parse_failure`
- JSON OK: `False`
- Schema OK: `False`
- Context echo detected: `False`

## `schema_context_echo`

- Passed: `True`
- Expected reason: `context_echo_detected`
- Reason: `context_echo_detected`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `True`


```

### `docs/LOCAL_AI_TASKS/gpu-planner-json-contract-hardening.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2133`
- SHA-256: `fa9cac6fac90165ecab746698bb0dfd21415428eac8ce99c89bad129289a04b0`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Hardening

## Purpose

This note documents the first hardening layer after PR #111.

The immediate goal is to reduce ambiguous GPU planner failures by classifying model output more precisely before it reaches recommendation merge/filter logic.

## Added helper

```text
Tools/ai/gpu_planner_json_contract.py
```

The helper is report-only and does not run providers.

It validates:

```text
JSON parseability
expected top-level recommendation schema
context echo outputs
recommendation object shape
risk/status enums
target_files, validation_commands and stop_conditions list types
```

## Added smoke

```text
Tools/validation/run_gpu_planner_json_contract_smoke.py
```

Smoke cases:

```text
valid_recommendation -> accepted
context_echo -> classified as context_echo_detected
malformed_json -> classified as json_parse_failure
```

## Why this matters

The project-complete AI-to-AI run showed:

```text
GPU/Ollama provider execution completed
round_count=24
json_parse_error_count=16
repair_attempt_count=18
recommendation_count=0
evidence_ready_for_manual_patch_count=12
empty_recommendations_reason=repair_attempt_failed
```

The included raw preview also showed the model returning a `files` payload with `content_preview` entries instead of the expected recommendation object. That is not only invalid JSON recovery; it is a task-shape failure.

## New classifications

```text
json_parse_failure
context_echo_detected
model_output_schema_mismatch
evidence_ready_but_no_gpu_plan
valid_json_empty_recommendations
```

## Intended integration path

This PR deliberately adds a reusable helper and smoke first.

Next integration step:

```text
replace local duplicated GPU parse/classification code with gpu_planner_json_contract.validate_model_response_contract
```

Target files:

```text
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
```

## Guardrails

```text
no provider/model setting changes
no automatic patch application
no source writes through patch runner
no Blender runtime execution
no raw output/** commit
manual review required
```

```

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
