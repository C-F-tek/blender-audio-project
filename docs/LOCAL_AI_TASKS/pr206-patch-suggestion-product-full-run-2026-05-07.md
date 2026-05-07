# PR206 Patch Suggestion Product Full Run

Status: historical task updated as product-flow reference  
Scope: unified Full0To10 launcher, patch suggestion product quality, draft review PR.

## Current interpretation

This task predates the final unified-product wording. It remains useful as a concrete example, but the active product interface is now:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Do not use this document as a separate manual runbook. Use it as a task Markdown input or as historical evidence for the product requirement.

## Objective

Run the local AI toolbox against one concrete repository request:

```text
Evaluate whether the current NPU observability proposal is a concrete,
review-ready patch suggestion product for this repository, while keeping
telemetry/debug findings separate from essential patch suggestions.
```

The desired output is now the complete launcher-owned product loop:

```text
task Markdown input
-> unified Full0To10 provider/tool/broker/validator run
-> repository consistency evidence
-> current suggestion/proposal JSON
-> patch suggestion bundle apply report
-> product-facing patch suggestion classification
-> supplemental telemetry/debug classification
-> compact validation evidence
-> deterministic patch applied on CARMINEai/* review branch when present
-> draft GitHub PR with applied code/MD diff
```

## Product acceptance

The run is product-useful only if it can show one of these states clearly:

```text
deterministic_patch_operations_ready and applied on review branch
manual_review_product_suggestions_ready with concrete source/doc targets
no_applicable_patch_product with telemetry/debug kept supplemental
```

For a real product PR, the required success surface is:

```text
patch_suggestion_bundle_apply passed
product-vs-supplemental separation passed
safe source/doc paths were derived from the apply report
draft GitHub PR was created from the CARMINEai/* review branch
output/** was not committed
DB/SQLite/render/generated chunk artifacts were not committed
```

Telemetry, heap, runtime usage, provider probes and evidence reports are secondary proof surfaces. They support or reject a patch suggestion, but they do not close the product loop by themselves.

## Launcher-owned variables

`$Stamp` belongs to the unified launcher run. The launcher receives or creates it once and propagates it to all internal tools.

Do not create a second stamp for patch apply, review PR preparation, telemetry, evidence or provider reports.

Environment is also launcher-owned:

```text
IA_CARMINE_PYTHON = provider-capable repository Python
PYTHONPATH = repository root
```

Local probe result from this session:

```text
OpenVINO devices: CPU, GPU.0, GPU.1, NPU
gpt-oss:20b: degraded for strict JSON probe, empty response observed
qwen2.5-coder:14b: strict JSON probe passed
autumnzsd/qwen2.5-coder-tools:latest: strict JSON probe passed
```

Use `qwen2.5-coder:14b` for this workstation snapshot unless a later provider probe proves another model healthy again.

## Online review PR output

The full run prepares the review PR through launcher flags, not by turning this document into a separate script chain.

The review PR phase must:

```text
use a CARMINEai/* branch
prefer automatic path discovery from patch_suggestion_bundle_apply results
allow explicit include paths only as additive/manual overrides
commit compact Git-trackable evidence only when requested and safe
push the branch to origin when -ReviewPrPush is supplied
create a draft GitHub PR when -ReviewPrCreate is supplied
never merge to master
never force-push
never stage output/**, generated code chunks, DBs, SQLite files or renders
```

If the `CARMINEai/*` branch already exists locally or remotely, the tool may reuse it. It must never apply on `master` or `main`.

## Review questions

```text
1. Did the unified launcher own the stamp and environment for the whole run?
2. Did Full0To10 run all selected provider/tool/broker/validator lanes or record explicit degradation?
3. Is there at least one concrete patch suggestion product?
4. Are telemetry/debug/validation signals kept supplemental?
5. Were source/doc paths derived from the apply report instead of broad git add?
6. Was the GitHub PR created as draft for human review?
```

## Minimum local validation

```powershell
python -m py_compile .\Tools\ai\prepare_review_pr.py
python -m py_compile .\Tools\validation\check_patch_suggestion_product_separation.py
git diff --check
```

After a real launcher run, inspect:

```powershell
Get-Content ".\output\validation\patch_suggestion_bundle_apply*.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, apply_requested, applied_count, changed_count, patch_product_status, ready_for_patch_suggestion_review, errors, warnings

Get-Content ".\output\validation\review_pr_prepare*.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, github_pr_created, github_pr_draft_requested, github_pr_url, product_commit, include_paths, auto_include_paths, errors, warnings
```
