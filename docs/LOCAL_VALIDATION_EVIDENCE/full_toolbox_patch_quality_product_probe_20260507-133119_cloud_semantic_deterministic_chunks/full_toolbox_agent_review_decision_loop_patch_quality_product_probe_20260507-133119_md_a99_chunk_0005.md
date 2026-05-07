# Evidence Chunk 0005/0024

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.md`
- source_sha256: `a996111fa318d87d97d3b80eb2d1e49442622645214c899236220d62065e9ccb`
- line_start: `630`
- line_end: `726`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0004.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0006.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: Artifact manifest; Included artifact contents; `output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.md`; Repository Consistency Map; Severity counts. Preview: ## Artifact manifest - `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json` exists=`True` size=`72790` suffix=`.json` preview_chars=`1500` - `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119...

## Context before

- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.

#### consistency_051 — md_powershell
- Source: `gpu_recommendation`
- Risk: `medium`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md']
- Rationale: Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:330` targeting `validate_after_patch.ps1`.
- Strategy: Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:330`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.



## Chunk content

````md
## Artifact manifest

- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json` exists=`True` size=`72790` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json` exists=`True` size=`23981` suffix=`.json` preview_chars=`1500`
- `output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`9571446` suffix=`.json` preview_chars=`1500`
- `output/validation/repository_consistency_map_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1228` suffix=`.json` preview_chars=`1189`
- `output/analysis/code_interpreter_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`2129738` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`3162` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`78343` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`5378` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/npu_provider_environment_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/validation/openvino_hardware_governance_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`2242` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`6376` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`5238` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_evidence_contract_full_toolbox_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`6878` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`8407` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`498` suffix=`.json` preview_chars=`486`
- `output/ai_pipeline/gpu0_peer_support_parallel_patch_quality_product_probe_20260507-133119/round_000_gpu0_peer_support.json` exists=`True` size=`1732` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu1_primary_advisory_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1478` suffix=`.json` preview_chars=`1436`
- `output/validation/gpu0_peer_task_packet_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`6134` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_peer_response_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`5011` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_tool_requests_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`3450` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`29697` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_micro_peer_assistant_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1492` suffix=`.json` preview_chars=`1452`
- `output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1010` suffix=`.json` preview_chars=`979`
- `output/validation/ai_peer_exchange_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`61320` suffix=`.json` preview_chars=`1500`
- `output/validation/ai_peer_exchange_contract_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`13421` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_init_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1573` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_gpu1_request_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1962` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_broker_results_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`4810` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_live_signals_npu_support_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1931` suffix=`.json` preview_chars=`1500`
- `output/ai_runtime_heap/patch_quality_product_probe_20260507-133119/snapshot.json` exists=`True` size=`7017` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`2286` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_workflow.json` exists=`True` size=`5705` suffix=`.json` preview_chars=`1500`
- `output/validation/provider_runtime_heap_from_peer_reports_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`1649` suffix=`.json` preview_chars=`1500`
- `docs/LOCAL_VALIDATION_EVIDENCE/patch_plan_quality_product_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`23363` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json` exists=`True` size=`379334` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_manifest.json` exists=`True` size=`379334` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_evidence_index.json` exists=`True` size=`202251` suffix=`.json` preview_chars=`1500`
- `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/full0to10_final_tool_product_readiness.json` exists=`True` size=`444` suffix=`.json` preview_chars=`430`
- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json` exists=`True` size=`368889` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_bridge_orchestrator.json` exists=`True` size=`1252` suffix=`.json` preview_chars=`1219`
- `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.json` exists=`True` size=`3058` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json` exists=`True` size=`441138` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `56878`
- SHA-256: `b8dc343722aa7723ab004fa279ffba3f19553d509c8404a2e97a2fa027ae62a2`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `12321`
- Repository files: `1642`
- File metadata records: `1642`
- Counted text-like files: `1616`
- Total counted text lines: `1409295`
- Markdown files: `635`
- Python files: `650`
- Markdown references: `84503`
- Markdown Python commands: `786`
- Provider execution performed: `False`
- Workers requested: `0`
- Adaptive worker mode: `True`
- Single file manifest: `True`
- File metadata enabled: `True`
- Total build seconds: `25.864`
- Markdown scan seconds: `18.523`
- Python inventory seconds: `0.407`
- Patch application performed: `False`

## Severity counts

- `high`: `3952`
- `low`: `48`
- `medium`: `8321`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `48`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `8319`
- `md_mentions_missing_powershell_path`: `524`
- `md_mentions_missing_python_path`: `3384`
- `md_python_command_script_missing`: `44`

````

## Context after

## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 374 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 375 | `patches/00_check_repo_ready.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AGENTS.md` | 372 | `text
README.md
run_patch_bundle.py
patches/00_check_repo_ready.py
patches/01_*.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | 237 | `run_patch_bundle.py` | Correct the documentation reference or restore the missing target if it is still required. |
