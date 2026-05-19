# Tools/repo_patch_runner context

## Role

`Tools/repo_patch_runner` contains controlled repository patch runner utilities. It is for deterministic, reviewed patch operations, not for free-form source rewriting.

Canonical invocation:

```powershell
python -m Tools.repo_patch_runner <tool> [tool args...]
```

The source of truth for public patch-runner tools is `Tools/repo_patch_runner/dispatch.py`.

## Current tools

```text
apply_repo_mods
```

The tool resolves to `Tools.repo_patch_runner.apply_repo_mods.cli:main`.

## Expected use

Use this area when a patch bundle or repository modification spec has already been produced, reviewed and is ready for controlled application.

Correct flow:

```text
proposal/code product -> reviewed patch/spec -> patch runner fixture/test -> explicit apply -> validation -> targeted commit
```

Do not use this area to turn provider prose directly into source writes.

## Safety model

Patch runner tools must:

- find the repository root from `.git` when possible;
- print branch and status before applying changes;
- fail if expected anchors do not match;
- avoid touching runtime artifacts and databases;
- avoid committing by themselves;
- keep backups or reversible evidence when applying controlled replacements;
- validate with `git diff --check` and relevant smoke tests after apply.

## Relationship to code products

`CODE_PRODUCT_FULL_PATCH.md` and patch candidates must be analyzed before application. Valid cases include:

```text
real diff/code present -> review/apply candidate
already integrated -> no-op
verified target with no diff -> evidence only
missing/truncated payload -> manual review/block
```

## Safe extension rules

- Add new runners only when a spec format is stable.
- Keep apply logic deterministic and small.
- Never bypass source allowlists or guardrails.
- Do not add automatic commit/push behavior here.
