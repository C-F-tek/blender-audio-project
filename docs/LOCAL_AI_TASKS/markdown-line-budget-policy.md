# Markdown line budget policy

## Scope

This policy defines the operational line budget for maintained Markdown in IA-Carmine.

## Rule

```text
active maintained .md hard threshold: <= 500 lines
preferred active runbook size: <= 400 lines
generated evidence: may exceed 500 only with compact manifest/summary/index
```

If a maintained Markdown file exceeds 500 lines, it must become a compact entrypoint that points to a folder of Markdown parts.

Split layout:

```text
<file>.md
<file>.md/part-001.md
<file>.md/part-002.md
...
```

The conversion must be recursive: generated parts must also respect the 500-line hard threshold.

Excluded from normal source-documentation enforcement:

```text
output/**
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
docs/LOCAL_VALIDATION_EVIDENCE/**
```

These locations may contain generated evidence or runtime artifacts. They are not maintained source documentation.

## Commands

Dry-run:

```powershell
python -m Tools.docs split_large_markdown `
  --repo-root . `
  --max-lines 500
```

Apply:

```powershell
python -m Tools.docs split_large_markdown `
  --repo-root . `
  --max-lines 500 `
  --apply
```

Validation:

```powershell
python -m Tools.validation check_markdown_line_limits `
  --repo-root . `
  --max-lines 500
```

## Canonical references

```text
docs/LOCAL_AI_TASKS/md-coherence-only-github-pass-2026-05-06.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
AGENTS.md
```

## Versioning

Version only source files, maintained documentation and intentional compact evidence.

Do not commit:

```text
output/**
indexAI/code_chunks/**
*.db
*.sqlite
renders/**
generated media
```
