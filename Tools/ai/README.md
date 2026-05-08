# AI Tools

`Tools/ai/` contains report-oriented tools for IA-Carmine local AI orchestration, context building, provider diagnostics, deterministic recommendations, telemetry, evidence, final tool-product packaging, patch suggestion handling and AI-to-AI handoff.

This README is a technical catalog. It is not the primary command source.

Primary operator entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Code-driven navigation:

```text
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
```

## Current doctrine

```text
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
provider/probe/workload-quality lanes are opt-out in Full0To10
GPU1/GPU0/NPU peer exchange is production evidence, not smoke-only proof
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
preferred active runbook/docs size <=400 lines; active Markdown hard threshold <=500 lines
maintained source/script target <=400 lines
limitations are backlog to overcome, not reasons to skip available tools
patch application is explicit and separate
tool output should become verifiable product/evidence/readiness material, not chat-only summary
patch notes are proposal ledgers until reviewed into a concrete patch bundle or branch diff
```

## Owner boundaries

Do not create a new script when one of these already owns the responsibility.

| Responsibility | Owner |
|---|---|
| Provider orchestrator | `run_agent_gpu_npu_parallel_orchestrator.py` |
| GPU1/Ollama planner worker | `run_agent_gpu_deep_planning_supervised.py` |
| GPU0 peer worker | `run_gpu0_peer_companion_worker.py` |
| AI peer exchange packet | `build_ai_peer_exchange_packet.py` |
| Runtime tool execution | `agent_runtime_tool_broker.py` |
| Runtime tool telemetry | `build_runtime_tool_usage_telemetry.py` |
| Full toolbox telemetry summary | `build_full_toolbox_run_telemetry_summary.py` |
| Shared AI-to-AI bundle | `build_shared_toolbox_ai_to_ai_bundle.py` |
| GitHub compact evidence bundle | `build_github_evidence_bundle.py` |
| Task patch suggestion report | `build_task_patch_suggestion_report.py` |
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
| `patch_suggestion_bundle/` | Deterministic patch suggestion discovery, classification and apply implementation. |
| `patch_notes_quality_product/` | Manual-review patch-note product/ledger support. |
| `full0to10_final_product/` | Final tool-product package builder: product Markdown, evidence index, readiness, manifest and README. |
| `full0to10_hardware_capability/` | Full0To10 hardware/capability visibility package. |
| `full_run_bundle_zip/` | Full-run evidence ZIP support in candidate foundation work. |
| `runtime_hardware_capability/` | Runtime hardware capability support in candidate foundation work. |

## Core tool groups

| Tool family | Examples | Notes |
|---|---|---|
| Context and chunks | `build_ai_context_pack.py`, `select_semantic_code_chunks.py` | Provider-free context evidence. |
| Agent state and memory | `build_agent_state_packet.py`, `review_agent_memory.py`, `agent_runtime_sqlite_memory.py` | SQLite outputs are local/private and must not be committed. |
| Provider diagnostics | `run_local_provider_probe.py`, `check_local_resource_lanes.py`, `analyze_gpu_npu_run_sync.py` | Provider state must flow to telemetry/bundle when used in Full0To10 handoff. |
| AI peer exchange | `build_ai_peer_exchange_packet.py`, `run_gpu0_peer_companion_worker.py`, `run_npu_gpu_deep_review_auditor.py` | GPU1 output to GPU0/NPU peer response and broker evidence. |
| Workload routing | `build_workload_quality_lane_routing.py` | Keeps unusable provider output out of advisory context. |
| Deterministic recommendations | `build_deterministic_recommendations.py` | Supports degraded-provider recovery without hallucinated provider success. |
| Patch planning/spec support | `build_agent_review_patch_plan.py`, `build_patch_specs_from_proposals.py`, `promote_patch_spec_draft.py` | Review-only unless explicit apply is authorized separately. |
| Patch suggestion product | `build_task_patch_suggestion_report.py`, `apply_patch_suggestion_bundle.py`, `prepare_review_pr.py` | Markdown/task suggestion product, deterministic apply, review PR preparation. |
| Runtime broker/telemetry | `agent_runtime_tool_broker.py`, `build_runtime_tool_usage_telemetry.py` | Broker-measured tool calls and normalized status. |
| Capability and telemetry summary | capability manifest packages/builders, `build_full_toolbox_run_telemetry_summary.py` | Handoff context for available tools/hardware lanes and run state. |
| Final tool product | `build_full0to10_final_tool_product.py`, `full0to10_final_product/*` | Product/evidence/readiness outputs from Full0To10 surfaces. |
| Production bundle | `build_shared_toolbox_ai_to_ai_bundle.py` | AI-to-AI evidence/telemetry/patch-plan handoff. |
| Evidence bundles | `build_github_evidence_bundle.py`, full-run bundle ZIP tools | Compact GitHub evidence only; raw `output/**` stays ignored. |

## Patch suggestion and review PR status

Current code is conservative:

```text
apply_patch_suggestion_bundle.py can dry-run or apply deterministic operations only when explicit --apply is supplied.
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

Patch notes are not patches. Convert only validated suggestions into a real patch bundle or branch diff.

## Final product behavior

The Full0To10 final-product builder composes these internal evidence families:

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
```

File existence alone is not proof of successful execution.

## Device strategy

```text
CPU: parsing, JSON generation, validation, orchestration.
GPU1/Ollama/RTX 5080: mandatory primary advisory planner/worker when Full0To10 provider execution is selected.
GPU0/OpenVINO: companion peer worker and controlled tool-request producer for GPU1 follow-up.
NPU/OpenVINO: orchestrator-called micro-fast task assistant, guardrail and lightweight tool-support lane.
Deterministic scripts: heavy audit and validation authority.
External GPU commands: explicit heavy generator path only, never implicit.
```

Full0To10 provider mesh runs use startup and close barriers. The legacy NPU auditor provider is diagnostics-only behind `-RunLegacyNpuAuditorProvider`.

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
