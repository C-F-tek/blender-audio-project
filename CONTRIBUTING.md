# Contributing

This repository is maintained by Carmine Faiola and is currently a work-in-progress Blender/Python project for audio-reactive visual generation, Blender scene automation, and AI-assisted package development.

## Maintainer

- Carmine Faiola
- LinkedIn: https://it.linkedin.com/in/carmine-faiola-12471a183

## Contribution principles

- Keep changes focused and reviewable.
- Prefer small pull requests over broad rewrites.
- Document assumptions explicitly.
- Preserve existing workflows unless a change explicitly replaces them.
- Do not remove generated data or project assets without a clear reason.
- Keep local workstation paths configurable when code is intended to be reusable.
- Mark unverified information as `not specified`.

## Default branch

The current default branch is:

```text
master
```

Use `master` as the PR base unless the repository configuration changes.

## Branch naming

Use descriptive branches:

```text
feature/<short-topic>
fix/<short-topic>
docs/<short-topic>
refactor/<short-topic>
compat/<short-topic>
```

Examples:

```text
docs/ai-friendly-github-dev-guide
fix/blender-51-musgrave-node
feature/audio-reactive-camera-rig
compat/blender-51-render-settings
```

## Development workflow

1. Pull the latest `master` branch.
2. Create a focused branch.
3. Read `README.md`, `AGENTS.md`, and `docs/README.md`.
4. Inspect the relevant package README and target files before editing.
5. Make the smallest safe change that solves the issue.
6. Run available syntax checks or targeted scripts.
7. Test with Blender when the change touches Blender runtime behavior.
8. Update documentation when behavior, workflow, paths, or assumptions change.
9. Open a pull request using `.github/PULL_REQUEST_TEMPLATE.md`.

## Python and Blender notes

- Prefer readable Blender Python code.
- Keep paths configurable.
- Avoid workstation-only absolute paths in reusable modules.
- Mark untested Blender versions as `not specified`.
- Add comments around Blender API compatibility-sensitive code.
- Do not use removed Blender node types without a compatibility fallback.
- Keep generated packages self-contained unless a shared utility is already stable.

## AI-assisted contribution rules

AI-generated or AI-refined changes must follow the same review process as manual changes.

Before applying AI-generated code:

1. Read `AGENTS.md`.
2. Read `docs/AI_REPOSITORY_MANIFEST.md` and `indexAI/ai_manifest.json` when available.
3. Validate target files exist.
4. Keep full analysis JSON files intact unless regeneration is explicitly requested.
5. Prefer additive hotpatches or small module-level changes.
6. Report changed files, risks, tests, and assumptions.
7. Report line counts for scripts created or modified.

## Pull request requirements

A PR should include:

- purpose of the change;
- files changed;
- related issue, if present;
- Blender version tested, or `not specified`;
- commands or manual actions used for testing;
- risk notes;
- follow-up work, if needed.

## Review checklist

Before requesting review:

- [ ] The change is focused.
- [ ] Target files were inspected before editing.
- [ ] No required generated data was deleted.
- [ ] Documentation was updated where needed.
- [ ] Python files compile with `python -m py_compile` where applicable.
- [ ] Blender-specific code was tested in Blender, or the missing test is documented.
- [ ] AI-generated assumptions are marked as `not specified` when unverified.
- [ ] `CHANGELOG.md` was updated when the change is notable.

## Commit message examples

Use concise commit messages in this style:

```text
docs: add project overview
fix: replace removed Blender node type
feat: add configurable render output path
refactor: split material setup helpers
ci: add lightweight syntax checks
```

## Release notes

Formal release automation is not specified yet. Until a release process is defined:

- keep notable changes in `CHANGELOG.md`;
- group documentation-only changes separately when practical;
- do not tag a release without a clear versioning decision.

## Not specified

Formal formatter, test runner, release automation, and branch protection policy are not fully specified yet.
