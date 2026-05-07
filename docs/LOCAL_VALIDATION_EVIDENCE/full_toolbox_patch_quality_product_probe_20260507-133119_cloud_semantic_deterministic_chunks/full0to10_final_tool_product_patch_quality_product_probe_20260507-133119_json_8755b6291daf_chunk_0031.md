# Evidence Chunk 0031/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `8135`
- line_end: `8450`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0030.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0032.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: provider_invocation_plan. Preview: "kind": "full0to10_provider_run_permit", "passed": true, "valid_result": true, "permit_allowed": false, "allow_provider_generation_requested": false, "decision": "deny", "decision_is_failure": false, "failed_requirements": [ { "requirement": "operator_intent",...

## Context before

            "check for excessive GPU claim",
            "check if GPU.0 tries to become primary",
            "check if patch plan is generated without explicit approval"
          ],
          "audit_samples": {
            "before_generation": true,
            "during_generation": false,
            "after_generation": true
          },
          "promotion_allowed": false
        },
        "run_permit": {

## Chunk content

```json
          "kind": "full0to10_provider_run_permit",
          "passed": true,
          "valid_result": true,
          "permit_allowed": false,
          "allow_provider_generation_requested": false,
          "decision": "deny",
          "decision_is_failure": false,
          "failed_requirements": [
            {
              "requirement": "operator_intent",
              "passed": false,
              "reason": "explicit -OperatorIntent is required"
            }
          ],
          "budget": {
            "kind": "full0to10_provider_budget_plan",
            "passed": true,
            "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
            "budgets": {
              "ollama_gpu": {
                "max_minutes": 20,
                "max_rounds": 8,
                "max_new_tokens": 2400,
                "keep_alive": "20m"
              },
              "openvino_npu": {
                "max_samples": 3,
                "model_load_required": false,
                "audit_only": true
              },
              "openvino_gpu0": {
                "max_samples": 2,
                "diagnostic_only": true,
                "promotion_required": true
              }
            },
            "global_limits": {
              "no_generation_without_permit": true,
              "no_patch_apply_from_provider": true,
              "no_blender_runtime": true,
              "no_ffmpeg_runtime": true,
              "output_only_under_output_validation": true
            },
            "budget_order": [
              "sqlite_memory_and_tools_first",
              "quality_gate_second",
              "accelerator_control_third",
              "permit_decision_fourth",
              "provider_generation_only_after_explicit_future_run"
            ]
          },
          "npu_audit": {
            "kind": "full0to10_npu_audit_plan",
            "passed": true,
            "npu_role": "sampled_auditor_or_diagnostic",
            "npu_device_visible": false,
            "gpu0_role": "secondary_diagnostic_accelerator",
            "audit_points": [
              "compare provider recommendation with memory/tool evidence",
              "check for missing telemetry",
              "check for excessive GPU claim",
              "check if GPU.0 tries to become primary",
              "check if patch plan is generated without explicit approval"
            ],
            "audit_samples": {
              "before_generation": true,
              "during_generation": false,
              "after_generation": true
            },
            "promotion_allowed": false
          },
          "execution_contract": {
            "this_report_executes_provider": false,
            "future_provider_run_requires_this_permit": true,
            "provider_generation_must_write_workload_report": true,
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
              "timestamp": "2026-05-07T11:33:40.644918+00:00"
            },
            {
              "event": "quality_gate_observed",
              "passed": true,
              "severity": "info",
              "structural": false,
              "details": {
                "quality_gate_passed": true
              },
              "timestamp": "2026-05-07T11:33:40.644918+00:00"
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
              "timestamp": "2026-05-07T11:33:40.644918+00:00"
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
              "timestamp": "2026-05-07T11:33:40.644918+00:00"
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
          "governor": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_governor.json",
          "permit": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_run_permit.json",
          "telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_governor_telemetry.json",
          "markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/full0to10_provider_governor.md"
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
```

## Context after

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
