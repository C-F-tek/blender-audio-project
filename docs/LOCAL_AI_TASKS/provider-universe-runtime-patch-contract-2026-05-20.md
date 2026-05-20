# Provider Universe Runtime Patch Contract - 2026-05-20

## Status

Active Markdown task contract.

This document converts the updated Deep Research reports and the current
Universo IA model docs into a compact implementation target. It is not runtime
evidence and it does not claim that a full provider run now passes.

## Sources Read

Current repository contracts and model docs:

```text
AGENTS.md
CHATGPT.md
CONTEXT_INDEX.md
docs/AI_DOCS_ENTRYPOINT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/CONTEXT_COVERAGE_STATUS.md
docs/DISPATCHER_CONTEXT_COVERAGE.md
Tools/CONTEXT_INDEX.md
```

External operator-supplied reports:

```text
C:\Users\carmi\Downloads\deep-research-report.md
C:\Users\carmi\Downloads\deep-research-report 2.md
```

## Current Corrected Facts

These should not be reopened as missing unless current source proves a
regression:

- PR301/local master is no longer only a small launcher patch; it became a broad
  tool-surface and canonical-run refactor.
- The code product intake path already recognizes no-worktree-diff integrated
  states in the current source described by Deep Research 2.
- False native tool calls salvaged from malformed OpenVINO text are already
  treated as non-operational in the current source described by Deep Research 2.
- GPU1 is intended to be text-first: it should produce advisory/proposal text,
  not only native tool calls.
- Provider prose remains evidence. It is not a product without concrete
  operations, target files and validation.

## Runtime Failure Still To Solve

The observed failure pattern remains:

```text
provider lanes active
broker/event counters grow
provider_blocks = 0
proposals = 0
GPU1 process alive or partial
GPU0/NPU degraded or diagnostic
CPU rises
operator interrupts
CODE_PRODUCT_FULL_PATCH missing
```

That is a product failure, not a console formatting issue.

## Provider Universe Rule

Selected provider lanes must not be hidden behind vague degraded status.

The implementation must distinguish these states explicitly:

```text
operational_provider_activity = useful provider contribution
diagnostic_only = report exists but cannot satisfy provider/product readiness
nonproductive_stall = selected provider universe is alive but not producing blocks
blocked_with_reason = deterministic safe stop
```

The unresolved design point must be made explicit in code and docs:

```text
same-universe strict mode:
  a selected lane that fails or becomes non-operational blocks the provider run

diagnostic-enrichment mode:
  GPU0/NPU can publish diagnostic-only evidence, but cannot satisfy product
  readiness and cannot be presented as three-lane success
```

No path may silently fall back from strict universe behavior to diagnostic
enrichment.

## Patch Target 1: Provider Activity Contract

Update the provider activity gate so it is lane-aware and product-aware.

Required semantics:

- GPU1 is operational when it has selected model evidence and useful proposal
  text, or selected model evidence and a structured allowlisted native tool
  call.
- GPU0 is operational only when it produces peer review/refinement evidence,
  contradiction evidence, useful semantic OpenVINO output or a structured
  allowlisted native tool call.
- NPU is operational only when it produces micro-audit evidence, guardrail
  evidence, useful semantic output or a structured allowlisted native tool call.
- Device visibility, workload-only output, empty text, timeout classification or
  salvaged malformed tool text are diagnostic only.

Likely source families:

```text
Tools/ai/heap_gate/provider_block_contract.py
Tools/ai/heap_gate/provider_report_absorption.py
Tools/ai/heap_gate/tool_broker_native_calls.py
Tools/ai/_shared/provider_tool_loop.py
Tools/ai/_shared/provider_ollama_probe.py
```

## Patch Target 2: Stop Nonproductive GPU1 Stall

GPU1 must not be treated as useful only because a PID is alive.

Add a deterministic watchdog for this condition:

```text
gpu1_planner running
broker request/result counts stable for threshold
provider_blocks = 0
proposals = 0
GPU0/NPU already failed, degraded or diagnostic-only
no partial checkpoint promoted to provider/proposal evidence
```

Expected exit:

```text
blocked_with_reason
reason = gpu1_nonproductive_runtime_stall
terminate remaining provider processes for this run
publish validation_signal / decision evidence
```

Likely source families:

```text
Tools/ai/heap_gate/run_loop.py
Tools/ai/heap_gate/provider_process_collection.py
Tools/ai/heap_gate/provider_universe_abort.py
```

## Patch Target 3: GPU1 Partial Checkpoint Or Streaming

Deep Research 2 identifies the current GPU1 Ollama call as monolithic:

```text
session.generate(... stream=False)
session.chat(... stream=False)
```

The runtime needs one of these:

```text
streaming provider output
partial checkpoint writer
periodic partial response JSON/Markdown
early proposal block when text crosses a valid threshold
```

The purpose is not cosmetics. The purpose is to make the primary provider lane
observable before the whole response finishes.

Likely source families:

```text
Tools/npu/provider_mesh/ollama_runtime_core/session.py
Tools/ai/_shared/provider_ollama_probe.py
Tools/ai/provider_mesh/
Tools/ai/heap_gate/provider_report_absorption.py
```

## Patch Target 4: Heap Index Sidecar

The current heap JSONL/event model is audit-friendly but weak for live query and
diagnostics. Add a local SQLite sidecar index without replacing JSONL.

Required design:

```text
JSONL remains audit trail
SQLite sidecar is run-local and not committed
append_event writes JSONL and updates sidecar
interrupt cleanup can still inspect latest materialized state
```

Candidate tables:

```text
events
pending_broker_requests
provider_reports
lane_status_materialized
latest_event_by_type
proposal_iterations
decisions
```

Likely source families:

```text
Tools/ai/provider_runtime_blackboard/
Tools/ai/heap_runtime/
Tools/ai/runtime_tool/
Tools/ai/agent_memory/
```

## Patch Target 5: Startup Context Must Stay Addressable

Large runtime-generated Markdown, semantic chunk dumps and startup context
material must not become live prompt ballast.

Expected behavior:

```text
large generated context -> local artifact refs
SQLite/FTS/chunk index -> searchable facts
provider prompt -> bounded excerpts plus refs
broker retrieval -> detail on demand
```

Do not commit raw runtime chunk output. Do not replace heap memory with a giant
Markdown prompt.

## Tests To Add Or Preserve

Provider/native call tests:

```text
salvaged OpenVINO text does not increment native_tool_call_count
salvaged OpenVINO text does not publish broker tool calls
structured allowlisted native call can count when complete
```

Provider activity tests:

```text
GPU1 selected model + useful text => operational
GPU1 selected model + structured native call => operational
GPU0/NPU workload-only or timeout => diagnostic_only
diagnostic_only does not publish provider_peer_block
strict selected universe blocks when a required lane is non-operational
diagnostic enrichment mode does not claim three-lane success
```

Runtime stall tests:

```text
gpu1 running + no provider blocks + no proposals + peer lanes degraded
=> gpu1_nonproductive_runtime_stall
=> blocked_with_reason
=> live provider processes terminated for this run
```

Code product tests:

```text
already_integrated_no_worktree_diff remains accepted
verified_target_no_worktree_diff remains compatible if historical artifacts use it
metadata-only patch specs remain non-product
```

Suggested validator names if new commands are added:

```text
run_heap_provider_operational_gate_smoke
run_gpu1_nonproductive_stall_smoke
run_runtime_heap_sqlite_sidecar_smoke
```

## CI Direction

Use existing dispatcher-owned validation surfaces. Do not add a parallel test
runner.

Suggested grouping:

```text
python -m Tools.validation run_provider_tool_loop_smoke
python -m Tools.validation run_code_product_artifact_intake_smoke
python -m Tools.validation run_heap_startup_context_ingestion_smoke
python -m Tools.validation run_heap_runtime_launcher_command_smoke
python -m Tools.validation run_operator_product_launcher_smoke
python -m Tools.validation run_observable_peer_activity_contract_smoke
```

Add the new provider-gate and GPU1-stall smokes only after the source behavior
exists.

## Guardrails

- Do not launch full provider/runtime runs from this Markdown pass.
- Do not commit `output/**`, SQLite files, raw chunk directories or provider raw
  logs.
- Do not call diagnostic-only evidence a product.
- Do not call a selected lane useful because a process exists.
- Do not claim GPU0/NPU are full compute providers unless source and validators
  prove it.
- Do not implement a new universe outside dispatcher-owned tools.

## Next Action

Open the listed source families and convert this contract into the smallest
code/test patch sequence:

```text
1. provider activity contract
2. nonproductive GPU1 stall stop
3. GPU1 partial checkpoint or streaming
4. SQLite sidecar heap index
5. startup context ref/excerpt discipline
```
