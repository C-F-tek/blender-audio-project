# Technical Debt Tracker

## Purpose

This tracker records known technical debt for `blender-audio-project`.

Use it when an issue is real but not fixed immediately. The goal is to prevent drift, repeated rediscovery, and accidental broad rewrites.

## Status values

```text
open
in_progress
blocked
resolved
wont_fix
```

## Priority values

```text
P0 critical
P1 high
P2 medium
P3 low
```

## Tracker

| ID | Area | Priority | Status | Symptom | Risk | Recommended action | Last reviewed |
|---|---|---:|---|---|---|---|---|
| TD-001 | AI pipeline validation | P2 | open | Local runner has required several PowerShell compatibility fixes. | Future unattended validation may regress on shell edge cases. | Keep runner simple, validate on Windows PowerShell, avoid Markdown backtick fences in `.ps1`. | 2026-04-29 |
| TD-002 | JSON validation | P3 | resolved | PowerShell-generated JSON reports can contain UTF-8 BOM. | Validator false negatives. | `check_json_artifacts.py` now reads with `utf-8-sig`. | 2026-04-29 |
| TD-003 | Blender shared compatibility | P2 | resolved | `Scripting/shared/blender_compat.py` needed runtime validation inside Blender. | Premature adoption could break audio strips or node creation. | Blender 5.1.1 no-render smoke passed for frame range, noise node and VSE audio strip creation; package migration remains a separate task. | 2026-04-29 |
| TD-004 | Ready To Jazz package | P2 | open | Large standalone/monolithic script. | Harder patching and reuse. | Do not split yet; extract shared infrastructure first and migrate one call site at a time. | 2026-04-29 |
| TD-005 | `v61b_backgood` backup folder | P3 | open | Backup-style folder appears in package validation context. | Validator noise and AI confusion. | Decide whether to archive, exclude, or document it after checking for unique fixes. | 2026-04-29 |
| TD-006 | Formal JSON schemas | P2 | open | JSON contracts are documented but not fully enforced. | AI artifacts can drift. | Add schema validators gradually for AI pipeline reports, scene specs and music summaries. | 2026-04-29 |
| TD-007 | NPU pipeline decomposition | P2 | open | Some NPU orchestration files remain large. | Harder testing and provider replacement. | Split later into config, context builder, prompts, providers, validators, artifact writer and runner. | 2026-04-29 |
| TD-008 | Documentation link validation | P3 | resolved | Many docs reference other docs, but no link checker existed. | Broken AI onboarding path. | `Tools/validation/check_docs_links.py` added; run after documentation changes. | 2026-04-29 |
| TD-009 | Refactor status consistency | P2 | resolved | Pipeline status is duplicated across docs and `refactor_status.py`. | Future inconsistency can confuse agents. | `Tools/validation/check_refactor_status_consistency.py` added; run after AI pipeline/status docs changes. | 2026-04-29 |
| TD-010 | Agent state memory integration | P2 | in_progress | Generic state packets and retention policy exist, but app integration is not validated yet. | Persistent memory could become stale, noisy or too project-specific. | Run memory policy validator regularly, validate packets on Blender/audio smoke tasks, keep SQLite generated/untracked. | 2026-04-29 |
| TD-011 | Local Blender add-ons | P3 | open | Blender 5.1 startup logs show Animation Nodes compiled for Python 3.11 while Blender uses Python 3.13. | Add-on startup noise could hide real smoke-test failures or slow background validation. | Disable/update Animation Nodes for Blender 5.1 or run smoke tests with a clean Blender profile. | 2026-04-29 |

## Add a new item

Use the next ID:

```text
TD-012
```

Template:

| ID | Area | Priority | Status | Symptom | Risk | Recommended action | Last reviewed |
|---|---|---:|---|---|---|---|---|
| TD-012 | area | P2 | open | symptom | risk | action | YYYY-MM-DD |

## Rules

- Keep items concise.
- Do not use this tracker as a replacement for specific execution plans.
- Mark resolved items instead of deleting them.
- Add a new execution plan for debt that requires multi-step work.
- Review this file after major refactors.
