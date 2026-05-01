# Local AI Tasks

This folder contains Markdown task entrypoints for non-interactive local AI runs.

A local AI runner can start from one task file without a chat prompt. Each task file must point back to:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
```

The local AI must always read those files first and treat them as the repository contract before acting.

## Current task entrypoints

| File | Purpose |
|---|---|
| `issue-57-docs-congruence-cleanup.md` | Complete the documentation/workflow-state cleanup after selective planner merge. |

## Runner expectation

A local command should pass one of these Markdown files as the task/instruction file to the AI runner.

The runner should not require interactive chat. The task file contains:

```text
required reading order
task scope
guardrails
allowed changes
validation commands
expected PR/report content
stop conditions
```

## Hard rule

If a task file conflicts with `AGENTS.md`, preserve `AGENTS.md` hard guardrails and stop with a conflict report.
