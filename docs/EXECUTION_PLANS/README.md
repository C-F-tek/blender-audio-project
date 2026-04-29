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

## Promotion rules

Move plans manually:

```text
active/ -> completed/   when implemented and validated
active/ -> abandoned/   when intentionally stopped
active/ -> active/      when still in progress
```

Do not delete completed or abandoned plans unless explicitly requested.

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

## Result

not completed yet

## Follow-up

<Next task or validation.>
```

## AI-agent rules

- Read active execution plans before starting related work.
- Update the plan when scope changes.
- Record validation commands and results.
- Do not treat a plan as completed without proof of work.
- Do not silently abandon a plan; move it to `abandoned/` with a reason.
