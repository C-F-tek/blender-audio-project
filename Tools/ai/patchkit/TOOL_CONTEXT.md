# Tools/ai/patchkit context

## Role

`Tools/ai/patchkit` contains controlled PatchKit helpers used when a reviewed patch bundle/spec needs a deterministic application path.

PatchKit is an apply boundary. It is not a provider proposal generator and not an authorization layer.

It concretizes:

```text
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Responsibilities

- Provide the packaged PatchKit apply command surface.
- Keep patch bundle handling deterministic and reviewable.
- Support dry-run before apply.
- Keep generated patch bundles separate from raw runtime output.
- Refuse or fail safely when anchors/contracts do not match.
- Preserve the distinction between reviewed patch material and source writes.

## Representative commands

Use through the AI dispatcher:

```powershell
python -m Tools.ai apply_patch_bundle --repo-root . --bundle .\patch_specs\<bundle>\bundle.json --dry-run
python -m Tools.ai apply_patch_bundle --repo-root . --bundle .\patch_specs\<bundle>\bundle.json
```

## Correct flow

```text
provider proposal -> evidence only
patch plan -> strategy only
patch candidate/code product -> reviewable payload
PatchKit bundle -> deterministic apply package
dry-run -> contract/anchor check
apply -> explicit reviewed source modification
validation -> proof or failure
commit/PR -> operator/review action
```

## Output role

Outputs are PatchKit execution reports or local apply artifacts, depending on command options and fixture/worktree scope.

Expected artifacts include:

```text
dry-run report
apply report
changed file list
blocked reason
anchor mismatch details
validation notes
```

## Boundary rules

- PatchKit is not a provider proposal generator.
- PatchKit does not make a patch safe merely because a bundle exists.
- Do not use PatchKit to bypass review.
- Do not use PatchKit to invent missing code payloads.
- Do not use PatchKit for automatic commit/push.
- Keep generated bundle artifacts out of Git unless explicitly selected as compact evidence.
- Source writes require explicit operator scope and reviewed bundle content.

## Validation expectations

Validate PatchKit behavior under `Tools/validation/patch_product`:

```powershell
python -m Tools.validation run_patchkit_smoke ...
python -m Tools.validation run_patchkit_bundle_contract_smoke ...
python -m Tools.validation check_patchkit_bundle_contract ...
python -m Tools.validation run_patch_suggestion_bundle_apply_smoke ...
```

## Extension notes

When adding bundle operations or new patch formats, update:

```text
Tools/ai/patchkit
Tools/validation/patch_product
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

Keep apply semantics deterministic and fixture-tested before touching real repo files.