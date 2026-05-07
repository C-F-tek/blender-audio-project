# Evidence Chunk 0025/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `6459`
- line_end: `6538`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0024.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0026.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: telemetry; provider_execution_performed; patch_application_performed; source_writes_performed; persistent_memory_write_performed. Preview: "telemetry": { "kind": "full0to10_provider_governor_telemetry", "passed": true, "event_count": 4, "events": [ { "event": "accelerator_control", "passed": true, "severity": "info", "structural": true, "details": { "score": 92 }, "timestamp": "2026-05-07T11:33:3...

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
          "timestamp": "2026-05-07T11:33:39.091040+00:00"
        },
        {
          "event": "quality_gate_observed",
          "passed": true,
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
    "persistent_memory_write_performed": false,
    "outputs": {
      "governor": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_governor.json",
      "permit": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_run_permit.json",
      "telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_governor_telemetry.json",
      "markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/provider_governor/full0to10_provider_governor.md"
    }
  },
  "provider_invocation_plan": {
    "kind": "full0to10_provider_invocation_plan",
    "passed": true,
    "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
    "provider_lane": "ollama_gpu",
    "permit_decision": "deny",
    "permit_allowed": false,
    "generation_executes_now": false,
```

## Context after

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
