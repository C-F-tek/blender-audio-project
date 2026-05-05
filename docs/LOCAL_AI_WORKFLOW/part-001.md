<!-- IA-CARMINE-MD-SPLIT: part -->
# LOCAL_AI_WORKFLOW — parte 001 di 002

Sorgente indice: [`../LOCAL_AI_WORKFLOW.md`](../LOCAL_AI_WORKFLOW.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Local AI Workflow

## Purpose

This document records the current local AI workflow for `IA-Carmine Local AI Orchestration Workbench`.

The workflow is no longer only about generating Blender scripts. It now covers run-unica orchestration, GPU/NPU parallelism, workload quality gates, advisory context filtering, provider diagnostics, SQLite-backed agent state, tool/function visibility, discovery/index repair, CSV/count surfaces and compact evidence for GitHub review.

## Primary workflow orchestrator

The active local-AI orchestration entrypoint is:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

All local-AI execution variants are launcher modes, parameters, presets or flags behind the run unica. This includes quick tests, complete runs, deep runs, provider probes, memory handoff, patch specs, reset, discovery/index repair visibility, CSV/count surfaces and full validation.

Do not start local-AI work from legacy wrappers. Supporting wrappers remain implementation lanes behind the launcher and must be visible in launcher manifest/status/report surfaces when used.

## Run unica / TUTTO SU TUTTO workflow contract

The primary operating model is one parameterized run:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters
-No* flags = explicit opt-out from selected lanes
```

`-Full0To10` means every active repository-understanding lane participates unless it is explicitly disabled, unavailable, represented as dry-run planned state, or excluded with a documented rationale. `quick`, `balanced`, `deep` and `custom` change budgets, limits and depth; they do not change the lane set.

The perimeter of `tutto` is expandable. When a new stable lane is promoted, such as a broker tool, validator, provider diagnostic, repository-consistency report, project-tool registry, memory/context builder, discovery/index surface, CSV/count surface or evidence surface, update this workflow, the launcher contract and the task index so the new lane is either included in the run unica full flow or explicitly excluded with rationale.

A run-unica workflow is not complete when a lane silently disappears. Missing phases must be visible in manifest, telemetry, warnings or errors.

## Current provider mapping

```text
Ollama -> GPU/CUDA -> primary advisory provider for Full0To10 when available and quality-gated
OpenVINO -> NPU -> probe / guardrail / decode diagnostic for Full0To10 when available
```

The mapping is intentional. Do not introduce OpenVINO GPU as the primary lane.

Provider execution is explicit when the operator selects `-Full0To10` or provider/probe modes. It is not an additional per-lane opt-in after `-Full0To10` is selected.

## Hybrid master-AI / unified local-pipeline model

The current model is hybrid.

```text
Chat / GitHub-only AI / Codex-style control plane
  -> strategic planning, review, issue/PR orchestration, small edits, human-facing summaries

Unified local AI pipeline
  -> heavy local context processing, validators, advisory packets, repository proposals, compact evidence

Human / master AI
  -> approves promotion from advisory/proposal outputs to patch specs, reviewed replacements, apply or merge
```

This is not an immediate full replacement for Codex/GitHub-only AI. During the transition, the master/control-plane AI coordinates GitHub work and reviews local evidence, while the unified local pipeline handles token-heavy local analysis and report/proposal generation.

Migration stages:

```text
Stage 0: GitHub/chat master AI controls workflow; unified launcher prepares evidence and proposals.
Stage 1: Unified launcher consumes task entrypoints and produces advisory packet/proposals.
Stage 2: Unified launcher emits draft patch specs from validated proposals.
Stage 3: Reviewed patch specs can be dry-run validated.
Stage 4: Apply/merge remains explicit and human/master-AI controlled.
Stage 5: Future automation may replace more chat/GitHub-only work after quality gates mature.
```

## Visibility-first rule

Every local-AI run must be inspectable from compact surfaces before detailed evidence.

Required reading order after a run:

```text
launcher command from unified-local-ai-refactor-launcher.md
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
telemetry summary / runtime tool telemetry / capability manifest
shared production AI-to-AI bundle
compact Markdown or CSV/count summaries
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
CSV/count surface
index/discovery report or plan
```

## Telemetry-first AI reasoning rule

Telemetry is a primary reasoning input for local and cloud AI agents.

The next AI must inspect telemetry before deciding that a run succeeded, failed or degraded. File existence alone is insufficient.

Required telemetry/capability surfaces include:

```text
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

AI-critical fields include:

```text
tool_call_entry_count
executed_count
failed_count
blocked_count
broker_reports
provider_advisory_state
provider_failure_reasons
degraded_provider_components
gpu_metrics_source
round_duration_source
patch_application_performed
source_writes_performed
```

Use these fields to distinguish:

```text
executed
failed
blocked
degraded
intentionally disabled
unavailable
planned-only dry run
```

## Discovery, index repair and CSV/count workflow

Discovery and count surfaces are first-class evidence lanes for run-unica planning and review.

Expected surfaces when relevant:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV
Python line-count CSV/MD
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD
repository consistency map/smoke JSON/MD
auto-discovery report when scanner/index visibility drift is suspected
index repair plan/report when generated indexes are stale or missing
```

Policy:

```text
CSV/count outputs are evidence surfaces, not source authority.
Generated indexes and code chunks are not hand-maintained source.
Do not commit output/**.
Do not commit indexAI/code_chunks/**.
Index repair is plan/report-first unless explicitly requested.
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

Current compact state docs:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
```

Current active review pass:

```text
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
```

Validated production states:

```text
broker telemetry validated by run 20260505-073332
provider diagnostics and deterministic recovery validated by run 20260505-081141
GPU sync timing source smoke validated with rounds[*].elapsed_seconds
ollama_gpu_primary_advisory is included by default in Full0To10 when available and quality-gated
npu_excluded_when_unusable=true
npu_decode_smoke_passed=true in previous evidence
```

Operational meaning:

- Ollama/GPU is usable as primary advisory provider under Full0To10 when available and quality-gated.
- Provider failure must be reported through provider failure reasons and degraded components.
- The old NPU workload report remains excluded from advisory context when it is numeric/hex-like.
- NPU/OpenVINO can execute a short decode smoke successfully through the dedicated NPU Python.
- NPU is not yet promoted to a general advisory lane.

## Current workflow

```text
Repository context and local reports
  -> unified launcher command
  -> manifest-first visibility
  -> Markdown/script inventories
  -> CSV/count evidence surfaces
  -> discovery/index drift reports or plans when relevant
  -> semantic code chunks and selected focused chunks when useful
  -> task-scoped AI context pack when useful
  -> SQLite-backed agent state packet when enabled
  -> workload quality gate for Full0To10/provider lanes
  -> quality-based advisory routing
  -> report-only local pipeline adapter
  -> multistep provider workflow unless disabled/unavailable
  -> primary advisory packet/proposals unless disabled/unavailable and quality-gated
  -> repository proposals
  -> agent review evidence sufficiency and manual-review patch plans
  -> full-context golden proposal families when requested
  -> proposal-derived draft patch specs
  -> reviewed dry-run patch specs from explicit replacement plans
  -> runtime broker telemetry and capability manifest
  -> full toolbox telemetry summary
  -> compact evidence bundle with report, patch-plan and artifact-manifest summaries
  -> shared production AI-to-AI bundle
  -> GitHub/master-AI review
```

## Unified phase / tool visibility map

| Area | Tool/script | Visible output | Launcher status |
|---|---|---|---|
| Unified launcher | `Tools/workflow/run_unified_local_ai_refactor.ps1` | run manifest with selected parameters, flags, reports, context and phase status | canonical |
| Markdown inventory | `Tools/validation/build_markdown_inventory.py` | JSON and Markdown inventory | `md` mode |
| Link validation | `Tools/validation/check_docs_links.py` | JSON link report | `md` / validation phases |
| Script inventory | `Tools/validation/build_script_inventory.py` | JSON, CSV and Markdown function/class inventory | `python` mode |
| Python line count | broker/runtime line-count helper and validation reports | CSV and Markdown line-count surfaces | inventory/evidence lane |
| Discovery/index repair | scanner/index validators and repair planners | report-only discovery/index repair reports | validation/refactor support lane |
| Report contracts | `Tools/validation/check_validation_report_contract.py` | JSON contract report | `json` / `contract` phases |
| Workload quality | `Tools/validation/check_ai_workload_report_quality.py` | `ai_workload_report_quality.json` | provider quality gate |
| Semantic chunks | `Tools/npu/build_semantic_code_chunks.py` | semantic chunk manifest | `chunks` mode |
| Context pack | `Tools/ai/build_ai_context_pack.py` | bounded Markdown/JSON context pack and evidence summary | `context_pack` mode |
| Agent state/memory | `Tools/ai/build_agent_state_packet.py` | agent-state packet and optional SQLite memory handoff | `agent_state` mode |
| Official adapter | `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | packet/proposals and adapter manifest | `official` mode / implementation lane |
| Ollama advisory | `Tools/workflow/run_post_validation_ai_packet.ps1` | advisory packet/proposals and manifest | provider/advisory implementation lane for Full0To10 unless disabled/unavailable |
| Multistep provider | `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | provider workflow report/proposals | provider implementation lane for Full0To10 unless disabled/unavailable |
| Legacy integrated lane | `Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1` | integrated full-toolbox report when selected | supporting selected phase only, not entrypoint |
| Runtime broker | `Tools/ai/agent_runtime_tool_broker.py` | broker report and runtime tool usage telemetry | supporting full-toolbox lane |
| Runtime capability manifest | `Tools/ai/build_runtime_tool_capability_manifest.py` | runtime tool capability manifest JSON/MD | production handoff |
| Telemetry summary | `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | full toolbox run telemetry summary JSON/MD | production handoff |
| Production bundle | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | shared toolbox AI-to-AI bundle and final summary | production handoff |
| Patch specs | patch-spec builders/validators | review-only patch-spec manifest and validation report | `patch_specs` mode |
| Reset | unified launcher reset mode | reset plan JSON/Markdown | `reset` mode |

If a new phase is added to the launcher, update this table and the launcher manifest contract in the same PR.

## Multistep heavy-work policy

For large Markdown files, large code files, repository-wide consistency checks, or generated artifacts that may exceed a safe single-pass context, multistep behavior must still be selected through the unified launcher.

Use multistep behavior for:

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
official adapter lane runs report-only/proposal-only analysis
Full0To10/provider lane produces provider evidence unless disabled/unavailable
proposal validators check output contracts
master-AI/human reviews proposals before patch specs or apply
```

Do not use multistep mode to bypass guardrails. It remains:

```text
report-only/proposal-only by default
no automatic patch apply
no automatic merge
NPU remains probe / guardrail / decode diagnostic
Ollama/GPU remains primary advisory behind quality gate
Full0To10 provider lanes are opt-out, not extra opt-in
```

## Supporting wrapper policy

These wrappers are not first entrypoints:

```text
Tools/workflow/run_local_ai_markdown_task.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
Tools/workflow/run_parallel_ai_provider_multistep.ps1
Tools/workflow/run_local_validation_after_refactor.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1
```

They may be used only as:

```text
launcher implementation lanes
focused validator/debug targets
historical compatibility lanes explicitly selected by the launcher
```

A wrapper promoted into the active flow must appear in:

```text
launcher mode/parameter/flag
unified manifest phase_status
unified manifest phase_reports when reports are produced
this visibility map
UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md when manifest shape changes
```
