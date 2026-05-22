# ia_carmine/product/patch_product context

## Role

`ia_carmine/product/patch_product` owns patch-product synthesis, patch plan quality, patch suggestion bundles, task patch suggestion artifacts and patch candidate extraction.

This area is for reviewed patch material. It should not turn provider prose directly into source writes.

It concretizes:

```text
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Main responsibilities

- Generate patch plans from reviewed evidence.
- Evaluate patch plan quality.
- Build patch suggestion bundles.
- Create task patch suggestion Markdown/report artifacts.
- Synthesize patch candidates only from valid evidence.
- Preserve product separation between diagnostic output, patch plan, patch candidate and apply-ready patch.
- Preserve blocked/manual-review state when a candidate is missing, ambiguous, invented or truncated.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m ia_carmine.cli patch_plan_generator ...
python -m ia_carmine.cli patch_plan_quality_product ...
python -m ia_carmine.cli build_patch_plan_quality_product_report ...
python -m ia_carmine.cli patch_suggestion_bundle ...
python -m ia_carmine.cli create_task_patch_suggestion_markdown ...
python -m ia_carmine.cli build_task_patch_suggestion_report ...
python -m ia_carmine.cli synthesize_patch_candidates ...
python -m ia_carmine.cli patch_notes_quality_product ...
```

## Patch candidate rule

Patch candidates should come only from concrete, reviewable inputs:

```text
unified diff already present in evidence/report/proposal/operator request
target file present in the repository/context universe
payload is complete and not truncated
path is verified and not invented
git apply --check or equivalent validation passed when applicable
```

Do not invent template patches to satisfy a product gate.

## Product separation

Keep these separate:

```text
provider proposal -> evidence
patch plan -> proposed edit strategy
patch suggestion -> review-oriented proposal material
patch candidate -> concrete diff/code artifact
PatchKit/repo-patch-runner/manual edit -> explicit apply boundary
```

A patch plan without concrete diff is not apply-ready.

## Invalid product states

These must remain evidence, blocked or manual-review states:

```text
provider prose only
recommendation without target file
metadata-only patch spec
empty patch suggestion
truncated diff/code block
invented path
manual review item with no payload
```

## Guardrails

- No direct source writes from synthesis unless the tool is explicitly an apply tool and the operator requested it.
- No Git writes.
- No runtime artifact commits.
- No generated patch over unknown or invented paths.
- Preserve manual-review state when payload is missing, ambiguous or truncated.
- Block product success when only patch plan/metadata exists.

## Validation expectations

Relevant checks include:

```powershell
python -m Tools.validation run_patch_candidate_synthesis_smoke ...
python -m Tools.validation check_patch_suggestion_product_separation ...
python -m Tools.validation run_patch_suggestion_bundle_apply_smoke ...
python -m Tools.validation run_task_patch_suggestion_markdown_authoring_smoke ...
python -m Tools.validation run_task_patch_suggestion_runtime_deferral_smoke ...
python -m Tools.validation run_patchkit_smoke ...
python -m Tools.validation run_patchkit_bundle_contract_smoke ...
python -m Tools.validation check_patchkit_bundle_contract ...
```

## Extension notes

When adding patch formats, update parser, bundle/report renderer and validation together. Keep PatchKit/apply semantics deterministic and fixture-tested before touching real repo files. Update `docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md` and `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` when product semantics change.