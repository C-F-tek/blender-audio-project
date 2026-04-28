# AI Repository Manifest

## Purpose

This document gives AI assistants, local LLM tools, and automated reviewers a compact technical map of the repository.

For machine-readable metadata, see:

```text
indexAI/ai_manifest.json
```

## Repository identity

| Field | Value |
|---|---|
| Name | `blender-audio-project` |
| Default branch | `master` |
| Main language | Python |
| Runtime target | Blender Python API |
| Domain | Audio-reactive 3D visual generation |
| License | MIT |
| Maintainer | Carmine Faiola |

## Primary goals

1. Convert audio analysis data into usable technical summaries.
2. Generate and refine Blender Python visual packages.
3. Keep AI-generated scripts reviewable and traceable.
4. Preserve high-quality reference packages such as `Scripting/v61b/`.
5. Support future local AI/NPU/GPU-assisted review and planning.

## Required reading order for AI systems

1. `AGENTS.md`
2. `README.md`
3. `docs/README.md`
4. `docs/MODULE_MAP.md`
5. `docs/DATA_FLOW.md`
6. `docs/QUALITY_GATE.md`
7. `docs/AI_GENERATED_PACKAGE_STANDARD.md`
8. `docs/PACKAGE_CREATION_WORKFLOW.md`
9. `docs/AI_PROMPTS.md`
10. Target package README under `Scripting/`
11. Target source file before editing

## Safe-edit policy

AI systems should:

- inspect current files before editing;
- prefer additive patches;
- avoid broad rewrites;
- avoid deleting generated analysis data;
- keep paths configurable;
- mark unverified runtime assumptions as `not specified`;
- document changed files, tests, risks, and line counts for scripts.

## High-value folders

| Folder | AI relevance |
|---|---|
| `Scripting/v61b/` | Quality reference for complex Blender script structure. |
| `Scripting/_template_audio_reactive_package/` | Template for new audio-reactive packages. |
| `Scripting/shared/` | Destination for stable reusable utilities. |
| `Tools/npu/` | Local AI context generation and review tooling. |
| `Tools/repo_patch_runner/` | Structured patch application tooling. |
| `indexAI/` | AI indexes, manifests, generated plans, and patch artifacts. |
| `docs/` | Technical documentation for developers and AI systems. |

## Patch strategy

Recommended patch categories:

| Category | Strategy |
|---|---|
| Documentation | Update directly when factual and scoped. |
| Blender compatibility | Patch smallest affected function and document tested version. |
| Scene generation | Prefer new package or hotpatch over destructive rewrite. |
| Shared utilities | Add utility first, migrate callers only after validation. |
| AI-generated plan | Store as derived artifact under `indexAI/` or `output/`; do not treat as source of truth. |

## Validation expectations

Minimum validation depends on the change type:

| Change type | Minimum validation |
|---|---|
| Markdown/docs | Link/path sanity check. |
| Generic Python | `python -m py_compile <file>`. |
| Blender Python | Blender launch or Blender background check when available. |
| JSON schema/manifest | JSON parse validation. |
| AI prompt/template | Manual review for target files, constraints, and output format. |

## Output format for AI reports

AI assistants should summarize changes with:

- changed files;
- purpose;
- tests performed;
- untested areas;
- risks;
- line counts for created or modified scripts;
- suggested next actions.
