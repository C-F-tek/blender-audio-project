# Patch/code product boundary model

## Status

Current compact model for source-change product boundaries in IA-Carmine.

Use this document to distinguish provider prose, patch suggestions, code products, PatchKit bundles, repo-patch-runner actions and real source application.

## One-line model

```text
evidence -> plan -> candidate operation -> code/patch product -> reviewed apply boundary -> validation -> commit/review
```

Do not skip stages.

## Artifact classes

### Provider proposal

```text
provider answer
Ollama reasoning/suggestion
GPU0 review note
NPU audit note
```

Status: evidence only.

### Recommendation / patch plan

```text
recommended change
patch plan
quality note
task patch suggestion
```

Status: planning evidence. Not apply-ready without concrete operation.

### Patch candidate

```text
target file exists
operation is concrete
unified diff or exact code payload exists
validation path exists
```

Status: possible product input.

### Code product

```text
CODE_PRODUCT_FULL_PATCH.md
captured real diff/code
section classification
already integrated/no-op/manual-review/apply candidate
```

Status: reviewable code product only when real diff/code or explicit no-op/non-applicable state is present.

### PatchKit bundle

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*
```

Status: deterministic apply boundary when reviewed and explicitly invoked.

### Repo patch runner

```text
python -m Tools.repo_patch_runner apply_repo_mods ...
```

Status: controlled repository modification runner. Use only when explicitly intended.

## Product separation rule

Keep these separate:

```text
provider proposal -> evidence
patch plan -> edit strategy
patch candidate -> concrete diff/code payload
code product -> reviewable captured product
patchkit bundle -> deterministic apply package
apply step -> explicit reviewed operation
commit/PR -> repository publication
```

A patch plan without concrete diff/code is not apply-ready.

## Invalid product states

Do not call these products:

```text
provider prose only
recommendation without target file
metadata-only patch spec
empty artifact without explicit no-op status
verified target with no diff
truncated code block
invented path
manual review item with no payload
```

These may be evidence or blocked states, not source-change products.

## Valid blocked states

A blocked state is valid when explicit:

```text
no concrete operation found
payload missing or truncated
target file missing
validator failed
source-write permission not granted
manual review required
```

Blocked is safer than fake success.

## Apply boundary rule

Source writes require an explicit apply boundary.

Accepted boundaries:

```text
reviewed code-product safe apply
reviewed PatchKit bundle apply
reviewed repo-patch-runner apply
manual operator edit
```

Not apply boundaries:

```text
provider answer
recommendation
patch plan
compact evidence
AI-to-AI bundle
runtime report
```

## Validation rule

Before a source-change product is trusted:

```text
target source inspected
operation/diff reviewed
line counts checked for code/script files
py_compile or parser checks run when applicable
git diff --check run when applicable
specific smoke/contract validator run when available
```

Missing validation must be reported, not hidden.

## Git rule

Commit only intended source/test/docs/compact-evidence files.

Do not commit runtime-heavy output:

```text
output/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```

## Related current files

```text
docs/REAL_PRODUCT_RUN_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
ia_carmine/product/code_product/TOOL_CONTEXT.md
ia_carmine/product/patch_product/TOOL_CONTEXT.md
ia_carmine/product/patchkit/TOOL_CONTEXT.md
Tools/repo_patch_runner/CONTEXT_INDEX.md
Tools/validation/code_product/TOOL_CONTEXT.md
Tools/validation/patch_product/TOOL_CONTEXT.md
```
