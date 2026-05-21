<!-- IA-CARMINE-MD-SPLIT: index -->
# Urgent — run unica, Universo IA, GitHub patch queue

## Status

Maintained operational entrypoint for urgent follow-up work. This directory uses the `.md/` split-document pattern described in `docs/LOCAL_AI_TASKS/markdown-directory-split-policy-2026-05-05.md`.

## Purpose

Keep the current operator request in one compact, reviewable location:

```text
read canonical and relevant non-canonical Markdown
preserve context
continue next run-unica inspection
target a real complex product with Universo IA in action
do not treat smoke, provider prose or bundles as product
patch GitHub source/docs through reviewed product boundaries
```

## Reading order

1. [`01-operational-contract.md`](01-operational-contract.md)
2. [`02-next-run-inspection.md`](02-next-run-inspection.md)
3. [`03-github-patch-targets.md`](03-github-patch-targets.md)

## Current decision

```text
full_run_complete: not_proven
github_source_write_done: not_proven_until_commit_sha_exists
allowed_exit_without_product: blocked_with_reason
next_action: inspect canonical run evidence, then patch concrete source/docs only
```

## Non-goals

```text
do not commit output/**
do not commit *.db or *.sqlite
do not call a bundle a source patch
do not call a smoke a full run
do not promote NPU to primary semantic provider
do not let provider prose bypass code/patch product boundaries
```

## Git hygiene

Commit only source, tests, documentation, compact evidence, or reviewed code/patch product files. Never stage broad runtime trees.
