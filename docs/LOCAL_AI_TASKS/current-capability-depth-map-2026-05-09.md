# Current capability depth map — 2026-05-09

Status: active code-derived capability map  
Scope: IA-Carmine Local AI Orchestration Workbench.

This compact map tells an AI what exists, how deep each capability goes, what it produces, and which guardrails apply. It intentionally separates active capability from architecture targets.

## Read after

```text
AGENTS.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/
docs/MAIN_RUNTIME_ARCHITECTURE.md
Tools/ai/README.md
```

Code, current reports and manifests override older handoffs.

## Status labels

| Label | Meaning |
|---|---|
| Active | Implemented and wired into current workflow/toolchain. |
| Report-only | Produces diagnostics/evidence; does not mutate source. |
| Provider-gated | Requires explicit provider/full-run flags and valid runtime environment. |
| Manual-review | Produces suggestions or deterministic edits only after explicit review/apply. |
| Local-private | Runtime state/output remains local and ignored by Git. |
| Target | Architecture goal; no execution claim without evidence. |
| Legacy/diagnostic | Available for focused diagnostics, not normal product path. |

## Depth model

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

The repository is now an AI orchestration workbench with a historical Blender/audio domain, not a Blender-only repo.

## Capability summary

| Capability | Status | Depth | Owner / entrypoint | Evidence surface |
|---|---|---|---|---|
| Operator launcher | Active | End-to-end wrapper | `Tools/workflow/run_unified_local_ai_refactor.ps1` | manifest, phase reports |
| Parameter decision map | Active | CLI/lane guidance | `unified-launcher-parameter-decision-map-2026-05-09.md` | doc contract |
| Script aging visibility | Active/docs-only | hidden/legacy script review map | `script-aging-visibility-audit-2026-05-09.md` | review queue, local inventory command |
| Repo-owned Python policy | Active | workflow/provider guardrail | `Tools/workflow/python_env.ps1`, launcher resolver | policy reports, stderr/classification |
| Deterministic validation | Active/report-only | CPU authority | `Tools/validation/` | JSON/MD validation reports |
| Markdown split/inventory | Active/report-only | doc scalability | `check_markdown_line_limits.py`, `check_file_line_limits.py`, `build_markdown_inventory.py` | inventory/line-limit reports |
| Context pack/chunks | Active/report-only | bounded evidence prep | `build_ai_context_pack.py`, `select_semantic_code_chunks.py` | context pack, selected chunk evidence |
| Agent state/memory | Active/local-private | continuity support | `build_agent_state_packet.py`, SQLite memory tools | agent-state packet, memory reports |
| Provider mesh | Active/provider-gated | multi-lane advisory | `run_agent_gpu_npu_parallel_orchestrator.py` | provider reports, orchestrator reports |
| GPU1/Ollama advisory | Active/provider-gated | primary planning lane | `run_agent_gpu_deep_planning_supervised.py`, provider probes | GPU/Ollama reports, quality gates |
| GPU0/OpenVINO companion | Active/provider-gated/degraded-aware | peer/helper lane | `run_gpu0_peer_companion_worker.py` | peer/companion packets |
| NPU/OpenVINO micro lane | Active/provider-gated/non-blocking | micro diagnostics/support | NPU probes, decode smoke, micro smoke | probe/decode/micro reports |
| Runtime heap / blackboard | Active foundation/target expansion | compact shared state | `provider_runtime_heap.py`, `provider_runtime_heap_live_signals.py` | heap/live-signal reports |
| Runtime broker | Active | controlled execution | `agent_runtime_tool_broker.py` | broker reports, tool telemetry |
| Observer consoles | Active | long-run visibility | `unified_run_observer.ps1`, watch scripts | current state, JSONL/log views |
| Workload quality routing | Active/report-only | provider quality gate | `build_workload_quality_lane_routing.py` | workload quality reports |
| Recommendation products | Active/manual-review | proposal synthesis | deterministic recommendation / patch-note tools | recommendation/product reports |
| Patch suggestion apply | Active/explicit apply only | deterministic operation executor | `apply_patch_suggestion_bundle.py`, `patch_suggestion_bundle/` | apply report |
| Review PR preparation | Active/explicit Git controls | review branch/PR bridge | `prepare_review_pr.py` | `review_pr_prepare` reports |
| Evidence/handoff bundles | Active/report-only | Git-trackable summary | `build_github_evidence_bundle.py`, `build_shared_toolbox_ai_to_ai_bundle.py` | compact evidence/bundle docs |
| Full0To10 final product | Active | product/readiness packaging | `full0to10_final_product/` builders | product, readiness, manifest |
| Semantic tools registry | Target/partial | capability metadata model | broker/capability docs and manifests | capability manifests |
| Blender/audio domain | Legacy/scoped | downstream app domain | `Scripting/`, Blender/audio scripts | scoped app validation only |

## What each layer really does

### Launcher

Selects phases, resolves repository Python, applies strict real-run activation, manages `Stamp`, routes `smoke`, single-phase, `LightFull0To10` and `Full0To10`, and writes phase/manifest evidence. It does not apply patches, commit, push, merge, run Blender or run FFmpeg by default.

### Deterministic validators

Turn repository state into pass/fail JSON/MD evidence: Python syntax, PowerShell parse, report contracts, file limits, Markdown inventory, repository consistency, workflow Python policy, observer smoke and patch-suggestion product separation. CPU validators remain the final local authority.

### Context, chunks and memory

Prepare bounded input/evidence surfaces for providers and future agents. Context/chunk outputs are generated evidence, not source authority. SQLite memory is local/private and must not be committed.

### Provider mesh

Runs only when explicitly selected and environment is valid. GPU1/Ollama is the primary advisory/planning lane. GPU0/OpenVINO is a companion/helper and tool-request producer. NPU/OpenVINO is non-blocking microtask/tool-support/diagnostic support. Providers advise; they do not mutate source directly.

### Runtime heap, broker and observer

The heap/live-signal layer records compact shared runtime state. The broker executes controlled tool requests and emits telemetry. Observer scripts expose current state, AI conversation and raw debug/good-info streams so long runs are inspectable instead of silent.

### Recommendation, patch and review PR lane

Recommendation and patch-note products are proposal ledgers. `apply_patch_suggestion_bundle.py` can apply only deterministic operations with explicit apply controls. `prepare_review_pr.py` stages only explicit or safely discovered paths and performs commit/push/PR only with explicit flags.

### Evidence, final product and script visibility

Evidence builders summarize raw `output/**` reports into compact Git-trackable handoff surfaces. Full0To10 product builders package readiness/product manifests so a run becomes reviewable product material, not only logs. Script aging audits are documentation-only visibility queues: they notice hidden/legacy wrappers but do not delete or mark obsolete without follow-up proof.

## Provider role boundaries

```text
GPU1/Ollama      = primary advisory planner/worker
GPU0/OpenVINO    = peer companion/helper, degraded-aware when unconfigured
NPU/OpenVINO     = microtask responder, diagnostics, non-blocking support
CPU validators   = deterministic pass/fail authority
Runtime broker   = controlled execution gateway
```

Do not promote GPU0, NPU or provider output over deterministic validators unless a future explicit contract changes that authority.

## Mutation authority matrix

| Surface | May mutate source by default? | Notes |
|---|---:|---|
| Launcher | No | Dispatch only unless explicit product flags are used. |
| Validators | No | Report-only. |
| Context/chunk/memory builders | No source mutation | Generated/local-private artifacts only. |
| Providers | No | Advisory/helper/micro roles only. |
| Broker | Controlled runtime execution | Must enforce guardrails. |
| Patch notes/recommendations | No | Proposal ledgers only. |
| Patch suggestion apply | Only with explicit apply | Deterministic operations, unsafe targets blocked. |
| Review PR prep | Only with explicit Git/PR flags | Allowlisted staging/commit/push/PR. |
| Script aging audit | No | Notice/review queue only; no deletion. |
| Blender/audio scripts | No unless scoped | Legacy application domain. |

## Evidence needed to claim execution

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
script aging inventory or audit entry for visibility claims
```

No report, no claim.

## High-potential next improvements

These are directions, not execution claims:

```text
make semantic tool registry more explicit and machine-readable
promote observer outputs into first-class manifest pointers
expand runtime heap/blackboard summaries without raw dumps
add focused smoke tests for provider/gateway contracts
document review PR draft/include-path autodiscovery from current code
continue splitting monolithic workflow/provider code by responsibility
run local oldest-to-newest script inventory and promote reviewed findings only
```

## Anti-confusion rules for future AI agents

```text
Do not infer current capability from target architecture alone.
Do not treat LightFull0To10 as provider execution proof.
Do not treat patch notes as patches.
Do not trust provider output without workload quality and validators.
Do not use system Python for workflow/provider lanes.
Do not stage output/**, DB, renders or generated chunks.
Do not delete or deprecate old scripts from age alone.
Do not change Blender/audio domain during infrastructure docs/refactors unless scoped.
```
