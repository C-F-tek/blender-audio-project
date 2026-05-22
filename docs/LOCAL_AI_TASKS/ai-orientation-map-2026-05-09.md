# AI Orientation Map — 2026-05-09

## Status

Historical orientation map.

This document captured the repository state around the heap/exchange lifecycle and patchkit work. It remains useful for conceptual background, but it is no longer the current first-read or tool-family map.

Current first-read sources:

```text
AGENTS.md
CHATGPT.md
CONTEXT_INDEX.md
docs/AI_DOCS_ENTRYPOINT.md
docs/CONTEXT_COVERAGE_STATUS.md
docs/DISPATCHER_CONTEXT_COVERAGE.md
Tools/CONTEXT_INDEX.md
Scripting/CONTEXT_INDEX.md
```

Before changing code, open the nearest current `TOOL_CONTEXT.md` from the area/family index and inspect the dispatcher/source file.

## Purpose

Compact historical orientation map for an AI agent entering the repository after the heap/exchange lifecycle and patchkit merges.

This is not a replacement for source inspection, context indexes or dispatcher coverage.

## One-sentence model

IA-Carmine is a code-driven local-AI orchestration workbench where a controlled task enters a dynamic heap/exchange, runtime lanes cooperate through evidence and public events, and the final source-change product exits through deterministic validators, patchkit/code-product boundaries and review paths.

## Historical baseline

```text
Historical baseline: master after PR #250
Runtime lifecycle: PR #249
Reusable patch boundary: PR #250
Historical doc PR: #251
```

Use this baseline as history, not current branch truth.

## Current navigation replacement

The old first-read path has been superseded by:

```text
CONTEXT_INDEX.md
-> docs/CONTEXT_COVERAGE_STATUS.md
-> docs/DISPATCHER_CONTEXT_COVERAGE.md
-> Tools/CONTEXT_INDEX.md
-> Tools/<area>/CONTEXT_INDEX.md
-> nearest TOOL_CONTEXT.md
-> dispatch.py/source file
```

## Historical mental model

```text
IN
  task Markdown
  stamp/run identity
  RepoPy gate
  inventories
  context pack
  agent state
  workload/capability evidence

LOOP / HEAP / EXCHANGE
  GPU1 / provider planner lane
  GPU0 / OpenVINO companion lane
  NPU / diagnostic microtask lane
  official adapter lane
  context/memory lane
  broker/tool evidence lane
  public exchange event stream

OUT
  heap exchange exit product
  concrete deterministic operation candidates
  lifecycle validator
  patchkit bundle or patch suggestion bridge
  review PR product
```

Entry and exit are controlled. The center is dynamic.

Do not reduce heap/exchange to a static chain. The run must provide context, evidence and lane registration; then the dynamic center may route/cooperate. The exit must still produce deterministic, reviewable product.

## Current owner-map rule

Do not use this historical document as the current owner map. Use:

```text
Tools/CONTEXT_INDEX.md
ia_carmine/CONTEXT_INDEX.md
Tools/validation/CONTEXT_INDEX.md
Tools/workflow/CONTEXT_INDEX.md
Tools/npu/CONTEXT_INDEX.md
docs/DISPATCHER_CONTEXT_COVERAGE.md
```

Then inspect the relevant `dispatch.py` file.

## Source-write rule

Preferred future source modification flow remains reviewed and evidence-driven:

```text
read target source
write compact patch/code product
run dry validation when available
run validators
inspect line counts
commit only intended files
```

Do not create a new one-off patcher if existing code-product, patchkit or repo-patch-runner paths can express the change.

## Run product classification

A full run may produce evidence but still fail as a product gate.

Valid successful product path:

```text
entry exists
runtime lanes available
runtime state events emitted
public exchange events emitted
exit product exists
concrete_operation_count > 0 when review product is requested
patch/code product produces deterministic product
review product is created
```

Valid blocked state:

```text
entry/lane/public events are good
exit product has no concrete deterministic operation candidate
review product must not pretend success
```

Metadata-only patch drafts are not enough.

## Validation routing

Use the current validation family index first:

```text
Tools/validation/CONTEXT_INDEX.md
```

Then run the specific dispatcher command from:

```text
Tools/validation/dispatch.py
```

Do not rely on old file-path invocation examples without checking the dispatcher.

## Guardrails

Never treat architecture docs as authorization to:

```text
merge without operator command
force-push
rewrite history
delete source
change secrets/permissions/billing/visibility
run Blender runtime
run FFmpeg runtime
commit output/**
commit indexAI/code_chunks/**
commit *.db / *.sqlite / renders/**
```

## What an AI should do when unsure

```text
1. Read CONTEXT_INDEX.md.
2. Read docs/CONTEXT_COVERAGE_STATUS.md.
3. Read docs/DISPATCHER_CONTEXT_COVERAGE.md.
4. Open the nearest current TOOL_CONTEXT.md.
5. Inspect dispatcher and source files.
6. Prefer existing validators and reviewed product paths.
7. Produce evidence, not confidence language.
8. Mark stale/obsolete docs as historical instead of following them blindly.
9. Stop if the run exits without concrete deterministic product.
```