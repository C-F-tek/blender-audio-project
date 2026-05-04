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
5. docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md
6. docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
7. docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
8. docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
9. docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
10. FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
11. docs/LOCAL_AI_TASKS/ai-patch-delivery-policy.md
12. docs/LOCAL_AI_TASKS/global-datastamp-ai-packets-contract.md
```

Current active follow-up:

```text
The post-broker run 20260505-002508 proved provider/bundle improvements but exposed incomplete final runtime broker telemetry.
Next code patch should preserve runtime_tool_broker_full_toolbox_<STAMP>.json inside final runtime_tool_usage_telemetry_<STAMP>.json.
See docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md.
```

Current tool documentation state:

```text
Tool audits must scan the whole repository, not only Tools/**.
Non-canonical candidates include root audio entrypoints and Scripting/** Blender/audio runtime scripts.
Promotion to project tool requires placement, CLI/report contract, guardrails and validation.
Broker promotion requires stricter report-only/no-side-effect guardrails.
See:
- docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
- docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
- docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
```

Git policy:

```text
Commit CHATGPT/*.md when they describe stable operational knowledge.
Do not commit output/**, renders/**, *.db, *.sqlite, *.sqlite3 or temporary local patch-builder outputs.
```
