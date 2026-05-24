# Compact evidence model

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `CODE_PRODUCT_FULL_PATCH.md` is the final patch/code product; `PLAN_PRODUCT_FULL_PATCH.md` is the final recomposed GPU1 prompt/chat product, with pointer graph and recovery/congruence as technical attachments.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


## Status

Current compact model extracted from historical `docs/LOCAL_VALIDATION_EVIDENCE/**` bundles and AI-to-AI evidence runs.

Use this document to decide what can be committed as evidence and what must remain runtime output.

## One-line model

```text
raw runtime output -> selected facts -> compact evidence -> Git-trackable reference
```

Evidence is useful only when it is small, current, attributable and linked to source/runtime artifacts.

## Why this exists

Runtime runs can generate large output trees:

```text
output/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
SQLite databases
semantic chunks
provider raw logs
render/media outputs
```

Those are not documentation by default.

The repository needs compact committed evidence that says:

```text
what ran
when it ran
which source/branch/stamp it used
which reports were produced
what passed/failed
which artifacts are intentionally not committed
what decision follows
```

## Artifact classes

### Raw runtime output

```text
output/**
local run directories
raw provider logs
raw chunk directories
SQLite runtime files
render outputs
large generated bundles
```

Default policy: do not commit.

### Compact evidence

```text
docs/LOCAL_VALIDATION_EVIDENCE/*.md
docs/LOCAL_VALIDATION_EVIDENCE/*.json
small selected summaries
run evidence summaries
validation evidence summaries
```

Commit only when selected intentionally.

### AI-to-AI bundle

An AI-to-AI bundle is compact context for another AI run.

It should include:

```text
run identity
request summary
relevant source refs
selected report refs
validation status
blocked/product status
next action
```

It should not copy the whole runtime output tree.

### Product evidence

Product evidence supports a code/patch/review product.

It should include:

```text
candidate operations
changed target files
validation reports
blocked/success classification
manual review notes
```

Evidence alone is not a product unless it supports a concrete product path.

## Commit policy

Allowed by default when intentional:

```text
source files
tests
small documentation
selected compact evidence
reviewed patch/code product docs
```

Not allowed by default:

```text
output/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
large generated chunk folders
```

## Evidence checklist

Before committing compact evidence, answer:

```text
Is it small enough to review?
Does it identify the run/stamp/branch/source?
Does it distinguish pass/fail/blocked?
Does it link or name raw artifacts instead of copying them?
Does it avoid secrets/private runtime state?
Does it support a current decision?
Is it still current after source changes?
```

If not, keep it local or regenerate a smaller summary.

## Staleness rules

Evidence becomes stale when:

```text
source changed after the run
branch changed
validation command changed
provider/tool behavior changed
artifact paths no longer exist
it was generated from an interrupted run
it reports only file existence without execution evidence
```

Stale evidence may remain historical, but it must not be used as current proof.

## Relation to real product model

```text
compact evidence -> may support product
compact evidence alone -> not product
raw output -> not product
metadata-only evidence -> not product
```

For product classification, read:

```text
docs/REAL_PRODUCT_RUN_MODEL.md
```

## Related current files

```text
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/CONTEXT_COVERAGE_STATUS.md
docs/DISPATCHER_CONTEXT_COVERAGE.md
docs/LOCAL_VALIDATION_EVIDENCE/TOOL_CONTEXT.md
Tools/validation/docs_hygiene/TOOL_CONTEXT.md
Tools/validation/runtime_universe/TOOL_CONTEXT.md
```

## Historical source examples

```text
docs/LOCAL_VALIDATION_EVIDENCE/*bundle*.md
docs/LOCAL_VALIDATION_EVIDENCE/*evidence*.md
docs/LOCAL_VALIDATION_EVIDENCE/*summary*.md
```
