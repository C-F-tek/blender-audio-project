# ia_carmine/product/agent_review context

## Role

`ia_carmine/product/agent_review` contains review-oriented tools for evidence sufficiency, warning policy, patch plans, patch bundles, code patch plans, decision loops and review preparation.

This area evaluates and packages review information. It should not be confused with direct application of changes.

## Responsibilities

- Check evidence sufficiency.
- Build and evaluate review patch plans.
- Build review bundles.
- Run decision-loop reports.
- Apply warning policy rules.
- Prepare compact review inputs for later operator review.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m ia_carmine.cli agent_review_evidence_sufficiency ...
python -m ia_carmine.cli agent_review_patch_plan ...
python -m ia_carmine.cli agent_review_code_patch_plan ...
python -m ia_carmine.cli agent_review_patch_bundle ...
python -m ia_carmine.cli agent_review_warning_policy ...
python -m ia_carmine.cli run_agent_review_decision_loop ...
python -m ia_carmine.cli agent_review_prepare_pr ...
```

## Review model

```text
evidence -> sufficiency check -> plan/bundle -> review decision -> later product path
```

The review layer should keep decisions auditable and separate from generated runtime output.

## Expected artifacts

```text
evidence sufficiency report
patch plan report
patch bundle report
decision loop report
warning policy report
review preparation artifact
```

## Boundaries

- A review plan is not automatically an applied change.
- A review bundle must preserve target paths and rationale.
- Evidence from older runs must be checked against current source.
- Do not turn provider prose into a final decision without deterministic checks.

## Validation expectations

Relevant checks include:

```powershell
python -m Tools.validation run_agent_review_evidence_sufficiency_smoke ...
python -m Tools.validation run_agent_review_patch_plan_smoke ...
python -m Tools.validation run_agent_review_patch_bundle_builder_smoke ...
python -m Tools.validation run_agent_review_decision_loop_smoke ...
```

## Extension notes

When extending review logic, keep the output structured and include clear reason fields for accepted, rejected and deferred items.