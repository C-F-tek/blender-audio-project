# IA-Carmine Codex Hooks

This directory contains experimental repository-local Codex lifecycle hook scripts.

## Default state

Repository hooks are **disabled by default**.

The active repository config is:

```json
{
  "hooks": {}
}
```

This prevents Codex App session startup, chat goal submission, and tool execution from being affected by repository-local hooks.

## Why disabled

During local Codex App usage, hook execution caused session/chat errors. The repository must prioritize stable Codex operation over hook automation.

## Available scripts

The scripts remain in this directory as opt-in experiments only:

- `session_start_context.py`: repository context loader.
- `pre_tool_guard.py`: advisory command context.
- `post_tool_review.py`: advisory validation reminders.
- `user_prompt_context.py`: disabled helper; do not wire into `UserPromptSubmit` until tested in the target Codex App build.

## Required policy for future reactivation

Do not enable hooks repo-wide until a small compatibility test proves that Codex App can:

- open a session;
- submit a chat goal/prompt;
- run a simple command;
- continue a normal conversation after hook output.

Any future hook configuration must remain non-destructive and must not merge, push, delete, deploy or change permissions.

## Local emergency disable

If a local session breaks, keep this file as documentation and disable only the config:

```text
.codex/hooks.json -> hooks.disabled.json
```

or replace the config with:

```json
{
  "hooks": {}
}
```
