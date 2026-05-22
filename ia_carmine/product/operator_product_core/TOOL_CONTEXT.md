# ia_carmine/product/operator_product_core context

## Role

`ia_carmine/product/operator_product_core` contains the operator launcher controller/model layer. It connects request Markdown, repository path, output directories, explicit runtime parameters and Python executable to the existing IA-Carmine run commands.

The GUI and CLI views should stay thin and call this package instead of duplicating command construction.

## Responsibilities

- Build repeatable run commands from operator configuration.
- Keep GUI and CLI launcher behavior aligned.
- Select repository, request file, intermediate output and final output directories.
- Run product flows through existing `ia_carmine` entrypoints.
- Request provider generation by default for real product runs.
- Locate final readable product and `CODE_PRODUCT_FULL_PATCH.md` artifacts.
- Review code product artifacts through intake tooling.
- Keep review and application as separate operator actions.
- Write launcher reports for operator visibility.
- Expose one canonical product state with product kind, approval status,
  resume pointer, continuation flag and soft-close reason.

## Typical flows

```text
operator fields -> command preview
request MD -> controller -> python -m ia_carmine.cli run ... -> product artifact discovery
CODE_PRODUCT_FULL_PATCH.md -> intake classification -> reviewed no-op or reviewed application
```

The final run outcome can be a code patch product or a non-code product such
as a complete operational text/plan/decision artifact. `CODE_PRODUCT_FULL_PATCH.md`
is sent to artifact intake only when it contains a reviewable non-truncated
`diff --git` product. Empty/no-applicable/no-diff code artifacts stay evidence
for a blocked or continuation product.

## Boundaries

- The launcher is not a second runtime universe.
- It should call existing tools rather than clone heap logic.
- Product discovery is not proof of applicability.
- Empty or already-integrated code products must be classified explicitly.
- Empty, no-applicable or no-diff code products must not be sent to artifact intake.
- A bounded run can soft-close, but must leave `resume_from_block_id` and
  continuation evidence instead of pretending that cycle limits are completion.
- GUI widgets should not be the only place where product rules live.

## Validation expectations

Relevant checks include:

```powershell
python -m Tools.validation run_operator_product_launcher_smoke ...
python -m Tools.validation run_code_product_artifact_intake_smoke ...
python -m Tools.validation run_heap_runtime_completeness_gate_smoke ...
```

## Extension notes

When adding new launcher fields, update command construction and smoke coverage together. Defaults should remain usable after a fresh PC startup: explicit repo dir, request file, Python path, output dirs and direct run parameters.
