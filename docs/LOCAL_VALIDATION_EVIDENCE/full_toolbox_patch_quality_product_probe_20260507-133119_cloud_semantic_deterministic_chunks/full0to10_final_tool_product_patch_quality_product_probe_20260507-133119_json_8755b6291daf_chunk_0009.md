# Evidence Chunk 0009/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `2145`
- line_end: `2434`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0008.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0010.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifacts. Preview: "severity": "info", "structural": false, "details": { "quality_gate_passed": true }, "timestamp": "2026-05-07T11:33:39.091040+00:00" }, { "event": "policy_decision", "passed": true, "severity": "info", "structural": false, "details": { "policy_passed": false, ...

## Context before

                "event": "accelerator_control",
                "passed": true,
                "severity": "info",
                "structural": true,
                "details": {
                  "score": 92
                },
                "timestamp": "2026-05-07T11:33:39.091040+00:00"
              },
              {
                "event": "quality_gate_observed",
                "passed": true,

## Chunk content

```json
                "severity": "info",
                "structural": false,
                "details": {
                  "quality_gate_passed": true
                },
                "timestamp": "2026-05-07T11:33:39.091040+00:00"
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
                "timestamp": "2026-05-07T11:33:39.091040+00:00"
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
                "timestamp": "2026-05-07T11:33:39.091040+00:00"
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
          "persistent_memory_write_performed": false
        }
      },
      "provider_run_permit": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_run_permit.json",
        "exists": true,
        "type": "json",
        "required": true,
        "size_bytes": 2851,
        "json": {
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
        }
      },
      "provider_invocation_plan": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_invocation_plan.json",
        "exists": true,
        "type": "json",
        "required": true,
        "size_bytes": 33956,
        "json": {
          "kind": "full0to10_provider_invocation_plan",
          "passed": true,
          "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
          "provider_lane": "ollama_gpu",
          "permit_decision": "deny",
          "permit_allowed": false,
          "generation_executes_now": false,
          "governor": {
            "kind": "full0to10_provider_governor",
            "passed": true,
            "valid_result": true,
            "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
            "operator_intent": false,
            "allow_provider_generation_requested": false,
            "decision": "deny",
            "permit_allowed": false,
            "deny_is_failure": false,
            "accelerator_control": {
              "kind": "full0to10_accelerator_control",
              "passed": true,
              "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
              "hardware_capability": {
                "kind": "full0to10_hardware_tool_capability",
                "generated_at": "2026-05-07T11:33:39.106140+00:00",
                "passed": true,
                "provider_execution_performed": false,
                "patch_application_performed": false,
                "source_writes_performed": false,
                "persistent_memory_write_performed": false,
                "external_probes_enabled": false,
                "python": {
                  "executable": "C:\\Users\\carmi\\blender\\blender-audio-project\\.venv\\Scripts\\python.exe",
                  "version": "3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]",
                  "version_info": [
                    3,
                    12,
                    10
                  ],
                  "platform": "Windows-11-10.0.26200-SP0",
                  "machine": "AMD64",
                  "processor": "Intel64 Family 6 Model 198 Stepping 2, GenuineIntel"
                },
                "tool_inventory": {
                  "passed": true,
                  "tool_count": 11,
                  "missing": [],
                  "tools": [
                    {
                      "path": "Tools/ai/agent_runtime_tool_broker.py",
                      "exists": true,
                      "lines": 759,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/ai/agent_runtime_sqlite_memory.py",
                      "exists": true,
                      "lines": 527,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/ai/build_runtime_tool_capability_manifest.py",
                      "exists": true,
                      "lines": 289,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/ai/build_runtime_tool_usage_telemetry.py",
                      "exists": true,
                      "lines": 823,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/ai/build_full0to10_run_manifest.py",
                      "exists": true,
                      "lines": 47,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
                      "exists": true,
                      "lines": 1100,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
                      "exists": true,
                      "lines": 2263,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/ai/run_agent_gpu_deep_planning_supervised.py",
                      "exists": true,
                      "lines": 1180,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/ai/check_local_resource_lanes.py",
                      "exists": true,
                      "lines": 335,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/ai/check_npu_provider_environment.py",
                      "exists": true,
                      "lines": 189,
                      "git_trackable": true
                    },
                    {
                      "path": "Tools/validation/check_full0to10_bundle_contracts.py",
                      "exists": true,
                      "lines": 49,
                      "git_trackable": true
                    }
                  ]
                },
                "gpu": {
                  "lane": "gpu_nvidia",
                  "command_available": true,
                  "probe_performed": false,
                  "provider_execution_performed": false,
                  "generation_performed": false,
                  "result": {
                    "requested": [
                      "nvidia-smi",
                      "--query-gpu=name,driver_version,memory.total",
                      "--format=csv,noheader"
                    ],
                    "skipped": true,
                    "passed": false,
                    "reason": "external probes disabled"
                  }
                },
                "ollama": {
                  "lane": "ollama",
                  "command_available": true,
                  "generation_performed": false,
                  "list": {
                    "requested": [
                      "ollama",
```

## Context after

                      "list"
                    ],
                    "skipped": true,
                    "passed": false,
                    "reason": "external probes disabled"
                  },
                  "ps": {
                    "requested": [
                      "ollama",
                      "ps"
                    ],
                    "skipped": true,
