# Evidence Chunk 0016/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `2155`
- line_end: `2158`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0015.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0017.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_manifest. Preview: "preview_chars": 1500, "line_count": 8816 } ],

## Context before

      "preview_chars": 1500,
      "line_count": 76
    },
    {
      "path": "output/patch_specs/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_patch_plan.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 441138,
      "sha256": "e6ee1fa6b054e7efd9c09075d21b62c9d7db3178e23a5defe6617a7338a33955",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_review_patch_plan\",\n  \"generated_at\": \"2026-05-07T13:33:30\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [\n    \"max_patch_plans is accepted for compatibility/telemetry but does not truncate patch plans; patch_plan_count may be lower than available_patch_plan_count only through guardrail rejection\"\n  ],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_manual_review_patch_plan\",\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_bridge_orchestrator.json\",\n    \"evidence\": \"output/ai_pipeline/agent_review_evidence_sufficiency.json\",\n    \"gpu_report\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_deterministic_recommendations.json\",\n    \"orchestrator_kind\": \"deterministic_recommendation_patch_plan_bridge_orchestrator\",\n    \"evidence_kind\": \"agent_review_evidence_sufficiency\",\n    \"gpu_kind\": \"deterministic_recommendation_synthesizer\"\n  },\n  \"decision\": {\n    \"ready_for_manual_review\": true,\n    \"patch_plan_count\": 20,\n    \"skipped_candidate_count\": 0,\n    \"gpu_recommendation_count\": 20,\n    \"gpu_ready_count\": 0,\n    \"fallback_used\": false,\n    \"evidence_ready_for_manual_patch_count\": 0,\n    \"evidence_sufficient_for_real_pr\": false,\n    \"recommended_next_layer\": \"manual_review_then_targ",

## Chunk content

```json
      "preview_chars": 1500,
      "line_count": 8816
    }
  ],
```

## Context after

  "included_artifacts": [
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 56878,
      "sha256": "b8dc343722aa7723ab004fa279ffba3f19553d509c8404a2e97a2fa027ae62a2",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": true,
      "chunked_content": true,
      "line_count": 405,
