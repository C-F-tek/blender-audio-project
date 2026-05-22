# Standalone Heap Universe Tool Surface — 2026-05-10

## Status

Companion document for the standalone heap universe incubation lane.

Primary design document:

```text
docs/LOCAL_AI_TASKS/standalone-heap-universe-incubation-2026-05-10.md
```

This file maps the tool and memory surfaces that the standalone heap lane must expose before it is promoted into the full run-unica path.

## Purpose

The standalone heap lane must not be a prompt-only experiment.

It must prove that the heap universe can operate on deterministic, inspectable surfaces:

```text
tool catalog
SQLite / operational memory
SQLite FTS5 search
markdown chunk memory
semantic code chunks
semantic evidence chunks
context namespace
AI context pack
transient request context
broker/tool execution
provider lane reports
validator evidence
final composer package
```

## Current owner scripts

| Responsibility | Owner |
|---|---|
| Standalone launcher / single strict input | `ia_carmine/runtime/heap_context_closure/cli.py` |
| Startup context/memory/tool preload | `ia_carmine/context/heap_context_memory_reload/cli.py` |
| Required docs initialization | `ia_carmine/ensure_ai_context_required_files.py` |
| Startup preload -> heap report reconciliation | `ia_carmine/reconcile_heap_report_with_startup_reload.py` |
| Heap universe / completeness / provider loop | `ia_carmine/runtime/heap_runtime/completeness_gate/cli.py` |
| Final package assembly | `ia_carmine/product/heap_final_proposals/cli.py` |
| Context pack | `ia_carmine/context/agent_context/ai_context_pack/cli.py` |
| Tool catalog | `ia_carmine/context/agent_context/agnostic_tool_inventory/cli.py` |
| Memory inventory | `ia_carmine/context/agent_context/memory_inventory/cli.py` |
| Transient request context | `ia_carmine/context/agent_context/transient_request_context/cli.py` |
| Operational SQLite memory | `python -m ia_carmine.cli agent_runtime_sqlite_memory` |
| Runtime broker | `ia_carmine/runtime/runtime_tool/agent_broker.py` |

## Preload surfaces

The standalone launcher should start heap execution only after a structured preload phase has produced artifact references.

Required preload surface:

```text
required_context_files_json
repo_docs_map_json
semantic_code_chunks_json
tool_catalog_json
shared_memory_json
operational_memory_status_json
operational_memory_search_json
shared_context_json
ai_context_pack_json
ai_context_pack_evidence_json
semantic_evidence_chunks_json
heap_task_file
```

Those artifacts become heap facts. They are not side logs.

## SQLite / FTS5 / operational memory

SQLite-backed memory is the persistent runtime surface for cross-run state and compact retrieval.

Expected behavior:

```text
memory write records current task/run facts
memory search retrieves previous facts and decisions
FTS5 search supports keyword retrieval
JSON reports expose what was written/searched
SQLite files remain local/private and are never committed
```

The heap should consume memory through artifact refs and compact summaries, not by assuming hidden model memory.

## Markdown chunk memory

Markdown and repository documentation should be represented as chunkable, addressable context.

Expected behavior:

```text
large docs -> chunks
chunks -> manifest
manifest -> startup task file
heap revisions -> consume compact chunk refs
composer -> cite/assemble from accepted heap states
```

This is the mechanism that lets output and context exceed a single model window.

## Context namespace

The heap should distinguish namespaces instead of flattening everything into one prompt.

Initial namespace model:

```text
operator_request
startup_preload
repo_docs
semantic_code
semantic_evidence
shared_memory
operational_memory
tool_catalog
provider_reports
proposal_iterations
refinement_tasks
validators
composer_package
```

A future hardening step should make namespace records explicit in JSON schema and validators.

## Hybrid search

Hybrid search is a target surface, not a required success condition for the first standalone lane.

Promotion expectation:

```text
BM25/FTS5 signal
vector/embedding signal when available
rerank or deterministic scoring when available
source artifact refs preserved
no hallucinated source refs
```

Until it is wired deterministically, the standalone heap lane may rely on semantic chunks + SQLite/FTS5 + explicit artifact manifests.

## Tool catalog and broker

The heap must know which tools exist before it asks providers to plan work.

Tool catalog contract:

```text
available tools
tool roles
input/output expectations
safe/unsafe classification
provider-execution flags
patch/source-write flags
artifact paths
```

Broker contract:

```text
provider-requested tools execute through controlled broker paths
outputs become heap events/artifacts
tool failures become heap facts
provider text alone is not a tool execution proof
```

## Provider lanes

Provider outputs must become structured heap facts.

Minimum lane surfaces:

```text
gpu1_provider_planner
gpu0_provider_peer
npu_micro_task_auditor
```

Acceptance requires same-heap evidence that the lanes participated when provider mode is enabled.

## Refinement loop

The standalone heap must produce refinement artifacts when a proposal is rejected.

Required artifact families:

```text
heap_proposal_revision_XXX.json/md
heap_parallel_cycle_XXX.json/md
heap_refinement_task_after_revision_XXX.json/md
```

A rejected proposal is useful when it produces a precise next-revision task.

## Composer boundary

Composer reads heap state and writes a single export package.

It must not be the primary judge of a proposal. It assembles:

```text
accepted proposals
rejected proposals
rejection reasons
GPU0 review
NPU audit
provider reports
preload manifest
parallel cycle reports
refinement tasks
action list
download manifest
```

## Promotion checklist

Before promoting the standalone heap lane into run-unica, verify:

```text
preload artifacts complete and non-degraded
SQLite/operational memory reports useful
tool catalog loaded before provider planning
semantic chunks and context pack visible in heap_task_file
GPU1/GPU0/NPU same-heap cycle visible
refinement task generated on veto
later revision consumes refinement artifact
composer package exported on success and blocked states
no source writes without explicit patchkit/review path
```
