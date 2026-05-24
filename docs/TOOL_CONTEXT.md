# docs context

## Role

`docs/` contains repository documentation, operator task files, validation evidence, execution plans, session notes, package creation guidance and architectural context.

This directory is a mixed documentation surface. Some files are stable runbooks, some are historical notes, some are task inputs, and some are compact evidence. AI agents must classify document role before acting on it.

## Main subareas

| Area | Role |
| --- | --- |
| `LOCAL_AI_TASKS/` | Operator task specs, handoffs, run requests and local workflow instructions. |
| `LOCAL_VALIDATION_EVIDENCE/` | Compact Git-trackable validation/evidence summaries. |
| `AI_SESSION_NOTES/` | Session notes, decision narratives and implementation summaries. |
| `EXECUTION_PLANS/` | Planned or completed execution plans. |
| Root docs | Architecture, workflow, package creation, audits and shared scripting guidance. |

## Document role classification

Before using a doc, classify it:

```text
contract      -> defines current rules or invariants
runbook       -> describes a command/procedure
request/task  -> input to a workflow
session note  -> narrative state/history
evidence      -> observed validation/run summary
reference     -> background or design material
obsolete      -> superseded by code or newer docs
```

Do not treat every Markdown file as current runtime truth.

## Important current docs

```text
CHATGPT.md
Tools/TOOL_CONTEXT.md
docs/SCRIPT_SURFACE_CONTEXT.md
docs/SHARED_SCRIPTING_UTILITIES.md
docs/LOCAL_AI_TASKS/tool-context-documentation-pass-2026-05-19.md
docs/LOCAL_AI_TASKS/non-tools-script-context-pass-2026-05-19.md
docs/LOCAL_AI_TASKS/exhaustive-script-surface-inventory-2026-05-19.md
docs/LOCAL_AI_TASKS/mapping-tool-evidence-publishing-2026-05-19.md
```

## Mapping and evidence publishing

When the repository surface changes or a documentation pass needs complete coverage, use:

```text
docs/LOCAL_AI_TASKS/exhaustive-script-surface-inventory-2026-05-19.md
docs/LOCAL_AI_TASKS/mapping-tool-evidence-publishing-2026-05-19.md
```

The first document defines the exhaustive script inventory procedure. The second defines how to run mapping tools locally and publish only compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`.

## Relationship to code

Docs must follow current code and dispatchers. If a doc references an old direct script path but the current code uses a package dispatcher, prefer the dispatcher and mark the doc as stale until updated.

Canonical tool invocation pattern:

```powershell
python -m Tools.<area> <tool> [tool args...]
```

## Evidence boundaries

Evidence docs prove only the checked property. They do not replace source inspection or current artifact verification.

Keep these separate:

```text
doc request -> intent
runtime output -> local run data
validation evidence -> compact observed check
code product -> diff/code applicability artifact
```

## Git hygiene

Do not paste raw logs, large runtime outputs, database dumps, generated chunks, render outputs or full provider raw transcripts into docs. Prefer compact summaries with paths and validation status.

## Extension rule

When adding a new major script surface or workflow area, add a local `TOOL_CONTEXT.md` or update `docs/SCRIPT_SURFACE_CONTEXT.md` so future agents can discover it without chat memory.
