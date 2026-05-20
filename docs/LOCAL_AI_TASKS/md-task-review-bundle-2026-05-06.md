# MD task review bundle — 2026-05-06

## Purpose

This note documents task-scoped review bundle behavior for Markdown-driven local AI runs.

## Entrypoints

```text
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_local_ai_markdown_task.ps1
```

## Reuse-first rule

Before adding new scripts, builders, validators or workflow tools, search the repository and reuse existing functionality where practical.

Preferred behavior:

```text
reuse existing modules and helpers
extend existing builders instead of creating near-equivalent replacements
avoid duplicate validators and parallel active entrypoints
document any unavoidable new tool and why reuse was not sufficient
```

## Contract

When `-BuildEvidence` is selected, the pipeline adapter builds a compact evidence bundle scoped to the current Markdown task run.

The bundle is generated with the existing evidence builder:

```text
Tools/ai/repository_product/github_evidence_bundle.py
```

and validated with:

```text
Tools/validation/repository_product/github_evidence_bundle/cli.py
```

No new independent bundle builder is introduced.

## Flow

```text
Markdown task / prompt
  -> local AI task pipeline adapter
  -> advisory packet
  -> repository change proposals
  -> proposal contract validation
  -> optional patch-spec draft manifest
  -> adapter manifest
  -> task-scoped evidence JSON/Markdown
  -> task-scoped GitHub evidence bundle
  -> evidence bundle validation
```

## Included reports

The bundle includes available JSON reports from the current run:

```text
adapter manifest
advisory packet JSON
suggestion manifest JSON
repository change proposals JSON
repository change proposal validation report
task-scoped evidence JSON
optional patch-spec draft manifest
selected-chunk validation when built
enrichment-plan validation when built
agent-state memory manifest when built
standard validation reports passed into the adapter
```

Missing optional standard reports are skipped, not fabricated.

## Guardrails

```text
provider_execution_performed_by_adapter=false
patch_application_performed=false
source_writes_performed=false
no Blender runtime
no FFmpeg runtime
no Git commit/push/merge
no output/** commit
no SQLite DB commit
```

Patch-spec generation remains draft-only under `output/patch_specs/`.

## Evidence contract

Current adapter evidence is emitted beside the task packet:

```text
output/local_ai_runs/<run>/pipeline/<basename>_evidence.json
output/local_ai_runs/<run>/pipeline/<basename>_evidence.md
```

The evidence records:

```text
expected output checks
proposal validation summary
provider execution requested/performed flags
patch application/source write flags
evidence request state
scenario flags
```

When `-BuildEvidence` is selected, evidence JSON is included as a report and evidence Markdown is included as an artifact in the compact evidence bundle. This lets a pushed compact bundle prove the patch/spec/proposal state without committing raw `output/**`.

## Smoke command

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

python -m Tools.workflow run_local_ai_task_via_pipeline `
  -PromptFile .\AGENTS.md `
  -TaskFile .\docs\LOCAL_AI_TASKS\current-operational-state-2026-05-05.md `
  -RunDir ".\output\local_ai_runs\md_task_review_bundle_smoke_$Stamp" `
  -Profile docs `
  -Basename "md_task_review_bundle_smoke_$Stamp" `
  -ProposalBasename "md_task_review_bundle_smoke_${Stamp}_proposals" `
  -FullContextGoldenPath `
  -GeneratePatchSpecs `
  -BuildEvidence
```

## Validation

```powershell
$Evidence = ".\docs\LOCAL_VALIDATION_EVIDENCE\md_task_review_bundle_smoke_${Stamp}_evidence.json"
$Validation = ".\output\validation\md_task_review_bundle_smoke_${Stamp}_evidence_validation.json"

Test-Path $Evidence
Test-Path $Validation

Get-Content $Validation -Raw | ConvertFrom-Json |
  Select-Object kind, passed, bundle_count, errors, warnings
```

## Versioning

Do not commit generated `output/**` files.

Commit only source/docs changes and optional compact evidence under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

when evidence is intentionally selected for review.

## Follow-up hygiene — selected chunks evidence

Task-scoped evidence bundles must not silently include old selected-chunks evidence from unrelated runs.

The runner passes:

```text
--no-auto-discover-selected-chunks-evidence
```

to `Tools.ai.repository_product.github_evidence_bundle` and adds selected-chunks evidence explicitly only when the current run produced it.

This prevents a docs-only smoke without `-BuildSelectedChunksEvidence` from reporting stale `full_context_golden_*selected_chunks_evidence.json` as if it belonged to the current run.
