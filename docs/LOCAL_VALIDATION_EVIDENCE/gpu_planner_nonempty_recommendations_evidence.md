# Local Validation Evidence Bundle

- Generated at: `2026-05-01T21:25:59`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`

## Reports

### `output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet`
- Passed: `True`
- Ollama: `{'used': False, 'model': None, 'error': '', 'text_preview': ''}`

### `output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

### `output/patch_specs/agent_review_patch_plan.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan`
- Passed: `True`
- Provider execution performed: `False`

### `output/validation/agent_review_patch_plan_full_validation.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan_full_validation`
- Passed: `False`
- Provider execution performed: `False`
- Errors: `["git_diff_check returned 2: warning: in the working copy of 'Tools/validation/README.md', CRLF will be replaced by LF the next time Git touches it\nwarning: in the working copy of 'docs/JSON_SCHEMAS.md', CRLF will be replaced by LF the next time Git touches it\nwarning: in the working copy of 'docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json', CRLF will be replaced by LF the next time Git touches it\nwarning: in the working copy of 'docs/LOCAL_VALIDATION_EVIDENCE/agent_review...[truncated]"]`

### `output/validation/agent_review_patch_plan_smoke.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan_smoke`
- Passed: `True`
- Provider execution performed: `False`

### `output/validation/validation_report_contract.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `validation_report_contract`
- Passed: `True`

### `output/ai_pipeline/repository_change_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

### `output/ai_pipeline/agent_gpu_npu_parallel_orchestrator_live.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`

### `output/ai_pipeline/agent_gpu_deep_planning_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`

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
