# docs/LOCAL_AI_TASKS context

## Role

`docs/LOCAL_AI_TASKS/` contains operator task documents, handoff notes, run requests, procedures and local AI workflow instructions.

These files are input/context for tools and humans. They are not runtime execution by themselves.

## How task Markdown is used

A task Markdown can drive a run only when an explicit launcher/tool consumes it, for example:

```powershell
python -m Tools.ai run --request-file <task.md> ...
python -m Tools.workflow run_local_ai_markdown_task ...
```

A Markdown file alone does not prove that a run happened.

## Typical content

```text
handoff state
operator request
runbook/procedure
known failure notes
patch planning notes
tool/context documentation tasks
validation checklist
next-chat continuation notes
```

## Rules for AI agents

- Read the current task file before acting.
- Check whether the task is historical, active, superseded or evidence-only.
- Do not follow stale invocation paths if current dispatchers differ.
- Prefer current `python -m Tools.<area> <tool>` commands.
- Do not treat a task proposal as a patch candidate.
- Convert task decisions into code/product only through validated tools and diffs.

## Relationship to evidence

Task files describe intent. Evidence files under `docs/LOCAL_VALIDATION_EVIDENCE/` describe observed outputs or compact validation summaries.

Keep these separate:

```text
task/request -> intent
runtime output -> observed run data
evidence bundle -> compact Git-trackable summary
code product -> diff/code applicability artifact
```

## Git policy

Task Markdown can be committed when it is useful handoff documentation. Do not include raw `output/**`, database contents, generated chunk caches or render artifacts inside task docs.
