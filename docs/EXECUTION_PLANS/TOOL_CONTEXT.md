# docs/EXECUTION_PLANS context

## Role

`docs/EXECUTION_PLANS/` contains planned, active or completed execution plans for repository work. These documents describe intended work sequencing, validation and implementation constraints.

Execution plans are not runtime artifacts and are not proof that work was executed.

## Expected content

```text
planned changes
implementation phases
validation commands
risk/rollback notes
completion summaries
completed plan archive
```

## How to use

Before acting on an execution plan:

1. Check whether it is active, completed, obsolete or superseded.
2. Verify referenced source files still exist.
3. Check current dispatchers and package paths.
4. Treat commands as guidance until executed and evidenced.
5. Use current validation gates, not stale script paths.

## Relationship to task/evidence docs

```text
LOCAL_AI_TASKS        -> current operator task/request/handoff
EXECUTION_PLANS       -> plan structure and sequencing
LOCAL_VALIDATION_EVIDENCE -> compact evidence after checks/runs
AI_SESSION_NOTES      -> narrative/decision notes
```

Keep these roles separate. Do not move evidence into plans or treat plans as evidence.

## Completed plans

Completed plans may remain useful for historical reasoning, but must not override current code. If a completed plan conflicts with source files or `TOOL_CONTEXT.md`, prefer current source and mark the plan as historical.

## Git hygiene

Execution plans may be committed when concise and useful. Do not include raw runtime output, SQLite data, render outputs, generated chunk caches or huge logs.
