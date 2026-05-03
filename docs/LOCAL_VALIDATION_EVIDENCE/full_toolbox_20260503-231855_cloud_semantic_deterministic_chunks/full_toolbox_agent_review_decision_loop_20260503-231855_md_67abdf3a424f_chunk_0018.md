# Evidence Chunk 0018/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `3149`
- line_end: `3277`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0017.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0019.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: Trusted context files; Report files; Guardrails; `output/ai_packets/gpu_planner_nonempty_recommendations_proposals.md`; Repository Change Proposals. Preview: ### Trusted context files - `AGENTS.md` - `WORKFLOW.md` - `docs/AI_DOCS_ENTRYPOINT.md` - `docs/PROJECT_STATUS_POINT.md` - `docs/TECH_DEBT_TRACKER.md` - `docs/REFACTORING_AND_REUSE_PLAN.md` - `docs/JSON_SCHEMAS.md` - `docs/AI_ARTIFACT_SCHEMAS.md` - `Tools/npu/p...

## Context before

### P2 — Review active execution plans before opening the next milestone

- Area: `execution_plans`
- Details: docs/EXECUTION_PLANS/active/2026-04-29_agent_state_memory_integration.md; docs/EXECUTION_PLANS/active/2026-04-29_agentic_memory_guardrail_pipeline.md; docs/EXECUTION_PLANS/active/2026-04-29_formal_json_schema_validation.md; docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_ai_pipeline_report_contracts.md; docs/EXECUTION_PLANS/active/2026-04-30_dry_run_matrix_contract_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_output_policy_provider_preflight.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_pipeline_decomposition_plan.md; docs/EXECUTION_PLANS/active/2026-04-30_runtime_safe_provider_report_adoption.md; docs/EXECUTION_PLANS/active/2026-04-30_validator_report_consistency_review.md

### P2 — Prefer additive observability before provider or Blender runtime changes

- Area: `agnostic_core`
- Details: Safe next steps: report contract consistency, runtime-output manifest emission, provider-result parsing/reporting without changing provider execution.

## Inputs


## Chunk content

````md
### Trusted context files
- `AGENTS.md`
- `WORKFLOW.md`
- `docs/AI_DOCS_ENTRYPOINT.md`
- `docs/PROJECT_STATUS_POINT.md`
- `docs/TECH_DEBT_TRACKER.md`
- `docs/REFACTORING_AND_REUSE_PLAN.md`
- `docs/JSON_SCHEMAS.md`
- `docs/AI_ARTIFACT_SCHEMAS.md`
- `Tools/npu/pipeline/README.md`
- `Tools/validation/README.md`
- `./docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md`
- `./Tools/ai/run_agent_gpu_deep_planning_review.py`
- `./Tools/ai/run_agent_gpu_deep_planning_supervised.py`
- `./Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py`
- `./Tools/ai/build_agent_review_patch_plan.py`

### Report files
- `output/validation/python_syntax.json`
- `output/validation/ai_pipeline_modules.json`
- `output/validation/npu_pipeline_modules.json`
- `output/validation/npu_pipeline_helper_tests.json`
- `output/validation/npu_pipeline_docs.json`
- `output/validation/provider_result_parsing.json`
- `output/validation/provider_result_report.json`
- `output/validation/ai_workload_report_quality.json`
- `output/validation/ai_workload_quality_lane_routing.json`
- `output/validation/npu_decode_quality_remediation.json`
- `output/validation/npu_decode_smoke_diagnostic.json`
- `output/validation/npu_runtime_output_manifest.json`
- `output/validation/local_ai_resource_lanes.json`
- `output/validation/local_provider_probe.json`
- `output/validation/execution_plan_status.json`
- `output/validation/validation_report_contract.json`
- `output/validation/docs_links.json`
- `./output/ai_pipeline/agent_gpu_npu_parallel_orchestrator_live.json`
- `output/ai_pipeline/agent_gpu_deep_planning_parallel_gpu.json`

## Guardrails

- Advisory only: do not auto-apply edits from this packet.
- Output/input paths are configurable; defaults are not part of the architecture boundary.
- Validate locally before committing generated indexes.
- Keep provider execution changes in a separate explicitly scoped milestone.

```

### `output/ai_packets/gpu_planner_nonempty_recommendations_proposals.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3476`
- SHA-256: `c13cf9413bd6e464df8b12b81138ae78a1dec8b8a06d76f8b31c5f6215410c9f`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-01T20:50:40`
- Profile: `core`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-AI-WORKLOAD-REPORT-QUALITY-GATE — Gate AI workload reports before using them as advisory context

- Priority: `P1`
- Area: `local_ai_workloads`
- Change type: `workload_quality_gate`
- Apply mode: `manual_review_only`
- Rationale: AI workload report quality found usable lanes: ollama; unusable lanes: npu. Downstream packets and proposals should trust only usable workload reports and keep unusable lanes limited to probes until their decoding/configuration is fixed.

### Evidence summary

```json
{
  "workload_quality_decision": {
    "quality_report_present": true,
    "usable_lanes": [
      "ollama"
    ],
    "unusable_lanes": [
      "npu"
    ],
    "ollama_gpu_primary_advisory_allowed": true,
    "npu_excluded_from_primary_advisory": true,
    "routing_policy": "usable_text_lanes_only_for_advisory_context"
  }
}
```

### Target files
- `Tools/validation/check_ai_workload_report_quality.py`
- `Tools/npu/run_npu_review.py`
- `Tools/ai/suggest_repository_updates.py`
- `Tools/ai/build_repository_change_proposals.py`
- `Tools/validation/README.md`
- `docs/JSON_SCHEMAS.md`

### Patch sketch
- Keep Ollama/GPU workload reports as primary advisory context when classified usable.
- Exclude or clearly mark NPU/OpenVINO generated reports as unusable when they are numeric/hex-like or non-linguistic.
- Do not disable NPU preflight/probe; only prevent low-quality NPU generation output from influencing suggestions.
- Add report metadata that distinguishes availability, execution and output usability.

### Suggestion outputs
- `python_code` `Tools/validation/check_ai_workload_report_quality.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/npu/run_npu_review.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/suggest_repository_updates.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/build_repository_change_proposals.py` (manual_patch_suggestion, manual_review_only)
- `markdown` `Tools/validation/README.md` (manual_patch_suggestion, manual_review_only)
- `markdown` `docs/JSON_SCHEMAS.md` (manual_patch_suggestion, manual_review_only)

### Validation
- `python .\Tools\validation\check_ai_workload_report_quality.py --repo-root . --output .\output\validation\ai_workload_report_quality.json`
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_ollama_real_workload_after_tests -ProposalBasename npu_ollama_real_workload_proposals -ContextFile output/ai_packets/npu_real_workload_report.md,output/ai_packets/ollama_gpu_real_workload_report.md -ReportFile output/validation/ai_workload_report_quality.json,output/validation/local_ai_resource_lanes.json,output/validation/provider_result_report.json,output/validation/local_provider_probe.json,output/validation/npu_runtime_output_manifest.json`

### Stop conditions
- Any change would execute providers implicitly or by default.
- Any change would hide a failing/unusable AI workload report instead of reporting it.
- Any change would alter NPU/Ollama model configuration, prompt prose or provider orchestration.

## Guardrail

These are proposals only. They must not be auto-applied without explicit review.

```

````

## Context after

### `output/ai_pipeline/agent_review_evidence_sufficiency.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `35905`
- SHA-256: `a2216b89a69fc267b8015cfcbf775591b4c8b05abd127aef322936947f80683c`
- Content included: `True`
- Content truncated: `True`

```text
{
