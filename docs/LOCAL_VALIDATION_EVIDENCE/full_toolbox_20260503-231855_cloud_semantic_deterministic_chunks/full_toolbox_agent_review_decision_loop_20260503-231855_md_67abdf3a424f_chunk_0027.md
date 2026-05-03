# Evidence Chunk 0027/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `4873`
- line_end: `5140`
- section_kinds: `['markdown_heading_section', 'markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0026.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0028.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json`; `output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.md`; Agent GPU Deep Planning Review; Decision; Recommendations. Preview: "args": {}, "source": "deterministic_fallback" }, { "id": "fallback_gpu_contract_smoke", "tool": "run_gpu_planner_json_contract_smoke", "reason": "Deterministic fallback to verify planner JSON/tool-request contract: model_output_schema_mismatch.", "args": {}, ...

## Context before

        },
        {
          "id": "fallback_validation_contract",
          "tool": "check_validation_report_contract",
          "reason": "Deterministic fallback to refresh validation contract evidence: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_transient_context",
          "tool": "build_agent_transient_request_context",
          "reason": "Deterministic fallback to refresh transient request context: model_output_schema_mismatch.",

## Chunk content

````md
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_gpu_contract_smoke",
          "tool": "run_gpu_planner_json_contract_smoke",
          "reason": "Deterministic fallback to verify planner JSON/tool-request contract: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        }
      ],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 4,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        },
        "source": "provider_tool_requests",
        "provider_generated_tool_requests": true
      },
      "provider_tool_request_count": 4,
      "deterministic_runtime_tool_fallback_used": false,
      "deterministic_runtime_tool_fallback_reason": "",
      "deterministic_runtime_tool_fallback_request_count": 0,
      "json_ok": true,
      "parse_error": "",
      "schema_ok": false,
      "schema_errors": [
        "missing top-level keys: recommendations"
      ],
      "context_echo_detected": false,
      "model_output_schema_mismatch": true,
      "contract_empty_recommendations_reason": "model_output_schema_mismatch",
      "contract": {
        "json_ok": true,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "",
        "schema_errors": [
          "missing top-level keys: recommendations"
        ],
        "raw_response_sha256": "50a2eed61fec792f17f6fa74a4e3ebd3efec834b87a7281f59dfe110c161f763",
        "raw_response_chars": 70,
        "top_level_keys": [
          "response"
        ],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "tool_request_count": 0,
        "valid_tool_request_count": 0,
        "invalid_tool_request_count": 0,
        "empty_recommendations_reason": "model_output_schema_mismatch"
      },
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "model_output_schema_mismatch",
      "evidence_ready_for_manual_patch_count": 12,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    },
    {
      "round": 4,
      "elapsed_seconds": 13.671,
      "file_count": 6,
      "files": [
        "docs/AI_SMART_POLICY.md",
        "docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md",
        "docs/AUDIO_ANALYSIS_PIPELINE.md",
        "docs/AUTO_PUSH_GENERATED_ARTIFACTS.md",
        "docs/BLENDER_SCRIPT_ENTRYPOINTS.md",
        "docs/CODE_CONSULTATION_REPORT.md"
      ],
      "response_chars": 70,
      "raw_response_preview": "{\n    \"response\": \"I'm sorry, but I can't assist with that request.\"\n}",
      "parsed_response": {
        "response": "I'm sorry, but I can't assist with that request.",
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
      "tool_requests": [
        {
          "id": "fallback_python_syntax",
          "tool": "check_python_syntax",
          "reason": "Deterministic fallback after provider emitted no valid tool_requests: model_output_schema_mismatch.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_validation_contract",
          "tool": "check_validation_report_contract",
          "reason": "Deterministic fallback to refresh validation contract evidence: model_output_sche
```

### `output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1060`
- SHA-256: `08d3b3b604843b7f810125964fe497e1e7569d002ef26e1d988f7378b51bca0d`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `50.391`
- Round count: `4`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- Tool request count: `0`
- Valid tool request count: `0`
- Invalid tool request count: `0`
- JSON parse error count: `0`
- Context echo detected count: `0`
- Model output schema mismatch count: `4`
- Empty recommendations reason: `model_output_schema_mismatch`
- Evidence ready for manual patch count: `12`

## Decision

- `ready_for_patch_plan`: `False`
- `ready_count`: `0`
- `needs_more_context_count`: `0`
- `fallback_patch_plan_recommended`: `True`
- `npu_auditor_non_blocking`: `True`
- `npu_unusable_or_failed_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_auditor_disabled_reason`: ``
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `manual_review_required`: `True`

## Recommendations


```

### `output/ai_pipeline/repository_change_proposals.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1648`
- SHA-256: `6b631c5a37d9c0d50199cbdee03cd33a269db1fdd1d529dd8b3ef10e7ec7a7c2`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-03T23:22:55`
- Profile: `core`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-REPORT-CONTRACT-CONSISTENCY — Normalize validation report root fields

- Priority: `P1`
- Area: `validation_contracts`
- Change type: `contract_normalization`
- Apply mode: `manual_review_only`
- Rationale: The validation-report contract checker found reports missing common fields or using inconsistent types.

### Target files
- `Tools/validation/*.py`
- `Tools/npu/pipeline/reports.py`
- `docs/JSON_SCHEMAS.md`

### Patch sketch
- Add missing root fields additively: schema_version, kind, repo_root, passed, errors, warnings where applicable.
- Do not remove validator-specific fields.
- Keep strict mode opt-in until all local reports are aligned.

### Suggestion outputs
- `path_group` `Tools/validation/*.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/npu/pipeline/reports.py` (manual_patch_suggestion, manual_review_only)
- `markdown` `docs/JSON_SCHEMAS.md` (manual_patch_suggestion, manual_review_only)

### Validation
- `python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json`
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2`

### Stop conditions
- A proposed normalization would change the meaning of existing report fields.

## Guardrail

These are proposals only. They must not be auto-applied without explicit review.

```

### `output/analysis/code_interpreter_full_toolbox_20260503-231855.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7088`
- SHA-256: `f2e1fadd2a0afa2180d5b0dbd6c71c8b89ed66ed73cab468842cdb417ae2a416`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `275`
- Parsed files: `275`
- Total lines: `77725`
- Total functions: `2751`
- Total classes: `93`
- Risk signals: `56`
- TODO/FIXME markers: `21`
- Recommendation count: `155`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/npu/run_dual_ai_pipeline.py` — `1774` lines, risk `high`
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines, risk `high`
- `Tools/workflow/workflow_state.py` — `1230` lines, risk `high`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `1179` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `1129` lines, risk `high`
- `Scripting/v61b/animation.py` — `1079` lines, risk `high`
- `Tools/ai/build_deterministic_recommendations.py` — `908` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines, risk `high`
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `694` lines, risk `medium`
- `Tools/ai/build_repository_consistency_map.py` — `687` lines, risk `medium`
- `Scripting/v61b/materials.py` — `657` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `631` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `626` lines, risk `medium`

````

## Context after

## Recommendations

- `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected
- `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_003` `Scripting/v61b/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_004` `Scripting/v61b/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_005` `Scripting/v61b/config.py` risk `medium`: medium-size Python module
- `code_static_006` `Scripting/v61b/encode_ffmpeg_v61b.py` risk `medium`: large functions detected, static risk calls detected
- `code_static_007` `Scripting/v61b/encode_image_sequence_v61b.py` risk `medium`: complex functions detected
- `code_static_008` `Scripting/v61b/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_009` `Scripting/v61b/hotpatch/accent_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_010` `Scripting/v61b/hotpatch/diagnostics.py` risk `medium`: large functions detected, complex functions detected
