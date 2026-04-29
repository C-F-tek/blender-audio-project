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

Recovered ideas:

```text
robust model JSON parsing concept -> Tools/ai/model_json.py
validator primitive concept -> Tools/validation/generated_file_policy.py
Blender generated script policy -> Tools/validation/check_generated_blender_script_policy.py as first adapter
```

Still recoverable ideas:

```text
Tools/ai_core-style reusable primitives
artifact store concept
model client interface concept
AI adapters split between generic core, input-domain adapters and output-application adapters
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
existing Tools/ai/model_json.py
existing Tools/validation/generated_file_policy.py
possible Tools/ai_core/
possible Tools/ai_adapters/
possible Tools/ai/common/
```

Outcome required before code:

```text
reuse existing Tools/ai/pipeline only
create Tools/ai_core as lower-level generic library
or extract selected utilities into Tools/ai/common
```

The decision must explicitly separate:

```text
input-domain adapters
output-application adapters
generated Python script policy adapters
```

Risk: medium, because duplicate abstractions are likely.

### Follow-up B — JSON parser utility review

Status: absorbed.

Result:

```text
Tools/ai/model_json.py
Tools/validation/check_ai_model_json.py
Tools/npu/ollama_runtime.py delegates parse_json_response() to model_json
```

The old PR #19 `Tools/ai_core/json_utils.py` idea is considered recovered in a smaller, safer form.

### Follow-up C — generated Python script policy

Status: partially absorbed.

Recovered now:

```text
Tools/validation/generated_file_policy.py
Tools/validation/check_generated_blender_script_policy.py
```

Important architectural decision:

```text
The policy model is input-agnostic and output-application-agnostic.
Blender is only the first generated Python script adapter.
WAV/audio is only one possible input-domain family and must not be embedded in the generic policy layer.
```

Current Blender adapter checks:

```text
forbid ShaderNodeTexMusgrave
forbid unsafe open project operator
forbid quit Blender operator
require import bpy
warn on save_as_mainfile
warn on eval/exec
```

Deferred checks:

```text
require keyframe_insert only for animation-oriented generated scripts
require reference to full keyframes/frame data only for frame-data-driven generated scripts
restrict generated files to safe output prefixes only after implementation draft path policy is defined
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

### Follow-up F — non-Blender Python-scriptable app adapter

Create only after identifying a real target application/runtime.

The adapter should reuse:

```text
Tools/validation/generated_file_policy.py
```

It must not inherit Blender assumptions such as `bpy`, scenes, render settings or Blender file operations.

Risk: low if sample-only and isolated.

### Follow-up G — input-domain validator family

Create separately from output-application policy.

Potential future input domains:

```text
WAV/audio analysis artifacts
JSON scene specs
CSV/TSV datasets
images or image-sequence manifests
text/context bundles
application configuration files
```

Risk: medium if mixed with application-output validators. Keep boundaries explicit.

## Guardrails

- Do not reopen or rebase old PRs directly.
- Do not copy large old branches wholesale.
- Do not create `Tools/ai_core` until a decision document explains why it is not duplicating `Tools/ai/pipeline`, `Tools/ai/model_json` or `Tools/validation/generated_file_policy`.
- Do not touch runtime Blender packages from this cleanup.
- Do not change FFmpeg behavior.
- Do not change schema-v6 meanings while validating additive fields.
- Do not make generic generated-file policy Blender-only.
- Do not make generic generated-file policy WAV/audio-only.
- Keep input-domain validators separate from output-application validators.
- Every recovered idea must be its own small PR with local validation.

## Immediate priority

Validate documentation alignment and regenerate AI/NPU indexes.

Then choose the next lowest-risk recovery task.

## Progress log

- 2026-04-29: PR #10, #15 and #19 evaluated as stale/superseded. Useful ideas captured here as future micro-tasks.
- 2026-04-29: JSON model parser idea recovered through `Tools/ai/model_json.py` and `check_ai_model_json.py`.
- 2026-04-29: Generated policy idea recovered as an input-agnostic/application-agnostic policy engine with Blender as first Python-scriptable app adapter.
