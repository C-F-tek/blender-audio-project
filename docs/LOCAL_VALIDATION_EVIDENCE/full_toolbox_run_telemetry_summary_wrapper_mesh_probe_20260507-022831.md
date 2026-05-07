# Full Toolbox Run Telemetry Summary

- Passed: `True`
- Stamp: `wrapper_mesh_probe_20260507-022831`
- Recommendation count: `20`
- Patch plan count: `20`
- Deterministic synthesizer used: `True`
- Patch plan fallback used: `None`
- Provider execution performed: `True`
- GPU provider execution performed: `True`
- GPU round count: `1`
- GPU0 startup peer support execution performed: `True`
- GPU0 startup peer support overlap count: `2`
- Legacy NPU auditor requested: `False`
- Legacy NPU auditor execution performed: `False`
- NPU audit success count: `0`
- NPU orchestrator micro execution performed: `False`
- NPU orchestrator micro tool lane performed: `True`
- NPU orchestrator micro overlap count: `1`
- NPU orchestrator micro runtime tool executions: `4`
- AI peer exchange passed: `True`
- GPU0 peer provider execution performed: `True`
- GPU0 peer broker tool executions: `3`
- NPU micro non-blocking: `True`
- NPU micro provider execution performed: `False`
- NPU micro broker tool executions: `4`
- Runtime heap events: `37`
- Runtime heap live signals: `4`
- Runtime heap direct execution violations: `0`
- Line-count CSV rows: `632`

## Provider runtime heap

- Telemetry seen: `True`
- Snapshot seen: `True`
- Pending broker requests: `0`
- Broker results: `11`
- `init` passed=`True` event_count=`1` heap_event_count=`1`
- `gpu1-request` passed=`True` event_count=`1` heap_event_count=`18`
- `broker-results` passed=`True` event_count=`3` heap_event_count=`25`
- `npu-support` passed=`True` event_count=`1` heap_event_count=`26`

## Line-count CSV

- Seen: `True`
- Path: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-022832.csv`
- Total lines: `116934`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py`: `2290`
- `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py`: `2197`
- `Tools/npu/run_dual_ai_pipeline.py`: `1774`
- `old script legacy/spaziotempo_asset_visual_v61.py`: `1513`
- `Scripting/v61b/scene_tuning_panel.py`: `1262`
- `Tools/workflow/workflow_state.py`: `1230`
- `old script legacy/spaziotempo_asset_visual_v6.py`: `1174`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py`: `1129`
- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py`: `1100`
- `Scripting/v61b_backgood/scene_tuning_panel.py`: `1097`

## Repository consistency performance

- `total_build_report_seconds`: `69.116`
- `markdown_scan_seconds`: `50.756`
- `file_discovery_seconds`: `8.368`
- `python_inventory_seconds`: `5.421`
- `path_index_seconds`: `4.541`
- `findings_build_seconds`: `0.031`

## Top recommendations

- `consistency_001` `md_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_002` `md_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_003` `md_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_004` `md_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_005` `md_python` `medium` -> `['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- `consistency_006` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md']`
- `consistency_007` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- `consistency_008` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_009` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_010` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- `consistency_011` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- `consistency_012` `md_python` `medium` -> `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- `consistency_013` `md_python` `medium` -> `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- `consistency_046` `md_powershell` `medium` -> `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_047` `md_powershell` `medium` -> `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_048` `md_powershell` `medium` -> `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- `consistency_049` `md_powershell` `medium` -> `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- `consistency_050` `md_powershell` `medium` -> `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- `consistency_051` `md_powershell` `medium` -> `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- `consistency_052` `md_powershell` `medium` -> `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']`

## Top patch plans

- `consistency_001` `md_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_002` `md_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_003` `md_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_004` `md_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/02-sqlite-heap-memory-design.md']`
- `consistency_005` `md_python` review=`True` -> `['CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md']`
- `consistency_006` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/14-markdown-line-budget-download-bundles.md']`
- `consistency_007` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-001.md']`
- `consistency_008` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_009` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate/part-002.md']`
- `consistency_010` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md']`
- `consistency_011` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md']`
- `consistency_012` `md_python` review=`True` -> `['docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md']`
- `consistency_013` `md_python` review=`True` -> `['docs/LOCAL_RUNS_TESTING_AND_EVIDENCE/part-001.md']`
- `consistency_046` `md_powershell` review=`True` -> `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_047` `md_powershell` review=`True` -> `['AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md']`
- `consistency_048` `md_powershell` review=`True` -> `['CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md']`
- `consistency_049` `md_powershell` review=`True` -> `['docs/AUTO_PUSH_GENERATED_ARTIFACTS.md']`
- `consistency_050` `md_powershell` review=`True` -> `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- `consistency_051` `md_powershell` review=`True` -> `['docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md']`
- `consistency_052` `md_powershell` review=`True` -> `['docs/LOCAL_AI_TASKS/full-run-tutto-su-tutto/01-startup-params-quality-supervisor.md']`

## GPU/NPU operational opinions

- GPU/NPU cadence is measurable; tune audit frequency from timing evidence rather than intuition.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.
- Runtime tool execution had failed or blocked requests; recommendations should reference broker evidence before proposing patches.
