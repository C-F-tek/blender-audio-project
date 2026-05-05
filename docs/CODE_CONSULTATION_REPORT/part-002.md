<!-- IA-CARMINE-MD-SPLIT: part -->
# CODE_CONSULTATION_REPORT — parte 002 di 002

Sorgente indice: [`../CODE_CONSULTATION_REPORT.md`](../CODE_CONSULTATION_REPORT.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

### `det_doc_code_009` — `doc_code`

- Source: `gpu_recommendation`
- Status: `ready_for_manual_review`
- Risk: `low`
- Target file: `docs/CODE_CONSULTATION_REPORT.md`
- Manual review required: `True`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/ci.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/ci.yml`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:END -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_code_007:docs-code_consultation_report.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_code_007`
- Area: `doc_code`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/CODE_CONSULTATION_REPORT.md`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/code-quality.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/code-quality.yml`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_code_007:docs-code_consultation_report.md -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_code_008:docs-code_consultation_report.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_code_008`
- Area: `doc_code`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/CODE_CONSULTATION_REPORT.md`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/code_quality.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/code_quality.yml`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_code_008:docs-code_consultation_report.md -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_code_009:docs-code_consultation_report.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_code_009`
- Area: `doc_code`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/CODE_CONSULTATION_REPORT.md`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/ci.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/ci.yml`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_code_009:docs-code_consultation_report.md -->
