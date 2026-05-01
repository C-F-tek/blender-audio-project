# Local Validation Evidence Bundle

- Generated at: `2026-05-01T20:07:55`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `False`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`

## Reports

### `output/patch_specs/agent_review_patch_plan.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan`
- Passed: `True`
- Provider execution performed: `False`

### `output/validation/agent_review_patch_plan_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan_smoke`
- Passed: `True`
- Provider execution performed: `False`

### `output/validation/docs_links.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `docs_links`
- Passed: `True`

### `output/validation/python_syntax.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/validation_report_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

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
