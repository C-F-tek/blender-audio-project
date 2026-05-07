# Evidence Chunk 0002/0002

- source: `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `e9acfbe7da1518838a8d24dc5eb25af09ae9634cf77df1ab8937e59e74933405`
- line_start: `412`
- line_end: `491`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/runtime_tool_capability_manifest_patch_quality_product_probe_20260507-133119_json_e9acfbe7_chunk_0001.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: observed_by_phase; supported_callers; cloud_handoff_rule; source_files; cloud_handoff_policy. Preview: "observed_by_phase": { "explicit_runtime_tool_broker_bootstrap": { "count": 3, "executed": 3, "failed": 0, "blocked": 0, "elapsed_seconds": 0.0 }, "gpu0_peer_runtime_tool_broker": { "count": 3, "executed": 3, "failed": 0, "blocked": 0, "elapsed_seconds": 0.0 }...

## Context before

        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "gpu0": {
        "count": 3,
        "executed": 3,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },

## Chunk content

```json
    "observed_by_phase": {
      "explicit_runtime_tool_broker_bootstrap": {
        "count": 3,
        "executed": 3,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "gpu0_peer_runtime_tool_broker": {
        "count": 3,
        "executed": 3,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "supported_callers": [
      "gpu",
      "npu",
      "orchestrator",
      "ollama-local",
      "deterministic"
    ],
    "cloud_handoff_rule": "cloud receives capability manifest plus runtime usage telemetry; local execution remains broker-controlled"
  },
  "source_files": [
    {
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "role": "runtime_tool_broker_allowlist_source",
      "exists": true,
      "size_bytes": 30891,
      "sha256": "9dd4d5307a1bb63ef5da341d0ac7bf44df1c7270018a011f9f6e8a30e153eca8"
    },
    {
      "path": "Tools/ai/build_runtime_tool_usage_telemetry.py",
      "role": "runtime_tool_usage_telemetry_builder",
      "exists": true,
      "size_bytes": 37862,
      "sha256": "3be03865ef3b906dd9587b0a4cbe4348217000e1083464929a5e5a2048a2fa3b"
    },
    {
      "path": "Tools/ai/build_semantic_evidence_chunks.py",
      "role": "semantic_cloud_handoff_chunker",
      "exists": true,
      "size_bytes": 22859,
      "sha256": "5fdcbc74f6eb931f3b95c6b54b1eb1071e57f8f41a34c694864b3ac8cdab80f7"
    },
    {
      "path": "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py",
      "role": "shared_toolbox_bundle_builder",
      "exists": true,
      "size_bytes": 57270,
      "sha256": "346f8bef6e54135ce297b99dd84a983268bea703a38bab373f51d8eb4634652a"
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119.json",
      "role": "observed_runtime_tool_usage_report",
      "exists": true,
      "size_bytes": 17990,
      "sha256": "5cdcb64b46f6cc3065f72dde3b721c2d526248d2a776d9c8d828d7d7a03606eb"
    }
  ],
  "cloud_handoff_policy": {
    "include_with_evidence_chunks": true,
    "include_runtime_usage_telemetry": true,
    "include_patch_plan_and_recommendations": true,
    "no_free_shell": true,
    "tool_execution_requires_local_broker": true,
    "cloud_model_may_reason_about_tools_but_must_not_execute_them": true
  },
  "guardrails": {
    "report_only": true,
    "committable_location": "docs/LOCAL_VALIDATION_EVIDENCE",
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false,
    "blender_runtime_execution_performed": false
  }
}
```
