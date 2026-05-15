# AI Tools

`Tools/ai/` contains report-oriented tools for IA-Carmine local AI orchestration, context building, provider diagnostics, deterministic recommendations, telemetry, evidence, final tool-product packaging, patch suggestion handling, reusable patchkit bundles and AI-to-AI handoff.

This README is a technical catalog. It is not the primary command source.

Primary operator entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
```

Code-driven navigation:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
```

## Current doctrine

```text
quick/balanced/deep/custom = intensity, not scope
GPU1/GPU0/NPU peer exchange is production evidence, not smoke-only proof
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
preferred active runbook/docs size <=400 lines; active Markdown hard threshold <=500 lines
maintained source/script target <=400 lines
limitations are backlog to overcome, not reasons to skip available tools
patch application is explicit and separate
tool output should become verifiable product/evidence/readiness material, not chat-only summary
patch notes are proposal ledgers until reviewed into a concrete patchkit bundle or branch diff
```

## Heap/exchange and patchkit boundary

The active model is:

```text
IN -> dynamic heap/exchange LOOP -> deterministic OUT
```

The heap/exchange center is the dynamic knowledge surface. GPU1, GPU0, NPU, provider lanes, official adapter, context/memory and broker evidence may cooperate through runtime routing and evidence quality. Do not model this center as a rigid static chain.

The boundary is deterministic:

```text
controlled task/context/capability entry
heap exchange runtime state and public events
exit product with concrete operation candidates
lifecycle validation
patchkit bundle/application or review PR product
```

Canonical docs and tools:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
Tools/ai/build_heap_exchange_runtime_entry.py
Tools/ai/build_heap_exchange_runtime_exit.py
Tools/validation/check_heap_exchange_runtime_lifecycle.py
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
Tools/ai/patchkit/apply_patch_bundle.py
Tools/validation/run_patchkit_smoke.py
```

## Owner boundaries

Do not create a new script when one of these already owns the responsibility.

| Responsibility | Owner |
|---|---|
| Provider orchestrator | `run_agent_gpu_npu_parallel_orchestrator.py` |
| GPU1/Ollama planner worker | `run_agent_gpu_deep_planning_supervised.py` |
| GPU0 peer worker | `run_gpu0_peer_companion_worker.py` |
| AI peer exchange packet | `build_ai_peer_exchange_packet.py` |
| Heap/exchange runtime entry | `build_heap_exchange_runtime_entry.py` |
| Heap/exchange runtime exit | `build_heap_exchange_runtime_exit.py` |
| Runtime tool execution | `agent_runtime_tool_broker.py` |
| Runtime tool telemetry | `build_runtime_tool_usage_telemetry.py` |
| Full toolbox telemetry summary | `build_full_toolbox_run_telemetry_summary.py` |
| Shared AI-to-AI bundle | `build_shared_toolbox_ai_to_ai_bundle.py` |
| GitHub compact evidence bundle | `build_github_evidence_bundle.py` |
| Task patch suggestion report | `build_task_patch_suggestion_report.py` |
| Deterministic patchkit application | `patchkit/apply_patch_bundle.py` |
| Patch suggestion dry-run/apply | `apply_patch_suggestion_bundle.py` and `patch_suggestion_bundle/cli.py` |
| Review PR preparation | `prepare_review_pr.py` |
| Context pack | `build_ai_context_pack.py` |
| Agent state packet | `build_agent_state_packet.py` |
| Semantic chunk selection | `select_semantic_code_chunks.py` |

Full owner map:

```text
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
```

## Package map

| Area | Role |
|---|---|
| `pipeline/` | Modular AI artifact pipeline implementation behind `run_parallel_artifact_pipeline.py`. |
| `patchkit/` | Reusable controlled patch-bundle runner, filesystem/anchor/PowerShell/report helpers and deterministic validators. |
| `patch_suggestion_bundle/` | Deterministic patch suggestion discovery, classification and apply implementation. |
| `patch_notes_quality_product/` | Manual-review patch-note product/ledger support. |
| `full_run_bundle_zip/` | Full-run evidence ZIP support in candidate foundation work. |
| `runtime_hardware_capability/` | Runtime hardware capability support in candidate foundation work. |

## Core tool groups

| Tool family | Examples | Notes |
|---|---|---|
| Context and chunks | `build_ai_context_pack.py`, `select_semantic_code_chunks.py` | Provider-free context evidence. |
| Agent state and memory | `build_agent_state_packet.py`, `review_agent_memory.py`, `agent_runtime_sqlite_memory.py` | SQLite outputs are local/private and must not be committed. |
| AI peer exchange | `build_ai_peer_exchange_packet.py`, `run_gpu0_peer_companion_worker.py`, `run_npu_gpu_deep_review_auditor.py` | GPU1 output to GPU0/NPU peer response and broker evidence. |
| Heap/exchange lifecycle | `build_heap_exchange_runtime_entry.py`, `build_heap_exchange_runtime_exit.py` | Dynamic center boundary: entry state, lane availability, public exchange events and deterministic exit product. |
| Workload routing | `build_workload_quality_lane_routing.py` | Keeps unusable provider output out of advisory context. |
| Deterministic recommendations | `build_deterministic_recommendations.py` | Supports degraded-provider recovery without hallucinated provider success. |
| Patch planning/spec support | `build_agent_review_patch_plan.py`, `build_patch_specs_from_proposals.py`, `promote_patch_spec_draft.py` | Review-only unless explicit apply is authorized separately. |
| Patchkit bundles | `patchkit/apply_patch_bundle.py`, `patchkit/*` | Preferred OOB application path for future core patch bundles. |
| Patch suggestion product | `build_task_patch_suggestion_report.py`, `apply_patch_suggestion_bundle.py`, `prepare_review_pr.py` | Markdown/task suggestion product, deterministic apply, review PR preparation. |
| Runtime broker/telemetry | `agent_runtime_tool_broker.py`, `build_runtime_tool_usage_telemetry.py` | Broker-measured tool calls and normalized status. |
| Capability and telemetry summary | capability manifest packages/builders, `build_full_toolbox_run_telemetry_summary.py` | Handoff context for available tools/hardware lanes and run state. |
| Production bundle | `build_shared_toolbox_ai_to_ai_bundle.py` | AI-to-AI evidence/telemetry/patch-plan handoff. |
| Evidence bundles | `build_github_evidence_bundle.py`, full-run bundle ZIP tools | Compact GitHub evidence only; raw `output/**` stays ignored. |

Use `docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md` to classify each family as active, report-only, provider-gated, manual-review, local-private, target or legacy/diagnostic.

## Patchkit bundle procedure

Future patch work should centralize only the modification core:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Apply it with:

```powershell
python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

python .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

Patchkit handles:

```text
backup
encoding/BOM preservation
newline preservation without Windows CRCRLF corruption
in-memory dry-run chain simulation
idempotency markers
PowerShell Invoke-Checked anchors
marker insertions
exact replacements
PowerShell parser validation
Python compile validation
git diff --check
JSON/Markdown reports
line count reporting
```

Supported initial operations:

```text
insert_after_invoke_checked
insert_before_marker
insert_after_marker
replace_once
append_once
assert_marker
assert_no_naked_throw
```

## Patch suggestion and review PR status

Current code is conservative:

```text
apply_patch_suggestion_bundle.py can dry-run or apply deterministic operations only when explicit --apply is supplied.
patchkit/apply_patch_bundle.py is preferred for new reviewed core patch bundles.
patch_suggestion_bundle/common.py owns the reusable operation model and report path normalization used by the final phase.
patch_suggestion_bundle/product.py exposes product/supplemental totals separately from capped published review-item lists.
prepare_review_pr.py requires explicit --include-path / launcher ReviewPrIncludePath.
prepare_review_pr.py can auto-discover include paths from apply reports with `--auto-include-from-apply-report` plus `--apply-report`.
prepare_review_pr.py does not create PRs as draft yet.
```

Use the final-phase runbook:

```text
docs/LOCAL_AI_TASKS/patch-suggestion-bundle-final-phase.md
```

## Proposal-core bundle rule

When `build_github_evidence_bundle.py` receives a `patch_notes_quality_product` report, the compact bundle must preserve the operational core under:

```text
summary.proposal_core
summary.proposal_core.notes[]
```

Patch notes are not patches. Convert only validated suggestions into a real patchkit bundle or branch diff.

## Final product behavior


```text
track input contract
accelerator control
provider governor
provider invocation plan
provider execution bridge
effective-use optimization summary
quality gate
```

It writes product Markdown, evidence index, readiness JSON, manifest and README.

## Full-run handoff rule

A recommendation, patch plan or patch spec produced from run-unica evidence is incomplete unless the handoff includes:

```text
launcher manifest
phase_status / phase_reports
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/index/discovery/file-line evidence when relevant
proposal_core when patch notes quality product is part of the run
heap/exchange entry, runtime state, public events and exit product when review PR product is requested
```

File existence alone is not proof of successful execution.

## Device strategy

```text
CPU: parsing, JSON generation, validation, orchestration.
GPU0/OpenVINO: companion peer worker and controlled tool-request producer for GPU1 follow-up.
NPU/OpenVINO: orchestrator-called micro-fast task assistant, guardrail and lightweight tool-support lane.
Deterministic scripts: heavy audit and validation authority.
External GPU commands: explicit heavy generator path only, never implicit.
```


## Safety policy

Tools in this folder should remain report-only or explicit-run by default.

They must not silently:

```text
apply patches
queue patch specs
edit Blender runtime files
edit full analysis JSON files
commit output/**
commit SQLite DB files
execute providers outside selected provider/full-run lanes
run Blender, FFmpeg, audio playback or media generation
convert patch notes directly into source writes without review
bypass agent_runtime_tool_broker.py for provider-requested tools
bypass prepare_review_pr.py for review PR staging/commit/push/create
bypass patchkit for long/delicate future patch bundles when patchkit operations can express the change
```

## Line-budget policy

Maintained tools and docs must stay within active line-budget policy.

```text
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Markdown >500 lines -> compact index + <file>.md/part-001.md layout.
Preferred active runbook size -> <=400 lines.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Validator:

```text
Tools/validation/check_file_line_limits.py
```

## Related docs

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/patch-suggestion-bundle-final-phase.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/DATA_FLOW.md
docs/MODULE_MAP.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

## Standalone heap universe tool owners

The standalone heap incubation lane is owned from `Tools/ai/`, not from the workflow wrapper.

Primary standalone path:

```text
Tools/ai/run_heap_runtime_context_closure.py
```

Tool surface map:

```text
docs/LOCAL_AI_TASKS/standalone-heap-universe-tool-surface-2026-05-10.md
```

Relevant owners:

| Surface | Owner |
|---|---|
| Strict startup launcher | `run_heap_runtime_context_closure.py` |
| Context/memory preload | `prepare_heap_context_memory_reload.py` |
| Required docs initialization | `ensure_ai_context_required_files.py` |
| Startup-to-heap reconciliation | `reconcile_heap_report_with_startup_reload.py` |
| Heap universe / provider loop | `run_heap_runtime_completeness_gate.py` |
| Final assembly | `compose_heap_final_proposals.py` |
| SQLite operational memory | `agent_runtime_sqlite_memory.py` |
| Tool catalog | `build_agent_agnostic_tool_inventory.py` |
| Runtime broker | `agent_runtime_tool_broker.py` |
| Operator product launcher | `operator_product_launcher.py`, `operator_product_launcher_core.py` |

Do not promote this lane into the full run until same-heap GPU1/GPU0/NPU participation, refinement artifacts and final package semantics are validator-backed.
