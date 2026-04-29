# Documentation

This folder contains the stable technical documentation for `blender-audio-project`.

The documentation is intended for both human developers and AI agents. It should describe the current repository structure, the expected workflow, safe modification rules, and the roadmap for refactoring the project into reusable components.

## Recommended reading order

1. `../AGENTS.md`
2. `../WORKFLOW.md`
3. `PROJECT_OVERVIEW.md`
4. `PROJECT_AI_CONSCIOUSNESS.md`
5. `AI_ONBOARDING.md`
6. `AI_PIPELINE_REFACTOR_STATUS.md`
7. `AI_PIPELINE_ARCHITECTURE.md`
8. `GITHUB_LOCAL_VALIDATION_WORKFLOW.md`
9. `AI_EXTERNAL_KNOWLEDGE.md`
10. `OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md`
11. `EXECUTION_PLANS/README.md`
12. `TECH_DEBT_TRACKER.md`
13. `MODULE_MAP.md`
14. `DATA_FLOW.md`
15. `REFACTORING_AND_REUSE_PLAN.md`
16. `PATCH_SPEC_WORKFLOW.md`
17. `SHARED_SCRIPTING_UTILITIES.md`
18. `BLENDER_SCRIPT_ENTRYPOINTS.md`
19. `AI_GENERATED_PACKAGE_STANDARD.md`
20. `PACKAGE_CREATION_WORKFLOW.md`
21. `QUALITY_GATE.md`
22. `AUDIO_ANALYSIS_PIPELINE.md`
23. `JSON_SCHEMAS.md`
24. `RENDER_WORKFLOW.md`
25. `FFMPEG_WORKFLOW.md`
26. `LOCAL_AI_WORKFLOW.md`
27. `NPU_GPU_PARALLELISM_PLAN.md`
28. `AI_PIPELINE_OPTIMIZATION.md`
29. `INSTALLATION.md`
30. `USAGE.md`
31. `COMPATIBILITY.md`
32. `KNOWN_LIMITATIONS.md`
33. `DEVELOPER_GUIDE.md`
34. `PROJECT_AUDIT.md`
35. `PROJECT_STATUS_POINT.md`

## Documentation groups

### Project context

| File | Purpose |
|---|---|
| `../WORKFLOW.md` | Root operational workflow for humans and AI agents. |
| `PROJECT_OVERVIEW.md` | High-level project identity and goals. |
| `PROJECT_AI_CONSCIOUSNESS.md` | Compact operational memory for AI agents and future development sessions. |
| `AI_ONBOARDING.md` | First-session guide for AI agents entering the project. |
| `AI_PIPELINE_REFACTOR_STATUS.md` | Stable marker for the current modular AI pipeline refactor state and validation requirements. |
| `AI_PIPELINE_ARCHITECTURE.md` | Map of the modular AI artifact pipeline, module responsibilities and validation commands. |
| `GITHUB_LOCAL_VALIDATION_WORKFLOW.md` | Local Git/GitHub validation, index regeneration, commit and push workflow after AI-assisted changes. |
| `AI_EXTERNAL_KNOWLEDGE.md` | External AI-coding knowledge adapted to this project. |
| `OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md` | OpenAI Harness Engineering and Symphony concepts adapted to this repository. |
| `EXECUTION_PLANS/README.md` | Durable task-plan workflow for multi-step work. |
| `TECH_DEBT_TRACKER.md` | Known technical debt, status and recommended remediation. |
| `MODULE_MAP.md` | Repository areas, source packages, generated artifacts and navigation order. |
| `DATA_FLOW.md` | Data movement from audio input to Blender scene and encoded video. |
| `PROJECT_STATUS_POINT.md` | Current state checkpoint and next recommended tasks. |
| `PROJECT_AUDIT.md` | Current technical assessment, maturity, risks and next actions. |
| `DEVELOPER_GUIDE.md` | Practical workflow for development and review. |

### Refactoring and reuse

| File | Purpose |
|---|---|
| `REFACTORING_AND_REUSE_PLAN.md` | Main roadmap for encapsulation, shared utilities and non-destructive migration. |
| `SHARED_SCRIPTING_UTILITIES.md` | Policy and target modules for reusable package-agnostic code. |
| `AI_PIPELINE_ARCHITECTURE.md` | Current modularization map for the AI artifact pipeline. |
| `AI_PIPELINE_REFACTOR_STATUS.md` | Current refactor status marker to avoid inconsistent AI interpretation. |
| `OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md` | External agent-first engineering patterns mapped into project actions. |
| `EXECUTION_PLANS/README.md` | Plan format for larger refactors or migration work. |
| `TECH_DEBT_TRACKER.md` | Queue of known debt to avoid repeated rediscovery. |
| `MODULE_MAP.md` | Source-to-target mapping for package modules and extraction candidates. |

### Patch, GitHub and automation workflow

| File | Purpose |
|---|---|
| `../WORKFLOW.md` | End-to-end operational flow from task to proof of work. |
| `PATCH_SPEC_WORKFLOW.md` | Safe JSON patch-spec workflow, dry-run/apply commands, diff display and GitHub Action queue. |
| `GITHUB_LOCAL_VALIDATION_WORKFLOW.md` | Local pull/validate/dry-run/index-regeneration/commit/push workflow. |
| `INDEX_REGEN_POLICY.md` | Regeneration policy for AI indexes and manifests. |
| `../patch_specs/README.md` | Patch spec inbox/applied folder convention. |
| `../Tools/validation/README.md` | Local non-invasive validation commands. |

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
2. read `../WORKFLOW.md`;
3. read this documentation index;
4. read `PROJECT_AI_CONSCIOUSNESS.md`;
5. read `AI_ONBOARDING.md`;
6. read `AI_PIPELINE_REFACTOR_STATUS.md`;
7. read `AI_PIPELINE_ARCHITECTURE.md`;
8. read `GITHUB_LOCAL_VALIDATION_WORKFLOW.md`;
9. read `AI_EXTERNAL_KNOWLEDGE.md`;
10. read `OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md`;
11. read `EXECUTION_PLANS/README.md`;
12. read `TECH_DEBT_TRACKER.md`;
13. read `MODULE_MAP.md`;
14. read `DATA_FLOW.md`;
15. read `REFACTORING_AND_REUSE_PLAN.md`;
16. read `PATCH_SPEC_WORKFLOW.md` when preparing mechanical edits;
17. read `QUALITY_GATE.md`;
18. read the README of the target package;
19. inspect the target source file before producing a patch.

## Refactoring note

The repository should move toward reusable modules, but not by breaking working packages. Shared utility extraction must be additive first, then validated, then adopted by package adapters.
