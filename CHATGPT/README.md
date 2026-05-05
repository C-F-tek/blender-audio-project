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
Source-of-truth remains code, tests, validation reports, runtime bundle evidence and canonical docs.
```

Recommended read order:

```text
1. docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
2. CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
3. docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
4. docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
5. docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
6. docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
7. docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
8. docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
9. docs/LOCAL_AI_TASKS/project-tool-registry.md
10. docs/TECH_DEBT_TRACKER.md
11. CHATGPT/next-chat-handoff-2026-05-05-post-broker-runtime-telemetry.md
12. CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md
13. CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
14. docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
15. docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
16. FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
17. docs/LOCAL_AI_TASKS/ai-patch-delivery-policy.md
18. docs/LOCAL_AI_TASKS/global-datastamp-ai-packets-contract.md
```

Current active follow-up:

```text
Inspect the refactor/reuse full-run runtime bundle for run 20260505-143844, classify recommendations and patch plans, and select a controlled review-first mega patch for method/class/helper/tool reuse.
```

Current runtime bundle:

```text
ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
```

Current compact context notes:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
```

Bundle handling policy:

```text
The bundle is a runtime artifact published as a GitHub draft release asset from PR #187.
It is intentionally not committed to the repository.
Do not infer bundle contents from file existence alone.
Inspect manifest, decision loop, recommendations, patch plan, telemetry, capability manifest, full toolbox telemetry summary, shared AI-to-AI bundle, provider diagnostics and workload quality before selecting patches.
```

Resolved broker telemetry context:

```text
The earlier broker telemetry gap from run 20260505-002508 is historical context.
Commit a85bbf4 and later evidence validated preservation of runtime_tool_broker_full_toolbox_<STAMP>.json inside final runtime_tool_usage_telemetry_<STAMP>.json.
Do not treat fix-final-runtime-broker-telemetry-task-2026-05-05.md as the current active task unless investigating a regression.
```

Current tool documentation state:

```text
Tool audits must scan the whole repository, not only Tools/**.
Non-canonical candidates include root audio entrypoints and Scripting/** Blender/audio runtime scripts.
Promotion to project tool requires placement, CLI/report contract, guardrails and validation.
Broker promotion requires stricter report-only/no-side-effect guardrails.
See:
- docs/LOCAL_AI_TASKS/project-tool-registry.md
- docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
- docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
- docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
- docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
```

Git policy:

```text
Commit CHATGPT/*.md when they describe stable operational knowledge.
Do not commit output/**, renders/**, *.db, *.sqlite, *.sqlite3 or temporary local patch-builder outputs.
```
