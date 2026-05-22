# ia_carmine/product/repository_product Context

## Role

`ia_carmine/product/repository_product` contains repository-level inspection, evidence,
review-preparation and proposal tools.

Repository-product tools produce structured evidence and planning artifacts.
They are not the source-write or apply layer.

## Responsibilities

- Build repository consistency maps.
- Build GitHub evidence bundles.
- Prepare review-oriented argument files.
- Produce repository change proposal reports.
- Produce repository update suggestions from checked evidence.
- Build large-scope repository review artifacts when explicitly scoped.

## Command Surface

Use commands through the AI dispatcher:

```powershell
python -m ia_carmine.cli <tool> [args...]
```

Representative tools include:

```text
repository_consistency_map
build_repository_consistency_map
repository_change_proposals
repository_update_suggestions
build_github_evidence_bundle
build_review_pr_prepare_args
agent_review_prepare_pr
megalithic_repo_review
megalithic_review_refinement
```

## Product Distinction

```text
repository evidence -> current repository facts
repository proposal -> suggested change candidate
review preparation -> compact review input artifact
source change -> separate validated diff/apply path
```

Repository findings are evidence. They do not mean code has changed.

## Expected Artifacts

```text
repository consistency map
repository change proposal report
GitHub evidence bundle
review preparation args
product readiness report
large-scope repository review report
```

## Boundaries

- Keep output structured and compact.
- Check current source before using older evidence.
- Keep raw runtime output out of Git unless converted into compact evidence.
- Keep source changes in separate code-product or patch-product paths.
- Keep generated runtime output out of versioned documentation unless it is
  compact evidence.

## Validation Expectations

Relevant checks include:

```text
python -m Tools.validation run_repository_consistency_map_smoke
python -m Tools.validation run_repository_change_proposals_runtime_evidence_smoke
python -m Tools.validation check_repository_change_proposals
python -m Tools.validation run_review_pr_prepare_args_smoke
```

## Extension Notes

When adding repository-product tools, include enough structured fields for later
review and avoid prose-only reports.
