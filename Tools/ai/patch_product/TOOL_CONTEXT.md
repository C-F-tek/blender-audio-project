# Tools/ai/patch_product context

## Role

`Tools/ai/patch_product` owns patch-product synthesis, patch plan quality, patch suggestion bundles, task patch suggestion artifacts and patch candidate extraction.

This area is for reviewed patch material. It should not turn provider prose directly into source writes.

## Main responsibilities

- Generate patch plans from reviewed evidence.
- Evaluate patch plan quality.
- Build patch suggestion bundles.
- Create task patch suggestion Markdown/report artifacts.
- Synthesize patch candidates only from valid evidence.
- Preserve product separation between diagnostic output, patch plan and apply-ready patch.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m Tools.ai patch_plan_generator ...
python -m Tools.ai patch_plan_quality_product ...
python -m Tools.ai build_patch_plan_quality_product_report ...
python -m Tools.ai patch_suggestion_bundle ...
python -m Tools.ai create_task_patch_suggestion_markdown ...
python -m Tools.ai build_task_patch_suggestion_report ...
python -m Tools.ai synthesize_patch_candidates ...
python -m Tools.ai patch_notes_quality_product ...
```

## Patch candidate rule

Patch candidates should come only from concrete, reviewable inputs:

```text
unified diff already present in evidence/report/proposal/operator request
target file present in the repository/context universe
git apply --check or equivalent validation passed when applicable
```

Do not invent template patches to satisfy a product gate.

## Product separation

Keep these separate:

```text
provider proposal -> evidence
patch plan -> proposed edit strategy
patch candidate -> concrete diff/code artifact
apply step -> explicit reviewed operation
```

A patch plan without concrete diff is not apply-ready.

## Guardrails

- No direct source writes from synthesis unless the tool is explicitly an apply tool and the operator requested it.
- No Git writes.
- No runtime artifact commits.
- No generated patch over unknown or invented paths.
- Preserve manual-review state when payload is missing, ambiguous or truncated.

## Validation expectations

Relevant checks include:

```powershell
python -m Tools.validation run_patch_candidate_synthesis_smoke ...
python -m Tools.validation run_patchkit_smoke ...
python -m Tools.validation run_patchkit_bundle_contract_smoke ...
python -m Tools.validation check_patchkit_bundle_contract ...
python -m Tools.validation check_patch_suggestion_product_separation ...
```

## Extension notes

When adding patch formats, update parser, bundle/report renderer and validation together. Keep PatchKit/apply semantics deterministic and fixture-tested before touching real repo files.
