# Next step — Tools/validation README reduction

## Status

`Tools/validation/README.md` is still too long for the new visibility/length policy and contains old long procedural blocks.

During GitHub-only review on PR #187, a full-file replacement attempt was intentionally stopped because the GitHub contents API returned a SHA mismatch on this long file. Do not force-update it blindly.

This file is a task brief, not a command catalog. Current executable commands live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
```

## Objective

Reduce `Tools/validation/README.md` to a compact validator catalog.

Preserve:

```text
purpose
common validation report contract
core validator catalog
inventory builder catalog
AI/provider/report validator catalog
NPU/helper validator catalog
Blender/generated-file validator catalog
minimal command ownership notes
guardrails
```

Move or replace long procedural flows with links to:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_WORKFLOW.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
```

## Known issues to fix

The current README has these policy problems:

```text
long procedural blocks make it function as a runbook instead of a catalog
old provider/multistep command chains can look like primary entrypoints
AI workload / NPU command examples may include control-character corruption in fetched content
no compact visibility-first front matter
no length-policy statement
```

## Required replacement shape

Target file should be approximately 300-500 lines, not 700+.

Sections:

```text
# Tools/validation
## Purpose
## Visibility and length policy
## Common validation report contract
## Unified flow entrypoints
## Validator groups
### Core repository checks
### Inventory builders
### AI pipeline and report checks
### Workload quality and provider-adjacent checks
### NPU helper checks
### Blender and generated-file checks
## Tool visibility contract
## Evidence policy
## Generated artifact path policy
## Guardrails
```

## Validation ownership

After local edit, validate through the unified launcher where possible. Focused validator checks may be run from `Tools/validation/README.md` only to debug or validate the catalog itself.

Required evidence surfaces:

```text
launcher manifest when launcher was used
docs link report
validation report contract
final git diff --check result
final git status summary
```

## Guardrail

Do not delete validator command references entirely unless the corresponding tool is absent from the repo. Prefer compact catalog rows over long copied command blocks.

Do not make `Tools/validation/README.md` another full-run or provider-runbook. It must remain a validator catalog with references back to the unified launcher.
