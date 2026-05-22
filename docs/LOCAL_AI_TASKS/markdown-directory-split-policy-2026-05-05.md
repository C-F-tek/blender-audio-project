# IA-Carmine — Markdown directory split policy — 2026-05-05

## Status

Global documentation policy for maintained operational Markdown.

This document generalizes the ChatGPT-session rule introduced in:

```text
CHATGPT/2026-05-05-newconcept-hardware-memory/06-md-directory-policy.md
```

## Core rule

When a maintained Markdown file exceeds 700 lines, it should not keep growing as a single file.

It should become or be complemented by a document-directory:

```text
<name>.md/
  README.md
  01-overview.md
  02-contract.md
  03-commands.md
  04-validation.md
  05-next-steps.md
```

The directory name may intentionally end with `.md`.

This is allowed and expected.

## AI reader rule

AI agents must not assume every path ending with `.md` is a file.

When a `.md` path appears in documentation or navigation:

```text
check whether it is a file or directory
if file: read it normally
if directory: read README.md first
then read numbered child Markdown files in order
then recurse into child `.md/` directories when relevant
```

The `.md/` suffix is intentionally used to make a directory behave like a document bundle.

## Recursive policy

This policy is recursive.

If a child Markdown file also exceeds 700 lines, it can itself become:

```text
child-topic.md/
  README.md
  01-section.md
  02-section.md
```

## Scope

Applies to maintained documentation such as:

```text
CHATGPT/**
docs/LOCAL_AI_TASKS/**
docs/EXECUTION_PLANS/**
docs architecture/policy/runbook files
root operational Markdown when actively maintained
```

Does not require immediate rewrite of every historical large file.

## Exceptions

Large files may remain single files when they are:

```text
generated evidence
historical/archive docs
schema notebooks/catalogs
validator/tool catalogs
external reference captures
```

But exceptions must not become primary operational entrypoints.

Known catalog/supporting examples:

```text
docs/JSON_SCHEMAS.md
Tools/validation/README.md
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
```

## Reason

Large Markdown harms future AI work because it:

```text
wastes context
hides the current entrypoint
increases stale reference drift
makes patch review harder
encourages macro-patches and fragile copy/paste
mixes policy, evidence, commands and history
```

External AI-coding guidance recommends keeping machine-readable instruction files compact and using nested/hierarchical documentation for complex projects. This project applies that principle with a local threshold: 700 lines for maintained operational docs.

## Implementation guidance

When editing a large maintained Markdown file:

```text
first create compact README/index
move long sections into numbered child files
keep active commands in command-specific files
move historical notes under historical/supporting child docs
move evidence details into LOCAL_VALIDATION_EVIDENCE or bundle manifests
update parent navigation and source-of-truth order
```

Do not split mechanically without understanding semantics.

Do not rename/delete existing paths without a migration plan.

## CHATGPT folder note

`CHATGPT/` remains the current physical session-memory folder.

A future `CHATGPT.md/` directory is allowed as a document-directory pattern, but do not rename `CHATGPT/` automatically. Existing reading order and handoff references already point to `CHATGPT/`.

## Acceptance criteria

A compliant large-document split has:

```text
compact parent README/index
clear reading order
numbered child docs
no hidden primary command blocks deep in children
no broken old references
large historical/supporting sections demoted
future AI can open only what is relevant
```
