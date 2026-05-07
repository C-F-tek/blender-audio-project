# Evidence Chunk 0004/0004

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `cf4364b662a4a63fc507c4039335852a4f76f55ebf6e95c2f55e0b56fa0bc9ae`
- line_start: `649`
- line_end: `986`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_run_telemetry_summary_patch_quality_product_probe_20260507-133119_json_cf4364_chunk_0003.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: provider_runtime_heap; sync_metrics; performance; operational_opinions; refactoring_suggestions. Preview: "provider_runtime_heap": { "telemetry_seen": true, "snapshot_seen": true, "live_signal_count": 4, "event_count": 32, "parse_error_count": 0, "direct_execution_violation_count": 0, "pending_broker_request_count": 0, "events_by_lane": { "broker": 6, "determinist...

## Context before

      "peer_contract_passed": true,
      "gpu0_peer_provider_execution_performed": true,
      "gpu0_peer_tool_request_count": 3,
      "gpu0_peer_tool_execution_count": 3,
      "npu_micro_non_blocking": true,
      "npu_micro_provider_execution_performed": false,
      "npu_micro_tool_request_count": 0,
      "npu_micro_tool_execution_count": 0,
      "classifications": [
        "gpu0_peer_semantic_model_unconfigured"
      ]
    },

## Chunk content

```json
    "provider_runtime_heap": {
      "telemetry_seen": true,
      "snapshot_seen": true,
      "live_signal_count": 4,
      "event_count": 32,
      "parse_error_count": 0,
      "direct_execution_violation_count": 0,
      "pending_broker_request_count": 0,
      "events_by_lane": {
        "broker": 6,
        "deterministic": 1,
        "gpu0": 13,
        "gpu1": 2,
        "npu": 2,
        "orchestrator": 8
      },
      "events_by_type": {
        "broker_request": 6,
        "broker_result": 6,
        "evidence_request": 7,
        "evidence_response": 9,
        "provider_state": 3,
        "validation_signal": 1
      },
      "interaction_edges": {
        "broker->gpu0:broker_result": 6,
        "deterministic->gpu1:validation_signal": 1,
        "gpu0->broker:broker_request": 6,
        "gpu0->gpu1:evidence_response": 7,
        "gpu1->gpu0:evidence_request": 2,
        "npu->gpu1:evidence_response": 2,
        "orchestrator->gpu0:evidence_request": 5,
        "orchestrator->none:provider_state": 3
      },
      "gpu1_to_gpu0_event_count": 2,
      "gpu0_to_gpu1_event_count": 7,
      "gpu1_gpu0_bidirectional": true,
      "broker_result_count": 6,
      "live_signals": [
        {
          "mode": "init",
          "passed": true,
          "event_count": 1,
          "heap_event_count": 1,
          "pending_broker_request_count": 0
        },
        {
          "mode": "gpu1-request",
          "passed": true,
          "event_count": 1,
          "heap_event_count": 13,
          "pending_broker_request_count": 0
        },
        {
          "mode": "broker-results",
          "passed": true,
          "event_count": 3,
          "heap_event_count": 20,
          "pending_broker_request_count": 0
        },
        {
          "mode": "npu-support",
          "passed": true,
          "event_count": 1,
          "heap_event_count": 21,
          "pending_broker_request_count": 0
        }
      ]
    },
    "sync_metrics": {
      "gpu_round_count": 4,
      "npu_audit_count": 0,
      "legacy_npu_audit_count": 0,
      "npu_micro_support_count": 0,
      "npu_micro_support_overlap_count": 0,
      "gpu0_peer_support_count": 5,
      "gpu0_peer_support_overlap_count": 4,
      "npu_audit_success_count": 0,
      "npu_audit_round_coverage": 0.0,
      "avg_gpu_round_seconds": 15.424,
      "p50_gpu_round_seconds": 15.424,
      "p90_gpu_round_seconds": 15.424,
      "avg_npu_audit_seconds": 0.0,
      "p50_npu_audit_seconds": 0.0,
      "p90_npu_audit_seconds": 0.0,
      "npu_to_gpu_avg_duration_ratio": 0.0,
      "gpu_elapsed_seconds": 61.694,
      "provider_execution_performed": true,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
    },
    "performance": {
      "analyzer_elapsed_seconds": 0.001,
      "gpu": {
        "elapsed_seconds": 61.694,
        "round_count": 4,
        "round_duration_source": "gpu_elapsed_divided_by_round_count",
        "round_duration_sample_count": 1,
        "avg_round_seconds": 15.424,
        "p50_round_seconds": 15.424,
        "p90_round_seconds": 15.424,
        "max_round_seconds": 15.424,
        "round_durations_total_seconds": 15.424,
        "provider_empty_response_count": 0,
        "schema_repair_retry_attempt_count": 0,
        "schema_repair_retry_accept_count": 0,
        "runtime_tool_counters": {
          "runtime_tool_request_count": 15,
          "runtime_tool_execution_count": 7,
          "runtime_tool_failed_count": 0,
          "runtime_tool_blocked_count": 0,
          "runtime_tool_provider_request_count": 8,
          "runtime_tool_provider_request_execution_count": 0,
          "deterministic_runtime_tool_fallback_request_count": 0,
          "deterministic_runtime_tool_fallback_execution_count": 0
        },
        "embedded_performance": {}
      },
      "npu": {
        "audit_count": 0,
        "audit_requested_count": 0,
        "audit_success_count": 0,
        "duration_sample_count": 0,
        "avg_audit_seconds": 0.0,
        "p50_audit_seconds": 0.0,
        "p90_audit_seconds": 0.0,
        "max_audit_seconds": 0.0,
        "audit_durations_total_seconds": 0.0,
        "status_counts": {},
        "classification_counts": {},
        "lane_diagnostics": {}
      },
      "sync": {
        "npu_to_gpu_avg_duration_ratio": 0.0,
        "npu_audit_round_coverage": 0.0,
        "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
      },
      "guardrails": {
        "report_only": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "blender_runtime_execution_performed": false,
        "sqlite_write_performed": false
      }
    },
    "operational_opinions": [
      "Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.",
      "GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present."
    ],
    "refactoring_suggestions": [
      {
        "priority": "high",
        "area": "gpu_runner_timing",
        "recommendation": "Use rounds[*].elapsed_seconds as the primary GPU round timing source.",
        "evidence": "gpu_metrics_source=gpu_elapsed_divided_by_round_count",
        "guardrail": "report_only_no_provider_setting_change"
      }
    ]
  },
  "provider_runtime_heap": {
    "telemetry_seen": true,
    "snapshot_seen": true,
    "live_signal_count": 4,
    "event_count": 32,
    "parse_error_count": 0,
    "direct_execution_violation_count": 0,
    "pending_broker_request_count": 0,
    "events_by_lane": {
      "broker": 6,
      "deterministic": 1,
      "gpu0": 13,
      "gpu1": 2,
      "npu": 2,
      "orchestrator": 8
    },
    "events_by_type": {
      "broker_request": 6,
      "broker_result": 6,
      "evidence_request": 7,
      "evidence_response": 9,
      "provider_state": 3,
      "validation_signal": 1
    },
    "interaction_edges": {
      "broker->gpu0:broker_result": 6,
      "deterministic->gpu1:validation_signal": 1,
      "gpu0->broker:broker_request": 6,
      "gpu0->gpu1:evidence_response": 7,
      "gpu1->gpu0:evidence_request": 2,
      "npu->gpu1:evidence_response": 2,
      "orchestrator->gpu0:evidence_request": 5,
      "orchestrator->none:provider_state": 3
    },
    "gpu1_to_gpu0_event_count": 2,
    "gpu0_to_gpu1_event_count": 7,
    "gpu1_gpu0_bidirectional": true,
    "broker_result_count": 6,
    "live_signals": [
      {
        "mode": "init",
        "passed": true,
        "event_count": 1,
        "heap_event_count": 1,
        "pending_broker_request_count": 0
      },
      {
        "mode": "gpu1-request",
        "passed": true,
        "event_count": 1,
        "heap_event_count": 13,
        "pending_broker_request_count": 0
      },
      {
        "mode": "broker-results",
        "passed": true,
        "event_count": 3,
        "heap_event_count": 20,
        "pending_broker_request_count": 0
      },
      {
        "mode": "npu-support",
        "passed": true,
        "event_count": 1,
        "heap_event_count": 21,
        "pending_broker_request_count": 0
      }
    ]
  },
  "line_count_csv": {
    "seen": true,
    "path": "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260507-133144.csv",
    "row_count": 650,
    "total_lines": 119498,
    "top_files": [
      {
        "file": "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
        "lines": 2263
      },
      {
        "file": "Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py",
        "lines": 2197
      },
      {
        "file": "Tools/npu/run_dual_ai_pipeline.py",
        "lines": 1774
      },
      {
        "file": "old script legacy/spaziotempo_asset_visual_v61.py",
        "lines": 1513
      },
      {
        "file": "Scripting/v61b/scene_tuning_panel.py",
        "lines": 1262
      },
      {
        "file": "Tools/workflow/workflow_state.py",
        "lines": 1230
      },
      {
        "file": "Tools/ai/run_agent_gpu_deep_planning_supervised.py",
        "lines": 1180
      },
      {
        "file": "old script legacy/spaziotempo_asset_visual_v6.py",
        "lines": 1174
      },
      {
        "file": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
        "lines": 1100
      },
      {
        "file": "Scripting/v61b_backgood/scene_tuning_panel.py",
        "lines": 1097
      },
      {
        "file": "Scripting/v61b/animation.py",
        "lines": 1079
      },
      {
        "file": "Scripting/v61b_backgood/animation.py",
        "lines": 1019
      },
      {
        "file": "old script legacy/spaziotempo_album_visual_v5.py",
        "lines": 969
      },
      {
        "file": "Tools/ai/build_deterministic_recommendations.py",
        "lines": 909
      },
      {
        "file": "Tools/ai/run_agent_gpu_deep_planning_review.py",
        "lines": 902
      },
      {
        "file": "Tools/ai/build_runtime_tool_usage_telemetry.py",
        "lines": 823
      },
      {
        "file": "Tools/ai/agent_runtime_tool_broker.py",
        "lines": 759
      },
      {
        "file": "Tools/workflow/gui/workflow_gui.py",
        "lines": 738
      },
      {
        "file": "Scripting/v61b/physics_setup.py",
        "lines": 737
      },
      {
        "file": "Scripting/v61b/asset_setup.py",
        "lines": 725
      }
    ]
  },
  "guardrails": {
    "report_only": true,
    "committable_location": "docs/LOCAL_VALIDATION_EVIDENCE",
    "raw_output_commit_allowed": false,
    "provider_execution_performed": true,
    "gpu_provider_execution_performed": true,
    "gpu0_peer_support_provider_execution_performed": true,
    "npu_provider_execution_performed": false,
    "npu_micro_orchestrator_provider_execution_performed": false,
    "npu_micro_orchestrator_tool_lane_performed": false,
    "gpu0_peer_provider_execution_performed": true,
    "npu_micro_provider_execution_performed": false,
    "npu_micro_non_blocking": true,
    "provider_runtime_heap_direct_execution_violation_count": 0,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false
  }
}
```
