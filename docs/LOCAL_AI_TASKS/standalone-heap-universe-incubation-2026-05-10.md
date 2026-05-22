# Standalone Heap Universe Incubation Lane — 2026-05-10

## Status

Design and operating note for the standalone heap runtime lane.

This lane is intentionally **separate from the full real-product run** while it is being tested and hardened. After it proves stable, it must be promoted into the full run-unica path as a first-class phase.

## Purpose

The standalone heap lane exists to test the project’s core operating theory without the noise of the full product wrapper:

```text
single strict input
  -> context/memory/tool preload
  -> heap universe / blackboard
  -> GPU1/GPU0/NPU/broker/memory/validators cooperate
  -> iterative refinement inside the heap
  -> single composed output from heap state
```

It is not a replacement for `Tools/workflow/run_unified_real_product_pr.ps1`. It is the incubation path for the heap universe behavior that will later be wired into that full product path.

## Current owner path

```text
ia_carmine/runtime/heap_context_closure/cli.py
```

Related helper/tooling surface:

```text
ia_carmine/context/heap_context_memory_reload/cli.py
ia_carmine/ensure_ai_context_required_files.py
ia_carmine/reconcile_heap_report_with_startup_reload.py
ia_carmine/runtime/heap_runtime/completeness_gate/cli.py
ia_carmine/product/heap_final_proposals/cli.py
```

## Strict input

The standalone lane starts from one operator request plus explicit runtime flags.

The launcher must build a deterministic startup task file containing references to the preloaded context artifacts:

```text
required context files report
repo docs map
semantic code chunks
tool catalog
shared memory inventory
operational memory status/search
transient request context
AI context pack
semantic evidence chunks
startup manifest
```

The heap must not rely on hidden prompt state. It must receive artifact paths and compact summaries.

## Tool-owned preload

Before the heap starts, the following context/memory/tool state must be loaded or explicitly classified degraded:

```text
required docs
repo docs
semantic code chunks
tool catalog
shared memory
SQLite/operational memory write/search
transient request context
AI context pack
semantic evidence chunks
```

Desired startup state:

```text
preflight_passed=true
startup_reload_passed=true
startup_reload_degraded=false
startup_blocking_requirements=[]
startup_degraded_requirements=[]
input_ready_before_heap=true
```

If startup context is partially degraded but useful, the degradation must be represented as heap facts, not hidden in stdout.

## Heap universe contract

The heap universe is the active blackboard. It must collect and expose:

```text
facts
constraints
context artifact refs
tool outputs
memory hits
provider lane reports
GPU0 review/refinement signals
NPU micro-audit signals
validator results
proposal revisions
accepted/rejected blocks
rejection reasons
refinement tasks
action list
```

The central rule is:

```text
the heap decides whether to refine;
the composer only assembles final state.
```

## Multi-lane loop

The lane must avoid a one-direction flow where GPU1 writes and the rest only decorates.

Correct loop:

```text
revision N:
  GPU1 proposes
  GPU0 reviews/refines
  NPU audits
  broker/tool results are attached
  CPU validators classify
  heap arbiter decides:
    accepted
    rejected_with_reason
    refinement_required
```

If a proposal is rejected, the heap writes a refinement artifact for the next revision.

Expected proposal artifacts:

```text
team_context/proposal_iterations/heap_proposal_revision_000.json
team_context/proposal_iterations/heap_proposal_revision_000.md
team_context/proposal_iterations/heap_parallel_cycle_000.json
team_context/proposal_iterations/heap_refinement_task_after_revision_000.json
```

## Output larger than model context

The heap lane must support output larger than one model context window.

Policy:

```text
long output -> artifact/chunk files
next revision context -> compact summary + artifact paths
final composition -> assembled from heap state and artifact references
```

Do not force GPU1/GPU0/NPU to hold the whole product in one context window.

## Standalone success criteria

A standalone heap run is successful only when:

```text
startup_reload_degraded=false
provider_execution_performed=true when provider mode is requested
missing_requirements=[]
GPU1/GPU0/NPU participation is visible when provider mode is requested
proposal acceptance respects GPU0/NPU/validator vetoes
composer package is exported
accepted/rejected reasons are visible
output package exists under Documents/aicarmine_heap_final_proposals_<stamp>/
```

A packaged blocked result is valid when it clearly says why no acceptable proposal exists.

## Promotion criteria into full run

Do not wire this lane as mandatory full-run behavior until these are stable:

```text
startup preload is deterministic
same-heap GPU1/GPU0/NPU cycle is observable
refinement task artifacts are consumed by later revisions
composer assembles without acting as primary arbiter
package exports on both success and failure
validators distinguish false positives from accepted products
line counts and docs remain within policy
```

Once stable, the full run should consume this lane as:

```text
run_unified_real_product_pr.ps1
  -> mandatory preflight
  -> existing run-unica phases
  -> standalone heap universe lane promoted into selected phase
  -> generated patch specs / review product
  -> final contract
```

## Current relation to run-unica

Current state:

```text
standalone heap lane = incubation / robustness path
run-unica = product path
```

Target state:

```text
standalone heap lane proven robust
  -> promoted into run-unica as first-class selected phase
  -> full product path keeps same strict IN and deterministic OUT
```

## Guardrails

The standalone heap lane must not:

```text
apply patches automatically
commit output/**
commit *.db or *.sqlite
pretend placeholder/stub/TODO output is accepted
treat diagnostic provider workload as semantic success
bypass preflight
move final arbitration into composer
```

## Tool surface companion

Detailed tool and memory surface map:

```text
docs/LOCAL_AI_TASKS/standalone-heap-universe-tool-surface-2026-05-10.md
```

Use it to verify that SQLite/FTS5, markdown chunks, semantic chunks, context namespace, tool catalog, broker outputs, provider reports and validators are represented as heap facts rather than side logs.
