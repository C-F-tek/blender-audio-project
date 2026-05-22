# Codex advisory hooks for IA-Carmine

## Scope

This runbook documents the repository-local Codex hook scripts added under `.codex/`.

The scripts are retained as opt-in experiments only.

## Current default

Repository hooks are disabled by default.

The active config is:

```json
{
  "hooks": {}
}
```

This avoids Codex App session/chat startup errors caused by repository-local hook execution.

## Policy

Do not enable hooks repo-wide until compatibility is validated in the target Codex App build.

Future hooks must not deny tool calls, rewrite tool calls, stop Codex, force operator approval, commit, push, merge, delete, deploy or change permissions.

There must be no `Stop` hook unless the operator explicitly asks for a hard completion gate.

`UserPromptSubmit` must remain disabled until tested because it runs exactly when the operator submits a chat prompt/goal.

## Installed files

```text
.codex/hooks.json
.codex/hooks/common.py
.codex/hooks/session_start_context.py
.codex/hooks/user_prompt_context.py
.codex/hooks/pre_tool_guard.py
.codex/hooks/post_tool_review.py
.codex/hooks/README.md
docs/LOCAL_AI_TASKS/codex-advisory-hooks-runbook-2026-05-22.md
```

## Script roles if manually tested later

### session_start_context.py

Repository context loader for startup/resume only.

### pre_tool_guard.py

Advisory command context for Bash/apply_patch/Edit/Write/MCP calls.

### post_tool_review.py

Advisory validation reminders after supported tool execution.

### user_prompt_context.py

Disabled helper. Do not wire into `UserPromptSubmit` until Codex App prompt submission is proven stable.

## Local emergency disable

Rename `.codex/hooks.json` to `hooks.disabled.json`, or replace it with:

```json
{
  "hooks": {}
}
```

Then reopen Codex App.

## Validation before any future reactivation

Validate scripts with Python bytecode compilation and confirm that Codex App can open a session, submit a chat prompt, run a simple command and continue the conversation normally.
