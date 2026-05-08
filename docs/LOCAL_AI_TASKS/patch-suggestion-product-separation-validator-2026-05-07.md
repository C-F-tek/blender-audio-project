# Patch Suggestion Product Separation Validator

Status: active validator integrated into the review PR product path
Date: 2026-05-07  
Scope: final product lane, patch suggestion review, product-vs-supplemental classification.

## Purpose

The patch suggestion final phase now has two different output classes:

```text
essential patch suggestion product
supplemental telemetry/debug/evidence context
```

The essential product is the only class that should drive a human-reviewed patch wave. Supplemental items remain useful for diagnostics, but must not be treated as automatic source-edit candidates.

## Validator

```text
Tools/validation/check_patch_suggestion_product_separation.py
```

The validator accepts either:

```text
patch_suggestion_bundle_apply
patch_suggestion_bundle_apply_smoke
```

For a direct `patch_suggestion_bundle_apply` report it verifies that:

```text
essential_patch_suggestion_items exists and matches manual_review_product.product_facing_manual_review_count
supplemental_telemetry_debug_items exists and matches manual_review_product.supplemental_manual_review_count
--require-product passes when either product-facing manual suggestions exist or deterministic operations are ready with failed_count=0
essential items have product_facing=true and supplemental!=true
supplemental items have supplemental=true and product_facing!=true
essential items have safe source/doc targets, rationale/title, patch sketch or operation, and validation or stop conditions
provider, Blender, FFmpeg and SQLite execution flags remain false
```

For the smoke wrapper it verifies that the smoke passed, nested commands passed, stamped deterministic suggestions were discovered, current product-facing proposal reports were included, and current supplemental update reports were included.

## Example commands

Validate the smoke wrapper produced by `run_patch_suggestion_bundle_apply_smoke.py`:

```powershell
python .\Tools\validation\check_patch_suggestion_product_separation.py `
  --repo-root . `
  --report .\output\validation\patch_suggestion_bundle_apply_smoke.json `
  --require-product `
  --require-supplemental `
  --output .\output\validation\patch_suggestion_product_separation.json
```

Validate a direct apply report:

```powershell
python .\Tools\validation\check_patch_suggestion_product_separation.py `
  --repo-root . `
  --report .\output\validation\patch_suggestion_bundle_apply.json `
  --require-product `
  --require-supplemental `
  --output .\output\validation\patch_suggestion_product_separation.json
```

For a deterministic-only run, `--require-product` is valid when `deterministic_apply_ready=true`, `deterministic_operation_count>0` and `failed_count=0`. Omit `--require-supplemental` when telemetry/debug items are not expected.

## Product rule

A patch suggestion is product-facing only when it has:

```text
safe concrete source/doc target
title, description or rationale
patch sketch or deterministic operation
validation commands or stop conditions
```

Deterministic operations are also a product when the apply report marks them ready and no operation failed.

Telemetry, debug, evidence-only, validation-only and provider diagnostic items stay supplemental.

## Guardrails

```text
report-only validator
no provider execution
no Blender runtime
no FFmpeg runtime
no SQLite writes
no patch application
no source writes
no output/** commit
```

## Launcher integration

The unified launcher runs this validator after `patch_suggestion_bundle_apply` and before `prepare_review_pr.py` when `-PrepareReviewPr` or `-ReviewPrApplyDeterministicSuggestions` is selected. The focused `run_full0to10_product_pr_chain_smoke.py` also verifies that this phase is present in the canonical workflow trace, so isolated Python smoke success is not confused with real launcher wiring.
