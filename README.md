# blender-audio-project

Python project for Blender scripting, audio-reactive scene generation, AI-assisted visual package creation, and experimental visual production workflows.

## Author

Carmine Faiola

LinkedIn: https://it.linkedin.com/in/carmine-faiola-12471a183

## License

MIT License. See `LICENSE`.

## Project status

Work in progress. The repository is a technical workspace for Blender scene automation, audio-driven visual production, AI-assisted package generation, and future local AI/NPU/GPU-assisted workflows.

The current default branch is `master`.

## Scope

The project is intended to support:

- audio analysis and compact track summaries;
- Blender Python scripting;
- procedural scene generation;
- audio-reactive animation logic;
- camera, light, fog, material, object, and render tuning;
- JSON-based intermediate data from audio analysis;
- AI-generated or AI-refined Blender script packages;
- versioned package development;
- future local AI-assisted generation and validation.

## Repository structure

| Path | Description |
|---|---|
| `analyze_wav.py` | Audio analysis tool. |
| `build_track_summary.py` | Compact summary builder for analysis data. |
| `normalize_scene_spec.py` | Scene-spec normalization tool. |
| `Scripting/` | Workspace for Blender script packages generated or refined from audio-analysis data. |
| `Scripting/v61b/` | Current quality reference for complex Blender scene scripting. |
| `Scripting/_template_audio_reactive_package/` | Template for future AI-generated audio-reactive Blender packages. |
| `Scripting/shared/` | Target area for reusable non-destructive shared utilities. |
| `Tools/npu/` | Local AI, NPU, context-building, and review tooling. |
| `Tools/git/` | Git automation helper scripts and generated-data push notes. |
| `Tools/repo_patch_runner/` | Structured repository patch tooling. |
| `indexAI/` | AI indexes, manifests, context, and patch artifacts. |
| `docs/` | Technical documentation for humans, developers, and AI agents. |
| `examples/` | Future examples and usage notes. |
| `.github/` | GitHub templates and CI workflow definitions. |

## Documentation index

Start here:

- `AGENTS.md` - operational rules for AI assistants and automated reviewers.
- `CONTRIBUTING.md` - contribution, branch, commit, PR, and testing rules.
- `CODE_OF_CONDUCT.md` - project conduct policy.
- `CHANGELOG.md` - tracked project changes.
- `docs/README.md` - full documentation reading order.
- `docs/PROJECT_OVERVIEW.md` - technical project overview.
- `docs/MODULE_MAP.md` - map of repository modules and folders.
- `docs/DATA_FLOW.md` - data flow from audio files to Blender/render artifacts.
- `docs/AI_GENERATED_PACKAGE_STANDARD.md` - standard for AI-generated Blender packages.
- `docs/PACKAGE_CREATION_WORKFLOW.md` - package creation workflow.
- `docs/QUALITY_GATE.md` - acceptance checklist for code and generated packages.
- `docs/REVIEW_CHECKLIST.md` - manual review checklist for developers and AI systems.
- `docs/AI_PROMPTS.md` - reusable prompt templates for local/remote AI assistants.
- `docs/AI_REPOSITORY_MANIFEST.md` - human-readable AI repository manifest.
- `docs/SHARED_SCRIPTING_UTILITIES.md` - shared utility extraction policy.
- `docs/LOCAL_AI_WORKFLOW.md` - local AI/NPU/GPU workflow notes.
- `docs/PROJECT_AUDIT.md` - audit notes and known improvement areas.
- `indexAI/ai_manifest.json` - machine-readable AI manifest.

## GitHub development entrypoints

| File | Purpose |
|---|---|
| `.github/PULL_REQUEST_TEMPLATE.md` | Standard PR description and review checklist. |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Bug report template. |
| `.github/ISSUE_TEMPLATE/feature_request.md` | Feature request template. |
| `.github/workflows/ci.yml` | Lightweight syntax/documentation CI. |

## Package workflow

New serious Blender packages should start from:

```text
Scripting/_template_audio_reactive_package/
```

and be copied to a project-specific folder such as:

```text
Scripting/track_name_visual_concept/
```

`Scripting/v61b/` remains the reference for richer scene complexity and scripting ambition.

## AI-assisted development workflow

AI systems and developers should follow this order:

1. Read `AGENTS.md` and `docs/README.md`.
2. Read `docs/MODULE_MAP.md`, `docs/DATA_FLOW.md`, and `docs/QUALITY_GATE.md`.
3. Inspect the target package README and target Python files before proposing changes.
4. Prefer small additive patches over destructive rewrites.
5. Keep full analysis JSON files intact unless explicitly asked to regenerate them.
6. Document assumptions, changed files, tests, and risks in the PR.

## Documentation policy

Information that is not confirmed by code or tests must remain marked as `not specified`.

Working code should not be broken for premature refactoring. Shared utilities should be extracted additively and tested before existing packages are migrated.
