# Execution Plans

## Purpose

Execution plans are durable task records for multi-step work in `blender-audio-project`.

They prevent important context from living only in chat history and make the repository easier for humans and AI agents to continue safely.

## Folder structure

```text
docs/EXECUTION_PLANS/
  README.md
  active/
  completed/
  abandoned/
```

## Current architecture context

Before acting on old plans, read the current operational and architecture contracts:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Current runtime target:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

## Legacy active plan policy

Some older plans remain under `active/` even when most of their original work was completed or superseded. Treat them as **legacy active / follow-up** unless current operational docs confirm they are still the primary task.

Rules:

```text
old active plans do not override AGENTS.md, current operational state or main runtime architecture;
if a plan predates Full0To10 post-PR187, verify it against current launcher and telemetry contracts;
if a plan mentions old provider roles, map them to current GPU1/GPU0/NPU/broker/validator/telemetry terminology;
do not move active/ -> completed/ or active/ -> abandoned/ without explicit approval for file moves;
when updating in place, add a current review note instead of deleting historical context.
```

## When to create an execution plan

Create a plan when work involves any of these:

```text
multiple files
runtime behavior changes
AI pipeline changes
shared utility migration
Blender package migration
validation/debug cycles
GitHub workflow changes
large documentation restructuring
```

A plan is usually not required for a one-file documentation typo or a small generated-index commit.

## Naming convention

Use:

```text
YYYY-MM-DD_short_slug.md
```

Examples:

```text
2026-04-29_validate_ai_pipeline_refactor.md
2026-04-29_blender_compat_manual_smoke.md
2026-04-29_ready_to_jazz_split_assessment.md
```

## Required sections

Each plan should contain:

```text
title
status
goal
scope
out of scope
files likely touched
validation commands
risk level
progress log
future task notes
result
follow-up
```

## Status values

Use one of:

```text
active
completed
abandoned
blocked
```

For old files left under `active/` for compatibility, add a `Current review note` explaining whether the plan is:

```text
legacy active / follow-up
legacy active / relocation-needed
legacy active / schema-follow-up
legacy active / architecture-seeded follow-up
```

## Promotion rules

Move plans manually:

```text
active/ -> completed/   when implemented and validated
active/ -> abandoned/   when intentionally stopped
active/ -> active/      when still in progress
```

Do not delete completed or abandoned plans unless explicitly requested.

File moves are structural documentation changes. Do not perform broad execution-plan moves without explicit approval.

## Template

```markdown
# <Task title>

## Status

active

## Goal

<What should be achieved.>

## Scope

<Files, folders, modules or behavior included.>

## Out of scope

<What must not be changed.>

## Files likely touched

```text
path/to/file
```

## Validation commands

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
```

## Risk level

low | medium | high

## Progress log

- YYYY-MM-DD: <note>

## Future task notes

- <Useful follow-up discovered while changing code, intentionally left out of this task.>

## Result

not completed yet

## Follow-up

<Next task or validation.>
```

## AI-agent rules

- Read active execution plans before starting related work.
- Read current operational state and main runtime architecture before old plans.
- Update the plan when scope changes.
- When code changes reveal a useful future capability, record it under `Future task notes` instead of expanding the current scope silently.
- Record validation commands and results.
- Do not treat a plan as completed without proof of work.
- Do not silently abandon a plan; move it to `abandoned/` with a reason only when file moves are explicitly approved.
- Do not let historical execution plans override current Full0To10, broker, telemetry, provider-lane or validator contracts.
