<!-- IA-CARMINE-MD-SPLIT: part -->
# LOCAL_RUNS_TESTING_AND_EVIDENCE — parte 002 di 002

Sorgente indice: [`../LOCAL_RUNS_TESTING_AND_EVIDENCE.md`](../LOCAL_RUNS_TESTING_AND_EVIDENCE.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Effective run bundle construction

An effective run bundle should include the same validation reports plus the compact artifact pack for actual review output.

Name effective bundles with a precise purpose:

```text
effective_<lane>_<purpose>_<YYYYMMDD-HHMMSS>.json
effective_<lane>_<purpose>_<YYYYMMDD-HHMMSS>.md
```

Examples:

```text
effective_code_patch_plan_validation_20260502-153000.json
effective_local_ai_core_activation_20260502-153000.json
```

Effective bundle requirements:

```text
include validation reports
include compact artifact packs, not large raw output
include fresh line-count CSV report
include explicit provider-execution status
include explicit patch-application status
include manual-review decision
```

Do not version raw effective run files from `output/**`.

## Commit policy

Before committing evidence:

```powershell
git status --short
git diff --check
git diff --cached --name-only
```

Stage only explicit compact evidence:

```powershell
git add `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\macro_validation_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\macro_validation_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\python_line_count_$Stamp.csv"
```

Never use:

```powershell
git add .
```

Recommended commit message pattern:

```text
test: add <lane> validation evidence
```

or:

```text
chore(evidence): add <effective-run-purpose> evidence bundle
```

## Stop conditions

Stop immediately if:

```text
validator output is not JSON-parseable
any output/** file is staged
any database file is staged
any full analysis JSON is staged
provider execution happens in a provider-free phase
Blender runtime starts in a non-runtime phase
patch application happens without explicit task authorization
contract drift reports source_writes_performed=true
bundle validation fails
merge conflict appears during stacked local testing
```

## Promotion model

Recommended promotion order:

```text
1. local branch validation
2. compact evidence bundle
3. manual review
4. PR merge only after green gate
5. effective/prototype branch only after documentation and validation lanes are stable
```

For multi-PR work:

```text
merge documentation/contract PR first
update dependent tooling PR on top of new master
rerun focused validators
then merge tooling PR
```

For prototype implementation:

```text
start a new branch
reuse existing report-only artifacts as input
keep provider execution explicit
keep Blender runtime separate
commit only reviewed source/docs/evidence
```
