# Data Flow

## Status

Current broad/background data-flow reference.

For first-session orientation and stale-document classification, start here instead:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

## Purpose

This document describes broad data movement across `IA-Carmine Local AI Orchestration Workbench`.

For current operator navigation, flow variants and owner boundaries, start from the compact code-driven maps:

```text
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
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
  -> heap/exchange runtime entry
  -> dynamic heap/exchange center with GPU1/GPU0/NPU/provider/context/broker lanes
  -> runtime state and public exchange events
  -> post-validation AI packet and proposals
  -> full-context golden proposal families when requested
  -> proposal-derived draft patch specs when requested
  -> patch suggestion product report when a task Markdown provides suggestions
  -> deterministic patch suggestion dry/apply when explicitly selected
  -> heap/exchange runtime exit product
  -> heap/exchange lifecycle validation
  -> product-vs-supplemental separation validation
  -> patchkit bundle/apply bridge when selected
  -> review PR preparation when explicitly selected
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
build_heap_exchange_runtime_entry owns heap/exchange entry
build_heap_exchange_runtime_exit owns heap/exchange exit product
check_heap_exchange_runtime_lifecycle owns lifecycle validation
patchkit/apply_patch_bundle owns new reviewed patchkit bundle application
apply_patch_suggestion_bundle owns legacy suggestion dry-run/apply
check_patch_suggestion_product_separation owns product-vs-supplemental validation
prepare_review_pr owns staging/commit/push/PR preparation
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
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
preferred active runbook/docs size <=400 lines
active Markdown hard threshold <=500 lines
maintained source/script target <=400 lines
limitations are backlog to overcome, not reasons to skip available tools
```

`-Full0To10` data flow is **TUTTO SU TUTTO**.

Every intensity preset must preserve the same semantic data surfaces. `quick`, `balanced`, `deep` and `custom` may change volume, context size, token limits and runtime budget, but they must not silently remove core data flows.

The full-run perimeter can expand. When a new production-ready data surface appears, such as a registry, broker tool report, provider diagnostic, repository-consistency map, memory/context builder, discovery/index report, CSV/count surface, file-line-limit report, product-separation report, heap/exchange lifecycle report, patchkit report or telemetry summary, it must be added to this document and to the launcher contract, or explicitly excluded with rationale.

## Markdown-to-review-PR product flow

Current product path:

```text
docs/LOCAL_AI_TASKS/<task>.md
  -> inventories/context/agent-state/workload-quality
  -> Tools/ai/build_heap_exchange_runtime_entry.py
  -> provider/official-adapter/proposal/patch-spec lanes
  -> Tools/ai/build_heap_exchange_runtime_exit.py
  -> Tools/validation/check_heap_exchange_runtime_lifecycle.py
  -> Tools/ai/patchkit/apply_patch_bundle.py or legacy deterministic patch suggestion bridge
  -> Tools/ai/prepare_review_pr.py
  -> GitHub PR for manual review
```

Focused proof:

```text
Tools/validation/run_full0to10_product_pr_chain_smoke.py
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
Tools/validation/run_patchkit_smoke.py
```

Current explicit limitations:

```text
ReviewPrIncludePath remains supported for explicit/manual allowlists.
prepare_review_pr.py can auto-discover include paths from apply reports with `--auto-include-from-apply-report` plus `--apply-report`.
prepare_review_pr.py does not create draft PRs yet.
metadata-only patch drafts are not enough for a successful review PR product.
```

This flow is not the same as the patch-spec queue. Patch specs remain explicit/manual-review-only and are documented in `docs/PATCH_SPEC_WORKFLOW.md`.

## Patchkit source-write flow

Preferred future source-write boundary:

```text
patch_specs/<bundle>/bundle.json
  -> fragments/*.ps1 or fragments/*.py
  -> Tools/ai/patchkit/apply_patch_bundle.py --dry-run
  -> Tools/ai/patchkit/apply_patch_bundle.py
  -> validators
  -> line counts
  -> review PR
```

Patchkit is deterministic infrastructure for reviewed source writes. It is not authorization to bypass guardrails.

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

If this compact map conflicts with the heap/exchange operating model or current source code, inspect source first and update the smallest map.

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
- Do not treat product-separation success as draft PR support until `prepare_review_pr.py` implements draft PR creation.
- Do not treat local output SQLite memory writes as source writes, and do not commit generated DB files.
- Do not treat metadata-only patch drafts as concrete review PR product.
- Do not bypass heap/exchange entry/exit for product paths.
- Do not bypass patchkit for new long/delicate patch bundles when patchkit can express the change.
- Do not overwrite large analysis JSON files unless explicitly requested.
- Treat `indexAI/` and generated manifests as generated context.
- Preserve local path configurability.
- Keep input-domain validators separate from output-application adapters.
- Keep Blender runtime out of core provider orchestration work unless explicitly scoped.
- Document every new expected input and output.

## Missing formal schemas

`docs/AI_ARTIFACT_SCHEMAS.md` is the compact schema guide. `docs/JSON_SCHEMAS.md` remains a broader schema/reference notebook and must not override current launcher or validator contracts.

The following contracts still need more formal treatment:

```text
unified launcher manifest/phase contract beyond the compact contract doc
heap/exchange runtime entry report
heap/exchange runtime state jsonl
heap/exchange runtime exit product report
heap/exchange lifecycle report
patchkit bundle schema and apply report
provider probe report
provider bridge/readiness report
effective-use SQLite memory/product report
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox run telemetry summary
shared AI-to-AI bundle final summary
discovery/index repair reports
Python line-count and function/class/method CSV surfaces
file-line-limit report
selected semantic chunks report/evidence beyond the focused contract already present
full-context golden proposal report beyond the focused validator already present
legacy audio analysis JSON
music context JSON
generated artifact plan/manifest schema
final tool-product manifest/evidence/readiness package
promotion from reviewed dry-run patch spec to approved local apply or GitHub Action queue
draft PR creation support for Markdown-to-review-PR product flow
draft PR creation support in prepare_review_pr.py
richer context-pack profiles and selective execution plans for changed-file workflows
```

## Recommended next improvement

Keep the code-driven maps synchronized with the single-owner scripts. Then inspect current Full0To10 evidence branches and compact runtime bundles, classify recommendations and patch plans, and select review-first refactor/reuse patch families only after telemetry, provider diagnostics, workload quality, heap/exchange lifecycle evidence, patchkit reports, discovery/index, CSV/count and file-line-limit evidence have been reviewed.
