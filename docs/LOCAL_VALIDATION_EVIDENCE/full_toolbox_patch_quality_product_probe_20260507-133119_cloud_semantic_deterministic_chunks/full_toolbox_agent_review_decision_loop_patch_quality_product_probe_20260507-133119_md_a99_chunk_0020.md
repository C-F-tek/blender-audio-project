# Evidence Chunk 0020/0024

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.md`
- source_sha256: `a996111fa318d87d97d3b80eb2d1e49442622645214c899236220d62065e9ccb`
- line_start: `3303`
- line_end: `3492`
- section_kinds: `['markdown_heading_section', 'markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0019.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0021.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json`; `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.md`; Agent GPU/NPU Parallel Orchestrator; Decision; NPU Audits. Preview: "memory_promotion_performed": false, "memory_delete_performed": false, "provider_execution_performed": false, "patch_application_performed": false, "blender_runtime_touched": false } }, "guardrails": { "provider_execution_performed": false, "patch_application_...

## Context before

          "json_report": "output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/round_000/orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json",
          "markdown_report": "output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/round_000/orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md"
        },
        "summary": {
          "kind": "agent_memory_inventory",
          "passed": true,
          "errors": [],
          "warnings": [],
          "decision": {},
          "guardrails": {
            "sqlite_read_only": true,
            "sqlite_db_committed": false,

## Chunk content

````md
            "memory_promotion_performed": false,
            "memory_delete_performed": false,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "blender_runtime_touched": false
          }
        },
        "guardrails": {
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "sqlite_write_performed": false,
          "persistent_memory_write_performed": false,
          "persistent_memory_write_count": 0,
          "persistent_memory_write_requires_explicit_confirm": true,
          "operational_sqlite_write_performed": false,
          "operational_memory_write_performed": false,
          "operational_memory_clear_performed": false,
          "blender_runtime_touched": false,
          "git_write_performed": false
        },
        "command": [
          "C:\\Users\\carmi\\blender\\blender-audio-project\\.venv\\Scripts\\python.exe",
          "Tools/ai/build_agent_memory_inventory.py",
          "--repo-root",
          ".",
          "--objective",
          "Runtime read-only memory inventory for IA-Carmine planner.",
          "--memory-db",
          "indexAI/agent_memory/agent_memory.sqlite",
          "--output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\patch_quality_product_probe_20260507-133119\\round_000\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json",
          "--markdown-output",
          "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_runtime_tools\\patch_quality_product_probe_20260507-133119\\round_000\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md"
        ],
        "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\patch_quality_product_probe_20260507-133119\\\\round_000\\\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_runtime_tools\\\\patch_quality_product_probe_20260507-133119\\\\round_000\\\\orchestrator_bootstrap_memory_inventory_agent_memory_inventory.md\",\n  \"record_count\": 101,\n  \"memory_db_exists\": true,\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false\n}\n",
        "stderr_tail": ""
      },
      {
        "id": "orchestrator_bootstrap_persistent_memory_status",
        "tool": "runtime_sqlite_memory",
        "reason": "Bootstrap persistent memory status in read-only mode before GPU/NPU orchestration.",
        "requested": true,
        "executed": true,
        "blocked": false,
        "dry_run": false,
        "persistent_memory_write_authorized": false,
        "returncode": 0,
        "errors": [],
        "warnings": [],
        "outputs": {
          "json_report": "output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/round_000/orchestrator_bootstrap_persistent_memory_status_runtime_sqlite_memory.json",
          "markdown_report": "output/ai_runtime_tools/patch_quality_product_probe_20260507-133119/round_000/orchestrator_bootstrap_persistent_memory_status_runtime_sqlite_memory.md"
        },
        "summary": {
          "kind": "agent_runtime_sqlite_memory",
          "passed": true,
          "errors": [],
          "warnings": [],
          "decision": {},
          "guardrails": {
            "persistent_memory_read_only": true,
            "persistent_memory_write_performed": false,
            "persistent_memory_promotion_performed": false,
            "persistent_memory_write_authorized": false,
            "sqlite_write_performed": false,
            "operational_sqlite_write_performed": false,
            "operational_memory_clear_performed": false,
            "operational_database_must_be_under_output": true,
            "operational_database_under_output": true,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "blender_runtime_touched": false,
            "git_write_performed": false
          }
        },
        "guardrails": {
          "provider_execution_performed": false,
          "patch_application_performed": fals
```

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3989`
- SHA-256: `3750ace6cb43a4fe63444f62993e00d0b7bf87020ce7a9a9edc9f0184f1697ea`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `61.694`
- `gpu0_peer_support_count`: `5`
- `gpu0_peer_support_success_count`: `5`
- `gpu0_peer_support_overlap_count`: `4`
- `gpu0_peer_support_provider_execution_performed`: `True`
- `npu_micro_support_count`: `0`
- `npu_micro_support_success_count`: `0`
- `npu_micro_support_overlap_count`: `0`
- `npu_micro_support_provider_execution_performed`: `False`
- `npu_micro_support_tool_request_count`: `0`
- `npu_micro_runtime_tool_execution_count`: `0`
- `npu_audit_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `model_output_schema_mismatch`
- `gpu_evidence_ready_for_manual_patch_count`: `0`
- `runtime_tool_broker_enabled`: `True`
- `runtime_tool_request_count`: `15`
- `runtime_tool_execution_count`: `7`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `7`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `provider_mesh_mode`: `startup_barrier_parallel_peer_support`
- `all_lanes_ready_at_start`: `True`
- `gpu0_peer_support_started_with_gpu1`: `True`
- `npu_micro_support_started_with_gpu1`: `False`
- `npu_auditor_mode`: `legacy_disabled`
- `npu_audit_success_count`: `0`
- `npu_micro_support_success_count`: `0`
- `npu_micro_support_provider_success_count`: `0`
- `npu_micro_support_tool_success_count`: `0`
- `npu_micro_support_tool_request_count`: `0`
- `npu_micro_live_tool_seed_count`: `0`
- `npu_micro_runtime_tool_execution_count`: `0`
- `npu_micro_runtime_tool_live_execution_count`: `0`
- `npu_micro_support_tool_lane_performed`: `False`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_deterministic_tool_fallback_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `ready_for_patch_plan`: `False`
- `fallback_patch_plan_recommended`: `False`
- `recommended_next_layer`: `collect_more_evidence`
- `gpu_empty_recommendations_reason`: `model_output_schema_mismatch`
- `runtime_tool_broker_enabled`: `True`
- `runtime_tool_bootstrap_executed`: `True`
- `runtime_tool_bootstrap_execution_count`: `7`
- `runtime_tool_provider_request_count`: `0`
- `runtime_tool_provider_request_execution_count`: `0`
- `deterministic_runtime_tool_fallback_execution_count`: `0`
- `runtime_tool_execution_count`: `7`
- `runtime_tool_result_count`: `7`
- `manual_review_required`: `True`
- `provider_execution_performed`: `True`
- `gpu_provider_execution_performed`: `True`
- `gpu0_peer_support_provider_execution_performed`: `True`
- `npu_provider_execution_performed`: `False`
- `npu_micro_support_provider_execution_performed`: `False`
- `legacy_npu_auditor_provider_requested`: `False`
- `provider_degraded_reasons`: `[]`
- `gpu_lane_mode`: `primary_fast_loop`
- `npu_lane_mode`: `metadata_only`
- `gpu_direct_runtime_tool_provider_request_execution_count`: `0`
- `runtime_tool_feedback_context_report_count`: `0`
- `npu_effective_auditor_every_rounds`: `4`

## NPU Audits

## GPU0 Peer Support
- round `0` status=`finished` provider=`True` overlap=`True`
- round `1` status=`finished` provider=`True` overlap=`True`
- round `2` status=`finished` provider=`True` overlap=`True`
- round `3` status=`finished` provider=`True` overlap=`True`
- round `4` status=`finished` provider=`True` overlap=`False`

## NPU Micro Support

```

````

## Context after

### `output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `23981`
- SHA-256: `ec608cb1c5e4c45e0b97e8fef54382afcea3497c02344be90c173e05042fe9b5`
- Content included: `True`
- Content truncated: `True`

```text
{
