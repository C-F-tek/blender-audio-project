# Shared Scripting Utilities

## Purpose

This document defines when functionality from a package such as `Scripting/v61b/` should be promoted into shared reusable code under `Scripting/shared/`.

## Principle

Package folders under `Scripting/` can contain project-specific Blender code. However, operational functions that are useful across multiple generated packages should become shared utilities.

This keeps future AI-generated packages cleaner, avoids duplication, and makes local automation easier.

## Critical safety rule

Do not break working package code through premature refactoring.

`Scripting/v61b/` is a working reference model and must not be destructively refactored only to make utilities global.

Shared extraction must be additive first:

1. Create a shared utility under `Scripting/shared/`.
2. Keep the original package file unchanged.
3. Test the shared utility separately.
4. Create an optional wrapper or adapter only after validation.
5. Update the original package only when the replacement has been tested in Blender.

A working duplicated function is better than a broken global abstraction.

## Functions that can become global/shared

The following categories can be extracted when they are reused and when the extraction is safe:

- FFmpeg encoding logic;
- image-sequence encoding logic;
- render profile selection;
- YouTube output presets;
- path resolution utilities;
- configuration loading utilities;
- scene tuning panel base classes;
- hot-update helpers;
- diagnostics helpers;
- Blender compatibility wrappers;
- JSON loading and validation helpers.

## v61b extraction candidates

| Source file | Candidate global function |
|---|---|
| `Scripting/v61b/encode_ffmpeg_v61b.py` | FFmpeg executable discovery, frame sequence detection, audio sync, CPU/GPU profiles. |
| `Scripting/v61b/encode_image_sequence_v61b.py` | Image sequence handling and export logic. |
| `Scripting/v61b/scene_tuning_panel.py` | Runtime profile normalization, render profile application, Blender panel pattern. |
| `Scripting/v61b/hot_update_scene_v61b.py` | Hot scene update workflow. |
| `Scripting/v61b/hotpatch/` | Diagnostics and compatibility patch patterns. |

## Target folder

Shared code should be placed under:

```text
Scripting/shared/
```

Suggested modules:

```text
Scripting/shared/ffmpeg_encoder.py
Scripting/shared/image_sequence_encoder.py
Scripting/shared/render_profiles.py
Scripting/shared/path_utils.py
Scripting/shared/panel_base.py
Scripting/shared/scene_update.py
Scripting/shared/diagnostics.py
```

## Safe migration strategy

1. Identify duplicated or reusable logic in a package.
2. Copy the logic into `Scripting/shared/` with package-neutral names.
3. Remove hardcoded package names and track-specific paths only in the shared copy.
4. Keep the original package script working.
5. Add parameters for package root, config object, and output paths in the shared copy.
6. Test the shared module independently.
7. Add an optional wrapper in a new package that calls the shared utility.
8. Only after successful Blender tests, consider updating existing packages.
9. Never perform broad refactoring in the same step as utility extraction.

## AI rules

- Do not move code out of `v61b` destructively.
- Do not refactor working scripts only for aesthetic reasons.
- Prefer non-breaking extraction: add shared module first, keep current consumers unchanged.
- New packages should check `Scripting/shared/` before duplicating encoding, render, path, or panel code.
- Existing packages should be migrated only after explicit validation.
- If code is tied to object names or materials of one scene, keep it package-specific.
- If code only depends on configuration and paths, it can be made shared, but only through additive extraction.

## Current status

The shared folder exists as a target area. Full code extraction is not completed yet. Existing working package code should remain untouched unless a tested migration is explicitly requested.
