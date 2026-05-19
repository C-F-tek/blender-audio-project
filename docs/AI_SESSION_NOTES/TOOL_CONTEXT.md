# docs/AI_SESSION_NOTES context

## Role

`docs/AI_SESSION_NOTES/` contains session notes, decision records, evidence narratives and human/AI-readable summaries created during repository work.

These files preserve operator intent and implementation history, but they are not runtime state and do not override current source code.

## Intended content

```text
session notes
implementation summaries
operator decisions
known limitations
validation narratives
handoff notes for future work
```

## How to use

AI agents may use these files to understand why a change exists, what was validated, and what risks were known at the time.

Before acting on a session note:

1. check the date and branch context;
2. verify whether the referenced files still exist;
3. inspect current code before applying recommendations;
4. distinguish narrative from validated artifact.

## Boundaries

- A session note is not a run report.
- A session note is not a patch candidate.
- A session note is not proof that a provider or validation actually executed.
- If a note references output paths, verify the artifacts before relying on them.

## Relationship to other docs

```text
LOCAL_AI_TASKS -> task/request intent
LOCAL_VALIDATION_EVIDENCE -> compact validation/evidence artifacts
AI_SESSION_NOTES -> narrative/handoff/decision summaries
```

Keep these roles separate when updating documentation.

## Git policy

Session notes may be committed when useful for handoff or review. Do not paste raw logs, full runtime artifacts, database dumps or generated chunk caches into session notes.
