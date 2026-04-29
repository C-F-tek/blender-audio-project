# Project AI Consciousness

## Purpose

This document is the compact operational memory of `blender-audio-project` for AI agents and future development sessions.

It describes what the project is, what must be preserved, what is currently mature, what is risky, and how an AI system should reason before changing files.

## Project identity

`blender-audio-project` is an audio-reactive Blender production workspace.

The project transforms music/audio analysis into Blender visuals through this flow:

```text
audio file
  -> technical analysis JSON
  -> compact track/music context
  -> AI scene brief or scene specification
  -> Blender Python package
  -> rendered frame sequence
  -> FFmpeg encoded video
```

## Current technical state

| Area | Status | Notes |
|---|---|---|
| Root audio tools | usable | `analyze_wav.py`, `build_track_summary.py`, `normalize_scene_spec.py`. |
| `Scripting/v61b/` | stable reference | Current high-quality reference package. Do not destructively refactor. |
| Ready To Jazz package | usable but monolithic | Good production/generation experiment; not yet reusable architecture. |
| `Scripting/shared/` | active foundation | Pure Python helpers exist for path, JSON, image sequence, FFmpeg commands and render profiles; `blender_compat.py` exists but still needs Blender runtime validation. |
| `Tools/validation/` | active foundation | Non-invasive validation scripts exist, including AI pipeline module smoke validation. |
| `Tools/ai/pipeline/` | modularized, pending local dry-run validation | AI artifact pipeline is split into focused modules with a thin entrypoint and machine-readable status marker. |
| `Tools/ai/` and `Tools/npu/` | active pipeline | AI/NPU context, review and artifact generation tooling. |
| `indexAI/` | generated context | Regenerate after structural changes. Do not hand-refactor as source. |
| `patch_specs/` | advanced patch queue | JSON patch specs can be applied manually or by GitHub Action. |
| Documentation | strong | Use docs as project contract. |

## Files and folders to understand first

```text
AGENTS.md
README.md
docs/README.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
docs/AI_EXTERNAL_KNOWLEDGE.md
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
docs/MODULE_MAP.md
docs/DATA_FLOW.md
docs/REFACTORING_AND_REUSE_PLAN.md
docs/PROJECT_STATUS_POINT.md
docs/PATCH_SPEC_WORKFLOW.md
Scripting/README.md
Scripting/v61b/README.md
Scripting/shared/README.md
Tools/validation/README.md
patch_specs/README.md
```

## Runtime preservation rules

These areas are sensitive:

```text
Scripting/v61b/
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/
output full frame-level JSON files
render output paths
FFmpeg command behavior
Blender audio/frame sync behavior
```

Do not modify these casually.

## Current direction

The active architectural direction is:

```text
working package code
  -> additive shared utility
  -> local validation
  -> optional adapter
  -> controlled migration
```

Do not start by rewriting working Blender packages.

## External AI engineering knowledge

OpenAI Harness Engineering and Symphony concepts have been adapted into:

```text
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
docs/AI_EXTERNAL_KNOWLEDGE.md
```

Adopted principles:

```text
AGENTS.md as short index, not encyclopedia
docs/ as versioned project knowledge
validators and dry-runs as mechanical guardrails
Markdown/JSON reports as proof of work
workflow files as operational control plane
small scoped tasks over broad rewrites
execution plans and tech-debt tracking as future drift control
```

Recommended future additions from this knowledge:

```text
WORKFLOW.md
docs/EXECUTION_PLANS/README.md
docs/TECH_DEBT_TRACKER.md
Tools/validation/check_refactor_status_consistency.py
Tools/validation/check_docs_links.py
```

## AI artifact pipeline status

The AI artifact pipeline refactor is marked as:

```text
modular_schedule_complete_pending_local_validation
```

Read before changing pipeline code:

```text
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
Tools/ai/pipeline/refactor_status.py
```

Current module family:

```text
Tools/ai/run_parallel_artifact_pipeline.py
Tools/ai/run_pipeline_dry_run_matrix.py
Tools/ai/pipeline/defaults.py
Tools/ai/pipeline/models.py
Tools/ai/pipeline/runner.py
Tools/ai/pipeline/compat.py
Tools/ai/pipeline/artifact_contracts.py
Tools/ai/pipeline/cli.py
Tools/ai/pipeline/preflight.py
Tools/ai/pipeline/steps.py
Tools/ai/pipeline/scheduler.py
Tools/ai/pipeline/orchestrator.py
Tools/ai/pipeline/schema_report.py
Tools/ai/pipeline/markdown_report.py
Tools/ai/pipeline/guardrail_models.py
Tools/ai/pipeline/remediation.py
Tools/ai/pipeline/refactor_status.py
```

Validation required after pulling latest pipeline changes:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

The dry-run matrix now writes both JSON and Markdown:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix_report.md
```

## Implemented shared foundation

Current shared modules:

| Module | Role |
|---|---|
| `Scripting/shared/path_utils.py` | Project root, file/directory checks, relative path helpers. |
| `Scripting/shared/json_io.py` | UTF-8 JSON read/write and small validation helpers. |
| `Scripting/shared/image_sequence.py` | Frame scan, contiguous sequence detection, FFmpeg pattern generation. |
| `Scripting/shared/ffmpeg_encoder.py` | Package-agnostic FFmpeg command building and dry-run execution helper. |
| `Scripting/shared/render_profiles.py` | Reusable encode profile definitions for YouTube-oriented output. |
| `Scripting/shared/blender_compat.py` | Blender-aware compatibility wrappers for VSE strips, frame range, FPS and node compatibility; not yet adopted by runtime packages. |

Next shared candidates:

```text
Scripting/shared/config_model.py
Scripting/shared/diagnostics.py
```

## Implemented validation foundation

Current validators:

| Tool | Role |
|---|---|
| `Tools/validation/check_python_syntax.py` | Compiles Python files without importing them. |
| `Tools/validation/check_package_structure.py` | Inspects Blender package folders under `Scripting/`. |
| `Tools/validation/check_json_artifacts.py` | Checks JSON parseability without rewriting artifacts. |
| `Tools/validation/check_ai_pipeline_modules.py` | Smoke-checks modular AI pipeline imports, step builders, preflight and report generation without heavy workloads. |

Preferred local validation:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
```

Unattended validation runner:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
```

## Known local validation result

Recent local validation before the final modular AI pipeline split found:

```text
Python syntax: passed
Package structure: passed with non-blocking warnings
JSON artifacts: passed
AI/NPU index generation: passed
```

The current modular AI pipeline split still requires local dry-run validation on the workstation.

Known non-blocking warnings:

```text
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync -> no config.py because it is standalone/monolithic
Scripting/v61b_backgood -> backup folder without README
```

Recommended action:

- optionally exclude backup-style folders from package-structure validation;
- do not force a `config.py` into Ready To Jazz yet.

## Generated index policy

After documentation or structural changes, regenerate:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Expected generated files:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

If only these files changed after regeneration, that is expected.

## Patch-spec capability

The repository contains an advanced patch runner:

```text
Tools/repo_patch_runner/apply_repo_mods.py
patch_specs/inbox/
patch_specs/applied/
.github/workflows/apply_repo_mods.yml
```

Use it for small, mechanical, reviewable edits.

Capabilities:

- dry-run;
- exact replacement;
- regex replacement;
- insert before/after anchor;
- path safety checks;
- before/after content validation;
- optional backup;
- line count summary;
- optional git diff display;
- GitHub Action queue through `patch_specs/inbox/*.json`.

## High-priority next tasks

1. Pull latest remote changes on the workstation.
2. Run Python syntax validation and AI pipeline module smoke validation.
3. Run the AI pipeline dry-run matrix.
4. Regenerate AI/NPU indexes after validation.
5. Commit regenerated AI/NPU indexes only.
6. Review dry-run report `summary`, `schedule` and Markdown output.
7. Continue only after resolving any local validation failures.
8. Consider adding `WORKFLOW.md`, execution plans and a tech debt tracker.

## Avoid now

Do not do these without explicit instruction:

```text
rewrite Scripting/v61b/main_v61b.py
split Ready To Jazz monolithic script
remove v61b_backgood before checking if it contains unique fixes
change Blender render behavior
change final FFmpeg output behavior
add dependencies without validation
modify generated full analysis JSON files
run long Blender renders or GPU generation automatically
change AI pipeline schema-v6 field meanings without local dry-run matrix validation
migrate runtime packages to Scripting/shared/blender_compat.py before Blender validation
```

## Reporting format for AI agents

Every implementation response should include:

```text
changed files
purpose
resulting line count for every created or modified script
validation commands run
validation result
risks
next recommended action
```

## Mental model

The project should be treated as a production pipeline, not a demo.

Correct posture:

```text
stability first
small patches
shared utilities before migration
validation before commit
indexes regenerated after structure changes
proof-of-work reports for agentic work
```
