# Selected Chunks Evidence Standard Block

This note documents the P5 standard evidence-bundle behavior for selected semantic chunks.

## Purpose

`Tools/ai/build_github_evidence_bundle.py` now treats compact selected-chunks evidence as a first-class optional evidence source.

The builder still reads long local validation reports from ignored `output/validation/*`, but it also discovers compact Git-trackable files matching:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*selected_chunks_evidence.json
```

The default golden-path evidence file remains:

```text
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json
```

## Guardrails

The standard block must remain:

```text
report-only
compact-evidence-only
provider-free
source-write-free
no raw output/ai_context_packs commit
no full analysis JSON commit
no patch apply
```

The evidence bundle reads only compact selected-chunks evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` unless a caller explicitly passes `--selected-chunks-evidence`.

## Added bundle fields

When selected-chunks evidence is present, the generated GitHub evidence bundle includes:

```text
source_selected_chunks_evidence
selected_chunks_evidence
decision.selected_chunks_evidence_seen
decision.selected_chunks_built
decision.budget_respected
```

These fields are optional for older or non-selected-chunks runs. Absence of selected chunks must not fail unrelated evidence bundles.

## Build command

```powershell
python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename latest_ai_workflow_evidence
```

Explicit selected-chunks evidence can be supplied with:

```powershell
python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename latest_ai_workflow_evidence `
  --selected-chunks-evidence .\docs\LOCAL_VALIDATION_EVIDENCE\full_context_golden_selected_chunks_evidence.json
```

## Validation command

```powershell
python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --output .\output\validation\github_evidence_bundle.json
```

The validator accepts the optional selected-chunks block and checks that the new decision fields are booleans when present.
