<!-- IA-CARMINE-MD-SPLIT: part -->
# LOCAL_AI_RUN_BOOTSTRAP — parte 001 di 002

Sorgente indice: [`../LOCAL_AI_RUN_BOOTSTRAP.md`](../LOCAL_AI_RUN_BOOTSTRAP.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Local AI Run Bootstrap

This file is the first local-run bootstrap for AI assistants working inside a checked-out copy of this repository.

Use it before changing files during local runs. It is intentionally operational and conservative.

## FIRST ENTRY — Unified Local AI run unica

When Carmine asks for any of these phrases, open the unified launcher runbook first:

```text
Tutto su tutto
run unica
run completa
full toolbox
0-10
cassetta degli attrezzi completa
multi-macro patch
multi-script
multi-fase
semi-automatic process
flusso unico
quick test
smoke
full validation
provider run
GPU/NPU run
memory handoff
patch specs
reset
tool promotion
runtime broker telemetry
telemetry summary
AI-to-AI bundle
auto-discovery
index repair
CSV count
line count
file line limit
function/class/method inventory
```

Primary current runbook:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Primary current launcher:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Current stable supporting docs:

```text
FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
docs/KNOWN_LIMITATIONS.md
docs/TECH_DEBT_TRACKER.md
```

No other local-AI runner is an active first entrypoint. Supporting wrappers may be called by the launcher, but they must not be used as separate operator paths unless a future PR explicitly promotes them into the launcher manifest/phase contract.

## Current active branch phase

```text
Baseline: master after PR #187 merge
Current documentation PR: #193 docs(ai): align operational docs with post-PR187 code state
Next clean report-only foundation candidate: PR #192
Useful but diverged evidence branch: PR #191
Mode: GitHub-only/API when maintainer is away; local validation only when explicitly requested
```

PR #187 is not the active branch anymore. It is the merged launcher baseline.

Do not infer runtime bundle contents from file existence alone. Inspect manifest, telemetry, capability, provider diagnostics, workload quality, patch-plan and final-summary fields.

## Run unica rule

The primary operating model is not a set of separate profiles. It is one parameterized run:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters
-No* flags = explicit opt-out from selected lanes
400-line policy applies to maintained docs and source files
limitations are backlog to overcome, not reasons to skip available tools
```

`quick`, `balanced`, `deep` and `custom` change budgets, limits, rounds, context, tokens, wait times and other execution parameters. They do not create smaller semantic scopes and must not remove lanes silently.

If the operator does not want a lane, the operator disables it explicitly with a `-No*` flag or documents the exclusion.

## One-flow rule

All local-AI execution variants must be modeled as launcher modes, parameters, presets or flags behind the run unica.

This includes:

```text
quick tests
smoke tests
complete runs
deep runs
full validation
documentation cleanup
script/tool inventory
provider runs
Ollama advisory
NPU probes
multistep provider workflow
SQLite memory handoff
context packs
semantic chunks
selected chunk evidence
patch-spec generation
runtime broker telemetry
runtime/hardware capability manifest
telemetry summary
project-tool promotion evidence
auto-discovery and index-drift evidence
index repair planning/reporting
CSV/count surfaces
file-line-limit surfaces
reset cleanup
legacy full-toolbox integrated behavior
```

Do not start from these as first entrypoints:

```text
run_local_ai_markdown_task.ps1
run_local_ai_task_via_pipeline.ps1
run_post_validation_ai_packet.ps1
run_parallel_ai_provider_multistep.ps1
run_local_validation_after_refactor.ps1
run_agent_review_full_toolbox_decision_loop_integrated.ps1
full-toolbox-0-to-10-semi-automatic-procedure.md
historical PR handoff or master-branch code-refactor runbooks
```

They are implementation lanes, historical material or scoped helpers behind the unified launcher.

## TUTTO SU TUTTO rule

Every run unica with `-Full0To10` is **TUTTO SU TUTTO**.

`Full0To10` is opt-out by lane, not opt-in per capability. Once `-Full0To10` is selected, the default assumption is that provider/probe/workload-quality, telemetry, discovery, index, CSV/count and file-line-limit lanes are included when relevant. If the operator does not want a lane, the operator must disable it explicitly with `-No*` flags or a documented exclusion.

The perimeter of `tutto` can expand. When a new stable validator, broker tool, provider diagnostic, memory/context surface, project-tool registry, repository-consistency check, telemetry surface, discovery/index surface, CSV/count surface, file-line-limit surface or evidence builder is promoted, it must be added to the run unica full-run contract or explicitly excluded with rationale.

## Current operating chain

```text
unified launcher command from unified-local-ai-refactor-launcher.md
  -> manifest-first run visibility
  -> inventories / reports / context packs / memory packet
  -> discovery, index-drift, CSV/count and file-line-limit evidence when relevant
  -> workload quality routing for Full0To10/provider lanes
  -> official pipeline adapter when selected
  -> Ollama advisory / primary provider lane unless disabled or diagnosed unavailable
  -> multistep provider probes unless disabled or diagnosed unavailable
  -> deterministic recommendations
  -> review-only patch specs / patch bundles
  -> runtime broker report and telemetry
  -> runtime/hardware capability manifest
  -> full toolbox telemetry summary
  -> shared production AI-to-AI bundle
  -> explicit apply only after review
  -> validation
  -> PR
```

Full toolbox body model remains valid, but it is now driven by the unified launcher:

```text
Skeleton / contracts
Nervous system / orchestration
Brain / decision layer
Eyes / evidence collectors
Immune system / validators
Memory / SQLite-backed local state when enabled
Muscles / patch bundle apply lane only after explicit review
Bloodstream / compact evidence and telemetry
Hands / GitHub + CLI
```

## Purpose

The local AI should autonomously read the current task context and repository guardrails before planning or editing.

The bootstrap prevents these common failures:

```text
starting from stale context
editing runtime files during documentation/backend tasks
running providers implicitly outside Full0To10/provider-selected workflows
forgetting active execution plans
forgetting compact evidence bundles
mixing GitHub-only review with local workstation evidence
opening huge evidence bundles before the manifest/summary
starting from superseded 0-to-10 runbooks
using a supporting wrapper as an active first entrypoint
triggering audio/media output during AI/tooling runs
inferring run success from file existence instead of telemetry
silently dropping a full-run lane that should be opt-out
mistaking quick/balanced/deep/custom for separate scopes instead of parameters
using historical limitation notes to skip available tools
creating new maintained docs/source files over 400 lines
```

## Visibility-first rule

Every local AI run must be understandable from compact surfaces before opening detailed evidence.

Required reading order after a run:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
runtime tool telemetry and capability manifest
full toolbox telemetry summary
production AI-to-AI bundle
compact Markdown, CSV/count or file-line-limit summaries
detailed evidence only when needed
```

A run is not operationally clear if the next agent must open a giant bundle to understand what happened.

Do not create new monolithic AI-to-AI bundles without a companion manifest/summary.

## Telemetry-first AI rule

Telemetry is a primary input for local and cloud AI agents.

The next AI must inspect:

```text
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md or runtime_hardware_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

before declaring a lane successful, failed, blocked, degraded, intentionally disabled or unavailable.

Important fields:

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

File existence alone is not evidence of successful execution.

## Discovery, index repair and CSV/count rule

Discovery and count surfaces are evidence lanes for full runs.

Expected surfaces when relevant:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV
Python line-count CSV/MD
file-line-limit JSON/MD
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD
repository consistency map/smoke JSON/MD
auto-discovery report when scanner/index visibility drift is suspected
index repair plan/report when generated indexes are stale or missing
```

Policy:

```text
CSV/count/file-line-limit outputs are evidence surfaces, not source authority.
Generated indexes and code chunks are not hand-maintained source.
Do not commit output/**.
Do not commit indexAI/code_chunks/**.
Index repair is plan/report-first unless explicitly requested.
```

## 400-line policy for local-run docs and source

Maintained documentation and source files must stay under 400 lines.

```text
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Validator:

```text
Tools/validation/check_file_line_limits.py
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```

Long historical/evidence files may exist only when indexed and kept out of the primary reading path.

## Hybrid master-AI / local-pipeline model

The current operating model is hybrid.

```text
Chat / GitHub-only AI / Codex-style control plane
  -> strategic planning, review, issue/PR orchestration, small edits, human-facing summaries

Unified local AI pipeline
  -> heavy local context processing, validators, advisory packets, repository proposals, compact evidence

Human / master AI
  -> approves promotion from advisory/proposal outputs to patch specs, reviewed replacements, apply or merge
```

Codex/GitHub-only AI is not obsolete. It remains useful as a master/control-plane during the transition. The unified local pipeline should take the token-heavy local work and produce report-only/proposal-only artifacts for review.

## Non-interactive entrypoint mode

Local AI runners may be launched without an interactive chat, but the launcher remains the entrypoint.

Use the unified launcher runbook for current commands and flags:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

A local AI runner started from a task file must still read `AGENTS.md` first, then this bootstrap, then the task file. The task file may define task intent, but execution still routes through the unified launcher unless a human explicitly scopes a one-off helper invocation.

## Phase 0 - Repository sync preflight

Before running an AI task locally, confirm:

```text
current branch
remote sync state
working tree state
whether dirty changes are intentional
Python/venv resolution
ignored output/cache/state files are not staged
```

Do not continue if the working tree contains unrelated changes unless the task explicitly covers them or `-AllowDirty` is intentionally supplied to the unified launcher.
