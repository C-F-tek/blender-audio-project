# Full Toolbox Run Telemetry Summary

- Passed: `True`
- Stamp: `20260505-073332`
- Recommendation count: `5`
- Patch plan count: `5`
- Deterministic synthesizer used: `False`
- Patch plan fallback used: `None`
- Provider execution performed: `True`

## Repository consistency performance

- `total_build_report_seconds`: `42.787`
- `markdown_scan_seconds`: `37.41`
- `file_discovery_seconds`: `1.861`
- `python_inventory_seconds`: `2.4`
- `path_index_seconds`: `1.092`
- `findings_build_seconds`: `0.023`

## Top recommendations

- `implement_adapter_manifest_validator` `validation` `low` -> `['Tools/validation/check_repository_change_proposals.py']`
- `extract_reusable_enrichment_plan_logic` `code_code` `medium` -> `['Tools/ai/README.md']`
- `add_optional_wrapper_preset_flag` `workflow` `low` -> `['Tools/workflow/run_local_ai_markdown_task.ps1']`
- `include_selected_chunks_evidence` `validation` `low` -> `['Tools/validation/check_selected_semantic_chunks.py']`
- `develop_npu_knowledge_broker_helper` `code_code` `medium` -> `['Tools/ai/README.md']`

## Top patch plans

- `implement_adapter_manifest_validator` `validation` review=`True` -> `['Tools/validation/check_repository_change_proposals.py']`
- `extract_reusable_enrichment_plan_logic` `code_code` review=`True` -> `['Tools/ai/README.md']`
- `add_optional_wrapper_preset_flag` `workflow` review=`True` -> `['Tools/workflow/run_local_ai_markdown_task.ps1']`
- `include_selected_chunks_evidence` `validation` review=`True` -> `['Tools/validation/check_selected_semantic_chunks.py']`
- `develop_npu_knowledge_broker_helper` `code_code` review=`True` -> `['Tools/ai/README.md']`

## GPU/NPU operational opinions

- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.
- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics.

