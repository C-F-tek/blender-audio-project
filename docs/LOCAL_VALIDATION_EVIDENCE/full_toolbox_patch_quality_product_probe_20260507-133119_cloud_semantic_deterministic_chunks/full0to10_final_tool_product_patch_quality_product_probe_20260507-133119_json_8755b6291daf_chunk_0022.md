# Evidence Chunk 0022/0035

- source: `output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `8755b6291dafb02a9387e89ef9948a1c0a9850a172d212bce6b03df7ba6ca391`
- line_start: `5752`
- line_end: `5767`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0021.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119_json_8755b6291daf_chunk_0023.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: outputs; provider_governor; valid_result; request; operator_intent. Preview: "outputs": { "control": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/accelerator_control/full0to10_accelerator_control.json", "telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_prob...

## Context before

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

## Chunk content

```json
    "outputs": {
      "control": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/accelerator_control/full0to10_accelerator_control.json",
      "telemetry": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/accelerator_control/full0to10_accelerator_telemetry.json",
      "markdown": "output/validation/full0to10_final_tool_product_patch_quality_product_probe_20260507-133119/accelerator_control/full0to10_accelerator_control.md"
    }
  },
  "provider_governor": {
    "kind": "full0to10_provider_governor",
    "passed": true,
    "valid_result": true,
    "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
    "operator_intent": false,
    "allow_provider_generation_requested": false,
    "decision": "deny",
    "permit_allowed": false,
    "deny_is_failure": false,
```

## Context after

    "accelerator_control": {
      "kind": "full0to10_accelerator_control",
      "passed": true,
      "request": "Build the final local AI product for stamp patch_quality_product_probe_20260507-133119 from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
      "hardware_capability": {
        "kind": "full0to10_hardware_tool_capability",
        "generated_at": "2026-05-07T11:33:38.199416+00:00",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "persistent_memory_write_performed": false,
