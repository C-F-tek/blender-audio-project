# Contributing

This repository is maintained by Carmine Faiola and is currently a work-in-progress Blender/Python project.

## Maintainer

- Carmine Faiola
- LinkedIn: https://it.linkedin.com/in/carmine-faiola-12471a183

## Contribution principles

- Keep changes focused.
- Prefer small pull requests.
- Document assumptions.
- Preserve existing workflows unless a change explicitly replaces them.
- Do not remove generated data or project assets without a clear reason.

## Development workflow

1. Create a branch.
2. Make focused changes.
3. Test with Blender when possible.
4. Update documentation when behavior changes.
5. Open a pull request using the provided template.

## Python and Blender notes

- Prefer readable Blender Python code.
- Keep paths configurable.
- Avoid workstation-only absolute paths in reusable modules.
- Mark untested Blender versions as `not specified`.

## Commit message examples

```text
docs: add project overview
fix: replace removed Blender node type
feat: add configurable render output path
refactor: split material setup helpers
```

## Not specified

Formal coding standards, formatter, test runner, and release process are not specified yet.
