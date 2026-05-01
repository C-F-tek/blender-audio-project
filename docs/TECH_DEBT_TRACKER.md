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
| TD-001 | AI pipeline validation | P2 | open | Local runner has required several PowerShell compatibility fixes. | Future unattended validation may regress on shell edge cases. | Keep runner simple, validate on Windows PowerShell, avoid Markdown backtick fences in `.ps1`. | 2026-04-30 |
| TD-002 | JSON validation | P3 | resolved | PowerShell-generated JSON reports can contain UTF-8 BOM. | Validator false negatives. | `check_json_artifacts.py` now reads with `utf-8-sig`. | 2026-04-29 |
| TD-003 | Blender shared compatibility | P2 | resolved | `Scripting/shared/blender_compat.py` needed runtime validation inside Blender. | Premature adoption could break audio strips or node creation. | Blender 5.1.1 no-render smoke passed for frame range, noise node and VSE audio strip creation; package migration remains a separate task. | 2026-04-29 |
| TD-004 | Ready To Jazz package | P2 | open | Large standalone/monolithic script. | Harder patching and reuse. | Do not split yet; finish the app-agnostic AI/NPU/backend core first, then migrate one call site at a time after workstation validation. | 2026-04-30 |
| TD-005 | `v61b_backgood` backup folder | P3 | open | Backup-style folder appears in package validation context. | Validator noise and AI confusion. | Decide whether to archive, exclude, or document it after checking for unique fixes locally. | 2026-04-30 |
| TD-006 | Formal JSON schemas | P2 | in_progress | JSON contracts are documented but not fully enforced. | AI artifacts can drift. | AI pipeline matrix, per-case reports, GitHub evidence bundles, repository proposal reports, proposal-derived patch-spec drafts and reviewed dry-run patch specs now have focused contract docs/validators; continue with provider probe raw reports, scene specs and music summaries after report contracts remain stable. | 2026-05-01 |
| TD-007 | NPU pipeline decomposition | P2 | in_progress | Some NPU orchestration files remain large. | Harder testing and provider replacement. | Helper package work is active under `Tools/npu/pipeline/`; IO, path/contract, prompt-payload, context-summary, support-file write-planning, exact legacy-output policy and provider-preflight normalization groups are being migrated incrementally before provider execution phases. | 2026-04-30 |
| TD-008 | Documentation link validation | P3 | resolved | Many docs reference other docs, but no link checker existed. | Broken AI onboarding path. | `Tools/validation/check_docs_links.py` added; run after documentation changes. | 2026-04-29 |
| TD-009 | Refactor status consistency | P2 | resolved | Pipeline status is duplicated across docs and `refactor_status.py`. | Future inconsistency can confuse agents. | `Tools/validation/check_refactor_status_consistency.py` added; run after AI pipeline/status docs changes. | 2026-04-29 |
| TD-010 | Agent state memory integration | P2 | in_progress | Generic state packets and retention policy exist, but app integration is not validated yet. | Persistent memory could become stale, noisy or too project-specific. | Run memory policy validator locally, keep SQLite generated/untracked, and promote only distilled facts into docs. | 2026-04-30 |
| TD-011 | Local Blender add-ons | P3 | open | Blender 5.1 startup logs show Animation Nodes compiled for Python 3.11 while Blender uses Python 3.13. | Add-on startup noise could hide real smoke-test failures or slow background validation. | Disable/update Animation Nodes for Blender 5.1 or run smoke tests with a clean Blender profile. | 2026-04-29 |
| TD-012 | Generated Python policy adapters | P2 | open | Generic generated Python policy is implemented, but future non-Blender application adapters are not documented as a repeatable template. | Future validators may duplicate logic or accidentally bake Blender/audio assumptions into generic policy. | Document adapter composition pattern and require app-specific adapters to call `generated_python_policy.py` first. | 2026-04-30 |
| TD-013 | Generated artifact path policy scope | P2 | open | Artifact path policy and report scanning exist, but safe destinations may need workflow-specific extension later. | Overly broad prefixes can allow generated files into source areas; overly narrow prefixes can block legitimate reports. | Keep defaults narrow; require explicit `--allowed-prefix` or `--allowed-exact-path` and document any extension. | 2026-04-30 |
| TD-014 | GitHub-only validation boundary | P1 | open | GitHub-only agents can edit docs and plans but cannot inspect local outputs or run workstation validation. | PRs may overclaim Blender/audio/GPU/NPU validation or hand-edit generated indexes. | Mark GitHub-only PRs with `Local workstation validation pending.`, avoid runtime claims, and leave index regeneration to local owner batch. | 2026-04-30 |
| TD-015 | Validator report consistency | P2 | open | Validators do not yet have one explicitly documented common report contract. | Downstream automation may need per-validator special cases. | Review common fields (`schema_version`, `repo_root`, `passed`, `errors`) and create small follow-up PRs only after documenting current differences. | 2026-04-30 |
| TD-016 | NPU runtime wiring | P2 | in_progress | `Tools/npu/run_dual_ai_pipeline.py` still owns orchestration while helper groups are being adopted incrementally. | Partial migration can drift if helper/runtime equivalence is not validated after each group. | Next continue with runtime-safe provider result report adoption; keep provider execution adapters last. | 2026-04-30 |
| TD-017 | Local AI broker identity/policy | P2 | open | NPU/GPU/Ollama lanes are visible and testable, but there is no durable authenticated local broker/policy model yet. | Future local AI tools could mix identity, permissions, network access, provider execution and file writes without a clear gate. | After the current internal report/proposal loop is stable, add an advisory-only authenticated local AI broker plan: identity context, permission profile, resource-lane routing, network gateway boundaries and audit reports. Do not implement network or secret access until explicit policy exists. | 2026-04-30 |

## Add a new item

Use the next ID:

```text
TD-018
```

Template:

| ID | Area | Priority | Status | Symptom | Risk | Recommended action | Last reviewed |
|---|---|---:|---|---|---|---|---|
| TD-018 | area | P2 | open | symptom | risk | action | YYYY-MM-DD |

## Rules

- Keep items concise.
- Do not use this tracker as a replacement for specific execution plans.
- Mark resolved items instead of deleting them.
- Add a new execution plan for debt that requires multi-step work.
- Review this file after major refactors.
- Mark GitHub-only limitations explicitly when local validation cannot be performed.
