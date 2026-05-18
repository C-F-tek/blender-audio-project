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
docs/AI_DOCS_ENTRYPOINT.md
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
docs/AI_DOCS_ENTRYPOINT.md: updated in PR #251 follow-up as docs-folder entrypoint.
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
WORKFLOW.md: root workflow policy, updated in PR #251 with heap/exchange product path and patchkit boundary; still has one blocked full-file update follow-up tracked in problems.md.
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
docs/PATCH_SPEC_WORKFLOW.md
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
patch suggestion = bridge/product candidate
heap exit product = deterministic product gate
patchkit bundle = preferred source-write boundary
agent_review_prepare_pr.py = branch/commit/push/PR preparation owner
review PR = human-review product
```

Status:

```text
docs/PATCH_SPEC_WORKFLOW.md: updated in PR #251 follow-up; patchkit/heap lifecycle is now primary product boundary context.
patch-suggestion-bundle-final-phase.md: updated in PR #251 follow-up as bridge lane, not whole product path.
patch-suggestion-review-workflow-2026-05-07.md: updated in PR #251 follow-up as historical proposal-ledger review reference.
patch-notes-quality-product-2026-05-07.md: updated in PR #251 follow-up as historical/reference task, not current product path.
```

Do not apply patch-note ledger entries directly.

## Validation layer

```text
Tools/validation/README.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
Tools/validation/heap_exchange/runtime_lifecycle_check/cli.py
Tools/validation/heap_exchange/runtime_lifecycle_smoke/cli.py
Tools/validation/run_patchkit_smoke.py
```

Status:

```text
Tools/validation/README.md is a large catalog, not a primary first-read entrypoint.
Use targeted validator/smoke maps first.
Future cleanup should split or index the validation README only if line-limit validators require it.
```

## Reference/external layer

```text
docs/AI_REFERENCE_ONBOARDING.md
docs/AI_REFERENCE_SOURCE_MAP.md
docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md
docs/AI_GUARDRAILS_VALIDATION_GUIDE.md
docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md
```

Status:

```text
AI_REFERENCE_ONBOARDING.md: updated in PR #251 follow-up with heap/exchange and patchkit mapping.
AI_REFERENCE_SOURCE_MAP.md: still has stale transient PR/branch state and old priority order; tracked in problems.md P-001/P-002.
Other files are reference material; inspect current code before treating them as active implementation state.
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
Older patch-suggestion docs may still exist; check this map before treating them as current.
Older product-chain docs may not include heap/exchange runtime entry/exit unless explicitly updated above.
Any doc that claims success without manifest/telemetry/evidence report fields is suspect.
```

## Future cleanup queue

Suggested next documentation-only PRs:

```text
1. Verify code-driven-data-flow-map-2026-05-07.md against heap/exchange entry/exit and patchkit.
2. Verify single-owner-scripts-and-flow-boundaries-2026-05-07.md includes patchkit and heap lifecycle owners.
3. Apply a focused safe patch to AI_REFERENCE_SOURCE_MAP.md to remove stale transient PR/branch state and update first-read priority.
4. Add a compact validation README index if Tools/validation/README.md becomes too hard to scan.
5. Add formal JSON schema validators for heap_exchange_runtime_entry, heap_exchange_runtime_exit_product and patchkit_apply_report.
6. Verify MODULE_MAP.md, PROJECT_AUDIT.md, KNOWN_LIMITATIONS.md and TECH_DEBT_TRACKER.md for stale current-state claims.
```

## Agent behavior when documentation conflicts

```text
1. Stop relying on the conflicting text.
2. Inspect current source owner.
3. Inspect current validator/smoke.
4. Inspect current PR/branch/GitHub state.
5. Update the smallest canonical map.
6. Record unresolved coherence issues in problems.md.
7. Do not create a parallel doctrine document unless the index points to it and marks older docs as historical.
```
