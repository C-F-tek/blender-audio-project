# Local Validation Evidence Bundle

- Generated at: `2026-05-01T12:07:17`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `True`
- `npu_excluded_when_unusable`: `True`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `True`

## Reports

### `output/validation/ai_workload_report_quality.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_workload_report_quality`
- Passed: `False`
- Usable lanes: `['ollama']`
- Unusable lanes: `['npu']`
- Errors: `['npu: alphabetic character ratio is too low', 'npu: word count is too low', 'npu: report appears numeric/hex-like rather than natural language']`
- Warnings: `['npu: report lacks Markdown headings and has few sentence markers']`

### `output/validation/ai_workload_quality_lane_routing.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_workload_quality_lane_routing`
- Passed: `True`
- Provider execution performed: `False`
- Primary advisory provider: `{'provider': 'ollama', 'compute_lane': 'gpu_cuda', 'role': 'primary_advisory', 'execution_mode': 'explicit_only', 'enabled_by_flag': '--use-primary-advisory-provider / -UsePrimaryAdvisoryProvider', 'provider_execution_performed': False}`
- Routing: `{'advisory_lanes': ['ollama'], 'excluded_advisory_lanes': ['npu'], 'primary_advisory_provider': {'provider': 'ollama', 'compute_lane': 'gpu_cuda', 'role': 'primary_advisory', 'execution_mode': 'explicit_only', 'enabled_by_flag': '--use-primary-advisory-provider / -UsePrimaryAdvisoryProvider', 'provider_execution_performed': False}, 'trusted_context_files': [{'path': 'docs/LOCAL_AI_TASKS/enrich-local-ai-memory-chunks-context-wrapper.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'indexAI/code_chunks/semantic_code_chunks_manifest.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_context_packs/enrichment_real_core_ai_backend.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_context_packs/enrichment_real_core_ai_backend.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/local_ai_runs/enrichment_real_run/pipeline/agent_state/enrichment_real_agent_state.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/local_ai_runs/enrichment_real_run/pipeline/agent_state/enrichment_real_agent_state.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}], 'excluded_context_files': []}`

### `output/validation/npu_decode_quality_remediation.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_decode_quality_remediation`
- Passed: `True`
- Provider execution performed: `False`

### `output/validation/npu_decode_smoke_diagnostic.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_decode_smoke_diagnostic`
- Passed: `True`
- Provider execution performed: `True`
- Python executable: `C:\Users\carmi\blender\venvs\blender-npu-ai\Scripts\python.exe`

### `output/validation/local_provider_probe.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `local_provider_probe`
- Passed: `True`
- Provider execution performed: `True`

### `output/validation/npu_runtime_output_manifest.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_runtime_output_manifest`
- Passed: `True`
- Provider execution performed: `False`

### `output/validation/provider_result_report.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `provider_result_report`
- Passed: `True`
- Provider execution performed: `False`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
