<!-- IA-CARMINE-MD-SPLIT: part -->
# LOCAL_AI_WORKFLOW — parte 002 di 002

Sorgente indice: [`../LOCAL_AI_WORKFLOW.md`](../LOCAL_AI_WORKFLOW.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Key tools

| File | Role |
|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | Canonical run-unica local AI orchestrator and Full0To10 entrypoint. |
| `Tools/workflow/run_local_ai_markdown_task.ps1` | Supporting task packet wrapper; not an active first entrypoint. |
| `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | Official adapter implementation lane behind launcher `official` mode. |
| `Tools/workflow/run_local_ai_core_tool_activation.ps1` | Supporting app-agnostic activation lane retained for focused/legacy validation; prefer the unified launcher. |
| `docs/LOCAL_AI_TASKS/` | Markdown task inputs and router docs; execution still routes through unified launcher. |
| `Tools/validation/build_markdown_inventory.py` | Builds Markdown lifecycle/length/pruning inventory. |
| `Tools/validation/build_script_inventory.py` | Builds script/tool/function/class/method inventory. |
| `Tools/ai/select_semantic_code_chunks.py` | Selects bounded task-focused semantic chunks from the generated semantic chunk index. |
| `Tools/validation/check_selected_semantic_chunks.py` | Validates selected-chunks bundles and can emit compact selected-chunks evidence. |
| `Tools/ai/build_ai_context_pack.py` | Builds bounded task-scoped context packs and compact evidence for future AI/human task planning. |
| `Tools/validation/check_ai_context_pack_contract.py` | Validates context packs and context-pack evidence without executing providers. |
| `Tools/ai/build_selective_execution_plan.py` | Builds report-only recommendations for next validators and candidate patch specs from context/evidence. |
| `Tools/validation/check_selective_execution_plan.py` | Validates selective execution plan reports. |
| `Tools/ai/build_local_ai_enrichment_plan.py` | Builds reusable local AI enrichment plans. |
| `Tools/validation/check_local_ai_enrichment_plan.py` | Validates enrichment plan reports. |
| `Tools/validation/check_local_ai_adapter_manifest.py` | Validates local AI task adapter manifests. |
| `Tools/npu/build_npu_knowledge_broker_packet.py` | Builds NPU knowledge-broker/context-oracle packets. |
| `Tools/validation/check_npu_knowledge_broker_packet.py` | Validates NPU knowledge-broker packets without provider promotion. |
| `Tools/ai/build_agent_review_evidence_sufficiency.py` | Builds evidence sufficiency reports for agent-review patch planning. |
| `Tools/ai/build_agent_review_patch_plan.py` | Builds manual-review-only documentation patch plans. |
| `Tools/validation/run_agent_review_patch_plan_full_validation.py` | Runs the provider-free patch-plan validation and evidence bundle wrapper. |
| `Tools/validation/check_ai_workload_report_quality.py` | Classifies workload reports into usable/unusable lanes. |
| `Tools/ai/workload_quality.py` | Shared routing helper for trusted/excluded advisory context. |
| `Tools/ai/build_workload_quality_lane_routing.py` | Builds routing report and declares primary advisory provider. |
| `Tools/ai/run_local_provider_probe.py` | Local provider probes for Ollama/GPU and NPU/OpenVINO. Full0To10 lane unless disabled/unavailable. |
| `Tools/ai/run_npu_decode_smoke_diagnostic.py` | OpenVINO/NPU decode smoke through dedicated NPU Python. Full0To10 diagnostic lane unless disabled/unavailable. |
| `Tools/validation/check_npu_decode_quality_remediation.py` | NPU remediation report from quality metrics. |
| `Tools/ai/suggest_repository_updates.py` | Builds advisory packet using quality-approved context only. |
| `Tools/ai/build_repository_change_proposals.py` | Builds manual-review proposals with code/MD/JSON suggestion descriptors. |
| `Tools/validation/check_repository_change_proposals.py` | Validates proposal reports before they are used as future patch work items. |
| `Tools/ai/build_patch_specs_from_proposals.py` | Converts validated proposals into inert draft patch specs under `output/patch_specs/`. |
| `Tools/validation/check_patch_spec_drafts.py` | Validates draft patch-spec contracts and blocks queued/concrete replacements. |
| `Tools/ai/promote_patch_spec_draft.py` | Combines one draft spec with an explicit replacement plan and writes a reviewed dry-run-passing spec under `output/patch_specs/`. |
| `Tools/validation/check_reviewed_patch_specs.py` | Revalidates reviewed patch specs and reruns dry-run without writing source files. |
| `Tools/ai/build_full_context_golden_proposals.py` | Builds deterministic manual-review-only proposal families P1-P6 from the full-context golden path. |
| `Tools/validation/check_full_context_golden_proposals.py` | Validates full-context golden proposal coverage beyond the generic proposal schema. |
| `Tools/ai/build_dry_run_matrix_evidence_bundle.py` | Summarizes ignored dry-run matrix reports into compact Git-trackable evidence. |
| `Tools/validation/check_dry_run_matrix_evidence_bundle.py` | Validates dry-run matrix evidence without executing providers or matrix cases. |
| `Tools/ai/build_github_evidence_bundle.py` | Summarizes long ignored `output/` reports into tracked docs evidence. |
| `Tools/workflow/run_post_validation_ai_packet.ps1` | Advisory packet implementation lane behind launcher provider/advisory phases. |
| `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | Parallel GPU/NPU multistep implementation lane behind launcher provider phases. |

## Evidence workflow

Because `output/` is ignored, use compact evidence bundles. Add only the specific compact evidence files produced by the intended run.

Do not bulk-add the whole evidence directory unless a human explicitly reviewed every changed evidence file.

For evidence commands, use the unified launcher runbook or tool-specific README. This workflow document intentionally avoids duplicating executable commands.

## Requirements for safe local generation

- Start run-unica local AI flows from the unified launcher.
- Route quick, complete, deep, custom, provider and validation work through launcher parameters/presets whenever possible.
- Preserve TUTTO SU TUTTO lane coverage for every Full0To10 intensity.
- Provider/probe/workload-quality lanes are included by default under Full0To10 unless disabled/unavailable.
- Advisory context must be quality-filtered before content is read.
- NPU promotion to advisory requires workload quality evidence, not just decode smoke.
- Generated evidence belongs under `docs/LOCAL_VALIDATION_EVIDENCE/`.
- Full local reports remain in ignored `output/`.
- Local task pipeline outputs remain in ignored `output/local_ai_runs/` unless compact evidence is intentionally built.
- Dry-run matrix evidence proves planning/report contracts only; it does not prove provider execution.
- Context packs belong under ignored `output/ai_context_packs/`; only compact evidence belongs in `docs/LOCAL_VALIDATION_EVIDENCE/`.
- Selected semantic chunks belong under ignored `output/ai_context_packs/`; compact selected-chunks evidence may be committed under `docs/LOCAL_VALIDATION_EVIDENCE/`.
- Full-context golden proposal reports remain manual-review-only and do not apply patches by themselves.
- Proposal-derived patch specs remain draft-only under `output/patch_specs/` until reviewed and dry-run.
- Reviewed patch specs are still manual-review-only and must not be queued or applied without a separate explicit approval.
- Discovery/index/CSV-count outputs are evidence surfaces and must not override source/canonical docs.
- Every active phase must expose manifest/report/summary visibility.
- Telemetry and capability manifests must travel with AI-to-AI handoff bundles.
- Long bundles must have compact companion manifests.
- No destructive overwrite of source or analysis data.
- No Blender runtime changes unless explicitly scoped.
- Manual review remains required for source patches and proposals.

## AI rules

- Treat local AI output as draft material until validated.
- Use the unified launcher for all run-unica local AI runs.
- Use launcher-selected multistep mode for large MD/code analysis and large artifact generation.
- Use telemetry before declaring a lane successful, failed, blocked, degraded or intentionally skipped.
- Keep generated packages or workflow outputs separated by task/version.
- Do not merge unrelated generated packages automatically.
- Preserve full analysis JSON files.
- Prefer compact summaries for model input.
- Record assumptions in generated implementation notes or evidence summaries.
- Do not interpret NPU smoke success as full NPU advisory readiness.
- Do not treat Codex/GitHub-only AI as obsolete during the transition; use it as master/control-plane when appropriate.

## Legacy Blender/audio workflow

The historical Blender/audio workflow remains available as a downstream application domain:

```text
Audio input
  -> technical analysis
  -> JSON files and compact context
  -> AI planning/review
  -> generated Blender script package or patch plan
  -> stored under Scripting/ or indexAI/patch_library/
  -> manual or assisted refinement
```

It is not the core local AI architecture and must not override unified launcher flow.

## Not specified

- Final repository rename.
- Final NPU general advisory promotion gate beyond current quality report shape.
- Final provider orchestration beyond run-unica parameters and provider/probe lanes.
- Final promotion flow from draft patch spec to queued/applied patch.
- Final validation command for Blender runtime.
- Final external-controls launcher patch for all output directories and basenames.
