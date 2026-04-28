# Review Checklist

## Purpose

This checklist is used for manual review, AI-assisted review, and pull request validation.

## Repository-level checks

- [ ] The target branch is correct. Current default branch: `master`.
- [ ] The change is scoped and reviewable.
- [ ] The change does not delete required generated data.
- [ ] The change does not rewrite unrelated packages.
- [ ] Documentation was updated when behavior changed.
- [ ] `CHANGELOG.md` was updated for notable changes.

## Python checks

- [ ] Python files compile with `python -m py_compile` where applicable.
- [ ] Functions have clear responsibilities.
- [ ] Paths are configurable.
- [ ] New external dependencies are documented.
- [ ] Workstation-only absolute paths are avoided in reusable code.

## Blender checks

- [ ] Blender API usage is compatible with the intended Blender version, or compatibility is marked as `not specified`.
- [ ] Removed or renamed node types are avoided or handled through fallback logic.
- [ ] Scene setup does not rely on hidden manual state unless documented.
- [ ] Audio strip loading is included when the package requires audio playback.
- [ ] Render settings are documented when changed.

## AI-generated package checks

- [ ] `AGENTS.md` was followed.
- [ ] `docs/AI_GENERATED_PACKAGE_STANDARD.md` was followed.
- [ ] `docs/QUALITY_GATE.md` was followed.
- [ ] Target package README exists.
- [ ] Target script was inspected before editing.
- [ ] Full analysis JSON files were not overwritten.
- [ ] Assumptions are marked as `not specified` when unverified.
- [ ] Resulting line counts are reported for created or modified scripts.

## Documentation checks

- [ ] Links and paths are current.
- [ ] The documentation distinguishes confirmed facts from assumptions.
- [ ] New files are listed in `README.md` or `docs/README.md` when useful.
- [ ] AI-facing documents point to `indexAI/ai_manifest.json` where relevant.

## PR checks

- [ ] PR uses `.github/PULL_REQUEST_TEMPLATE.md`.
- [ ] PR describes why the change is needed.
- [ ] PR lists main files changed.
- [ ] PR lists tests performed.
- [ ] PR lists untested areas and risks.
