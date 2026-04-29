# Superseded PR Follow-ups

## Status

active

## Goal

Preserve useful ideas from old divergent pull requests without merging stale branches into the current `master`.

The old PRs are treated as historical design input, not as merge candidates.

## Source PRs

```text
PR #10 — Fix Scene Director empty replies and add NPU runtime tracing
PR #15 — Add smart AI context packets and NPU guardrail lane
PR #19 — Add reusable AI pipeline core
```

## Current decision

The PRs should remain closed/unmerged because they are behind the current repository state and overlap with newer architecture.

Reasons:

```text
large divergence from master
older schema/report versions
overlap with Tools/ai/pipeline modularization
overlap with smart context and NPU guardrail already merged
overlap with agent_state and validator work
risk of duplicate architecture or regression
```

## What is already absorbed

### From PR #15

Already absorbed by current architecture:

```text
Tools/workflow/smart_ai_context.py
Tools/npu/npu_guardrail_service.py
AI pipeline smart context stage
NPU guardrail lane
schema-v6 pipeline report
run_pipeline_dry_run_matrix.py
```

No direct follow-up needed unless GUI integration requires a fresh review.

### From PR #10

Partially superseded. Useful ideas remain as possible future tasks:

```text
Scene Director deterministic fallback for empty model replies
Scene Director runtime events
NPU diagnostics visibility even when heavy NPU work is skipped
ai_runtime_diagnostics NPU section
```

These should be reintroduced only after reading current files, not by merging the old PR.

### From PR #19

Contains useful architectural ideas but should not be merged directly.

Recoverable ideas:

```text
Tools/ai_core-style reusable primitives
artifact store concept
model client interface concept
robust model JSON parsing concept
validator primitive concept
AI adapters split between generic core, audio and Blender
Blender generated script policy
implementation draft validator bridge
aggregated smoke-test runner concept
rollback/checklist docs
```

These must be split into new small execution plans and PRs.

## Follow-up backlog

### Follow-up A — generic core decision record

Create a short design decision document comparing:

```text
existing Tools/ai/pipeline/
existing Tools/ai/agent_state.py
proposed Tools/ai_core/
proposed Tools/ai_adapters/
```

Outcome required before code:

```text
reuse existing Tools/ai/pipeline only
or create Tools/ai_core as lower-level generic library
or extract selected utilities into Tools/ai/common
```

Risk: medium, because duplicate abstractions are likely.

### Follow-up B — JSON parser utility review

Review whether a reusable robust JSON parser is still missing.

Candidate source idea from PR #19:

```text
Tools/ai_core/json_utils.py
```

Current target must be decided after checking existing parsing helpers.

Risk: low if additive and tested.

### Follow-up C — generated Blender script policy

Recover the policy idea only if current validators do not already cover it.

Candidate checks:

```text
forbid ShaderNodeTexMusgrave
forbid unsafe open/save project operators
require import bpy
require keyframe_insert
require reference to full keyframes/frame data
restrict generated files to safe output prefixes
```

Risk: low/medium. Do not block legitimate generated scripts too early.

### Follow-up D — Scene Director empty-response diagnostics

Review current `Tools/workflow/scene_brief.py` and `Tools/workflow/ai_runtime_diagnostics.py`.

Recover only missing behavior:

```text
empty model reply logging
safe deterministic fallback
NPU preflight visibility when heavy pass is skipped
runtime trace JSONL
```

Risk: medium. Must avoid adding stale assumptions or noisy logs.

### Follow-up E — aggregated smoke runner

Review existing validation runner before creating another smoke-test system.

Current likely preferred target:

```text
Tools/workflow/run_local_validation_after_refactor.ps1
Tools/validation/*.py
```

Recover only the concept of a single summary report if not already covered.

Risk: low if wrapper-only.

## Guardrails

- Do not reopen or rebase old PRs directly.
- Do not copy large old branches wholesale.
- Do not create `Tools/ai_core` until a decision document explains why it is not duplicating `Tools/ai/pipeline`.
- Do not touch runtime Blender packages from this cleanup.
- Do not change FFmpeg behavior.
- Do not change schema-v6 meanings while validating additive fields.
- Every recovered idea must be its own small PR with local validation.

## Immediate priority

Finish the already-started `TD-006` micro-task:

```text
validate agent_state_packet report contract
```

Then review this follow-up backlog and choose the next lowest-risk recovery task.

## Progress log

- 2026-04-29: PR #10, #15 and #19 evaluated as stale/superseded. Useful ideas captured here as future micro-tasks.
