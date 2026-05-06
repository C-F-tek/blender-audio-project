# Technical Debt Tracker

## Purpose

This tracker records known technical debt for `IA-Carmine Local AI Orchestration Workbench`.

Use it when an issue is real but not fixed immediately. The goal is to prevent drift, repeated rediscovery, and accidental broad rewrites.

## Current doctrine

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
telemetry accompanies evidence and patch plans for completeness
CSV/index/discovery surfaces are evidence lanes when relevant
large Markdown must not be a primary operational entrypoint
limitations are overcome backlog, not static reasons to skip available tools
```

Technical debt that affects manifest visibility, runtime telemetry, capability manifests, full toolbox telemetry summary, shared AI-to-AI bundles, discovery/index/CSV surfaces, oversized Markdown entrypoints or measurable capability limits should be tracked here when not fixed immediately.

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
| TD-006 | Formal JSON schemas | P2 | in_progress | JSON contracts are documented but not fully enforced, and `docs/JSON_SCHEMAS.md` is large with managed blocks. | AI artifacts can drift, and API-only rewrites risk damaging managed sections. | Treat `docs/JSON_SCHEMAS.md` as schema notebook/catalog, not a primary entrypoint. Use `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` for current launcher semantics and add compact bridge docs instead of broad rewrites. | 2026-05-05 |
| TD-007 | NPU pipeline decomposition | P2 | in_progress | Some NPU orchestration files remain large. | Harder testing and provider replacement. | Helper package work is active under `Tools/npu/pipeline/`; IO, path/contract, prompt-payload, context-summary, support-file write-planning, exact legacy-output policy and provider-preflight normalization groups are being migrated incrementally before provider execution phases. | 2026-04-30 |
| TD-008 | Documentation link validation | P3 | resolved | Many docs reference other docs, but no link checker existed. | Broken AI onboarding path. | `Tools/validation/check_docs_links.py` added; run after documentation changes. | 2026-04-29 |
| TD-009 | Refactor status consistency | P2 | resolved | Pipeline status is duplicated across docs and `refactor_status.py`. | Future inconsistency can confuse agents. | `Tools/validation/check_refactor_status_consistency.py` added; run after AI pipeline/status docs changes. | 2026-04-29 |
| TD-010 | Agent state memory integration | P2 | in_progress | Generic state packets and retention policy exist, but app integration is not fully validated yet. | Persistent memory could become stale, noisy or too project-specific. | Run memory policy validator locally when available, keep SQLite generated/untracked, expose memory state through manifest/telemetry/bundle when it contributes to full-run handoff, and promote only distilled facts into docs. | 2026-05-05 |
| TD-011 | Local Blender add-ons | P3 | open | Blender 5.1 startup logs show Animation Nodes compiled for Python 3.11 while Blender uses Python 3.13. | Add-on startup noise could hide real smoke-test failures or slow background validation. | Disable/update Animation Nodes for Blender 5.1 or run smoke tests with a clean Blender profile. | 2026-04-29 |
| TD-012 | Generated Python policy adapters | P2 | open | Generic generated Python policy is implemented, but future non-Blender application adapters are not documented as a repeatable template. | Future validators may duplicate logic or accidentally bake Blender/audio assumptions into generic policy. | Document adapter composition pattern and require app-specific adapters to call `generated_python_policy.py` first. | 2026-04-30 |
| TD-013 | Generated artifact path policy scope | P2 | open | Artifact path policy and report scanning exist, but safe destinations may need workflow-specific extension later. | Overly broad prefixes can allow generated files into source areas; overly narrow prefixes can block legitimate reports. | Keep defaults narrow; require explicit `--allowed-prefix` or `--allowed-exact-path` and document any extension. | 2026-04-30 |
| TD-014 | GitHub-only validation boundary | P1 | in_progress | GitHub-only agents can edit docs and plans but cannot inspect local outputs or run workstation validation. | PRs may overclaim Blender/audio/GPU/NPU validation, hand-edit generated indexes or ask for local sync while the maintainer is away. | GitHub-only PRs must state local validation limits, rely only on committed/pasted telemetry/evidence, avoid local-run requests unless asked, and never claim runtime success from file existence. | 2026-05-05 |
| TD-015 | Validator report consistency | P2 | open | Validators do not yet have one explicitly documented common report contract. | Downstream automation may need per-validator special cases. | Review common fields (`schema_version`, `repo_root`, `passed`, `errors`) and create small follow-up PRs only after documenting current differences. | 2026-04-30 |
| TD-016 | NPU runtime wiring | P2 | in_progress | `Tools/npu/run_dual_ai_pipeline.py` still owns orchestration while helper groups are being adopted incrementally. | Partial migration can drift if helper/runtime equivalence is not validated after each group. | Next continue with runtime-safe provider result report adoption; keep provider execution adapters last and carry quality/degradation state into telemetry/bundle when used. | 2026-05-05 |
| TD-017 | Local AI broker identity/policy | P2 | open | NPU/GPU/Ollama lanes are visible and testable, but there is no durable authenticated local broker/policy model yet. | Future local AI tools could mix identity, permissions, network access, provider execution and file writes without a clear gate. | After the current internal report/proposal loop is stable, add an advisory-only authenticated local AI broker plan: identity context, permission profile, resource-lane routing, network gateway boundaries and audit reports. Do not implement network or secret access until explicit policy exists. | 2026-04-30 |
| TD-018 | AI context packs and selective planning | P2 | in_progress | Context packs, selected semantic chunks and the report-only selective planner now exist, but ranking/freshness logic is still basic. | Agents may still choose broad or stale validation paths when several evidence bundles exist. | Continue with validator scoring, evidence freshness heuristics and clearer GitHub-only versus local-only action ranking. Full-run-derived plans must include telemetry/capability context. | 2026-05-05 |
| TD-019 | Full-context golden proposal promotion | P2 | in_progress | The deterministic full-context golden proposal generator emits P1-P6 proposal families, and later tooling now builds agent-review patch plans and richer evidence bundles. | Valuable proposal output can remain inert or be applied too broadly if promotion is not staged. | Promote one proposal or patch-plan family at a time through reviewed patch specs, focused validators, compact evidence and companion telemetry/capability summaries. Keep all application explicit and manual-review-only until validated. | 2026-05-05 |
| TD-020 | Evidence bundle growth | P2 | in_progress | Evidence bundles now include patch-plan and artifact-manifest summaries as well as provider/report decisions. | Bundles can become too large or too broad for GitHub-only review if summaries are not curated. | Keep compact summary fields stable, avoid long ignored-output payloads, and add validators for new evidence summary sections before treating them as automation inputs. Telemetry/capability should accompany evidence instead of being embedded as uncontrolled bulk. | 2026-05-05 |
| TD-021 | GPU planner fallback semantics | P2 | open | GPU planner diagnostics and fallback evidence exist, but the boundary between useful empty-state diagnostics and forced recommendations needs continued tuning. | Future agents may overfit to non-empty recommendation counts and generate low-quality patch plans. | Prefer explicit evidence-readiness diagnostics over hallucinated recommendations; keep fallback plans manual-review-only and expose degraded-provider state in telemetry/bundle summaries. | 2026-05-05 |
| TD-022 | Telemetry completeness contract | P1 | in_progress | Multiple docs now require telemetry/capability/final-summary as accessories for evidence and patch plans, but validators may not yet enforce completeness uniformly. | Future full-run evidence or patch plans may be treated as complete without executed/failed/blocked/degraded/source-write context. | Add or extend validators to check production handoff completeness: runtime usage telemetry, runtime capability manifest, full toolbox telemetry summary, shared AI-to-AI bundle/final summary and patch-plan summary references. | 2026-05-05 |
| TD-023 | Full-run perimeter expansion governance | P2 | in_progress | The `TUTTO SU TUTTO` perimeter is intentionally expandable, but new lanes need a mechanical promotion/exclusion checklist. | New tools or evidence surfaces can be omitted silently or over-promoted into the full run. | Keep `project-tool-registry.md`, promotion guide, module map and launcher contract aligned. Any new lane must be included in Full0To10 or explicitly excluded with rationale and telemetry/bundle visibility note. | 2026-05-05 |
| TD-024 | Obsolete MD drift after PR187 | P2 | in_progress | Many older docs contained legacy runbooks, old PR chains, old local commands or proof-of-work definitions without telemetry. | AI agents may restart from obsolete flows or request local commands while GitHub-only. | Continue MD/CODE audit; demote historical runbooks, remove active-start drift, and update onboarding/schema/status docs to reference launcher-first telemetry-complete handoff. | 2026-05-05 |
| TD-025 | Python string patch hygiene | P1 | in_progress | Real `SyntaxWarning` findings showed Windows-style command examples with invalid escape sequences such as `\T` and `\e`; an attempted patch bundle also exposed fragility around multiline/triple-quote edits. | Future AI or manual patches may overcorrect by introducing raw multiline/triple-quoted strings, changing indentation, corrupting embedded Markdown/code fences or masking syntax warnings instead of fixing the exact command literal. | Treat triple-quote/raw multiline rewrites as high-risk for command-example cleanup. Prefer minimal one-line literal edits, POSIX-style relative examples like `./Tools/...`, or explicit doubled backslashes. Validate with `python -m py_compile`, `git diff --check`, line counts and focused diff review. | 2026-05-05 |
| TD-026 | Large Markdown operational drift | P1 | in_progress | Some Markdown files are too large or too catalog-like to be opened reliably by future chats, local AI context packs or GitHub-only reviewers. Examples include `Tools/validation/README.md` and `docs/JSON_SCHEMAS.md`. | Oversized docs can become false primary entrypoints, hide stale commands, or force agents to rely on truncated content. | Keep oversized docs out of the primary reading path. Classify them as catalog/schema/historical/supporting/evidence, add compact bridge docs, and use Markdown inventory/length reports to find more candidates. | 2026-05-05 |
| TD-027 | Full-toolbox limitation handling | P1 | in_progress | Historical limitation notes can be misread as reasons to skip tools or shrink Full0To10 scope. | Agents may avoid available tool lanes instead of measuring and overcoming limitations. | Use all available/relevant tools by default. Treat limitations as backlog to overcome. Mark lanes unavailable/degraded only from current code, telemetry, capability manifest, provider diagnostic or validator evidence. | 2026-05-06 |

## Add a new item

Use the next ID:

```text
TD-028
```

Template:

| ID | Area | Priority | Status | Symptom | Risk | Recommended action | Last reviewed |
|---|---|---:|---|---|---|---|---|
| TD-028 | area | P2 | open | symptom | risk | action | YYYY-MM-DD |

## Rules

- Keep items concise.
- Do not use this tracker as a replacement for specific execution plans.
- Mark resolved items instead of deleting them.
- Add a new execution plan for debt that requires multi-step work.
- Review this file after major refactors.
- Mark GitHub-only limitations explicitly when local validation cannot be performed.
- Track missing telemetry/capability/final-summary enforcement when it affects full-run evidence or patch-plan completeness.
- Track oversized Markdown that cannot be opened reliably as operational drift until it is split, summarized or demoted from primary entrypoints.
- Treat limitations as backlog to overcome; do not use historical limitation notes to skip available Full0To10 tool lanes.
- Treat triple-quote/raw multiline rewrites as high-risk when fixing Python command examples or embedded Markdown/code fences; prefer minimal literal edits and validate with `py_compile` plus focused diff review.
