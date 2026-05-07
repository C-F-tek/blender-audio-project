# Evidence Chunk 0029/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `7513`
- line_end: `7817`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0028.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0030.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: provider_invocation_plan. Preview: "provider_invocation_plan": { "kind": "full0to10_provider_invocation_plan", "passed": true, "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patc...

## Context before

      "workload_contract": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_workload_report_contract.json",
      "telemetry_contract": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_expected_telemetry_contract.json",
      "dry_run_steps": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_dry_run_steps.json",
      "markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_invocation_plan/full0to10_provider_invocation_plan.md"
    }
  },
  "provider_execution_bridge": {
    "kind": "full0to10_provider_execution_bridge",
    "passed": true,
    "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
    "operator_intent": false,
    "allow_provider_generation_requested": false,

## Chunk content

```json
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
            ],
            "command_available": true,
            "device_query": null,
            "driver_visible": true,
            "memory_budget_policy": {
              "reserve_for_blender": true,
              "avoid_unbounded_context_growth": true,
              "prefer_telemetry_before_generation": true
            },
            "process_ownership_policy": {
              "ollama_gpu_advisory_is_primary_when_enabled": true,
              "openvino_gpu0_secondary_until_promoted": true,
              "no_untracked_gpu_consumers": true
            },
            "required_telemetry": [
              "gpu command availability",
              "provider lane using GPU",
              "generation enabled flag",
              "quality gate status"
            ],
            "passed": true
          },
          "gpu_mind": {
            "kind": "gpu_mind_contract",
            "passed": true,
            "role": "primary_advisory_mind_when_explicit",
            "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
            "owns": [
              "advisory_policy",
              "provider_selection",
              "quality_gate_awareness",
              "fallback_reasoning",
              "no_implicit_generation"
            ],
            "decision_policy": {
              "may_generate": false,
              "requires_run_launcher": true,
              "requires_quality_gate_clean": true,
              "requires_workload_quality_passed": true,
              "requires_operator_intent": true
            },
            "fallback_policy": {
              "if_gpu_unavailable": "use report-only memory/tool product",
              "if_ollama_unavailable": "keep advisory disabled",
              "if_quality_gate_blocked": "produce blockers not generation"
            },
            "confidence": "prepared"
          },
          "npu_auditor": {
            "kind": "npu_auditor_contract",
            "passed": true,
            "role": "sampled_auditor_or_diagnostic",
            "device_visible": false,
            "normalized_devices": [],
            "probe_performed": false,
            "allowed_actions": [
              "sampled review",
              "diagnostic evidence",
              "provider disagreement audit",
              "quality gate cross-check"
            ],
            "blocked_actions": [
              "primary advisory by default",
              "implicit model loading",
              "patch application",
              "runtime generation without explicit promotion"
            ],
            "promotion_requirements": [
              "dedicated patch",
              "smoke evidence",
              "quality stack approval",
              "operator explicit request"
            ]
          },
          "openvino_gpu0": {
            "kind": "openvino_gpu0_contract",
            "passed": true,
            "role": "secondary_diagnostic_accelerator",
            "device_visible": false,
            "normalized_devices": [],
            "gpu_devices": [],
            "relationship_to_primary_gpu": "must_not_steal_ollama_gpu_lane",
            "allowed_actions": [
              "OpenVINO diagnostic",
              "capability listing",
              "secondary audit",
              "future promoted workload only with explicit patch"
            ],
            "blocked_actions": [
              "primary advisory default",
              "silent GPU provider takeover",
```

## Context after

              "implicit generation"
            ]
          },
          "scheduler": {
            "kind": "accelerator_scheduler_policy",
            "passed": true,
            "generation_allowed": false,
            "default_mode": "quality_and_evidence_only",
            "lanes": [
              {
                "lane": "sqlite_fts5_memory",
                "allowed": true,
