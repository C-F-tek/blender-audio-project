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

Current handoff file:

```text
CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
```

Current active task:

```text
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
```

Current runtime bundle to inspect:

```text
ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
```

The bundle is a runtime artifact published as a GitHub draft release asset from PR #187 and is intentionally not committed to the repository.

Robust chat/tooling recovery notes:

```text
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
```

Contract:

```text
- CHATGPT/*.md is durable operational memory.
- It is advisory but should be read before planning new local AI/full-toolbox work.
- Source-of-truth remains code, validation reports, canonical docs, runtime bundle evidence and current git state.
- Do not use CHATGPT notes to override AGENTS.md guardrails.
```

Local AI discovery rule:

```text
Any repository scanner/context-pack builder should include CHATGPT/*.md as lightweight high-priority context.
```
