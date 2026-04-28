# Shared Scripting Utilities

## Purpose

This document defines when functionality from a package such as `Scripting/v61b/` should be promoted into shared reusable code under `Scripting/shared/`.

## Principle

Package folders under `Scripting/` can contain project-specific Blender code. However, operational functions that are useful across multiple generated packages should become shared utilities.

This keeps future AI-generated packages cleaner, avoids duplication, and makes local automation easier.

## Functions that should become global/shared

The following categories should be extracted when they are reused:

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

## Migration strategy

1. Identify duplicated or reusable logic in a package.
2. Copy the logic into `Scripting/shared/` with package-neutral names.
3. Remove hardcoded package names and track-specific paths.
4. Add parameters for package root, config object, and output paths.
5. Keep the original package script working.
6. Add a wrapper in the package that calls the shared utility.
7. Test inside Blender.
8. Update package README and this document if behavior changes.

## AI rules

- Do not move code out of `v61b` destructively without testing.
- Prefer non-breaking extraction: add shared module first, then update consumers.
- New packages should check `Scripting/shared/` before duplicating encoding, render, path, or panel code.
- If code is tied to object names or materials of one scene, keep it package-specific.
- If code only depends on configuration and paths, make it shared.

## Current status

The shared folder exists as a target area. Full code extraction is not completed yet.
