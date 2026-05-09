# AI Reference Onboarding

## Status

Current external-reference onboarding map.

This is reference onboarding only. It is not the primary operator entrypoint and not a command catalog.

Read current local orientation first:

```text
docs/AI_ONBOARDING.md
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

## Purpose

This document explains how external AI, NPU, validation and agent-engineering references map into this repository.

Primary onboarding and current maps:

```text
docs/AI_ONBOARDING.md
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Current doctrine

External concepts must be mapped to the current IA-Carmine operating model:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
telemetry accompanies evidence and patch plans for completeness
heap/exchange center is dynamic; entry and exit are controlled
patchkit is the preferred deterministic source-write boundary for reviewed bundles
monolithic/historical runbooks stay out of the primary path
```

## Main runtime architecture mapping

External references must be adapted to this target runtime model:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Canonical local contract:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Mapping rules:

```text
agent memory/context -> blackboard summaries and retention policy
model/router/planner concepts -> GPU1 advisory/planner or GPU0 helper lanes
small local inference/probe concepts -> NPU microtask responder only when validated
function/tool calling concepts -> broker unico executor plus semantic tools registry
schema/eval/guardrail concepts -> deterministic validators / CPU authority
observability concepts -> telemetry/event stream and compact evidence
controlled dynamic-runtime concepts -> heap/exchange entry, runtime state, public events and exit product
source-write bundle concepts -> patchkit bundle schema, dry-run, apply report and validators
```

External references do not authorize direct repository mutation, provider execution, Blender runtime, FFmpeg runtime, dependency changes or secret/network work.

## What this layer is

This layer is:

```text
a stable AI-readable map of external concepts adopted by the project
a project-specific translation of external documentation into repository rules
a navigation aid for future AI coding sessions
a contract for generating, validating and reviewing AI artifacts
a compact alternative to committing full external repositories
```

## What this layer is not

This layer is not:

```text
a complete mirror of upstream docs
a replacement for local validation
a runtime dependency
a permission to perform destructive changes
a reason to bypass AGENTS.md, the unified launcher, owner maps, validators, heap/exchange lifecycle, patchkit or telemetry
a reason to skip available tools because of historical limitation notes
a place for long generated patch-plan/evidence blocks
```

## Curated reference docs

```text
docs/AI_REFERENCE_SOURCE_MAP.md
docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md
docs/AI_GUARDRAILS_VALIDATION_GUIDE.md
docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
```

Large tool/schema catalogs such as `Tools/validation/README.md` and `docs/JSON_SCHEMAS.md` are references only. They must not be treated as first operational entrypoints.

## Manual-review patch-plan evidence route

Documentation patch plans generated from local AI evidence should use repository task/evidence routes instead of long chat paste, ignored report commits or managed blocks embedded into onboarding docs.

Rules:

```text
keep full local reports under ignored output/**
commit only compact task-scoped evidence under docs/LOCAL_VALIDATION_EVIDENCE/ when useful
keep documentation-only patch plans provider-free unless explicitly derived from run-unica evidence
include telemetry/capability/final-summary context when derived from run-unica evidence
include heap/exchange lifecycle context when product lanes were selected
keep patch application manual-review-only
use patchkit for reviewed source-write bundles when expressible
```

## Run-unica evidence and reference rules

A run-unica reference or handoff is incomplete if it only points to evidence or a patch plan.

Use the full group:

```text
launcher manifest
phase_status / phase_reports
evidence artifacts
heap/exchange runtime entry
heap/exchange runtime state
heap/exchange runtime exit product
heap/exchange lifecycle report
patchkit report when source-write boundary was selected
patch-plan artifacts when produced
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
file-line-limit reports when maintainability is in scope
```

GitHub-only agents may rely on local/runtime facts only when those facts are committed, pasted by the maintainer or included in a PR/comment with concrete fields.

## Safe extension rule

If a new external reference becomes useful, do not paste large upstream docs into this repository.

Instead:

```text
1. add the source to AI_REFERENCE_SOURCE_MAP.md
2. describe only the project-relevant concept
3. map it to local files and validators
4. add telemetry/capability/handoff implications if it affects run-unica evidence
5. add broker/registry/validator/telemetry implications if it affects runtime architecture
6. add heap/exchange lifecycle or patchkit implications if it affects product/source-write boundaries
7. keep the original source external
```
