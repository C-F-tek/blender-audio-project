# Full Toolbox Run Telemetry Summary

- Passed: `True`
- Stamp: `post_patchable_doc_python_probe_20260507-180555`
- Recommendation count: `240`
- Patch plan count: `240`
- Deterministic synthesizer used: `True`
- Patch plan fallback used: `None`
- Provider execution performed: `True`
- GPU provider execution performed: `True`
- GPU round count: `4`
- GPU0 startup peer support execution performed: `True`
- GPU0 startup peer support overlap count: `5`
- Legacy NPU auditor requested: `False`
- Legacy NPU auditor execution performed: `False`
- NPU audit success count: `0`
- NPU orchestrator micro execution performed: `False`
- NPU orchestrator micro tool lane performed: `True`
- NPU orchestrator micro overlap count: `2`
- NPU orchestrator micro runtime tool executions: `11`
- AI peer exchange passed: `True`
- GPU0 peer provider execution performed: `True`
- GPU0 peer broker tool executions: `3`
- NPU micro non-blocking: `True`
- NPU micro provider execution performed: `False`
- NPU micro broker tool executions: `0`
- NPU final review classification: `gpu1_gpu0_npu_final_review`
- NPU final review on performant lane: `True`
- NPU final close-path provider required: `False`
- Runtime heap events: `60`
- Runtime heap live signals: `5`
- Runtime heap direct execution violations: `0`
- Line-count CSV rows: `661`

## Provider runtime heap

- Telemetry seen: `True`
- Snapshot seen: `True`
- Pending broker requests: `0`
- Broker results: `20`
- `init` passed=`True` event_count=`1` heap_event_count=`1`
- `gpu1-request` passed=`True` event_count=`1` heap_event_count=`39`
- `broker-results` passed=`True` event_count=`3` heap_event_count=`46`
- `npu-support` passed=`True` event_count=`1` heap_event_count=`47`
- `tool-catalog-complete` passed=`True` event_count=`2` heap_event_count=`60`

## Line-count CSV

- Seen: `True`
- Path: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-180624.csv`
- Total lines: `121515`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py`: `2263`
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

- `total_build_report_seconds`: `32.449`
- `markdown_scan_seconds`: `21.912`
- `file_discovery_seconds`: `9.345`
- `python_inventory_seconds`: `0.756`
- `path_index_seconds`: `0.4`
- `findings_build_seconds`: `0.035`

## Top recommendations

- `consistency_001` `python_python` `medium` -> `['Tools/ai/build_agent_review_code_patch_plan.py']`
- `consistency_002` `doc_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_003` `doc_doc` `low` -> `['CHATGPT.md']`
- `consistency_004` `python_doc` `low` -> `['Tools/ai/analyze_gpu_npu_run_sync.py']`
- `consistency_005` `python_python` `medium` -> `['Tools/ai/build_code_edit_proposal_from_plan.py']`
- `consistency_006` `doc_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_007` `doc_doc` `low` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_008` `python_doc` `low` -> `['Tools/ai/build_agent_agnostic_tool_inventory.py']`
- `consistency_009` `python_python` `medium` -> `['Tools/ai/build_code_patch_artifact_pack.py']`
- `consistency_010` `doc_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_011` `doc_doc` `low` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_012` `python_doc` `low` -> `['Tools/ai/build_agent_review_code_patch_plan.py']`
- `consistency_013` `python_python` `medium` -> `['Tools/ai/build_code_patch_docs_followup.py']`
- `consistency_014` `doc_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_015` `doc_doc` `low` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_016` `python_doc` `low` -> `['Tools/ai/build_agent_review_evidence_sufficiency.py']`
- `consistency_017` `python_python` `medium` -> `['Tools/ai/enrich_github_evidence_bundle_code_plan.py']`
- `consistency_018` `doc_python` `medium` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_019` `doc_doc` `low` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_020` `python_doc` `low` -> `['Tools/ai/build_agent_review_patch_bundle.py']`

## Top patch plans

- `consistency_001` `python_python` review=`True` -> `['Tools/ai/build_agent_review_code_patch_plan.py']`
- `consistency_002` `doc_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_003` `doc_doc` review=`True` -> `['CHATGPT.md']`
- `consistency_004` `python_doc` review=`True` -> `['Tools/ai/analyze_gpu_npu_run_sync.py']`
- `consistency_005` `python_python` review=`True` -> `['Tools/ai/build_code_edit_proposal_from_plan.py']`
- `consistency_006` `doc_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_007` `doc_doc` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_008` `python_doc` review=`True` -> `['Tools/ai/build_agent_agnostic_tool_inventory.py']`
- `consistency_009` `python_python` review=`True` -> `['Tools/ai/build_code_patch_artifact_pack.py']`
- `consistency_010` `doc_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_011` `doc_doc` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_012` `python_doc` review=`True` -> `['Tools/ai/build_agent_review_code_patch_plan.py']`
- `consistency_013` `python_python` review=`True` -> `['Tools/ai/build_code_patch_docs_followup.py']`
- `consistency_014` `doc_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_015` `doc_doc` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_016` `python_doc` review=`True` -> `['Tools/ai/build_agent_review_evidence_sufficiency.py']`
- `consistency_017` `python_python` review=`True` -> `['Tools/ai/enrich_github_evidence_bundle_code_plan.py']`
- `consistency_018` `doc_python` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/04-implementation-plan.md']`
- `consistency_019` `doc_doc` review=`True` -> `['CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md']`
- `consistency_020` `python_doc` review=`True` -> `['Tools/ai/build_agent_review_patch_bundle.py']`

## GPU/NPU operational opinions

- GPU/NPU cadence is measurable; tune audit frequency from timing evidence rather than intuition.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.

