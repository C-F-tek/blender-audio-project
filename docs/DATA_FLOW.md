# Data Flow

## Purpose

This document describes the broad data movement across `IA-Carmine Local AI Orchestration Workbench`.

For current operator navigation, flow variants and owner boundaries, start from the compact code-driven maps:

```text
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
```

This file remains the broad/background data-flow reference. The compact maps above are preferred for daily operations and PR review.

## Current core AI orchestration flow

```text
unified launcher command
  -> run unica parameters / Full0To10 perimeter / explicit -No* opt-outs
  -> unified_local_ai_refactor_manifest.json
  -> local source/docs/context
  -> Markdown and script inventories
  -> CSV/count evidence surfaces
  -> file-line-limit evidence surface
  -> auto-discovery and index-drift reports when relevant
  -> semantic code chunks and selected focused chunks when useful
  -> task-scoped AI context pack when useful
  -> SQLite-backed agent state packet when enabled
  -> validation reports
  -> workload report quality gate for Full0To10/provider lanes
  -> advisory lane routing
  -> trusted/excluded context selection
  -> provider probes and primary advisory generation unless disabled or diagnosed unavailable
  -> provider bridge/gate/readiness planning when selected
  -> effective-use local memory/product surfaces when selected
  -> post-validation AI packet and proposals
  -> full-context golden proposal families when requested
  -> proposal-derived draft patch specs
  -> explicit replacement plan and reviewed dry-run spec
  -> runtime broker report
  -> runtime tool usage telemetry
  -> runtime/hardware capability manifest
  -> final tool-product evidence/readiness package when selected
  -> full toolbox run telemetry summary
  -> generated artifact path policy for push-safe bundle names
  -> compact evidence bundle under docs/LOCAL_VALIDATION_EVIDENCE/
  -> shared production AI-to-AI bundle
  -> manual review / PR / merge
```

Primary operator entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

The manifest is the first review object. Telemetry and capability manifests are the next AI reasoning surfaces. Detailed reports are opened only after manifest and telemetry show which phases produced them.

## Flow ownership rule

Normal flows must not bypass single-owner scripts.

```text
launcher owns operator entry
broker owns provider tool execution
apply_patch_suggestion_bundle owns suggestion dry-run/apply
prepare_review_pr owns staging/commit/push/PR creation
bundle builders own handoff/evidence packaging
validators own smoke and contract claims
```

Detailed owner map:

```text
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
```

## Run unica / TUTTO SU TUTTO data-flow rule

The primary model is one parameterized run:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
LightFull0To10 = evidence-only profile, not provider/runtime proof
quick/balanced/deep/custom = presets or operator parameters
-No* flags = explicit opt-out from selected lanes
400-line policy applies to maintained docs and source files
limitations are backlog to overcome, not reasons to skip available tools
```

`-Full0To10` data flow is **TUTTO SU TUTTO**.

Every intensity preset must preserve the same semantic data surfaces. `quick`, `balanced`, `deep` and `custom` may change volume, context size, token limits and runtime budget, but they must not silently remove core data flows.

The full-run perimeter can expand. When a new production-ready data surface appears, such as a registry, broker tool report, provider diagnostic, repository-consistency map, memory/context builder, discovery/index report, CSV/count surface, file-line-limit report or telemetry summary, it must be added to this document and to the launcher contract, or explicitly excluded with rationale.

## Operational data-flow map

The current operational map is maintained separately to stay compact and navigable:

```text
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
```

It includes:

```text
normal full product run
phase diagnostics
provider mesh
deterministic foundation
context and memory
patch suggestion product
deterministic patch apply
review PR preparation
validation and smoke
docs-only update
LightFull0To10
reset planning
output class map
do-not-bypass list
```

## Legacy Blender/audio flow

The historical Blender application flow remains:

```text
Audio file
  -> audio analysis process
  -> JSON analysis data
  -> music context / scene specification
  -> Blender Python script or package
  -> generated or tuned Blender scene
  -> render frames
  -> encoded video
```

This is now one application domain over the local AI orchestration workbench, not the project boundary.

## Rules for AI systems

- Start local AI flows from the unified launcher manifest path.
- Preserve run unica semantics: parameters change capacity, not scope.
- Preserve TUTTO SU TUTTO coverage for `Full0To10` unless a lane is explicitly disabled, unavailable or excluded with rationale.
- Add new stable data surfaces to the compact data-flow map when the full-run perimeter expands.
- Read telemetry/capability surfaces before declaring run success or failure.
- Treat limitations as backlog to overcome, not as reasons to skip available tools.
- Exclude unusable workload reports from advisory context before reading their content.
- Treat NPU short smoke success as diagnostic evidence, not as general advisory promotion.
- Keep provider execution report-bound and opt-out inside Full0To10, not implicit outside selected workflows.
- Do not treat LightFull0To10, provider bridge/readiness or capability manifests as real provider execution proof unless the artifact itself records provider execution.
- Do not treat local output SQLite memory writes as source writes, and do not commit generated DB files.
- Do not overwrite large analysis JSON files unless explicitly requested.
- Treat `indexAI/` and generated manifests as generated context.
- Preserve local path configurability.
- Keep input-domain validators separate from output-application adapters.
- Keep Blender runtime out of core provider orchestration work unless explicitly scoped.
- Document every new expected input and output.

## Missing formal schemas

`docs/JSON_SCHEMAS.md` exists as a schema-notes file, but the following contracts still need more formal treatment:

- unified launcher manifest/phase contract beyond the compact contract doc;
- provider probe report;
- provider bridge/readiness report;
- effective-use SQLite memory/product report;
- runtime tool usage telemetry;
- runtime/hardware capability manifest;
- full toolbox run telemetry summary;
- shared AI-to-AI bundle final summary;
- discovery/index repair reports;
- Python line-count and function/class/method CSV surfaces;
- file-line-limit report;
- selected semantic chunks report/evidence beyond the focused contract already present;
- full-context golden proposal report beyond the focused validator already present;
- legacy audio analysis JSON;
- music context JSON;
- generated artifact plan/manifest schema;
- final tool-product manifest/evidence/readiness package;
- promotion from reviewed dry-run patch spec to approved local apply or GitHub Action queue;
- richer context-pack profiles and selective execution plans for changed-file workflows.

## Recommended next improvement

Keep the code-driven maps synchronized with the single-owner scripts. Then inspect current Full0To10 evidence branches and compact runtime bundles, classify recommendations and patch plans, and select review-first refactor/reuse patch families only after telemetry, provider diagnostics, workload quality, discovery/index, CSV/count and file-line-limit evidence have been reviewed.
