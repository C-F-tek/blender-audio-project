# Evidence Chunk 0012/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `3004`
- line_end: `3299`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0011.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0013.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifacts. Preview: "telemetry": { "kind": "full0to10_provider_governor_telemetry", "passed": true, "event_count": 4, "events": [ { "event": "accelerator_control", "passed": true, "severity": "info", "structural": true, "details": { "score": 92 }, "timestamp": "2026-05-07T11:33:3...

## Context before

                "provider_generation_must_write_tool_telemetry": true,
                "deny_is_valid_governor_result": true
              },
              "errors": [],
              "warnings": [
                "permit denied by policy; artifact generation is still valid"
              ],
              "provider_execution_performed": false,
              "patch_application_performed": false,
              "source_writes_performed": false,
              "persistent_memory_write_performed": false
            },

## Chunk content

```json
            "telemetry": {
              "kind": "full0to10_provider_governor_telemetry",
              "passed": true,
              "event_count": 4,
              "events": [
                {
                  "event": "accelerator_control",
                  "passed": true,
                  "severity": "info",
                  "structural": true,
                  "details": {
                    "score": 92
                  },
                  "timestamp": "2026-05-07T11:33:39.899989+00:00"
                },
                {
                  "event": "quality_gate_observed",
                  "passed": true,
                  "severity": "info",
                  "structural": false,
                  "details": {
                    "quality_gate_passed": true
                  },
                  "timestamp": "2026-05-07T11:33:39.899989+00:00"
                },
                {
                  "event": "policy_decision",
                  "passed": true,
                  "severity": "info",
                  "structural": false,
                  "details": {
                    "policy_passed": false,
                    "operator_intent": false
                  },
                  "timestamp": "2026-05-07T11:33:39.899989+00:00"
                },
                {
                  "event": "run_permit_decision",
                  "passed": true,
                  "severity": "info",
                  "structural": false,
                  "details": {
                    "permit_allowed": false,
                    "decision": "deny"
                  },
                  "timestamp": "2026-05-07T11:33:39.899989+00:00"
                }
              ],
              "structural_failure_count": 0,
              "policy_denial_event_count": 0,
              "errors": [],
              "warnings": [],
              "provider_execution_performed": false,
              "patch_application_performed": false,
              "source_writes_performed": false,
              "persistent_memory_write_performed": false
            },
            "errors": [],
            "warnings": [
              "permit denied by policy; artifact generation is still valid"
            ],
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "source_writes_performed": false,
            "persistent_memory_write_performed": false,
            "outputs": {
              "governor": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_governor.json",
              "permit": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_run_permit.json",
              "telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_governor_telemetry.json",
              "markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/provider_governor/full0to10_provider_governor.md"
            }
          },
          "workload_report_contract": {
            "kind": "full0to10_provider_workload_report_contract",
            "passed": true,
            "provider_lane": "ollama_gpu",
            "permit_required": true,
            "permit_decision": "deny",
            "permit_allowed": false,
            "reports_required_after_real_run": [
              "ollama_gpu_real_workload_report.md",
              "full0to10_provider_runtime_telemetry.json",
              "full0to10_provider_recommendations.json"
            ],
            "minimum_content_requirements": [
              "provider lane",
              "model name",
              "GPU visibility",
              "input evidence references",
              "recommendations",
              "tool usage telemetry",
              "no patch applied flag"
            ],
            "quality_validator": "Tools/validation/check_ai_workload_report_quality.py --report-dir",
            "failure_policy": {
              "missing_report": "block_bundle_promotion",
              "unusable_report": "block_primary_advisory",
              "patch_application_detected": "hard_fail"
            },
            "notes": [
              "This contract does not execute provider generation.",
              "The real run must satisfy this contract before bundle promotion."
            ],
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "source_writes_performed": false,
            "persistent_memory_write_performed": false
          },
          "expected_telemetry_contract": {
            "kind": "full0to10_provider_expected_telemetry_contract",
            "passed": true,
            "provider_lane": "ollama_gpu",
            "budget": {
              "max_minutes": 20,
              "max_rounds": 8,
              "max_new_tokens": 2400,
              "keep_alive": "20m"
            },
            "events_required": [
              "provider_invocation_requested",
              "permit_loaded",
              "quality_gate_loaded",
              "gpu_capability_loaded",
              "prompt_or_context_bound",
              "provider_started",
              "provider_completed_or_failed",
              "workload_report_written",
              "runtime_telemetry_written",
              "npu_audit_scheduled"
            ],
            "fields_required": [
              "timestamp",
              "provider_lane",
              "model",
              "permit_decision",
              "generation_enabled",
              "duration_ms",
              "exit_code",
              "output_paths"
            ],
            "forbidden_flags": {
              "patch_application_performed": true,
              "blender_runtime_performed": true,
              "ffmpeg_runtime_performed": true
            },
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "source_writes_performed": false,
            "persistent_memory_write_performed": false
          },
          "npu_audit_hooks": {
            "kind": "full0to10_provider_npu_audit_hooks",
            "passed": true,
            "auditor_lane": "openvino_npu",
            "diagnostic_lane": "openvino_gpu0",
            "before_provider": [
              "verify permit",
              "verify evidence index",
              "verify GPU lane is primary only by permit"
            ],
            "after_provider": [
              "compare provider recommendations to memory evidence",
              "verify no patch apply occurred",
              "verify GPU.0 did not become primary",
              "verify telemetry completeness"
            ],
            "sample_count": 3,
            "promotion_allowed": false,
            "model_load_required_for_dry_run": false,
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "source_writes_performed": false,
            "persistent_memory_write_performed": false
          },
          "dry_run_steps": {
            "kind": "full0to10_provider_dry_run_steps",
            "passed": true,
            "provider_lane": "ollama_gpu",
            "permit_decision": "deny",
            "permit_allowed": false,
            "generation_would_execute": false,
            "steps": [
              {
                "index": 1,
                "name": "load_permit",
                "action": "read provider_run_permit.json",
                "executes_provider": false
              },
              {
                "index": 2,
                "name": "load_quality_gate",
                "action": "read final product quality gate evidence",
                "executes_provider": false
              },
              {
                "index": 3,
                "name": "load_accelerator_control",
                "action": "read GPU body/mind and scheduler",
                "executes_provider": false
              },
              {
                "index": 4,
                "name": "bind_context",
                "action": "bind SQLite/memory/final-product evidence",
                "executes_provider": false
              },
              {
                "index": 5,
                "name": "prepare_provider_command",
                "action": "prepare Ollama/GPU command but do not execute",
                "executes_provider": false
              },
              {
                "index": 6,
                "name": "prepare_workload_report_paths",
                "action": "reserve output paths for workload report and telemetry",
                "executes_provider": false
              },
              {
                "index": 7,
                "name": "prepare_npu_audit_hooks",
                "action": "schedule before/after NPU audit hooks",
                "executes_provider": false
              },
              {
                "index": 8,
                "name": "deny_or_wait",
                "action": "stop unless a future explicit real-run flag is supplied",
                "executes_provider": false
              }
            ],
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "source_writes_performed": false,
            "persistent_memory_write_performed": false
          },
          "readiness": {
            "kind": "full0to10_provider_invocation_plan_readiness",
            "passed": true,
            "score": 100,
            "ready_for_bundle_inclusion": true,
            "ready_for_real_generation": false,
            "blockers": [],
            "warnings": [
              "permit_denied_valid_for_dry_run_plan"
            ],
            "provider_execution_performed": false,
            "patch_application_performed": false,
            "source_writes_performed": false,
            "persistent_memory_write_performed": false
          },
          "errors": [],
          "warnings": [
            "permit_denied_valid_for_dry_run_plan"
          ],
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "source_writes_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "provider_workload_report_contract": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_workload_report_contract.json",
        "exists": true,
        "type": "json",
        "required": true,
        "size_bytes": 1198,
        "json": {
          "kind": "full0to10_provider_workload_report_contract",
          "passed": true,
          "provider_lane": "ollama_gpu",
          "permit_required": true,
          "permit_decision": "deny",
          "permit_allowed": false,
          "reports_required_after_real_run": [
            "ollama_gpu_real_workload_report.md",
            "full0to10_provider_runtime_telemetry.json",
            "full0to10_provider_recommendations.json"
          ],
          "minimum_content_requirements": [
            "provider lane",
            "model name",
            "GPU visibility",
            "input evidence references",
            "recommendations",
            "tool usage telemetry",
            "no patch applied flag"
          ],
          "quality_validator": "Tools/validation/check_ai_workload_report_quality.py --report-dir",
          "failure_policy": {
            "missing_report": "block_bundle_promotion",
            "unusable_report": "block_primary_advisory",
            "patch_application_detected": "hard_fail"
          },
          "notes": [
            "This contract does not execute provider generation.",
```

## Context after

            "The real run must satisfy this contract before bundle promotion."
          ],
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "source_writes_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "provider_expected_telemetry_contract": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_expected_telemetry_contract.json",
        "exists": true,
        "type": "json",
