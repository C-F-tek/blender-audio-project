# Evidence Chunk 0004/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `599`
- line_end: `913`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0003.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0005.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifacts. Preview: "hardening": [ "no_primary_advisory_default", "model_load_not_required_for_preflight" ] }, "openvino_gpu0": { "role": "secondary_diagnostic_gpu0", "primary": false, "execution": "diagnostic_only_until_promoted", "hardening": [ "document_gpu0_relationship", "do...

## Context before

              "primary": false,
              "execution": "explicit_provider_only",
              "hardening": [
                "no_implicit_generation",
                "quality_preflight_required",
                "gpu_telemetry_required"
              ]
            },
            "openvino_npu": {
              "role": "sampled_auditor_or_diagnostic",
              "primary": false,
              "execution": "explicit_probe_or_sample_only",

## Chunk content

```json
              "hardening": [
                "no_primary_advisory_default",
                "model_load_not_required_for_preflight"
              ]
            },
            "openvino_gpu0": {
              "role": "secondary_diagnostic_gpu0",
              "primary": false,
              "execution": "diagnostic_only_until_promoted",
              "hardening": [
                "document_gpu0_relationship",
                "do_not_steal_primary_gpu_lane"
              ]
            }
          },
          "hardware_capability": {
            "kind": "full0to10_hardware_tool_capability",
            "generated_at": "2026-05-07T11:33:40.667958+00:00",
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
          "optimization_policy": {
            "gpu": "optimize visibility and telemetry before generation",
            "npu": "use as sampled auditor/diagnostic, not primary advisory",
            "gpu0": "keep OpenVINO GPU.0 secondary unless explicitly promoted",
            "ollama": "list/ps/probe safe; generation requires explicit run lane"
          },
          "errors": [],
          "warnings": [],
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "source_writes_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "tool_telemetry": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_tool_telemetry.json",
        "exists": true,
        "type": "json",
        "required": true,
        "size_bytes": 1379,
        "json": {
          "kind": "full0to10_effective_use_tool_telemetry",
          "passed": true,
          "tool_count": 4,
          "event_count": 5,
          "tools": [
            "hardware_capability",
            "optimizer",
            "quality_product",
            "sqlite_memory"
          ],
          "events": [
            {
              "tool": "hardware_capability",
              "action": "build_provider_contracts",
              "passed": true,
              "details": {},
              "timestamp": "2026-05-07T11:33:40.667958+00:00"
            },
            {
              "tool": "optimizer",
              "action": "build_optimization",
              "passed": true,
              "details": {},
              "timestamp": "2026-05-07T11:33:40.667958+00:00"
            },
            {
              "tool": "sqlite_memory",
              "action": "seed_context",
              "passed": true,
              "details": {},
              "timestamp": "2026-05-07T11:33:40.680970+00:00"
            },
            {
              "tool": "sqlite_memory",
              "action": "search_context",
              "passed": true,
              "details": {},
              "timestamp": "2026-05-07T11:33:40.680970+00:00"
            },
            {
              "tool": "quality_product",
              "action": "render_markdown",
              "passed": true,
              "details": {},
              "timestamp": "2026-05-07T11:33:40.680970+00:00"
            }
          ],
          "errors": [],
          "warnings": [],
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "source_writes_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "optimization": {
        "path": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_optimization.json",
        "exists": true,
        "type": "json",
        "required": true,
        "size_bytes": 1206,
        "json": {
          "kind": "full0to10_effective_use_optimization",
          "passed": true,
          "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
          "scores": {
            "sqlite_memory_effective_use": 95,
            "runtime_tool_telemetry": 90,
            "gpu_ollama_hardening": 85,
            "npu_gpu0_contract": 88,
            "real_run_readiness": 65
          },
          "next_actions": [
            "Run quality supervisor in quality-only mode before provider generation.",
            "Use SQLite memory product output as evidence in the next bundle.",
            "Require runtime tool telemetry for every memory/tool operation.",
            "Keep NPU as sampled auditor unless a dedicated promotion patch passes.",
            "Keep OpenVINO GPU.0 diagnostic/secondary until explicit contract patch.",
            "Only run Ollama/GPU advisory after workload quality validator passes."
          ],
          "warnings": [
            "NPU probe not performed or disabled"
          ],
          "errors": [],
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
```

## Context after

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
