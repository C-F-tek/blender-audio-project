# 06 — Recursive `.md/` directory policy

## Purpose

Define the documentation structure rule discussed in chat:

```text
When a Markdown document grows beyond 500 lines, it should stop growing as a single file and become a document-directory.
```

The concept is recursive and applies to ChatGPT handoffs, operational runbooks, architectural notes and long evidence-oriented documentation.

## Rule

If a Markdown file exceeds 500 lines, convert it conceptually into:

```text
<name>.md/
  README.md
  01-*.md
  02-*.md
  03-*.md
```

The directory name intentionally keeps the `.md` suffix.

This is a feature, not a typo.

AI agents must not assume that paths ending in `.md` are always files. They must check whether a path is a file or a directory.

## Why

Large Markdown files degrade future AI sessions because they:

```text
consume too much context
hide the current entrypoint
make diff review difficult
mix policy, examples, evidence and historical notes
become stale faster
encourage copy/paste macro-patches
```

The 500-line threshold keeps operational docs compact and aligns with the current run-unica policy that the first layer must remain navigable.

## Recursive behavior

The policy can be repeated inside a `.md/` directory.

Example:

```text
CHATGPT.md/
  README.md
  hardware-memory.md/
    README.md
    01-architecture-summary.md
    02-sqlite-heap-memory-design.md
    03-broker-hardware-delegation-contract.md
```

If `02-sqlite-heap-memory-design.md` later exceeds 500 lines, it may become:

```text
02-sqlite-heap-memory-design.md/
  README.md
  01-schema.md
  02-chunking.md
  03-search.md
  04-cli.md
```

## Discovery rule for AI agents

When reading documentation, an AI agent must:

```text
check whether a `.md` path is a file or directory
if it is a file, read normally
if it is a directory, read README.md first
then read numbered child Markdown files in order
then recurse into child `.md/` directories when relevant
```

This prevents the agent from being fooled by the `.md` suffix.

## Naming convention

Preferred directory form:

```text
<topic>.md/
  README.md
  01-overview.md
  02-contract.md
  03-commands.md
  04-validation.md
  05-next-steps.md
```

For ChatGPT session memory:

```text
CHATGPT/<date>-<topic>/
  README.md
  01-*.md
  02-*.md
```

If later desired, `CHATGPT/` can be mirrored by or migrated toward a `CHATGPT.md/` directory, but do not rename/delete the existing `CHATGPT/` folder without an explicit migration PR because current repository reading order already references it.

## What belongs in README.md of a `.md/` directory

The index file must contain:

```text
purpose
current status
reading order
child file list
source-of-truth precedence
what not to read first
what is historical/supporting
```

It must stay compact.

## 500-line enforcement policy

When a maintained Markdown file exceeds 500 lines:

```text
new content should go into a child file or a sibling `.md/` directory
large historical sections should be moved under a numbered child doc
command blocks should move to command-specific docs
artifact/evidence details should move to evidence docs or bundle manifests
```

Do not rewrite large files mechanically just to satisfy the threshold. Split them when editing naturally or when they block future AI readability.

## Large files that may remain larger than 500 lines

Allowed exceptions:

```text
generated evidence with manifest/summary
historical/archive docs
schema notebooks/catalogs
validator/tool catalogs
external reference captures
```

But these must not be primary operational entrypoints.

Examples already treated as catalog/supporting:

```text
docs/JSON_SCHEMAS.md
Tools/validation/README.md
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
```

## Relation to AGENTS-style best practices

External AI-coding guidance recommends keeping machine-readable agent instruction files compact and splitting complex projects into nested/hierarchical files when documentation grows. This project extends that principle with a stricter local convention: 500 lines triggers `.md/` modularization for maintained operational docs.

## Relation to ChatGPT folder

`CHATGPT/` remains the current advisory session-memory folder.

Future-compatible concept:

```text
CHATGPT/      current physical folder
CHATGPT.md/   allowed future document-directory form
```

Do not treat either as a replacement for:

```text
AGENTS.md
README.md
WORKFLOW.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

`CHATGPT/` and any future `CHATGPT.md/` are advisory handoff surfaces.

## Guardrails

Do not perform destructive renames automatically.

Do not delete existing `CHATGPT/` content.

Do not move files between documentation trees without updating reading order and references.

Do not make oversized Markdown primary again just because it exists in a `.md/` directory.

Do not hide active commands inside deep child files without a compact parent index.
