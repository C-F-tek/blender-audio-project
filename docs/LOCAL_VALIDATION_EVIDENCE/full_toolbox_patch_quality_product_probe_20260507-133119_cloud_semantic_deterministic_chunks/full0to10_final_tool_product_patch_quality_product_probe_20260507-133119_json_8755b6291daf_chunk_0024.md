# Evidence Chunk 0024/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `6118`
- line_end: `6458`
- section_kinds: `['json_key_section', 'json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0023.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0025.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: accelerator_control; quality_gate; budget; policy; npu_audit. Preview: "readiness": { "kind": "full0to10_accelerator_readiness", "passed": true, "score": 92, "ready_for_product_package": true, "ready_for_real_provider_generation": false, "blockers": [], "warnings": [ "npu_not_visible_or_probe_disabled" ], "provider_execution_perf...

## Context before

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

## Chunk content

```json
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
        "control": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/accelerator_control/full0to10_accelerator_control.json",
        "telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/accelerator_control/full0to10_accelerator_telemetry.json",
        "markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/accelerator_control/full0to10_accelerator_control.md"
      }
    },
    "quality_gate": {
      "kind": "full0to10_quality_gate",
      "generated_at": "2026-05-07T11:33:39.091040+00:00",
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
    },
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
    "policy": {
      "kind": "full0to10_provider_governor_policy",
      "passed": false,
      "requirements": [
        {
          "requirement": "operator_intent",
          "passed": false,
          "reason": "explicit -OperatorIntent is required"
        },
        {
          "requirement": "quality_gate_passed",
          "passed": true,
          "reason": "quality gate must pass"
        },
        {
          "requirement": "accelerator_scheduler_generation_blocked_pre_run",
          "passed": true,
          "reason": "pre-run scheduler must keep generation disabled"
        },
        {
          "requirement": "gpu_mind_requires_launcher",
          "passed": true,
          "reason": "GPU mind must require explicit launcher"
        },
        {
          "requirement": "workload_quality_policy_available",
          "passed": true,
          "reason": "validator supports --report-dir"
        },
        {
          "requirement": "npu_audit_plan_available",
          "passed": true,
          "reason": "NPU audit plan is generated by governor"
        },
        {
          "requirement": "gpu0_guardrail_available",
          "passed": true,
          "reason": "GPU.0 guardrail is generated by governor"
        }
      ],
      "operator_intent": false,
      "default_decision": "deny_until_all_requirements_pass"
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
    "run_permit": {
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
```

## Context after

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
