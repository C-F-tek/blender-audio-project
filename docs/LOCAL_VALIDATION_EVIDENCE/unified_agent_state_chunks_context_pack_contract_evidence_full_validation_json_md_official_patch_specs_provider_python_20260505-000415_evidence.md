# Local Validation Evidence Bundle

- Generated at: `2026-05-05T00:05:40`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `True`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `1`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/validation/ai_workload_report_quality.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_workload_report_quality`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Usable lanes: `['npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu']`
- Unusable lanes: `[]`
- Warnings: `['ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'npu: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder', 'ollama: known workload report not selected: known_workload_report_missing_from_selected_output_folder']`

### `output/validation/ai_workload_quality_lane_routing.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `ai_workload_quality_lane_routing`
- Passed: `True`
- Provider execution performed: `False`
- Primary advisory provider: `{'provider': None, 'compute_lane': None, 'role': 'none', 'execution_mode': 'unavailable_no_usable_lane', 'enabled_by_flag': None, 'provider_execution_performed': False}`
- Routing: `{'advisory_lanes': ['npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu', 'npu'], 'excluded_advisory_lanes': [], 'primary_advisory_provider': {'provider': None, 'compute_lane': None, 'role': 'none', 'execution_mode': 'unavailable_no_usable_lane', 'enabled_by_flag': None, 'provider_execution_performed': False}, 'trusted_context_files': [{'path': 'docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_pipeline/full_context_golden_enrichment_plan.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_pipeline/full_context_golden_enrichment_plan.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'indexAI/code_chunks/semantic_code_chunks_manifest.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_context_packs/full_context_golden_selected_chunks.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_context_packs/full_context_golden_selected_chunks.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_context_packs/full_context_golden_core_ai_backend.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/ai_context_packs/full_context_golden_core_ai_backend.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/local_ai_runs/20260505-000415_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_unified/pipeline/agent_state/full_context_golden_agent_state.md', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}, {'path': 'output/local_ai_runs/20260505-000415_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_unified/pipeline/agent_state/full_context_golden_agent_state.json', 'lane': '', 'trusted': True, 'reason': 'not_a_tracked_workload_report', 'classification': ''}], 'excluded_context_files': []}`

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
- Passed: `False`
- Provider execution performed: `True`
- Errors: `['ollama: probe failed']`

### `output/validation/npu_runtime_output_manifest.json`

- Exists: `False`
- JSON OK: `False`
- Kind: `None`
- Passed: `None`

### `output/validation/provider_result_report.json`

- Exists: `False`
- JSON OK: `False`
- Kind: `None`
- Passed: `None`

## Artifact manifest

- `output/validation/ai_workload_report_quality.json` exists=`True` size=`18613` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_workload_quality_lane_routing.json` exists=`True` size=`7643` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_decode_quality_remediation.json` exists=`True` size=`2426` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_decode_smoke_diagnostic.json` exists=`True` size=`2150` suffix=`.json` preview_chars=`1500`
- `output/validation/local_provider_probe.json` exists=`True` size=`2528` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_runtime_output_manifest.json` exists=`False` size=`None` suffix=`.json` preview_chars=`None`
- `output/validation/provider_result_report.json` exists=`False` size=`None` suffix=`.json` preview_chars=`None`

## Included artifact contents

### `output/validation/ai_workload_quality_lane_routing.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2428`
- SHA-256: `53fc86b534cb6cee9e8373d596bab28a4bd3ae29c226dee78d6a480206b86f66`
- Content included: `True`
- Content truncated: `False`

```text
# AI Workload Quality Lane Routing

- Mode: `report_only_quality_based_lane_routing`
- Provider execution performed: `False`
- Quality report present: `True`
- Advisory lanes: `npu, npu, npu, npu, npu, npu, npu, npu, npu, npu`
- Excluded advisory lanes: `none`
- Primary advisory provider: `none`
- Primary compute lane: `none`

## Trusted context files

- `docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md` — lane `untracked`, reason `not_a_tracked_workload_report`
- `output/ai_pipeline/full_context_golden_enrichment_plan.md` — lane `untracked`, reason `not_a_tracked_workload_report`
- `output/ai_pipeline/full_context_golden_enrichment_plan.json` — lane `untracked`, reason `not_a_tracked_workload_report`
- `indexAI/code_chunks/semantic_code_chunks_manifest.json` — lane `untracked`, reason `not_a_tracked_workload_report`
- `output/ai_context_packs/full_context_golden_selected_chunks.md` — lane `untracked`, reason `not_a_tracked_workload_report`
- `output/ai_context_packs/full_context_golden_selected_chunks.json` — lane `untracked`, reason `not_a_tracked_workload_report`
- `output/ai_context_packs/full_context_golden_core_ai_backend.md` — lane `untracked`, reason `not_a_tracked_workload_report`
- `output/ai_context_packs/full_context_golden_core_ai_backend.json` — lane `untracked`, reason `not_a_tracked_workload_report`
- `output/local_ai_runs/20260505-000415_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_unified/pipeline/agent_state/full_context_golden_agent_state.md` — lane `untracked`, reason `not_a_tracked_workload_report`
- `output/local_ai_runs/20260505-000415_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_unified/pipeline/agent_state/full_context_golden_agent_state.json` — lane `untracked`, reason `not_a_tracked_workload_report`

## Excluded context files

- none

## Guardrails

- Any change would execute providers implicitly or by default.
- Any change would use an unusable workload report as advisory context.
- Any change would alter NPU/Ollama model configuration, prompt prose or provider orchestration.
- Any change would touch Blender runtime, Ready To Jazz, full analysis JSON, output legacy or generated indexes by hand.
- Any change would introduce OpenVINO GPU as a primary lane.

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
- Total selected chars: `30701`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
