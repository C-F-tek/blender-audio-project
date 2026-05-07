# Evidence Chunk 0005/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `914`
- line_end: `1240`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0004.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0006.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifacts. Preview: "json": { "kind": "full0to10_quality_gate", "generated_at": "2026-05-07T11:33:41.410835+00:00", "passed": true, "provider_execution_performed": false, "patch_application_performed": false, "source_writes_performed": false, "persistent_memory_write_performed": ...

## Context before

          "provider_execution_performed": false,
          "patch_application_performed": false,
          "source_writes_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "quality_gate": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/quality_gate/full0to10_quality_gate.json",
        "exists": true,
        "type": "json",
        "required": true,
        "size_bytes": 3621,

## Chunk content

```json
        "json": {
          "kind": "full0to10_quality_gate",
          "generated_at": "2026-05-07T11:33:41.410835+00:00",
          "passed": true,
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "source_writes_performed": false,
          "persistent_memory_write_performed": false,
          "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
          "main_objective": [
            "SQLite FTS5 memory",
            "runtime tool usage",
            "GPU/Ollama readiness",
            "NPU/OpenVINO GPU.0 contract",
            "bundle telemetry/capability quality"
          ],
          "checks": {
            "required_scripts": {
              "passed": true,
              "missing": [],
              "records": [
                {
                  "path": "Tools/ai/full0to10_memory_tool.py",
                  "exists": true,
                  "lines": 101
                },
                {
                  "path": "Tools/ai/full0to10_runtime_tool.py",
                  "exists": true,
                  "lines": 55
                },
                {
                  "path": "Tools/ai/build_full0to10_runtime_tool_registry.py",
                  "exists": true,
                  "lines": 41
                },
                {
                  "path": "Tools/ai/build_full0to10_hardware_tool_capability.py",
                  "exists": true,
                  "lines": 47
                },
                {
                  "path": "Tools/ai/build_full0to10_run_manifest.py",
                  "exists": true,
                  "lines": 47
                },
                {
                  "path": "Tools/validation/check_full0to10_bundle_contracts.py",
                  "exists": true,
                  "lines": 49
                },
                {
                  "path": "Tools/workflow/run_full0to10_manifest_contract_gate.ps1",
                  "exists": true,
                  "lines": 72
                },
                {
                  "path": "Tools/workflow/run_unified_full0to10_with_contract_gate.ps1",
                  "exists": true,
                  "lines": 95
                },
                {
                  "path": "Tools/ai/build_full0to10_auto_refactor_plan.py",
                  "exists": true,
                  "lines": 50
                },
                {
                  "path": "Tools/ai/apply_full0to10_auto_refactor_patch_specs.py",
                  "exists": true,
                  "lines": 49
                },
                {
                  "path": "Tools/ai/apply_full0to10_markdown_split_patch_specs.py",
                  "exists": true,
                  "lines": 53
                }
              ]
            },
            "md_split_quarantine": {
              "passed": true,
              "source_side_md_split_count": 0,
              "source_side_md_split_dirs": []
            },
            "report_visibility": {
              "passed": false,
              "missing_report_roles": [
                "hardware_capability",
                "runtime_tool_registry",
                "sqlite_memory",
                "manifest_gate",
                "contract_gate"
              ],
              "found_report_counts": {
                "hardware_capability": 0,
                "runtime_tool_registry": 0,
                "sqlite_memory": 0,
                "manifest_gate": 0,
                "contract_gate": 0
              },
              "found_reports": {
                "hardware_capability": [],
                "runtime_tool_registry": [],
                "sqlite_memory": [],
                "manifest_gate": [],
                "contract_gate": []
              }
            }
          },
          "split_advisory": {
            "spec_count": 0,
            "kind_counts": {},
            "useful_markdown_splits": [],
            "useful_code_splits": [],
            "hardware_contract_suggestions": [],
            "advisory_only": true,
            "apply_performed": false
          },
          "readiness": {
            "score": 85,
            "ready_for_real_run": true,
            "blockers": [],
            "warnings": [
              "some_recent_quality_reports_not_visible",
              "no_refactor_patch_specs_supplied"
            ]
          },
          "errors": [],
          "warnings": [
            "some_recent_quality_reports_not_visible",
            "no_refactor_patch_specs_supplied"
          ]
        }
      },
      "accelerator_control": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/accelerator_control/full0to10_accelerator_control.json",
        "exists": true,
        "type": "json",
        "required": true,
        "size_bytes": 11433,
        "json": {
          "kind": "full0to10_accelerator_control",
          "passed": true,
          "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
          "hardware_capability": {
            "kind": "full0to10_hardware_tool_capability",
            "generated_at": "2026-05-07T11:33:38.129136+00:00",
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
            "errors": [],
            "warnings": []
          },
          "gpu_body": {
```

## Context after

            "kind": "gpu_body_contract",
            "role": "primary_compute_body_when_available",
            "owns": [
              "device_visibility",
              "memory_budget",
              "thermal_and_driver_state",
              "process_ownership",
              "runtime_telemetry"
            ],
            "command_available": true,
            "device_query": null,
            "driver_visible": true,
