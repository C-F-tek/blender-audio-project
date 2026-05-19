# Tools/ai/operator_product_core context

## Role

`Tools/ai/operator_product_core` contains the operator launcher controller/model layer. It connects request Markdown, repository path, output directories, intensity profile and Python executable to the existing IA-Carmine run commands.

The GUI and CLI views should stay thin and call this package instead of duplicating command construction.

## Responsibilities

- Build repeatable run commands from operator configuration.
- Keep GUI and CLI launcher behavior aligned.
- Select repository, request file, intermediate output and final output directories.
- Run product flows through existing `Tools.ai` entrypoints.
- Locate final readable product and `CODE_PRODUCT_FULL_PATCH.md` artifacts.
- Review code product artifacts through intake tooling.
- Keep review and application as separate operator actions.
- Write launcher reports for operator visibility.

## Typical flows

```text
operator fields -> command preview
request MD -> controller -> python -m Tools.ai run ... -> product artifact discovery
CODE_PRODUCT_FULL_PATCH.md -> intake classification -> reviewed no-op or reviewed application
```

## Boundaries

- The launcher is not a second runtime universe.
- It should call existing tools rather than clone heap logic.
- Product discovery is not proof of applicability.
- Empty or already-integrated code products must be classified explicitly.
- GUI widgets should not be the only place where product rules live.

## Validation expectations

Relevant checks include:

```powershell
python -m Tools.validation run_operator_product_launcher_smoke ...
python -m Tools.validation run_code_product_artifact_intake_smoke ...
python -m Tools.validation run_heap_runtime_completeness_gate_smoke ...
```

## Extension notes

When adding new launcher fields, update command construction and smoke coverage together. Defaults should remain usable after a fresh PC startup: explicit repo dir, request file, Python path, output dirs and profile.
