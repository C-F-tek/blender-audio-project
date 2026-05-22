# ia_carmine/product/generated_patch_specs context

## Role

`ia_carmine/product/generated_patch_specs` contains tooling for generated patch specification drafts, review lanes, promotion and controlled application of concrete reviewed specs.

This area is the generated-spec product lane. It sits between proposals and controlled source changes.

## Responsibilities

- Build patch specs from proposals.
- Promote draft specs when review conditions are met.
- Review generated specs before use.
- Apply concrete specs through the controlled spec apply CLI.
- Keep empty/non-applicable products explicit.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m ia_carmine.cli generated_patch_specs_from_proposals ...
python -m ia_carmine.cli generated_patch_specs_promote_draft ...
python -m ia_carmine.cli generated_patch_specs_apply ...
```

## Spec lifecycle

```text
proposal evidence -> generated spec draft -> review/promote -> controlled apply path
```

A generated spec must carry enough concrete operation data to be reviewable.

## Expected artifacts

```text
patch spec draft
reviewed spec report
promotion report
apply report
empty product report
```

## Boundaries

- Draft spec is not final application.
- Empty product must remain explicit.
- Do not infer targets from provider prose alone.
- Keep spec operations deterministic and reviewable.
- Keep generated runtime output out of Git unless explicitly selected as compact evidence.

## Validation expectations

Relevant checks include:

```powershell
python -m Tools.validation check_patch_spec_drafts ...
python -m Tools.validation reviewed_patch_specs_check ...
python -m Tools.validation run_generated_patch_specs_empty_product_smoke ...
python -m Tools.validation run_generated_patch_specs_review_pr_lane_smoke ...
```

## Extension notes

When adding a spec operation type, update parser, renderer, apply behavior and validation together.