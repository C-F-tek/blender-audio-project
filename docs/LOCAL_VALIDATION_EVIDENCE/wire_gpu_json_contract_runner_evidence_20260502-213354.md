# Local Validation Evidence Bundle

- Generated at: `2026-05-02T21:34:19`
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

### `output/validation/python_syntax_wire_gpu_json_contract_runner_20260502-213354.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/validation_report_contract_wire_gpu_json_contract_runner_20260502-213354.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `False`
- Errors: `['output/validation/gpu_planner_json_contract_runner_wiring_smoke_20260502-213354.json: missing required field: repo_root', 'output/validation/gpu_planner_json_contract_smoke_20260502-204056.json: missing required field: repo_root', 'output/validation/gpu_planner_json_contract_smoke_20260502-204231.json: missing required field: repo_root', 'output/validation/gpu_planner_json_contract_smoke_20260502-204345.json: missing required field: repo_root', 'output/validation/gpu_planner_json_contract_smoke_20260502-204507.json: missing required field: repo_root', 'output/validation/gpu_planner_json_contract_smoke_20260502-210841.json: missing required field: repo_root', 'output/validation/gpu_planner_json_contract_smoke_wire_runner_20260502-213129.json: missing required field: repo_root', 'output/validation/gpu_planner_json_contract_smoke_wire_runner_20260502-213308.json: missing required field: repo_root', 'output/validation/gpu_planner_json_contract_smoke_wire_runner_20260502-213354.json: missing required field: repo_root']`

### `output/validation/gpu_planner_json_contract_smoke_wire_runner_20260502-213354.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/gpu_planner_json_contract_runner_wiring_smoke_20260502-213354.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_runner_wiring_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Artifact manifest

- `output/validation/python_syntax_wire_gpu_json_contract_runner_20260502-213354.json` exists=`True` size=`32226` suffix=`.json` preview_chars=`1500`
- `output/validation/validation_report_contract_wire_gpu_json_contract_runner_20260502-213354.json` exists=`True` size=`44973` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_wire_runner_20260502-213354.json` exists=`True` size=`3635` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_runner_wiring_smoke_20260502-213354.json` exists=`True` size=`2621` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/validation/gpu_planner_json_contract_smoke_wire_runner_20260502-213354.md`

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

### `output/validation/gpu_planner_json_contract_runner_wiring_smoke_20260502-213354.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `879`
- SHA-256: `fb2e57644d8c1c4c67d4f7da3105da6c876b02a02eb62352087d7427801d1183`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Runner Wiring Smoke

- Passed: `True`
- Case count: `4`
- Failed case count: `0`
- Aggregate reason: `context_echo_detected`
- Context echo detected count: `1`
- JSON parse error count: `1`
- Model output schema mismatch count: `2`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## `context_echo`

- Passed: `True`
- Expected: `context_echo_detected`
- Actual: `context_echo_detected`

## `malformed_json`

- Passed: `True`
- Expected: `json_parse_failure`
- Actual: `json_parse_failure`

## `schema_mismatch`

- Passed: `True`
- Expected: `model_output_schema_mismatch`
- Actual: `model_output_schema_mismatch`

## `evidence_ready_empty`

- Passed: `True`
- Expected: `evidence_ready_but_no_gpu_plan`
- Actual: `evidence_ready_but_no_gpu_plan`


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
