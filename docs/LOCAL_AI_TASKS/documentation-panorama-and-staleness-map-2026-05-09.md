# Documentation Panorama and Staleness Map — 2026-05-09

## Purpose

Compact map for repository-wide documentation review.

Use this to decide which documents are canonical, which are navigational, which are historical, and where a future AI must verify against code before acting.

## Source hierarchy

Use this precedence order:

```text
1. current source code
2. current validators/smokes and their reports
3. current launcher manifests / phase reports / telemetry
4. canonical compact docs listed below
5. historical handoffs and generated evidence
6. old runbooks / stale PR notes
```

Docs must never override source, validators or current GitHub state.

## Canonical orientation layer

These files form the current first-read layer:

```text
AGENTS.md
README.md
CHATGPT.md
CHATGPT/README.md
docs/README.md
docs/AI_ONBOARDING.md
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

Status:

```text
AGENTS.md: primary contract, updated in PR #251 to link heap/exchange, orientation, staleness and patchkit.
README.md: updated in PR #251 to describe heap/exchange and patchkit.
CHATGPT.md: updated in PR #251 to point at heap/exchange and patchkit.
CHATGPT/README.md: updated in PR #251 to include the current read order.
docs/README.md: updated in PR #251 as current doc index.
docs/AI_ONBOARDING.md: updated in PR #251 as compact onboarding bridge.
heap-exchange operating model: new canonical post-#249/#250 model.
ai-orientation map: new compact first-orientation map for AI agents.
documentation panorama: this stale-zone map.
```

## Canonical architecture and run layer

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
WORKFLOW.md
Tools/workflow/README.md
Tools/ai/README.md
```

Status:

```text
MAIN_RUNTIME_ARCHITECTURE.md: architecture target; do not claim implemented execution without evidence.
UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md: split contract index updated in PR #251 to mention heap/exchange lifecycle and patchkit surfaces.
unified-local-ai-refactor-launcher.md: operator runbook; verify current flags against Tools/workflow/run_unified_local_ai_refactor.ps1.
unified-launcher-parameter-decision-map: current parameter decision map.
WORKFLOW.md: root workflow policy, updated in PR #251 with heap/exchange product path and patchkit boundary.
Tools/workflow/README.md: updated in PR #251 for lifecycle and patchkit.
Tools/ai/README.md: updated in PR #251 for lifecycle and patchkit.
AI_PIPELINE_ARCHITECTURE.md: updated in PR #251 so dry-run pipeline evidence cannot be mistaken for full product proof.
DATA_FLOW.md: updated in PR #251 to include heap/exchange lifecycle and patchkit.
AI_ARTIFACT_SCHEMAS.md: updated in PR #251 to include heap/exchange and patchkit artifact families.
```

## Code-driven map layer

```text
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md
```

Status:

```text
Use these for current source orientation.
They may not yet include every #249/#250 patchkit detail.
If they disagree with heap-exchange-and-patchkit-operating-model-2026-05-09.md, inspect current code and update the smaller map first.
```

## Patch/product layer

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/patch-suggestion-bundle-final-phase.md
docs/LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md
docs/LOCAL_AI_TASKS/patch-notes-quality-product-2026-05-07.md
Tools/ai/patchkit/apply_patch_bundle.py
Tools/validation/run_patchkit_smoke.py
```

Current rule:

```text
patch notes = ledger
patch suggestion = product candidate
heap exit product = deterministic product gate
patchkit bundle = preferred source-write boundary
review PR = human-review product
```

Do not apply patch-note ledger entries directly.

## Validation layer

```text
Tools/validation/README.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
Tools/validation/check_heap_exchange_runtime_lifecycle.py
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
Tools/validation/run_patchkit_smoke.py
```

Status:

```text
Tools/validation/README.md is a large catalog, not a primary first-read entrypoint.
Use targeted validator/smoke maps first.
Future cleanup should split or index the validation README only if line-limit validators require it.
```

## Historical/reference split indexes classified in PR #251

These split docs remain available, but their README indexes now warn agents not to treat them as current first-read state:

```text
docs/LOCAL_AI_WORKFLOW.md/README.md = historical/reference workflow split; use current heap/exchange and launcher docs first.
docs/PROJECT_STATUS_POINT.md/README.md = historical/reference project-status snapshot; verify against current source and maps.
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/README.md = current contract index; now points to heap/exchange lifecycle and patchkit surfaces.
```

Do not edit all split parts unless a dedicated cleanup task requires it. Prefer index banners first.

## Evidence layer

```text
docs/LOCAL_VALIDATION_EVIDENCE/**
output/**
indexAI/**
```

Policy:

```text
docs/LOCAL_VALIDATION_EVIDENCE/** may hold compact committed evidence.
output/** is generated and must not be committed.
indexAI/code_chunks/** is generated and must not be committed.
Evidence proves runs only when the matching manifest/report fields show execution, not from file existence alone.
```

## Application-domain layer

```text
Scripting/**
docs/PROJECT_OVERVIEW.md
docs/BLENDER_SCRIPT_ENTRYPOINTS.md
docs/AUDIO_ANALYSIS_PIPELINE.md
docs/RENDER_WORKFLOW.md
docs/FFMPEG_WORKFLOW.md
```

Status:

```text
These are application-domain assets.
Do not refactor or execute Blender/FFmpeg/audio paths unless the task explicitly enters that scope.
```

## Known stale or caution zones

```text
Old handoff files under CHATGPT/next-chat-handoff-*.md are forensic context only.
Old current-* documents may contain historical PR/branch references.
Large generated evidence Markdown must not become first-read documentation.
Older patch-suggestion docs may refer to pre-patchkit behavior.
Older product-chain docs may not include heap/exchange runtime entry/exit.
Any doc that claims success without manifest/telemetry evidence is suspect.
```

## Future cleanup queue

Suggested next documentation-only PRs:

```text
1. Verify MAIN_RUNTIME_ARCHITECTURE.md against the exact post-#249/#250 code and add only missing implemented-surface links.
2. Verify code-driven-data-flow-map-2026-05-07.md against heap/exchange entry/exit and patchkit.
3. Verify single-owner-scripts-and-flow-boundaries-2026-05-07.md includes patchkit and heap lifecycle owners.
4. Add a compact validation README index if Tools/validation/README.md becomes too hard to scan.
5. Add formal JSON schema validators for heap_exchange_runtime_entry, heap_exchange_runtime_exit_product and patchkit_apply_report.
```

## Agent behavior when documentation conflicts

```text
1. Stop relying on the conflicting text.
2. Inspect current source owner.
3. Inspect current validator/smoke.
4. Inspect current PR/branch/GitHub state.
5. Update the smallest canonical map.
6. Do not create a parallel doctrine document unless the index points to it and marks older docs as historical.
```
