# Patch specs

Ogni patch-spec contiene:

- target path;
- candidate kind;
- proposed action;
- guardrail;
- `apply_automatically=false`;
- `requires_human_review=true`.

L'applier controllato arriverà solo dopo validazione del planner.
