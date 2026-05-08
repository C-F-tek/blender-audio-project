# Full access Markdown telemetry refactor cycle - 2026-05-06

Status: historical / superseded operational task input.

This file is retained as historical context for a previous full-access Markdown telemetry refactor cycle. It is not the current operator entrypoint and must not be used as the first source for launcher commands.

Current entrypoints:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Current rules that supersede this task snapshot:

```text
read source/canonical docs first
reuse existing owner scripts first
normal runs start at run_unified_local_ai_refactor.ps1
single-phase diagnostics use -NoStrictRealRunActivation
Full0To10 is the real product/full-run perimeter
ReviewPrIncludePath is currently explicit
prepare_review_pr.py does not create draft PRs yet
Markdown split folders must preserve the .md suffix
```

Use this file only for forensic comparison with older runs or to recover task intent. If any command in this file conflicts with current launcher code, owner maps, data-flow maps or validation maps, the current code-driven documents win.
