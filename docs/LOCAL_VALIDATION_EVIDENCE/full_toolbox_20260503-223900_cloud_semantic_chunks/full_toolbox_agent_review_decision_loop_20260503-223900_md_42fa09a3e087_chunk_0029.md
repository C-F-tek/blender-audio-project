# Evidence Chunk 0029/0031

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.md`
- source_sha256: `42fa09a3e087ebc6b51a8d9d2d501922dd8ed8c400791441877ab803557340fa`
- line_start: `4735`
- line_end: `4864`
- section_kinds: `['markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_md_42fa09a3e087_chunk_0028.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_md_42fa09a3e087_chunk_0030.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Def

## Context before

- `gpu_lane_mode`: `primary_fast_loop`
- `npu_lane_mode`: `slow`
- `gpu_direct_runtime_tool_provider_request_execution_count`: `0`
- `runtime_tool_feedback_context_report_count`: `0`
- `npu_effective_auditor_every_rounds`: `6`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`
- round `6` status=`finished` class=`usable_audit_text` success=`True`

```


## Chunk content

````md
### `output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `68132`
- SHA-256: `c62431d23c5e6894a6e5413eff1074d8fdf62669d2b9a43563bae9bbc3bfbcbb`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-03T22:44:16",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
  "model_used": "qwen2.5-coder:14b",
  "ollama_base_url": "http://127.0.0.1:11434",
  "budget_minutes": 12,
  "elapsed_seconds": 203.44,
  "context_file_count": 120,
  "round_count": 8,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 43.381,
      "file_count": 8,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
        "docs/AI_ARTIFACT_SCHEMAS.md",
        "docs/AI_CHUNKING_STRATEGY.md",
        "docs/AI_CONTEXT_PACKS.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/AI_EXTERNAL_KNOWLEDGE.md",
        "docs/AI_GENERATED_PACKAGE_STANDARD.md",
        "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md"
      ],
      "response_chars": 4656,
      "raw_response_preview": "{\n    \"path\": \"docs/AI_GUARDRAILS_VALIDATION_GUIDE.md\",\n    \"exists\": true,\n    \"lines\": 212,\n    \"chars\": 5842,\n    \"content_preview\": \"# AI Guardrails and Validation Guide\\n\\n## Purpose\\n\\nThis guide defines how guardrails, schema validation and evaluation-style workflows should be applied to AI-generated artifacts in this repository.\\n\\nIt adapts guardrails/evals concepts into local repository rules without adding mandatory external runtime dependencies.\\n\\n## Core rule\\n\\nAI-generated output is not accepted because it looks plausible. It is accepted only after it passes the relevant local contracts.\\n\\nFor this project, that means:\\n\\n```text\\nmodel output\\n  -> parse\\n  -> normalize\\n  -> schema validation\\n  -> path validation\\n  -> Blender compatibility validation when relevant\\n  -> generated Python policy validation when relevant\\n  -> report\\n```\\n\\n## Local validation assets\\n\\n| Local asset | Role |\\n|---|---|\\n| `Tools/validation/` | Non-invasive validation scripts. |\\n| `docs/JSON_SCHEMAS.md` | Existing JSON schema notes and report contract map. |\\n| `docs/AI_ARTIFACT_SCHEMAS.md` | AI artifact schema notes. |\\n| `docs/QUALITY_GATE.md` | Acceptance rules for generated packages. |\\n| `Tools/ai/run_pipeline_dry_run_matrix.py` | Repeatable AI pipeline dry-run matrix. |\\n| `output/validation/` | Recommended validation report output folder. |\\n| `docs/EXECUTION_PLANS/` | Durable task records for complex validation/refactor work. |\\n\\n## Required validation dimensions\\n\\n### 1. Syntax validity\\n\\nGenerated JSON must parse as JSON.\\n\\nGenerated Python must pass syntax checks before it is considered usable.\\n\\nRecommended command:\\n\\n```powershell\\npython .\\\\Tools\\\\validation\\\\check_python_syntax.py --repo-root . --output .\\\\output\\\\validation\\\\python_syntax.json\\n```\\n\\n### 2. Schema conformance\\n\\nGenerated artifacts should declare or imply a schema version and satisfy required fields.\\n\\nMinimum expected fields for AI artifacts usually include:\\n\\n```text\\nschema_version\\nsource_inputs\\nstage\\nstatus\\noutput_path or planned_output_path\\nvalidation\\nerrors\\nwarnings\\n```\\n\\nPatch-related artifacts should also include:\\n\\n```text\\ntarget_files\\nsafe_write_plan\\nreview_notes\\n```\\n\\n### 3. Repository path safety\\n\\nGenerated artifact paths must be checked before file writes.\\n\\nRules:\\n\\n- do not write outside the repository root;\\n- do not overwrite raw frame-by-frame analysis JSON files;\\n- prefer `output/`, `indexAI/patch_library/`, `Scripting/v61b/hotpatch/` or explicit safe folders;\\n- use patch specs for mechanical edits when reviewability matters.\\n\\n### 4. Blender compatibility\\n\\nGenerated Blender Python must avoid known incompatible APIs and deprecated node types.\\n\\nCurrent hard rule:\\n\\n```text\\nDo not use ShaderNodeTexMusgrave for Blender 5.x.\\n```\\n\\nGenerated scene scripts should preserve:\\n\\n- audio loading;\\n- frame range setup;\\n- FPS setup;\\n- camera;\\n- lighting;\\n- render configuration;\\n- output path configuration.\\n\\n#",
      "parsed_response": {
        "path": "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md",
        "exists": true,
        "lines": 212,
        "chars": 5842,
        "content_preview": "# AI Guardrails and Validation Guide\n\n## Purpose\n\nThis guide defines how guardrails, schema validation and evaluation-style workflows should be applied to AI-generated artifacts in this repository.\n\nIt adapts guardrails/evals concepts into local repository rules without adding mandatory external runtime dependencies.\n\n## Core rule\n\nAI-generated output is not accepted because it looks plausible. It is accepted only after it passes the relevant local contracts.\n\nFor this project, that means:\n\n```text\nmodel output\n  -> parse\n  -> normalize\n  -> schema validation\n  -> path validation\n  -> Blender compatibility validation when relevant\n  -> generated Python policy validation when relevant\n  -> report\n```\n\n## Local validation assets\n\n| Local asset | Role |\n|---|---|\n| `Tools/validation/` | Non-invasive validation scripts. |\n| `docs/JSON_SCHEMAS.md` | Existing JSON schema notes and report contract map. |\n| `docs/AI_ARTIFACT_SCHEMAS.md` | AI artifact schema notes. |\n| `docs/QUALITY_GATE.md` | Acceptance rules for generated packages. |\n| `Tools/ai/run_pipeline_dry_run_matrix.py` | Repeatable AI pipeline dry-run matrix. |\n| `output/validation/` | Recommended validation report output folder. |\n| `docs/EXECUTION_PLANS/` | Durable task records for complex validation/refactor work. |\n\n## Required validation dimensions\n\n### 1. Syntax validity\n\nGenerated JSON must parse as JSON.\n\nGenerated Python must pass syntax checks before it is considered usable.\n\nRecommended command:\n\n```powershell\npython .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json\n```\n\n### 2. Schema conformance\n\nGenerated artifacts should declare or imply a schema version and satisfy required fields.\n\nMinimum expected fields for AI artifacts usually include:\n\n```text\nschema_version\nsource_inputs\nstage\nstatus\noutput_path or planned_output_path\nvalidation\nerrors\nwarnings\n```\n\nPatch-related artifacts should also include:\n\n```text\ntarget_files\nsafe_write_plan\nreview_notes\n```\n\n### 3. Repository path safety\n\nGenerated artifact paths must be checked before file writes.\n\nRules:\n\n- do not write outside the repository root;\n- do not overwrite raw frame-by-frame analysis JSON files;\n- prefer `output/`, `indexAI/patch_library/`, `Scripting/v61b/hotpatch/` or explicit safe folders;\n- use patch specs for mechanical edits when reviewability matters.\n\n### 4. Blender compatibility\n\nGenerated Blender Python must avoid known incompatible APIs and deprecated node types.\n\nCurrent hard rule:\n\n```text\nDo not use ShaderNodeTexMusgrave for Blender 5.x.\n```\n\nGenerated scene scripts should preserve:\n\n- audio loading;\n- frame range setup;\n- FPS setup;\n- camera;\n- lighting;\n- render configuration;\n- output path configuration.\n\n### 5. Policy validation\n\nUse existing policy validators for generated files:\n\n```powershell\npython .\\Tools\\validation\\check_generated_python_policy.py --repo-root . --output .\\output\\validation\\generated_python_policy.json\npython .\\Tools\\validation\\check_generated_artifact_path_policy.py --repo-root . --output .\\output\\validation\\generated_artifact_path_policy.json\n```\n\n## Guardrail failure behavior\n\nA failed validation must produce a structured failure, not a silent fallback.\n\nRecommended report shape:\n\n```json\n{\n  \"status\": \"failed\",\n  \"stage\": \"schema_validation\",\n  \"errors\": [\n    {\n      \"code\": \"missing_required_field\",\n      \"field\": \"target_files\",\n      \"message\": \"Patch artifact does not declare target files.\"\n    }\n  ],\n  \"warnings\": [],\n  \"artifact_written\": false\n}\n```\n\n## Evaluation-style workflow\n\nFor repeatable AI work, prefer a small fixture/eval set:\n\n```text\ninput fixture\n  -> expected artifact shape\n  -> validation command\n  -> report path\n  -> pass/fail result\n```\n\nGood future locations:\n\n```text\nTools/ai/fixtures/\nTools/validation/fixtures/\noutput/validation/\ndocs/EXECUTION_PLANS/\n```\n\n## Promote reusable logic\n\n- Extract common validation patterns into shared scripts.\n- Document all assumptions and deviations from the reference model.\n- Use `Scripting/shared/` for global operational tasks when available.\n- Add comments around Blender API compatibility-sensitive code.\n\n## Not specified\n\n- Final package generator command.\n- Final local AI model.\n- Final validation runner.\n- Final Blender version matrix.\n",
        "recommendations": [],
        "missing_evidence": [],
        "next_best_action": ""
      },
      "schema_repair_retry": {
        "attempted": true,
        "accepted": false,
        "reason": "schema_repair_retry_rejected",
        "json_ok": true,
        "schema_ok": false,
        "recommendation_count": 0,
        "valid_tool_request_count": 0,
        "empty_recommendations_reason": "model_output_schema_mismatch"
      },
      "provider_empty_response": false,
      "tool_requests": [],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 0,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        }
      },
      "provider_tool_request_count": 0,
      "deterministic_runtime_tool_fallback_used": false,
      "deterministic_runtime_tool_fallback_reason": "",
      "deterministic_runtime_tool_fallback_request_count": 0,
      "json_ok": true,
      "parse_error": "",
      "schema_ok": false,
      "schema_errors": [
        "missing top-level keys: recommendations"
      ],
      "context_echo_detected": true,
      "model_output_schema_mismatch": true,
      "contract_empty_recommendations_reason": "context_echo_detected",
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": true,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "1d7909e3ca25cc3c6370dbdd5d8bc5761570a1cf7963730ec075a103bd7c1289",
        "raw_response_chars": 4656,
        "top_level_keys": [
          "chars",
          "content_preview",
          "exists",
          "lines",
          "path"
        ],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "context_echo_detected"
      },
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "context_echo_detected",
      "evidence_ready_for_manual_patch_count": 12,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    },
````

## Context after

    {
      "round": 2,
      "elapsed_seconds": 33.877,
      "file_count": 8,
      "files": [
        "docs/AI_MEMORY_POLICY.md",
        "docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md",
        "docs/AI_ONBOARDING.md",
        "docs/AI_PIPELINE_ARCHITECTURE.md",
        "docs/AI_PIPELINE_OPTIMIZATION.md",
        "docs/AI_PIPELINE_REFACTOR_STATUS.md",
        "docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md",
