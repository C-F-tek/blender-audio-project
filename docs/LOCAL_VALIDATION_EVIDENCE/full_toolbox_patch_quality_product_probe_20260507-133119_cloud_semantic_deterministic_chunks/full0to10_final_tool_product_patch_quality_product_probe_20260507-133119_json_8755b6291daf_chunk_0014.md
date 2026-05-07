# Evidence Chunk 0014/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `3571`
- line_end: `3831`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0013.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0015.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifacts. Preview: "errors": [], "warnings": [] }, "gpu_body": { "kind": "gpu_body_contract", "role": "primary_compute_body_when_available", "owns": [ "device_visibility", "memory_budget", "thermal_and_driver_state", "process_ownership", "runtime_telemetry" ], "command_available...

## Context before

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

## Chunk content

```json
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
                      "reason": "deterministic local context lane",
                      "priority": 10
                    },
                    {
                      "lane": "runtime_tools",
                      "allowed": true,
                      "reason": "local telemetry-capable tool lane",
                      "priority": 20
                    },
                    {
                      "lane": "ollama_gpu",
                      "allowed": false,
                      "reason": "requires explicit RunLauncher and quality gates",
                      "priority": 30
                    },
                    {
                      "lane": "openvino_npu",
                      "allowed": false,
                      "reason": "auditor/diagnostic only until promoted",
                      "priority": 60
                    },
                    {
                      "lane": "openvino_gpu0",
                      "allowed": false,
                      "reason": "secondary diagnostic only until promoted",
                      "priority": 70
                    }
                  ],
                  "routing_rules": [
                    "memory and tool lanes run before provider generation",
                    "GPU advisory cannot start without explicit launcher",
                    "NPU can disagree or audit, not lead by default",
                    "GPU.0 cannot take the primary GPU lane implicitly",
                    "quality product package must exist before real run"
                  ],
                  "gpu_mind_policy": {
                    "may_generate": false,
                    "requires_run_launcher": true,
                    "requires_quality_gate_clean": true,
                    "requires_workload_quality_passed": true,
                    "requires_operator_intent": true
                  },
                  "npu_role": "sampled_auditor_or_diagnostic",
                  "gpu0_role": "secondary_diagnostic_accelerator"
                },
                "errors": [],
                "warnings": [],
                "provider_execution_performed": false,
                "patch_application_performed": false,
                "source_writes_performed": false,
                "persistent_memory_write_performed": false,
                "readiness": {
                  "kind": "full0to10_accelerator_readiness",
                  "passed": true,
                  "score": 92,
                  "ready_for_product_package": true,
                  "ready_for_real_provider_generation": false,
                  "blockers": [],
                  "warnings": [
                    "npu_not_visible_or_probe_disabled"
                  ],
                  "provider_execution_performed": false,
                  "patch_application_performed": false,
                  "source_writes_performed": false,
                  "persistent_memory_write_performed": false
                },
                "outputs": {
                  "control": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_control.json",
                  "telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_telemetry.json",
                  "markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/provider_governor/accelerator_control/full0to10_accelerator_control.md"
                }
              },
              "quality_gate": {
                "kind": "full0to10_quality_gate",
                "generated_at": "2026-05-07T11:33:40.644918+00:00",
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
```

## Context after

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
