# Evidence Chunk 0032/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `8451`
- line_end: `8715`
- section_kinds: `['json_key_section', 'json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0031.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0033.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: provider_invocation_plan; real_run_gate; command_plan; workload_output_paths; telemetry. Preview: } ], "provider_execution_performed": false, "patch_application_performed": false, "source_writes_performed": false, "persistent_memory_write_performed": false }, "readiness": { "kind": "full0to10_provider_invocation_plan_readiness", "passed": true, "score": 10...

## Context before

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

## Chunk content

```json
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
      "persistent_memory_write_performed": false,
      "outputs": {
        "plan": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_invocation_plan.json",
        "workload_contract": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_workload_report_contract.json",
        "telemetry_contract": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_expected_telemetry_contract.json",
        "dry_run_steps": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_dry_run_steps.json",
        "markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/provider_invocation_plan/full0to10_provider_invocation_plan.md"
      }
    },
    "real_run_gate": {
      "kind": "full0to10_provider_real_run_gate",
      "passed": true,
      "real_run_allowed": false,
      "real_run_requested": false,
      "requirements": [
        {
          "requirement": "operator_intent",
          "passed": false,
          "reason": "explicit operator intent required"
        },
        {
          "requirement": "allow_provider_generation",
          "passed": false,
          "reason": "real generation flag required"
        },
        {
          "requirement": "permit_allowed",
          "passed": false,
          "reason": "provider run permit must allow generation"
        },
        {
          "requirement": "dry_run_plan_ready",
          "passed": true,
          "reason": "dry-run plan must be bundle-ready"
        },
        {
          "requirement": "workload_contract_ready",
          "passed": true,
          "reason": "workload report contract must pass"
        },
        {
          "requirement": "telemetry_contract_ready",
          "passed": true,
          "reason": "telemetry contract must pass"
        },
        {
          "requirement": "npu_audit_hooks_ready",
          "passed": true,
          "reason": "NPU audit hooks must pass"
        },
        {
          "requirement": "quality_gate_acknowledged",
          "passed": true,
          "reason": "quality gate is captured as evidence, not overridden"
        }
      ],
      "failed_requirements": [
        {
          "requirement": "operator_intent",
          "passed": false,
          "reason": "explicit operator intent required"
        },
        {
          "requirement": "allow_provider_generation",
          "passed": false,
          "reason": "real generation flag required"
        },
        {
          "requirement": "permit_allowed",
          "passed": false,
          "reason": "provider run permit must allow generation"
        }
      ],
      "decision": "block_real_run",
      "deny_is_failure": false,
      "errors": [],
      "warnings": [
        "real provider run blocked by gate"
      ],
      "provider_execution_performed": false,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "persistent_memory_write_performed": false
    },
    "command_plan": {
      "kind": "full0to10_provider_command_plan",
      "passed": true,
      "real_run_gate_decision": "block_real_run",
      "commands": [
        {
          "name": "ollama_gpu_primary_advisory",
          "provider_lane": "ollama_gpu",
          "would_execute": false,
          "requires_gate_allowed": true,
          "budget": {
            "max_minutes": 20,
            "max_rounds": 8,
            "max_new_tokens": 2400,
            "keep_alive": "20m"
          },
          "expected_outputs": [
            "ollama_gpu_real_workload_report.md",
            "full0to10_provider_runtime_telemetry.json",
            "full0to10_provider_recommendations.json"
          ]
        },
        {
          "name": "npu_after_run_audit",
          "provider_lane": "openvino_npu",
          "would_execute": false,
          "requires_primary_output": true,
          "audit_hooks": [
            "compare provider recommendations to memory evidence",
            "verify no patch apply occurred",
            "verify GPU.0 did not become primary",
            "verify telemetry completeness"
          ]
        },
        {
          "name": "gpu0_diagnostic_probe",
          "provider_lane": "openvino_gpu0",
          "would_execute": false,
          "requires_promotion": true,
          "reason": "GPU.0 remains secondary diagnostic"
        }
      ],
      "all_commands_are_non_executing": true,
      "future_execution_flag_required": true,
      "provider_execution_performed": false,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "persistent_memory_write_performed": false
    },
    "workload_output_paths": {
      "kind": "full0to10_provider_workload_output_paths",
      "passed": true,
      "workload_dir": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs",
      "paths": {
        "ollama_workload_report": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/ollama_gpu_real_workload_report.md",
        "runtime_telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/full0to10_provider_runtime_telemetry.json",
        "recommendations": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/full0to10_provider_recommendations.json",
        "npu_audit_report": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/full0to10_npu_after_run_audit.json",
        "quality_validation": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs/ai_workload_report_quality.json"
      },
      "write_policy": {
        "future_real_run_only": true,
        "current_bridge_writes_placeholder": false,
        "output_root_only": true
      },
      "validator_command": "python Tools/validation/check_ai_workload_report_quality.py --report-dir <workload_dir> --output <quality_validation>",
      "provider_execution_performed": false,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "persistent_memory_write_performed": false
    },
    "telemetry": {
      "kind": "full0to10_provider_execution_bridge_telemetry",
      "passed": true,
      "event_count": 4,
      "events": [
        {
          "event": "invocation_plan",
          "passed": true,
          "details": {
            "permit_decision": "deny"
          },
          "timestamp": "2026-05-07T11:33:40.654951+00:00"
        },
        {
          "event": "real_run_gate",
          "passed": true,
          "details": {
            "decision": "block_real_run"
          },
          "timestamp": "2026-05-07T11:33:40.654951+00:00"
        },
        {
          "event": "command_plan",
          "passed": true,
          "details": {
            "non_executing": true
          },
          "timestamp": "2026-05-07T11:33:40.654951+00:00"
        },
        {
          "event": "workload_paths",
          "passed": true,
          "details": {
            "workload_dir": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/future_real_run_outputs"
          },
          "timestamp": "2026-05-07T11:33:40.654951+00:00"
        }
      ],
      "errors": [],
      "warnings": [],
      "provider_execution_performed": false,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "persistent_memory_write_performed": false
    },
    "readiness": {
      "kind": "full0to10_provider_execution_bridge_readiness",
      "passed": true,
      "score": 95,
      "ready_for_final_product_inclusion": true,
      "ready_for_real_provider_execution": false,
      "blockers": [],
      "warnings": [
        "real_run_blocked_valid_pre_run_state"
      ],
      "provider_execution_performed": false,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "persistent_memory_write_performed": false
    },
    "errors": [],
    "warnings": [
      "real_run_blocked_valid_pre_run_state"
    ],
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "persistent_memory_write_performed": false,
    "outputs": {
      "bridge": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge.json",
      "real_run_gate": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_real_run_gate.json",
      "command_plan": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_command_plan.json",
      "workload_output_paths": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_workload_output_paths.json",
      "telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge_telemetry.json",
      "markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_execution_bridge/full0to10_provider_execution_bridge.md"
    }
  },
  "effective_use_summary": {
    "kind": "full0to10_effective_use_optimization_summary",
    "passed": true,
    "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
```

## Context after

    "outputs": {
      "quality_product": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_quality_product.md",
      "provider_hardening": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_provider_hardening_contracts.json",
      "optimization": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_optimization.json",
      "tool_telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_tool_telemetry.json",
      "memory_db": "output/ai_runtime_memory/full0to10_effective_use.sqlite",
      "summary": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_summary.json",
      "summary_markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/effective_use/full0to10_effective_use_summary.md"
    },
    "provider_contracts": {
      "kind": "full0to10_provider_hardening_contracts",
      "passed": true,
