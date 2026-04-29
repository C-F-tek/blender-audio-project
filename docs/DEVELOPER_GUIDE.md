# Developer Guide

## Purpose

This guide defines a practical development workflow for `blender-audio-project`.

The repository contains working Blender packages, generated AI artifacts, local AI/NPU tooling and documentation. Development should prioritize small, traceable changes that do not break existing render workflows.

## Recommended workflow

1. Pull the latest `master` branch.
2. Read `README.md` and `AGENTS.md`.
3. Read `docs/README.md`, `docs/PROJECT_AI_CONSCIOUSNESS.md` and `docs/AI_ONBOARDING.md`.
4. Read `docs/AI_PIPELINE_REFACTOR_STATUS.md` and `docs/AI_PIPELINE_ARCHITECTURE.md` before changing AI pipeline code.
5. Read `docs/MODULE_MAP.md` and `docs/DATA_FLOW.md`.
6. Read `docs/REFACTORING_AND_REUSE_PLAN.md` when touching reusable logic.
7. Identify the target area: root tool, Blender package, shared utility, AI/NPU tool, generated artifact or documentation.
8. Inspect the target file before editing.
9. Make a focused change.
10. Run the smallest relevant validation.
11. Test inside Blender when the change touches Blender runtime behavior.
12. Document assumptions, results, risks and line counts for scripts.
13. Commit with a clear message.

## Working with Blender scripts

Rules:

- Keep local paths configurable.
- Add comments around Blender API compatibility-sensitive code.
- Prefer functions with clear responsibility.
- Avoid global side effects where a parameter or config object is practical.
- Do not destructively refactor working packages only for style.
- Keep object creation, material creation, animation, render settings and encoding separated where possible.
- Isolate Blender-version compatibility in helper functions.

## Working with shared utilities

Shared utilities live under:

```text
Scripting/shared/
```

Use shared utilities for reusable operational behavior:

- path resolution;
- JSON loading/writing;
- input validation;
- Blender API compatibility wrappers;
- image-sequence scanning;
- FFmpeg command building;
- render profile definitions;
- diagnostics;
- hotpatch support;
- scene registry patterns.

Do not migrate an existing working package to a new shared utility until the utility has been tested.

Safe order:

```text
create shared utility
  -> validate utility
  -> add optional package adapter
  -> test package
  -> migrate one call site
```

## Working with the AI artifact pipeline

The AI artifact pipeline entrypoint is:

```text
Tools/ai/run_parallel_artifact_pipeline.py
```

It should remain thin. Implementation belongs under:

```text
Tools/ai/pipeline/
```

Current status marker:

```text
modular_schedule_complete_pending_local_validation
```

Read before editing:

```text
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
Tools/ai/pipeline/refactor_status.py
```

Module responsibilities:

| Module | Role |
|---|---|
| `defaults.py` | Central constants and defaults. |
| `models.py` | Pipeline dataclasses and lane enum. |
| `runner.py` | Low-level subprocess execution. |
| `compat.py` | Schema-v6 compatibility adapters. |
| `artifact_contracts.py` | Expected artifacts and planned outputs. |
| `cli.py` | CLI parser. |
| `preflight.py` | Pre-run checks. |
| `steps.py` | Step and command builders. |
| `scheduler.py` | Serial/parallel scheduling policy. |
| `orchestrator.py` | Concrete serial/parallel execution helpers. |
| `schema_report.py` | Report generation. |
| `guardrail_models.py` | Typed guardrail queue models. |
| `remediation.py` | Auto-safe remediation loop. |
| `refactor_status.py` | Machine-readable status marker. |

AI pipeline validation:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

Important rule: do not change schema-v6 field meanings without running the dry-run matrix locally.

## Working with root tools

Root scripts such as `analyze_wav.py`, `build_track_summary.py` and `normalize_scene_spec.py` should gradually move toward this shape:

```text
importable service function
  -> CLI wrapper
  -> explicit input/output paths
  -> predictable JSON output
```

Do not break the existing command-line behavior during this transition.

## Working with AI/NPU tooling

For files under `Tools/npu/`:

- keep provider/runtime code separate from prompts;
- keep prompts separate from validators;
- keep generated artifacts separate from hand-maintained code;
- preserve deterministic fallbacks;
- keep large model outputs out of source modules;
- document every expected input/output file.

Longer-term target:

```text
Tools/npu/pipeline/
  config.py
  context_builder.py
  prompts.py
  providers.py
  validators.py
  artifact_writer.py
  runner.py
```

## Working with generated data

- Do not commit heavy render outputs unless explicitly required.
- Do not overwrite full frame-by-frame analysis JSON files without explicit instruction.
- Keep compact summaries separate from full data.
- Keep output paths configurable.
- Treat `indexAI/` as generated context unless a specific source file inside it is intentionally curated.
- Regenerate indexes after major structural changes.

## Working with README and documentation files

When code structure changes, update the nearest documentation:

| Change | Documentation to update |
|---|---|
| New package under `Scripting/` | package `README.md`, `Scripting/README.md`, `docs/MODULE_MAP.md` |
| New shared utility | `Scripting/shared/README.md`, `docs/SHARED_SCRIPTING_UTILITIES.md`, `docs/REFACTORING_AND_REUSE_PLAN.md` |
| New AI pipeline module | `docs/AI_PIPELINE_ARCHITECTURE.md`, `docs/AI_PIPELINE_REFACTOR_STATUS.md`, `docs/PROJECT_AI_CONSCIOUSNESS.md` |
| New entry point | `docs/BLENDER_SCRIPT_ENTRYPOINTS.md` or the closest workflow document. |
| New JSON contract | `docs/JSON_SCHEMAS.md` |
| New render or encode workflow | `docs/RENDER_WORKFLOW.md`, `docs/FFMPEG_WORKFLOW.md` |
| New AI/NPU workflow | `docs/LOCAL_AI_WORKFLOW.md`, `docs/AI_PIPELINE_OPTIMIZATION.md` |
| New validation workflow | `docs/QUALITY_GATE.md`, `Tools/validation/README.md` |

## Commit style

Use concise commit messages:

```text
docs: refresh repository readmes
docs: add refactoring and reuse plan
feat(shared): add json io helpers
feat(shared): add ffmpeg profile builder
feat(ai): add artifact pipeline dry-run matrix
refactor(ai): slim artifact pipeline orchestrator
refactor(npu): split prompt builders
fix(blender): add node compatibility fallback
test: add package structure validation
```

## Test notes

When reporting a change, include:

- changed files;
- reason for the change;
- Blender version tested, when relevant;
- command or action used;
- result;
- line count for scripts created or modified;
- risks or missing validation.

## Minimal validation checklist

| Change type | Minimum validation |
|---|---|
| Markdown/docs only | Review paths and links. |
| Pure Python utility | `python .\Tools\validation\check_python_syntax.py --repo-root .`. |
| Root CLI | Run with a small input or dry-run mode if available. |
| AI artifact pipeline | `check_ai_pipeline_modules.py` plus `run_pipeline_dry_run_matrix.py`. |
| Blender module | Import/run inside Blender, or run a controlled manual test. |
| FFmpeg utility | Print command and run a short encode test. |
| NPU/Ollama pipeline | Dry-run or deterministic fallback path. |
| Generated package | Open target package, verify inputs, frame range, audio strip and output path. |

## Standard local validation block

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## Not specified

- Formal release automation.
- Branch protection policy.
- Complete Blender headless CI.
- Full JSON schema enforcement for every artifact.
