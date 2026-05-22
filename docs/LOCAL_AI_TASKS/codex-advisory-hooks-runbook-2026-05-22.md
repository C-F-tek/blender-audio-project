# Codex advisory hooks for IA-Carmine

## Scope

This runbook documents the repository-local Codex hooks added under `.codex/`.

The hooks improve context, continuity and validation quality while preserving normal Codex flow.

## Policy

These hooks are advisory only.

They do not deny tool calls, rewrite tool calls, stop Codex, force operator approval, commit, push, merge, delete, deploy or change permissions.

There is deliberately no `Stop` hook.

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

## Behavior

### SessionStart

Adds repository state, current branch, latest commit, dirty state, known guide files, latest task handoffs, latest compact evidence and IA-Carmine policy reminders.

### UserPromptSubmit

Classifies the incoming prompt and injects the closest available repository context.

Detected labels include:

```text
heap_runtime
provider_gpu_npu
evidence_bundle
patch_or_refactor
docs_hygiene
git_flow
general_repo_work
```

### PreToolUse

Adds advisory context before Bash, apply_patch, Edit, Write and MCP tool calls.

It highlights broad Git staging, runtime artifact paths and other command shapes that should normally be handled with explicit scope.

### PostToolUse

Adds advisory validation reminders after tool execution, especially when Python paths or runtime/local paths appear in the working tree.

## Local activation

After pulling the files locally, open Codex and run:

```text
/hooks
```

Review and trust the hook definitions.

## Validation

Validate the hook scripts locally with Python bytecode compilation and `git diff --check` before relying on them for daily work.
