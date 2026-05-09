# Current capability depth map — 2026-05-09

Status: active code-derived capability map  
Scope: IA-Carmine Local AI Orchestration Workbench.

This document tells an AI what exists in the repository, how deep each capability currently goes, what it really does, what evidence it should produce, and what potential it unlocks.

It is not a wish list. When a capability is only a target, it is marked as target.

## Reading rule

Use this map after:

```text
AGENTS.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/
docs/MAIN_RUNTIME_ARCHITECTURE.md
Tools/ai/README.md
```

Code and current manifests beat older handoffs.

## Capability status labels

| Label | Meaning |
|---|---|
| Active | Implemented and wired into current workflow or toolchain. |
| Report-only | Produces evidence/diagnostics; does not mutate source. |
| Provider-gated | Runs only when explicit provider/full-run flags and environment are valid. |
| Manual-review | Produces suggestions or deterministic edits only after explicit review/apply. |
| Local-private | Runtime state/output remains local and ignored by Git. |
| Target | Architecture goal; do not claim execution unless evidence proves it. |
| Legacy/diagnostic | Available for specific diagnostics; not normal product path. |

## System depth model

Think of the project in layers:

```text
operator launcher
  -> deterministic discovery and validation
  -> context/chunk/memory/evidence preparation
  -> provider mesh and peer exchange
  -> broker/tool execution and telemetry
  -> recommendation / patch-note / patch-plan products
  -> deterministic suggestion apply on review branch
  -> review PR preparation
  -> compact Git-trackable evidence and AI handoff
```

The repository is no longer just Blender automation. It is an AI orchestration workbench with a historical Blender domain.

## 1. Operator launcher

| Field | Value |
|---|---|
| Primary file | `Tools/workflow/run_unified_local_ai_refactor.ps1` |
| Status | Active |
| Depth | End-to-end local orchestration wrapper |
| Main doc | `docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md` |

What it does:

```text
selects phases
resolves repository-owned Python
sets run identity and Stamp
controls strict real-run activation
routes lightweight, single-phase and Full0To10 runs
produces manifest/phase reports
optionally dispatches provider, evidence, patch specs and review PR phases
```

What it must not do by default:

```text
apply patches
commit
push
merge
run Blender
run FFmpeg
perform reset deletion without double confirmation
```

Potential:

```text
single operator interface for task Markdown -> full evidence -> review PR
stable machine-readable entrypoint for future agents
```

## 2. Python runtime policy

| Field | Value |
|---|---|
| Primary files | `Tools/workflow/python_env.ps1`, launcher Python resolution |
| Status | Active |
| Depth | Cross-workflow interpreter guardrail |

What it does:

```text
forces workflow/provider lanes toward repository-owned Python
rejects WindowsApps/system Python for workflow/provider lanes
keeps provider imports tied to the project .venv
propagates PythonExe into nested official/provider flows
```

Provider preflight must prove:

```text
numpy import works
openvino import works
openvino Core sees CPU/GPU.0/GPU.1/NPU on the workstation
openvino-genai exists when GenAI provider work is selected
```

Potential:

```text
prevents false GPU0/NPU failures caused by wrong interpreter
makes provider diagnostics reproducible across nested wrappers
```

## 3. Deterministic discovery and validation

| Field | Value |
|---|---|
| Primary folder | `Tools/validation/` |
| Status | Active / report-only |
| Depth | CPU authority for local truth claims |

Representative capabilities:

```text
Python syntax checks
PowerShell parser checks
validation report contract checks
Markdown inventory and line-limit checks
file-line-limit checks
repository consistency maps
patch suggestion product separation checks
workflow Python invocation policy checks
observer smoke tests
provider probe policy smoke tests
```

What it does:

```text
turns repository state into deterministic JSON/MD reports
accepts or rejects report contracts
keeps provider output from becoming unverified truth
```

Potential:

```text
lets AI-generated recommendations be gated by deterministic repo facts
supports safe CI-like validation even when providers are unavailable
```

## 4. Markdown split and documentation inventory

| Field | Value |
|---|---|
| Primary tools | `check_markdown_line_limits.py`, `check_file_line_limits.py`, `build_markdown_inventory.py` |
| Status | Active / report-only |
| Depth | Maintained-doc scalability layer |

What it does:

```text
recognizes ordinary .md files and directory-form split containers
supports <name>.md/README.md + part-xxx.md layout
prevents split members from being treated as stale prune candidates
keeps active runbooks compact and navigable
```

Potential:

```text
keeps long project knowledge readable by humans and AI agents
prevents massive monolithic docs from hiding operational truth
```

## 5. Context pack and semantic chunks

| Field | Value |
|---|---|
| Primary tools | `build_ai_context_pack.py`, `select_semantic_code_chunks.py` |
| Status | Active / report-only |
| Depth | Bounded context preparation |

What it does:

```text
builds bounded context files from selected docs/code
supports split Markdown directory layout
produces selected chunk evidence when available
keeps raw generated indexes out of source truth
```

Potential:

```text
feeds providers and future agents focused evidence instead of whole-repo noise
supports code-aware review without relying on chat memory
```

## 6. Agent state and memory

| Field | Value |
|---|---|
| Primary tools | `build_agent_state_packet.py`, `agent_runtime_sqlite_memory.py`, memory review tools |
| Status | Active / local-private |
| Depth | Continuity and handoff support |

What it does:

```text
builds agent-state packets
can persist selected input state to SQLite when allowed
supports handoff context for later runs
```

Guardrail:

```text
SQLite DB files are local/private and must not be committed.
```

Potential:

```text
lets the local AI remember task-relevant evidence without polluting Git
supports long-running project continuity through compact packets
```

## 7. Provider mesh

| Field | Value |
|---|---|
| Primary orchestrator | `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` |
| Status | Active / provider-gated |
| Depth | Multi-lane advisory/provider coordination |

Roles:

```text
GPU1/Ollama = primary advisory planner/worker
GPU0/OpenVINO = peer companion/helper and tool-request producer
NPU/OpenVINO = non-blocking microtask/tool-support lane
CPU validators = final pass/fail authority
```

What it does:

```text
runs GPU/NPU provider paths when explicitly requested
collects raw provider reports under output/**
feeds peer exchange, workload routing and evidence bundles
classifies degraded/unavailable provider state
```

Potential:

```text
parallel AI workers over shared repository evidence
hardware-aware advisory without giving providers mutation authority
```

## 8. Ollama/GPU1 primary advisory

| Field | Value |
|---|---|
| Primary tools | `run_agent_gpu_deep_planning_supervised.py`, provider probe tools |
| Status | Active / provider-gated |
| Depth | High-capacity advisory lane |

What it does:

```text
produces advisory recommendations and patch-plan reasoning
uses workload quality gates and strict JSON probes where available
records empty output and model/probe diagnostics instead of failing silently
```

Potential:

```text
main reasoning lane for whole-repo refactor and recommendation synthesis
```

## 9. GPU0/OpenVINO companion

| Field | Value |
|---|---|
| Primary tools | `run_gpu0_peer_companion_worker.py`, GPU0 support modules |
| Status | Active / provider-gated or degraded/report-only depending config |
| Depth | Secondary peer/helper lane |

What it does:

```text
consumes GPU1/provider packets when peer exchange is active
can produce companion response/evidence packets
can produce broker-routed tool requests
runs semantic OpenVINO GenAI only when companion model path is configured
otherwise can still emit numeric/static/tool-request/report-only evidence
```

Potential:

```text
turns the local GPU.0 lane into a coworker rather than passive hardware evidence
supports cross-provider disagreement checks and focused helper work
```

## 10. NPU/OpenVINO micro lane

| Field | Value |
|---|---|
| Primary surfaces | NPU provider checks, NPU decode smoke, micro companion smoke |
| Status | Active / provider-gated / non-blocking |
| Depth | Microtask and diagnostics lane |

What it does:

```text
checks NPU/OpenVINO environment
runs decode/probe diagnostics when enabled
can act as non-blocking micro support in peer/provider flows
stays out of heavy audit authority by default
```

Potential:

```text
fast low-power guardrail/classification/tool-support lane
future cheap assistant for small structured tasks while GPU handles heavy planning
```

## 11. Runtime heap / blackboard

| Field | Value |
|---|---|
| Primary files | `provider_runtime_heap.py`, `provider_runtime_heap_live_signals.py` |
| Status | Active foundation / target expansion |
| Depth | Shared state evidence layer |

What it does now:

```text
records provider/runtime heap state and live signals
supports peer reports and telemetry summaries
keeps state represented through compact reports instead of raw dumps
```

Target potential:

```text
shared blackboard for provider observations, tool outputs, validator decisions and patch products
```

Do not claim full blackboard intelligence unless a report proves that surface was emitted.

## 12. Runtime broker and tool execution

| Field | Value |
|---|---|
| Primary tool | `agent_runtime_tool_broker.py` |
| Status | Active / controlled execution |
| Depth | Brokered tool invocation surface |

What it does:

```text
executes registered/allowed runtime tool requests
normalizes execution results into reports
emits tool usage telemetry inputs
keeps provider-requested tools behind a deterministic broker surface
```

Potential:

```text
single execution gateway for future semantic tool registry
prevents provider lanes from directly mutating repository state
```

## 13. Observer consoles

| Field | Value |
|---|---|
| Primary scripts | `unified_run_observer.ps1`, `watch_unified_run_telemetry.ps1`, `watch_unified_ai_conversation.ps1`, `watch_unified_raw_debug_good_info.ps1` |
| Status | Active / visibility layer |
| Depth | Long-run human/AI observability |

What they do:

```text
surface current state and JSONL/event-style run observations
show public AI exchange and raw debug/good-info channels
reduce silent launcher hangs
help another AI inspect a running or completed run quickly
```

Potential:

```text
turns long Full0To10 runs into observable systems rather than black boxes
```

## 14. Workload quality routing

| Field | Value |
|---|---|
| Primary tool | `build_workload_quality_lane_routing.py` |
| Status | Active / report-only |
| Depth | Provider output quality gate |

What it does:

```text
prevents bad/empty/degraded provider output from being promoted silently
records quality routing status in manifests/evidence
```

Potential:

```text
allows provider mesh to scale without trusting every model response
```

## 15. Recommendation and patch-note products

| Field | Value |
|---|---|
| Primary tools | deterministic recommendation builders, patch notes quality product tools |
| Status | Active / manual-review |
| Depth | Proposal ledger generation |

What they do:

```text
turn repository evidence into recommendation or patch-note products
preserve proposal_core for future AI sessions
separate product-facing items from supplemental telemetry/debug noise
```

Guardrail:

```text
patch notes are not patches.
```

Potential:

```text
a durable ledger of what local AI discovered and what a reviewer may apply later
```

## 16. Patch suggestion dry-run/apply

| Field | Value |
|---|---|
| Primary tool | `apply_patch_suggestion_bundle.py` and `patch_suggestion_bundle/` |
| Status | Active / explicit apply only |
| Depth | Deterministic operation executor |

What it does:

```text
discovers suggestion/proposal JSON reports
classifies product versus supplemental review items
supports dry-run reports
applies deterministic operations only with explicit --apply
blocks unsafe targets such as output/**, renders/**, DB/SQLite and generated chunks
```

Potential:

```text
turns reviewed suggestions into reproducible source/doc changes without prompt-based free editing
```

## 17. Review PR preparation

| Field | Value |
|---|---|
| Primary tool | `prepare_review_pr.py` |
| Status | Active / explicit Git/PR controls |
| Depth | Product branch and PR staging surface |

What it does:

```text
stages only explicit or safely discovered include paths
rejects forbidden artifacts
commits reviewable product changes when requested
pushes and creates PRs only with explicit flags
writes review_pr_prepare JSON/MD reports
```

Potential:

```text
final bridge from task Markdown and local evidence to a human-reviewable GitHub PR
```

## 18. Compact evidence and AI-to-AI handoff

| Field | Value |
|---|---|
| Primary tools | `build_github_evidence_bundle.py`, `build_shared_toolbox_ai_to_ai_bundle.py`, telemetry summary builders |
| Status | Active / report-only |
| Depth | Git-trackable summary layer |

What they do:

```text
summarize raw output reports without committing output/**
carry provider/telemetry/patch/product summaries into docs/LOCAL_VALIDATION_EVIDENCE
preserve enough context for ChatGPT/GitHub-only sessions to continue
```

Potential:

```text
lets remote AI sessions review local results without raw runtime artifacts
```

## 19. Full0To10 final product

| Field | Value |
|---|---|
| Primary package | `full0to10_final_product/` and related builders |
| Status | Active / evidence-product layer |
| Depth | Product/readiness packaging |

What it does:

```text
packages product Markdown
evidence indexes
readiness JSON
manifest/README surfaces
quality and capability summaries
```

Potential:

```text
makes full-run output consumable as a product rather than a pile of logs
```

## 20. Blender/audio legacy domain

| Field | Value |
|---|---|
| Primary folders | `Scripting/`, Blender/audio scripts |
| Status | Legacy domain / scoped only |
| Depth | Application-domain code, not current architecture boundary |

Policy:

```text
do not modify Blender runtime broadly during AI orchestration refactors
no Blender/FFmpeg runtime unless explicitly requested
keep infrastructure/refactor work separate from artistic scene behavior
```

Potential:

```text
future downstream consumer of the orchestration workbench once AI patch/review loops are stable
```

## Capability matrix

| Capability | Status | Mutation authority | Evidence surface |
|---|---|---|---|
| Launcher orchestration | Active | No default mutation | manifest, phase reports |
| Python policy | Active | No source mutation | policy validator reports |
| Deterministic validators | Active | Report-only | output/validation, compact evidence |
| Markdown split handling | Active | Report-only unless refactor tool explicitly used | inventory/line-limit reports |
| Context pack/chunks | Active | Generated local artifacts | context/evidence reports |
| Memory | Active/local-private | DB local only | agent-state packet, memory reports |
| GPU1/Ollama | Provider-gated | Advisory only | provider reports, quality gates |
| GPU0/OpenVINO | Provider-gated/degraded-aware | Helper only | peer reports, companion evidence |
| NPU/OpenVINO | Provider-gated/non-blocking | Micro support only | probe/decode/micro reports |
| Broker | Active | Controlled tool execution | broker/telemetry reports |
| Observer | Active | No mutation | current state, JSONL/log views |
| Patch notes | Manual-review | No mutation | proposal_core ledgers |
| Patch suggestion apply | Explicit apply | Deterministic source/doc edits only | apply report |
| Review PR prep | Explicit Git/PR | Allowlisted staging/commit/push/PR | review_pr_prepare reports |
| Full0To10 final product | Active | Evidence packaging | product/readiness/manifest |
| Runtime blackboard | Active foundation/target | State coordination only | heap/live signal reports |
| Semantic tools registry | Target/partial via broker/capability docs | Capability metadata only | capability manifests |

## How another AI should use this map

1. Identify the layer involved.
2. Read the owner file or owner README.
3. Check whether the capability is active, provider-gated, report-only, manual-review or target.
4. Look for the expected evidence surface.
5. Never infer successful execution from a desired architecture statement.
6. Apply no source change unless the lane explicitly allows it and guardrails are satisfied.

## High-potential next improvements

These are safe directions, not current execution claims:

```text
make semantic tool registry more explicit and machine-readable
promote observer outputs into first-class run manifest pointers
expand runtime heap/blackboard summaries without raw dumps
add more focused smoke tests for provider/gateway contracts
make review PR draft behavior and include-path autodiscovery fully documented from current code
keep splitting monolithic workflow/provider code by responsibility under 400-line policy
```

## Minimal evidence to prove a capability ran

A valid claim should cite at least one of:

```text
launcher manifest field
phase_status entry
phase_reports entry
validator JSON report
provider raw report path plus compact summary
observer current_state/JSONL pointer
runtime tool usage telemetry
shared AI-to-AI bundle
review_pr_prepare report
patch_suggestion_bundle_apply report
```

No report, no claim.
