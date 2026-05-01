# Local Validation Evidence Bundle

- Generated at: `2026-05-01T00:40:44`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `True`
- `npu_excluded_when_unusable`: `True`
- `provider_execution_seen`: `True`

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
- Routing: `{'advisory_lanes': ['ollama'], 'excluded_advisory_lanes': ['npu'], 'primary_advisory_provider': {'provider': 'ollama', 'compute_lane': 'gpu_cuda', 'role': 'primary_advisory', 'execution_mode': 'explicit_only', 'enabled_by_flag': '--use-primary-advisory-provider / -UsePrimaryAdvisoryProvider', 'provider_execution_performed': False}, 'trusted_context_files': [{'path': 'output/ai_packets/ollama_gpu_real_workload_report.md', 'lane': 'ollama', 'trusted': True, 'reason': 'usable_text', 'classification': 'usable_text'}], 'excluded_context_files': [{'path': 'output/ai_packets/npu_real_workload_report.md', 'lane': 'npu', 'trusted': False, 'reason': 'unusable_output', 'classification': 'unusable_output'}]}`

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
- Passed: `False`
- Provider execution performed: `True`
- Errors: `["ModuleNotFoundError: No module named 'openvino_genai'"]`
- Warnings: `['NPU execution was not requested; run with --run-npu for a real decode smoke.']`

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

### `output/ai_packets/npu_ollama_primary_after_routing.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet`
- Passed: `True`
- Ollama: `{'used': True, 'model': None, 'error': '', 'text_preview': '<markdown fence>\n# Next Safe Milestone\n\n**Title:** Review and Fix Failing Validation Reports\n\n**Details:** \n- Focus on fixing the failing validation reports identified in `C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\validation\\\\ai_workload_report_quality.json`.\n- Ensure that the AI workload report meets quality standards by addressing issues related to alphabetic character ratio, word count, and natural language appearance.\n\n# Files to Inspect\n\n1. **Validation Report:**\n   - `C:\\\\Users\\'}`

### `output/ai_packets/npu_ollama_primary_routing_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
