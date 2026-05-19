# Tools/validation/agent_review context

## Role

`Tools/validation/agent_review` contains checks for agent-review decision loops, patch plan reports, evidence sufficiency and review bundle behavior.

## Responsibilities

- Validate agent review decision-loop reports.
- Validate patch plan smoke behavior.
- Validate evidence sufficiency reports.
- Validate review bundle builder reports.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_agent_review_decision_loop_smoke ...
python -m Tools.validation run_agent_review_patch_plan_smoke ...
python -m Tools.validation run_agent_review_evidence_sufficiency_smoke ...
python -m Tools.validation run_agent_review_patch_bundle_builder_smoke ...
```

## Output role

Outputs are validation reports for review-loop and review-artifact behavior.

## Notes

- Review validation is not the same as final product success.
- Keep review artifacts linked to source evidence.
- Add checks here when review decision schema changes.
