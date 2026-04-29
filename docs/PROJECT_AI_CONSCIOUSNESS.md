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
| `Scripting/shared/` | active foundation | First pure Python helpers exist: path, JSON, image sequence. |
| `Tools/validation/` | active foundation | Non-invasive validation scripts exist. |
| `Tools/ai/` and `Tools/npu/` | active pipeline | AI/NPU context, review and artifact generation tooling. |
| `indexAI/` | generated context | Regenerate after structural changes. Do not hand-refactor as source. |
| `patch_specs/` | advanced patch queue | JSON patch specs can be applied manually or by GitHub Action. |
| Documentation | strong | Use docs as project contract. |

## Files and folders to understand first

```text
AGENTS.md
README.md
docs/README.md
docs/MODULE_MAP.md
docs/DATA_FLOW.md
docs/REFACTORING_AND_REUSE_PLAN.md
docs/PROJECT_STATUS_POINT.md
docs/AI_EXTERNAL_KNOWLEDGE.md
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

## Implemented shared foundation

Current shared modules:

| Module | Role |
|---|---|
| `Scripting/shared/path_utils.py` | Project root, file/directory checks, relative path helpers. |
| `Scripting/shared/json_io.py` | UTF-8 JSON read/write and small validation helpers. |
| `Scripting/shared/image_sequence.py` | Frame scan, contiguous sequence detection, FFmpeg pattern generation. |

Next shared candidates:

```text
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/render_profiles.py
Scripting/shared/blender_compat.py
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

Preferred local validation:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

## Known local validation result

Recent local validation found:

```text
Python syntax: passed
Package structure: passed with non-blocking warnings
JSON artifacts: passed
AI/NPU index generation: passed
```

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

1. Commit regenerated AI/NPU indexes after validation.
2. Add `.gitattributes` line-ending policy in a separate commit.
3. Update docs index to include new AI knowledge and project consciousness files.
4. Implement `Scripting/shared/ffmpeg_encoder.py` and `render_profiles.py`.
5. Add a small validation tweak to ignore backup folders like `v61b_backgood`.
6. Later: add `Scripting/shared/blender_compat.py`.
7. Later: split large AI/NPU orchestrator modules.

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
```

## Reporting format for AI agents

Every implementation response should include:

```text
changed files
purpose
resulting line counts for scripts
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
```
