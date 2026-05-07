# Evidence Chunk 0013/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `3300`
- line_end: `3570`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0012.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0014.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifacts. Preview: "The real run must satisfy this contract before bundle promotion." ], "provider_execution_performed": false, "patch_application_performed": false, "source_writes_performed": false, "persistent_memory_write_performed": false } }, "provider_expected_telemetry_co...

## Context before

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

## Chunk content

```json
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
        "required": true,
        "size_bytes": 1085,
        "json": {
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
        }
      },
      "provider_execution_bridge": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge.json",
        "exists": true,
        "type": "json",
        "required": true,
        "size_bytes": 45251,
        "json": {
          "kind": "full0to10_provider_execution_bridge",
          "passed": true,
          "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
          "operator_intent": false,
          "allow_provider_generation_requested": false,
          "provider_invocation_plan": {
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
                  "generated_at": "2026-05-07T11:33:39.914759+00:00",
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
                      "passed": false,
                      "reason": "external probes disabled"
                    }
                  },
                  "openvino_devices": [],
                  "openvino_cpu": {
                    "device": "CPU",
                    "device_visible": false,
                    "role": "host_fallback_and_baseline",
                    "primary_advisory_allowed": false
                  },
                  "openvino_gpu0": {
                    "device": "GPU.0",
                    "device_visible": false,
                    "role": "secondary_diagnostic_only",
                    "primary_advisory_allowed": false
                  },
                  "openvino_gpu1": {
                    "device": "GPU.1",
                    "device_visible": false,
                    "role": "secondary_diagnostic_only",
                    "primary_advisory_allowed": false
                  },
                  "openvino_npu": {
                    "device": "NPU",
                    "device_visible": false,
                    "role": "sampled_auditor_or_diagnostic",
                    "primary_advisory_allowed": false
                  },
                  "npu": {
                    "lane": "npu_openvino",
                    "probe_performed": false,
                    "model_load_performed": false,
                    "generation_performed": false,
                    "result": {
                      "requested": [
                        "C:\\Users\\carmi\\blender\\blender-audio-project\\.venv\\Scripts\\python.exe",
                        "-c",
                        "import json\ntry:\n import openvino as ov\n core=ov.Core()\n print(json.dumps({'import_ok': True, 'devices': list(core.available_devices)}))\nexcept Exception as exc:\n print(json.dumps({'import_ok': False, 'error': type(exc).__name__ + ': ' + str(exc)}))\n"
                      ],
                      "skipped": true,
                      "passed": false,
                      "reason": "external probes disabled"
                    },
                    "devices": [],
                    "normalized_devices": [],
                    "device_visible": false,
                    "role": "sampled_auditor_or_diagnostic",
                    "primary_advisory_allowed": false
                  },
```

## Context after

                  "errors": [],
                  "warnings": []
                },
                "gpu_body": {
                  "kind": "gpu_body_contract",
                  "role": "primary_compute_body_when_available",
                  "owns": [
                    "device_visibility",
                    "memory_budget",
                    "thermal_and_driver_state",
                    "process_ownership",
                    "runtime_telemetry"
