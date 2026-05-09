# Problems — IA-Carmine documentation and workflow coherence

## Purpose

Code-driven register for documentation or workflow coherence problems discovered during repository review.

Use this file for issues that are not fixed in the current PR or that need a dedicated code/validation follow-up.

## Open problems

### P-001 — `docs/AI_REFERENCE_SOURCE_MAP.md` contains stale transient PR/branch state

Status: open.

Evidence from code/document review:

```text
docs/AI_REFERENCE_SOURCE_MAP.md contains a `Current branch phase` section with historical PR/branch references such as PR #187/#193/#192/#191.
```

Why it matters:

```text
This file is a reference map, not a live project-status document.
A future AI can read stale PR state and make wrong assumptions about current master, current PRs or current workflow capability.
```

Expected fix:

```text
Remove transient PR/branch status from AI_REFERENCE_SOURCE_MAP.md.
Replace it with stable pointers to current orientation docs, GitHub state, launcher manifests and validation reports.
```

Notes:

```text
A full replacement attempt was blocked by the GitHub connector safety layer during PR #251 follow-up.
Retry as a smaller focused patch.
```

### P-002 — `docs/AI_REFERENCE_SOURCE_MAP.md` priority order predates heap/exchange and patchkit

Status: open.

Evidence from code/document review:

```text
The reference map priority order still points to older operational-state and policy docs before the new heap/exchange operating model and AI orientation maps.
```

Why it matters:

```text
This can route agents into pre-#249/#250 documentation before they understand the current IN -> dynamic heap/exchange LOOP -> OUT lifecycle and patchkit boundary.
```

Expected fix:

```text
Move these documents into the first-read block:
- docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
- docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
- docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

## Closed problems

### P-003 — `prepare_review_pr.py` draft PR support was documented as not implemented

Status: closed in PR #251 documentation follow-up.

Code-driven finding:

```text
Tools/ai/prepare_review_pr.py supports --draft-pr.
validate_pr_flags() enforces --draft-pr requires --create-pr.
create_github_pr() appends --draft to gh pr create when args.draft_pr is true.
```

Outcome:

```text
Docs that claimed draft PR creation was not implemented should be updated to describe the implemented --draft-pr path.
```

### P-004 — older product-chain docs described pre-heap patch suggestion flow as current

Status: closed in PR #251 documentation follow-up.

Patched files:

```text
docs/PATCH_SPEC_WORKFLOW.md
docs/LOCAL_AI_TASKS/patch-suggestion-bundle-final-phase.md
docs/LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md
docs/LOCAL_AI_TASKS/patch-notes-quality-product-2026-05-07.md
```

Outcome:

```text
Patch/product docs now route current product work through heap/exchange entry/exit, lifecycle validation, patchkit or deterministic patch suggestion bridge, and prepare_review_pr.py.
Historical ledger docs are classified as reference/ledger workflows, not primary product paths.
```
