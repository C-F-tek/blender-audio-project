# docs/LOCAL_VALIDATION_EVIDENCE context

## Role

`docs/LOCAL_VALIDATION_EVIDENCE/` contains compact, Git-trackable validation and evidence summaries. It is the place for selected reports that help future agents understand what was checked without committing raw runtime output.

This directory is evidence, not runtime state.

## Intended content

```text
compact JSON/Markdown evidence bundles
validation summaries
line-count CSV/Markdown reports
repository consistency summaries
AI-to-AI bundle summaries
selected chunk manifests when intentionally tracked
```

## Not intended content

Do not use this directory as a dump target for raw run output.

Keep these out unless explicitly converted into compact evidence:

```text
output/** raw reports/checkpoints
provider raw logs
large context packs
SQLite databases
render/video/audio outputs
generated code chunk caches
```

## Evidence interpretation

Evidence proves only what the report checked. It does not automatically prove that a final product is apply-ready.

Keep these distinct:

```text
smoke passed -> checked property passed
provider ran -> provider execution occurred
matrix passed -> deterministic code/lab check passed
code product -> diff/code artifact or explicit no-op/non-applicable state
```

## AI usage

When using evidence files:

- cite the exact evidence file and field;
- check freshness and branch relevance;
- prefer current run artifacts if available;
- do not use old evidence to override current source code;
- do not infer source writes from report existence.

## Git policy

Evidence here may be committed when it is compact and intentionally selected. Do not include raw artifacts, checkpoint directories or databases.
