# Evidence Chunk 0020/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `3494`
- line_end: `3650`
- section_kinds: `['markdown_heading_section', 'markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0019.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0021.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `output/ai_pipeline/agent_review_evidence_sufficiency.json`; `output/ai_pipeline/full_toolbox_20260503-231855_bridge_orchestrator.json`. Preview: "exists": true, "kind": "source_markdown", "chars": 3909, "lines": 106, "matched_terms": [ "docs/references", "docs/references" ], "snippet": "t this layer is not\n\nThis layer is not:\n\n- a complete mirror of OpenVINO, ONNX Runtime, Guardrails, Promptfoo, De...

## Context before

          "reference": "docs/references",
          "candidate_references": [
            "docs/references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_ONBOARDING.md",

## Chunk content

````md
              "exists": true,
              "kind": "source_markdown",
              "chars": 3909,
              "lines": 106,
              "matched_terms": [
                "docs/references",
                "docs/references"
              ],
              "snippet": "t this layer is not\n\nThis layer is not:\n\n- a complete mirror of OpenVINO, ONNX Runtime, Guardrails, Promptfoo, DeepEval, OpenAI Evals, AGENTS.md or MCP documentation;\n- a replacement for local validation;\n- a runtime dependency;\n- a permission to perform destructive changes;\n- a reason to bypass `AGENTS.md`, execution plans or validators.\n\n## Repository policy\n\nFull external repositories, if downloaded locally for study, should remain outside committed source or under ignored folders such as:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nThe committed repository should contain only:\n\n```text\ndocs/AI_REFERENCE_ONBOARDING.md\ndocs/AI_REFERENCE_SOURCE_MAP.md\ndocs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md\ndocs/AI_GUARDRAILS_VALIDATION_GUIDE.md\ndocs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md\n```\n\nThis keeps remote AI agents effective without bloating the repository.\n\n## Recommended agent behavior\n\nWhen an AI agent uses this reference layer, it should:\n\n1. identify the target work area;\n2. read the related guide;\n3. map external concepts to existing project files;\n4. avoid introducing new dependencies unless explicitly approved;\n5. prefer additive documentation, validators and helper modules;\n6. preserve current Blender package behavior;\n7. keep NPU helper work provider-free unless a validated phase says otherwise;\n8. update `docs/README.md` when adding stable documentation;\n9. report uncertainty rather than inventing unsupported repository state.\n\n## Task routing\n\n| Task | Read first |\n|---|---|\n| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md` |\n| NPU"
            },
            {
              "path": "docs/references",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_SOURCE_MAP.md",
          "reference": "docs/external_references",
          "candidate_references": [
            "docs/external_references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_SOURCE_MAP.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3956,
              "lines": 94,
              "matched_terms": [
                "docs/external_references",
                "docs/external_references"
              ],
              "snippet": "command;\n- a package README update;\n- a documented execution plan.\n\n### 4. Keep AI instructions compact\n\nLarge instructions degrade agent reliability. Long background belongs in `docs/`; immediate rules belong in `AGENTS.md` and package-level README files.\n\n### 5. Prefer provider-agnostic architecture\n\nThe project may use OpenVINO, Ollama, OpenAI-compatible endpoints or local Python tools, but orchestration should avoid hard-coding one provider into core logic.\n\n## Local reference folders\n\nOptional local-only folders:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nSuggested `.gitignore` entries if those folders are used:\n\n```gitignore\ndocs/external_references/\ndocs/references/\n```\n\n## Maintenance rules\n\nWhen adding a new reference:\n\n1. add it to this source map;\n2. explain why it matters to this repository;\n3. map it to concrete local files;\n4. avoid copying large upstream content;\n5. add or update a validator when the rule is enforceable;\n6. update `docs/README.md` if the new document is stable.\n"
            },
            {
              "path": "docs/external_references",
              "exists": false,
          
```

### `output/ai_pipeline/full_toolbox_20260503-231855_bridge_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `5267`
- SHA-256: `da76d67b8b48c27aa042047e263d140063df659cd111e54daf8bb03153ce4584`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
  "generated_at": "2026-05-03T23:22:55",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "gpu_output": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
  "gpu_recommendation_count": 20,
  "gpu_empty_recommendations_reason": "",
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260503-231855_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260503-231855_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-03T23:21:08",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "8000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "skipped",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T23:22:52",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-231855_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-231855_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    }
  ],
  "decision": {
    "deterministic_recommendation_bridge": true,
    "manual_review_required": true,
    "recommended_next_layer": "build_agent_review_patch_plan.py"
  },
  "guardrails": {
    "report_only": true,
    "manual_review_required": true,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "blender_runtime_execution_performed": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false,
    "real_github_pr_created": false
  }
}

```

````

## Context after

### `output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `173927`
- SHA-256: `d7ee8744f7bccfd214b41c06c043668fc320019a33afcb3c4e9b61692c2ae769`
- Content included: `True`
- Content truncated: `True`

```text
{
