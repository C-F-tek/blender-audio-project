# Evidence Chunk 0002/0002

- source: `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_20260503-231855.json`
- source_sha256: `a545ff4a9bb4e2b0f6ff96ea64034f639739a6fd7d06dbe5bf81b4337ecb0341`
- line_start: `379`
- line_end: `433`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/runtime_tool_capability_manifest_20260503-231855_json_a545ff4a9bb4_chunk_0001.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: source_files; cloud_handoff_policy; include_with_evidence_chunks; include_runtime_usage_telemetry; include_patch_plan_and_recommendations. Preview: "source_files": [ { "path": "Tools/ai/agent_runtime_tool_broker.py", "role": "runtime_tool_broker_allowlist_source", "exists": true, "size_bytes": 29351, "sha256": "f948a459a39709877fac86cf098601b01f9560628644ec87d080c11f6fe3f449" }, { "path": "Tools/ai/build_...

## Context before

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

## Chunk content

```json
  "source_files": [
    {
      "path": "Tools/ai/agent_runtime_tool_broker.py",
      "role": "runtime_tool_broker_allowlist_source",
      "exists": true,
      "size_bytes": 29351,
      "sha256": "f948a459a39709877fac86cf098601b01f9560628644ec87d080c11f6fe3f449"
    },
    {
      "path": "Tools/ai/build_runtime_tool_usage_telemetry.py",
      "role": "runtime_tool_usage_telemetry_builder",
      "exists": true,
      "size_bytes": 26844,
      "sha256": "80fc480fb078e22658d537990eb1af1610fe27124eab5f1b8cb48d05240a7154"
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
      "size_bytes": 28918,
      "sha256": "0e20f26f7f15f8994bfc4b22ee420d068b6ce9c6aa8b2c5236b5f6f6c3eab812"
    },
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260503-231855.json",
      "role": "observed_runtime_tool_usage_report",
      "exists": true,
      "size_bytes": 5523,
      "sha256": "8a104e5ae602928a01d3ef4bcf10b83c36576f73023ab8ea6108d23c61f7eb19"
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
