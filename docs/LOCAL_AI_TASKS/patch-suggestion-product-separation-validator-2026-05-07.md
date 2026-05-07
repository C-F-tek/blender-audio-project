# Patch Suggestion Product Separation Validator

Status: active proposal for next review PR  
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

The validator reads one `patch_suggestion_bundle_apply` JSON report and verifies that:

```text
essential_patch_suggestion_items exists and matches manual_review_product.product_facing_manual_review_count
supplemental_telemetry_debug_items exists and matches manual_review_product.supplemental_manual_review_count
essential items have product_facing=true and supplemental!=true
supplemental items have supplemental=true and product_facing!=true
essential items have safe source/doc targets, rationale/title, patch sketch or operation, and validation or stop conditions
provider, Blender, FFmpeg and SQLite execution flags remain false
```

## Example command

```powershell
python .\Tools\validation\check_patch_suggestion_product_separation.py `
  --repo-root . `
  --report .\output\validation\patch_suggestion_bundle_apply.json `
  --require-product `
  --require-supplemental `
  --output .\output\validation\patch_suggestion_product_separation.json
```

For a deterministic-only run, omit `--require-product` or `--require-supplemental` when that class is not expected.

## Product rule

A patch suggestion is product-facing only when it has:

```text
safe concrete source/doc target
title, description or rationale
patch sketch or deterministic operation
validation commands or stop conditions
```

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

## Follow-up integration target

Wire this validator into the final product run after `patch_suggestion_bundle_apply` so the run can fail closed when a future change collapses product-facing suggestions and telemetry/debug noise into one undifferentiated list.
