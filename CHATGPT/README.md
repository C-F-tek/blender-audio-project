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
Historical handoffs must be checked against current operational state and GitHub state before acting.
```

Recommended read order:

```text
1. AGENTS.md
2. CHATGPT.md
3. docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
4. docs/MAIN_RUNTIME_ARCHITECTURE.md
5. docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
6. docs/AI_PIPELINE_ARCHITECTURE.md
7. docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
8. docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
9. docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
10. docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
11. docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
12. docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
13. docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
14. docs/LOCAL_AI_TASKS/project-tool-registry.md
15. docs/TECH_DEBT_TRACKER.md
16. CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
17. CHATGPT/next-chat-handoff-2026-05-05-post-broker-runtime-telemetry.md
18. CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md
19. CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
20. AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md
```

Current active follow-up:

```text
Use docs/MAIN_RUNTIME_ARCHITECTURE.md as the architecture target for shared runtime heap / blackboard, GPU1 planner, GPU0 OpenVINO helper, NPU microtask responder, broker executor, semantic tools registry, deterministic CPU validators and telemetry/event stream work.
Keep implementation incremental, report-only first and congruent with the unified launcher and Full0To10 doctrine.
```

Historical refactor/reuse full-run handoff:

```text
CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
```

Historical runtime bundle:

```text
ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
```

The historical handoff and bundle remain useful forensic/evidence context, but they are not current branch state by themselves. Prefer:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Current compact context notes:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
```

400-line policy:

```text
Active Markdown notes should remain under 400 lines.
If a maintained Markdown file exceeds 400 lines, keep it as a compact index and move content into <file>.md/part-001.md, part-002.md, ...
Code/script files follow the same 400-line limit through compact entrypoints plus responsibility-based modules.
Use Tools/validation/check_file_line_limits.py for report-only measurement.
```

Full-toolbox limitation policy:

```text
Limitations are backlog to overcome, not reasons to skip available tools.
Use every relevant Full0To10 lane by default.
Mark a lane unavailable/degraded only from current code, telemetry, capability manifest, provider diagnostic or validator evidence.
```

Main runtime architecture policy:

```text
Provider lanes do not directly mutate repository state.
Broker unico executor is the target execution gateway for registered tools.
Semantic tools registry is the target capability source of truth.
Deterministic validators / CPU authority decide local pass/fail claims.
Telemetry/event stream must make executed, skipped, degraded and blocked phases visible.
```

Bundle handling policy:

```text
Runtime bundles are local/GitHub release artifacts, not source files.
They are intentionally not committed to the repository.
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
