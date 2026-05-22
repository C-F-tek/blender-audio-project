# IA-Carmine Codex Hooks

This directory contains repository-local Codex lifecycle hooks.

## Mode

These hooks are intentionally **non-blocking**.

They add context, warnings and validation reminders, but they do not:

- deny tool calls;
- approve tool calls;
- rewrite tool calls;
- stop Codex;
- force operator approval;
- merge, push, delete or deploy anything.

The goal is to improve continuity and action quality without breaking Codex work.

## Active hooks

- `SessionStart`: loads repository state, relevant guides, latest task handoffs and latest compact evidence.
- `PreToolUse`: adds advisory context before risky or broad commands.
- `PostToolUse`: adds validation reminders after tool execution.

## Disabled by design

- `UserPromptSubmit` is not enabled in `hooks.json`. It runs exactly when the operator submits a chat goal/prompt and can interfere with prompt entry in some Codex App builds.
- `Stop` is not enabled. The hook layer must not become a hard completion gate.

## Local review

After pulling these files locally, inspect and trust them from Codex with:

```text
/hooks
```

If needed, disable any single hook from the Codex hook browser.
