# Documentation

This folder contains the stable technical documentation for `blender-audio-project`.

The documentation is intended for both human developers and AI agents. It should describe the current repository structure, the expected workflow, safe modification rules, and the roadmap for refactoring the project into reusable components.

## Recommended reading order

1. `../AGENTS.md`
2. `PROJECT_OVERVIEW.md`
3. `MODULE_MAP.md`
4. `DATA_FLOW.md`
5. `REFACTORING_AND_REUSE_PLAN.md`
6. `SHARED_SCRIPTING_UTILITIES.md`
7. `BLENDER_SCRIPT_ENTRYPOINTS.md`
8. `AI_GENERATED_PACKAGE_STANDARD.md`
9. `PACKAGE_CREATION_WORKFLOW.md`
10. `QUALITY_GATE.md`
11. `AUDIO_ANALYSIS_PIPELINE.md`
12. `JSON_SCHEMAS.md`
13. `RENDER_WORKFLOW.md`
14. `FFMPEG_WORKFLOW.md`
15. `LOCAL_AI_WORKFLOW.md`
16. `NPU_GPU_PARALLELISM_PLAN.md`
17. `AI_PIPELINE_OPTIMIZATION.md`
18. `INSTALLATION.md`
19. `USAGE.md`
20. `COMPATIBILITY.md`
21. `KNOWN_LIMITATIONS.md`
22. `DEVELOPER_GUIDE.md`
23. `PROJECT_AUDIT.md`

## Documentation groups

### Project context

| File | Purpose |
|---|---|
| `PROJECT_OVERVIEW.md` | High-level project identity and goals. |
| `MODULE_MAP.md` | Repository areas, source packages, generated artifacts and navigation order. |
| `DATA_FLOW.md` | Data movement from audio input to Blender scene and encoded video. |
| `PROJECT_AUDIT.md` | Current technical assessment, maturity, risks and next actions. |
| `DEVELOPER_GUIDE.md` | Practical workflow for development and review. |

### Refactoring and reuse

| File | Purpose |
|---|---|
| `REFACTORING_AND_REUSE_PLAN.md` | Main roadmap for encapsulation, shared utilities and non-destructive migration. |
| `SHARED_SCRIPTING_UTILITIES.md` | Policy and target modules for reusable package-agnostic code. |
| `MODULE_MAP.md` | Source-to-target mapping for package modules and extraction candidates. |

### AI-generated package workflow

| File | Purpose |
|---|---|
| `AI_GENERATED_PACKAGE_STANDARD.md` | Expected structure of generated Blender packages. |
| `PACKAGE_CREATION_WORKFLOW.md` | Operational workflow for creating future packages. |
| `QUALITY_GATE.md` | Acceptance checks before a package is considered usable. |
| `LOCAL_AI_WORKFLOW.md` | Direction for local AI/NPU/GPU-assisted generation and review. |
| `AI_PIPELINE_OPTIMIZATION.md` | Optimization notes for AI artifact production. |
| `NPU_GPU_PARALLELISM_PLAN.md` | Parallel execution plan for NPU and GPU workloads. |

### Blender workflow

| File | Purpose |
|---|---|
| `BLENDER_SCRIPT_ENTRYPOINTS.md` | Known script entry points and execution notes. |
| `AUDIO_ANALYSIS_PIPELINE.md` | Audio analysis workflow and generated data. |
| `RENDER_WORKFLOW.md` | Blender rendering workflow. |
| `FFMPEG_WORKFLOW.md` | Final video encoding workflow. |
| `COMPATIBILITY.md` | Known compatibility notes, especially Blender-version-sensitive behavior. |

### Data and schemas

| File | Purpose |
|---|---|
| `JSON_SCHEMAS.md` | Current JSON schema notes and missing formal contracts. |
| `AI_ARTIFACT_SCHEMAS.md` | AI artifact schema notes. |
| `AI_CHUNKING_STRATEGY.md` | Chunking strategy for AI-readable project context. |
| `INDEX_REGEN_POLICY.md` | Regeneration policy for AI indexes and manifests. |

### Setup and operations

| File | Purpose |
|---|---|
| `INSTALLATION.md` | Environment setup notes. |
| `USAGE.md` | Common usage notes. |
| `KNOWN_LIMITATIONS.md` | Known gaps and incomplete areas. |
| `LOCAL_WORKSTATION_TARGET.md` | Local workstation target notes. |

## Documentation style

Use direct, explicit documentation.

Rules:

- Mark unverified information as `not specified`.
- Prefer tables for file maps and contracts.
- Keep package-specific instructions near the package.
- Keep global project rules in `docs/` and `AGENTS.md`.
- Do not document generated artifacts as manually maintained source.
- Update this index when adding a new stable documentation file.

## AI usage

AI systems should treat this folder as the contract layer for the repository.

Before editing code, an AI system should:

1. read `../AGENTS.md`;
2. read this documentation index;
3. read `MODULE_MAP.md`;
4. read `DATA_FLOW.md`;
5. read `REFACTORING_AND_REUSE_PLAN.md`;
6. read `QUALITY_GATE.md`;
7. read the README of the target package;
8. inspect the target source file before producing a patch.

## Refactoring note

The repository should move toward reusable modules, but not by breaking working packages. Shared utility extraction must be additive first, then validated, then adopted by package adapters.
