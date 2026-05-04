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
1. CHATGPT/next-chat-handoff-2026-05-05-post-broker-runtime-telemetry.md
2. CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md
3. CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
4. docs/LOCAL_AI_TASKS/post-broker-runtime-telemetry-followup-2026-05-05.md
5. docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
6. FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
7. docs/LOCAL_AI_TASKS/ai-patch-delivery-policy.md
8. docs/LOCAL_AI_TASKS/global-datastamp-ai-packets-contract.md
```

Current active follow-up:

```text
The post-broker run 20260505-002508 proved provider/bundle improvements but exposed incomplete final runtime broker telemetry.
Next code patch should preserve runtime_tool_broker_full_toolbox_<STAMP>.json inside final runtime_tool_usage_telemetry_<STAMP>.json.
See docs/LOCAL_AI_TASKS/post-broker-runtime-telemetry-followup-2026-05-05.md.
```

Git policy:

```text
Commit CHATGPT/*.md when they describe stable operational knowledge.
Do not commit output/**, renders/**, *.db, *.sqlite, *.sqlite3 or temporary local patch-builder outputs.
```
