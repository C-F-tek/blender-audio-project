# Local AI Workflow

## Purpose

This document records the current local AI workflow for `IA-Carmine Local AI Orchestration Workbench`.

The workflow is no longer only about generating Blender scripts. It now covers local provider orchestration, GPU/NPU parallelism, workload quality gates, advisory context filtering, explicit provider diagnostics, SQLite-backed agent state, tool/function visibility and compact evidence for GitHub review.

## Primary workflow orchestrator

The active local-AI orchestration entrypoint is:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Balanced full run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Quick 5-minute style run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity quick `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Use older wrappers as internal lanes or supporting tools. Do not start full 0-to-10 local AI work from a legacy wrapper unless the user explicitly asks for that legacy/manual flow.

## Current provider mapping

```text
Ollama -> GPU/CUDA -> primary advisory provider
OpenVINO -> NPU -> probe / guardrail / decode diagnostic
```

The mapping is intentional. Do not introduce OpenVINO GPU as the primary lane.

## Hybrid master-AI / local-pipeline model

The current model is hybrid.

```text
Chat / GitHub-only AI / Codex-style control plane
  -> strategic planning, review, issue/PR orchestration, small edits, human-facing summaries

Local AI/NPU prototype pipeline
  -> heavy local context processing, validators, advisory packets, repository proposals, compact evidence

Human / master AI
  -> approves promotion from advisory/proposal outputs to patch specs, reviewed replacements, apply or merge
```

This is not an immediate full replacement for Codex/GitHub-only AI. During the transition, the master/control-plane AI coordinates GitHub work and reviews local evidence, while the project-owned local pipeline handles token-heavy local analysis and report/proposal generation.

Migration stages:

```text
Stage 0: GitHub/chat master AI controls workflow; local pipeline prepares evidence and proposals.
Stage 1: Local pipeline consumes Markdown task entrypoints and produces advisory packet/proposals.
Stage 2: Local pipeline emits draft patch specs from validated proposals.
Stage 3: Reviewed patch specs can be dry-run validated.
Stage 4: Apply/merge remains explicit and human/master-AI controlled.
Stage 5: Future local automation may replace more chat/GitHub-only work after quality gates mature.
```

## Visibility-first rule

Every local-AI run must be inspectable from compact surfaces before detailed evidence.

Required reading order after a run:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
compact Markdown or CSV summaries
detailed evidence only when needed
```

A run is not operationally clear if the next agent must open a giant bundle to understand what happened.

Every active phase should expose at least one of:

```text
phase_status
phase_reports
context_files
report_files
compact Markdown summary
CSV/JSON inventory
```

## Length policy

Long outputs are allowed as generated evidence only when indexed by compact manifests.

```text
Active operator runbook: prefer ~500 lines.
Maintained source documentation: prefer ~700 lines.
Generated compact evidence: prefer ~1200 lines.
Large historical/evidence bundles: allowed only when indexed and never as first entrypoint.
```

Do not create new monolithic AI-to-AI bundles without a companion manifest/summary.

## Current validated state

Provider baseline evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json
```

Current full-context golden path evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_core_ai_backend_context_pack_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_multistep_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/local_ai_core_tool_activation_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_master_final_smoke_20260501-232755.json
```

Validated decisions:

```text
ollama_gpu_primary_advisory: true
npu_excluded_when_unusable: true
provider_execution_seen: true
npu_decode_smoke_passed: true
```

Operational meaning:

- Ollama/GPU is usable as primary advisory provider when explicitly enabled.
- The old NPU workload report remains excluded from advisory context because it is numeric/hex-like.
- NPU/OpenVINO can execute a short decode smoke successfully through the dedicated NPU Python.
- NPU is not yet promoted to a general advisory lane.

## Current workflow

```text
Repository context and local reports
  -> unified launcher command
  -> manifest-first visibility
  -> Markdown/script inventories
  -> semantic code chunks and selected focused chunks when useful
  -> task-scoped AI context pack when useful
  -> optional SQLite-backed agent state packet
  -> workload quality gate when provider routing is requested
  -> quality-based advisory routing
  -> report-only local pipeline adapter
  -> explicit multistep provider workflow for heavy local analysis when requested
  -> primary advisory packet/proposals when explicitly requested and quality-gated
  -> repository proposals
  -> agent review evidence sufficiency and manual-review patch plans
  -> full-context golden proposal families when requested
  -> proposal-derived draft patch specs
  -> reviewed dry-run patch specs from explicit replacement plans
  -> compact evidence bundle with report, patch-plan and artifact-manifest summaries
  -> GitHub/master-AI review
```

## Unified phase / tool visibility map

| Area | Tool/script | Visible output |
|---|---|---|
| Unified launcher | `Tools/workflow/run_unified_local_ai_refactor.ps1` | run manifest with selected modes, flags, reports, context and phase status. |
| Markdown inventory | `Tools/validation/build_markdown_inventory.py` | JSON and Markdown inventory. |
| Link validation | `Tools/validation/check_docs_links.py` | JSON link report. |
| Script inventory | `Tools/validation/build_script_inventory.py` | JSON, CSV and Markdown function/class inventory. |
| Report contracts | `Tools/validation/check_validation_report_contract.py` | JSON contract report. |
| Workload quality | `Tools/validation/check_ai_workload_report_quality.py` | `ai_workload_report_quality.json`. |
| Semantic chunks | `Tools/npu/build_semantic_code_chunks.py` | semantic chunk manifest. |
| Context pack | `Tools/ai/build_ai_context_pack.py` | bounded Markdown/JSON context pack and evidence summary. |
| Agent state/memory | `Tools/ai/build_agent_state_packet.py` | agent-state packet and optional SQLite memory handoff. |
| Official adapter | `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | packet/proposals and adapter manifest. |
| Ollama advisory | `Tools/workflow/run_post_validation_ai_packet.ps1` | advisory packet/proposals and manifest. |
| Multistep provider | `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | provider workflow report/proposals when selected. |
| Legacy integrated lane | `Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1` | historical/supporting full-toolbox report when explicitly selected. |
| Patch specs | patch-spec builders/validators | review-only patch-spec manifest and validation report. |
| Reset | unified launcher reset mode | reset plan JSON/Markdown. |

If a new phase is added to the launcher, update this table and the launcher manifest contract in the same PR.

## Multistep heavy-work policy

For large Markdown files, large code files, repository-wide consistency checks, or generated artifacts that may exceed a safe single-pass context, multistep mode is the preferred local execution pattern.

Use multistep mode for:

```text
large docs/code consistency reviews
cross-file Markdown/code contract checks
proposal generation from master-AI task files
candidate patch-spec generation from validated proposals
large file generation that needs staged review
provider evidence that must stay compact and Git-trackable
```

The expected heavy-work flow is:

```text
master-AI writes or updates docs/LOCAL_AI_TASKS/*.md
unified launcher builds manifest/context/report surfaces
local adapter runs report-only/proposal-only analysis
optional explicit multistep provider workflow produces provider evidence
proposal validators check output contracts
master-AI/human reviews proposals before patch specs or apply
```

Do not use multistep mode to bypass guardrails. It remains:

```text
explicit provider execution only
report-only/proposal-only by default
no automatic patch apply
no automatic merge
NPU remains probe / guardrail / decode diagnostic
Ollama/GPU remains primary advisory behind quality gate
```

## Local Markdown task runner

The unified launcher is the first entrypoint for full 0-to-10 flows. The older Markdown task wrappers remain useful for task-scoped adapter runs.

Task-scoped wrapper:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -TaskBranch codex/full-context-ai-npu-golden-run
```

The project-owned runner path invokes the local pipeline adapter:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -TaskBranch codex/full-context-ai-npu-golden-run `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}"'
```

Default adapter behavior:

```text
reads the generated local_ai_prompt.md
uses it as context for report-only/proposal-only repository tools
writes outputs under output/local_ai_runs/<run>/pipeline/
validates repository proposals when produced
does not apply patches
does not execute providers unless explicit provider flags are passed
```

Explicit multistep adapter mode:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 `
  -PromptFile .\output\local_ai_runs\<run>\local_ai_prompt.md `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -RunDir .\output\local_ai_runs\<run> `
  -Profile npu `
  -RunMultistepProviderWorkflow `
  -RunOllamaProbe `
  -RunNpuProbe `
  -RunNpuDecodeSmoke `
  -UsePrimaryAdvisoryProvider `
  -BuildEvidence
```

## Provider multistep lane

The multistep provider wrapper is a supporting lane, not the first full 0-to-10 entrypoint:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_parallel_ai_provider_multistep.ps1 `
  -Profile npu `
  -RunOllamaProbe `
  -RunNpuProbe `
  -RunNpuDecodeSmoke `
  -UsePrimaryAdvisoryProvider `
  -Basename parallel_gpu_npu_multistep_real_npu_v2 `
  -ProposalBasename parallel_gpu_npu_multistep_real_npu_v2_proposals `
  -EvidenceBasename parallel_gpu_npu_multistep_real_npu_v2_evidence
```

This lane performs:

| Step | Action | Output family |
|---|---|---|
| 1 | Workload quality gate | `output/validation/ai_workload_report_quality.json` |
| 2 | Parallel provider probes / diagnostics | `output/validation/local_provider_probe.json`, `output/validation/npu_decode_smoke_diagnostic.json` |
| 3 | Quality-based routing and NPU remediation | `output/validation/ai_workload_quality_lane_routing.json`, `output/validation/npu_decode_quality_remediation.json` |
| 4 | Primary advisory packet/proposals | `output/ai_packets/*` |
| 5 | Pushable evidence bundle | `docs/LOCAL_VALIDATION_EVIDENCE/*` |

Use this wrapper only for explicit provider diagnostics/evidence or when the unified launcher calls it as a selected phase. Do not use it as an implicit replacement for report-only local task processing.

## Key tools

| File | Role |
|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | Canonical local AI orchestrator and full 0-to-10 entrypoint. |
| `Tools/workflow/run_local_ai_markdown_task.ps1` | Builds task-scoped non-interactive local AI run packets from Markdown task entrypoints. |
| `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | Project-owned adapter from local task prompt to report-only/proposal-only pipeline outputs; can explicitly call multistep provider workflow. |
| `Tools/workflow/run_local_ai_core_tool_activation.ps1` | Supporting app-agnostic activation lane retained for focused/legacy validation; prefer the unified launcher. |
| `docs/LOCAL_AI_TASKS/` | Markdown task entrypoints for non-interactive local runs. |
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
| `Tools/ai/run_local_provider_probe.py` | Explicit local provider probes for Ollama/GPU and NPU/OpenVINO. |
| `Tools/ai/run_npu_decode_smoke_diagnostic.py` | Explicit OpenVINO/NPU decode smoke through dedicated NPU Python. |
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
| `Tools/workflow/run_post_validation_ai_packet.ps1` | Builds packet/proposals and supports primary advisory provider mode. |
| `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | Supporting parallel GPU/NPU multistep lane for explicit provider evidence. |

## Evidence workflow

Because `output/` is ignored, use compact evidence bundles. Add only the specific compact evidence files produced by the intended run.

```powershell
python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename latest_ai_workflow_evidence

git add `
  .\docs\LOCAL_VALIDATION_EVIDENCE\latest_ai_workflow_evidence.json `
  .\docs\LOCAL_VALIDATION_EVIDENCE\latest_ai_workflow_evidence.md

git commit -m "test: add local ai workflow evidence bundle"
git push
```

Do not bulk-add the whole evidence directory unless a human explicitly reviewed every changed evidence file.

For the AI pipeline dry-run matrix:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error --matrix-workers 12 --repeat-cases 2
python .\Tools\ai\build_dry_run_matrix_evidence_bundle.py --repo-root . --basename ai_pipeline_dry_run_matrix_evidence
python .\Tools\validation\check_dry_run_matrix_evidence_bundle.py --repo-root . --evidence .\docs\LOCAL_VALIDATION_EVIDENCE\ai_pipeline_dry_run_matrix_evidence.json --output .\output\validation\dry_run_matrix_evidence_bundle.json
```

## Requirements for safe local generation

- Start full 0-to-10 flows from the unified launcher.
- Provider execution must be explicit.
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
- Every active phase must expose manifest/report/summary visibility.
- Long bundles must have compact companion manifests.
- No destructive overwrite of source or analysis data.
- No Blender runtime changes unless explicitly scoped.
- Manual review remains required for source patches and proposals.

## AI rules

- Treat local AI output as draft material until validated.
- Use the unified launcher for full 0-to-10 local AI runs.
- Use multistep mode for large MD/code analysis and large artifact generation.
- Keep generated packages or workflow outputs separated by task/version.
- Do not merge unrelated generated packages automatically.
- Preserve full analysis JSON files.
- Prefer compact summaries for model input.
- Record assumptions in generated implementation notes or evidence summaries.
- Do not interpret NPU smoke success as full NPU advisory readiness.
- Do not treat Codex/GitHub-only AI as obsolete during the transition; use it as master/control-plane when appropriate.

## Legacy Blender/audio workflow

The historical workflow remains available:

```text
Audio input
  -> technical analysis
  -> JSON files and compact context
  -> AI planning/review
  -> generated Blender script package or patch plan
  -> stored under Scripting/ or indexAI/patch_library/
  -> manual or assisted refinement
```

However, this is now a downstream application domain, not the core local AI architecture.

## Not specified

- Final repository rename.
- Final NPU general advisory promotion gate beyond current quality report shape.
- Final provider orchestration beyond explicit workflow flags.
- Final promotion flow from draft patch spec to queued/applied patch.
- Final validation command for Blender runtime.
- Final external-controls launcher patch for all output directories and basenames.
