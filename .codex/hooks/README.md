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
- `UserPromptSubmit`: classifies the prompt and injects nearby repo context.
- `PreToolUse`: adds advisory context before risky or broad commands.
- `PostToolUse`: adds validation reminders after tool execution.

There is deliberately no `Stop` hook.

## Local review

After pulling these files locally, inspect and trust them from Codex with:

```text
/hooks
```

If needed, disable any single hook from the Codex hook browser.
