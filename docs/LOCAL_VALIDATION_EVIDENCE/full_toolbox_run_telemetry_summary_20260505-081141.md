# Full Toolbox Run Telemetry Summary

- Passed: `True`
- Stamp: `20260505-081141`
- Recommendation count: `3`
- Patch plan count: `3`
- Deterministic synthesizer used: `False`
- Patch plan fallback used: `None`
- Provider execution performed: `True`

## Repository consistency performance

- `total_build_report_seconds`: `42.01`
- `markdown_scan_seconds`: `36.814`
- `file_discovery_seconds`: `1.85`
- `python_inventory_seconds`: `2.297`
- `path_index_seconds`: `1.03`
- `findings_build_seconds`: `0.019`

## Top recommendations

- `rec_doc_code_001` `doc_code` `low` -> `['docs/AI_ONBOARDING.md']`
- `rec_doc_code_003` `doc_code` `low` -> `['docs/AI_REFERENCE_ONBOARDING.md']`
- `rec_doc_code_005` `doc_code` `low` -> `['docs/AI_REFERENCE_SOURCE_MAP.md']`

## Top patch plans

- `rec_doc_code_001` `doc_code` review=`True` -> `['docs/AI_ONBOARDING.md']`
- `rec_doc_code_003` `doc_code` review=`True` -> `['docs/AI_REFERENCE_ONBOARDING.md']`
- `rec_doc_code_005` `doc_code` review=`True` -> `['docs/AI_REFERENCE_SOURCE_MAP.md']`

## GPU/NPU operational opinions

- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.
- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics.

