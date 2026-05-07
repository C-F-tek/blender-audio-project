# Obsolete and monolithic docs review — 2026-05-07

Status: active review index  
Scope: documents that are historical, oversized, monolithic, generated-like, or unsafe as primary operator entrypoints.

## Rule

Do not delete these files automatically. Mark them as historical/reference/superseded first, then prune only under an explicit documentation-pruning task.

Current replacement reading path:

```text
read-first-reuse-first-small-files-rule-2026-05-07.md
code-derived-ai-toolchain-map-2026-05-07.md
script-census-and-validation-flow-2026-05-07.md
single-owner-scripts-and-flow-boundaries-2026-05-07.md
code-driven-data-flow-map-2026-05-07.md
validator-smoke-cycle-map-2026-05-07.md
unified-local-ai-refactor-launcher.md
UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

## Flag meanings

| Flag | Meaning |
|---|---|
| `historical` | Retained for old task/run context, not current command source. |
| `reference-catalog` | Useful lookup catalog, but not a primary entrypoint. |
| `monolithic` | Too broad/large for first-read usage; should point to compact maps. |
| `superseded` | Current code-driven maps or launcher contract should be used instead. |
| `generated-like` | Looks like generated/captured inventory or evidence; do not hand-maintain as source authority. |

## Current flagged documents

| Document | Flags | Current action |
|---|---|---|
| `docs/LOCAL_AI_TASKS/full-access-md-telemetry-refactor-cycle-2026-05-06.md` | historical, superseded | Already reduced to historical pointer. Do not use as current command source. |
| `docs/LOCAL_AI_TASKS/code-aware-command-contract.md` | reference-catalog, monolithic | Keep as CLI arg reference only. Do not use as primary workflow map. Prefer script census and owner maps. |
| `docs/LOCAL_AI_TASKS/code-aware-tool-index.md` | reference-catalog, monolithic | Keep as tool lookup only. Prefer single-owner and script census maps. |
| `Tools/validation/README.md` | reference-catalog, monolithic | Keep as validator catalog. Prefer validator-smoke-cycle-map for choosing checks. |
| `docs/DATA_FLOW.md` | broad-reference | Already compacted to point at code-driven data-flow map. |
| `docs/MODULE_MAP.md` | broad-reference | Already compacted to point at owner maps. |
| historical `next-chat-handoff-*` docs | historical | Use only when explicitly resuming that exact handoff. Current maps win. |
| old full-access/full0to10 task snapshots | historical, superseded | Retain for forensic comparison; do not start from them. |

## Obsolete marker template

Use this header when converting a specific document:

```text
Status: historical / superseded reference.
Current entrypoint: docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md.
Current code-derived behavior: docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md.
Current owner map: docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md.
```

## Review process

Before marking a document obsolete:

```text
1. read the document
2. inspect the referenced code or owner script
3. verify a current compact map covers the behavior
4. mark as historical/reference/superseded
5. do not delete unless an explicit prune task exists
```

## Stop conditions

Do not mark a document obsolete if it is the only place that documents active code behavior. First move the active behavior into a compact current map, then mark the old document.
