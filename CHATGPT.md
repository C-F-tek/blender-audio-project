# CHATGPT operational memory

This is the root pointer for ChatGPT-assisted repository memory.

Read this directory early when entering the repository as a human, cloud AI, local AI, Codex-style agent or automated review assistant:

```text
CHATGPT/
```

Primary file:

```text
CHATGPT/README.md
```

Current source-of-truth bridge:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

Current heap/exchange and patchkit model:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
```

Current capability and decision maps:

```text
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
docs/LOCAL_AI_TASKS/script-aging-visibility-audit-2026-05-09.md
```

Main runtime architecture target:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Current canonical launcher contract:

```text
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Current active task family:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
```

Historical handoff file:

```text
CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
```

This handoff remains useful forensic context for the refactor/reuse run and draft release bundle, but it is no longer the current repository state by itself. Prefer the current operational bridge, heap/exchange operating model, AI orientation map, capability depth map, parameter decision map, main runtime architecture and launcher contract before following old branch/PR references from this handoff.

Historical runtime bundle:

```text
ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
```

The bundle is a runtime artifact published as a GitHub draft release asset from PR #187 and is intentionally not committed to the repository.

Robust chat/tooling recovery notes:

```text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md
```

Current patch application boundary:

```text
Tools/ai/patchkit/apply_patch_bundle.py
```

Future long or delicate patch work should prefer repository-native patchkit bundles:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.ps1
patch_specs/<bundle>/fragments/*.py
```

Contract:

```text
- CHATGPT/*.md is durable operational memory.
- It is advisory but should be read before planning new local AI/full-toolbox work.
- Source-of-truth remains code, validation reports, canonical docs, runtime bundle evidence and current git state.
- Capability claims require report/manifest/telemetry/evidence, not only historical handoff text.
- Do not use CHATGPT notes to override AGENTS.md guardrails.
- Do not use historical handoffs as active branch state without checking current operational docs and GitHub state.
- Do not treat patch-note ledgers as executable patches; convert them into reviewed branch diffs or patchkit bundles.
```

Local AI discovery rule:

```text
Any repository scanner/context-pack builder should include CHATGPT/*.md as lightweight high-priority context.
```
