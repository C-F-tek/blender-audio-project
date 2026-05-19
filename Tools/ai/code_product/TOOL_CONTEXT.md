# Tools/ai/code_product context

## Role

`Tools/ai/code_product` owns code-product artifact handling: interpreter reports, edit proposals, patch artifact packs, docs follow-up and `CODE_PRODUCT_FULL_PATCH.md` intake.

This area turns validated code/diff evidence into reviewable artifacts. It must not confuse provider prose with apply-ready code.

## Main responsibilities

- Build code interpreter reports.
- Convert reviewed plans into code edit proposals.
- Build patch artifact packs and docs follow-up artifacts.
- Analyze `CODE_PRODUCT_FULL_PATCH.md` sections.
- Classify code-product sections as already integrated, safe-applicable, blocked or manual-review.
- Support reviewed safe application through explicit operator action.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m Tools.ai build_code_interpreter_report ...
python -m Tools.ai build_code_edit_proposal_from_plan ...
python -m Tools.ai build_code_patch_artifact_pack ...
python -m Tools.ai build_code_patch_docs_followup ...
python -m Tools.ai code_product_artifact_intake ...
python -m Tools.ai analyze_code_product_artifact ...
python -m Tools.ai full_run_bundle_zip ...
```

## Code-product states

A `CODE_PRODUCT_FULL_PATCH.md` section should be classified explicitly:

```text
real diff/code present -> review/apply candidate
already integrated -> no-op but valid
verified target with no diff -> evidence only
missing/truncated payload -> blocked/manual review
empty product -> explicit no-op/non-applicable state
```

## Guardrails

- `CODE_PRODUCT_FULL_PATCH.md` is not valid merely because it exists.
- Empty or diagnostic artifacts must not be presented as apply-ready code.
- Safe apply should be explicit and review-driven.
- Source writes must be reported accurately.
- Do not commit generated runtime bundles unless explicitly Git-trackable.

## Relationship to heap/matrix

```text
provider proposal -> heap evidence
lab/matrix diff/code -> code product source
code product intake -> review/apply classification
```

The code product should be derived from concrete diff/code captured by matrix/lab or reviewed patch evidence.

## Extension notes

When adding a new code-product format, update parser, report rendering and smoke coverage together. Add validation under `Tools/validation/code_product` or `Tools/validation/patch_product` when applicability changes.
