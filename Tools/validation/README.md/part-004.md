<!-- IA-CARMINE-MD-SPLIT: part -->
# README â€” parte 004 di 004

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-003.md)

## Agent review patch-plan full validation

The agent-review documentation patch-plan lane has a canonical wrapper:

```powershell
python -m Tools.validation run_agent_review_patch_plan_full_validation `
  --repo-root . `
  --orchestrator .\output\ai_pipeline\agent_gpu_npu_parallel_orchestrator_live.json `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --min-patch-plans 12 `
  --expect-fallback `
  --bundle-basename agent_review_doc_patch_plan_evidence `
  --output .\output\validation\agent_review_patch_plan_full_validation.json `
  --markdown-output .\output\validation\agent_review_patch_plan_full_validation.md
```

The wrapper runs:

```text
run_agent_review_patch_plan_smoke.py
check_docs_links.py
check_python_syntax.py
check_validation_report_contract.py
build_github_evidence_bundle.py
check_github_evidence_bundle.py
git diff --check
git status --short
```

Expected tracked evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
```

This lane is provider-free, patch-runner-free and documentation-only. Long reports remain under ignored output/**; GitHub review uses only the compact task-scoped evidence bundle.

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:START -->

## IA-Carmine patch-plan application notes

This managed block was generated from `output/patch_specs/agent_review_patch_plan.json`.
It records the manual-review patch-plan decisions for this file without applying runtime/provider changes.

### `det_doc_doc_003` — `doc_doc`

- Source: `gpu_recommendation`
- Status: `ready_for_manual_review`
- Risk: `low`
- Target file: `Tools/validation/README.md`
- Manual review required: `True`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.
- Validation commands:
  - `python -m Tools.validation check_python_syntax --repo-root . --output output/validation/python_syntax.json`
  - `python -m Tools.validation check_validation_report_contract --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the missing terms are already present after refreshing master.
  - Stop if the edit would duplicate large generated artifacts.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:END -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_doc_003:tools-validation-readme.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_doc_003`
- Area: `doc_doc`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `Tools/validation/README.md`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.
- Validation commands:
  - `python -m Tools.validation check_python_syntax --repo-root . --output output/validation/python_syntax.json`
  - `python -m Tools.validation check_validation_report_contract --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the missing terms are already present after refreshing master.
  - Stop if the edit would duplicate large generated artifacts.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_doc_003:tools-validation-readme.md -->
