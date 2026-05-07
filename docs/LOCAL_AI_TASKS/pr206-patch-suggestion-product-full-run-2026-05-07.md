# PR206 Patch Suggestion Product Full Run

Status: active local full-run task  
Scope: PR206 final phase, patch suggestion product quality, report-only review.

## Objective

Run the local AI toolbox against one concrete repository request:

```text
Evaluate whether the current NPU observability proposal is a concrete,
review-ready patch suggestion product for this repository, while keeping
telemetry/debug findings separate from essential patch suggestions.
```

The desired output is not automatic source editing. The desired output is a
reviewable product surface:

```text
task Markdown input
-> repository consistency evidence
-> current suggestion/proposal JSON
-> patch suggestion bundle dry-run
-> product-facing patch suggestion classification
-> supplemental telemetry/debug classification
-> compact validation evidence
```

## Product Acceptance

The run is product-useful only if it can show:

```text
patch_product_status != no_applicable_patch_product
ready_for_patch_suggestion_review = true
essential_patch_suggestion_items contains concrete target files
supplemental_telemetry_debug_items is separate from product suggestions
operation_count = 0 unless deterministic operations are explicit
applied_count = 0
source_writes_performed = false for the full-run evidence path
```

The expected product-facing item is the NPU observability proposal only if it
has all of:

```text
safe source/doc target files
patch sketch
validation commands
stop conditions
manual_review_only apply mode
```

## Guardrails

```text
No merge to master.
No force-push.
No rewrite history.
No destructive delete.
No deploy.
No secrets, permissions, billing or visibility changes.
No Blender runtime.
No FFmpeg runtime.
No automatic patch-spec apply.
No commit of output/**.
No commit of indexAI/code_chunks/**.
No commit of indexAI/project_code_chunks/**.
No commit of *.db, *.sqlite or *.sqlite3.
No commit of renders/**.
```

Provider execution is allowed only through the explicit Full0To10 command for
this validation run. Patch application stays disabled unless
`-ReviewPrApplyDeterministicSuggestions` is supplied and the product contains
deterministic operations.

## Environment Note

The unified launcher must export the resolved project interpreter before any
provider, broker, GPU0 or NPU subprocess runs:

```powershell
$env:IA_CARMINE_PYTHON = "<repo>\.venv\Scripts\python.exe"
$env:PYTHONPATH = "<repo>"
```

Local probe result from this session:

```text
OpenVINO devices: CPU, GPU.0, GPU.1, NPU
gpt-oss:20b: degraded for strict JSON probe, empty response observed
qwen2.5-coder:14b: strict JSON probe passed
autumnzsd/qwen2.5-coder-tools:latest: strict JSON probe passed
```

Use `qwen2.5-coder:14b` for the PR206 full-run validation unless a later
provider probe proves `gpt-oss:20b` healthy again.

## Online Review PR Output

The full run may prepare the review PR directly when invoked with
`-PrepareReviewPr`. That phase must:

```text
use a CARMINEai/... branch
stage only explicit allowlisted source/doc/evidence paths
commit compact Git-trackable evidence under docs/LOCAL_VALIDATION_EVIDENCE
push the branch to origin
create a GitHub PR for human manual review
never merge to master
never force-push
never stage output/**, generated code chunks, DBs, SQLite files or renders
```

## Review Questions

```text
1. Is there at least one concrete patch suggestion product?
2. Are telemetry/debug/validation signals kept supplemental?
3. Does the final phase keep proposal-only output in manual review?
4. Are current suggestions regenerated from the current repository state?
5. Are validation commands and stop conditions present for the product item?
```

## Minimum Local Validation

```powershell
$ProjectPython = $env:IA_CARMINE_PYTHON
if (-not $ProjectPython) { $ProjectPython = ".\.venv\Scripts\python.exe" }

& $ProjectPython .\Tools\validation\run_patch_suggestion_bundle_apply_smoke.py `
  --repo-root . `
  --output .\output\validation\patch_suggestion_bundle_apply_smoke_pr206_product_final.json

& $ProjectPython .\Tools\ai\apply_patch_suggestion_bundle.py `
  --repo-root . `
  --output .\output\validation\patch_suggestion_bundle_apply_dry_run_current_only_pr206_product_final.json
```
