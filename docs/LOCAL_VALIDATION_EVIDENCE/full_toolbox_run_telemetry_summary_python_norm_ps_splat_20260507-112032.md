# Full Toolbox Run Telemetry Summary

- Passed: `True`
- Stamp: `python_norm_ps_splat_20260507-112032`
- Recommendation count: `1`
- Patch plan count: `1`
- Deterministic synthesizer used: `False`
- Patch plan fallback used: `None`
- Provider execution performed: `True`
- GPU provider execution performed: `True`
- GPU round count: `2`
- GPU0 startup peer support execution performed: `True`
- GPU0 startup peer support overlap count: `2`
- Legacy NPU auditor requested: `False`
- Legacy NPU auditor execution performed: `False`
- NPU audit success count: `0`
- NPU orchestrator micro execution performed: `False`
- NPU orchestrator micro tool lane performed: `False`
- NPU orchestrator micro overlap count: `0`
- NPU orchestrator micro runtime tool executions: `0`
- AI peer exchange passed: `True`
- GPU0 peer provider execution performed: `True`
- GPU0 peer broker tool executions: `3`
- NPU micro non-blocking: `True`
- NPU micro provider execution performed: `False`
- NPU micro broker tool executions: `0`
- Runtime heap events: `28`
- Runtime heap live signals: `4`
- Runtime heap direct execution violations: `0`
- Line-count CSV rows: `638`

## Provider runtime heap

- Telemetry seen: `True`
- Snapshot seen: `True`
- Pending broker requests: `0`
- Broker results: `6`
- `init` passed=`True` event_count=`1` heap_event_count=`1`
- `gpu1-request` passed=`True` event_count=`1` heap_event_count=`9`
- `broker-results` passed=`True` event_count=`3` heap_event_count=`16`
- `npu-support` passed=`True` event_count=`1` heap_event_count=`17`

## Line-count CSV

- Seen: `True`
- Path: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-112058.csv`
- Total lines: `118794`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py`: `2478`
- `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py`: `2197`
- `Tools/npu/run_dual_ai_pipeline.py`: `1774`
- `old script legacy/spaziotempo_asset_visual_v61.py`: `1513`
- `Scripting/v61b/scene_tuning_panel.py`: `1262`
- `Tools/workflow/workflow_state.py`: `1230`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py`: `1180`
- `old script legacy/spaziotempo_asset_visual_v6.py`: `1174`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py`: `1100`
- `Scripting/v61b_backgood/scene_tuning_panel.py`: `1097`

## Repository consistency performance

- `total_build_report_seconds`: `83.605`
- `markdown_scan_seconds`: `59.577`
- `file_discovery_seconds`: `10.631`
- `python_inventory_seconds`: `7.251`
- `path_index_seconds`: `6.096`
- `findings_build_seconds`: `0.051`

## Top recommendations

- `rec_summarize_evidence_bundle` `doc_code` `low` -> `['docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-002.md']`

## Top patch plans

- `rec_summarize_evidence_bundle` `doc_code` review=`True` -> `['docs/AGENT_REVIEW_CODE_PATCH_PLAN/part-002.md']`

## GPU/NPU operational opinions

- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.

