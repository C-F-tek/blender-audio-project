# CHATGPT session memory index

This directory contains compact, human-readable operational notes produced during ChatGPT-assisted repository work.

Purpose:

```text
- preserve recurring chat/tooling problems and robust recovery patterns;
- make handoff state discoverable to local AI and future cloud AI sessions;
- avoid repeating fragile long-chat debugging steps;
- keep notes small enough for context packs, semantic chunks and repository scans.
```

Discovery contract:

```text
AI agents should scan CHATGPT/*.md early when resuming repository work.
These notes are advisory memory, not source-of-truth code.
Source-of-truth remains code, tests, validation reports and canonical docs.
```

Recommended read order:

```text
1. CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md
2. CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
3. docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
4. docs/LOCAL_AI_TASKS/ai-patch-delivery-policy.md
5. docs/LOCAL_AI_TASKS/global-datastamp-ai-packets-contract.md
```

Git policy:

```text
Commit CHATGPT/*.md when they describe stable operational knowledge.
Do not commit output/**, renders/**, *.db, *.sqlite, *.sqlite3 or temporary local patch-builder outputs.
```
